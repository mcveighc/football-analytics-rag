from argparse import ArgumentParser
from football_rag.analytics.team import match_summary as team_match_summary


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--match-id", type=int, required=True)
    args = parser.parse_args()

    match_id = args.match_id
    parquet_path = f"data/raw/events/match_{match_id}_events.parquet"    
    summary = team_match_summary(parquet_path)
    
    print(summary)

if __name__ == "__main__":
    main()
