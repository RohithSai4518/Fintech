"""
Fintech Enterprise Core Platform Entrypoint
Zero external library dependencies (pure Python standard library).
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.server.app import run_server


def main():
    """Main application entry point."""
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "127.0.0.1")
    db_path = os.environ.get("DB_PATH", "fintech_core.db")
    run_server(host=host, port=port, db_path=db_path)


if __name__ == "__main__":
    main()
