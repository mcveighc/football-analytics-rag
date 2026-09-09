import pandas as pd


def main():
    goals = pd.read_parquet(
        "data/raw/match_3913082_events.parquet",
        columns=["type", "player", "shot_outcome", "shot_statsbomb_xg"],
    );

    shots = goals[goals["type"] == "Shot"]

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