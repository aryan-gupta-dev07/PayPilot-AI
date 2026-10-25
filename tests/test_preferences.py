import pytest
from app.core.preferences import reset_user_preferences
@pytest.fixture(autouse=True)
def reset_preferences_before_each_test():
    reset_user_preferences()

from app.core.preferences import (
    get_user_preferences,
    update_user_preference,
)


def test_default_preferences():
    preferences = get_user_preferences()

    assert preferences == {
        "battery_life": 0.5,
        "performance": 0.5,
        "rating": 0.5,
    }


def test_update_user_preference():
    updated = update_user_preference("battery_life", 0.9)

    assert updated["battery_life"] == 0.9


def test_invalid_priority_is_rejected():
    with pytest.raises(ValueError):
        update_user_preference("battery_life", 1.5)


def test_unknown_preference_is_rejected():
    with pytest.raises(ValueError):
        update_user_preference("camera", 0.8)
