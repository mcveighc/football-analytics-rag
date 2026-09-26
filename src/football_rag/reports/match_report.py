import pandas as pd

def get_match_report(match_id: int, match_data: pd.DataFrame) -> str:
    indexed_match_data = match_data.set_index(["match_id", "home_or_away"])
    home_team = indexed_match_data.loc[match_id, "home"]
    away_team = indexed_match_data.loc[match_id, "away"]
    
    return str.join("\n", [
        get_match_headline(match_id, home_team, away_team),
        "",
        get_match_score_report(home_team, away_team),
        get_match_shots_report(home_team, away_team),
        get_match_xg_report(home_team, away_team)])


def get_match_headline(match_id: int, home_team: pd.Series, away_team: pd.Series) -> str:
    match_date = home_team.get("match_date")
    home_team_name = home_team.get("team")
    away_team_name = away_team.get("team")

    title = f"# {home_team_name} vs {away_team_name}"
    date = f"Date: {match_date}"
    id = f"Match ID: {match_id}"
    
    return str.join("\n", [title, date, id])
    

def get_match_score_report(home_team: pd.Series, away_team: pd.Series) -> str:
    home_goals = home_team.get("goals")
    away_goals = away_team.get("goals")
    
    return f"- Score (from event data): {home_goals}-{away_goals}"

def get_match_shots_report(home_team: pd.Series, away_team: pd.Series) -> str:
    home_shots = home_team.get("shots")
    away_shots = away_team.get("shots")
    
    return f"- Shots: {home_shots}-{away_shots}"

def get_match_xg_report(home_team: pd.Series, away_team: pd.Series) -> str:
    home_xg = home_team.get("total_xg")
    away_xg = away_team.get("total_xg")
    
    return f"- Expected goals: {home_xg:.2f}-{away_xg:.2f}"


