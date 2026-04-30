# risk/loss_manager.py

import threading


class LossManager:
    def __init__(self, position_tracker, config_manager):
        self.positions = position_tracker
        self.config = config_manager
        self._lock = threading.RLock()

        self.max_loss = self.config.get_float("loss_limit", -1.0)
        self.enabled = True

    # -------------------------
    # Check Loss
    # -------------------------

    def should_close(self):
        if not self.enabled:
            return False

        total_profit = self.positions.get_profit()

        return total_profit <= self.max_loss

    def get_loss(self):
        return self.positions.get_profit()