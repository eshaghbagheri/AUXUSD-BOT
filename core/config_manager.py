import json
import threading
import os
from copy import deepcopy


class ConfigManager:
    def __init__(self, config_path=None):

        # -------------------------
        # Resolve config path safely
        # -------------------------
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config", "settings.json")

        self.config_path = config_path

        # -------------------------
        # Init state (IMPORTANT FIX)
        # -------------------------
        self._lock = threading.RLock()
        self._config = {}

        self._load()

    # -------------------------
    # Load / Save
    # -------------------------
    def _load(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in config file: {e}")

        with self._lock:
            self._config = data

    def reload(self):
        self._load()

    def save(self):
        with self._lock:
            data = deepcopy(self._config)

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # -------------------------
    # Getters
    # -------------------------
    def get(self, key, default=None):
        with self._lock:
            return self._config.get(key, default)

    def get_all(self):
        with self._lock:
            return deepcopy(self._config)

    # -------------------------
    # Setters
    # -------------------------
    def set(self, key, value, auto_save=False):
        with self._lock:
            self._config[key] = value

        if auto_save:
            self.save()

    def update(self, data: dict, auto_save=False):
        with self._lock:
            self._config.update(data)

        if auto_save:
            self.save()

    # -------------------------
    # Typed helpers
    # -------------------------
    def get_float(self, key, default=0.0):
        try:
            return float(self.get(key, default))
        except:
            return default

    def get_int(self, key, default=0):
        try:
            return int(self.get(key, default))
        except:
            return default

    def get_bool(self, key, default=False):
        return bool(self.get(key, default))

    def get_str(self, key, default=""):
        return str(self.get(key, default))

    # -------------------------
    # Nested access
    # -------------------------
    def get_nested(self, *keys, default=None):
        with self._lock:
            data = self._config
            for k in keys:
                if isinstance(data, dict) and k in data:
                    data = data[k]
                else:
                    return default
            return deepcopy(data)

    def set_nested(self, keys, value, auto_save=False):
        with self._lock:
            data = self._config

            for k in keys[:-1]:
                if k not in data or not isinstance(data[k], dict):
                    data[k] = {}
                data = data[k]

            data[keys[-1]] = value

        if auto_save:
            self.save()