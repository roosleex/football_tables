"""Standings schemas."""

from pydantic import BaseModel

from app.models.league import League


class Team(BaseModel):
    id: int | None = None
    name: str
    short_name: str | None = None
    tla: str | None = None
    crest: str | None = None


class StandingRow(BaseModel):
    position: int
    team: Team
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    form: str | None = None


class StandingsData(BaseModel):
    """Raw standings payload returned by a data provider."""

    season: str | None = None
    table: list[StandingRow]


class LeagueStandings(BaseModel):
    """Public standings response: league metadata + ordered table."""

    league: League
    table: list[StandingRow]
    season: str | None = None
    source: str = "demo"