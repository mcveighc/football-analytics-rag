from statsbombpy import sb

def load_matches(competition_id: int, season_id: int):
    return sb.matches(competition_id=competition_id, season_id=season_id)

def load_events(match_id: int):
    return sb.events(match_id=match_id)