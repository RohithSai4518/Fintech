"""
Fintech Database Layer
Thread-safe ACID relational storage with schema migrations and query helpers.
Zero external library dependencies (uses Python standard library sqlite3).
"""

import sqlite3
import threading
import json
import os
from typing import List, Dict, Any, Optional, Tuple


class DatabaseManager:
    """Thread-safe SQLite database manager for the Fintech Core Platform."""

    _instance = None
    _lock = threading.Lock()

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._local = threading.local()
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        """Provides a thread-local SQLite connection with foreign keys and WAL mode."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            # If folder path doesn't exist, create it
            if self.db_path != ":memory:":
                os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("PRAGMA journal_mode = WAL;")
            conn.execute("PRAGMA synchronous = NORMAL;")
            self._local.conn = conn
        return self._local.conn

    def _init_schema(self) -> None:
        """Creates the relational schema with constraints, foreign keys, and indexes."""
        conn = self.get_connection()
        with conn:
            # Users / Entities Table
            conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'CUSTOMER',
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
            """)

            # Seed system user
            conn.execute("""
            INSERT OR IGNORE INTO users (id, username, email, password_hash, salt, role, is_active, created_at)
            VALUES ('SYSTEM', 'system_daemon', 'system@fintech.local', 'n/a', 'n/a', 'ADMIN', 1, '2026-01-01T00:00:00Z');
            """)

            # Accounts Table (Chart of Accounts / Customer Accounts)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id TEXT PRIMARY KEY,
                account_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                account_type TEXT NOT NULL,
                account_subtype TEXT NOT NULL,
                currency TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0.0,
                available_balance REAL NOT NULL DEFAULT 0.0,
                hold_balance REAL NOT NULL DEFAULT 0.0,
                credit_limit REAL NOT NULL DEFAULT 0.0,
                interest_rate REAL NOT NULL DEFAULT 0.0,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                owner_id TEXT,
                metadata_json TEXT,
                FOREIGN KEY(owner_id) REFERENCES users(id)
            );
            """)

            # Journal Entries (Header table for Double-Entry Accounting)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id TEXT PRIMARY KEY,
                reference_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                description TEXT NOT NULL,
                metadata_json TEXT
            );
            """)

            # Journal Entry Lines (Debit & Credit legs)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS journal_entry_lines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                journal_entry_id TEXT NOT NULL,
                account_id TEXT NOT NULL,
                direction TEXT NOT NULL, -- 'DEBIT' or 'CREDIT'
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                memo TEXT,
                FOREIGN KEY(journal_entry_id) REFERENCES journal_entries(id) ON DELETE CASCADE,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            );
            """)

            # Transactions (High-level business payment operations)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                source_account_id TEXT,
                destination_account_id TEXT,
                amount REAL NOT NULL,
                fee REAL NOT NULL DEFAULT 0.0,
                currency TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                status TEXT NOT NULL,
                idempotency_key TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                risk_score REAL NOT NULL DEFAULT 0.0,
                risk_level TEXT NOT NULL DEFAULT 'LOW',
                created_at TEXT NOT NULL,
                settled_at TEXT,
                failure_reason TEXT,
                metadata_json TEXT,
                FOREIGN KEY(source_account_id) REFERENCES accounts(id),
                FOREIGN KEY(destination_account_id) REFERENCES accounts(id)
            );
            """)

            # Orders (Trading & FX Limit/Market Orders)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                account_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                order_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                filled_quantity REAL NOT NULL DEFAULT 0.0,
                price REAL,
                average_fill_price REAL NOT NULL DEFAULT 0.0,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            );
            """)

            # Trades Execution Log
            conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                buy_order_id TEXT NOT NULL,
                sell_order_id TEXT NOT NULL,
                price REAL NOT NULL,
                quantity REAL NOT NULL,
                executed_at TEXT NOT NULL
            );
            """)

            # Fraud Detection Rules
            conn.execute("""
            CREATE TABLE IF NOT EXISTS fraud_rules (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                rule_type TEXT NOT NULL,
                threshold REAL NOT NULL,
                action TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                description TEXT
            );
            """)

            # Cryptographically chained Audit Logs (Merkle / Chained hashes)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id TEXT PRIMARY KEY,
                entity_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                action TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                details_json TEXT NOT NULL,
                checksum TEXT NOT NULL
            );
            """)

            # Performance Indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_acc_num ON accounts(account_number);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_acc_owner ON accounts(owner_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jel_entry ON journal_entry_lines(journal_entry_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jel_acc ON journal_entry_lines(account_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tx_src ON transactions(source_account_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tx_dst ON transactions(destination_account_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tx_idem ON transactions(idempotency_key);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_tx_created ON transactions(created_at);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_sym ON orders(symbol, status);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_logs(timestamp);")

    def execute(self, sql: str, params: Tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """Executes a single SQL query and commits."""
        conn = self.get_connection()
        with conn:
            cursor = conn.execute(sql, params)
            return cursor

    def query_all(self, sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """Queries multiple rows and returns as a list of dictionaries."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def query_one(self, sql: str, params: Tuple[Any, ...] = ()) -> Optional[Dict[str, Any]]:
        """Queries a single row and returns as a dictionary or None."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
