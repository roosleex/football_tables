"""Background task that periodically refreshes standings into SQLite."""

from __future__ import annotations

import logging
import threading
import time

from app.core.leagues import LEAGUES
from app.db.sqlite import StandingsRepository
from app.models.league import League
from app.services.base import ProviderError, StandingsProvider

logger = logging.getLogger(__name__)


class RefreshScheduler:
    """Fetches standings (and form) for every league into SQLite on an interval.

    Requests for all leagues go through the provider's per-minute queue, so
    updates never exceed ``MAX_REQUESTS_PER_MINUTE``; if the budget is exhausted
    the remaining leagues wait for the next minute and then continue.
    """

    def __init__(
        self,
        provider: StandingsProvider,
        repository: StandingsRepository,
        leagues: list[League] | None = None,
        interval_seconds: int = 60,
        form_interval_seconds: int = 600,
    ) -> None:
        self._provider = provider
        self._repository = repository
        self._leagues = leagues if leagues is not None else list(LEAGUES)
        self._interval = interval_seconds
        self._form_interval = form_interval_seconds
        self._stop = threading.Event()
        self._last_form_refresh = 0.0

    def refresh_standings(self) -> None:
        for league in self._leagues:
            try:
                data = self._provider.get_standings(league.code)
                self._repository.save_standings(
                    league.code, data.season, self._provider.source, data.table
                )
                logger.info(
                    "Refreshed standings for %s (%d teams)", league.code, len(data.table)
                )
            except ProviderError as exc:
                logger.warning("Skipping standings for %s: %s", league.code, exc)
            except Exception:  # pragma: no cover - defensive
                logger.exception("Unexpected error refreshing standings for %s", league.code)

    def refresh_form(self) -> None:
        # Form is derived from match history, which only the live provider exposes.
        if self._provider.source != "live":
            return
        for league in self._leagues:
            try:
                form_by_team = self._provider.get_team_form(league.code)
                self._repository.apply_form(league.code, form_by_team)
                logger.info(
                    "Refreshed form for %s (%d teams)", league.code, len(form_by_team)
                )
            except ProviderError as exc:
                logger.warning("Skipping form for %s: %s", league.code, exc)
            except Exception:  # pragma: no cover - defensive
                logger.exception("Unexpected error refreshing form for %s", league.code)

    def _run(self) -> None:
        # Standings are loaded synchronously at startup; compute form next.
        self._last_form_refresh = time.monotonic()
        self.refresh_form()

        while not self._stop.wait(self._interval):
            self.refresh_standings()
            if time.monotonic() - self._last_form_refresh >= self._form_interval:
                self.refresh_form()
                self._last_form_refresh = time.monotonic()

    def start(self) -> threading.Thread:
        thread = threading.Thread(target=self._run, name="standings-refresh", daemon=True)
        thread.start()
        return thread

    def stop(self) -> None:
        self._stop.set()