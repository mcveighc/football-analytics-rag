from pathlib import Path
import re
from typing import Sequence, Union

def search_documents(
    query: str, 
    sources: Sequence[Union[str, Path]] = ("data/reports", "docs/knowledge"),
    limit: int = 3) -> list[dict]:
    
    search_results: list[dict] = []
    
    # Normalise a split the search term once
    tokenized_query = tokenize(query)
  
    # Loop over sources and search each .md file for matching words
    for source_path in sources:
        directory = Path(source_path)
        for file_path in directory.glob("*.md"):
            searched_file = search_source_file(file_path, tokenized_query)
            if searched_file != {}:
                search_results.append(searched_file)
                
    # Sort the search results by score - highest to lowest
    search_results.sort(key=lambda sr: sr["score"], reverse=True)
    
    return search_results[:limit]


def search_source_file(file_path: Path, tokenized_query: set[str]) -> dict:
    total_score = 0
    content = file_path.read_text(encoding="utf-8")
    
    tokenized_content = tokenize(content)
    score = len(tokenized_query & tokenized_content)

    if (score > 0):
        return {
            "source_path": file_path,
            "text": content,
            "score": score
        }
    else:
        return {}


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"\b\w+\b", text.lower()))