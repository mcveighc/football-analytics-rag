from argparse import ArgumentParser
from football_rag.analytics.team import match_summary as team_match_summary

def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--match-id", type=int, required=False)
    args = parser.parse_args()

    match_id = args.match_id
    matches_parquet_path = "data/raw/wsl_matches.parquet"
    
    event_dir = "data/raw/events"
    match_event_parquet_path = f"{event_dir}/match_{match_id}_events.parquet" if match_id is not None else f"{event_dir}/match_*_events.parquet"    
    summary = team_match_summary(matches_parquet_path, match_event_parquet_path)
    
    print(summary)

if __name__ == "__main__":
    main()
