# signal/scorer.py

from signals.velocity import VelocityCalculator
from signals.tick_imbalance import TickImbalanceCalculator
from signals.acceleration import AccelerationCalculator


class SignalScorer:
    def __init__(self, config_manager, tick_buffer):
        self.config = config_manager
        self.tick_buffer = tick_buffer

        self.velocity = VelocityCalculator(tick_buffer, config_manager)
        self.imbalance = TickImbalanceCalculator(tick_buffer, config_manager)
        self.acceleration = AccelerationCalculator(tick_buffer, config_manager)

        # weights
        self.w_velocity = self.config.get_float("weight_velocity", 1.0)
        self.w_imbalance = self.config.get_float("weight_imbalance", 1.0)
        self.w_acceleration = self.config.get_float("weight_acceleration", 1.0)

        self.strong_threshold = self.config.get_float("strong_threshold", 0.7)
        self.weak_threshold = self.config.get_float("weak_threshold", 0.3)

    # -------------------------
    # Score
    # -------------------------

    def get_score(self):
        v = self.velocity.get_normalized_velocity()
        i = self.imbalance.get_imbalance()
        a = self.acceleration.get_acceleration()

        score = (
            self.w_velocity * v +
            self.w_imbalance * i +
            self.w_acceleration * a
        )

        return score

    # -------------------------
    # Signal
    # -------------------------

    def get_signal(self):
        score = self.get_score()

        if score >= self.strong_threshold:
            return {
                "direction": "BUY",
                "strength": "STRONG",
                "score": score
            }

        elif score >= self.weak_threshold:
            return {
                "direction": "BUY",
                "strength": "WEAK",
                "score": score
            }

        elif score <= -self.strong_threshold:
            return {
                "direction": "SELL",
                "strength": "STRONG",
                "score": score
            }

        elif score <= -self.weak_threshold:
            return {
                "direction": "SELL",
                "strength": "WEAK",
                "score": score
            }

        else:
            return {
                "direction": "NONE",
                "strength": "NONE",
                "score": score
            }