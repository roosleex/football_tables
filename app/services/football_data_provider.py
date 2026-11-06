"""Live standings provider backed by the football-data.org API (v4)."""

from __future__ import annotations

from typing import Any

import httpx

from app.core.config import Settings
from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import ProviderError, StandingsProvider
from app.services.rate_limiter import RequestQueue


class FootballDataProvider:
    """Fetches standings and recent-match form from football-data.org (v4)."""

    source = "live"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._queue = RequestQueue(settings.max_requests_per_minute)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._queue.acquire()
        headers = {"X-Auth-Token": self._settings.football_data_api_key or ""}
        try:
            response = httpx.get(
                f"{self._settings.football_data_base_url}{path}",
                headers=headers,
                params=params,
                timeout=self._settings.http_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"request failed: {exc}") from exc

        if response.status_code == 429:
            raise ProviderError("football-data.org rate limit exceeded")
        if response.status_code != 200:
            detail = response.text.strip().replace("\n", " ")[:200]
            raise ProviderError(
                f"football-data.org returned {response.status_code}: {detail}"
            )
        return response.json()

    def get_standings(self, league_code: str) -> StandingsData:
        payload = self._get(f"/competitions/{league_code}/standings")
        return StandingsData(
            season=_season_label(payload),
            table=_parse_table(payload),
        )

    def get_team_form(self, league_code: str) -> dict[int, str]:
        """Return `{team_id: 'W,D,W,L,W'}` for every team with recent results."""
        # Request the current season's finished matches only. No date filter is
        # used because some competitions reject an explicit `dateFrom`.
        payload = self._get(
            f"/competitions/{league_code}/matches",
            params={"status": "FINISHED"},
        )
        return _compute_form(payload.get("matches") or [])


def _compute_form(matches: list[dict[str, Any]]) -> dict[int, str]:
    """Derive each team's last-5 form from a list of matches."""
    results: dict[int, list[str]] = {}
    ordered = sorted(matches, key=lambda m: m.get("utcDate") or "")
    for match in ordered:
        winner = (match.get("score") or {}).get("winner")
        home = match.get("homeTeam") or {}
        away = match.get("awayTeam") or {}
        for team, is_home in ((home, True), (away, False)):
            team_id = team.get("id")
            if team_id is None:
                continue
            outcome = _outcome(is_home, winner)
            if outcome:
                results.setdefault(int(team_id), []).append(outcome)
    return {team_id: ",".join(seq[-5:]) for team_id, seq in results.items()}


def _outcome(is_home: bool, winner: Any) -> str | None:
    if winner == "DRAW":
        return "D"
    if winner == "HOME_TEAM":
        return "W" if is_home else "L"
    if winner == "AWAY_TEAM":
        return "L" if is_home else "W"
    return None


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
                # The standings endpoint does not provide per-team form; it is
                # derived from match history via get_team_form() instead.
                form=None,
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