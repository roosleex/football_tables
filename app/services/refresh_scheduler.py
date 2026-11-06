"""Background task that periodically refreshes leagues, standings and form."""

from __future__ import annotations

import logging
import threading
import time

from app.core.leagues import LeagueCatalog
from app.db.sqlite import StandingsRepository
from app.models.league import League
from app.services.base import ProviderError, StandingsProvider

logger = logging.getLogger(__name__)


class RefreshScheduler:
    """Fetches leagues and standings into SQLite on an interval.

    Leagues are gathered from one or more providers and each one is routed back
    to the provider that supplied it when its standings are refreshed. Requests
    go through each provider's per-minute queue, so updates never exceed a
    provider's rate limit.
    """

    def __init__(
        self,
        providers: list[StandingsProvider],
        repository: StandingsRepository,
        catalog: LeagueCatalog,
        interval_seconds: int = 60,
        form_interval_seconds: int = 600,
    ) -> None:
        self._providers = providers
        self._repository = repository
        self._catalog = catalog
        self._interval = interval_seconds
        self._form_interval = form_interval_seconds
        self._stop = threading.Event()
        self._last_form_refresh = 0.0
        self._provider_by_code: dict[str, StandingsProvider] = {}

    def refresh_leagues(self) -> None:
        merged: list[League] = []
        mapping: dict[str, StandingsProvider] = {}
        for provider in self._providers:
            try:
                leagues = provider.get_leagues()
            except ProviderError as exc:
                logger.warning(
                    "Skipping league list refresh from %s: %s", provider.source, exc
                )
                continue
            except Exception:  # pragma: no cover - defensive
                logger.exception(
                    "Unexpected error refreshing league list from %s", provider.source
                )
                continue
            for league in leagues:
                merged.append(league)
                mapping[league.code.upper()] = provider

        if merged:
            self._catalog.replace(merged)
            self._provider_by_code = mapping
            logger.info(
                "Loaded %d leagues from %d providers", len(merged), len(self._providers)
            )

    def refresh_standings(self) -> None:
        for league in self._catalog.all():
            provider = self._provider_by_code.get(league.code.upper())
            if provider is None:
                continue
            try:
                data = provider.get_standings(league.code)
                self._repository.save_standings(
                    league.code, data.season, provider.source, data.table
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
        for league in self._catalog.all():
            provider = self._provider_by_code.get(league.code.upper())
            if provider is None or provider.source != "live":
                continue
            try:
                form_by_team = provider.get_team_form(league.code)
                self._repository.apply_form(league.code, form_by_team)
                logger.info(
                    "Refreshed form for %s (%d teams)", league.code, len(form_by_team)
                )
            except ProviderError as exc:
                logger.warning("Skipping form for %s: %s", league.code, exc)
            except Exception:  # pragma: no cover - defensive
                logger.exception("Unexpected error refreshing form for %s", league.code)

    def _run(self) -> None:
        # Initial standings + form run in the background so server startup is
        # not blocked waiting on many league requests.
        self.refresh_standings()
        self._last_form_refresh = time.monotonic()
        self.refresh_form()

        while not self._stop.wait(self._interval):
            # Keep the catalog fresh (and self-heal if the startup fetch failed).
            self.refresh_leagues()
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