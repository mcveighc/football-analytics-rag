# Football Analytics RAG

A hands-on learning project combining football event-data analytics, retrieval augmented generation (RAG), and agentic workflows in one Python repository.

The project currently turns StatsBomb open data into queryable Parquet files, reusable DuckDB analytics, and factual Markdown match reports, with local keyword search over reports and knowledge notes. The next milestone is a minimal RAG flow that generates answers with source references; embeddings, LLM answers, and agent routing are not implemented yet.

## Current Status

- Ingestion of WSL match metadata and event data, with an optional match limit.
- Local Parquet storage and per-file required-column validation.
- A player leaderboard with shots, goals, and total xG, for one match or all locally stored matches.
- Team summaries with match ID, date, opponent, home/away status, shots, goals, and xG.
- Metadata joins and multi-file queries that keep each match's team totals separate.
- Markdown reports for individual matches, with home-first ordering, match identification, an event-derived score, and xG formatted to two decimal places.
- Synthetic-data tests covering team analytics, own goals, zero-shot teams, metadata joins, multiple matches, and report formatting.
- Knowledge notes explaining xG, goals, and how to interpret match summaries.
- Keyword retrieval that ranks Markdown documents by distinct shared words and returns full text, source path, and score.
- A search CLI with a configurable result limit and document previews.
- Retrieval tests covering whole-word matching, repeated words, partial query matches, multiple sources, score ordering, result limits, and no matches.

## Architecture

```text
StatsBomb open data
  -> ingestion
  -> local Parquet files
  -> DuckDB analytics
  -> pandas DataFrames
  -> Markdown match reports

Knowledge notes + generated reports
  -> local keyword retrieval
  -> labelled document context (planned)
  -> LLM answers with source references (next milestone)
```

Structured event data belongs in the analytics layer. Exact calculations, rankings, and cross-match comparisons use SQL. Text retrieval supplies metric explanations and match context. The planned LLM flow will explain retrieved material and quote reported values; new numeric calculations remain in the analytics layer.

CLI scripts connect the steps. Analytics functions return DataFrames, report functions turn supplied summaries into text, and scripts handle arguments, printing, and file output.

## Project Structure

```text
football-analytics-rag/
  data/                              # Local artifacts; ignored by git
    raw/
      wsl_matches.parquet
      events/
        match_<match_id>_events.parquet
    reports/
      match_<match_id>.md
  docs/knowledge/
    expected-goals.md
    goals.md
    match-summaries.md
  scripts/
    ingest_statsbomb.py
    shots_by_player.py
    match_summary_by_team.py
    match_report.py
    search.py
  src/football_rag/
    ingest/statsbomb.py
    analytics/shots.py
    analytics/team.py
    validate/parquet.py
    reports/match_report.py
    search/search.py
  test/football_rag/
    analytics/test_team.py
    reports/test_match_report.py
    search/test_search.py
  pyproject.toml
  README.md
```

## Setup

From the repository root, create and activate a virtual environment and install the project:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
```

Dependencies currently include `statsbombpy`, `pandas`, `pyarrow`, `duckdb`, and `pytest`.

## Usage

Run these commands from the repository root; scripts use relative data paths.

### Ingest data

Start with three matches:

```sh
python scripts/ingest_statsbomb.py --limit 3
```

The script saves match metadata and fetches events for the first three returned matches. It currently uses competition ID `37` and season ID `281`. Omitting `--limit` fetches events for all returned matches and makes more network requests.

The following examples use match ID `3913082`. Use an ID with an event file already present in `data/raw/events/`.

### Player leaderboard

```sh
python scripts/shots_by_player.py --match-id 3913082
python scripts/shots_by_player.py --all
```

The `--all` option aggregates each player's totals across all matching local event files.

### Team match summaries

```sh
python scripts/match_summary_by_team.py --match-id 3913082
python scripts/match_summary_by_team.py
```

Omitting the match ID reads all matching local event files and returns separate rows for each match and team.

### Generate a match report

```sh
python scripts/match_report.py --match-id 3913082
```

This writes `data/reports/match_3913082.md`. Running it again for the same match replaces that report.

Example output:

```markdown
# Brighton & Hove Albion WFC vs Manchester United W
Date: 2023-11-05
Match ID: 3913082

- Score (from event data): 2-2
- Shots: 11-22
- Expected goals: 1.23-3.04
```

Raw extracts and generated reports live under the git-ignored `data/` directory. Knowledge notes are versioned under `docs/knowledge/`.

### Search documents

```sh
python scripts/search.py --query "expected goals"
python scripts/search.py --query "Manchester United" --limit 5
```

Search reads Markdown files directly within `data/reports/` and `docs/knowledge/`. The default result limit is three. Each result prints its source path, score, and a preview of up to 200 characters, with an ellipsis when truncated. Queries with no matching documents produce no output.

## Tests

Run the full suite from the repository root:

```sh
python -m pytest
```

Use `python -m pytest -v` to see individual test names. Tests use synthetic data, temporary Parquet files, and temporary Markdown documents rather than downloading StatsBomb data.

## Metric Definitions and Current Assumptions

- Team shots count events whose `type` is `Shot`.
- Team goals count successful shots plus `Own Goal For` events. The player leaderboard counts goals from shots only.
- Team xG sums `shot_statsbomb_xg` for shot events. Analytics retain precision; reports format xG to two decimal places.
- A team with non-shot events can appear with zero shots. A team with no event rows is not automatically created from metadata.
- Metadata must have one row per match ID. Duplicate rows can inflate aggregates; events without matching metadata are excluded by the inner join.
- Validation checks required columns in each input file, not completeness of values or uniqueness of metadata rows.
- The current query has no separate penalty-shootout policy.

Read the project notes for more detail:

- [Expected goals](docs/knowledge/expected-goals.md)
- [Goals and own goals](docs/knowledge/goals.md)
- [Understanding match summaries](docs/knowledge/match-summaries.md)

## Local Document Retrieval

The keyword search treats each Markdown document as one searchable unit. It lowercases the query and document text, extracts whole-word tokens, and scores each document by the number of distinct words shared with the query. Repeated words do not increase the score; `goal` does not match `goalkeeper`.

`search_documents()` excludes zero-score documents, sorts by descending score, and applies the result limit. Each result contains:

- `text`: full document content.
- `source_path`: the document's `Path`.
- `score`: the number of distinct shared words, not a confidence estimate.

**Known limitation:** equally scored documents retain their discovery order. With the default source order, reports are searched before knowledge notes, so tied reports can push explanatory notes below the result limit. There is no semantic matching, chunking, or preference for explanatory content yet.

## Next Milestone: Minimal RAG Flow

Build the flow in small steps using the existing retrieval results:

1. Format retrieved documents into context labelled `[1]`, `[2]`, and so on, preserving their order, full text, and source paths. Keep retrieval scores out of the context. Start with a pure `format_context(results: list[dict]) -> str` function in `src/football_rag/rag/context.py`, returning an empty string for no results.
2. Pass the question and labelled context to an LLM with instructions to answer from the supplied evidence, cite document labels, and acknowledge missing evidence.
3. Connect retrieval and generation through a small CLI that returns the answer and maps source labels to document paths. Handle empty retrieval without calling the LLM.
4. Check supported answers, insufficient evidence, and whether citations refer to documents that support the claims.

This flow is planned, not implemented. Exact calculations, rankings, and cross-match comparisons stay in DuckDB. An LLM cannot compensate for relevant evidence omitted by retrieval, so the known ranking limitation remains part of evaluation.

## Longer-Term Direction

- Evaluate retrieval quality and add embeddings where useful.
- Expose analytics and retrieval as tools for an agent.
- Let the agent choose analytics, retrieval, or both, combining numeric results with explanations.
- Add evaluation questions with known answers to check accuracy.

## Data Source

Data is ingested from StatsBomb open data through `statsbombpy`, starting with women's football data. See the upstream repository for data documentation and usage requirements:

- [StatsBomb Open Data](https://github.com/statsbomb/open-data)
- [statsbombpy](https://github.com/statsbomb/statsbombpy)
