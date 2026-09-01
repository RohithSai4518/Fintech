/**
 * Trading & FX Order Execution Component
 * Real-time Order Book Depth, Market/Limit Execution, and FX Spot Rates.
 */

const TradingComponent = {
  currentSymbol: "BTC/USD",

  async render() {
    const container = document.getElementById("tab-trading");
    if (!container) return;

    try {
      const [pricesData, orderBookData, tradesData, accountsData] = await Promise.all([
        Api.getMarketPrices(),
        Api.getOrderBook(this.currentSymbol),
        Api.getTrades(),
        Api.getAccounts()
      ]);

      const prices = pricesData.prices || {};
      const orderBook = orderBookData || { bids: [], asks: [] };
      const trades = tradesData.trades || [];
      const accounts = accountsData.accounts || [];

      // Filter trades for active symbol
      const filteredTrades = trades.filter(t => t.symbol === this.currentSymbol);

      container.innerHTML = `
        <!-- Market Ticker Strip -->
        <div style="display: flex; gap: 12px; overflow-x: auto; margin-bottom: 24px; padding-bottom: 4px;">
          ${Object.entries(prices).map(([sym, price]) => `
            <div 
              onclick="TradingComponent.setSymbol('${sym}')"
              style="cursor: pointer; background: ${sym === this.currentSymbol ? 'var(--primary)' : 'var(--bg-card)'}; border: 1px solid var(--border-color); border-radius: 8px; padding: 12px 16px; min-width: 140px;"
            >
              <div style="font-size: 12px; color: ${sym === this.currentSymbol ? '#fff' : 'var(--text-secondary)'};">${sym}</div>
              <div style="font-size: 16px; font-weight: 700; font-family: var(--font-mono); margin-top: 4px;">
                $${price.toLocaleString(undefined, {minimumFractionDigits: 2})}
              </div>
            </div>
          `).join("")}
        </div>

        <div class="trading-layout">
          <!-- Left Column: Order Book & Trades -->
          <div>
            <div class="card-panel">
              <div class="panel-header">
                <div>
                  <h2 class="panel-title">Order Book Depth: ${this.currentSymbol}</h2>
                  <span style="font-size: 12px; color: var(--text-secondary);">
                    Spot Reference: $${(prices[this.currentSymbol] || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}
                  </span>
                </div>
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <!-- Bids Table -->
                <div>
                  <h4 style="font-size: 13px; color: var(--success); margin-bottom: 8px;">Bids (Buy Orders)</h4>
                  <table class="order-book-table">
                    <thead>
                      <tr>
                        <th>Price ($)</th>
                        <th>Qty</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${(orderBook.bids || []).length === 0 ? '<tr><td colspan="2" style="text-align: center; color: var(--text-muted);">No open bids</td></tr>' : ''}
                      ${(orderBook.bids || []).map(b => `
                        <tr class="bid-row">
                          <td>$${b.price.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                          <td>${b.total_qty.toFixed(4)}</td>
                        </tr>
                      `).join("")}
                    </tbody>
                  </table>
                </div>

                <!-- Asks Table -->
                <div>
                  <h4 style="font-size: 13px; color: var(--danger); margin-bottom: 8px;">Asks (Sell Orders)</h4>
                  <table class="order-book-table">
                    <thead>
                      <tr>
                        <th>Price ($)</th>
                        <th>Qty</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${(orderBook.asks || []).length === 0 ? '<tr><td colspan="2" style="text-align: center; color: var(--text-muted);">No open asks</td></tr>' : ''}
                      ${(orderBook.asks || []).map(a => `
                        <tr class="ask-row">
                          <td>$${a.price.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                          <td>${a.total_qty.toFixed(4)}</td>
                        </tr>
                      `).join("")}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Recent Executed Trades -->
            <div class="card-panel">
              <div class="panel-header">
                <h2 class="panel-title">Executed Market Trades</h2>
              </div>
              <div class="table-responsive">
                <table class="fin-table">
                  <thead>
                    <tr>
                      <th>Time</th>
                      <th>Trade ID</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th>Total Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${filteredTrades.slice(0, 10).map(t => `
                      <tr>
                        <td class="font-mono" style="color: var(--text-secondary);">${new Date(t.executed_at).toLocaleTimeString()}</td>
                        <td class="font-mono">${t.id}</td>
                        <td class="font-mono" style="font-weight: 600;">$${t.price.toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                        <td class="font-mono">${t.quantity.toFixed(4)}</td>
                        <td class="font-mono">$${(t.price * t.quantity).toLocaleString(undefined, {minimumFractionDigits: 2})}</td>
                      </tr>
                    `).join("")}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Right Column: Order Placement Ticket -->
          <div>
            <div class="card-panel">
              <div class="panel-header">
                <h2 class="panel-title">Order Ticket</h2>
              </div>
              <form id="order-form" onsubmit="TradingComponent.handleOrderSubmit(event)">
                <div class="form-group" style="margin-bottom: 16px;">
                  <label>Trading Account</label>
                  <select id="trade-acc" class="form-control">
                    ${accounts.map(a => `
                      <option value="${a.id}">
                        ${a.name} ($${a.available_balance.toLocaleString()})
                      </option>
                    `).join("")}
                  </select>
                </div>

                <div class="form-group" style="margin-bottom: 16px;">
                  <label>Order Side</label>
                  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <button type="button" id="side-buy-btn" class="btn btn-success" onclick="TradingComponent.setSide('BUY')">BUY</button>
                    <button type="button" id="side-sell-btn" class="btn btn-secondary" onclick="TradingComponent.setSide('SELL')">SELL</button>
                  </div>
                  <input type="hidden" id="order-side" value="BUY" />
                </div>

                <div class="form-group" style="margin-bottom: 16px;">
                  <label>Order Type</label>
                  <select id="order-type" class="form-control" onchange="TradingComponent.onOrderTypeChange()">
                    <option value="LIMIT">Limit Order (Rest on Book)</option>
                    <option value="MARKET">Market Order (Immediate Execution)</option>
                  </select>
                </div>

                <div class="form-group" style="margin-bottom: 16px;">
                  <label>Quantity</label>
                  <input type="number" step="0.0001" min="0.0001" id="order-qty" class="form-control" placeholder="1.0" required />
                </div>

                <div class="form-group" id="group-price" style="margin-bottom: 20px;">
                  <label>Limit Price ($)</label>
                  <input type="number" step="0.01" min="0.01" id="order-price" class="form-control" value="${prices[this.currentSymbol] || 100.0}" required />
                </div>

                <button type="submit" class="btn btn-primary" style="width: 100%; justify-content: center;">
                  Submit Order
                </button>
              </form>
            </div>
          </div>
        </div>
      `;
    } catch (err) {
      container.innerHTML = `<div class="toast toast-error">Failed to load trading: ${err.message}</div>`;
    }
  },

  setSymbol(sym) {
    this.currentSymbol = sym;
    this.render();
  },

  setSide(side) {
    document.getElementById("order-side").value = side;
    const buyBtn = document.getElementById("side-buy-btn");
    const sellBtn = document.getElementById("side-sell-btn");

    if (side === "BUY") {
      buyBtn.className = "btn btn-success";
      sellBtn.className = "btn btn-secondary";
    } else {
      buyBtn.className = "btn btn-secondary";
      sellBtn.className = "btn btn-primary";
      sellBtn.style.backgroundColor = "var(--danger)";
    }
  },

  onOrderTypeChange() {
    const type = document.getElementById("order-type").value;
    const priceGroup = document.getElementById("group-price");
    if (type === "MARKET") {
      priceGroup.style.display = "none";
      document.getElementById("order-price").removeAttribute("required");
    } else {
      priceGroup.style.display = "flex";
      document.getElementById("order-price").setAttribute("required", "true");
    }
  },

  async handleOrderSubmit(event) {
    event.preventDefault();
    const accountId = document.getElementById("trade-acc").value;
    const side = document.getElementById("order-side").value;
    const orderType = document.getElementById("order-type").value;
    const qty = parseFloat(document.getElementById("order-qty").value);
    const price = orderType === "LIMIT" ? parseFloat(document.getElementById("order-price").value) : null;

    try {
      const res = await Api.submitOrder({
        account_id: accountId,
        symbol: this.currentSymbol,
        side,
        order_type: orderType,
        quantity: qty,
        price
      });

      const fillCount = (res.fills || []).length;
      App.showToast(`Order ${res.order.id} placed (${res.order.status}) - ${fillCount} fill(s) executed`, "success");
      this.render();
      App.refreshKPIs();
    } catch (err) {
      App.showToast(err.message, "error");
    }
  }
};
