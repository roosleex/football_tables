"""SQLite storage for standings snapshots."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.models.standings import StandingRow, Team

_SCHEMA = """
CREATE TABLE IF NOT EXISTS standings (
    league_code TEXT NOT NULL,
    position INTEGER NOT NULL,
    team_id INTEGER,
    team_name TEXT NOT NULL,
    team_short_name TEXT,
    team_tla TEXT,
    team_crest TEXT,
    played INTEGER NOT NULL,
    won INTEGER NOT NULL,
    drawn INTEGER NOT NULL,
    lost INTEGER NOT NULL,
    goals_for INTEGER NOT NULL,
    goals_against INTEGER NOT NULL,
    goal_difference INTEGER NOT NULL,
    points INTEGER NOT NULL,
    form TEXT,
    PRIMARY KEY (league_code, position)
);

CREATE TABLE IF NOT EXISTS standings_meta (
    league_code TEXT PRIMARY KEY,
    season TEXT,
    source TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


@dataclass
class StoredStandings:
    """A league's standings snapshot as persisted in SQLite."""

    season: str | None
    source: str
    updated_at: str
    rows: list[StandingRow]


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class StandingsRepository:
    """Reads and writes standings snapshots in a local SQLite database."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)

    def init_schema(self) -> None:
        conn = sqlite3.connect(self._db_path)
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(_SCHEMA)
            conn.commit()
        finally:
            conn.close()

    def save_standings(
        self,
        league_code: str,
        season: str | None,
        source: str,
        rows: list[StandingRow],
    ) -> None:
        now = _utcnow_iso()
        existing_form = self._existing_form(league_code)
        conn = sqlite3.connect(self._db_path)
        try:
            with conn:
                conn.execute(
                    "DELETE FROM standings WHERE league_code = ?", (league_code,)
                )
                conn.executemany(
                    """
                    INSERT INTO standings (
                        league_code, position, team_id, team_name, team_short_name,
                        team_tla, team_crest, played, won, drawn, lost,
                        goals_for, goals_against, goal_difference, points, form
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            league_code,
                            row.position,
                            row.team.id,
                            row.team.name,
                            row.team.short_name,
                            row.team.tla,
                            row.team.crest,
                            row.played,
                            row.won,
                            row.drawn,
                            row.lost,
                            row.goals_for,
                            row.goals_against,
                            row.goal_difference,
                            row.points,
                            row.form
                            if row.form is not None
                            else existing_form.get(row.team.id),
                        )
                        for row in rows
                    ],
                )
                conn.execute(
                    """
                    INSERT INTO standings_meta (league_code, season, source, updated_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(league_code) DO UPDATE SET
                        season = excluded.season,
                        source = excluded.source,
                        updated_at = excluded.updated_at
                    """,
                    (league_code, season, source, now),
                )
        finally:
            conn.close()

    def get_standings(self, league_code: str) -> StoredStandings | None:
        conn = sqlite3.connect(self._db_path)
        try:
            conn.row_factory = sqlite3.Row
            meta = conn.execute(
                "SELECT season, source, updated_at FROM standings_meta WHERE league_code = ?",
                (league_code,),
            ).fetchone()
            if meta is None:
                return None

            rows: list[StandingRow] = []
            for record in conn.execute(
                "SELECT * FROM standings WHERE league_code = ? ORDER BY position",
                (league_code,),
            ).fetchall():
                r = dict(record)
                rows.append(
                    StandingRow(
                        position=r["position"],
                        team=Team(
                            id=r["team_id"],
                            name=r["team_name"],
                            short_name=r["team_short_name"],
                            tla=r["team_tla"],
                            crest=r["team_crest"],
                        ),
                        played=r["played"],
                        won=r["won"],
                        drawn=r["drawn"],
                        lost=r["lost"],
                        goals_for=r["goals_for"],
                        goals_against=r["goals_against"],
                        goal_difference=r["goal_difference"],
                        points=r["points"],
                        form=r["form"],
                    )
                )

            if not rows:
                return None

            return StoredStandings(
                season=meta["season"],
                source=meta["source"],
                updated_at=meta["updated_at"],
                rows=rows,
            )
        finally:
            conn.close()

    def apply_form(self, league_code: str, form_by_team: dict[int, str]) -> None:
        """Update the form column for existing standings rows."""
        conn = sqlite3.connect(self._db_path)
        try:
            with conn:
                conn.executemany(
                    "UPDATE standings SET form = ? WHERE league_code = ? AND team_id = ?",
                    [
                        (form, league_code, team_id)
                        for team_id, form in form_by_team.items()
                    ],
                )
        finally:
            conn.close()

    def _existing_form(self, league_code: str) -> dict[int | None, str]:
        """Map team_id -> previously stored form so it survives standings saves."""
        conn = sqlite3.connect(self._db_path)
        try:
            conn.row_factory = sqlite3.Row
            records = conn.execute(
                "SELECT team_id, form FROM standings"
                " WHERE league_code = ? AND form IS NOT NULL",
                (league_code,),
            ).fetchall()
            return {record["team_id"]: record["form"] for record in records}
        finally:
            conn.close()