"""Ensure tests run against demo data and an isolated SQLite database."""

import os
import tempfile
from pathlib import Path

# Force demo data regardless of a local .env, and use a temp database so tests
# never touch the real football_tables.db in the project root.
os.environ["FOOTBALL_DATA_API_KEY"] = ""
os.environ["OPENFOOT_API_KEY"] = ""
os.environ["APIFOOTBALL_API_KEY"] = ""
os.environ["DATABASE_PATH"] = str(Path(tempfile.gettempdir()) / "football_tables_test.db")