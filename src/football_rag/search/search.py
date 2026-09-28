from pathlib import Path
import re

def search_documents(query: str, sources: list = ["data/reports", "docs/knowledge"], limit: int = 3) -> list[dict]:
    search_results: list[dict] = []
    
    # Normalise a split the search term once
    normalized_search_words = query.lower().split(" ")
  
    # Loop over sources and search each .md file for matching words
    for source_path in sources:
        directory = Path(source_path)
        for file_path in directory.glob("*.md"):
            searched_file = search_source_file(file_path, normalized_search_words)
            if searched_file != {}:
                search_results.append(searched_file)
                
    # Sort the search results by score - highest to lowest
    search_results.sort(key=lambda sr: sr["score"], reverse=True)
    
    return search_results[:limit]


def search_source_file(file_path: Path, normalized_words: list) -> dict:
    total_score = 0
    content = file_path.read_text(encoding="utf-8")
    normalized_content = content.lower()
    
    for normalized_word in normalized_words:
        word_score = len(re.findall(re.escape(normalized_word), normalized_content))
        total_score += word_score

    if (total_score > 0):
        return {
            "source_path": file_path,
            "text": content,
            "score": total_score
        }
    else:
        return {}
