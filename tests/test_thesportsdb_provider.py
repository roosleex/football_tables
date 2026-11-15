"""Unit tests for thesportsdb.com standings parsing."""

from app.services.thesportsdb_provider import (
    _badge,
    _form,
    _parse_table,
    _season_label,
)


def _row(
    group: str,
    rank: str,
    team: str,
    team_id: str = "1",
    badge: str | None = None,
    form: str | None = "WDLDW",
) -> dict:
    return {
        "intRank": rank,
        "idTeam": team_id,
        "strTeam": team,
        "strBadge": badge or "https://cdn.test/badge/a.png/tiny",
        "strGroup": group,
        "strSeason": "2026-2027",
        "strForm": form,
        "intPlayed": "10",
        "intWin": "6",
        "intDraw": "2",
        "intLoss": "2",
        "intGoalsFor": "20",
        "intGoalsAgainst": "10",
        "intGoalDifference": "10",
        "intPoints": "20",
    }


def test_season_label_from_first_row() -> None:
    assert _season_label([_row("Czech Liga", "1", "A"), _row("Czech Liga", "2", "B")]) == "2026-2027"


def test_parse_table_maps_fields_and_orders_rows() -> None:
    rows = _parse_table(
        [
            _row("1. Liga , Relegation Round", "1", "Relegation Top"),
            _row("1. Liga , Championship Round", "2", "Runner Up"),
            _row("1. Liga , Championship Round", "1", "Champion"),
        ]
    )

    assert [row.position for row in rows] == [1, 2, 3]
    assert [row.team.name for row in rows] == ["Champion", "Runner Up", "Relegation Top"]
    first = rows[0]
    assert first.played == 10
    assert first.won == 6
    assert first.drawn == 2
    assert first.lost == 2
    assert first.goals_for == 20
    assert first.goals_against == 10
    assert first.goal_difference == 10
    assert first.points == 20
    assert first.form == "W,D,L,D,W"
    assert first.team.id == 1


def test_badge_drops_tiny_suffix() -> None:
    assert _badge("https://cdn.test/badge/a.png/tiny") == "https://cdn.test/badge/a.png"
    assert _badge("https://cdn.test/badge/a.png") == "https://cdn.test/badge/a.png"
    assert _badge(None) is None


def test_form_reformats_compact_string() -> None:
    assert _form("WDLDW") == "W,D,L,D,W"
    assert _form("") is None
    assert _form(None) is None