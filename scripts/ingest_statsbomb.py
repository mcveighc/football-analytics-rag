from argparse import ArgumentParser
from football_rag.ingest.statsbomb import load_matches, load_events
from pathlib import Path

def main():
    parser = ArgumentParser()
    parser.add_argument("-l", "--limit", type=int)
    args = parser.parse_args()

    # Ingest matches for competition and season
    data_dir = ensure_data_dir("data/raw")
    matches = load_matches(competition_id=37, season_id=281)
    matches.to_parquet(data_dir / "wsl_matches.parquet")

    # Ingest events for each match
    events_dir = ensure_data_dir("data/raw/events")
    for match_id in matches["match_id"][:args.limit or len(matches)]:
        print(f"Fetching events for match {match_id}")
        match_events = load_events(match_id=match_id)
        match_events.to_parquet(events_dir / f"match_{match_id}_events.parquet")


def ensure_data_dir(path: str):
    data_dir = Path(path)
    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir

if __name__ == "__main__":
    main()