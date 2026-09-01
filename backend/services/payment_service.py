"""
Fintech Payment & Settlement Orchestration Service
Handles payment lifecycle, authorization holds, clearing, multi-rail routing (ACH, Wire, Card, Internal),
idempotent execution, and double-entry general ledger posting.
"""

import uuid
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from backend.core.models import (
    Transaction, TransactionStatus, PaymentMethod, Currency,
    JournalEntryLine, EntryDirection, RiskLevel
)
from backend.core.database import DatabaseManager
from backend.core.idempotency import IdempotencyManager
from backend.services.ledger_service import LedgerService
from backend.services.fraud_service import FraudService
from backend.core.security import SecurityManager


class PaymentService:
    """Enterprise payment orchestrator coordinating risk, double-entry ledger, and rail routing."""

    def __init__(
        self,
        db: DatabaseManager,
        ledger_service: LedgerService,
        fraud_service: FraudService,
        idempotency_manager: IdempotencyManager
    ):
        self.db = db
        self.ledger_service = ledger_service
        self.fraud_service = fraud_service
        self.idempotency_manager = idempotency_manager
        self._ensure_system_accounts()

    def _ensure_system_accounts(self) -> None:
        """Ensures system clearing and fee collection accounts exist."""
        # 1. Processing Fee Revenue Account
        fee_acc = self.ledger_service.get_account("acc_sys_fee_usd")
        if not fee_acc:
            self.db.execute(
                """
                INSERT OR IGNORE INTO accounts (
                    id, account_number, name, account_type, account_subtype, currency,
                    balance, available_balance, hold_balance, credit_limit, interest_rate,
                    is_active, created_at, owner_id, metadata_json
                ) VALUES (
                    'acc_sys_fee_usd', '3000000001', 'Platform Processing Fee Revenue',
                    'REVENUE', 'FEE_COLLECTION', 'USD', 0.0, 0.0, 0.0, 0.0, 0.0,
                    1, ?, 'SYSTEM', '{"system_managed": true}'
                );
                """,
                (datetime.now(timezone.utc).isoformat(),)
            )

        # 2. Card Settlement Clearing Vault
        clearing_acc = self.ledger_service.get_account("acc_sys_clearing_usd")
        if not clearing_acc:
            self.db.execute(
                """
                INSERT OR IGNORE INTO accounts (
                    id, account_number, name, account_type, account_subtype, currency,
                    balance, available_balance, hold_balance, credit_limit, interest_rate,
                    is_active, created_at, owner_id, metadata_json
                ) VALUES (
                    'acc_sys_clearing_usd', '1000000001', 'Card Gateway Inbound Clearing Asset',
                    'ASSET', 'CLEARING', 'USD', 1000000.0, 1000000.0, 0.0, 0.0, 0.0,
                    1, ?, 'SYSTEM', '{"system_managed": true}'
                );
                """,
                (datetime.now(timezone.utc).isoformat(),)
            )

    def process_payment(
        self,
        source_account_id: Optional[str],
        destination_account_id: Optional[str],
        amount: float,
        currency: Currency,
        payment_method: PaymentMethod,
        idempotency_key: str,
        description: str,
        fee_rate: float = 0.005,  # 0.5% default fee
        card_data: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        actor_id: str = "SYSTEM"
    ) -> Transaction:
        """
        Executes an end-to-end payment with strict idempotency, fraud evaluation,
        and atomic double-entry general ledger posting.
        """
        if amount <= 0:
            raise ValueError(f"Transaction amount must be positive, got {amount}")

        # 1. Idempotency Check
        is_cached, cached_res = self.idempotency_manager.check_or_lock(idempotency_key)
        if is_cached and cached_res:
            # Return reconstituted transaction from cache
            return self.get_transaction(cached_res["id"]) or Transaction(**cached_res)

        tx_id = f"tx_{uuid.uuid4().hex[:12]}"
        meta = metadata or {}

        try:
            # 2. Card Validation (PCI-DSS & Luhn Check if card payment)
            if payment_method == PaymentMethod.CARD:
                if not card_data or not card_data.get("card_number"):
                    raise ValueError("Card payment requires card_number")
                raw_pan = card_data["card_number"]
                if not SecurityManager.validate_luhn(raw_pan):
                    raise ValueError("Invalid credit card number checksum (Luhn check failed)")
                meta["masked_card"] = SecurityManager.mask_card_number(raw_pan)
                meta["card_brand"] = card_data.get("brand", "VISA")
                # Source account is the external clearing vault if not explicitly specified
                if not source_account_id:
                    source_account_id = "acc_sys_clearing_usd"

            # 3. Pre-flight Balance Verification (if internal source account)
            if source_account_id and not source_account_id.startswith("acc_sys_clearing"):
                src_acc = self.ledger_service.get_account(source_account_id)
                if not src_acc:
                    raise ValueError(f"Source account '{source_account_id}' does not exist.")
                if src_acc.available_balance < amount:
                    raise ValueError(
                        f"Insufficient available balance (${src_acc.available_balance:,.2f}) for transfer of ${amount:,.2f}"
                    )

            # 4. Real-time Fraud Risk Evaluation
            risk_score, risk_level, triggers, recommended_action = self.fraud_service.evaluate_transaction(
                source_account_id=source_account_id,
                destination_account_id=destination_account_id,
                amount=amount,
                currency=currency.value if isinstance(currency, Currency) else currency,
                metadata=meta
            )
            meta["risk_triggers"] = triggers

            # If risk engine decides to block, record failed/blocked transaction
            if recommended_action == "BLOCK":
                failed_tx = Transaction(
                    id=tx_id,
                    source_account_id=source_account_id,
                    destination_account_id=destination_account_id,
                    amount=amount,
                    fee=0.0,
                    currency=currency,
                    payment_method=payment_method,
                    status=TransactionStatus.FAILED,
                    idempotency_key=idempotency_key,
                    description=description,
                    risk_score=risk_score,
                    risk_level=risk_level,
                    created_at=datetime.now(timezone.utc).isoformat(),
                    settled_at=None,
                    failure_reason=f"Transaction blocked by risk policy: {'; '.join(triggers)}",
                    metadata=meta
                )
                self._save_transaction(failed_tx)
                self.idempotency_manager.store_result(idempotency_key, failed_tx.to_dict())
                return failed_tx

            # 5. Calculate Fees & Net Amount
            fee = round(amount * fee_rate, 2)
            net_destination_amount = round(amount - fee, 2) if destination_account_id else amount

            # 6. Post Double-Entry Ledger Transaction Legs
            # Leg 1: Debit Source (Amount)
            # Leg 2: Credit Destination (Net Amount)
            # Leg 3: Credit Fee Revenue (Fee Amount)
            lines: List[JournalEntryLine] = []

            if source_account_id:
                lines.append(
                    JournalEntryLine(
                        account_id=source_account_id,
                        direction=EntryDirection.DEBIT,
                        amount=amount,
                        currency=currency,
                        memo=f"Payment debit for {description}"
                    )
                )

            if destination_account_id:
                lines.append(
                    JournalEntryLine(
                        account_id=destination_account_id,
                        direction=EntryDirection.CREDIT,
                        amount=net_destination_amount,
                        currency=currency,
                        memo=f"Payment receipt for {description}"
                    )
                )

            if fee > 0:
                lines.append(
                    JournalEntryLine(
                        account_id="acc_sys_fee_usd",
                        direction=EntryDirection.CREDIT,
                        amount=fee,
                        currency=currency,
                        memo=f"Processing fee on {tx_id}"
                    )
                )

            self.ledger_service.post_journal_entry(
                reference_id=tx_id,
                description=f"Settlement: {description}",
                lines=lines,
                metadata={"payment_method": payment_method.value, "risk_score": risk_score},
                actor_id=actor_id
            )

            # 7. Record Settled Transaction
            status = TransactionStatus.FLAGGED if risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH] else TransactionStatus.SETTLED
            settled_tx = Transaction(
                id=tx_id,
                source_account_id=source_account_id,
                destination_account_id=destination_account_id,
                amount=amount,
                fee=fee,
                currency=currency,
                payment_method=payment_method,
                status=status,
                idempotency_key=idempotency_key,
                description=description,
                risk_score=risk_score,
                risk_level=risk_level,
                created_at=datetime.now(timezone.utc).isoformat(),
                settled_at=datetime.now(timezone.utc).isoformat(),
                failure_reason=None,
                metadata=meta
            )

            self._save_transaction(settled_tx)
            self.idempotency_manager.store_result(idempotency_key, settled_tx.to_dict())
            return settled_tx

        except Exception as e:
            self.idempotency_manager.release_lock(idempotency_key)
            raise e

    def get_transaction(self, tx_id: str) -> Optional[Transaction]:
        """Retrieves a transaction by its unique identifier."""
        row = self.db.query_one("SELECT * FROM transactions WHERE id = ?;", (tx_id,))
        if not row:
            return None
        return self._row_to_tx(row)

    def list_transactions(self, account_id: Optional[str] = None, limit: int = 50) -> List[Transaction]:
        """Lists transactions, optionally filtered by associated account."""
        if account_id:
            rows = self.db.query_all(
                """
                SELECT * FROM transactions
                WHERE source_account_id = ? OR destination_account_id = ?
                ORDER BY created_at DESC LIMIT ?;
                """,
                (account_id, account_id, limit)
            )
        else:
            rows = self.db.query_all("SELECT * FROM transactions ORDER BY created_at DESC LIMIT ?;", (limit,))
        return [self._row_to_tx(r) for r in rows]

    def _save_transaction(self, tx: Transaction) -> None:
        """Persists transaction to SQLite datastore."""
        self.db.execute(
            """
            INSERT INTO transactions (
                id, source_account_id, destination_account_id, amount, fee,
                currency, payment_method, status, idempotency_key, description,
                risk_score, risk_level, created_at, settled_at, failure_reason, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                tx.id, tx.source_account_id, tx.destination_account_id, tx.amount, tx.fee,
                tx.currency.value if isinstance(tx.currency, Currency) else tx.currency,
                tx.payment_method.value if isinstance(tx.payment_method, PaymentMethod) else tx.payment_method,
                tx.status.value if isinstance(tx.status, TransactionStatus) else tx.status,
                tx.idempotency_key, tx.description, tx.risk_score,
                tx.risk_level.value if isinstance(tx.risk_level, RiskLevel) else tx.risk_level,
                tx.created_at, tx.settled_at, tx.failure_reason, json.dumps(tx.metadata)
            )
        )

    @staticmethod
    def _row_to_tx(row: Any) -> Transaction:
        meta = json.loads(row["metadata_json"]) if row["metadata_json"] else {}
        return Transaction(
            id=row["id"],
            source_account_id=row["source_account_id"],
            destination_account_id=row["destination_account_id"],
            amount=row["amount"],
            fee=row["fee"],
            currency=Currency(row["currency"]),
            payment_method=PaymentMethod(row["payment_method"]),
            status=TransactionStatus(row["status"]),
            idempotency_key=row["idempotency_key"],
            description=row["description"],
            risk_score=row["risk_score"],
            risk_level=RiskLevel(row["risk_level"]),
            created_at=row["created_at"],
            settled_at=row["settled_at"],
            failure_reason=row["failure_reason"],
            metadata=meta
        )
