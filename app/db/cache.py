"""A minimal in-memory, time-to-live cache."""

import time
from typing import Any


class InMemoryCache:
    """Stores values for a fixed number of seconds."""

    def __init__(self, ttl_seconds: int = 300) -> None:
        self._ttl = ttl_seconds
        self._data: dict[str, tuple[float, Any]] = {}

    def get(self, key: str) -> Any | None:
        entry = self._data.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if expires_at < time.monotonic():
            self._data.pop(key, None)
            return None
        return value

    def set(self, key: str, value: Any) -> None:
        self._data[key] = (time.monotonic() + self._ttl, value)