"""A thread-safe rate limiter for outbound requests (per-minute budget)."""

from __future__ import annotations

import threading
import time
from collections import deque


class RequestQueue:
    """Serializes requests so they never exceed ``max_per_minute`` per minute.

    Requests pass through immediately while fewer than ``max_per_minute`` have
    been sent in the last ``window_seconds`` (one minute by default). When the
    budget is exhausted, :meth:`acquire` blocks until a slot opens in the next
    (rolling) minute and then returns, so callers simply continue their queue.
    """

    def __init__(self, max_per_minute: int, window_seconds: float = 60.0) -> None:
        if max_per_minute < 1:
            raise ValueError("max_per_minute must be at least 1")
        self._max = max_per_minute
        self._window = window_seconds
        self._times: deque[float] = deque()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until a request slot is available, then claim it."""
        with self._lock:
            now = time.monotonic()
            self._expire_old(now)

            if len(self._times) >= self._max:
                # Budget exhausted: await the next minute until a slot frees up.
                wait = self._times[0] + self._window - now
                time.sleep(max(0.0, wait))
                now = time.monotonic()
                self._expire_old(now)

            self._times.append(now)

    def _expire_old(self, now: float) -> None:
        while self._times and now - self._times[0] >= self._window:
            self._times.popleft()

    @property
    def max_per_minute(self) -> int:
        return self._max