"""
Fintech REST API Handlers
Maps HTTP endpoints to domain services and returns JSON payloads.
Zero external library dependencies.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from backend.core.models import (
    AccountType, AccountSubtype, Currency, PaymentMethod,
    OrderSide, OrderType, JournalEntryLine, EntryDirection
)
from backend.core.database import DatabaseManager
from backend.core.idempotency import IdempotencyManager
from backend.services.ledger_service import LedgerService
from backend.services.payment_service import PaymentService
from backend.services.trading_service import TradingService
from backend.services.fraud_service import FraudService
from backend.services.interest_service import InterestService
from backend.services.reporting_service import ReportingService
from backend.server.router import HTTPResponse


class APIHandlerContainer:
    """Dependency injection container holding services and HTTP route handlers."""

    def __init__(
        self,
        db: DatabaseManager,
        ledger_service: LedgerService,
        payment_service: PaymentService,
        trading_service: TradingService,
        fraud_service: FraudService,
        interest_service: InterestService,
        reporting_service: ReportingService
    ):
        self.db = db
        self.ledger = ledger_service
        self.payments = payment_service
        self.trading = trading_service
        self.fraud = fraud_service
        self.interest = interest_service
        self.reporting = reporting_service

    # --- System & Seed ---
    def handle_seed_data(self, req: Dict[str, Any]) -> Dict[str, Any]:
        """Seeds initial chart of accounts, customers, transactions, and orders for realistic simulation."""
        # 1. Create Sample Customer Accounts if not exist
        sample_accounts = [
            ("acc_alice_chk", "Alice Smith - Checking", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.USD, 15450.00, 0.0),
            ("acc_alice_sav", "Alice Smith - High Yield Savings", AccountType.LIABILITY, AccountSubtype.SAVINGS, Currency.USD, 45200.00, 0.045),
            ("acc_bob_chk", "Bob Johnson - Prime Checking", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.USD, 8920.00, 0.0),
            ("acc_bob_inv", "Bob Johnson - Multi-Asset Trading", AccountType.LIABILITY, AccountSubtype.INVESTMENT, Currency.USD, 25000.00, 0.0),
            ("acc_acme_corp", "Acme Global Merchant Escrow", AccountType.LIABILITY, AccountSubtype.ESCROW, Currency.USD, 128400.00, 0.0),
            ("acc_intl_eur", "Euro Foreign Currency Holding", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.EUR, 12000.00, 0.0)
        ]

        # Initial capital vaults (Asset) to balance starting customer deposits
        for v_curr in [Currency.USD, Currency.EUR]:
            vault_id = f"acc_sys_bank_capital_{v_curr.value.lower()}"
            vault = self.ledger.get_account(vault_id)
            if not vault:
                self.db.execute(
                    """
                    INSERT OR IGNORE INTO accounts (
                        id, account_number, name, account_type, account_subtype, currency,
                        balance, available_balance, hold_balance, credit_limit, interest_rate,
                        is_active, created_at, owner_id, metadata_json
                    ) VALUES (
                        ?, ?, ?, 'ASSET', 'VAULT', ?, 10000000.0, 10000000.0, 0.0, 0.0, 0.0,
                        1, ?, 'SYSTEM', '{"system_managed": true}'
                    );
                    """,
                    (vault_id, f"109999999{1 if v_curr == Currency.USD else 2}", f"Central Bank Operating Reserves ({v_curr.value})", v_curr.value, datetime.now(timezone.utc).isoformat())
                )

        created = []
        for acc_id, name, a_type, a_sub, curr, initial_bal, apy in sample_accounts:
            existing = self.ledger.get_account(acc_id)
            if not existing:
                acc = self.ledger.create_account(
                    name=name,
                    account_type=a_type,
                    account_subtype=a_sub,
                    currency=curr,
                    owner_id=f"user_{name.split()[0].lower()}",
                    interest_rate=apy
                )
                self.db.execute("UPDATE accounts SET id = ? WHERE id = ?;", (acc_id, acc.id))
                acc.id = acc_id

                # Fund initial balance with double-entry journal entry against corresponding Currency Central Reserves
                if initial_bal > 0:
                    reserve_vault = f"acc_sys_bank_capital_{curr.value.lower()}"
                    lines = [
                        JournalEntryLine(reserve_vault, EntryDirection.DEBIT, initial_bal, curr, f"Initial deposit funding for {name}"),
                        JournalEntryLine(acc_id, EntryDirection.CREDIT, initial_bal, curr, "Opening balance deposit")
                    ]
                    self.ledger.post_journal_entry(
                        reference_id=f"seed_{acc_id}",
                        description=f"Initial Opening Deposit for {name}",
                        lines=lines
                    )
                created.append(acc.name)

        # 2. Seed Sample Limit Orders for Trading Engine
        self.trading.submit_order("acc_bob_inv", "BTC/USD", OrderSide.BUY, OrderType.LIMIT, 0.5, 64100.00)
        self.trading.submit_order("acc_acme_corp", "BTC/USD", OrderSide.SELL, OrderType.LIMIT, 0.75, 64450.00)
        self.trading.submit_order("acc_alice_chk", "EUR/USD", OrderSide.BUY, OrderType.LIMIT, 5000.0, 1.0820)
        self.trading.submit_order("acc_bob_inv", "EUR/USD", OrderSide.SELL, OrderType.LIMIT, 4000.0, 1.0880)

        # 3. Seed Sample Transactions
        self.payments.process_payment(
            source_account_id="acc_alice_chk",
            destination_account_id="acc_acme_corp",
            amount=350.00,
            currency=Currency.USD,
            payment_method=PaymentMethod.INTERNAL,
            idempotency_key="seed_tx_001",
            description="Enterprise Cloud Software Subscription"
        )
        self.payments.process_payment(
            source_account_id="acc_bob_chk",
            destination_account_id="acc_alice_chk",
            amount=120.00,
            currency=Currency.USD,
            payment_method=PaymentMethod.INTERNAL,
            idempotency_key="seed_tx_002",
            description="Dinner reimbursement split"
        )

        return {"status": "success", "message": "Synthetic banking environment seeded successfully", "created_accounts": created}

    # --- Accounts ---
    def handle_list_accounts(self, req: Dict[str, Any]) -> Dict[str, Any]:
        accounts = self.ledger.list_accounts()
        return {"accounts": [a.to_dict() for a in accounts]}

    def handle_get_account(self, req: Dict[str, Any], id: str) -> Dict[str, Any]:
        acc = self.ledger.get_account(id)
        if not acc:
            raise ValueError(f"Account '{id}' not found")
        return acc.to_dict()

    def handle_create_account(self, req: Dict[str, Any]) -> Dict[str, Any]:
        body = req.get("body", {})
        acc = self.ledger.create_account(
            name=body.get("name", "New Account"),
            account_type=AccountType(body.get("account_type", "LIABILITY")),
            account_subtype=AccountSubtype(body.get("account_subtype", "CHECKING")),
            currency=Currency(body.get("currency", "USD")),
            owner_id=body.get("owner_id"),
            credit_limit=float(body.get("credit_limit", 0.0)),
            interest_rate=float(body.get("interest_rate", 0.0))
        )
        return acc.to_dict()

    # --- Ledger & Audit ---
    def handle_list_journal_entries(self, req: Dict[str, Any]) -> Dict[str, Any]:
        params = req.get("params", {})
        limit = int(params.get("limit", 50))
        entries = self.ledger.list_journal_entries(limit=limit)
        return {"journal_entries": entries}

    def handle_verify_ledger_integrity(self, req: Dict[str, Any]) -> Dict[str, Any]:
        return self.ledger.verify_system_integrity()

    # --- Payments ---
    def handle_process_payment(self, req: Dict[str, Any]) -> Dict[str, Any]:
        body = req.get("body", {})
        idem_key = body.get("idempotency_key") or f"idem_{uuid.uuid4().hex}"
        tx = self.payments.process_payment(
            source_account_id=body.get("source_account_id"),
            destination_account_id=body.get("destination_account_id"),
            amount=float(body.get("amount", 0.0)),
            currency=Currency(body.get("currency", "USD")),
            payment_method=PaymentMethod(body.get("payment_method", "INTERNAL")),
            idempotency_key=idem_key,
            description=body.get("description", "Transfer"),
            card_data=body.get("card_data"),
            metadata=body.get("metadata")
        )
        return tx.to_dict()

    def handle_list_transactions(self, req: Dict[str, Any]) -> Dict[str, Any]:
        params = req.get("params", {})
        acc_id = params.get("account_id")
        limit = int(params.get("limit", 50))
        txs = self.payments.list_transactions(account_id=acc_id, limit=limit)
        return {"transactions": [t.to_dict() for t in txs]}

    # --- Trading ---
    def handle_get_market_prices(self, req: Dict[str, Any]) -> Dict[str, Any]:
        return {"prices": self.trading.get_market_prices()}

    def handle_get_order_book(self, req: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        # Handle encoded symbols (e.g. BTC%2FUSD -> BTC/USD)
        decoded_symbol = symbol.replace("%2F", "/")
        return self.trading.get_order_book(decoded_symbol)

    def handle_submit_order(self, req: Dict[str, Any]) -> Dict[str, Any]:
        body = req.get("body", {})
        order, fills = self.trading.submit_order(
            account_id=body.get("account_id", "acc_bob_inv"),
            symbol=body.get("symbol", "BTC/USD"),
            side=OrderSide(body.get("side", "BUY")),
            order_type=OrderType(body.get("order_type", "LIMIT")),
            quantity=float(body.get("quantity", 0.0)),
            price=float(body.get("price")) if body.get("price") is not None else None
        )
        return {"order": order.to_dict(), "fills": fills}

    def handle_list_orders(self, req: Dict[str, Any]) -> Dict[str, Any]:
        orders = self.trading.list_orders()
        return {"orders": orders}

    def handle_list_trades(self, req: Dict[str, Any]) -> Dict[str, Any]:
        trades = self.trading.list_trades()
        return {"trades": trades}

    # --- Fraud & Risk ---
    def handle_list_fraud_rules(self, req: Dict[str, Any]) -> Dict[str, Any]:
        rules = self.fraud.list_rules()
        return {"rules": [r.to_dict() for r in rules]}

    def handle_create_fraud_rule(self, req: Dict[str, Any]) -> Dict[str, Any]:
        body = req.get("body", {})
        rule = self.fraud.create_rule(
            name=body.get("name", "Custom Rule"),
            rule_type=body.get("rule_type", "AMOUNT_THRESHOLD"),
            threshold=float(body.get("threshold", 1000.0)),
            action=body.get("action", "FLAG"),
            description=body.get("description", "")
        )
        return rule.to_dict()

    # --- Financial Reports & KPIs ---
    def handle_get_kpis(self, req: Dict[str, Any]) -> Dict[str, Any]:
        return self.reporting.get_executive_kpis()

    def handle_get_trial_balance(self, req: Dict[str, Any]) -> Dict[str, Any]:
        return self.reporting.get_trial_balance()

    def handle_get_balance_sheet(self, req: Dict[str, Any]) -> Dict[str, Any]:
        return self.reporting.get_balance_sheet()

    def handle_get_income_statement(self, req: Dict[str, Any]) -> Dict[str, Any]:
        return self.reporting.get_income_statement()

    # --- Interest Run ---
    def handle_run_interest_accrual(self, req: Dict[str, Any]) -> Dict[str, Any]:
        accruals = self.interest.run_interest_accrual_batch()
        return {"status": "success", "accruals_posted": len(accruals), "details": accruals}
