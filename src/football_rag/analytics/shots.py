import pandas as pd
import duckdb as db
from football_rag.validate.parquet import validate_files

def shots_by_player(parquet_path: str) -> pd.DataFrame:
    validate_files(
        parquet_path, {"player", "shot_outcome", "shot_statsbomb_xg", "type"})

    return db.sql(f"""
            SELECT 
                player, 
                COUNT(*) as shots,
                COUNT_IF (shot_outcome = 'Goal') as goals,
                SUM(shot_statsbomb_xg) as total_xg
            FROM read_parquet('{parquet_path}')
            WHERE type = 'Shot' AND player IS NOT NULL
            GROUP BY player
            ORDER BY goals DESC, total_xg DESC, shots DESC
        """).df()
