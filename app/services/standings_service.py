"""Application service that serves standings stored in SQLite."""

from __future__ import annotations

from fastapi import Request

from app.core.leagues import LEAGUES, LEAGUES_BY_CODE
from app.db.sqlite import StandingsRepository
from app.models.league import League
from app.models.standings import LeagueStandings
from app.services.base import LeagueNotFoundError, StandingsNotAvailableError


class StandingsService:
    def __init__(self, repository: StandingsRepository) -> None:
        self._repository = repository

    def list_leagues(self) -> list[League]:
        return list(LEAGUES)

    def get_standings(self, league_code: str) -> LeagueStandings:
        league = LEAGUES_BY_CODE.get(league_code.upper())
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