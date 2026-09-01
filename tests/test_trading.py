"""
Unit Tests for Trading & Order Matching Engine
Validates Limit Order Book matching, price-time priority, and trade execution.
"""

import unittest
from backend.core.database import DatabaseManager
from backend.core.models import (
    AccountType, AccountSubtype, Currency,
    OrderSide, OrderType, OrderStatus
)
from backend.services.ledger_service import LedgerService
from backend.services.trading_service import TradingService


class TestTradingService(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager(":memory:")
        self.ledger = LedgerService(self.db)
        self.trading = TradingService(self.db, self.ledger)

        self.trader1 = self.ledger.create_account("Trader 1", AccountType.LIABILITY, AccountSubtype.INVESTMENT, Currency.USD)
        self.trader2 = self.ledger.create_account("Trader 2", AccountType.LIABILITY, AccountSubtype.INVESTMENT, Currency.USD)

    def test_limit_order_resting_and_matching(self):
        # Trader 1 places a SELL Limit order for 1.0 BTC @ $65,000
        sell_order, fills1 = self.trading.submit_order(
            account_id=self.trader1.id,
            symbol="BTC/USD",
            side=OrderSide.SELL,
            order_type=OrderType.LIMIT,
            quantity=1.0,
            price=65000.0
        )
        self.assertEqual(sell_order.status, OrderStatus.OPEN)
        self.assertEqual(len(fills1), 0)

        # Inspect order book depth
        book = self.trading.get_order_book("BTC/USD")
        self.assertEqual(len(book["asks"]), 1)
        self.assertEqual(book["asks"][0]["price"], 65000.0)

        # Trader 2 places a BUY Limit order matching the price for 0.5 BTC @ $65,000
        buy_order, fills2 = self.trading.submit_order(
            account_id=self.trader2.id,
            symbol="BTC/USD",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=0.5,
            price=65000.0
        )

        self.assertEqual(buy_order.status, OrderStatus.FILLED)
        self.assertEqual(len(fills2), 1)
        self.assertEqual(fills2[0]["quantity"], 0.5)
        self.assertEqual(fills2[0]["price"], 65000.0)

        # Verify trades log
        trades = self.trading.list_trades("BTC/USD")
        self.assertEqual(len(trades), 1)
        self.assertEqual(trades[0]["quantity"], 0.5)


if __name__ == "__main__":
    unittest.main()
