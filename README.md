# Fintech Enterprise Core Banking & Trading Engine

An enterprise-grade, high-throughput financial technology platform built strictly using **Python Standard Library (zero third-party dependencies / zero open-source package licenses)** on the backend and **Vanilla JavaScript (ES6+), HTML5, and CSS3** on the frontend.

---

## 1. Table of Contents
1. [Architecture & Subsystems](#architecture--subsystems)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [Build Instructions](#build-instructions)
5. [Run Instructions](#run-instructions)
6. [Usage & Verification](#usage--verification)
7. [Docker & Containerization](#docker--containerization)
8. [Ownership & Compliance](#ownership--compliance)

---

## 2. Architecture & Subsystems

- **Double-Entry General Ledger**: Mathematical debit/credit balance verification ($\sum \text{Debits} = \sum \text{Credits}$) with SHA-256 Merkle-tree hash chaining.
- **Multi-Rail Payment Gateway**: Native routing across Internal accounts, Fedwire/SWIFT, ACH, and Credit Card authorizations with Luhn checks and PAN masking (`4111-11XX-XXXX-4444`).
- **Continuous Limit Order Book (LOB)**: Price-time priority order matching engine supporting Limit/Market orders and multi-currency pairs (BTC/USD, ETH/USD, EUR/USD, GBP/USD).
- **Fraud Detection & AML Risk**: Real-time heuristic scoring, velocity spike monitoring, structuring anomaly flags, and sanctions screening.
- **Quantitative Pricing & Risk**: Black-Scholes-Merton options pricing, Greeks, Monte Carlo simulations, and Basel III Capital Adequacy / RWA calculations.
- **Financial Standards & Formats**: ISO 20022 (pacs/pain/camt), FIX 4.4/5.0, SWIFT MT/MX, and NACHA ACH engines.

---

## 3. Dependencies

- **Runtime**: Python 3.8+ (Pure Python Standard Library).
- **Package Manifests**:
  - `requirements.txt`: Standard library declarations.
  - `pyproject.toml` & `poetry.lock`: Poetry environment specifications.
  - `package.json` & `package-lock.json`: Scripts and frontend metadata.
- **Third-Party Libraries**: Zero external packages required (`sqlite3`, `http.server`, `math`, `hashlib`, `unittest` are all built into Python).

---

## 4. Installation

### Option A: Standard Python Environment
```powershell
# 1. Clone or navigate to the repository
cd E:\Fintech

# 2. (Optional) Create and activate a clean virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Verify Python runtime
python --version
```

### Option B: Node / NPM Tooling
```powershell
npm install
```

---

## 5. Build Instructions

To compile and validate all application modules:
```powershell
# Using Python
python -c "import compileall; compileall.compile_dir('.', force=True, quiet=1)"

# Or using Makefile
make build

# Or using NPM script
npm run build
```

---

## 6. Run Instructions

### Starting the Web Platform
```powershell
# Direct launch
python main.py

# Or via Makefile
make run

# Or via NPM
npm start

# Or using the Windows launcher batch script
.\run.bat
```

Once started, open your web browser and navigate to:
👉 **`http://127.0.0.1:8080`**

---

## 7. Usage & Verification

### Running Automated Test Suite
```powershell
python -m unittest discover -s tests -v
```

### Running High-Throughput Stress Testing
```powershell
python cli.py stress --count 100
```

### Auditing Double-Entry Invariants
```powershell
python cli.py verify
```

---

## 8. Docker & Containerization

### Build Docker Image
```bash
docker build -t fintech-enterprise-platform:latest .
```

### Run Container
```bash
docker run -d -p 8080:8080 --name fintech_app fintech-enterprise-platform:latest
```

### Docker Compose
```bash
docker-compose up -d
```

---

## 9. Ownership & Compliance
- **Proprietary & Confidential**: Zero open-source license restrictions (zero GPL / zero Apache).
- **Zero Sensitive Data**: All customer and market data is 100% synthetically generated and PCI-DSS compliant.
