# Football Tables

Standings for the major European football leagues — a **FastAPI** backend and a
**React (Vite + TypeScript)** frontend.

## Supported leagues

| League | Code | Country |
| --- | --- | --- |
| Premier League | `PL` | England |
| La Liga | `PD` | Spain |
| Bundesliga | `BL1` | Germany |
| Serie A | `SA` | Italy |
| Ligue 1 | `FL1` | France |
| Eredivisie | `DED` | Netherlands |

## Architecture

```
football_tables/
├── app/                       # FastAPI backend (Python package)
│   ├── api/                    #   HTTP routes
│   ├── core/                   #   settings + league catalog
│   ├── db/                     #   SQLite snapshot repository
│   ├── models/                 #   Pydantic schemas
│   ├── services/               #   data providers + refresh scheduler
│   └── main.py                 #   FastAPI app factory
├── frontend/                   # React (Vite + TypeScript) app
├── tests/                      # backend tests
├── football_tables.db          # SQLite database (auto-created, gitignored)
└── pyproject.toml              # uv project config
```

## Backend

Requirements: **Python 3.14** and **uv**.

```bash
uv sync
uv run uvicorn app.main:app --reload
```

- API: `http://localhost:8000/api`
- Interactive docs: `http://localhost:8000/docs`

### Data source & storage

Standings are stored in a **SQLite** database (`football_tables.db` in the
project root). On startup, and then **every minute**, a background task fetches
the standings for every league from the data provider and writes a fresh
snapshot to SQLite; the API always reads from SQLite.

By default the backend uses **deterministic demo data**, so it runs with no
configuration. To use live standings from [football-data.org](https://www.football-data.org),
register for a free API key and set it:

```bash
# .env
FOOTBALL_DATA_API_KEY=your_key_here
```

`GET /api/health` reports the active data source (`demo` or `live`), and each
standings response includes the `updated_at` timestamp of the last refresh.
The refresh interval is configurable via `REFRESH_INTERVAL_SECONDS` (default 60).

For live data, the per-team **form** (last 5 results) is derived from recent
finished matches and refreshed less often (via `FORM_REFRESH_INTERVAL_SECONDS`,
default 600).

All football-data.org requests go through a per-minute queue controlled by
`MAX_REQUESTS_PER_MINUTE` (default 10). When the minute's budget is exhausted,
the queue waits for the next minute before continuing.

## Frontend

Requirements: **Node.js 18+** (tested with Node 24) and **npm**.

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` requests to the backend on
port `8000`, so you need the backend running too. Standings auto-refresh every
minute, and the page shows the date and time of the last update.

For a production build:

```bash
npm run build
```

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Service status + active data source |
| `GET` | `/api/leagues` | List supported leagues |
| `GET` | `/api/leagues/{code}/standings` | Standings table for a league |

## Tests

```bash
uv run pytest
```
