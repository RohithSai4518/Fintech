"""
Fintech Core Platform CLI Administration & Stress Tool
Zero external library dependencies.
Provides administrative actions, audit verification, and high-throughput batch transaction stress testing.
"""

import sys
import os
import argparse
import time
import random
import uuid

# Ensure root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.core.database import DatabaseManager
from backend.core.idempotency import IdempotencyManager
from backend.core.models import (
    AccountType, AccountSubtype, Currency, PaymentMethod,
    JournalEntryLine, EntryDirection
)
from backend.services.ledger_service import LedgerService
from backend.services.payment_service import PaymentService
from backend.services.trading_service import TradingService
from backend.services.fraud_service import FraudService
from backend.services.reporting_service import ReportingService


def setup_services(db_path: str = "fintech_core.db"):
    db = DatabaseManager(db_path=db_path)
    idempotency = IdempotencyManager()
    ledger = LedgerService(db=db)
    fraud = FraudService(db=db)
    payments = PaymentService(db=db, ledger_service=ledger, fraud_service=fraud, idempotency_manager=idempotency)
    trading = TradingService(db=db, ledger_service=ledger)
    reporting = ReportingService(db=db)
    return db, ledger, payments, trading, fraud, reporting


def cmd_verify(args):
    _, ledger, _, _, _, reporting = setup_services(args.db)
    print("Executing system-wide double-entry ledger integrity audit...")
    integrity = ledger.verify_system_integrity()
    print(f"System Invariant Status: {'[OK] BALANCED' if integrity['is_balanced'] else '[FAILED] IMBALANCED'}")
    for curr, totals in integrity.get("totals_by_currency", {}).items():
        print(f"  Currency {curr}: Debits = ${totals['DEBIT']:,.2f} | Credits = ${totals['CREDIT']:,.2f}")

    tb = reporting.get_trial_balance()
    print(f"\nTrial Balance Summary:")
    print(f"  Total Debits:  ${tb['total_debits']:,.2f}")
    print(f"  Total Credits: ${tb['total_credits']:,.2f}")
    print(f"  Difference:    ${tb['difference']:,.2f}")


def cmd_stress(args):
    db, ledger, payments, trading, _, _ = setup_services(args.db)
    count = args.count
    print(f"Starting financial transaction stress test ({count} operations)...")

    # Create 2 stress testing accounts
    acc_a = ledger.create_account("Stress Account A", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.USD)
    acc_b = ledger.create_account("Stress Account B", AccountType.LIABILITY, AccountSubtype.CHECKING, Currency.USD)

    # Fund Account A
    lines = [
        JournalEntryLine("acc_sys_clearing_usd", EntryDirection.DEBIT, 1000000.0, Currency.USD),
        JournalEntryLine(acc_a.id, EntryDirection.CREDIT, 1000000.0, Currency.USD)
    ]
    ledger.post_journal_entry("fund_stress_a", "Fund Stress Test", lines)

    start_time = time.time()
    settled = 0

    for i in range(count):
        amount = round(random.uniform(10.0, 500.0), 2)
        try:
            payments.process_payment(
                source_account_id=acc_a.id,
                destination_account_id=acc_b.id,
                amount=amount,
                currency=Currency.USD,
                payment_method=PaymentMethod.INTERNAL,
                idempotency_key=f"stress_{uuid.uuid4().hex}",
                description=f"Automated Stress Transfer #{i+1}"
            )
            settled += 1
        except Exception as ex:
            print(f"Transfer {i+1} failed: {ex}")

    elapsed = time.time() - start_time
    tps = settled / elapsed if elapsed > 0 else 0
    print(f"\nStress Test Complete:")
    print(f"  Settled Transactions: {settled} / {count}")
    print(f"  Total Time:           {elapsed:.2f} seconds")
    print(f"  Throughput:           {tps:.1f} transactions/sec")

    # Run integrity verification
    cmd_verify(args)


def main():
    parser = argparse.ArgumentParser(description="Fintech Platform Administration CLI")
    parser.add_argument("--db", default="fintech_core.db", help="SQLite database path")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Verify Command
    verify_p = subparsers.add_parser("verify", help="Audit double-entry ledger invariant")
    verify_p.set_defaults(func=cmd_verify)

    # Stress Command
    stress_p = subparsers.add_parser("stress", help="Execute high-throughput transaction stress test")
    stress_p.add_argument("--count", type=int, default=100, help="Number of simulated transactions")
    stress_p.set_defaults(func=cmd_stress)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
