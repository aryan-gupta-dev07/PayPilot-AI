import json
from typing import Any

from .llm import generate_response


def create_intent(
    category: str | None = None,
    budget: float | None = None,
    currency: str = "INR",
    use_case: str | None = None,
    requirements: list[str] | None = None,
    preferences: list[str] | None = None,
    constraints: list[str] | None = None,
) -> dict[str, Any]:
    """Create a standardized shopping intent."""

    return {
        "category": category,
        "budget": budget,
        "currency": currency,
        "use_case": use_case,
        "requirements": requirements or [],
        "preferences": preferences or [],
        "constraints": constraints or [],
    }


def extract_intent(user_request: str) -> dict[str, Any]:
    """Extract structured shopping intent from a natural-language request."""

    prompt = f"""
You are the intent extraction module of PayPilot AI.

Extract the user's shopping requirements and return ONLY valid JSON.

Use exactly these fields:
- category
- budget
- currency
- use_case
- requirements
- preferences
- constraints

Rules:
- budget must be a number or null
- currency should be a 3-letter currency code
- requirements, preferences, and constraints must be arrays of strings
- Do not add extra fields
- If information is missing, use null or an empty array

User request:
{user_request}
"""

    response = generate_response(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("LLM did not return valid JSON.")