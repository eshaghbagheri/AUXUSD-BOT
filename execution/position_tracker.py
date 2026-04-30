# execution/position_tracker.py

import threading


class PositionTracker:
    def __init__(self, mt5_connector):
        self.mt5 = mt5_connector
        self._lock = threading.RLock()

        self._positions = []

    # -------------------------
    # Sync with MT5
    # -------------------------

    def refresh(self):
        positions = self.mt5.get_positions()

        with self._lock:
            self._positions = positions if positions else []

    # -------------------------
    # Getters
    # -------------------------

    def get_all(self):
        with self._lock:
            return list(self._positions)

    def get_by_symbol(self, symbol: str):
        with self._lock:
            return [p for p in self._positions if p["symbol"] == symbol]

    def get_profit(self):
        with self._lock:
            return sum(p.get("profit", 0) for p in self._positions)

    def count(self):
        with self._lock:
            return len(self._positions)

    # -------------------------
    # Filters
    # -------------------------

    def get_profitable(self):
        with self._lock:
            return [p for p in self._positions if p.get("profit", 0) > 0]

    def get_losing(self):
        with self._lock:
            return [p for p in self._positions if p.get("profit", 0) < 0]

    # -------------------------
    # Position by ticket
    # -------------------------

    def get_by_ticket(self, ticket):
        with self._lock:
            for p in self._positions:
                if p.get("ticket") == ticket:
                    return p
            return None