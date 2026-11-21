"""Tests for the app factory and provider construction."""

from app.core.config import Settings
from app.main import build_providers


def test_build_providers_demo_when_no_keys() -> None:
    providers = build_providers(
        Settings(
            football_data_api_key="",
            openfoot_api_key="",
            thesportsdb_api_key="",
        )
    )
    assert [provider.source for provider in providers] == ["demo"]


def test_build_providers_live_when_football_key_set() -> None:
    providers = build_providers(
        Settings(
            football_data_api_key="key",
            openfoot_api_key="",
            thesportsdb_api_key="",
        )
    )
    assert [provider.source for provider in providers] == ["live"]


def test_build_providers_all_sources() -> None:
    providers = build_providers(
        Settings(
            football_data_api_key="a",
            openfoot_api_key="b",
            thesportsdb_api_key="c",
        )
    )
    assert [provider.source for provider in providers] == ["live", "openfoot", "thesportsdb"]