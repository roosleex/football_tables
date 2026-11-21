"""Tests for the standings application service."""

import pytest

from app.core.leagues import LeagueCatalog
from app.db.sqlite import StandingsRepository
from app.models.league import League
from app.models.standings import StandingRow, Team
from app.services.base import LeagueNotFoundError, StandingsNotAvailableError
from app.services.standings_service import StandingsService


def _league(
    code: str,
    standings_available: bool = True,
    country_code: str | None = None,
) -> League:
    return League(
        code=code,
        name=code,
        country="Country",
        country_code=country_code if country_code is not None else code,
        region="Europe",
        standings_available=standings_available,
    )


def _row(position: int, team_id: int) -> StandingRow:
    return StandingRow(
        position=position,
        team=Team(id=team_id, name="Team"),
        played=1,
        won=1,
        drawn=0,
        lost=0,
        goals_for=1,
        goals_against=0,
        goal_difference=1,
        points=3,
    )


def _repo(tmp_path) -> StandingsRepository:
    repo = StandingsRepository(tmp_path / "test.db")
    repo.init_schema()
    return repo


def test_get_standings_unknown_raises(tmp_path) -> None:
    service = StandingsService(_repo(tmp_path), LeagueCatalog())
    with pytest.raises(LeagueNotFoundError):
        service.get_standings("XX")


def test_get_standings_empty_when_unavailable(tmp_path) -> None:
    service = StandingsService(
        _repo(tmp_path), LeagueCatalog([_league("PL", standings_available=False)])
    )
    result = service.get_standings("pl")
    assert result.table == []
    assert result.source == "openfoot"


def test_get_standings_raises_when_not_loaded(tmp_path) -> None:
    service = StandingsService(_repo(tmp_path), LeagueCatalog([_league("PL")]))
    with pytest.raises(StandingsNotAvailableError):
        service.get_standings("PL")


def test_get_standings_returns_stored(tmp_path) -> None:
    repo = _repo(tmp_path)
    repo.save_standings("PL", "2025/26", "demo", [_row(1, 1)])
    service = StandingsService(repo, LeagueCatalog([_league("PL")]))

    result = service.get_standings("PL")
    assert result.league.code == "PL"
    assert result.season == "2025/26"
    assert result.source == "demo"
    assert len(result.table) == 1


def test_list_leagues_sorted_by_coefficient(tmp_path) -> None:
    service = StandingsService(
        _repo(tmp_path),
        LeagueCatalog(
            [
                _league("FL1", country_code="FR"),
                _league("PL", country_code="ENG"),
                _league("SA", country_code="IT"),
            ]
        ),
    )
    assert [league.code for league in service.list_leagues()] == ["PL", "SA", "FL1"]