# loop/fast_loop.py

import time


class FastLoop:
    def __init__(self, state_manager, profit_manager, loss_manager, momentum_exit, order_manager, config):
        self.state = state_manager
        self.profit = profit_manager
        self.loss = loss_manager
        self.momentum = momentum_exit
        self.orders = order_manager
        self.config = config

        self.running = False
        self.interval = 0.2  # 200ms

    # -------------------------
    # Start
    # -------------------------

    def start(self):
        self.running = True

        while self.running:
            self._run()
            time.sleep(self.interval)

    def stop(self):
        self.running = False

    # -------------------------
    # Core logic
    # -------------------------

    def _run(self):
        if self.profit.should_close():
            self.orders.close_all()
            return

        if self.loss.should_close():
            self.orders.close_all()
            return

        if self.momentum.should_exit():
            self.orders.close_all()
            return