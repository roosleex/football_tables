"""API routes."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import get_settings
from app.models.league import League
from app.models.standings import LeagueStandings
from app.services.base import LeagueNotFoundError, ProviderError
from app.services.standings_service import (
    StandingsService,
    get_standings_service,
)

router = APIRouter()


@router.get("/health", tags=["meta"])
def health() -> dict[str, Any]:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "data_source": "live" if settings.football_data_api_key else "demo",
    }


@router.get("/leagues", response_model=list[League], tags=["leagues"])
def list_leagues(
    service: StandingsService = Depends(get_standings_service),
) -> list[League]:
    return service.list_leagues()


@router.get(
    "/leagues/{league_code}/standings",
    response_model=LeagueStandings,
    tags=["leagues"],
)
def get_league_standings(
    league_code: str,
    service: StandingsService = Depends(get_standings_service),
) -> LeagueStandings:
    try:
        return service.get_standings(league_code)
    except LeagueNotFoundError:
        raise HTTPException(status_code=404, detail=f"Unknown league: {league_code}")
    except ProviderError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Upstream data provider error: {exc}",
        )