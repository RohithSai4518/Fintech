/**
 * Fintech Client API Service
 * Pure JavaScript Fetch Wrapper (Zero External Dependencies)
 */

const API_BASE = "/api";

const Api = {
  async get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString();
    const url = `${API_BASE}${endpoint}${query ? `?${query}` : ""}`;
    const res = await fetch(url, {
      method: "GET",
      headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: "Request failed" }));
      throw new Error(err.details || err.error || `HTTP ${res.status}`);
    }
    return res.json();
  },

  async post(endpoint, body = {}, headers = {}) {
    const url = `${API_BASE}${endpoint}`;
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...headers
      },
      body: JSON.stringify(body)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: "Request failed" }));
      throw new Error(err.details || err.error || `HTTP ${res.status}`);
    }
    return res.json();
  },

  // Seed Initial Environment
  seedData() {
    return this.post("/seed", {});
  },

  // KPI Dashboard
  getKPIs() {
    return this.get("/kpis");
  },

  // Accounts
  getAccounts() {
    return this.get("/accounts");
  },

  createAccount(data) {
    return this.post("/accounts", data);
  },

  // General Ledger
  getJournalEntries(limit = 50) {
    return this.get("/ledger/entries", { limit });
  },

  verifyLedger() {
    return this.get("/ledger/verify");
  },

  // Payments & Transfers
  processPayment(paymentData) {
    return this.post("/payments", paymentData);
  },

  getTransactions(limit = 50) {
    return this.get("/transactions", { limit });
  },

  // Trading & FX
  getMarketPrices() {
    return this.get("/trading/prices");
  },

  getOrderBook(symbol) {
    return this.get(`/trading/orderbook/${encodeURIComponent(symbol)}`);
  },

  submitOrder(orderData) {
    return this.post("/trading/orders", orderData);
  },

  getTrades() {
    return this.get("/trading/trades");
  },

  // Fraud & Risk
  getFraudRules() {
    return this.get("/fraud/rules");
  },

  createFraudRule(ruleData) {
    return this.post("/fraud/rules", ruleData);
  },

  // Financial Reports
  getTrialBalance() {
    return this.get("/reports/trial-balance");
  },

  getBalanceSheet() {
    return this.get("/reports/balance-sheet");
  },

  getIncomeStatement() {
    return this.get("/reports/income-statement");
  },

  accrueInterest() {
    return this.post("/interest/accrue", {});
  }
};
