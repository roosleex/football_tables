"""Tests for football-data.org response parsing and league filtering."""

import pytest

from app.core.config import Settings
from app.services.base import ProviderError
from app.services.football_data_provider import (
    FootballDataProvider,
    _parse_table,
    _season_label,
)


def _entry(
    position: int,
    name: str | None = None,
    *,
    team: dict | None = None,
    **overrides,
) -> dict:
    entry = {
        "position": str(position),
        "team": team if team is not None else {"id": position, "name": name},
        "playedGames": 10,
        "won": 6,
        "draw": 2,
        "lost": 2,
        "goalsFor": 20,
        "goalsAgainst": 10,
        "goalDifference": 10,
        "points": 20,
    }
    entry.update(overrides)
    return entry


def test_parse_table_maps_fields() -> None:
    rows = _parse_table({"standings": [{"type": "TOTAL", "table": [_entry(1, "Arsenal")]}]})
    assert len(rows) == 1
    row = rows[0]
    assert row.position == 1
    assert row.team.id == 1
    assert row.team.name == "Arsenal"
    assert row.played == 10
    assert row.won == 6
    assert row.drawn == 2
    assert row.lost == 2
    assert row.goals_for == 20
    assert row.goals_against == 10
    assert row.goal_difference == 10
    assert row.points == 20
    assert row.form is None


def test_parse_table_prefers_total_type() -> None:
    payload = {
        "standings": [
            {"type": "HOME", "table": [_entry(1, "Home")]},
            {"type": "TOTAL", "table": [_entry(2, "Total")]},
        ]
    }
    rows = _parse_table(payload)
    assert [row.team.name for row in rows] == ["Total"]


def test_parse_table_falls_back_to_first_when_no_total() -> None:
    payload = {"standings": [{"type": "AWAY", "table": [_entry(3, "First")]}]}
    rows = _parse_table(payload)
    assert [row.team.name for row in rows] == ["First"]


def test_parse_table_team_name_falls_back_to_short_name() -> None:
    rows = _parse_table(
        {
            "standings": [
                {
                    "type": "TOTAL",
                    "table": [_entry(1, team={"id": 1, "shortName": "Short"})],
                }
            ]
        }
    )
    assert rows[0].team.name == "Short"


def test_parse_table_raises_when_no_standings() -> None:
    with pytest.raises(ProviderError):
        _parse_table({"standings": []})
    with pytest.raises(ProviderError):
        _parse_table({})


def test_season_label() -> None:
    payload = {"season": {"startDate": "2025-08-01", "endDate": "2026-05-31"}}
    assert _season_label(payload) == "2025/26"
    assert _season_label({"season": {"startDate": "2025-08-01"}}) == "2025"
    assert _season_label({}) is None


def test_get_leagues_filters_type_country_and_exclusions(monkeypatch) -> None:
    provider = FootballDataProvider(
        Settings(football_data_api_key="key", excluded_league_codes=["ELC"])
    )
    payload = {
        "competitions": [
            {
                "type": "LEAGUE",
                "code": "PL",
                "name": "Premier League",
                "area": {"code": "ENG", "name": "England"},
                "emblem": None,
            },
            {
                "type": "LEAGUE",
                "code": "ELC",
                "name": "Championship",
                "area": {"code": "ENG", "name": "England"},
                "emblem": None,
            },
            {
                "type": "CUP",
                "code": "FAC",
                "name": "FA Cup",
                "area": {"code": "ENG", "name": "England"},
                "emblem": None,
            },
            {
                "type": "LEAGUE",
                "code": "MLS",
                "name": "Major League Soccer",
                "area": {"code": "USA", "name": "United States"},
                "emblem": None,
            },
        ]
    }
    monkeypatch.setattr(provider, "_get", lambda *args, **kwargs: payload)

    leagues = provider.get_leagues()
    assert [league.code for league in leagues] == ["PL"]
    assert leagues[0].name == "Premier League"
    assert leagues[0].country == "England"
    assert leagues[0].country_code == "ENG"