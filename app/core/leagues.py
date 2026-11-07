"""Catalog of supported leagues."""

from __future__ import annotations

import threading

from app.models.league import League

# Fallback catalog used in demo mode (no football-data.org API key). It is kept
# in the current UEFA country-coefficient order so the menu reads naturally even
# before the scheduler has replaced it with the live catalog.
DEFAULT_LEAGUES: list[League] = [
    League(code="PL", name="Premier League", country="England", country_code="GB"),
    League(code="SA", name="Serie A", country="Italy", country_code="IT"),
    League(code="PD", name="La Liga", country="Spain", country_code="ES"),
    League(code="BL1", name="Bundesliga", country="Germany", country_code="DE"),
    League(code="FL1", name="Ligue 1", country="France", country_code="FR"),
    League(code="DED", name="Eredivisie", country="Netherlands", country_code="NL"),
]

# Current UEFA association club coefficients (country coefficients). The menu and
# the top-3 board are ordered by this ranking, strongest association first.
#
# Snapshot of the live ranking in the 2026/27 season; update the order below when
# UEFA publishes a newer association ranking.
#
# Each entry lists every country-code spelling used across providers so a league
# can be ranked no matter where it came from: football-data.org (ISO-3 codes such
# as "ENG"/"DEU"), openfootapi ("UKR"/"GRC"/"DNK"), or the demo catalog ("GB"/"DE").
_UEFA_COUNTRY_ORDER: tuple[tuple[str, ...], ...] = (
    ("ENG", "GB"),
    ("ITA", "IT"),
    ("ESP", "ES"),
    ("GER", "DEU", "DE"),
    ("FRA", "FR"),
    ("POR", "PRT", "PT"),
    ("BEL", "BE"),
    ("NED", "NLD", "NL"),
    ("TUR", "TR"),
    ("GRE", "GRC", "GR"),
    ("CZE", "CZ"),
    ("POL", "PL"),
    ("NOR", "NO"),
    ("DEN", "DNK", "DK"),
    ("CYP", "CY"),
    ("SUI", "CHE", "CH"),
    ("AUT", "AT"),
    ("HUN", "HU"),
    ("CRO", "HRV", "HR"),
    ("SWE", "SE"),
    ("SCO",),
    ("ROU", "RO"),
    ("UKR", "UA"),
    ("AZE", "AZ"),
    ("ISR", "IL"),
    ("SVN", "SI"),
    ("SVK", "SK"),
    ("BUL", "BGR", "BG"),
    ("SRB", "RS"),
    ("RUS", "RU"),
    ("ISL", "IS"),
    ("IRL", "IE"),
    ("ARM", "AM"),
    ("LVA", "LV"),
    ("BIH", "BA"),
    ("KOS", "XK"),
    ("FIN", "FI"),
    ("KAZ", "KZ"),
    ("LIE", "LI"),
    ("MDA", "MD"),
    ("FRO", "FO"),
    ("ALB", "AL"),
    ("MKD", "MK"),
    ("BLR", "BY"),
    ("LTU", "LT"),
    ("GIB", "GI"),
    ("AND", "AD"),
    ("MLT", "MT"),
    ("EST", "EE"),
    ("GEO", "GE"),
    ("NIR",),
    ("LUX", "LU"),
    ("MNE", "ME"),
    ("WAL",),
    ("SMR", "SM"),
)

_UEFA_COUNTRY_RANK: dict[str, int] = {
    code: rank
    for rank, codes in enumerate(_UEFA_COUNTRY_ORDER, start=1)
    for code in codes
}

# Associations without a known coefficient are shown last, sorted alphabetically.
_UEFA_UNRANKED_POSITION = len(_UEFA_COUNTRY_ORDER) + 1


def sort_leagues_by_uefa_coefficient(leagues: list[League]) -> list[League]:
    """Return leagues ordered by UEFA country coefficient, then by name."""

    def sort_key(league: League) -> tuple[int, str]:
        code = league.country_code.strip().upper()
        return (
            _UEFA_COUNTRY_RANK.get(code, _UEFA_UNRANKED_POSITION),
            league.name.casefold(),
        )

    return sorted(leagues, key=sort_key)


class LeagueCatalog:
    """A mutable, thread-safe list of leagues with a code lookup."""

    def __init__(self, leagues: list[League] | None = None) -> None:
        self._lock = threading.Lock()
        self._leagues: list[League] = []
        self._by_code: dict[str, League] = {}
        self.replace(leagues or [])

    def replace(self, leagues: list[League]) -> None:
        with self._lock:
            self._leagues = list(leagues)
            self._by_code = {league.code.upper(): league for league in self._leagues}

    def all(self) -> list[League]:
        with self._lock:
            return list(self._leagues)

    def get(self, code: str) -> League | None:
        with self._lock:
            return self._by_code.get(code.upper())