from typing import Any


DEFAULT_PREFERENCES: dict[str, Any] = {
    "battery_life": 0.5,
    "performance": 0.5,
    "rating": 0.5,
}

_USER_PREFERENCES = DEFAULT_PREFERENCES.copy()


def get_user_preferences() -> dict[str, Any]:
    """Return a copy of the current user preferences."""
    return _USER_PREFERENCES.copy()


def update_user_preference(
    preference: str,
    priority: float,
) -> dict[str, Any]:
    """Update one preference and return the updated preferences."""

    if preference not in DEFAULT_PREFERENCES:
        raise ValueError(f"Unknown preference: {preference}")

    if not 0.0 <= priority <= 1.0:
        raise ValueError("Priority must be between 0.0 and 1.0")

    _USER_PREFERENCES[preference] = priority

    return get_user_preferences()


def reset_user_preferences() -> None:
    """Reset preferences to their default values."""
    _USER_PREFERENCES.clear()
    _USER_PREFERENCES.update(DEFAULT_PREFERENCES)