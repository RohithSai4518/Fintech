"""
Unit Tests for Payment Processing & Settlement Service
Validates multi-rail payment routing, fee deductions, idempotency, and card checks.
"""

import unittest
from backend.core.database import DatabaseManager
from backend.core.idempotency import IdempotencyManager
from backend.core.models import (
    AccountType, AccountSubtype, Currency, PaymentMethod,
    JournalEntryLine, EntryDirection, TransactionStatus
)
from backend.services.ledger_service import LedgerService
from backend.services.fraud_service import FraudService
from backend.services.payment_service import PaymentService


class TestPaymentService(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.ledger = LedgerService(self.db)
        self.fraud = FraudService(self.db)
        self.idempotency = IdempotencyManager()
        self.payments = PaymentService(
            db=self.db,
            ledger_service=self.ledger,
            fraud_service=self.fraud,
            idempotency_manager=self.idempotency
        )

        # Setup test accounts
        self.alice = self.ledger.create_account("Alice", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.USD)
        self.bob = self.ledger.create_account("Bob", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.USD)

        # Fund Alice with $500 initial balance
        lines = [
            JournalEntryLine("acc_sys_clearing_usd", EntryDirection.DEBIT, 500.0, Currency.USD),
            JournalEntryLine(self.alice.id, EntryDirection.CREDIT, 500.0, Currency.USD)
        ]
        self.ledger.post_journal_entry("fund_alice", "Initial deposit", lines)

    def test_internal_transfer_settlement(self):
        tx = self.payments.process_payment(
            source_account_id=self.alice.id,
            destination_account_id=self.bob.id,
            amount=100.00,
            currency=Currency.USD,
            payment_method=PaymentMethod.INTERNAL,
            idempotency_key="tx_test_001",
            description="Lunch reimbursement",
            fee_rate=0.01  # 1% fee = $1.00
        )

        self.assertEqual(tx.status, TransactionStatus.SETTLED)
        self.assertEqual(tx.fee, 1.00)

        alice_updated = self.ledger.get_account(self.alice.id)
        bob_updated = self.ledger.get_account(self.bob.id)
        fee_updated = self.ledger.get_account("acc_sys_fee_usd")

        # Alice paid $100 -> balance becomes $400
        self.assertEqual(alice_updated.balance, 400.00)
        # Bob received $100 - $1 = $99 -> balance becomes $99
        self.assertEqual(bob_updated.balance, 99.00)
        # Fee revenue received $1.00
        self.assertEqual(fee_updated.balance, 1.00)

    def test_idempotency_prevents_duplicate_charge(self):
        # First call
        tx1 = self.payments.process_payment(
            source_account_id=self.alice.id,
            destination_account_id=self.bob.id,
            amount=50.00,
            currency=Currency.USD,
            payment_method=PaymentMethod.INTERNAL,
            idempotency_key="idem_unique_key_123",
            description="Monthly subscription"
        )

        # Second call with same idempotency key
        tx2 = self.payments.process_payment(
            source_account_id=self.alice.id,
            destination_account_id=self.bob.id,
            amount=50.00,
            currency=Currency.USD,
            payment_method=PaymentMethod.INTERNAL,
            idempotency_key="idem_unique_key_123",
            description="Monthly subscription"
        )

        self.assertEqual(tx1.id, tx2.id)

        # Verify Alice was only charged ONCE ($50)
        alice_updated = self.ledger.get_account(self.alice.id)
        self.assertEqual(alice_updated.balance, 450.00)

    def test_insufficient_funds_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            self.payments.process_payment(
                source_account_id=self.alice.id,
                destination_account_id=self.bob.id,
                amount=99999.00,
                currency=Currency.USD,
                payment_method=PaymentMethod.INTERNAL,
                idempotency_key="tx_fail_01",
                description="Overdraft attempt"
            )
        self.assertIn("Insufficient available balance", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
