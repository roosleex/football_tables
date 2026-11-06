"""Tests for the per-minute request queue."""

import time

from app.services.rate_limiter import RequestQueue


def test_acquires_up_to_budget_without_blocking() -> None:
    queue = RequestQueue(max_per_minute=3)
    start = time.monotonic()
    queue.acquire()
    queue.acquire()
    queue.acquire()
    assert time.monotonic() - start < 0.1


def test_blocks_until_next_window_once_budget_exceeded() -> None:
    # Small window keeps the test fast: 2 slots per 0.3s.
    queue = RequestQueue(max_per_minute=2, window_seconds=0.3)
    start = time.monotonic()
    queue.acquire()
    queue.acquire()
    queue.acquire()  # third slot must wait for the first to expire
    assert time.monotonic() - start >= 0.25