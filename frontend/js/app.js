/**
 * Fintech Main Application Controller
 * Handles tab navigation, KPI cards refresh, toast notification system, and initial bootstrap.
 */

const App = {
  activeTab: "overview",

  init() {
    this.setupNavigation();
    this.refreshKPIs();
    this.loadAccountsList();
  },

  setupNavigation() {
    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(item => {
      item.addEventListener("click", () => {
        const tab = item.getAttribute("data-tab");
        this.switchTab(tab);
      });
    });
  },

  switchTab(tabName) {
    this.activeTab = tabName;

    // Update active class on nav
    document.querySelectorAll(".nav-item").forEach(el => {
      if (el.getAttribute("data-tab") === tabName) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    });

    // Update active tab content
    document.querySelectorAll(".tab-content").forEach(el => {
      if (el.id === `tab-${tabName}`) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    });

    // Update Title
    const titleMap = {
      overview: "Executive Overview & Core Banking KPIs",
      accounts: "Accounts & Balances Portfolio",
      ledger: "Double-Entry General Ledger",
      payments: "Money Movement & Payment Routing",
      trading: "Multi-Asset & FX Trading Terminal",
      risk: "Fraud & AML Risk Console",
      reports: "Financial Statements & Analytics"
    };
    document.getElementById("page-title-text").innerText = titleMap[tabName] || "Dashboard";

    // Lazy load tab components
    if (tabName === "overview") {
      this.refreshKPIs();
      this.loadAccountsList();
    } else if (tabName === "accounts") {
      this.loadAccountsList();
    } else if (tabName === "ledger") {
      LedgerComponent.render();
    } else if (tabName === "payments") {
      PaymentsComponent.render();
    } else if (tabName === "trading") {
      TradingComponent.render();
    } else if (tabName === "risk") {
      RiskComponent.render();
    } else if (tabName === "reports") {
      ReportsComponent.render();
    }
  },

  async refreshKPIs() {
    try {
      const kpi = await Api.getKPIs();
      document.getElementById("kpi-accounts").innerText = kpi.total_accounts || 0;
      document.getElementById("kpi-tx-count").innerText = (kpi.total_transactions || 0).toLocaleString();
      document.getElementById("kpi-volume").innerText = `$${(kpi.total_volume_processed || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
      document.getElementById("kpi-revenue").innerText = `$${(kpi.total_fee_revenue || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
      document.getElementById("kpi-trades").innerText = `${kpi.total_trades || 0} ($${(kpi.trade_volume || 0).toLocaleString(undefined, {minimumFractionDigits: 2})})`;
    } catch (err) {
      console.error("KPI refresh failed:", err);
    }
  },

  async loadAccountsList() {
    try {
      const data = await Api.getAccounts();
      const accounts = data.accounts || [];

      // Render accounts table in Accounts tab
      const accContainer = document.getElementById("accounts-table-body");
      if (accContainer) {
        accContainer.innerHTML = accounts.map(a => `
          <tr>
            <td class="font-mono"><strong>${a.account_number}</strong></td>
            <td><strong>${a.name}</strong></td>
            <td><span class="badge badge-info">${a.account_type}</span></td>
            <td>${a.account_subtype}</td>
            <td class="font-mono">${a.currency}</td>
            <td class="font-mono" style="font-weight: 700;">$${a.balance.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
            <td class="font-mono" style="color: var(--success);">$${a.available_balance.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
            <td>${(a.interest_rate * 100).toFixed(2)}%</td>
            <td><span class="badge badge-success">ACTIVE</span></td>
          </tr>
        `).join("");
      }

      // Also render overview recent accounts table
      const overviewAccContainer = document.getElementById("overview-accounts-body");
      if (overviewAccContainer) {
        overviewAccContainer.innerHTML = accounts.slice(0, 5).map(a => `
          <tr>
            <td class="font-mono"><strong>${a.account_number}</strong></td>
            <td>${a.name}</td>
            <td><span class="badge badge-info">${a.account_subtype}</span></td>
            <td class="font-mono" style="font-weight: 600;">$${a.available_balance.toLocaleString(undefined, {minimumFractionDigits: 2})} ${a.currency}</td>
          </tr>
        `).join("");
      }
    } catch (err) {
      console.error("Failed to load accounts:", err);
    }
  },

  async handleCreateAccount(event) {
    event.preventDefault();
    const name = document.getElementById("new-acc-name").value;
    const type = document.getElementById("new-acc-type").value;
    const subtype = document.getElementById("new-acc-subtype").value;
    const currency = document.getElementById("new-acc-curr").value;
    const rate = parseFloat(document.getElementById("new-acc-apy").value || 0) / 100.0;

    try {
      const res = await Api.createAccount({
        name,
        account_type: type,
        account_subtype: subtype,
        currency,
        interest_rate: rate
      });
      this.showToast(`Account created: ${res.name} (${res.account_number})`, "success");
      document.getElementById("create-account-form").reset();
      this.loadAccountsList();
      this.refreshKPIs();
    } catch (err) {
      this.showToast(err.message, "error");
    }
  },

  async seedData() {
    try {
      const res = await Api.seedData();
      this.showToast(res.message, "success");
      this.refreshKPIs();
      this.loadAccountsList();
      if (this.activeTab !== "overview") {
        this.switchTab(this.activeTab);
      }
    } catch (err) {
      this.showToast(err.message, "error");
    }
  },

  showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.innerText = message;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(20px)";
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }
};

window.addEventListener("DOMContentLoaded", () => {
  App.init();
});
