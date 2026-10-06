def plan_shopping_request(user_request: str) -> dict:
    """
    Convert a natural-language shopping request
    into structured requirements.
    """

    return {
        "original_request": user_request,
        "category": "laptop",
        "budget": 50000,
        "currency": "INR",
        "preferences": ["gaming"],
        "requirements": ["good battery life"],
    }