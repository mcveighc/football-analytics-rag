from argparse import ArgumentParser
from pyexpat import model

from openai import OpenAI

from football_rag.rag import answer
from football_rag.rag.answer import generate_answer
from football_rag.rag.context import format_context
from football_rag.search.search import search_documents


def main():
    parser = ArgumentParser()
    parser.add_argument("-q", "--question", type=str, required=True)
    parser.add_argument("-m", "--model", type=str, default="gpt-6-luna")
    parser.add_argument("-l", "--limit", type=int, default=3)
    args = parser.parse_args()
    
    question = args.question
    model = args.model
    
    documents = search_documents(question, limit=args.limit)

    if not documents:
        print("No relevant documents found to answer the question.")
        return

    client = OpenAI()
    answer = generate_answer(question, documents, client, model)

    print(answer)
    
    print("\nRetrieved sources:")
    for number, document in enumerate(documents, start=1):
        print(f"[{number}] {document['source_path']}")
    
if __name__ == "__main__":
    main()
    