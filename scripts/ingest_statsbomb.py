from argparse import ArgumentParser
from football_rag.ingest.statsbomb import load_matches, load_events
from pathlib import Path

def main():
    parser = ArgumentParser()
    parser.add_argument("-l", "--limit", type=int, default=1)
    args = parser.parse_args()

    # Ingest matches for competition and season
    DATA_DIR = create_data_dir("data/raw")
    matches = load_matches(competition_id=37, season_id=281);
    matches.to_parquet(DATA_DIR / "wsl_matches.parquet")

    # Ingest events for each match
    EVENTS_DIR = create_data_dir("data/raw/events")
    for match_id in matches["match_id"][:args.limit]:
        match_events = load_events(match_id=match_id)
        match_events.to_parquet(EVENTS_DIR / f"{match_id}.parquet")


def create_data_dir(path: str):
    DATA_DIR = Path(path)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    return DATA_DIR

if __name__ == "__main__":
    main()