from football_rag.analytics.team import match_summary
import pandas as pd
import pytest

def test_match_summary_counts_own_goals_as_goals(tmp_path):
    # Given
    test_data = [
        # Team A
        {"type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.5, "team": "Team A"},
        {"type": "Shot", "shot_outcome": "Off T",
         "shot_statsbomb_xg": 0.2, "team": "Team A"},
        {"type": "Own Goal For", "shot_outcome": None,
         "shot_statsbomb_xg": None, "team": "Team A"},
        
        # Team B
        {"type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.7, "team": "Team B"},

    ]
    parquet_path = tmp_path / "events.parquet"
    pd.DataFrame(test_data).to_parquet(parquet_path)

    # When
    result = match_summary(str(parquet_path))
    result = result.set_index("team")
    
    # Then
    assert result.loc["Team A", "shots"] == 2
    assert result.loc["Team A", "goals"] == 2
    assert result.loc["Team A", "total_xg"] == pytest.approx(0.7)
    assert result.loc["Team B", "shots"] == 1
    assert result.loc["Team B", "goals"] == 1
    assert result.loc["Team B", "total_xg"] == pytest.approx(0.7)
    
def test_match_summary_includes_zero_shots(tmp_path):
    # Given
    test_data = [
        # Team A
        {"type": "Pass", "shot_outcome": None,
         "shot_statsbomb_xg": None, "team": "Team A"}

    ]
    parquet_path = tmp_path / "events.parquet"
    pd.DataFrame(test_data).to_parquet(parquet_path)

    # When
    result = match_summary(str(parquet_path))
    result = result.set_index("team")
    
    # Then
    assert result.loc["Team A", "shots"] == 0
    assert result.loc["Team A", "goals"] == 0
    assert result.loc["Team A", "total_xg"] == pytest.approx(0.0)