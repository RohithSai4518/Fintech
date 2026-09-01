"""
Fintech Financial Reporting & Analytics Service
Generates GAAP/IFRS-compliant financial statements:
- Balance Sheet (Assets = Liabilities + Equity)
- Income Statement / P&L (Net Income = Revenue - Expenses)
- Trial Balance (Total Debits == Total Credits)
- Operational Analytics & KPIs
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

from backend.core.database import DatabaseManager


class ReportingService:
    """Enterprise reporting engine providing audit trails, financial statements, and analytics."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_trial_balance(self) -> Dict[str, Any]:
        """
        Calculates the Trial Balance across all ledger accounts.
        Verifies that Sum(Debits) == Sum(Credits).
        """
        rows = self.db.query_all(
            """
            SELECT 
                a.id, a.account_number, a.name, a.account_type, a.currency,
                SUM(CASE WHEN jel.direction = 'DEBIT' THEN jel.amount ELSE 0 END) as total_debit,
                SUM(CASE WHEN jel.direction = 'CREDIT' THEN jel.amount ELSE 0 END) as total_credit
            FROM accounts a
            LEFT JOIN journal_entry_lines jel ON a.id = jel.account_id
            GROUP BY a.id, a.account_number, a.name, a.account_type, a.currency
            ORDER BY a.account_type, a.account_number;
            """
        )

        total_system_debits = 0.0
        total_system_credits = 0.0
        accounts_summary = []

        for r in rows:
            debit = round(r["total_debit"] or 0.0, 2)
            credit = round(r["total_credit"] or 0.0, 2)
            total_system_debits += debit
            total_system_credits += credit

            accounts_summary.append({
                "id": r["id"],
                "account_number": r["account_number"],
                "name": r["name"],
                "account_type": r["account_type"],
                "currency": r["currency"],
                "debit": debit,
                "credit": credit
            })

        total_system_debits = round(total_system_debits, 2)
        total_system_credits = round(total_system_credits, 2)
        is_balanced = abs(total_system_debits - total_system_credits) < 0.01

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "is_balanced": is_balanced,
            "total_debits": total_system_debits,
            "total_credits": total_system_credits,
            "difference": round(abs(total_system_debits - total_system_credits), 2),
            "accounts": accounts_summary
        }

    def get_balance_sheet(self) -> Dict[str, Any]:
        """
        Generates Balance Sheet statement:
        Assets, Liabilities, Equity.
        """
        accounts = self.db.query_all("SELECT * FROM accounts WHERE is_active = 1;")
        
        assets: List[Dict[str, Any]] = []
        liabilities: List[Dict[str, Any]] = []
        equity: List[Dict[str, Any]] = []

        total_assets = 0.0
        total_liabilities = 0.0
        total_equity = 0.0

        for acc in accounts:
            bal = round(acc["balance"], 2)
            item = {
                "account_id": acc["id"],
                "account_number": acc["account_number"],
                "name": acc["name"],
                "subtype": acc["account_subtype"],
                "currency": acc["currency"],
                "balance": bal
            }

            if acc["account_type"] == "ASSET":
                assets.append(item)
                total_assets += bal
            elif acc["account_type"] == "LIABILITY":
                liabilities.append(item)
                total_liabilities += bal
            elif acc["account_type"] == "EQUITY":
                equity.append(item)
                total_equity += bal

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "assets": {
                "items": assets,
                "total": round(total_assets, 2)
            },
            "liabilities": {
                "items": liabilities,
                "total": round(total_liabilities, 2)
            },
            "equity": {
                "items": equity,
                "total": round(total_equity, 2)
            },
            "net_worth": round(total_assets - total_liabilities, 2)
        }

    def get_income_statement(self) -> Dict[str, Any]:
        """
        Generates Income Statement (Profit & Loss / P&L):
        Revenues, Expenses, Net Profit/Loss.
        """
        accounts = self.db.query_all("SELECT * FROM accounts WHERE is_active = 1;")

        revenues: List[Dict[str, Any]] = []
        expenses: List[Dict[str, Any]] = []

        total_revenue = 0.0
        total_expense = 0.0

        for acc in accounts:
            bal = round(acc["balance"], 2)
            item = {
                "account_id": acc["id"],
                "account_number": acc["account_number"],
                "name": acc["name"],
                "subtype": acc["account_subtype"],
                "currency": acc["currency"],
                "amount": bal
            }

            if acc["account_type"] == "REVENUE":
                revenues.append(item)
                total_revenue += bal
            elif acc["account_type"] == "EXPENSE":
                expenses.append(item)
                total_expense += bal

        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "revenues": {
                "items": revenues,
                "total": round(total_revenue, 2)
            },
            "expenses": {
                "items": expenses,
                "total": round(total_expense, 2)
            },
            "net_income": round(total_revenue - total_expense, 2)
        }

    def get_executive_kpis(self) -> Dict[str, Any]:
        """Calculates executive dashboard metrics and transaction volume analytics."""
        acc_count = self.db.query_one("SELECT COUNT(*) as c FROM accounts;")
        tx_stats = self.db.query_one(
            """
            SELECT 
                COUNT(*) as total_tx,
                SUM(amount) as total_vol,
                SUM(fee) as total_fees,
                SUM(CASE WHEN status = 'FLAGGED' THEN 1 ELSE 0 END) as flagged_tx,
                SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed_tx
            FROM transactions;
            """
        )
        trade_stats = self.db.query_one("SELECT COUNT(*) as total_trades, SUM(price * quantity) as trade_vol FROM trades;")

        return {
            "total_accounts": acc_count["c"] if acc_count else 0,
            "total_transactions": tx_stats["total_tx"] or 0 if tx_stats else 0,
            "total_volume_processed": round(tx_stats["total_vol"] or 0.0, 2) if tx_stats else 0.0,
            "total_fee_revenue": round(tx_stats["total_fees"] or 0.0, 2) if tx_stats else 0.0,
            "flagged_transactions": tx_stats["flagged_tx"] or 0 if tx_stats else 0,
            "failed_transactions": tx_stats["failed_tx"] or 0 if tx_stats else 0,
            "total_trades": trade_stats["total_trades"] or 0 if trade_stats else 0,
            "trade_volume": round(trade_stats["trade_vol"] or 0.0, 2) if trade_stats else 0.0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
