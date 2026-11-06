"""Deterministic demo standings used when no live data source is configured.

The squad lists below are illustrative and are replaced by live data as soon as
``FOOTBALL_DATA_API_KEY`` is set.
"""

import random

from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import StandingsProvider

_PREMIER_LEAGUE = [
    "Arsenal", "Aston Villa", "Bournemouth", "Brentford", "Brighton & Hove Albion",
    "Chelsea", "Crystal Palace", "Everton", "Fulham", "Liverpool",
    "Manchester City", "Manchester United", "Newcastle United", "Nottingham Forest",
    "Tottenham Hotspur", "West Ham United", "Wolverhampton Wanderers",
    "Ipswich Town", "Leicester City", "Southampton",
]

_LA_LIGA = [
    "Real Madrid", "Barcelona", "Atletico Madrid", "Athletic Bilbao", "Sevilla",
    "Real Sociedad", "Real Betis", "Villarreal", "Valencia", "Girona",
    "Osasuna", "Celta Vigo", "Rayo Vallecano", "Mallorca", "Getafe",
    "Alaves", "Espanyol", "Leganes", "Las Palmas", "Real Valladolid",
]

_BUNDESLIGA = [
    "Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen",
    "Eintracht Frankfurt", "VfB Stuttgart", "Borussia Monchengladbach", "SC Freiburg",
    "VfL Wolfsburg", "Werder Bremen", "Hoffenheim", "Mainz 05",
    "Union Berlin", "Augsburg", "St. Pauli", "Heidenheim",
    "Holstein Kiel", "Bochum",
]

_SERIE_A = [
    "Inter Milan", "AC Milan", "Juventus", "Napoli", "Atalanta",
    "AS Roma", "Lazio", "Fiorentina", "Bologna", "Torino",
    "Genoa", "Udinese", "Cagliari", "Empoli", "Lecce",
    "Verona", "Parma", "Como", "Monza", "Venezia",
]

_LIGUE_1 = [
    "Paris Saint-Germain", "Marseille", "Monaco", "Lyon", "Lille",
    "Nice", "Lens", "Rennes", "Strasbourg", "Nantes",
    "Reims", "Montpellier", "Toulouse", "Auxerre", "Angers",
    "Le Havre", "Saint-Etienne", "Brest",
]

_EREDIVISIE = [
    "Ajax", "PSV Eindhoven", "Feyenoord", "AZ Alkmaar", "FC Twente",
    "FC Utrecht", "Vitesse Arnhem", "SC Heerenveen", "FC Groningen", "NEC Nijmegen",
    "Sparta Rotterdam", "PEC Zwolle", "Heracles Almelo", "Fortuna Sittard",
    "Go Ahead Eagles", "RKC Waalwijk", "Willem II", "NAC Breda",
]

_TEAMS: dict[str, list[str]] = {
    "PL": _PREMIER_LEAGUE,
    "PD": _LA_LIGA,
    "BL1": _BUNDESLIGA,
    "SA": _SERIE_A,
    "FL1": _LIGUE_1,
    "DED": _EREDIVISIE,
}


class DemoProvider:
    """Returns deterministic, realistic-looking standings for every league."""

    source = "demo"

    def get_standings(self, league_code: str) -> StandingsData:
        team_names = _TEAMS.get(league_code, [])
        return StandingsData(
            season="2025/26",
            table=_generate_table(league_code, team_names),
        )

    def get_team_form(self, league_code: str) -> dict[int, str]:
        # Demo standings already include a generated form on each row.
        return {}


def _generate_table(league_code: str, team_names: list[str]) -> list[StandingRow]:
    rng = random.Random(league_code)
    games = 2 * (len(team_names) - 1)  # full double round-robin
    rows: list[StandingRow] = []

    for name in team_names:
        # Hidden team strength drives wins, goals and final position.
        strength = rng.random()
        win_prob = 0.15 + 0.55 * strength
        draw_prob = 0.22

        won = 0
        drawn = 0
        for _ in range(games):
            roll = rng.random()
            if roll < win_prob:
                won += 1
            elif roll < win_prob + draw_prob:
                drawn += 1
        lost = games - won - drawn

        goals_for = round(games * (0.9 + 1.1 * strength))
        goals_against = round(games * (1.6 - 0.7 * strength))
        form = "".join(
            rng.choices("WDL", weights=[win_prob, draw_prob, 1 - win_prob - draw_prob], k=5)
        )

        rows.append(
            StandingRow(
                position=0,
                team=Team(name=name, short_name=name, tla=_initials(name), crest=None),
                played=games,
                won=won,
                drawn=drawn,
                lost=lost,
                goals_for=goals_for,
                goals_against=goals_against,
                goal_difference=goals_for - goals_against,
                points=won * 3 + drawn,
                form=form,
            )
        )

    rows.sort(key=lambda r: (-r.points, -r.goal_difference, -r.goals_for, r.team.name))
    for position, row in enumerate(rows, start=1):
        row.position = position
    return rows


def _initials(name: str) -> str:
    words = name.split()
    if len(words) == 1:
        return words[0][:3].upper()
    return "".join(word[0] for word in words).upper()[:3]