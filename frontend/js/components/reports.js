/**
 * Financial Statements & Reporting Component
 * Generates Balance Sheet, Profit & Loss (P&L), and Trial Balance.
 */

const ReportsComponent = {
  async render() {
    const container = document.getElementById("tab-reports");
    if (!container) return;

    try {
      const [bsData, isData, tbData] = await Promise.all([
        Api.getBalanceSheet(),
        Api.getIncomeStatement(),
        Api.getTrialBalance()
      ]);

      container.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
          <div>
            <h2 style="font-size: 20px; font-weight: 700;">Financial Statements & Regulatory Reporting</h2>
            <p style="font-size: 13px; color: var(--text-secondary);">
              GAAP/IFRS-Compliant Double-Entry Aggregations (Live System Ledger)
            </p>
          </div>
          <button class="btn btn-primary" onclick="ReportsComponent.runInterest()">
            ⚡ Run Daily Compound Interest Batch
          </button>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px;">
          <!-- Balance Sheet -->
          <div class="card-panel">
            <div class="panel-header">
              <h3 class="panel-title">Balance Sheet</h3>
              <span class="font-mono" style="font-size: 12px; color: var(--text-secondary);">
                Net Worth: $${bsData.net_worth.toLocaleString(undefined, {minimumFractionDigits: 2})}
              </span>
            </div>

            <!-- Assets -->
            <div style="margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; font-weight: 700; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; margin-bottom: 8px;">
                <span>ASSETS</span>
                <span class="font-mono" style="color: var(--success);">$${bsData.assets.total.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
              </div>
              ${bsData.assets.items.map(i => `
                <div style="display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; color: var(--text-secondary);">
                  <span>${i.name}</span>
                  <span class="font-mono" style="color: var(--text-primary);">$${i.balance.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
                </div>
              `).join("")}
            </div>

            <!-- Liabilities -->
            <div style="margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; font-weight: 700; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; margin-bottom: 8px;">
                <span>LIABILITIES (Customer Deposits)</span>
                <span class="font-mono" style="color: var(--danger);">$${bsData.liabilities.total.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
              </div>
              ${bsData.liabilities.items.map(i => `
                <div style="display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; color: var(--text-secondary);">
                  <span>${i.name}</span>
                  <span class="font-mono" style="color: var(--text-primary);">$${i.balance.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
                </div>
              `).join("")}
            </div>
          </div>

          <!-- Income Statement (P&L) -->
          <div class="card-panel">
            <div class="panel-header">
              <h3 class="panel-title">Income Statement (P&L)</h3>
              <span class="font-mono" style="font-size: 12px; font-weight: 700; color: ${isData.net_income >= 0 ? 'var(--success)' : 'var(--danger)'};">
                Net Income: $${isData.net_income.toLocaleString(undefined, {minimumFractionDigits: 2})}
              </span>
            </div>

            <!-- Revenues -->
            <div style="margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; font-weight: 700; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; margin-bottom: 8px;">
                <span>REVENUE</span>
                <span class="font-mono" style="color: var(--success);">$${isData.revenues.total.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
              </div>
              ${isData.revenues.items.map(i => `
                <div style="display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; color: var(--text-secondary);">
                  <span>${i.name}</span>
                  <span class="font-mono" style="color: var(--text-primary);">$${i.amount.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
                </div>
              `).join("")}
            </div>

            <!-- Expenses -->
            <div style="margin-bottom: 16px;">
              <div style="display: flex; justify-content: space-between; font-weight: 700; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; margin-bottom: 8px;">
                <span>OPERATING EXPENSES</span>
                <span class="font-mono" style="color: var(--warning);">$${isData.expenses.total.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
              </div>
              ${isData.expenses.items.map(i => `
                <div style="display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; color: var(--text-secondary);">
                  <span>${i.name}</span>
                  <span class="font-mono" style="color: var(--text-primary);">$${i.amount.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
                </div>
              `).join("")}
            </div>
          </div>
        </div>

        <!-- Trial Balance -->
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <h3 class="panel-title">Trial Balance Invariant Audit</h3>
              <span style="font-size: 12px; color: var(--text-secondary);">
                Ensures total debit balance equals total credit balance
              </span>
            </div>
            <div>
              <span class="badge ${tbData.is_balanced ? 'badge-success' : 'badge-danger'}">
                Total Debits: $${tbData.total_debits.toLocaleString(undefined, {minimumFractionDigits: 2})} | Total Credits: $${tbData.total_credits.toLocaleString(undefined, {minimumFractionDigits: 2})}
              </span>
            </div>
          </div>

          <div class="table-responsive">
            <table class="fin-table">
              <thead>
                <tr>
                  <th>Account Number</th>
                  <th>Account Name</th>
                  <th>Type</th>
                  <th>Debit Balance</th>
                  <th>Credit Balance</th>
                </tr>
              </thead>
              <tbody>
                ${tbData.accounts.map(a => `
                  <tr>
                    <td class="font-mono">${a.account_number}</td>
                    <td><strong>${a.name}</strong></td>
                    <td><span class="badge badge-info">${a.account_type}</span></td>
                    <td class="font-mono" style="color: ${a.debit > 0 ? 'var(--primary)' : 'var(--text-muted)'};">
                      $${a.debit.toLocaleString(undefined, {minimumFractionDigits: 2})}
                    </td>
                    <td class="font-mono" style="color: ${a.credit > 0 ? 'var(--success)' : 'var(--text-muted)'};">
                      $${a.credit.toLocaleString(undefined, {minimumFractionDigits: 2})}
                    </td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div class="toast toast-error">Failed to load reports: ${err.message}</div>`;
    }
  },

  async runInterest() {
    try {
      const res = await Api.accrueInterest();
      App.showToast(`Batch completed: ${res.accruals_posted} interest accrual(s) posted to general ledger`, "success");
      this.render();
      App.refreshKPIs();
    } catch (err) {
      App.showToast(err.message, "error");
    }
  }
};
