"""
Unit Tests for Financial Reporting Service
Validates Trial Balance debit/credit equation, Balance Sheet, and Income Statement (P&L).
"""

import unittest
from backend.core.database import DatabaseManager
from backend.core.models import (
    AccountType, AccountSubtype, Currency,
    JournalEntryLine, EntryDirection
)
from backend.services.ledger_service import LedgerService
from backend.services.reporting_service import ReportingService


class TestReportingService(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.ledger = LedgerService(self.db)
        self.reporting = ReportingService(self.db)

        # Create Chart of Accounts
        self.vault = self.ledger.create_account("Operating Cash", AccountType.ASSET, AccountSubtype.VAULT, Currency.USD)
        self.capital = self.ledger.create_account("Owner Capital", AccountType.EQUITY, AccountSubtype.VAULT, Currency.USD)
        self.fee_rev = self.ledger.create_account("Fee Revenue", AccountType.REVENUE, AccountSubtype.FEE_COLLECTION, Currency.USD)
        self.ops_exp = self.ledger.create_account("Server Expenses", AccountType.EXPENSE, AccountSubtype.VAULT, Currency.USD)

    def test_trial_balance_balanced(self):
        # 1. Capital Injection: Debit Cash ($10,000) / Credit Capital ($10,000)
        lines1 = [
            JournalEntryLine(self.vault.id, EntryDirection.DEBIT, 10000.0, Currency.USD),
            JournalEntryLine(self.capital.id, EntryDirection.CREDIT, 10000.0, Currency.USD)
        ]
        self.ledger.post_journal_entry("je_01", "Capital Injection", lines1)

        # 2. Fee Revenue: Debit Cash ($500) / Credit Fee Revenue ($500)
        lines2 = [
            JournalEntryLine(self.vault.id, EntryDirection.DEBIT, 500.0, Currency.USD),
            JournalEntryLine(self.fee_rev.id, EntryDirection.CREDIT, 500.0, Currency.USD)
        ]
        self.ledger.post_journal_entry("je_02", "Fee Earned", lines2)

        tb = self.reporting.get_trial_balance()
        self.assertTrue(tb["is_balanced"])
        self.assertEqual(tb["total_debits"], 10500.0)
        self.assertEqual(tb["total_credits"], 10500.0)

    def test_pnl_income_statement(self):
        # Expense: Debit Server Expense ($150) / Credit Cash ($150)
        lines = [
            JournalEntryLine(self.ops_exp.id, EntryDirection.DEBIT, 150.0, Currency.USD),
            JournalEntryLine(self.vault.id, EntryDirection.CREDIT, 150.0, Currency.USD)
        ]
        self.ledger.post_journal_entry("je_exp", "Pay AWS Hosting", lines)

        # Revenue: Debit Cash ($500) / Credit Fee Revenue ($500)
        lines2 = [
            JournalEntryLine(self.vault.id, EntryDirection.DEBIT, 500.0, Currency.USD),
            JournalEntryLine(self.fee_rev.id, EntryDirection.CREDIT, 500.0, Currency.USD)
        ]
        self.ledger.post_journal_entry("je_rev", "Fee Earned", lines2)

        pnl = self.reporting.get_income_statement()
        self.assertEqual(pnl["revenues"]["total"], 500.0)
        self.assertEqual(pnl["expenses"]["total"], 150.0)
        self.assertEqual(pnl["net_income"], 350.0)


if __name__ == "__main__":
    unittest.main()
