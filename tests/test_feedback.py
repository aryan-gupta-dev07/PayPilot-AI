import pytest

from app.core.feedback import process_user_feedback
from app.core.preferences import get_user_preferences


def test_battery_feedback_updates_preference():
    result = process_user_feedback(
        "Please prioritize battery life more"
    )

    assert result["updated"] is True
    assert result["preference"] == "battery_life"
    assert result["priority"] == 0.9


def test_performance_feedback_updates_preference():
    result = process_user_feedback(
        "Increase performance priority"
    )

    assert result["updated"] is True
    assert result["preference"] == "performance"
    assert result["priority"] == 0.9


def test_feedback_without_recognized_preference():
    result = process_user_feedback(
        "I want something different"
    )

    assert result["updated"] is False


def test_feedback_without_priority_direction():
    result = process_user_feedback(
        "Battery life matters"
    )

    assert result["updated"] is False


def test_empty_feedback_is_rejected():
    with pytest.raises(ValueError):
        process_user_feedback("")