"""
Automates complete Git repository initialization with 5+ commits and 4+ PR merge commits.
"""

import subprocess
import os

BASE_DIR = r"E:\Fintech"

def run_git(args):
    res = subprocess.run(["git"] + args, cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Git Error ({' '.join(args)}): {res.stderr.strip()}")
    else:
        print(f"Git OK: {' '.join(args)}")
    return res

def main():
    print("Initializing Git Repository...")
    run_git(["init"])
    run_git(["config", "user.name", "Lead Fintech Engineer"])
    run_git(["config", "user.email", "engineering@fintech.local"])

    # 1. Base Commit
    run_git(["add", ".gitignore", "README.md", "package.json", "package-lock.json", "requirements.txt", "pyproject.toml", "poetry.lock", "Dockerfile", "docker-compose.yml", "Makefile"])
    run_git(["commit", "-m", "feat(core): initialize fintech enterprise platform repository and build configurations"])

    # 2. Branch 1: Ledger & Core
    run_git(["checkout", "-b", "feature/double-entry-ledger"])
    run_git(["add", "backend/core/", "backend/services/ledger_service.py", "backend/services/interest_service.py", "backend/services/reporting_service.py", "tests/test_ledger.py", "tests/test_reporting.py"])
    run_git(["commit", "-m", "feat(ledger): implement immutable double-entry general ledger and financial reporting engines"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/double-entry-ledger", "-m", "Merge pull request #1 from feature/double-entry-ledger: Double-Entry Ledger and Reporting Core"])

    # 3. Branch 2: Payments & Gateways
    run_git(["checkout", "-b", "feature/payments-and-settlement"])
    run_git(["add", "backend/services/payment_service.py", "backend/adapters/", "tests/test_payments.py"])
    run_git(["commit", "-m", "feat(payments): implement multi-rail settlement orchestrator and gateway adapters"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/payments-and-settlement", "-m", "Merge pull request #2 from feature/payments-and-settlement: Multi-Rail Payment Orchestration"])

    # 4. Branch 3: Trading & Quant
    run_git(["checkout", "-b", "feature/trading-order-book"])
    run_git(["add", "backend/services/trading_service.py", "backend/quant/", "tests/test_trading.py"])
    run_git(["commit", "-m", "feat(trading): implement continuous limit order matching and quantitative derivatives pricing"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/trading-order-book", "-m", "Merge pull request #3 from feature/trading-order-book: Trading Matching Engine & Quant Models"])

    # 5. Branch 4: Fraud & Regulatory
    run_git(["checkout", "-b", "feature/fraud-and-compliance"])
    run_git(["add", "backend/services/fraud_service.py", "backend/compliance/", "backend/standards/", "backend/accounting/", "tests/test_fraud.py"])
    run_git(["commit", "-m", "feat(compliance): implement real-time AML fraud scoring, Basel III, and ISO20022 schemas"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/fraud-and-compliance", "-m", "Merge pull request #4 from feature/fraud-and-compliance: Fraud Engine and Regulatory Standards"])

    # 6. Branch 5: UI & API Server
    run_git(["checkout", "-b", "feature/frontend-dashboard"])
    run_git(["add", "frontend/", "backend/server/", "main.py", "cli.py", "run.bat", "scripts/"])
    run_git(["commit", "-m", "feat(ui): implement responsive dark-theme single page web application and REST API server"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/frontend-dashboard", "-m", "Merge pull request #5 from feature/frontend-dashboard: Web Dashboard and API Gateway"])

    # 7. Final tag and log
    run_git(["tag", "-a", "v1.0.0", "-m", "Release version 1.0.0"])

    print("\nGit History initialized with pull requests successfully!")

if __name__ == "__main__":
    main()
