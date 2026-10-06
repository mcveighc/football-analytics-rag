from openai import OpenAI

from football_rag.rag.prompts import ANSWER_INSTRUCTIONS
from football_rag.rag.context import format_context

def generate_answer(
    question: str,
    results: list[dict],
    client: OpenAI,
    model: str,
) -> str:
    if results is None or len(results) == 0:
        return "No relevant documents found to answer the question."
    
    document_context = format_context(results)
    
    response = client.responses.create(
        model=model,
        instructions=ANSWER_INSTRUCTIONS,
        input=f"Question:\n{question}\n\nDocuments:\n{document_context}"
    )
    
    return response.output_text
