"""Live standings provider backed by the football-data.org API (v4)."""

from typing import Any

import httpx

from app.core.config import Settings
from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import ProviderError, StandingsProvider


class FootballDataProvider:
    """Fetches standings from https://api.football-data.org/v4."""

    source = "live"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_standings(self, league_code: str) -> StandingsData:
        url = (
            f"{self._settings.football_data_base_url}"
            f"/competitions/{league_code}/standings"
        )
        headers = {"X-Auth-Token": self._settings.football_data_api_key or ""}

        try:
            response = httpx.get(
                url,
                headers=headers,
                timeout=self._settings.http_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"request failed: {exc}") from exc

        if response.status_code == 429:
            raise ProviderError("football-data.org rate limit exceeded")
        if response.status_code != 200:
            raise ProviderError(f"football-data.org returned {response.status_code}")

        payload = response.json()
        return StandingsData(
            season=_season_label(payload),
            table=_parse_table(payload),
        )


def _parse_table(payload: dict[str, Any]) -> list[StandingRow]:
    standings = payload.get("standings") or []
    if not standings:
        raise ProviderError("no standings found in upstream response")

    # Prefer the aggregate table; fall back to the first available group.
    total = next((s for s in standings if s.get("type") == "TOTAL"), standings[0])

    rows: list[StandingRow] = []
    for entry in total.get("table", []) or []:
        team = entry.get("team") or {}
        rows.append(
            StandingRow(
                position=int(entry.get("position", 0)),
                team=Team(
                    id=team.get("id"),
                    name=team.get("name") or team.get("shortName") or "Unknown",
                    short_name=team.get("shortName"),
                    tla=team.get("tla"),
                    crest=team.get("crest"),
                ),
                played=int(entry.get("playedGames", 0)),
                won=int(entry.get("won", 0)),
                drawn=int(entry.get("draw", 0)),
                lost=int(entry.get("lost", 0)),
                goals_for=int(entry.get("goalsFor", 0)),
                goals_against=int(entry.get("goalsAgainst", 0)),
                goal_difference=int(entry.get("goalDifference", 0)),
                points=int(entry.get("points", 0)),
                form=entry.get("form"),
            )
        )
    return rows


def _season_label(payload: dict[str, Any]) -> str | None:
    season = payload.get("season") or {}
    start = (season.get("startDate") or "")[:4]
    end = (season.get("endDate") or "")[:4]
    if start and end:
        return f"{start}/{end[2:]}"
    return start or None