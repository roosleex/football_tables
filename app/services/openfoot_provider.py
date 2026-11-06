"""Standings provider for openfootapi.com (v1).

Currently scoped to the Ukrainian Premier League, which football-data.org does
not expose in its top-flight catalog.
"""

from __future__ import annotations

from typing import Any

import httpx

from app.core.config import Settings
from app.models.league import League
from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import ProviderError, StandingsProvider
from app.services.rate_limiter import RequestQueue

# openfootapi.com identifiers for the Ukrainian top flight.
_UKRAINIAN_LEAGUE_ID = "comp_premier_league_ukr"
_UKRAINIAN_COUNTRY_CODE = "UKR"  # ISO 3166-1 alpha-3 (Ukraine)


class OpenFootProvider:
    """openfootapi.com standings provider (Ukraine, tier 1)."""

    source = "openfoot"

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._queue = RequestQueue(settings.footapi_max_requests_per_minute)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self._queue.acquire()
        headers = {
            "Authorization": f"Bearer {self._settings.openfoot_api_key or ''}",
            "Accept": "application/json",
        }
        try:
            response = httpx.get(
                f"{self._settings.openfoot_base_url}{path}",
                headers=headers,
                params=params,
                timeout=self._settings.http_timeout_seconds,
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"openfootapi request failed: {exc}") from exc

        if response.status_code == 429:
            raise ProviderError("openfootapi rate limit exceeded")
        if response.status_code != 200:
            detail = response.text.strip().replace("\n", " ")[:160]
            raise ProviderError(f"openfootapi returned {response.status_code}: {detail}")

        payload = response.json()
        if not isinstance(payload, dict) or payload.get("data") is None:
            message = payload.get("message") if isinstance(payload, dict) else None
            raise ProviderError(f"openfootapi error: {message or 'no data'}")
        return payload

    def get_leagues(self) -> list[League]:
        payload = self._get("/v1/competitions")
        for comp in payload.get("data") or []:
            if comp.get("id") != _UKRAINIAN_LEAGUE_ID:
                continue
            coverage = comp.get("coverage") or {}
            if not coverage.get("standings"):
                raise ProviderError(f"{_UKRAINIAN_LEAGUE_ID} has no standings coverage")
            return [
                League(
                    code=comp.get("id", _UKRAINIAN_LEAGUE_ID),
                    name=comp.get("name") or "Ukrainian Premier League",
                    country=comp.get("country") or "Ukraine",
                    country_code=_UKRAINIAN_COUNTRY_CODE,
                    emblem=None,
                )
            ]
        raise ProviderError(
            f"Ukrainian Premier League ({_UKRAINIAN_LEAGUE_ID}) not found"
        )

    def get_standings(self, league_code: str) -> StandingsData:
        payload = self._get("/v1/standings", params={"competition": league_code})
        data = payload.get("data") or {}
        return StandingsData(
            season=data.get("season"),
            table=_parse_table(data.get("table") or []),
        )

    def get_team_form(self, league_code: str) -> dict[int, str]:
        # openfootapi returns each team's recent form in the standings table.
        return {}


def _parse_table(table: list[dict[str, Any]]) -> list[StandingRow]:
    rows: list[StandingRow] = []
    for entry in table:
        team = entry.get("team") or {}
        total = entry.get("total") or {}
        form = entry.get("form") or []
        rows.append(
            StandingRow(
                position=int(entry.get("position", 0)),
                team=Team(
                    name=team.get("name") or "Unknown",
                    short_name=team.get("shortName"),
                    tla=team.get("code"),
                    crest=team.get("logoUrl"),
                ),
                played=int(total.get("played", 0)),
                won=int(total.get("won", 0)),
                drawn=int(total.get("drawn", 0)),
                lost=int(total.get("lost", 0)),
                goals_for=int(total.get("goalsFor", 0)),
                goals_against=int(total.get("goalsAgainst", 0)),
                goal_difference=int(total.get("goalDifference", 0)),
                points=int(total.get("points", 0)),
                form=",".join(form) if form else None,
            )
        )
    return rows