from openai import OpenAI
from pytest_mock import MockerFixture
from football_rag.rag.answer import generate_answer
from football_rag.rag.prompts import ANSWER_INSTRUCTIONS
from football_rag.rag.context import format_context


def test_generate_answer_returns_expected_string_when_no_results(mocker: MockerFixture):
    # assemble
    question = "What is the score of the match?"
    results = []
    fake_client = get_fake_client(mocker, "should not be used")
    model = "gpt-4"

    # act
    answer = generate_answer(question, results, fake_client, model)

    # assert
    expected_answer = "No relevant documents found to answer the question."
    assert answer == expected_answer
    fake_client.responses.create.assert_not_called()

def test_generate_answer_returns_expected_string_when_results_is_none():
    # assemble
    question = "What is the score of the match?"
    results = None
    client = None  # Mock or stub the OpenAI client if needed
    model = "gpt-4"

    # act
    answer = generate_answer(question, results, client, model)

    # assert
    expected_answer = "No relevant documents found to answer the question."
    assert answer == expected_answer
    


def test_generate_answer_returns_expected_string_with_results(mocker: MockerFixture):
    # assemble
    model = "gpt-4"
    question = "What is the score of the match?"
    results = [
        {
            "source_path": "test_source_1.txt",
            "score": 1,
            "text": "The match ended with a score of 2-1."
        }
    ]
    expected_output = "This is the only text I care about"
    fake_client = get_fake_client(mocker, expected_output)

    # act
    answer = generate_answer(question, results, fake_client, model)

    # assert
    assert answer == expected_output
    fake_client.responses.create.assert_called_once()

    call_arguments = fake_client.responses.create.call_args.kwargs
    
    assert call_arguments["model"] == model
    assert call_arguments["instructions"] == ANSWER_INSTRUCTIONS
    assert question in call_arguments["input"]
    assert format_context(results) in call_arguments["input"]
    assert "Question:" in call_arguments["input"]
    assert "Documents:" in call_arguments["input"]

def get_fake_client(mocker, expected_output):
    mock_response = mocker.MagicMock()
    mock_response.output_text = expected_output
    
    fake_client = OpenAI(api_key="fake-key-for-testing")
    mocker.patch.object(fake_client.responses, 'create', return_value=mock_response)
    
    return fake_client
