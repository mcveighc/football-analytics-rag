from pathlib import Path
from football_rag.reports.match_report import get_match_report

from argparse import ArgumentParser
from football_rag.analytics.team import match_summary


def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--match-id", type=int, required=True)
    args = parser.parse_args()

    match_id = args.match_id
    
    matches_parquet_path = "data/raw/wsl_matches.parquet"
    match_event_parquet_path = f"data/raw/events/match_{match_id}_events.parquet"
    summary = match_summary(matches_parquet_path, match_event_parquet_path)
    
    output_dir = Path("data/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"match_{match_id}.md"
    
    report = get_match_report(match_id, summary)
    output_path.write_text(report + "\n", encoding="utf-8")
    
    print(f"Report saved to {output_path}")

if __name__ == "__main__":
    main()
