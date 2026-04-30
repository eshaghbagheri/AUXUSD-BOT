# events/event_bus.py

import threading
from collections import defaultdict
from typing import Callable, Any, Dict, List


class EventBus:
    def __init__(self):
        self._lock = threading.RLock()
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)

    # -------------------------
    # Subscribe / Unsubscribe
    # -------------------------

    def subscribe(self, event_name: str, handler: Callable):
        with self._lock:
            if handler not in self._subscribers[event_name]:
                self._subscribers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: Callable):
        with self._lock:
            if handler in self._subscribers[event_name]:
                self._subscribers[event_name].remove(handler)

    # -------------------------
    # Publish
    # -------------------------

    def publish(self, event_name: str, data: Any = None):
        with self._lock:
            handlers = list(self._subscribers[event_name])

        for handler in handlers:
            try:
                handler(data)
            except Exception as e:
                # جلوگیری از کرش کل سیستم
                print(f"[EVENT ERROR] {event_name} -> {e}")

    # -------------------------
    # Clear
    # -------------------------

    def clear(self):
        with self._lock:
            self._subscribers.clear()