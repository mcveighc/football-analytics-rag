from football_rag.analytics.team import match_summary
import pandas as pd
import pytest

def test_match_summary_joins_correct_match(tmp_path):
    matches = pd.DataFrame([
        {"match_id": 1, "match_date": "2023-01-01",
         "home_team": "Team A", "away_team": "Team B"},
        {"match_id": 2, "match_date": "2023-01-02",
         "home_team": "Team C", "away_team": "Team A"},
    ])

    events = pd.DataFrame([
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.5, "team": "Team A"},
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.7, "team": "Team B"},
    ])

    matches_path = tmp_path / "matches.parquet"
    events_path = tmp_path / "events.parquet"
    matches.to_parquet(matches_path)
    events.to_parquet(events_path)

    result = match_summary(
        str(matches_path), str(events_path)
    ).set_index("team")

    assert len(result) == 2
    assert set(result.index) == {"Team A", "Team B"}
    assert (result["match_id"] == 1).all()
    assert (result["match_date"] == "2023-01-01").all()

    assert result.loc["Team A", "opponent"] == "Team B"
    assert result.loc["Team A", "home_or_away"] == "home"
    assert result.loc["Team B", "opponent"] == "Team A"
    assert result.loc["Team B", "home_or_away"] == "away"

    for team, expected_xg in [("Team A", 0.5), ("Team B", 0.7)]:
        assert result.loc[team, "shots"] == 1
        assert result.loc[team, "goals"] == 1
        assert result.loc[team, "total_xg"] == pytest.approx(expected_xg)
        
def test_match_summary_counts_own_goals_as_goals(tmp_path):
    # Given
    test_match_data = [
        {"match_id": 1, "match_date": "2023-01-01",
            "home_team": "Team A", "away_team": "Team B"}
    ]

    test_event_data = [
        # Team A
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.5, "team": "Team A"},
        {"match_id": 1, "type": "Shot", "shot_outcome": "Off T",
         "shot_statsbomb_xg": 0.2, "team": "Team A"},
        {"match_id": 1, "type": "Own Goal For", "shot_outcome": None,
         "shot_statsbomb_xg": None, "team": "Team A"},

        # Team B
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.7, "team": "Team B"},

    ]
    matches_parquet_path = tmp_path / "matches.parquet"
    pd.DataFrame(test_match_data).to_parquet(matches_parquet_path)

    match_events_parquet_path = tmp_path / "events.parquet"
    pd.DataFrame(test_event_data).to_parquet(match_events_parquet_path)

    # When
    result = match_summary(str(matches_parquet_path),
                           str(match_events_parquet_path))
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
    test_match_data = [
        {"match_id": 1, "match_date": "2023-01-01",
            "home_team": "Team A", "away_team": "Team B"}
    ]

    test_event_data = [
        # Team A
        {"match_id": 1, "type": "Pass", "shot_outcome": None,
         "shot_statsbomb_xg": None, "team": "Team A"}

    ]
    matches_parquet_path = tmp_path / "matches.parquet"
    pd.DataFrame(test_match_data).to_parquet(matches_parquet_path)

    match_events_parquet_path = tmp_path / "events.parquet"
    pd.DataFrame(test_event_data).to_parquet(match_events_parquet_path)

    # When
    result = match_summary(str(matches_parquet_path),
                           str(match_events_parquet_path))
    result = result.set_index("team")

    # Then
    assert result.loc["Team A", "shots"] == 0
    assert result.loc["Team A", "goals"] == 0
    assert result.loc["Team A", "total_xg"] == pytest.approx(0.0)


def test_match_summary_includes_expected_home_away(tmp_path):
    # Given
    test_match_data = [
        {"match_id": 1, "match_date": "2023-01-01",
            "home_team": "Team A", "away_team": "Team B"}
    ]

    test_event_data = [
        # Team A
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.5, "team": "Team A"},

        # Team B
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.7, "team": "Team B"},

    ]
    matches_parquet_path = tmp_path / "matches.parquet"
    pd.DataFrame(test_match_data).to_parquet(matches_parquet_path)

    match_events_parquet_path = tmp_path / "events.parquet"
    pd.DataFrame(test_event_data).to_parquet(match_events_parquet_path)

    # When
    result = match_summary(str(matches_parquet_path),
                           str(match_events_parquet_path))
    result = result.set_index("team")

    # Then
    assert result.loc["Team A", "home_or_away"] == "home"
    assert result.loc["Team B", "home_or_away"] == "away"


def test_match_summary_includes_expected_opponent(tmp_path):
    # Given
    test_match_data = [
        {"match_id": 1, "match_date": "2023-01-01",
         "home_team": "Team A", "away_team": "Team B"},
    ]

    test_event_data = [
        # Team A
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.5, "team": "Team A"},

        # Team B
        {"match_id": 1, "type": "Shot", "shot_outcome": "Goal",
         "shot_statsbomb_xg": 0.7, "team": "Team B"},

    ]
    matches_parquet_path = tmp_path / "matches.parquet"
    pd.DataFrame(test_match_data).to_parquet(matches_parquet_path)

    match_events_parquet_path = tmp_path / "events.parquet"
    pd.DataFrame(test_event_data).to_parquet(match_events_parquet_path)

    # When
    result = match_summary(str(matches_parquet_path),
                           str(match_events_parquet_path))
    result = result.set_index("team")

    # Then
    assert result.loc["Team A", "opponent"] == "Team B"
    assert result.loc["Team B", "opponent"] == "Team A"

