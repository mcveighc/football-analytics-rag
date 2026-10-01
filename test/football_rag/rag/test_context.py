from pathlib import Path

from football_rag.rag.context import format_context

def test_context_returns_expected_string():
    # assemble
    results = [
        {
            "source_path": "test_source_1.txt",
            "score": 1,
            "text": "This is the first test document."
        },
        {
            "source_path": "test_source_2.txt",
            "score": 2,
            "text": "This is the second test document."
        }
    ]

    # act
    context = format_context(results)

    # assert
    expected = "\n".join(
        (
            "[1]",
            "Source: test_source_1.txt",
            "Content:",
            "This is the first test document.",
            
            "[2]",
            "Source: test_source_2.txt",
            "Content:",
            "This is the second test document.",
        )
    )
    assert context == expected
    
def test_context_formats_path_and_multiline_markdown():
    # assemble
    source_path = Path("data/reports/match_3913082.md")
    text = "# Match summary\n\nArsenal won 2-1.\n\n## Key moments\n- Two goals before halftime."
    results = [{"source_path": source_path, "text": text}]

    # act
    context = format_context(results)

    # assert
    expected = "\n".join(("[1]", f"Source: {source_path}", "Content:", text))
    assert context == expected

def test_context_with_empty_list_returns_empty_string():
    # assemble
    results = []

    # act
    context = format_context(results)

    # assert
    assert context == ""