/**
 * Fraud & Risk Management Console Component
 * Configures AML rules, velocity limits, and displays anomalous activity alerts.
 */

const RiskComponent = {
  async render() {
    const container = document.getElementById("tab-risk");
    if (!container) return;

    try {
      const [rulesData, txData] = await Promise.all([
        Api.getFraudRules(),
        Api.getTransactions(50)
      ]);

      const rules = rulesData.rules || [];
      const txs = (txData.transactions || []).filter(t => t.risk_score > 0 || t.status === "FLAGGED" || t.status === "FAILED");

      container.innerHTML = `
        <div class="card-panel">
          <div class="panel-header">
            <div>
              <h2 class="panel-title">Active Fraud Detection & AML Rules</h2>
              <p style="font-size: 13px; color: var(--text-secondary); margin-top: 4px;">
                Real-time transaction inspection heuristics and threshold enforcement
              </p>
            </div>
            <button class="btn btn-secondary" onclick="RiskComponent.showAddRuleModal()">
              + Add Custom Rule
            </button>
          </div>

          <div class="table-responsive">
            <table class="fin-table">
              <thead>
                <tr>
                  <th>Rule Name</th>
                  <th>Category</th>
                  <th>Threshold</th>
                  <th>Action</th>
                  <th>Status</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                ${rules.map(r => `
                  <tr>
                    <td><strong>${r.name}</strong></td>
                    <td><span class="badge badge-info">${r.rule_type}</span></td>
                    <td class="font-mono">$${r.threshold.toLocaleString()}</td>
                    <td>
                      <span class="badge ${r.action === 'BLOCK' ? 'badge-danger' : 'badge-warning'}">
                        ${r.action}
                      </span>
                    </td>
                    <td>
                      <span class="badge badge-success">ACTIVE</span>
                    </td>
                    <td style="color: var(--text-secondary); font-size: 12px;">${r.description}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>

        <div class="card-panel">
          <div class="panel-header">
            <h2 class="panel-title">Real-Time Risk Alerts & Flagged Activity Feed</h2>
          </div>

          <div class="table-responsive">
            <table class="fin-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>TX Reference</th>
                  <th>Amount</th>
                  <th>Risk Score</th>
                  <th>Risk Level</th>
                  <th>Status</th>
                  <th>Policy Triggers</th>
                </tr>
              </thead>
              <tbody>
                ${txs.length === 0 ? '<tr><td colspan="7" style="text-align: center; color: var(--text-muted);">No flagged or anomalous transactions recorded.</td></tr>' : ''}
                ${txs.map(t => `
                  <tr>
                    <td class="font-mono" style="color: var(--text-secondary);">${new Date(t.created_at).toLocaleTimeString()}</td>
                    <td class="font-mono"><strong>${t.id}</strong></td>
                    <td class="font-mono">$${t.amount.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                    <td>
                      <span style="font-weight: 700; color: ${
                        t.risk_score >= 50 ? 'var(--danger)' :
                        t.risk_score >= 25 ? 'var(--warning)' : 'var(--success)'
                      };">
                        ${t.risk_score} / 100
                      </span>
                    </td>
                    <td>
                      <span class="badge ${
                        t.risk_level === 'CRITICAL' ? 'badge-danger' :
                        t.risk_level === 'HIGH' ? 'badge-warning' : 'badge-info'
                      }">
                        ${t.risk_level}
                      </span>
                    </td>
                    <td>
                      <span class="badge ${
                        t.status === 'SETTLED' ? 'badge-success' :
                        t.status === 'FLAGGED' ? 'badge-warning' : 'badge-danger'
                      }">
                        ${t.status}
                      </span>
                    </td>
                    <td style="font-size: 12px; color: var(--danger);">
                      ${(t.metadata && t.metadata.risk_triggers ? t.metadata.risk_triggers.join("<br>") : t.failure_reason) || 'Threshold violation'}
                    </td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div class="toast toast-error">Failed to load risk console: ${err.message}</div>`;
    }
  },

  async showAddRuleModal() {
    const name = prompt("Enter Rule Name:");
    if (!name) return;
    const threshold = parseFloat(prompt("Enter Amount Threshold ($):", "5000"));
    if (isNaN(threshold)) return;
    const action = prompt("Action (FLAG / BLOCK / REVIEW):", "FLAG").toUpperCase();

    try {
      await Api.createFraudRule({
        name,
        rule_type: "AMOUNT_THRESHOLD",
        threshold,
        action: action === "BLOCK" ? "BLOCK" : "FLAG",
        description: `Flag or block single operations exceeding $${threshold}`
      });
      App.showToast(`Risk rule '${name}' registered successfully`, "success");
      this.render();
    } catch (err) {
      App.showToast(err.message, "error");
    }
  }
};
