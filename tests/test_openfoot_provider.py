"""Tests for the openfootapi standings parser and league definitions."""

from app.services.openfoot_provider import _league_definitions, _parse_table


def _entry(position: int, name: str, **overrides) -> dict:
    entry = {
        "position": str(position),
        "team": {"name": name},
        "total": {
            "played": 10,
            "won": 6,
            "drawn": 2,
            "lost": 2,
            "goalsFor": 20,
            "goalsAgainst": 10,
            "goalDifference": 10,
            "points": 20,
        },
        "form": ["W", "D", "L"],
    }
    entry.update(overrides)
    return entry


def test_parse_table_maps_fields_and_form() -> None:
    rows = _parse_table(
        [
            _entry(
                1,
                "Dynamo",
                team={
                    "name": "Dynamo",
                    "shortName": "DYN",
                    "code": "DYN",
                    "logoUrl": "https://cdn.test/logo.png",
                },
                form=["W", "D", "L", "W", "D"],
            )
        ]
    )
    assert len(rows) == 1
    row = rows[0]
    assert row.position == 1
    assert row.team.name == "Dynamo"
    assert row.team.short_name == "DYN"
    assert row.team.tla == "DYN"
    assert row.team.crest == "https://cdn.test/logo.png"
    assert row.played == 10
    assert row.won == 6
    assert row.points == 20
    assert row.form == "W,D,L,W,D"


def test_parse_table_missing_form_is_none() -> None:
    rows = _parse_table([_entry(1, "Team", form=[])])
    assert rows[0].form is None


def test_parse_table_missing_name_defaults_to_unknown() -> None:
    rows = _parse_table([_entry(1, "Team", team={})])
    assert rows[0].team.name == "Unknown"


def test_league_definitions_includes_europe_and_asia() -> None:
    definitions = _league_definitions()
    by_id = {entry[0]: entry for entry in definitions}
    assert by_id["comp_premier_league_ukr"] == (
        "comp_premier_league_ukr",
        "Ukrainian Premier League",
        "Ukraine",
        "UKR",
        "Europe",
    )
    assert by_id["comp_j1_league_jpn"] == (
        "comp_j1_league_jpn",
        "J1 League",
        "Japan",
        "JPN",
        "Asia",
    )
    assert all(len(entry) == 5 for entry in definitions)