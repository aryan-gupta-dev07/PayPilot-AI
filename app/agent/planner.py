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

    if not user_request or not user_request.strip():
        raise ValueError("Shopping request cannot be empty.")

    prompt = f"""
You are the shopping intent extraction module of PayPilot AI.

Convert the user's shopping request into structured JSON.
Return ONLY valid JSON. Do not include Markdown or explanations.

Use exactly these fields:
- category
- budget
- currency
- use_case
- requirements
- preferences
- constraints

Rules:
1. Category is the product type, such as "laptop" or "phone".
2. Budget must be a number or null.
3. For "under 55000", extract the budget as 55000.
4. Currency must be a 3-letter code. Use "INR" if unspecified.
5. Use_case describes the purpose, such as "gaming" or "study".
6. Requirements contain specific features, such as "good battery",
   "16GB RAM", "1TB SSD", or "lightweight".
7. Preferences contain optional priorities explicitly mentioned.
8. Constraints contain additional restrictions explicitly mentioned.
9. Do not put the complete product phrase, such as "gaming laptop",
   into requirements when category and use_case represent it.
10. Do not omit features explicitly requested by the user.
11. Do not invent requirements or preferences.
12. Use empty arrays for missing list fields.
13. Use null for missing category, budget, or use_case.
14. Return exactly the seven specified fields.

Example:
User request: "I need a gaming laptop under 55000 with good battery"

Correct JSON:
{{
    "category": "laptop",
    "budget": 55000,
    "currency": "INR",
    "use_case": "gaming",
    "requirements": ["good battery"],
    "preferences": [],
    "constraints": []
}}

User request:
{user_request}
"""

    response = generate_response(prompt)

    if not isinstance(response, str) or not response.strip():
        raise ValueError("LLM returned an empty or invalid response.")

    cleaned_response = response.strip()

    if cleaned_response.startswith("```"):
        lines = cleaned_response.splitlines()
        lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        cleaned_response = "\n".join(lines).strip()

        if cleaned_response.lower().startswith("json"):
            cleaned_response = cleaned_response[4:].strip()

    try:
        intent = json.loads(cleaned_response)
    except json.JSONDecodeError as error:
        raise ValueError("LLM did not return valid JSON.") from error

    if not isinstance(intent, dict):
        raise ValueError("LLM response must be a JSON object.")

    required_fields = {
        "category",
        "budget",
        "currency",
        "use_case",
        "requirements",
        "preferences",
        "constraints",
    }

    if set(intent.keys()) != required_fields:
        raise ValueError(
            "LLM response contains missing or unexpected fields."
        )

    for field in ("requirements", "preferences", "constraints"):
        if not isinstance(intent[field], list) or not all(
            isinstance(item, str) for item in intent[field]
        ):
            raise ValueError(
                f"LLM field '{field}' must be a list of strings."
            )

    if intent["category"] is not None and not isinstance(
        intent["category"], str
    ):
        raise ValueError("LLM field 'category' must be a string or null.")

    if intent["use_case"] is not None and not isinstance(
        intent["use_case"], str
    ):
        raise ValueError("LLM field 'use_case' must be a string or null.")

    if not isinstance(intent["currency"], str):
        raise ValueError("LLM field 'currency' must be a string.")

    budget = intent["budget"]

    if budget is not None and (
        isinstance(budget, bool) or not isinstance(budget, (int, float))
    ):
        raise ValueError("LLM field 'budget' must be a number or null.")

    return intent
