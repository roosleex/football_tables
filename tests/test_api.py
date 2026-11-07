"""API smoke tests using the deterministic demo provider and SQLite storage."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["data_source"] == "demo"


def test_list_leagues(client) -> None:
    response = client.get("/api/leagues")
    assert response.status_code == 200
    leagues = response.json()
    assert len(leagues) == 6
    assert {league["code"] for league in leagues} == {
        "PL", "PD", "BL1", "SA", "FL1", "DED",
    }


def test_list_leagues_ordered_by_uefa_coefficient(client) -> None:
    response = client.get("/api/leagues")
    assert response.status_code == 200
    assert [league["code"] for league in response.json()] == [
        "PL", "SA", "PD", "BL1", "FL1", "DED",
    ]


def test_get_standings_demo(client) -> None:
    response = client.get("/api/leagues/PL/standings")
    assert response.status_code == 200
    body = response.json()
    assert body["league"]["code"] == "PL"
    assert body["source"] == "demo"
    assert len(body["table"]) == 20
    assert [row["position"] for row in body["table"]] == list(range(1, 21))
    assert body["table"][0]["points"] >= body["table"][-1]["points"]
    assert body["updated_at"] is not None


def test_unknown_league_returns_404(client) -> None:
    response = client.get("/api/leagues/XX/standings")
    assert response.status_code == 404