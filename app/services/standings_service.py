"""Application service that serves standings stored in SQLite."""

from __future__ import annotations

from fastapi import Request

from app.core.leagues import LeagueCatalog, sort_leagues_by_uefa_coefficient
from app.db.sqlite import StandingsRepository
from app.models.league import League
from app.models.standings import LeagueStandings
from app.services.base import LeagueNotFoundError, StandingsNotAvailableError


class StandingsService:
    def __init__(self, repository: StandingsRepository, catalog: LeagueCatalog) -> None:
        self._repository = repository
        self._catalog = catalog

    def list_leagues(self) -> list[League]:
        return sort_leagues_by_uefa_coefficient(self._catalog.all())

    def get_standings(self, league_code: str) -> LeagueStandings:
        league = self._catalog.get(league_code)
        if league is None:
            raise LeagueNotFoundError(league_code)

        stored = self._repository.get_standings(league.code)
        if stored is None:
            raise StandingsNotAvailableError(league.code)

        return LeagueStandings(
            league=league,
            table=stored.rows,
            season=stored.season,
            source=stored.source,
            updated_at=stored.updated_at,
        )


def get_standings_service(request: Request) -> StandingsService:
    """FastAPI dependency that returns the app's configured service."""
    return request.app.state.standings_service