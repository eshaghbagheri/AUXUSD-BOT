# loop/event_loop.py

class EventLoop:
    def __init__(self, event_bus, signal_scorer, burst_executor, state_manager):
        self.bus = event_bus
        self.scorer = signal_scorer
        self.executor = burst_executor
        self.state = state_manager

        self.running = False

        self.bus.subscribe("on_tick", self.on_tick)

    # -------------------------
    # Start / Stop
    # -------------------------

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    # -------------------------
    # Tick handler
    # -------------------------

    def on_tick(self, tick):
        if not self.running:
            return

        if self.state.is_in_burst():
            return

        signal = self.scorer.get_signal()

        if signal["direction"] != "NONE":
            self.executor.execute(signal)