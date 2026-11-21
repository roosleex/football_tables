"""Tests for the deterministic demo provider."""

from app.services.demo_provider import DemoProvider, _initials


def test_get_leagues_returns_default_catalog() -> None:
    provider = DemoProvider()
    leagues = provider.get_leagues()
    assert {league.code for league in leagues} == {"PL", "PD", "BL1", "SA", "FL1", "DED"}
    assert len(leagues) == 6


def test_get_standings_is_deterministic_and_sorted() -> None:
    provider = DemoProvider()
    data = provider.get_standings("PL")
    assert data.season == "2025/26"
    assert len(data.table) == 20
    assert [row.position for row in data.table] == list(range(1, 21))
    points = [row.points for row in data.table]
    assert points == sorted(points, reverse=True)

    again = provider.get_standings("PL")
    assert [row.team.name for row in again.table] == [row.team.name for row in data.table]


def test_get_standings_unknown_code_returns_empty() -> None:
    data = DemoProvider().get_standings("UNKNOWN")
    assert data.table == []


def test_get_team_form_is_empty() -> None:
    assert DemoProvider().get_team_form("PL") == {}


def test_initials() -> None:
    assert _initials("Arsenal") == "ARS"
    assert _initials("Real Madrid") == "RM"