from argparse import ArgumentParser
from football_rag.search.search import search_documents

def main():
    parser = ArgumentParser()
    parser.add_argument("-m", "--query", type=str, required=True)
    parser.add_argument("-l", "--limit", type=int, default=3, required=False)
    args = parser.parse_args()
    
    query = args.query;
    limit = args.limit;
    
    search_results: list[dict] = search_documents(query, limit=limit)
    
    for result in search_results:
        source_path = result["source_path"]
        score = result["score"]
        text = " ".join(result["text"].split())
        preview = text[:200] + ("..." if len(text) > 200 else "")

        print(f"Source: {source_path}\nScore: {score}\nPreview: {preview}\n")
    
if __name__ == "__main__":
    main()
    