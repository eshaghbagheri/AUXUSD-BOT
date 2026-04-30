# execution/order_manager.py

import threading
import time


class OrderManager:
    def __init__(self, mt5_connector, position_tracker, config_manager):
        self.mt5 = mt5_connector
        self.positions = position_tracker
        self.config = config_manager

        self._lock = threading.RLock()

        self.symbol = self.mt5.get_symbol()
        self.max_retries = self.config.get_int("order_max_retries", 3)
        self.slippage = self.config.get_int("slippage", 10)

    # -------------------------
    # Send Order
    # -------------------------

    def send_order(self, direction: str, volume: float, comment="BOT"):
        price = self._get_price(direction)

        order_type = "BUY" if direction == "BUY" else "SELL"

        request = {
            "symbol": self.symbol,
            "type": order_type,
            "volume": volume,
            "price": price,
            "sl": 0,
            "tp": 0,
            "deviation": self.slippage,
            "comment": comment
        }

        return self._execute_with_retry(request)

    # -------------------------
    # Execution
    # -------------------------

    def _execute_with_retry(self, request):
        for attempt in range(self.max_retries):
            result = self.mt5.send_order(request)

            if result and result.get("retcode") == 0:
                return result

            time.sleep(0.05)

        return None

    # -------------------------
    # Close Orders
    # -------------------------

    def close_position(self, ticket):
        return self.mt5.close_position(ticket)

    def close_all(self):
        positions = self.positions.get_all()

        for p in positions:
            self.close_position(p["ticket"])

    def close_profitable(self):
        for p in self.positions.get_profitable():
            self.close_position(p["ticket"])

    def close_losing(self):
        for p in self.positions.get_losing():
            self.close_position(p["ticket"])

    # -------------------------
    # Helpers
    # -------------------------

    def _get_price(self, direction):
        tick = self.mt5.get_tick(self.symbol)

        if direction == "BUY":
            return tick["ask"]
        else:
            return tick["bid"]