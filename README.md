# Football Analytics RAG

An exemplar learning project for combining football event-data analytics, retrieval augmented generation (RAG), and agentic workflows.

The project starts with a small, practical analytics pipeline over open StatsBomb football data. The longer-term goal is to build an agent that can answer football analysis questions by combining precise structured-data queries with retrieved documentation, notes, and generated scouting context.

## Goals

- Ingest open StatsBomb match and event data.
- Store raw event data locally in analysis-friendly formats such as Parquet.
- Build reusable football analytics queries with pandas, and later DuckDB.
- Add a RAG layer for schema notes, metric explanations, tactical concepts, and generated reports.
- Wrap analytics and retrieval capabilities as tools in a simple agentic workflow.

## Current Status

Implemented so far:

- Basic StatsBomb ingestion helpers in `src/football_rag/ingest/`.
- A script to fetch WSL match data and one match's event data.
- Local Parquet output under `data/raw/`.
- A first pandas aggregation script for shots, goals, and xG by player.

## Project Structure

```text
football-analytics-rag/
  data/
    raw/                         # Local StatsBomb data extracts
  scripts/
    ingest_statsbomb.py           # Fetch and save initial StatsBomb data
    shots_by_player.py            # Example pandas analytics query
  src/
    football_rag/
      ingest/
        statsbomb.py              # Reusable StatsBomb loading functions
  pyproject.toml
  README.md
```

## Setup

Create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

```sh
python -m pip install --upgrade pip setuptools wheel
pip install -e .
```

## Usage

Fetch initial WSL match and event data:

```sh
python scripts/ingest_statsbomb.py
```

Run the first analytics query:

```sh
python scripts/shots_by_player.py
```

The current query reads a saved match event file and produces a player-level summary with:

- shot count
- goals
- total StatsBomb xG

## Data Source

This project uses StatsBomb open data via `statsbombpy`.

The initial example uses the WSL competition and season IDs referenced in Hudl/StatsBomb's free women's data release.

## Why Analytics And RAG?

Raw event data is structured data, so it belongs in a queryable analytics layer rather than a vector database. Questions like "who had the most xG?" or "which players took the most shots?" should be answered with pandas, SQL, or DuckDB.

RAG is better suited to textual context, such as:

- event schema explanations
- metric definitions
- tactical analysis notes
- generated match summaries
- generated scouting reports

The intended final shape is a hybrid system:

```text
User question
  -> agent decides what is needed
  -> analytics tool queries structured event data
  -> retrieval tool fetches explanatory context
  -> LLM combines numbers, evidence, and interpretation
```

## Roadmap

Near-term:

- Parameterize scripts by `match_id`.
- Ingest all matches for one competition.
- Store event files in a consistent `data/raw/events/` layout.
- Add more analytics queries, such as shot maps, xG by team, and player involvement.
- Add basic tests around reusable ingestion and analytics functions.

RAG layer:

- Collect notes on StatsBomb event fields and football metrics.
- Chunk and index text documentation.
- Add a vector store for retrieval.
- Return cited context in answers.

Agentic layer:

- Expose analytics queries as callable tools.
- Expose RAG retrieval as a callable tool.
- Build a simple workflow that chooses between data queries, retrieval, and final answer generation.
- Add evaluation examples with known questions and expected outputs.
