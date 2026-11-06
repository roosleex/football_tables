"""Unit tests for form derivation."""

from app.services.football_data_provider import _compute_form, _outcome


def test_outcome_draw() -> None:
    assert _outcome(True, "DRAW") == "D"
    assert _outcome(False, "DRAW") == "D"


def test_outcome_from_perspective() -> None:
    assert _outcome(True, "HOME_TEAM") == "W"
    assert _outcome(False, "HOME_TEAM") == "L"
    assert _outcome(True, "AWAY_TEAM") == "L"
    assert _outcome(False, "AWAY_TEAM") == "W"


def test_outcome_undecided() -> None:
    assert _outcome(True, None) is None


def _match(utc: str, home_id: int, away_id: int, winner: str | None) -> dict:
    return {
        "utcDate": utc,
        "score": {"winner": winner},
        "homeTeam": {"id": home_id},
        "awayTeam": {"id": away_id},
    }


def test_compute_form_keeps_last_five_in_order() -> None:
    matches = [
        _match("2026-01-01", 10, 20, "HOME_TEAM"),  # team 10: W
        _match("2026-01-08", 21, 10, "AWAY_TEAM"),  # team 10: W
        _match("2026-01-15", 10, 22, "DRAW"),       # team 10: D
        _match("2026-01-22", 23, 10, "HOME_TEAM"),  # team 10: L
        _match("2026-01-29", 10, 24, "AWAY_TEAM"),  # team 10: L
        _match("2026-02-05", 25, 10, "DRAW"),       # team 10: D
    ]
    result = _compute_form(matches)
    # Chronological results W,W,D,L,L,D -> drop the oldest W -> last five.
    assert result[10] == "W,D,L,L,D"
    assert result[20] == "L"