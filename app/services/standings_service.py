"""Application service that coordinates providers, caching and domain objects."""

from __future__ import annotations

from app.core.config import Settings, get_settings
from app.core.leagues import LEAGUES, LEAGUES_BY_CODE
from app.db.cache import InMemoryCache
from app.models.league import League
from app.models.standings import LeagueStandings, StandingsData
from app.services.base import LeagueNotFoundError, StandingsProvider
from app.services.demo_provider import DemoProvider
from app.services.football_data_provider import FootballDataProvider


class StandingsService:
    def __init__(
        self,
        provider: StandingsProvider,
        cache: InMemoryCache | None = None,
    ) -> None:
        self._provider = provider
        self._cache = cache

    @property
    def source(self) -> str:
        return self._provider.source

    def list_leagues(self) -> list[League]:
        return list(LEAGUES)

    def get_standings(self, league_code: str) -> LeagueStandings:
        league = LEAGUES_BY_CODE.get(league_code.upper())
        if league is None:
            raise LeagueNotFoundError(league_code)

        data: StandingsData | None = None
        if self._cache is not None:
            data = self._cache.get(league.code)

        if data is None:
            data = self._provider.get_standings(league.code)
            if self._cache is not None:
                self._cache.set(league.code, data)

        return LeagueStandings(
            league=league,
            table=data.table,
            season=data.season,
            source=self._provider.source,
        )


def build_standings_service(settings: Settings | None = None) -> StandingsService:
    settings = settings or get_settings()

    provider: StandingsProvider
    if settings.football_data_api_key:
        provider = FootballDataProvider(settings)
    else:
        provider = DemoProvider()

    # Only live data needs caching (demo data is cheap and deterministic).
    cache = (
        InMemoryCache(ttl_seconds=settings.standings_cache_ttl_seconds)
        if provider.source == "live"
        else None
    )
    return StandingsService(provider, cache)


def get_standings_service() -> StandingsService:
    """FastAPI dependency factory."""
    return build_standings_service()