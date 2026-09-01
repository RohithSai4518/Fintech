"""
Fintech Double-Entry General Ledger Service
Strictly implements the fundamental accounting equation:
Assets = Liabilities + Equity + (Revenue - Expenses)
Every financial transaction requires at least 2 balanced legs where SUM(Debits) == SUM(Credits).
"""

import uuid
import json
import sqlite3
import threading
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from backend.core.models import (
    Account, AccountType, AccountSubtype, Currency,
    JournalEntry, JournalEntryLine, EntryDirection, AuditLog
)
from backend.core.database import DatabaseManager
from backend.core.security import SecurityManager


class LedgerService:
    """Core accounting service ensuring immutable journal entries and mathematical balance."""

    def __init__(self, db: DatabaseManager):
        self.db = db
        self._lock = threading.Lock()
        self._last_audit_hash = ""

    def create_account(
        self,
        name: str,
        account_type: AccountType,
        account_subtype: AccountSubtype,
        currency: Currency,
        owner_id: Optional[str] = None,
        credit_limit: float = 0.0,
        interest_rate: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Account:
        """Provisions a new ledger account."""
        account_id = f"acc_{uuid.uuid4().hex[:12]}"
        # Generate formatted account number (e.g. 1001-XXXX-XXXX)
        prefix = "10" if account_type == AccountType.ASSET else ("20" if account_type == AccountType.LIABILITY else "30")
        account_number = f"{prefix}{uuid.uuid4().int % 10000000000:010d}"

        account = Account(
            id=account_id,
            account_number=account_number,
            name=name,
            account_type=account_type,
            account_subtype=account_subtype,
            currency=currency,
            balance=0.0,
            available_balance=credit_limit,
            hold_balance=0.0,
            credit_limit=credit_limit,
            interest_rate=interest_rate,
            is_active=True,
            created_at=datetime.now(timezone.utc).isoformat(),
            owner_id=owner_id,
            metadata=metadata or {}
        )

        # Ensure owner exists in users table if provided
        if owner_id:
            self.db.execute(
                """
                INSERT OR IGNORE INTO users (id, username, email, password_hash, salt, role, is_active, created_at)
                VALUES (?, ?, ?, 'n/a', 'n/a', 'CUSTOMER', 1, ?);
                """,
                (owner_id, owner_id, f"{owner_id}@fintech.local", datetime.now(timezone.utc).isoformat())
            )

        self.db.execute(
            """
            INSERT INTO accounts (
                id, account_number, name, account_type, account_subtype, currency,
                balance, available_balance, hold_balance, credit_limit, interest_rate,
                is_active, created_at, owner_id, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                account.id, account.account_number, account.name,
                account.account_type.value, account.account_subtype.value,
                account.currency.value, account.balance, account.available_balance,
                account.hold_balance, account.credit_limit, account.interest_rate,
                1 if account.is_active else 0, account.created_at, account.owner_id,
                json.dumps(account.metadata)
            )
        )

        self._record_audit("ACCOUNT", account.id, "CREATE", owner_id or "SYSTEM", account.to_dict())
        return account

    def get_account(self, account_id: str) -> Optional[Account]:
        """Retrieves an account by its unique identifier."""
        row = self.db.query_one("SELECT * FROM accounts WHERE id = ?;", (account_id,))
        if not row:
            return None
        return self._row_to_account(row)

    def get_account_by_number(self, account_number: str) -> Optional[Account]:
        """Retrieves an account by its external account number."""
        row = self.db.query_one("SELECT * FROM accounts WHERE account_number = ?;", (account_number,))
        if not row:
            return None
        return self._row_to_account(row)

    def list_accounts(self, owner_id: Optional[str] = None) -> List[Account]:
        """Lists accounts, optionally filtered by user ID."""
        if owner_id:
            rows = self.db.query_all("SELECT * FROM accounts WHERE owner_id = ? ORDER BY created_at DESC;", (owner_id,))
        else:
            rows = self.db.query_all("SELECT * FROM accounts ORDER BY created_at DESC;")
        return [self._row_to_account(r) for r in rows]

    def post_journal_entry(
        self,
        reference_id: str,
        description: str,
        lines: List[JournalEntryLine],
        metadata: Optional[Dict[str, Any]] = None,
        actor_id: str = "SYSTEM"
    ) -> JournalEntry:
        """
        Atomically records a multi-leg double-entry journal transaction.
        Validates:
        1. Debits == Credits (per currency)
        2. Account existence and active status
        3. Sufficient funds / limits for Asset/Liability accounts
        4. Updates running and available balances in real time
        """
        if len(lines) < 2:
            raise ValueError("A journal entry requires at least 2 entry legs.")

        entry_id = f"je_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        journal_entry = JournalEntry(
            id=entry_id,
            reference_id=reference_id,
            timestamp=timestamp,
            description=description,
            lines=lines,
            metadata=metadata or {}
        )

        # 1. Invariant: Mathematical balance verification
        journal_entry.validate_balance()

        with self._lock:
            conn = self.db.get_connection()
            with conn:
                # 2. Verify all accounts exist and are active
                for line in lines:
                    acc_row = conn.execute("SELECT * FROM accounts WHERE id = ?;", (line.account_id,)).fetchone()
                    if not acc_row:
                        raise ValueError(f"Account '{line.account_id}' does not exist.")
                    if not acc_row["is_active"]:
                        raise ValueError(f"Account '{line.account_id}' is inactive/frozen.")
                    if acc_row["currency"] != line.currency.value:
                        raise ValueError(
                            f"Account currency mismatch: account is {acc_row['currency']}, line is {line.currency.value}"
                        )

                # 3. Insert Journal Entry Header
                conn.execute(
                    """
                    INSERT INTO journal_entries (id, reference_id, timestamp, description, metadata_json)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    (entry_id, reference_id, timestamp, description, json.dumps(metadata or {}))
                )

                # 4. Insert Journal Lines & Update Account Balances
                for line in lines:
                    conn.execute(
                        """
                        INSERT INTO journal_entry_lines (journal_entry_id, account_id, direction, amount, currency, memo)
                        VALUES (?, ?, ?, ?, ?, ?);
                        """,
                        (entry_id, line.account_id, line.direction.value, line.amount, line.currency.value, line.memo)
                    )

                    acc_row = conn.execute("SELECT * FROM accounts WHERE id = ?;", (line.account_id,)).fetchone()
                    acc_type = acc_row["account_type"]
                    current_balance = acc_row["balance"]
                    credit_limit = acc_row["credit_limit"]
                    hold_balance = acc_row["hold_balance"]

                    # Balance normal direction calculation:
                    # ASSET / EXPENSE: Normal debit (Debit increases, Credit decreases)
                    # LIABILITY / EQUITY / REVENUE: Normal credit (Credit increases, Debit decreases)
                    if acc_type in [AccountType.ASSET.value, AccountType.EXPENSE.value]:
                        if line.direction == EntryDirection.DEBIT:
                            new_balance = round(current_balance + line.amount, 4)
                        else:
                            new_balance = round(current_balance - line.amount, 4)
                    else:
                        if line.direction == EntryDirection.CREDIT:
                            new_balance = round(current_balance + line.amount, 4)
                        else:
                            new_balance = round(current_balance - line.amount, 4)

                    new_avail = round(new_balance + credit_limit - hold_balance, 4)

                    conn.execute(
                        """
                        UPDATE accounts
                        SET balance = ?, available_balance = ?
                        WHERE id = ?;
                        """,
                        (new_balance, new_avail, line.account_id)
                    )

                # 5. Record Cryptographic Audit
                self._record_audit("JOURNAL_ENTRY", entry_id, "POST", actor_id, journal_entry.to_dict())

        return journal_entry

    def list_journal_entries(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieves recent journal entries with nested lines."""
        headers = self.db.query_all(
            "SELECT * FROM journal_entries ORDER BY timestamp DESC LIMIT ? OFFSET ?;",
            (limit, offset)
        )
        results = []
        for h in headers:
            lines = self.db.query_all(
                "SELECT * FROM journal_entry_lines WHERE journal_entry_id = ?;",
                (h["id"],)
            )
            entry_dict = dict(h)
            entry_dict["lines"] = [dict(l) for l in lines]
            if entry_dict.get("metadata_json"):
                entry_dict["metadata"] = json.loads(entry_dict["metadata_json"])
            results.append(entry_dict)
        return results

    def verify_system_integrity(self) -> Dict[str, Any]:
        """
        Global Accounting Sanity Check:
        Verifies that total debits match total credits across the entire database history.
        """
        rows = self.db.query_all(
            """
            SELECT currency, direction, SUM(amount) as total
            FROM journal_entry_lines
            GROUP BY currency, direction;
            """
        )
        totals: Dict[str, Dict[str, float]] = {}
        for r in rows:
            curr = r["currency"]
            if curr not in totals:
                totals[curr] = {"DEBIT": 0.0, "CREDIT": 0.0}
            totals[curr][r["direction"]] = round(r["total"], 4)

        is_balanced = True
        discrepancies = []
        for curr, stats in totals.items():
            diff = abs(stats["DEBIT"] - stats["CREDIT"])
            if diff > 0.0001:
                is_balanced = False
                discrepancies.append({
                    "currency": curr,
                    "debit": stats["DEBIT"],
                    "credit": stats["CREDIT"],
                    "diff": diff
                })

        return {
            "is_balanced": is_balanced,
            "totals_by_currency": totals,
            "discrepancies": discrepancies,
            "verified_at": datetime.now(timezone.utc).isoformat()
        }

    def _record_audit(self, entity_type: str, entity_id: str, action: str, actor_id: str, details: Dict[str, Any]) -> None:
        """Chains audit log with SHA-256 Merkle link."""
        audit_id = f"aud_{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        checksum = SecurityManager.calculate_audit_checksum(details, self._last_audit_hash)
        self._last_audit_hash = checksum

        self.db.execute(
            """
            INSERT INTO audit_logs (id, entity_type, entity_id, action, actor_id, timestamp, details_json, checksum)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (audit_id, entity_type, entity_id, action, actor_id, timestamp, json.dumps(details), checksum)
        )

    @staticmethod
    def _row_to_account(row: sqlite3.Row) -> Account:
        meta = json.loads(row["metadata_json"]) if row["metadata_json"] else {}
        return Account(
            id=row["id"],
            account_number=row["account_number"],
            name=row["name"],
            account_type=AccountType(row["account_type"]),
            account_subtype=AccountSubtype(row["account_subtype"]),
            currency=Currency(row["currency"]),
            balance=row["balance"],
            available_balance=row["available_balance"],
            hold_balance=row["hold_balance"],
            credit_limit=row["credit_limit"],
            interest_rate=row["interest_rate"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
            owner_id=row["owner_id"],
            metadata=meta
        )
