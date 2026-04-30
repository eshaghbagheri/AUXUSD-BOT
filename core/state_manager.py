# core/state_manager.py

import threading
import time


class StateManager:
    def __init__(self):
        self._lock = threading.RLock()

        self._state = "IDLE"
        self._prev_state = None
        self._state_timestamp = time.time()

        # Runtime flags
        self._running = False
        self._in_burst = False

    # -------------------------
    # State control
    # -------------------------

    def set_state(self, new_state: str):
        with self._lock:
            if new_state != self._state:
                self._prev_state = self._state
                self._state = new_state
                self._state_timestamp = time.time()

    def get_state(self):
        with self._lock:
            return self._state

    def get_prev_state(self):
        with self._lock:
            return self._prev_state

    def get_state_duration(self):
        with self._lock:
            return time.time() - self._state_timestamp

    def is_state(self, state_name: str):
        with self._lock:
            return self._state == state_name

    # -------------------------
    # Running flag
    # -------------------------

    def set_running(self, value: bool):
        with self._lock:
            self._running = value

    def is_running(self):
        with self._lock:
            return self._running

    # -------------------------
    # Burst flag
    # -------------------------

    def set_burst(self, value: bool):
        with self._lock:
            self._in_burst = value

    def is_in_burst(self):
        with self._lock:
            return self._in_burst

    # -------------------------
    # Reset
    # -------------------------

    def reset(self):
        with self._lock:
            self._state = "IDLE"
            self._prev_state = None
            self._state_timestamp = time.time()
            self._running = False
            self._in_burst = False