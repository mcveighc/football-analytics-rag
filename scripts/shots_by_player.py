from argparse import ArgumentParser
from football_rag.ingest.statsbomb import validate_columns, validate_files
import duckdb as db


def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--match-id", type=int)
    group.add_argument("-a", "--all", action="store_true")
    args = parser.parse_args()

    match_id = args.match_id
    
    event_dir = "data/raw/events"
    parquet_path = f"{event_dir}/match_{match_id}_events.parquet" if match_id is not None else f"{event_dir}/match_*_events.parquet"


    validate_files(parquet_path, {"player", "shot_outcome", "shot_statsbomb_xg", "type"})

    summary = db.sql(f"""
        SELECT 
            player, 
            COUNT(*) as shots,
            COUNT_IF (shot_outcome = 'Goal') as goals,
            SUM(shot_statsbomb_xg) as total_xg
        FROM read_parquet('{parquet_path}')
        WHERE type = 'Shot' AND player IS NOT NULL
        GROUP BY player
        ORDER BY goals DESC, total_xg DESC, shots DESC
    """)
    
    print(summary.df())


if __name__ == "__main__":
    main()
