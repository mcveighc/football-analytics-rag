from football_rag.reports.match_report import get_match_report
import pandas as pd

def test_match_report_displays_expected_report():
    # assemble
    match_id = 1
    match_date = "2023-11-05"
    home_team_name = "Manchester United W"
    away_team_name = "Brighton & Hove Albion WFC"

    home_goals = 2
    away_goals = 1

    home_shots = 10
    away_shots = 5

    home_xg = 1.6512
    away_xg = 1.9212

    match_summary_data = pd.DataFrame([
        {"match_id": match_id, "match_date": f"{match_date}", "team": f"{away_team_name}",
            "home_or_away": "away", "goals": away_goals, "shots": away_shots, "total_xg": away_xg},
        {"match_id": match_id, "match_date": f"{match_date}", "team": f"{home_team_name}",
            "home_or_away": "home", "goals": home_goals, "shots": home_shots, "total_xg": home_xg}
    ])

    # act
    output = get_match_report(1, match_summary_data).splitlines()

    # assert
    assert output[0] == f"# {home_team_name} vs {away_team_name}"
    assert output[1] == f"Date: {match_date}"
    assert output[2] == f"Match ID: {match_id}"
    assert output[3] == ""
    assert output[4] == f"- Score (from event data): {home_goals:.0f}-{away_goals:.0f}"
    assert output[5] == f"- Shots: {home_shots:.0f}-{away_shots:.0f}"
    assert output[6] == f"- Expected goals: 1.65-1.92"
