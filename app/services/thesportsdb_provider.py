"""Standings provider backed by thesportsdb.com (free v1 API).

Covers the Czech First League, which is not exposed by football-data.org's
free tier and was previously sourced from api-football.com. The public free
API key ("123") is used unless THESPORTSDB_API_KEY is configured, and requests
are throttled by THESPORTSDB_MAX_REQUESTS_PER_MINUTE.
"""

from __future__ import annotations

from typing import Any

import httpx

from app.core.config import Settings
from app.models.league import League
from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import ProviderError, StandingsProvider
from app.services.rate_limiter import RequestQueue

# The frontend resolves the league name, country and Ukrainian team names by
# this code (it was added earlier for the openfootapi Czech league).
CZECH_LEAGUE_CODE = "comp_czech_first_league_cze"

_CZECH_LEAGUE_ID = "4631"
_CZECH_LEAGUE_NAME = "Czech First League"
_CZECH_COUNTRY = "Czech Republic"
_CZECH_COUNTRY_CODE = "CZE"

_FALLBACK_API_KEY = "123"


class TheSportsDbProvider:
    """thesportsdb.com standings provider for the Czech First League."""

    source = "thesportsdb"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._api_key = settings.thesportsdb_api_key or _FALLBACK_API_KEY
        self._queue = RequestQueue(settings.thesportsdb_max_requests_per_minute)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._queue.acquire()
        url = f"{self._settings.thesportsdb_base_url}/{self._api_key}/{path}"
        try:
            response = httpx.get(
                url,
                params=params,
                timeout=self._settings.http_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"thesportsdb request failed: {exc}") from exc

        if response.status_code == 429:
            raise ProviderError("thesportsdb rate limit exceeded")
        if response.status_code != 200:
            detail = response.text.strip().replace("\n", " ")[:200]
            raise ProviderError(f"thesportsdb returned {response.status_code}: {detail}")

        payload = response.json()
        if not isinstance(payload, dict):
            raise ProviderError("thesportsdb returned an unexpected response")
        return payload

    def get_leagues(self) -> list[League]:
        # The Czech First League is a single, statically-known league, so no
        # upstream list request is required here.
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
        # Omitting the season returns the current season's table, and each row
        # includes the season label, so a single request is enough per refresh.
        payload = self._get("lookuptable.php", params={"l": _CZECH_LEAGUE_ID})
        entries = payload.get("table") or []
        if not entries:
            raise ProviderError("thesportsdb: no standings for the Czech First League")
        return StandingsData(
            season=_season_label(entries),
            table=_parse_table(entries),
        )

    def get_team_form(self, league_code: str) -> dict[int, str]:
        # The standings rows already include each team's recent form.
        return {}


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _season_label(entries: list[dict[str, Any]]) -> str | None:
    for entry in entries:
        season = entry.get("strSeason")
        if season:
            return str(season)
    return None


def _parse_table(entries: list[dict[str, Any]]) -> list[StandingRow]:
    """Map thesportsdb table rows into ordered standings rows.

    The Czech league sometimes splits into a Championship round and a Relegation
    round; keep the Championship/regular section ahead of the relegation section
    and enumerate final positions from top to bottom.
    """
    raw: list[dict[str, Any]] = []
    for entry in entries:
        raw.append(
            {
                "group": entry.get("strGroup") or "",
                "rank": _int(entry.get("intRank")),
                "team": _team(entry),
                "played": _int(entry.get("intPlayed")),
                "won": _int(entry.get("intWin")),
                "drawn": _int(entry.get("intDraw")),
                "lost": _int(entry.get("intLoss")),
                "goals_for": _int(entry.get("intGoalsFor")),
                "goals_against": _int(entry.get("intGoalsAgainst")),
                "goal_difference": _int(entry.get("intGoalDifference")),
                "points": _int(entry.get("intPoints")),
                "form": _form(entry.get("strForm")),
            }
        )

    raw.sort(key=lambda row: (_group_index(row["group"]), row["rank"]))

    return [
        StandingRow(
            position=position,
            team=row["team"],
            played=row["played"],
            won=row["won"],
            drawn=row["drawn"],
            lost=row["lost"],
            goals_for=row["goals_for"],
            goals_against=row["goals_against"],
            goal_difference=row["goal_difference"],
            points=row["points"],
            form=row["form"],
        )
        for position, row in enumerate(raw, start=1)
    ]


def _team(entry: dict[str, Any]) -> Team:
    team_id = entry.get("idTeam")
    return Team(
        id=_int(team_id) if team_id is not None else None,
        name=entry.get("strTeam") or "Unknown",
        crest=_badge(entry.get("strBadge")),
    )


def _badge(value: Any) -> str | None:
    if not value:
        return None
    badge = str(value)
    # TheSportsDB appends "/tiny" to badge URLs; strip it for the full image.
    return badge[:-5] if badge.endswith("/tiny") else badge


def _form(value: Any) -> str | None:
    form = (value or "").strip()
    if not form:
        return None
    return ",".join(list(form))


def _group_index(group: str) -> int:
    name = (group or "").casefold()
    if "relegation" in name:
        return 2
    return 0