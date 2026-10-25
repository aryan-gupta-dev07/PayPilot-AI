from app.core.preferences import update_user_preference


def process_user_feedback(feedback: str) -> dict:
    """Convert simple user feedback into a preference update."""

    feedback_text = feedback.lower().strip()

    if not feedback_text:
        raise ValueError("Feedback cannot be empty")

    # Identify the preference mentioned in the feedback.
    if "battery" in feedback_text:
        preference = "battery_life"
    elif "performance" in feedback_text:
        preference = "performance"
    elif "rating" in feedback_text or "review" in feedback_text:
        preference = "rating"
    else:
        return {
            "updated": False,
            "message": "No recognized preference found.",
        }

    # Determine whether the user wants to increase or decrease priority.
    decrease_words = ["less", "decrease", "lower"]
    increase_words = [
        "more",
        "increase",
        "higher",
        "prioritize",
        "priority",
    ]

    if any(word in feedback_text for word in decrease_words):
        priority = 0.2
    elif any(word in feedback_text for word in increase_words):
        priority = 0.9
    else:
        return {
            "updated": False,
            "message": (
                "Please specify whether to increase "
                "or decrease priority."
            ),
        }

    # Update the selected preference.
    preferences = update_user_preference(
        preference,
        priority,
    )

    return {
        "updated": True,
        "preference": preference,
        "priority": priority,
        "preferences": preferences,
    }
