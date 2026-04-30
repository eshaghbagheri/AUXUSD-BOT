# core/main.py

import threading
import time
import signal
import sys

from core.config_manager import ConfigManager
from core.state_manager import StateManager
from events.event_bus import EventBus

from mt5.connector import MT5Connector

from tick.tick_listener import TickListener
from tick.tick_buffer import TickBuffer

from signals.scorer import SignalScorer

from execution.order_manager import OrderManager
from execution.burst_executor import BurstExecutor
from execution.position_tracker import PositionTracker

from risk.profit_manager import ProfitManager
from risk.loss_manager import LossManager
from risk.momentum_exit import MomentumExit

from loop.fast_loop import FastLoop
from loop.event_loop import EventLoop


class TradingBot:
    def __init__(self):
        # Core systems
        self.config = ConfigManager()
        self.state = StateManager()
        self.event_bus = EventBus()

        # MT5 اتصال
        self.mt5 = MT5Connector(self.config)

        # Tick system
        self.tick_buffer = TickBuffer(self.config)
        self.tick_listener = TickListener(self.mt5, self.tick_buffer, self.event_bus)

        # Signal system
        self.signal_scorer = SignalScorer(self.config, self.tick_buffer)

        # Execution system
        self.position_tracker = PositionTracker(self.mt5)
        self.order_manager = OrderManager(self.mt5, self.position_tracker, self.config)
        self.burst_executor = BurstExecutor(
            self.order_manager,
            self.position_tracker,
            self.signal_scorer,
            self.config,
            self.state
        )

        # Risk system
        self.profit_manager = ProfitManager(self.position_tracker, self.config)
        self.loss_manager = LossManager(self.position_tracker, self.config)
        self.momentum_exit = MomentumExit(self.signal_scorer, self.position_tracker)

        # Loops
        self.fast_loop = FastLoop(
            self.state,
            self.profit_manager,
            self.loss_manager,
            self.momentum_exit,
            self.order_manager,
            self.config
        )

        self.event_loop = EventLoop(
            self.event_bus,
            self.signal_scorer,
            self.burst_executor,
            self.state
        )

        # Threads
        self.threads = []
        self.running = False

    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self):
        print("[BOT] Starting...")

        if not self.mt5.connect():
            print("[ERROR] MT5 connection failed")
            return

        self.running = True
        self.state.set_state("IDLE")

        # Threads
        self.threads = [
            threading.Thread(target=self.tick_listener.start, daemon=True),
            threading.Thread(target=self.fast_loop.start, daemon=True),
            threading.Thread(target=self.event_loop.start, daemon=True),
        ]

        for t in self.threads:
            t.start()

        print("[BOT] Running")

        self._wait()

    def stop(self):
        print("[BOT] Stopping...")

        self.running = False

        self.tick_listener.stop()
        self.fast_loop.stop()
        self.event_loop.stop()

        self.mt5.shutdown()

        print("[BOT] Stopped")

    # -------------------------
    # Internal
    # -------------------------

    def _wait(self):
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()


# -------------------------
# Entry Point
# -------------------------

def main():
    bot = TradingBot()

    def handle_signal(sig, frame):
        bot.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    bot.start()


if __name__ == "__main__":
    main()