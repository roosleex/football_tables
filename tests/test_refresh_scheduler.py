"""Tests for the background refresh scheduler."""

from app.core.leagues import LeagueCatalog
from app.db.sqlite import StandingsRepository
from app.models.league import League
from app.models.standings import StandingsData, StandingRow, Team
from app.services.base import ProviderError
from app.services.refresh_scheduler import RefreshScheduler


class _FakeProvider:
    def __init__(
        self,
        source: str,
        leagues: list[League] | None = None,
        standings: dict[str, StandingsData] | None = None,
        form: dict[str, dict[int, str]] | None = None,
        *,
        league_error: bool = False,
        standings_error: bool = False,
    ) -> None:
        self.source = source
        self._leagues = leagues or []
        self._standings = standings or {}
        self._form = form or {}
        self.league_error = league_error
        self.standings_error = standings_error

    def get_leagues(self) -> list[League]:
        if self.league_error:
            raise ProviderError("league list failed")
        return list(self._leagues)

    def get_standings(self, league_code: str) -> StandingsData:
        if self.standings_error:
            raise ProviderError("standings failed")
        return self._standings[league_code]

    def get_team_form(self, league_code: str) -> dict[int, str]:
        return self._form.get(league_code, {})


def _row(position: int, team_id: int) -> StandingRow:
    return StandingRow(
        position=position,
        team=Team(id=team_id, name="Team"),
        played=1,
        won=1,
        drawn=0,
        lost=0,
        goals_for=1,
        goals_against=0,
        goal_difference=1,
        points=3,
    )


def _league(code: str, standings_available: bool = True) -> League:
    return League(
        code=code,
        name=code,
        country="Country",
        country_code=code,
        region="Europe",
        standings_available=standings_available,
    )


def _repo(tmp_path) -> StandingsRepository:
    repo = StandingsRepository(tmp_path / "test.db")
    repo.init_schema()
    return repo


def test_refresh_leagues_merges_and_skips_errors(tmp_path) -> None:
    ok = _FakeProvider("demo", leagues=[_league("PL")])
    failing = _FakeProvider("openfoot", leagues=[_league("XX")], league_error=True)

    scheduler = RefreshScheduler([ok, failing], _repo(tmp_path), LeagueCatalog())
    scheduler.refresh_leagues()

    assert [league.code for league in scheduler._catalog.all()] == ["PL"]
    assert scheduler._provider_by_code["PL"] is ok


def test_refresh_standings_saves_and_skips_unavailable(tmp_path) -> None:
    repo = _repo(tmp_path)
    leagues = [_league("PL"), _league("XX", standings_available=False)]
    provider = _FakeProvider(
        "demo",
        leagues=leagues,
        standings={"PL": StandingsData(season="2025/26", table=[_row(1, 1)])},
    )

    scheduler = RefreshScheduler([provider], repo, LeagueCatalog())
    scheduler.refresh_leagues()
    scheduler.refresh_standings()

    assert repo.get_standings("PL") is not None
    assert repo.get_standings("XX") is None


def test_refresh_standings_skips_provider_errors(tmp_path) -> None:
    repo = _repo(tmp_path)
    provider = _FakeProvider("demo", leagues=[_league("PL")], standings_error=True)

    scheduler = RefreshScheduler([provider], repo, LeagueCatalog())
    scheduler.refresh_leagues()
    scheduler.refresh_standings()

    assert repo.get_standings("PL") is None


def test_refresh_form_only_applies_to_live_source(tmp_path) -> None:
    repo = _repo(tmp_path)
    live = _FakeProvider("live", leagues=[_league("PL")], form={"PL": {1: "W,W"}})
    repo.save_standings("PL", None, "live", [_row(1, 1)])

    scheduler = RefreshScheduler([live], repo, LeagueCatalog())
    scheduler.refresh_leagues()
    scheduler.refresh_form()

    stored = repo.get_standings("PL")
    assert stored is not None
    assert stored.rows[0].form == "W,W"


def test_refresh_form_skips_non_live_source(tmp_path) -> None:
    repo = _repo(tmp_path)
    demo = _FakeProvider("demo", leagues=[_league("PL")], form={"PL": {1: "W,W"}})
    repo.save_standings("PL", None, "demo", [_row(1, 1)])

    scheduler = RefreshScheduler([demo], repo, LeagueCatalog())
    scheduler.refresh_leagues()
    scheduler.refresh_form()

    stored = repo.get_standings("PL")
    assert stored is not None
    assert stored.rows[0].form is None