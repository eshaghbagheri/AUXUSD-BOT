# risk/profit_manager.py

import threading


class ProfitManager:
    def __init__(self, position_tracker, config_manager):
        self.positions = position_tracker
        self.config = config_manager
        self._lock = threading.RLock()

        self.target_profit = self.config.get_float("profit_target", 1.0)
        self.enabled = True

    # -------------------------
    # Check Profit
    # -------------------------

    def should_close(self):
        if not self.enabled:
            return False

        total_profit = self.positions.get_profit()

        return total_profit >= self.target_profit

    def get_profit(self):
        return self.positions.get_profit()