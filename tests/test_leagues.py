"""Tests for the league catalog and UEFA coefficient ordering."""

from app.core.leagues import LeagueCatalog, sort_leagues_by_uefa_coefficient
from app.models.league import League


def _league(code: str, country_code: str) -> League:
    return League(code=code, name=code, country="Country", country_code=country_code)


def test_sort_by_uefa_coefficient_orders_known_codes() -> None:
    leagues = [
        _league("FL1", "FR"),
        _league("PL", "ENG"),
        _league("SA", "IT"),
    ]
    result = sort_leagues_by_uefa_coefficient(leagues)
    assert [league.code for league in result] == ["PL", "SA", "FL1"]


def test_sort_puts_unknown_country_last_alphabetically() -> None:
    leagues = [
        _league("Zed", "ZZZ"),
        _league("PL", "ENG"),
        _league("Alpha", "AAA"),
    ]
    result = sort_leagues_by_uefa_coefficient(leagues)
    assert result[0].code == "PL"
    assert [league.code for league in result[1:]] == ["Alpha", "Zed"]


def test_catalog_replace_all_and_get_case_insensitive() -> None:
    catalog = LeagueCatalog([_league("PL", "ENG")])
    assert [league.code for league in catalog.all()] == ["PL"]
    assert catalog.get("pl") is not None
    assert catalog.get("pl").code == "PL"
    assert catalog.get("XX") is None


def test_catalog_all_returns_copy() -> None:
    catalog = LeagueCatalog([_league("PL", "ENG")])
    leagues = catalog.all()
    leagues.clear()
    assert len(catalog.all()) == 1