"""Catalog of supported leagues.

``code`` matches football-data.org competition codes so live data can be
dropped in without changing the public API.
"""

from app.models.league import League

LEAGUES: list[League] = [
    League(code="PL", name="Premier League", country="England", country_code="GB"),
    League(code="PD", name="La Liga", country="Spain", country_code="ES"),
    League(code="BL1", name="Bundesliga", country="Germany", country_code="DE"),
    League(code="SA", name="Serie A", country="Italy", country_code="IT"),
    League(code="FL1", name="Ligue 1", country="France", country_code="FR"),
    League(code="DED", name="Eredivisie", country="Netherlands", country_code="NL"),
]

LEAGUES_BY_CODE: dict[str, League] = {league.code: league for league in LEAGUES}