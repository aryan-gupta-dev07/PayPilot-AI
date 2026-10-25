from unittest.mock import patch

from app.agent.planner import create_intent, extract_intent


def test_create_intent():
    intent = create_intent(
        category="laptop",
        budget=55000,
        use_case="gaming",
        requirements=["battery"],
    )

    assert intent["category"] == "laptop"
    assert intent["budget"] == 55000
    assert intent["currency"] == "INR"
    assert intent["use_case"] == "gaming"
    assert intent["requirements"] == ["battery"]
    assert intent["preferences"] == []
    assert intent["constraints"] == []


@patch("app.agent.planner.generate_response")
def test_extract_intent(mock_generate_response):
    mock_generate_response.return_value = """
    {
        "category": "laptop",
        "budget": 55000,
        "currency": "INR",
        "use_case": "gaming",
        "requirements": ["battery"],
        "preferences": [],
        "constraints": []
    }
    """

    user_request = (
        "I need a gaming laptop under 55000 "
        "with good battery"
    )

    intent = extract_intent(user_request)

    assert intent["category"] == "laptop"
    assert intent["budget"] == 55000
    assert intent["currency"] == "INR"
    assert intent["use_case"] == "gaming"
    assert intent["requirements"] == ["battery"]
    assert intent["preferences"] == []
    assert intent["constraints"] == []

    mock_generate_response.assert_called_once()


@patch("app.agent.planner.generate_response")
def test_extract_intent_invalid_json(mock_generate_response):
    mock_generate_response.return_value = "This is not valid JSON"

    try:
        extract_intent("I need a gaming laptop")
    except ValueError as error:
        assert str(error) == "LLM did not return valid JSON."
    else:
        raise AssertionError("Expected ValueError for invalid JSON")
