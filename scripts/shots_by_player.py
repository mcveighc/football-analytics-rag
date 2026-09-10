from argparse import ArgumentParser
import pandas as pd


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--match-id", type=int, default=3913082)
    args = parser.parse_args()

    events = pd.read_parquet(
        f"data/raw/events/match_{args.match_id}_events.parquet",
        columns=["type", "player", "shot_outcome", "shot_statsbomb_xg"],
    )

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