"""Tests for the SQLite standings repository."""

from app.db.sqlite import StandingsRepository
from app.models.standings import StandingRow, Team


def _row(position: int, team_id: int, name: str, form: str | None = None) -> StandingRow:
    return StandingRow(
        position=position,
        team=Team(
            id=team_id,
            name=name,
            short_name=name,
            tla=name[:3].upper(),
            crest=None,
        ),
        played=10,
        won=6,
        drawn=2,
        lost=2,
        goals_for=20,
        goals_against=10,
        goal_difference=10,
        points=20,
        form=form,
    )


def test_init_schema_and_round_trip(tmp_path) -> None:
    repo = StandingsRepository(tmp_path / "test.db")
    repo.init_schema()

    repo.save_standings(
        "PL", "2025/26", "demo", [_row(1, 1, "Arsenal"), _row(2, 2, "Chelsea")]
    )

    stored = repo.get_standings("PL")
    assert stored is not None
    assert stored.season == "2025/26"
    assert stored.source == "demo"
    assert stored.updated_at is not None
    assert [row.team.name for row in stored.rows] == ["Arsenal", "Chelsea"]
    assert [row.position for row in stored.rows] == [1, 2]
    assert all(row.form is None for row in stored.rows)


def test_get_standings_unknown_returns_none(tmp_path) -> None:
    repo = StandingsRepository(tmp_path / "test.db")
    repo.init_schema()
    assert repo.get_standings("XX") is None


def test_save_replaces_previous_rows(tmp_path) -> None:
    repo = StandingsRepository(tmp_path / "test.db")
    repo.init_schema()

    repo.save_standings("PL", "2024/25", "demo", [_row(1, 1, "A"), _row(2, 2, "B")])
    repo.save_standings("PL", "2025/26", "demo", [_row(1, 1, "A")])

    stored = repo.get_standings("PL")
    assert stored is not None
    assert stored.season == "2025/26"
    assert [row.position for row in stored.rows] == [1]
    assert stored.rows[0].team.name == "A"


def test_save_preserves_existing_form_when_new_form_missing(tmp_path) -> None:
    repo = StandingsRepository(tmp_path / "test.db")
    repo.init_schema()

    repo.save_standings("PL", "2024/25", "demo", [_row(1, 1, "A", form="W,D,W")])
    repo.save_standings("PL", "2025/26", "demo", [_row(1, 1, "A")])

    stored = repo.get_standings("PL")
    assert stored is not None
    assert stored.rows[0].form == "W,D,W"


def test_apply_form_updates_matching_team(tmp_path) -> None:
    repo = StandingsRepository(tmp_path / "test.db")
    repo.init_schema()

    repo.save_standings("PL", "2024/25", "demo", [_row(1, 1, "A"), _row(2, 2, "B")])
    repo.apply_form("PL", {1: "W,W,W,W,W"})

    stored = repo.get_standings("PL")
    assert stored is not None
    by_id = {row.team.id: row.form for row in stored.rows}
    assert by_id[1] == "W,W,W,W,W"
    assert by_id[2] is None