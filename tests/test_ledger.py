"""
Unit Tests for Double-Entry General Ledger Service
Validates mathematical balance invariants (Debits == Credits), account types, and audit logging.
"""

import unittest
from backend.core.database import DatabaseManager
from backend.core.models import (
    AccountType, AccountSubtype, Currency,
    JournalEntryLine, EntryDirection
)
from backend.services.ledger_service import LedgerService


class TestLedgerService(unittest.TestCase):

    def setUp(self):
        # In-memory database for isolation
        self.db = DatabaseManager(":memory:")
        self.ledger = LedgerService(self.db)

    def test_create_account(self):
        acc = self.ledger.create_account(
            name="Alice Checking",
            account_type=AccountType.LIABILITY,
            account_subtype=AccountSubtype.CHECKING,
            currency=Currency.USD,
            credit_limit=500.0
        )
        self.assertIsNotNone(acc.id)
        self.assertEqual(acc.name, "Alice Checking")
        self.assertEqual(acc.balance, 0.0)
        self.assertEqual(acc.available_balance, 500.0)

        retrieved = self.ledger.get_account(acc.id)
        self.assertEqual(retrieved.id, acc.id)
        self.assertEqual(retrieved.account_number, acc.account_number)

    def test_double_entry_balance_success(self):
        # Setup Vault (Asset) and Customer (Liability)
        vault = self.ledger.create_account(
            name="Bank Vault",
            account_type=AccountType.ASSET,
            account_subtype=AccountSubtype.VAULT,
            currency=Currency.USD
        )
        customer = self.ledger.create_account(
            name="Bob Customer",
            account_type=AccountType.LIABILITY,
            account_subtype=AccountSubtype.CHECKING,
            currency=Currency.USD
        )

        # Deposit $1,000 into Bob's account
        # Debit Vault ($1,000) [Asset increases]
        # Credit Bob ($1,000) [Liability increases]
        lines = [
            JournalEntryLine(vault.id, EntryDirection.DEBIT, 1000.0, Currency.USD, "Cash deposit into vault"),
            JournalEntryLine(customer.id, EntryDirection.CREDIT, 1000.0, Currency.USD, "Customer deposit balance credit")
        ]

        entry = self.ledger.post_journal_entry(
            reference_id="dep_001",
            description="Initial deposit",
            lines=lines
        )
        self.assertIsNotNone(entry.id)

        # Verify updated balances
        vault_updated = self.ledger.get_account(vault.id)
        cust_updated = self.ledger.get_account(customer.id)
        self.assertEqual(vault_updated.balance, 1000.0)
        self.assertEqual(cust_updated.balance, 1000.0)

        # Verify global integrity
        integrity = self.ledger.verify_system_integrity()
        self.assertTrue(integrity["is_balanced"])

    def test_double_entry_imbalance_rejected(self):
        acc1 = self.ledger.create_account("Acc 1", AccountType.ASSET, AccountSubtype.CHECKING, Currency.USD)
        acc2 = self.ledger.create_account("Acc 2", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.USD)

        # Intentional imbalance: Debit $100 vs Credit $90
        lines = [
            JournalEntryLine(acc1.id, EntryDirection.DEBIT, 100.0, Currency.USD),
            JournalEntryLine(acc2.id, EntryDirection.CREDIT, 90.0, Currency.USD)
        ]

        with self.assertRaises(ValueError) as ctx:
            self.ledger.post_journal_entry("imbalanced_ref", "Broken tx", lines)
        self.assertIn("Double-entry imbalance", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
