/**
 * Ledger Component
 * Visualizes double-entry journal transactions, debit/credit legs, and mathematical integrity.
 */

const LedgerComponent = {
  async render() {
    const container = document.getElementById("tab-ledger");
    if (!container) return;

    try {
      const [entriesData, integrityData] = await Promise.all([
        Api.getJournalEntries(30),
        Api.verifyLedger()
      ]);

      const entries = entriesData.journal_entries || [];
      const isBalanced = integrityData.is_balanced;

      let totalsHtml = "";
      for (const [curr, stats] of Object.entries(integrityData.totals_by_currency || {})) {
        totalsHtml += `<span class="badge ${isBalanced ? 'badge-success' : 'badge-danger'}" style="margin-left: 8px;">
          ${curr}: Dr $${stats.DEBIT.toLocaleString()} | Cr $${stats.CREDIT.toLocaleString()}
        </span>`;
      }

      container.innerHTML = `
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <h2 class="panel-title">Immutable Double-Entry General Ledger</h2>
              <p style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                Strict multi-leg debit and credit invariant checking (Assets = Liabilities + Equity)
              </p>
            </div>
            <div>
              <span class="badge ${isBalanced ? 'badge-success' : 'badge-danger'}">
                ${isBalanced ? '✓ System Invariant Balanced' : '⚠ Balance Imbalance'}
              </span>
              ${totalsHtml}
            </div>
          </div>

          <div class="table-responsive">
            <table class="fin-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Reference ID</th>
                  <th>Description</th>
                  <th>Journal Legs (Account | Direction | Amount)</th>
                </tr>
              </thead>
              <tbody>
                ${entries.map(e => `
                  <tr>
                    <td class="font-mono" style="color: var(--text-secondary); white-space: nowrap;">
                      ${new Date(e.timestamp).toLocaleString()}
                    </td>
                    <td class="font-mono"><strong>${e.reference_id}</strong></td>
                    <td>${e.description}</td>
                    <td>
                      <div style="display: flex; flex-direction: column; gap: 4px;">
                        ${e.lines.map(l => `
                          <div style="display: flex; justify-content: space-between; font-size: 12px; background: rgba(0,0,0,0.15); padding: 4px 8px; border-radius: 4px;">
                            <span class="font-mono">${l.account_id}</span>
                            <span>
                              <strong style="color: ${l.direction === 'DEBIT' ? 'var(--primary)' : 'var(--success)'};">
                                ${l.direction}
                              </strong>
                              $${l.amount.toLocaleString(undefined, {minimumFractionDigits: 2})} ${l.currency}
                            </span>
                          </div>
                        `).join("")}
                      </div>
                    </td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div class="toast toast-error">Failed to load ledger: ${err.message}</div>`;
    }
  }
};
