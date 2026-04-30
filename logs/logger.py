# logs/logger.py

import logging
import os


class Logger:
    def __init__(self, name="BOT"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            os.makedirs("logs", exist_ok=True)

            formatter = logging.Formatter(
                "[%(asctime)s] %(levelname)s - %(message)s"
            )

            # Trades log
            trade_handler = logging.FileHandler("logs/trades.log")
            trade_handler.setFormatter(formatter)
            trade_handler.setLevel(logging.INFO)

            # Error log
            error_handler = logging.FileHandler("logs/errors.log")
            error_handler.setFormatter(formatter)
            error_handler.setLevel(logging.ERROR)

            # Signals log
            signal_handler = logging.FileHandler("logs/signals.log")
            signal_handler.setFormatter(formatter)
            signal_handler.setLevel(logging.INFO)

            self.logger.addHandler(trade_handler)
            self.logger.addHandler(error_handler)
            self.logger.addHandler(signal_handler)

    # -------------------------
    # API
    # -------------------------

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)