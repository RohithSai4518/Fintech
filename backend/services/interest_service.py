"""
Fintech Interest & Fee Accrual Engine
Calculates daily/monthly compound interest accruals, APY yield, and overdraft fees.
Zero external library dependencies.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

from backend.core.models import (
    Account, AccountType, AccountSubtype, Currency,
    JournalEntryLine, EntryDirection
)
from backend.core.database import DatabaseManager
from backend.services.ledger_service import LedgerService


class InterestService:
    """Accrues interest on interest-bearing deposit accounts and applies scheduled fees."""

    def __init__(self, db: DatabaseManager, ledger_service: LedgerService):
        self.db = db
        self.ledger_service = ledger_service
        self._ensure_interest_expense_account()

    def _ensure_interest_expense_account(self) -> None:
        """Ensures the bank's interest expense account exists."""
        acc = self.ledger_service.get_account("acc_sys_interest_expense_usd")
        if not acc:
            self.db.execute(
                """
                INSERT OR IGNORE INTO accounts (
                    id, account_number, name, account_type, account_subtype, currency,
                    balance, available_balance, hold_balance, credit_limit, interest_rate,
                    is_active, created_at, owner_id, metadata_json
                ) VALUES (
                    'acc_sys_interest_expense_usd', '5000000001', 'Bank Interest Expense',
                    'EXPENSE', 'VAULT', 'USD', 0.0, 0.0, 0.0, 0.0, 0.0,
                    1, ?, 'SYSTEM', '{"system_managed": true}'
                );
                """,
                (datetime.now(timezone.utc).isoformat(),)
            )

    def calculate_daily_accrual(self, principal: float, annual_rate: float) -> float:
        """
        Calculates daily interest:
        Interest = Principal * (Annual Rate / 365)
        """
        if principal <= 0 or annual_rate <= 0:
            return 0.0
        daily_rate = annual_rate / 365.0
        return round(principal * daily_rate, 4)

    def run_interest_accrual_batch(self) -> List[Dict[str, Any]]:
        """
        Runs batch calculation and general ledger posting for all active savings accounts
        with an interest rate > 0.
        """
        accounts = self.db.query_all(
            """
            SELECT * FROM accounts
            WHERE is_active = 1 AND interest_rate > 0 AND balance > 0
            AND account_type = 'LIABILITY';
            """
        )

        accrual_records: List[Dict[str, Any]] = []

        for acc in accounts:
            interest_amount = self.calculate_daily_accrual(acc["balance"], acc["interest_rate"])
            if interest_amount < 0.01:
                continue

            ref_id = f"int_{acc['id']}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

            # Post Double-Entry Journal Entry:
            # Debit: Bank Interest Expense
            # Credit: Customer Savings Account Balance
            lines = [
                JournalEntryLine(
                    account_id="acc_sys_interest_expense_usd",
                    direction=EntryDirection.DEBIT,
                    amount=interest_amount,
                    currency=Currency(acc["currency"]),
                    memo=f"Interest expense payout for account {acc['account_number']}"
                ),
                JournalEntryLine(
                    account_id=acc["id"],
                    direction=EntryDirection.CREDIT,
                    amount=interest_amount,
                    currency=Currency(acc["currency"]),
                    memo=f"Daily compound interest accrual ({acc['interest_rate'] * 100:.2f}% APY)"
                )
            ]

            self.ledger_service.post_journal_entry(
                reference_id=ref_id,
                description=f"Interest Accrual on {acc['account_number']}",
                lines=lines,
                metadata={"principal": acc["balance"], "apy": acc["interest_rate"]}
            )

            accrual_records.append({
                "account_id": acc["id"],
                "account_number": acc["account_number"],
                "principal": acc["balance"],
                "apy": acc["interest_rate"],
                "interest_earned": interest_amount
            })

        return accrual_records
