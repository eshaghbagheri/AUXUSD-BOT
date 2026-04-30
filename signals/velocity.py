# signal/velocity.py

import time


class VelocityCalculator:
    def __init__(self, tick_buffer, config_manager):
        self.tick_buffer = tick_buffer
        self.config = config_manager

        self.window_ms = self.config.get_int("velocity_window_ms", 300)
        self.norm_window_ms = self.config.get_int("velocity_norm_window_ms", 3000)

    # -------------------------
    # Raw Velocity
    # -------------------------

    def get_velocity(self):
        ticks = self.tick_buffer.get_ticks_in_range(self.window_ms)

        if len(ticks) < 2:
            return 0.0

        dt = (ticks[-1]["time"] - ticks[0]["time"]) / 1000.0
        if dt <= 0:
            return 0.0

        dp = ticks[-1]["last"] - ticks[0]["last"]

        return dp / dt

    # -------------------------
    # Normalized Velocity
    # -------------------------

    def get_normalized_velocity(self):
        current_velocity = self.get_velocity()

        base_ticks = self.tick_buffer.get_ticks_in_range(self.norm_window_ms)

        if len(base_ticks) < 3:
            return 0.0

        velocities = []

        for i in range(1, len(base_ticks)):
            dt = (base_ticks[i]["time"] - base_ticks[i - 1]["time"]) / 1000.0
            if dt <= 0:
                continue

            dp = base_ticks[i]["last"] - base_ticks[i - 1]["last"]
            velocities.append(abs(dp / dt))

        if not velocities:
            return 0.0

        avg_velocity = sum(velocities) / len(velocities)

        if avg_velocity == 0:
            return 0.0

        return current_velocity / avg_velocity