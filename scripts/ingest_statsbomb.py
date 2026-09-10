from football_rag.ingest.statsbomb import load_matches, load_events
from pathlib import Path

def main():
    matches = load_matches(competition_id=37, season_id=281)
    first_match_id = matches.iloc[0]["match_id"]
    events = load_events(match_id=first_match_id)
    
    DATA_DIR = Path("data/raw")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    EVENTS_DIR = Path("data/raw/events")
    EVENTS_DIR.mkdir(parents=True, exist_ok=True)

    matches.to_parquet(DATA_DIR / "wsl_matches.parquet")
    events.to_parquet(EVENTS_DIR / f"match_{first_match_id}_events.parquet")

if __name__ == "__main__":
    main()