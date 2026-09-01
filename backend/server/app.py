"""
Fintech Platform HTTP Server Application
Zero external dependencies (pure Python standard library).
Provides REST API endpoints and serves responsive frontend static assets.
"""

import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.core.database import DatabaseManager
from backend.core.idempotency import IdempotencyManager
from backend.services.ledger_service import LedgerService
from backend.services.payment_service import PaymentService
from backend.services.trading_service import TradingService
from backend.services.fraud_service import FraudService
from backend.services.interest_service import InterestService
from backend.services.reporting_service import ReportingService
from backend.server.router import Router, HTTPResponse
from backend.server.handlers import APIHandlerContainer


def create_app(db_path: str = "fintech_core.db") -> tuple:
    """Factory creating and wiring all platform components."""
    db = DatabaseManager(db_path=db_path)
    idempotency = IdempotencyManager()
    ledger = LedgerService(db=db)
    fraud = FraudService(db=db)
    payments = PaymentService(db=db, ledger_service=ledger, fraud_service=fraud, idempotency_manager=idempotency)
    trading = TradingService(db=db, ledger_service=ledger)
    interest = InterestService(db=db, ledger_service=ledger)
    reporting = ReportingService(db=db)

    handlers = APIHandlerContainer(
        db=db,
        ledger_service=ledger,
        payment_service=payments,
        trading_service=trading,
        fraud_service=fraud,
        interest_service=interest,
        reporting_service=reporting
    )

    router = Router()

    # Register API Routes
    router.add_route("POST", "/api/seed", handlers.handle_seed_data)
    router.add_route("GET", "/api/kpis", handlers.handle_get_kpis)
    router.add_route("GET", "/api/accounts", handlers.handle_list_accounts)
    router.add_route("POST", "/api/accounts", handlers.handle_create_account)
    router.add_route("GET", "/api/accounts/:id", handlers.handle_get_account)

    router.add_route("GET", "/api/ledger/entries", handlers.handle_list_journal_entries)
    router.add_route("GET", "/api/ledger/verify", handlers.handle_verify_ledger_integrity)

    router.add_route("POST", "/api/payments", handlers.handle_process_payment)
    router.add_route("GET", "/api/transactions", handlers.handle_list_transactions)

    router.add_route("GET", "/api/trading/prices", handlers.handle_get_market_prices)
    router.add_route("GET", "/api/trading/orderbook/:symbol", handlers.handle_get_order_book)
    router.add_route("GET", "/api/trading/orders", handlers.handle_list_orders)
    router.add_route("POST", "/api/trading/orders", handlers.handle_submit_order)
    router.add_route("GET", "/api/trading/trades", handlers.handle_list_trades)

    router.add_route("GET", "/api/fraud/rules", handlers.handle_list_fraud_rules)
    router.add_route("POST", "/api/fraud/rules", handlers.handle_create_fraud_rule)

    router.add_route("GET", "/api/reports/trial-balance", handlers.handle_get_trial_balance)
    router.add_route("GET", "/api/reports/balance-sheet", handlers.handle_get_balance_sheet)
    router.add_route("GET", "/api/reports/income-statement", handlers.handle_get_income_statement)
    router.add_route("POST", "/api/interest/accrue", handlers.handle_run_interest_accrual)

    return router, handlers


class FintechHTTPHandler(BaseHTTPRequestHandler):
    """Custom HTTP request handler with CORS support and static file serving."""

    router: Router = None
    frontend_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        params = {k: v[0] if len(v) == 1 else v for k, v in query.items()}

        if path.startswith("/api/"):
            req_data = {"params": params, "headers": dict(self.headers)}
            res = self.router.dispatch("GET", path, req_data)
            self._write_response(res)
        else:
            self._serve_static(path)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        params = {k: v[0] if len(v) == 1 else v for k, v in query.items()}

        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            body = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        except Exception:
            body = {}

        req_data = {"params": params, "body": body, "headers": dict(self.headers)}
        res = self.router.dispatch("POST", path, req_data)
        self._write_response(res)

    def _write_response(self, res: HTTPResponse):
        self.send_response(res.status)
        self._send_cors_headers()
        for h, v in res.headers.items():
            self.send_header(h, v)
        self.end_headers()
        self.wfile.write(res.body)

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Idempotency-Key")

    def _serve_static(self, path: str):
        if path == "/" or path == "":
            path = "/index.html"
        
        # Remove leading slash for local path resolution
        rel_path = path.lstrip("/")
        file_path = os.path.join(self.frontend_dir, rel_path)

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"File not found: {path}".encode('utf-8'))
            return

        content_type = "text/plain"
        if file_path.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif file_path.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        elif file_path.endswith(".js"):
            content_type = "application/javascript; charset=utf-8"
        elif file_path.endswith(".json"):
            content_type = "application/json"
        elif file_path.endswith(".svg"):
            content_type = "image/svg+xml"

        with open(file_path, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # Override to suppress noisy default logging or format cleanly
        pass


def run_server(host: str = "127.0.0.1", port: int = 8080, db_path: str = "fintech_core.db"):
    router, handlers = create_app(db_path=db_path)
    FintechHTTPHandler.router = router

    # Pre-seed initial sample data on startup
    handlers.handle_seed_data({})

    server = HTTPServer((host, port), FintechHTTPHandler)
    print(f"================================================================")
    print(f"   FINTECH ENTERPRISE PLATFORM (Core Banking & Trading Engine)   ")
    print(f"================================================================")
    print(f" Server running at: http://{host}:{port}/")
    print(f" REST API Base:     http://{host}:{port}/api/")
    print(f" Press Ctrl+C to stop the server.")
    print(f"================================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.server_close()


if __name__ == "__main__":
    run_server()
