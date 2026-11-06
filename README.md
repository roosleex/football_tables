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
│   ├── db/                     #   in-memory TTL cache
│   ├── models/                 #   Pydantic schemas
│   ├── services/               #   data providers + service layer
│   └── main.py                 #   FastAPI app factory
├── frontend/                   # React (Vite + TypeScript) app
├── tests/                      # backend tests
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

### Data source

By default the backend serves **deterministic demo data**, so it runs with no
configuration. To use live standings from [football-data.org](https://www.football-data.org),
register for a free API key and set it:

```bash
# .env
FOOTBALL_DATA_API_KEY=your_key_here
```

`GET /api/health` reports the active data source (`demo` or `live`). Live
results are cached in memory for a short time to stay within rate limits.

## Frontend

Requirements: **Node.js 18+** (tested with Node 24) and **npm**.

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Vite proxies `/api` requests to the backend on
port `8000`, so you need the backend running too.

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
