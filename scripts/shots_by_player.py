from argparse import ArgumentParser
from email import parser
from tokenize import group
import pandas as pd


def main():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-m", "--match-id", type=int)
    group.add_argument("-a", "--all", action="store_true")
    args = parser.parse_args()

  
    match_id = args.match_id
    if match_id is not None: 
        # Get events for match id if its specified
        events = pd.read_parquet(
            f"data/raw/events/match_{match_id}_events.parquet",
            columns=["type", "player", "shot_outcome", "shot_statsbomb_xg"]) 
    elif args.all:
        # Get events for match id if it is specified.
        events = pd.read_parquet(
            "data/raw/events",
            columns=["type", "player", "shot_outcome", "shot_statsbomb_xg"],)

    shots = events[events["type"] == "Shot"]

    summary = (
        shots.groupby("player", dropna=True)
        .agg(
            shots=("type", "count"),
            goals=("shot_outcome", lambda x: (x == "Goal").sum()),
            total_xg=("shot_statsbomb_xg", "sum"),
        )
        .reset_index()
        .sort_values(["goals", "total_xg", "shots"], ascending=False)
    )

    print(summary)

if __name__ == "__main__":
    main()