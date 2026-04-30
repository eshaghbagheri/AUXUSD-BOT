# tick/tick_buffer.py

import threading
import time
from collections import deque


class TickBuffer:
    def __init__(self, config_manager):
        self.config = config_manager

        self._lock = threading.RLock()

        # مدت نگهداری (میلی‌ثانیه)
        self.max_age_ms = self.config.get_int("tick_buffer_ms", 3000)

        self._ticks = deque()

    # -------------------------
    # Add Tick
    # -------------------------

    def add_tick(self, tick: dict):
        with self._lock:
            self._ticks.append(tick)
            self._cleanup()

    # -------------------------
    # Cleanup old ticks
    # -------------------------

    def _cleanup(self):
        now = int(time.time() * 1000)

        while self._ticks:
            if now - self._ticks[0]["time"] > self.max_age_ms:
                self._ticks.popleft()
            else:
                break

    # -------------------------
    # Get Data
    # -------------------------

    def get_ticks(self):
        with self._lock:
            return list(self._ticks)

    def get_last_tick(self):
        with self._lock:
            if self._ticks:
                return self._ticks[-1]
            return None

    def get_ticks_in_range(self, ms: int):
        now = int(time.time() * 1000)

        with self._lock:
            return [
                t for t in self._ticks
                if now - t["time"] <= ms
            ]

    # -------------------------
    # Metrics
    # -------------------------

    def get_tick_rate(self, window_ms=1000):
        ticks = self.get_ticks_in_range(window_ms)
        return len(ticks)

    def get_price_change(self, window_ms=500):
        ticks = self.get_ticks_in_range(window_ms)

        if len(ticks) < 2:
            return 0.0

        return ticks[-1]["last"] - ticks[0]["last"]