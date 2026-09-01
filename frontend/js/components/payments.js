/**
 * Payments & Money Movement Component
 * Handles wire transfers, internal accounts settlement, and card charges.
 */

const PaymentsComponent = {
  async render() {
    const container = document.getElementById("tab-payments");
    if (!container) return;

    try {
      const [accountsData, txData] = await Promise.all([
        Api.getAccounts(),
        Api.getTransactions(25)
      ]);

      const accounts = accountsData.accounts || [];
      const txs = txData.transactions || [];

      container.innerHTML = `
        <div class="card-panel">
          <div class="panel-header">
            <h2 class="panel-title">Execute Money Movement & Settlement</h2>
          </div>
          
          <form id="payment-form" onsubmit="PaymentsComponent.handleSubmit(event)">
            <div class="form-grid">
              <div class="form-group">
                <label>Payment Rail / Method</label>
                <select id="pay-method" class="form-control" onchange="PaymentsComponent.onMethodChange()">
                  <option value="INTERNAL">Internal Ledger Transfer (Zero Settlement Lag)</option>
                  <option value="CARD">Credit / Debit Card Authorization (PCI-DSS Luhn Checked)</option>
                  <option value="ACH">ACH Direct Deposit / Debit</option>
                  <option value="WIRE">Fedwire / SWIFT High Value Wire</option>
                </select>
              </div>

              <div class="form-group" id="group-src-account">
                <label>Source Account</label>
                <select id="pay-source" class="form-control">
                  ${accounts.map(a => `
                    <option value="${a.id}">
                      ${a.name} (${a.account_number}) - Avail: $${a.available_balance.toLocaleString()} ${a.currency}
                    </option>
                  `).join("")}
                </select>
              </div>

              <div class="form-group">
                <label>Destination Account</label>
                <select id="pay-dest" class="form-control">
                  ${accounts.map(a => `
                    <option value="${a.id}">
                      ${a.name} (${a.account_number})
                    </option>
                  `).join("")}
                </select>
              </div>

              <div class="form-group">
                <label>Amount (USD)</label>
                <input type="number" step="0.01" min="1" id="pay-amount" class="form-control" placeholder="100.00" required />
              </div>

              <div class="form-group">
                <label>Description / Remittance Memo</label>
                <input type="text" id="pay-desc" class="form-control" placeholder="Invoice #1092 Settlement" required />
              </div>
            </div>

            <!-- Card simulation fields -->
            <div id="card-fields" style="display: none; margin-top: 20px; padding: 16px; background: var(--bg-secondary); border-radius: 8px; border: 1px solid var(--border-color);">
              <h3 style="font-size: 14px; margin-bottom: 12px; color: var(--accent);">Simulated Card Details (PCI-DSS Sanitized)</h3>
              <div class="form-grid">
                <div class="form-group">
                  <label>Card Number (Luhn-Valid Test PAN)</label>
                  <input type="text" id="card-pan" class="form-control font-mono" placeholder="4111111111111111" value="4111111111111111" />
                </div>
                <div class="form-group">
                  <label>Cardholder Name</label>
                  <input type="text" id="card-holder" class="form-control" value="Alice Smith" />
                </div>
              </div>
            </div>

            <div style="margin-top: 20px; display: flex; justify-content: flex-end; gap: 12px;">
              <button type="submit" class="btn btn-primary">
                Confirm & Dispatch Payment
              </button>
            </div>
          </form>
        </div>

        <div class="card-panel">
          <div class="panel-header">
            <h2 class="panel-title">Transaction History & Settlement Log</h2>
          </div>
          <div class="table-responsive">
            <table class="fin-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>TX ID</th>
                  <th>Method</th>
                  <th>Amount</th>
                  <th>Fee</th>
                  <th>Status</th>
                  <th>Risk Score</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                ${txs.map(t => `
                  <tr>
                    <td class="font-mono" style="color: var(--text-secondary); white-space: nowrap;">
                      ${new Date(t.created_at).toLocaleString()}
                    </td>
                    <td class="font-mono"><strong>${t.id}</strong></td>
                    <td><span class="badge badge-info">${t.payment_method}</span></td>
                    <td class="font-mono" style="font-weight: 600;">
                      $${t.amount.toLocaleString(undefined, {minimumFractionDigits: 2})}
                    </td>
                    <td class="font-mono" style="color: var(--text-muted); font-size: 12px;">
                      $${t.fee.toLocaleString(undefined, {minimumFractionDigits: 2})}
                    </td>
                    <td>
                      <span class="badge ${
                        t.status === 'SETTLED' ? 'badge-success' :
                        t.status === 'FLAGGED' ? 'badge-warning' : 'badge-danger'
                      }">
                        ${t.status}
                      </span>
                    </td>
                    <td>
                      <span style="font-weight: 700; color: ${
                        t.risk_score >= 50 ? 'var(--danger)' :
                        t.risk_score >= 25 ? 'var(--warning)' : 'var(--success)'
                      };">
                        ${t.risk_score} / 100
                      </span>
                    </td>
                    <td>${t.description}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div class="toast toast-error">Failed to load payments: ${err.message}</div>`;
    }
  },

  onMethodChange() {
    const method = document.getElementById("pay-method").value;
    const cardFields = document.getElementById("card-fields");
    const srcGroup = document.getElementById("group-src-account");

    if (method === "CARD") {
      cardFields.style.display = "block";
      srcGroup.style.display = "none";
    } else {
      cardFields.style.display = "none";
      srcGroup.style.display = "flex";
    }
  },

  async handleSubmit(event) {
    event.preventDefault();
    const method = document.getElementById("pay-method").value;
    const amount = parseFloat(document.getElementById("pay-amount").value);
    const desc = document.getElementById("pay-desc").value;
    const dest = document.getElementById("pay-dest").value;
    const src = method === "CARD" ? null : document.getElementById("pay-source").value;

    let cardData = null;
    if (method === "CARD") {
      cardData = {
        card_number: document.getElementById("card-pan").value,
        holder: document.getElementById("card-holder").value
      };
    }

    try {
      const res = await Api.processPayment({
        source_account_id: src,
        destination_account_id: dest,
        amount,
        currency: "USD",
        payment_method: method,
        description: desc,
        card_data: cardData
      });

      if (res.status === "FAILED") {
        App.showToast(`Transaction Blocked by Risk Policy: ${res.failure_reason}`, "error");
      } else {
        App.showToast(`Payment successfully settled (${res.id})`, "success");
      }
      this.render();
      App.refreshKPIs();
    } catch (err) {
      App.showToast(err.message, "error");
    }
  }
};
