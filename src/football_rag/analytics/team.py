import pandas as pd
import duckdb as db
from football_rag.validate.parquet import validate_files

def match_summary(matches_parquet_path: str, match_event_parquet_path: str) -> pd.DataFrame:
    validate_files(
        matches_parquet_path, {"match_id", "match_date", "home_team", "away_team"})
    validate_files(
        match_event_parquet_path, {"match_id", "team", "shot_outcome", "type", "shot_statsbomb_xg"})

    return db.sql(f"""
            SELECT 
                events.match_id, matches.match_date, events.team,
                CASE
                    WHEN events.team = matches.home_team THEN matches.away_team
                    WHEN events.team = matches.away_team THEN matches.home_team
                    ELSE 'unknown'
                END AS opponent,
                CASE
                    WHEN events.team = matches.home_team THEN 'home'
                    WHEN events.team = matches.away_team THEN 'away'
                    ELSE 'unknown'
                END AS home_or_away,
                COUNT_IF(type = 'Shot') as shots,
                COUNT_IF (
                    (type = 'Shot' AND shot_outcome = 'Goal')
                    OR type = 'Own Goal For') as goals,
                SUM(CASE WHEN type = 'Shot' THEN shot_statsbomb_xg ELSE 0 END) as total_xg
            FROM read_parquet('{match_event_parquet_path}') AS events
            JOIN read_parquet('{matches_parquet_path}') AS matches ON events.match_id = matches.match_id
            Group BY events.match_id, matches.match_date, events.team, matches.home_team, matches.away_team
            ORDER BY goals DESC, total_xg DESC, shots DESC
        """).df()
