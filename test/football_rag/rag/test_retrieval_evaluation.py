from pathlib import Path
from typing import Optional

from football_rag.search.search import search_documents
from test.football_rag import EXPECTED_GOALS_MD, GOALS_MD, MATCH_REPORT_MD, UNRELATED_MD

import pytest

@pytest.mark.parametrize("retrieval_ids, relevant_ids, k, expected_precision, expected_recall", [
    (["a", "b"], {"a", "b"}, 2, 1.0, 1.0),
    (["a", "c", "b"], {"a", "b"}, 2, 0.5, 0.5),
    (["c", "d"], {"a", "b"}, 2, 0, 0),
    (["a"], {"a", "b"}, 2, 0.5, 0.5),
    (["a", "c"], {"a", "b", "d"}, 2, 0.5, 1/3),
    (["a", "b"], set(), 2, 0.0, None)
])
def test_retrieval_metrics(retrieval_ids, relevant_ids, k, expected_precision, expected_recall):
    precision = precision_at_k(retrieval_ids, relevant_ids, k)
    recall = recall_at_k(retrieval_ids, relevant_ids, k)
    
    assert precision == expected_precision
    
    if expected_recall is None:
        assert recall is None
    else:   
        assert recall == pytest.approx(expected_recall)

@pytest.mark.parametrize("question, relevant_filenames, k, expected_precision, expected_recall", 
    [
        ("Do own goals contribute to a team’s xG?", {"expected_goals.md", "goals.md"}, 2, 1.0, 1.0),
        ("What were the expected goals in match 3913082?", {"match_report.md"}, 2, 1/2, 1.0),
        ("Do own goals increase expected goals?", {"expected_goals.md", "goals.md"}, 2, 1.0, 1.0),
        ("How many spectators attended match 3913082?", set(), 2, 0.0, None)
    ],
    ids=[
        "own_goals_xg",
        "match_xg",
        "own_goals_paraphrase",
        "missing_attendance_evidence",
    ])
def test_retrieval_quality(tmp_path, question, relevant_filenames, k, expected_precision, expected_recall):
    # assemble
    assemble_corpus(tmp_path)
    
    # act
    results = search_documents(question, sources=[tmp_path], limit=k)
    
    # Assert
    retrieved_paths = [ Path(result["source_path"]) for result in results ]
    relevant_documents = { tmp_path / filename for filename in relevant_filenames }
    
    precision = precision_at_k(retrieved_paths, relevant_documents, k)
    recall = recall_at_k(retrieved_paths, relevant_documents, k)
    
    
    assert precision == expected_precision
    
    if expected_recall is None:
        assert recall is None
    else:
        assert recall == pytest.approx(expected_recall)
    

def precision_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> float:
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = set(retrieved_k).intersection(relevant_ids)
    return len(relevant_retrieved) / k

def recall_at_k(retrieved_ids: list, relevant_ids: set, k: int) -> Optional[float]:
    if len(relevant_ids) == 0:
        return None
    
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = set(retrieved_k).intersection(relevant_ids)
    return len(relevant_retrieved) / len(relevant_ids)


def assemble_corpus(tmp_path):
    md_files = {
        "expected_goals.md": EXPECTED_GOALS_MD,
        "goals.md": GOALS_MD,
        "match_report.md": MATCH_REPORT_MD,
        "unrelated.md": UNRELATED_MD
    }
    
    for filename, content in md_files.items():
        md_file = tmp_path / filename
        md_file.write_text(content, encoding="utf-8")
    
    
    
    
