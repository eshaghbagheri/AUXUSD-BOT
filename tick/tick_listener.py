# tick/tick_listener.py

import threading
import time


class TickListener:
    def __init__(self, mt5_connector, tick_buffer, event_bus):
        self.mt5 = mt5_connector
        self.tick_buffer = tick_buffer
        self.event_bus = event_bus

        self._running = False
        self._thread = None

        # Symbol از config داخل connector گرفته می‌شود
        self.symbol = self.mt5.get_symbol()

    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    # -------------------------
    # Core Loop
    # -------------------------

    def _run(self):
        last_tick_time = 0

        while self._running:
            tick = self.mt5.get_tick(self.symbol)

            if tick is None:
                time.sleep(0.01)
                continue

            # جلوگیری از تکرار تیک
            tick_time = tick.get("time_msc", 0)
            if tick_time == last_tick_time:
                continue

            last_tick_time = tick_time

            # ساختار استاندارد تیک
            processed_tick = {
                "bid": tick.get("bid"),
                "ask": tick.get("ask"),
                "last": tick.get("last"),
                "time": tick.get("time_msc"),
                "volume": tick.get("volume", 0)
            }

            # ذخیره در buffer
            self.tick_buffer.add_tick(processed_tick)

            # انتشار event
            self.event_bus.publish("on_tick", processed_tick)