# risk/momentum_exit.py

class MomentumExit:
    def __init__(self, signal_scorer, position_tracker):
        self.scorer = signal_scorer
        self.positions = position_tracker

        self.last_score = 0.0

        self.decline_threshold = -0.2

    # -------------------------
    # Momentum check
    # -------------------------

    def should_exit(self):
        current_score = self.scorer.get_score()

        delta = current_score - self.last_score
        self.last_score = current_score

        # اگر momentum در حال سقوط باشد
        if delta < self.decline_threshold:
            return True

        return False