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
    # openfootapi returns form most-recent-first; it is reversed to
    # oldest-first so the rightmost badge is the latest result.
    assert row.form == "D,W,L,D,W"


def test_parse_table_form_is_oldest_first() -> None:
    rows = _parse_table([_entry(1, "Team", form=["W", "L", "D", "W", "L"])])
    assert rows[0].form == "L,W,D,L,W"


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


def test_league_definitions_includes_north_america() -> None:
    definitions = _league_definitions()
    by_id = {entry[0]: entry for entry in definitions}
    assert by_id["comp_mls_usa"] == (
        "comp_mls_usa",
        "Major League Soccer",
        "United States",
        "USA",
        "North America",
    )
    assert by_id["comp_liga_mx_mex"][-1] == "North America"
    assert by_id["comp_canadian_premier_league_can"][-1] == "North America"
    assert by_id["comp_primera_division_crc"][-1] == "North America"


def test_league_definitions_includes_south_america() -> None:
    definitions = _league_definitions()
    by_id = {entry[0]: entry for entry in definitions}
    assert by_id["comp_brasileirao_bra"] == (
        "comp_brasileirao_bra",
        "Brasileirão Série A",
        "Brazil",
        "BRA",
        "South America",
    )
    south_american_ids = (
        "comp_liga_profesional_arg",
        "comp_primera_division_bol",
        "comp_primera_division_chi",
        "comp_primera_a_col",
        "comp_ligapro_ecu",
        "comp_primera_division_par",
        "comp_liga_1_per",
        "comp_primera_division_uru",
        "comp_primera_division_ven",
    )
    assert all(by_id[code][-1] == "South America" for code in south_american_ids)


def test_league_definitions_includes_africa() -> None:
    definitions = _league_definitions()
    by_id = {entry[0]: entry for entry in definitions}
    assert by_id["comp_npfl_nga"] == (
        "comp_npfl_nga",
        "Nigerian Professional Football League",
        "Nigeria",
        "NGA",
        "Africa",
    )
    african_ids = (
        "comp_ligue_1_dza",
        "comp_egyptian_prem_egy",
        "comp_botola_pro_mar",
        "comp_psl_rsa",
        "comp_ligue_1_tun",
    )
    assert all(by_id[code][-1] == "Africa" for code in african_ids)