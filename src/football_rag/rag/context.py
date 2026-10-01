
def format_context(results: list[dict]) -> str:
    context_lines = []
    for i, result in enumerate(results):
        context_lines.append(f"[{i + 1}]")
        context_lines.append(f"Source: {result['source_path']}")
        context_lines.append("Content:")
        context_lines.append(result['text'])
        
    return "\n".join(context_lines)