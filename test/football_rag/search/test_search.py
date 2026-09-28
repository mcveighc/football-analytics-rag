from football_rag.search.search import search_documents

def test_search_documents_returns_expected_when_query_matches(tmp_path):
    # assemble
    md_file = tmp_path / "test_document.md"
    content = "expected goals"
    
    md_file.write_text(content, encoding="utf-8")
    
    # act
    search_results: list[dict] = search_documents("expected goals", sources=[tmp_path])
    
    # assert
    assert len(search_results) == 1
    assert search_results[0]["source_path"] == md_file
    assert search_results[0]["text"] == content
    assert search_results[0]["score"] == 2

def test_search_documents_returns_expected_when_query_partial_matches(tmp_path):
    # assemble
    md_file = tmp_path / "test_document.md"
    content = "expected goals"
    
    md_file.write_text(content, encoding="utf-8")
    
    # act
    search_results: list[dict] = search_documents("goals", sources=[tmp_path])
    
    # assert
    assert len(search_results) == 1
    assert search_results[0]["source_path"] == md_file
    assert search_results[0]["text"] == content
    assert search_results[0]["score"] == 1
    
def test_search_documents_returns_empty_when_query_does_not_match(tmp_path):
    # assemble
    md_file = tmp_path / "test_document.md"
    content = "expected goals"
    
    md_file.write_text(content, encoding="utf-8")
    
    # act
    search_results: list[dict] = search_documents("no match", sources=[tmp_path])
    
    # assert
    assert len(search_results) == 0

def test_search_documents_returns_expected_when_query_matches_multiple_files(tmp_path):
    # assemble
    md_file_one = tmp_path / "expected_goals.md"
    md_file_one_content = "expected goals"
    md_file_one.write_text(md_file_one_content, encoding="utf-8")
    
    md_file_two = tmp_path / "home_goals.md"
    md_file_two_content = "home goals"
    md_file_two.write_text(md_file_two_content, encoding="utf-8")
    
    # act
    search_results: list[dict] = search_documents("expected goals", sources=[tmp_path])
    
    # assert
    assert len(search_results) == 2
    
    assert search_results[0]["source_path"] == md_file_one
    assert search_results[0]["text"] == md_file_one_content
    assert search_results[0]["score"] == 2
    
    assert search_results[1]["source_path"] == md_file_two
    assert search_results[1]["text"] == md_file_two_content
    assert search_results[1]["score"] == 1
    
def test_search_documents_returns_expected_when_query_matches_files_from_multiple_sources(tmp_path_factory):
    # assemble
    knowledge_path = tmp_path_factory.mktemp("knowldege")
    md_file_one = knowledge_path / "expected_goals.md"
    md_file_one_content = "expected goals"
    md_file_one.write_text(md_file_one_content, encoding="utf-8")
    
    reports_path = tmp_path_factory.mktemp("reports")
    md_file_two = reports_path / "match_report.md"
    md_file_two_content = "Goals: 1"
    md_file_two.write_text(md_file_two_content, encoding="utf-8")
    
    # act
    search_results: list[dict] = search_documents("expected goals", sources=[knowledge_path, reports_path])
    
    # assert
    assert len(search_results) == 2
    
    assert search_results[0]["source_path"] == md_file_one
    assert search_results[0]["text"] == md_file_one_content
    assert search_results[0]["score"] == 2
    
    assert search_results[1]["source_path"] == md_file_two
    assert search_results[1]["text"] == md_file_two_content
    assert search_results[1]["score"] == 1
    
def test_search_documents_returns_results_ordered_by_score(tmp_path_factory):
    # assemble
    knowledge_path = tmp_path_factory.mktemp("knowldege")
    md_file_one = knowledge_path / "expected_goals.md"
    md_file_one_content = "expected goals"
    md_file_one.write_text(md_file_one_content, encoding="utf-8")
    
    reports_path = tmp_path_factory.mktemp("reports")
    md_file_two = reports_path / "match_report.md"
    md_file_two_content = "Goals: 1"
    md_file_two.write_text(md_file_two_content, encoding="utf-8")
    
    # act
    search_results: list[dict] = search_documents("expected goals", sources=[reports_path, knowledge_path])
    
    # assert
    assert len(search_results) == 2
    assert search_results[0]["score"] == 2
    assert search_results[1]["score"] == 1

def test_search_documents_returns_results_at_limit(tmp_path):    
    # assemble
        md_file_one = tmp_path / "expected_goals.md"
        md_file_one_content = "expected goals"
        md_file_one.write_text(md_file_one_content, encoding="utf-8")
        
        md_file_two = tmp_path / "home_goals.md"
        md_file_two_content = "home goals"
        md_file_two.write_text(md_file_two_content, encoding="utf-8")
        
        # act
        search_results: list[dict] = search_documents("expected goals", sources=[tmp_path], limit=1)
        
        # assert
        assert len(search_results) == 1