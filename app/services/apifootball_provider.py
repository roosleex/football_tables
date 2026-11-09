"""Standings provider backed by the api-football.com (API-Sports) API (v3)."""

from __future__ import annotations

import threading
import time
from typing import Any

import httpx

from app.core.config import Settings
from app.models.league import League
from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import ProviderError, StandingsProvider

# The frontend resolves the league name, country and Ukrainian team names by
# this code (it was added earlier for the openfootapi Czech league).
CZECH_LEAGUE_CODE = "comp_czech_first_league_cze"

_CZECH_LEAGUE_NAME = "Czech First League"
_CZECH_COUNTRY = "Czech Republic"
_CZECH_COUNTRY_CODE = "CZE"


class ApiFootballProvider:
    """api-football.com standings provider for the Czech First League.

    Requests are throttled to at most one HTTP request every
    ``apifootball_one_req_every_minutes`` minutes. Calls arriving before the
    interval has elapsed return the previously cached table.
    """

    source = "apifootball"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._league_id = settings.apifootball_czech_league_id
        self._interval_seconds = max(60, settings.apifootball_one_req_every_minutes * 60)
        self._lock = threading.Lock()
        self._season: int | None = None
        self._standings: StandingsData | None = None
        self._last_request_at = 0.0

    def _headers(self) -> dict[str, str]:
        return {"x-apisports-key": self._settings.apifootball_api_key or ""}

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        try:
            response = httpx.get(
                f"{self._settings.apifootball_base_url}{path}",
                params=params,
                headers=self._headers(),
                timeout=self._settings.http_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"api-football request failed: {exc}") from exc
        if response.status_code != 200:
            detail = response.text.strip().replace("\n", " ")[:200]
            raise ProviderError(f"api-football returned {response.status_code}: {detail}")
        return response.json()

    def get_leagues(self) -> list[League]:
        return [
            League(
                code=CZECH_LEAGUE_CODE,
                name=_CZECH_LEAGUE_NAME,
                country=_CZECH_COUNTRY,
                country_code=_CZECH_COUNTRY_CODE,
                emblem=None,
            )
        ]

    def get_standings(self, league_code: str) -> StandingsData:
        with self._lock:
            if (
                self._standings is not None
                and time.monotonic() - self._last_request_at < self._interval_seconds
            ):
                return self._standings

        season = self._current_season()
        standings = self._fetch_standings(season)

        with self._lock:
            self._standings = standings
            self._last_request_at = time.monotonic()
        return standings

    def get_team_form(self, league_code: str) -> dict[int, str]:
        return {}

    def _current_season(self) -> int:
        with self._lock:
            if self._season is not None:
                return self._season
        payload = self._get("/leagues", {"id": self._league_id, "current": "true"})
        season = _first_season_year(payload)
        with self._lock:
            self._season = season
        return season

    def _fetch_standings(self, season: int) -> StandingsData:
        payload = self._get("/standings", {"league": self._league_id, "season": season})
        return StandingsData(season=str(season), table=_parse_standings(payload))


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _first_season_year(payload: dict[str, Any]) -> int:
    leagues = payload.get("response") or []
    if not leagues:
        raise ProviderError("api-football: league not found")
    seasons = (leagues[0].get("league") or {}).get("seasons") or []
    if not seasons:
        raise ProviderError("api-football: no seasons available for the Czech league")
    return _int(seasons[0].get("year"))


def _group_index(group: str) -> int:
    name = (group or "").casefold()
    if "relegation" in name:
        return 2
    if "playoff" in name:
        return 1
    return 0


def _parse_standings(payload: dict[str, Any]) -> list[StandingRow]:
    rows: list[dict[str, Any]] = []
    for league in payload.get("response") or []:
        groups = (league.get("league") or {}).get("standings") or []
        for entries in groups:
            for entry in entries or []:
                team = entry.get("team") or {}
                overall = entry.get("all") or {}
                goals = overall.get("goals") or {}
                rows.append(
                    {
                        "group": entry.get("group") or "",
                        "rank": _int(entry.get("rank")),
                        "team_id": team.get("id"),
                        "name": team.get("name") or "Unknown",
                        "logo": team.get("logo"),
                        "points": _int(entry.get("points")),
                        "played": _int(overall.get("played")),
                        "won": _int(overall.get("win")),
                        "drawn": _int(overall.get("draw")),
                        "lost": _int(overall.get("lose")),
                        "goals_for": _int(goals.get("for")),
                        "goals_against": _int(goals.get("against")),
                        "goal_difference": _int(entry.get("goalsDiff")),
                        "form": entry.get("form") or "",
                    }
                )

    rows.sort(key=lambda row: (_group_index(row["group"]), row["rank"]))
    return [
        StandingRow(
            position=position,
            team=Team(id=row["team_id"], name=row["name"], crest=row["logo"]),
            played=row["played"],
            won=row["won"],
            drawn=row["drawn"],
            lost=row["lost"],
            goals_for=row["goals_for"],
            goals_against=row["goals_against"],
            goal_difference=row["goal_difference"],
            points=row["points"],
            form=",".join(list(row["form"])) if row["form"] else None,
        )
        for position, row in enumerate(rows, start=1)
    ]