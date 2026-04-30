# signal/tick_imbalance.py

class TickImbalanceCalculator:
    def __init__(self, tick_buffer, config_manager):
        self.tick_buffer = tick_buffer
        self.config = config_manager

        self.window_ms = self.config.get_int("imbalance_window_ms", 500)

    # -------------------------
    # Imbalance
    # -------------------------

    def get_imbalance(self):
        ticks = self.tick_buffer.get_ticks_in_range(self.window_ms)

        if len(ticks) < 2:
            return 0.0

        up = 0
        down = 0

        for i in range(1, len(ticks)):
            diff = ticks[i]["last"] - ticks[i - 1]["last"]

            if diff > 0:
                up += 1
            elif diff < 0:
                down += 1

        total = up + down

        if total == 0:
            return 0.0

        return (up - down) / total