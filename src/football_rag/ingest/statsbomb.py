from statsbombpy import sb
from glob import glob

import duckdb as db


def load_matches(competition_id: int, season_id: int):
    return sb.matches(competition_id=competition_id, season_id=season_id)

def load_events(match_id: int):
    return sb.events(match_id=match_id)

def validate_files(parquet_path: str, required: set[str]) -> None:
    files = sorted(glob(parquet_path))

    if not files:
        raise FileNotFoundError(f"No files matched: {parquet_path}")

    for file_path in files:
        try:
            validate_columns(file_path, required)
        except ValueError as exc:
            raise ValueError(f"{file_path}: {exc}") from exc

def validate_columns(parquet_path: str, required: set[str]) -> None:
    columns = {
        row[0]
        for row in db.sql(
            f"SELECT name FROM parquet_schema('{parquet_path}')"
        ).fetchall()
    }

    missing = required - columns

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )