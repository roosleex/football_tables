"""Catalog of supported leagues."""

from __future__ import annotations

import threading

from app.models.league import League

# Fallback catalog used in demo mode (no football-data.org API key).
DEFAULT_LEAGUES: list[League] = [
    League(code="PL", name="Premier League", country="England", country_code="GB"),
    League(code="PD", name="La Liga", country="Spain", country_code="ES"),
    League(code="BL1", name="Bundesliga", country="Germany", country_code="DE"),
    League(code="SA", name="Serie A", country="Italy", country_code="IT"),
    League(code="FL1", name="Ligue 1", country="France", country_code="FR"),
    League(code="DED", name="Eredivisie", country="Netherlands", country_code="NL"),
]


class LeagueCatalog:
    """A mutable, thread-safe list of leagues with a code lookup."""

    def __init__(self, leagues: list[League] | None = None) -> None:
        self._lock = threading.Lock()
        self._leagues: list[League] = []
        self._by_code: dict[str, League] = {}
        self.replace(leagues or [])

    def replace(self, leagues: list[League]) -> None:
        with self._lock:
            self._leagues = list(leagues)
            self._by_code = {league.code.upper(): league for league in self._leagues}

    def all(self) -> list[League]:
        with self._lock:
            return list(self._leagues)

    def get(self, code: str) -> League | None:
        with self._lock:
            return self._by_code.get(code.upper())