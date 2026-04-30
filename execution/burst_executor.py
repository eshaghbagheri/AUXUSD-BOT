# execution/burst_executor.py

import time


class BurstExecutor:
    def __init__(self, order_manager, position_tracker, signal_scorer, config_manager, state_manager):
        self.orders = order_manager
        self.positions = position_tracker
        self.scorer = signal_scorer
        self.config = config_manager
        self.state = state_manager

        self.cooldown = self.config.get_float("burst_cooldown", 2.0)

    # -------------------------
    # Main Entry
    # -------------------------

    def execute(self, signal: dict):
        if signal["direction"] == "NONE":
            return

        self.state.set_burst(True)

        strength = signal["strength"]
        direction = signal["direction"]

        if strength == "STRONG":
            count = self.config.get_int("burst_strong_count", 5)
            step = self.config.get_float("burst_strong_step", 0.5)
        else:
            count = self.config.get_int("burst_weak_count", 2)
            step = self.config.get_float("burst_weak_step", 1.0)

        volume = self.config.get_float("lot_size", 0.01)

        self._burst_trade(direction, volume, count, step)

        self.state.set_burst(False)

        time.sleep(self.cooldown)

    # -------------------------
    # Burst logic
    # -------------------------

    def _burst_trade(self, direction, volume, count, step):
        for i in range(count):
            self.orders.send_order(
                direction=direction,
                volume=volume,
                comment=f"BURST_{i}"
            )

            time.sleep(step)