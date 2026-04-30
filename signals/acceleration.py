# signal/acceleration.py

class AccelerationCalculator:
    def __init__(self, tick_buffer, config_manager):
        self.tick_buffer = tick_buffer
        self.config = config_manager

        self.window_ms = self.config.get_int("acceleration_window_ms", 400)

    # -------------------------
    # Acceleration
    # -------------------------

    def get_acceleration(self):
        ticks = self.tick_buffer.get_ticks_in_range(self.window_ms)

        if len(ticks) < 3:
            return 0.0

        velocities = []

        for i in range(1, len(ticks)):
            dt = (ticks[i]["time"] - ticks[i - 1]["time"]) / 1000.0
            if dt <= 0:
                continue

            dp = ticks[i]["last"] - ticks[i - 1]["last"]
            velocities.append(dp / dt)

        if len(velocities) < 2:
            return 0.0

        return velocities[-1] - velocities[-2]