import pandas as pd
import duckdb as db
from football_rag.validate.parquet import validate_files

def match_summary(parquet_path: str) -> pd.DataFrame:
    validate_files(
        parquet_path, {"team", "shot_outcome", "type", "shot_statsbomb_xg"})

    return db.sql(f"""
            SELECT 
                team, 
                COUNT_IF(type = 'Shot') as shots,
                COUNT_IF (
                    (type = 'Shot' AND shot_outcome = 'Goal')
                    OR type = 'Own Goal For') as goals,
                SUM(CASE WHEN type = 'Shot' THEN shot_statsbomb_xg ELSE 0 END) as total_xg
            FROM read_parquet('{parquet_path}')
            GROUP BY team
            ORDER BY goals DESC, total_xg DESC, shots DESC
        """).df()
