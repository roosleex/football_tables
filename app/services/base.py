"""Shared contracts for standings data providers."""

from typing import Protocol

from app.models.standings import StandingsData


class LeagueNotFoundError(Exception):
    """Raised when a requested league code is not in the catalog."""


class ProviderError(Exception):
    """Raised when a data provider cannot fulfil a request."""


class StandingsNotAvailableError(Exception):
    """Raised when standings have not been loaded into storage yet."""


class StandingsProvider(Protocol):
    """Interface implemented by all standings data providers."""

    source: str

    def get_standings(self, league_code: str) -> StandingsData:
        """Return the ordered standings table for a league."""
        ...

    def get_team_form(self, league_code: str) -> dict[int, str]:
        """Return {team_id: 'W,D,W,L,W'} of recent results (live providers)."""
        ...