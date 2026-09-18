from argparse import ArgumentParser
from football_rag.analytics.shots import shots_by_player


def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--match-id", type=int)
    group.add_argument("-a", "--all", action="store_true")
    args = parser.parse_args()

    match_id = args.match_id
    
    event_dir = "data/raw/events"
    parquet_path = f"{event_dir}/match_{match_id}_events.parquet" if match_id is not None else f"{event_dir}/match_*_events.parquet"
    
    summary = shots_by_player(parquet_path)
    print(summary)

if __name__ == "__main__":
    main()
