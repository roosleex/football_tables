"""Standings provider for openfootapi.com (v1).

Covers top-flight leagues that football-data.org does not expose on its free
tier: the Ukrainian Premier League, the Belgian Pro League, the Turkish Süper
Lig, the Greek Super League, the Polish Ekstraklasa,
the Norwegian Eliteserien, the Danish Superliga, the Cypriot First Division,
the Swiss Super League, the Austrian Bundesliga, the Nemzeti Bajnokság I, the
Croatian Football League (HNL), the Swedish Allsvenskan, the Scottish
Premiership, the Romanian SuperLiga, the Azerbaijan Premier League, the
Israeli Premier League, the Slovenian PrvaLiga, the Slovak Super Liga, the
Bulgarian First League, the Serbian SuperLiga, the Icelandic Besta deild, the
League of Ireland Premier Division, the Armenian Premier League, the Latvian
Virslīga, the Bosnian Premier League, the Kosovar Superleague, the
Veikkausliiga, the Kazakhstan Premier League, the Moldovan Super League, the
Faroe Islands Premier League, the Albanian Superliga, the North Macedonian
First League, the Lithuanian A Lyga, the Gibraltar Football League, the
Andorran Primera Divisió, the Maltese Premier League, the Estonian Premium
Liiga, the Georgian Erovnuli Liga, the Northern Irish Premiership, the
Luxembourg National Division, the Montenegrin First League, the Cymru Premier,
the Campionato Sammarinese, and the Asian top flights (Japan's J1 League, the
K League 1, the A-League, the Chinese Super League, the Indian Super League,
the Qatar Stars League, the UAE Pro League, the Saudi Pro League, the Persian
Gulf Pro League, the Uzbekistan Super League, Thai League 1, the Iraq Stars
League, Vietnam's V-League 1 and the Indonesia Super League). The
Liechtensteiner Cup is also exposed in the menu with an empty table, since
Liechtenstein has no domestic league.
"""

from __future__ import annotations

from typing import Any

import httpx

from app.core.config import Settings
from app.models.league import League
from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import ProviderError, StandingsProvider
from app.services.rate_limiter import RequestQueue

# openfootapi.com identifiers for top flights absent from football-data.org.
# id -> (fallback name, fallback country name, ISO 3166-1 alpha-3 country code)
_OPENFOOT_LEAGUES: dict[str, tuple[str, str, str]] = {
    "comp_premier_league_ukr": ("Ukrainian Premier League", "Ukraine", "UKR"),
    "comp_pro_league_be": ("Pro League", "Belgium", "BEL"),
    "comp_super_lig_tr": ("Süper Lig", "Turkey", "TUR"),
    "comp_super_league_grc": ("Super League", "Greece", "GRC"),
    "comp_ekstraklasa_pol": ("Ekstraklasa", "Poland", "POL"),
    "comp_eliteserien_nor": ("Eliteserien", "Norway", "NOR"),
    "comp_superliga_dnk": ("Danish Superliga", "Denmark", "DNK"),
    "comp_first_division_cyp": ("Cypriot First Division", "Cyprus", "CYP"),
    "comp_super_league_sui": ("Swiss Super League", "Switzerland", "CHE"),
    "comp_bundesliga_aut": ("Austrian Bundesliga", "Austria", "AUT"),
    "comp_nb_1_hun": ("Nemzeti Bajnokság I", "Hungary", "HUN"),
    "comp_hnl_cro": ("Croatian Football League (HNL)", "Croatia", "HRV"),
    "comp_allsvenskan_swe": ("Allsvenskan", "Sweden", "SWE"),
    "comp_scottish_prem_sco": ("Scottish Premiership", "Scotland", "SCO"),
    "comp_superliga_ro": ("SuperLiga", "Romania", "ROU"),
    "comp_premier_league_aze": ("Azerbaijan Premier League", "Azerbaijan", "AZE"),
    "comp_ligat_ha_al_isr": ("Israeli Premier League", "Israel", "ISR"),
    "comp_prva_liga_svn": ("Slovenian PrvaLiga", "Slovenia", "SVN"),
    "comp_nike_liga_svk": ("Slovak Super Liga", "Slovakia", "SVK"),
    "comp_parva_liga_bul": ("Bulgarian First League", "Bulgaria", "BGR"),
    "comp_superliga_srb": ("Serbian SuperLiga", "Serbia", "SRB"),
    "comp_besta_deild_isl": ("Icelandic Besta deild", "Iceland", "ISL"),
    "comp_premier_division_irl": (
        "League of Ireland Premier Division",
        "Ireland",
        "IRL",
    ),
    "comp_premier_league_arm": ("Armenian Premier League", "Armenia", "ARM"),
    "comp_virsliga_lva": ("Latvian Virslīga", "Latvia", "LVA"),
    "comp_premijer_liga_bih": (
        "Bosnian Premier League",
        "Bosnia and Herzegovina",
        "BIH",
    ),
    "comp_superliga_kos": ("Kosovar Superleague", "Kosovo", "KOS"),
    "comp_veikkausliiga_fin": ("Veikkausliiga", "Finland", "FIN"),
    "comp_premier_league_kaz": (
        "Kazakhstan Premier League",
        "Kazakhstan",
        "KAZ",
    ),
    "comp_national_division_mda": (
        "Moldovan Super League",
        "Moldova",
        "MDA",
    ),
    "comp_premier_league_fro": (
        "Faroe Islands Premier League",
        "Faroe Islands",
        "FRO",
    ),
    "comp_kategoria_superiore_alb": (
        "Albanian Superliga",
        "Albania",
        "ALB",
    ),
    "comp_prva_liga_mkd": (
        "North Macedonian First League",
        "North Macedonia",
        "MKD",
    ),
    "comp_a_lyga_ltu": (
        "Lithuanian A Lyga",
        "Lithuania",
        "LTU",
    ),
    "comp_football_league_gib": (
        "Gibraltar Football League",
        "Gibraltar",
        "GIB",
    ),
    "comp_primera_divisio_and": (
        "Andorran Primera Divisió",
        "Andorra",
        "AND",
    ),
    "comp_premier_league_mlt": (
        "Maltese Premier League",
        "Malta",
        "MLT",
    ),
    "comp_premium_liiga_est": (
        "Estonian Premium Liiga",
        "Estonia",
        "EST",
    ),
    "comp_erovnuli_liga_geo": (
        "Georgian Erovnuli Liga",
        "Georgia",
        "GEO",
    ),
    "comp_premiership_nir": (
        "Northern Irish Premiership",
        "Northern Ireland",
        "NIR",
    ),
    "comp_national_division_lux": (
        "Luxembourg National Division",
        "Luxembourg",
        "LUX",
    ),
    "comp_1_cfl_mne": (
        "Montenegrin First League",
        "Montenegro",
        "MNE",
    ),
    "comp_cymru_premier_wal": (
        "Cymru Premier",
        "Wales",
        "WAL",
    ),
    "comp_campionato_sammarinese_smr": (
        "Campionato Sammarinese",
        "San Marino",
        "SMR",
    ),
}

# Asian top flights exposed via openfootapi. They are grouped under the Asia
# menu entry, separate from the European competitions listed above.
_ASIAN_LEAGUES: dict[str, tuple[str, str, str]] = {
    "comp_j1_league_jpn": ("J1 League", "Japan", "JPN"),
    "comp_k_league_1_kor": ("K League 1", "South Korea", "KOR"),
    "comp_a_league_aus": ("A-League Men", "Australia", "AUS"),
    "comp_chinese_super_league_chn": ("Chinese Super League", "China", "CHN"),
    "comp_indian_super_league_ind": ("Indian Super League", "India", "IND"),
    "comp_qatar_stars_league_qat": ("Qatar Stars League", "Qatar", "QAT"),
    "comp_uae_pro_league_uae": ("UAE Pro League", "United Arab Emirates", "ARE"),
    "comp_saudi_pro_league_sau": ("Saudi Pro League", "Saudi Arabia", "SAU"),
    "comp_persian_gulf_league_irn": ("Persian Gulf Pro League", "Iran", "IRN"),
    "comp_super_league_uzb": ("Uzbek Super League", "Uzbekistan", "UZB"),
    "comp_thai_league_1_tha": ("Thai League 1", "Thailand", "THA"),
    "comp_stars_league_irq": ("Iraq Stars League", "Iraq", "IRQ"),
    "comp_v_league_vie": ("V-League 1", "Vietnam", "VNM"),
    "comp_super_league_idn": ("Indonesia Super League", "Indonesia", "IDN"),
}

# North American top flights exposed via openfootapi. They are grouped under the
# North America menu entry and cover the United States, Mexico, Canada and Costa
# Rica (the CONCACAF members whose domestic leagues openfootapi serves).
_NORTH_AMERICA_LEAGUES: dict[str, tuple[str, str, str]] = {
    "comp_mls_usa": ("Major League Soccer", "United States", "USA"),
    "comp_liga_mx_mex": ("Liga MX", "Mexico", "MEX"),
    "comp_canadian_premier_league_can": ("Canadian Premier League", "Canada", "CAN"),
    "comp_primera_division_crc": ("Primera División", "Costa Rica", "CRI"),
}

# South American top flights exposed via openfootapi. They are grouped under the
# South America menu entry and cover the ten CONMEBOL members whose domestic
# leagues openfootapi serves.
_SOUTH_AMERICA_LEAGUES: dict[str, tuple[str, str, str]] = {
    "comp_liga_profesional_arg": ("Argentine Primera División", "Argentina", "ARG"),
    "comp_primera_division_bol": ("Bolivian Primera División", "Bolivia", "BOL"),
    "comp_brasileirao_bra": ("Brasileirão Série A", "Brazil", "BRA"),
    "comp_primera_division_chi": ("Chilean Primera División", "Chile", "CHI"),
    "comp_primera_a_col": ("Categoría Primera A", "Colombia", "COL"),
    "comp_ligapro_ecu": ("LigaPro Serie A", "Ecuador", "ECU"),
    "comp_primera_division_par": ("Paraguayan Primera División", "Paraguay", "PAR"),
    "comp_liga_1_per": ("Liga 1", "Peru", "PER"),
    "comp_primera_division_uru": ("Uruguayan Primera División", "Uruguay", "URU"),
    "comp_primera_division_ven": ("Venezuelan Primera División", "Venezuela", "VEN"),
}

# African top flights exposed via openfootapi. They are grouped under the Africa
# menu entry and cover the CAF members whose domestic leagues openfootapi serves.
_AFRICA_LEAGUES: dict[str, tuple[str, str, str]] = {
    "comp_ligue_1_dza": ("Algerian Ligue 1", "Algeria", "DZA"),
    "comp_egyptian_prem_egy": ("Egyptian Premier League", "Egypt", "EGY"),
    "comp_botola_pro_mar": ("Botola Pro", "Morocco", "MAR"),
    "comp_npfl_nga": ("Nigerian Professional Football League", "Nigeria", "NGA"),
    "comp_psl_rsa": ("South African Premiership", "South Africa", "RSA"),
    "comp_ligue_1_tun": ("Tunisian Ligue 1", "Tunisia", "TUN"),
}

# Competitions exposed in the menu even though they have no standings table
# (Liechtenstein has no domestic league — only a cup). Selecting one shows an
# empty table.
_EMPTY_STANDINGS_LEAGUES: dict[str, tuple[str, str, str]] = {
    "comp_cup_lie": ("Liechtensteiner Cup", "Liechtenstein", "LIE"),
}


def _league_definitions() -> list[tuple[str, str, str, str, str]]:
    """Return every tracked league as ``(id, name, country, code, region)``."""
    definitions: list[tuple[str, str, str, str, str]] = []
    for league_id, (fallback_name, country, country_code) in _OPENFOOT_LEAGUES.items():
        definitions.append((league_id, fallback_name, country, country_code, "Europe"))
    for league_id, (fallback_name, country, country_code) in _ASIAN_LEAGUES.items():
        definitions.append((league_id, fallback_name, country, country_code, "Asia"))
    for league_id, (fallback_name, country, country_code) in _NORTH_AMERICA_LEAGUES.items():
        definitions.append((league_id, fallback_name, country, country_code, "North America"))
    for league_id, (fallback_name, country, country_code) in _SOUTH_AMERICA_LEAGUES.items():
        definitions.append((league_id, fallback_name, country, country_code, "South America"))
    for league_id, (fallback_name, country, country_code) in _AFRICA_LEAGUES.items():
        definitions.append((league_id, fallback_name, country, country_code, "Africa"))
    return definitions


class OpenFootProvider:
    """openfootapi.com standings provider for leagues missing from football-data.org."""

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
        by_id = {comp.get("id"): comp for comp in payload.get("data") or []}

        leagues: list[League] = []
        for league_id, fallback_name, country, country_code, region in _league_definitions():
            comp = by_id.get(league_id)
            if comp is None:
                raise ProviderError(f"{fallback_name} ({league_id}) not found")
            coverage = comp.get("coverage") or {}
            if not coverage.get("standings"):
                raise ProviderError(f"{league_id} has no standings coverage")
            leagues.append(
                League(
                    code=comp.get("id", league_id),
                    name=comp.get("name") or fallback_name,
                    country=comp.get("country") or country,
                    country_code=country_code,
                    region=region,
                    emblem=None,
                )
            )
        for league_id, (fallback_name, country, country_code) in _EMPTY_STANDINGS_LEAGUES.items():
            comp = by_id.get(league_id)
            leagues.append(
                League(
                    code=league_id,
                    name=(comp.get("name") if comp else None) or fallback_name,
                    country=(comp.get("country") if comp else None) or country,
                    country_code=country_code,
                    region="Europe",
                    emblem=None,
                    standings_available=False,
                )
            )
        return leagues

    def get_standings(self, league_code: str) -> StandingsData:
        if league_code in _EMPTY_STANDINGS_LEAGUES:
            return StandingsData(season=None, table=[])
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
        # openfootapi lists recent form most-recent-first; reverse it so the
        # rightmost badge in the Form column is the most recent (5th) result.
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
                form=",".join(reversed(form[:5])) if form else None,
            )
        )
    return rows