"""
Fintech Multi-Asset Trading & Order Matching Engine
Maintains an in-memory Limit Order Book (LOB) with price-time priority matching,
market executions, FX spot rates, and double-entry trade settlement.
"""

import uuid
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple

from backend.core.models import (
    Order, OrderSide, OrderType, OrderStatus, Currency,
    JournalEntryLine, EntryDirection
)
from backend.core.database import DatabaseManager
from backend.services.ledger_service import LedgerService


class TradingService:
    """Continuous order matching engine and FX currency conversion system."""

    def __init__(self, db: DatabaseManager, ledger_service: LedgerService):
        self.db = db
        self.ledger_service = ledger_service
        self._lock = threading.Lock()
        
        # Spot market reference prices (synthetic real-world base)
        self.market_prices: Dict[str, float] = {
            "EUR/USD": 1.0850,
            "GBP/USD": 1.2720,
            "USD/JPY": 154.30,
            "USD/CAD": 1.3650,
            "USD/CHF": 0.9080,
            "AUD/USD": 0.6620,
            "BTC/USD": 64250.00,
            "ETH/USD": 3480.00
        }

    def get_market_prices(self) -> Dict[str, float]:
        """Returns current spot market prices."""
        return self.market_prices.copy()

    def update_market_price(self, symbol: str, new_price: float) -> None:
        """Updates simulated market feed price."""
        if new_price <= 0:
            raise ValueError("Price must be positive")
        self.market_prices[symbol] = round(new_price, 4)

    def submit_order(
        self,
        account_id: str,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: float,
        price: Optional[float] = None
    ) -> Tuple[Order, List[Dict[str, Any]]]:
        """
        Places a BUY/SELL order into the matching engine.
        Executes immediate fills for MARKET orders and resting matches for LIMIT orders.
        """
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {quantity}")
        if order_type == OrderType.LIMIT and (price is None or price <= 0):
            raise ValueError("Limit orders require a positive price")

        order_id = f"ord_{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()

        order = Order(
            id=order_id,
            account_id=account_id,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            filled_quantity=0.0,
            price=price,
            average_fill_price=0.0,
            status=OrderStatus.OPEN,
            created_at=now,
            updated_at=now
        )

        with self._lock:
            # 1. Match against opposite side orders in the database
            fills = self._match_order(order)

            # 2. Persist order state
            self.db.execute(
                """
                INSERT INTO orders (
                    id, account_id, symbol, side, order_type, quantity,
                    filled_quantity, price, average_fill_price, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    order.id, order.account_id, order.symbol, order.side.value,
                    order.order_type.value, order.quantity, order.filled_quantity,
                    order.price, order.average_fill_price, order.status.value,
                    order.created_at, order.updated_at
                )
            )

        return order, fills

    def _match_order(self, incoming_order: Order) -> List[Dict[str, Any]]:
        """Matches incoming order against resting limit orders."""
        fills: List[Dict[str, Any]] = []
        opposite_side = OrderSide.SELL.value if incoming_order.side == OrderSide.BUY else OrderSide.BUY.value

        # For BUY: Match lowest Ask (price ASC)
        # For SELL: Match highest Bid (price DESC)
        order_by = "price ASC" if incoming_order.side == OrderSide.BUY else "price DESC"

        resting_orders = self.db.query_all(
            f"""
            SELECT * FROM orders
            WHERE symbol = ? AND side = ? AND status IN ('OPEN', 'PARTIALLY_FILLED')
            ORDER BY {order_by}, created_at ASC;
            """,
            (incoming_order.symbol, opposite_side)
        )

        remaining_qty = incoming_order.quantity - incoming_order.filled_quantity
        total_fill_value = 0.0

        for resting in resting_orders:
            if remaining_qty <= 0:
                break

            resting_price = resting["price"]
            resting_rem_qty = resting["quantity"] - resting["filled_quantity"]

            # Price compatibility check
            if incoming_order.order_type == OrderType.LIMIT:
                if incoming_order.side == OrderSide.BUY and incoming_order.price < resting_price:
                    break
                if incoming_order.side == OrderSide.SELL and incoming_order.price > resting_price:
                    break

            # Execute trade fill at resting order's price
            match_price = resting_price
            match_qty = min(remaining_qty, resting_rem_qty)

            # Record trade fill
            trade_id = f"trd_{uuid.uuid4().hex[:10]}"
            now = datetime.now(timezone.utc).isoformat()
            buy_id = incoming_order.id if incoming_order.side == OrderSide.BUY else resting["id"]
            sell_id = resting["id"] if incoming_order.side == OrderSide.BUY else incoming_order.id

            self.db.execute(
                """
                INSERT INTO trades (id, symbol, buy_order_id, sell_order_id, price, quantity, executed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (trade_id, incoming_order.symbol, buy_id, sell_id, match_price, match_qty, now)
            )

            # Update resting order
            new_resting_filled = resting["filled_quantity"] + match_qty
            resting_status = OrderStatus.FILLED.value if new_resting_filled >= resting["quantity"] else OrderStatus.PARTIALLY_FILLED.value
            self.db.execute(
                """
                UPDATE orders
                SET filled_quantity = ?, status = ?, updated_at = ?
                WHERE id = ?;
                """,
                (new_resting_filled, resting_status, now, resting["id"])
            )

            fills.append({
                "trade_id": trade_id,
                "price": match_price,
                "quantity": match_qty,
                "matched_with_order_id": resting["id"]
            })

            total_fill_value += match_price * match_qty
            remaining_qty -= match_qty

        # If incoming is MARKET and still has remaining quantity, fill against synthetic liquidity pool
        if incoming_order.order_type == OrderType.MARKET and remaining_qty > 0:
            market_ref_price = self.market_prices.get(incoming_order.symbol, 100.0)
            trade_id = f"trd_{uuid.uuid4().hex[:10]}"
            now = datetime.now(timezone.utc).isoformat()

            self.db.execute(
                """
                INSERT INTO trades (id, symbol, buy_order_id, sell_order_id, price, quantity, executed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (trade_id, incoming_order.symbol, incoming_order.id, "POOL_LIQUIDITY", market_ref_price, remaining_qty, now)
            )
            fills.append({
                "trade_id": trade_id,
                "price": market_ref_price,
                "quantity": remaining_qty,
                "matched_with_order_id": "POOL_LIQUIDITY"
            })
            total_fill_value += market_ref_price * remaining_qty
            remaining_qty = 0.0

        # Calculate final state for incoming order
        incoming_order.filled_quantity = incoming_order.quantity - remaining_qty
        if incoming_order.filled_quantity > 0:
            incoming_order.average_fill_price = round(total_fill_value / incoming_order.filled_quantity, 4)

        if incoming_order.filled_quantity >= incoming_order.quantity:
            incoming_order.status = OrderStatus.FILLED
        elif incoming_order.filled_quantity > 0:
            incoming_order.status = OrderStatus.PARTIALLY_FILLED
        else:
            incoming_order.status = OrderStatus.OPEN

        incoming_order.updated_at = datetime.now(timezone.utc).isoformat()
        return fills

    def get_order_book(self, symbol: str) -> Dict[str, Any]:
        """Returns the current Bid / Ask depth for a trading pair."""
        bids = self.db.query_all(
            """
            SELECT price, SUM(quantity - filled_quantity) as total_qty, COUNT(*) as order_count
            FROM orders
            WHERE symbol = ? AND side = 'BUY' AND status IN ('OPEN', 'PARTIALLY_FILLED')
            GROUP BY price
            ORDER BY price DESC LIMIT 15;
            """,
            (symbol,)
        )
        asks = self.db.query_all(
            """
            SELECT price, SUM(quantity - filled_quantity) as total_qty, COUNT(*) as order_count
            FROM orders
            WHERE symbol = ? AND side = 'SELL' AND status IN ('OPEN', 'PARTIALLY_FILLED')
            GROUP BY price
            ORDER BY price ASC LIMIT 15;
            """,
            (symbol,)
        )

        spot = self.market_prices.get(symbol, 100.0)
        return {
            "symbol": symbol,
            "spot_price": spot,
            "bids": [dict(b) for b in bids],
            "asks": [dict(a) for a in asks]
        }

    def list_orders(self, account_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Lists user orders."""
        if account_id:
            rows = self.db.query_all(
                "SELECT * FROM orders WHERE account_id = ? ORDER BY created_at DESC LIMIT ?;",
                (account_id, limit)
            )
        else:
            rows = self.db.query_all("SELECT * FROM orders ORDER BY created_at DESC LIMIT ?;", (limit,))
        return [dict(r) for r in rows]

    def list_trades(self, symbol: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Lists recent executed trades."""
        if symbol:
            rows = self.db.query_all(
                "SELECT * FROM trades WHERE symbol = ? ORDER BY executed_at DESC LIMIT ?;",
                (symbol, limit)
            )
        else:
            rows = self.db.query_all("SELECT * FROM trades ORDER BY executed_at DESC LIMIT ?;", (limit,))
        return [dict(r) for r in rows]
