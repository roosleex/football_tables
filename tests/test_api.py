"""API smoke tests using the deterministic demo provider."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["data_source"] in {"demo", "live"}


def test_list_leagues() -> None:
    response = client.get("/api/leagues")
    assert response.status_code == 200
    leagues = response.json()
    assert len(leagues) == 6
    assert {league["code"] for league in leagues} == {
        "PL", "PD", "BL1", "SA", "FL1", "DED",
    }


def test_get_standings_demo() -> None:
    response = client.get("/api/leagues/PL/standings")
    assert response.status_code == 200
    body = response.json()
    assert body["league"]["code"] == "PL"
    assert body["source"] == "demo"
    assert len(body["table"]) == 20
    assert [row["position"] for row in body["table"]] == list(range(1, 21))
    assert body["table"][0]["points"] >= body["table"][-1]["points"]


def test_unknown_league_returns_404() -> None:
    response = client.get("/api/leagues/XX/standings")
    assert response.status_code == 404