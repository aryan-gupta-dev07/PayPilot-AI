from app.tools.products import (
    find_products,
    calculate_product_score,
    explain_recommendation,
)

from app.core.preferences import get_user_preferences
from app.core.feedback import process_user_feedback

preferences = get_user_preferences()

feedback = input(
    "Any preference to update? "
    "(e.g. prioritize battery life more, or press Enter to skip): "
).strip()

if feedback:
    feedback_result = process_user_feedback(feedback)

    if feedback_result["updated"]:
        preferences = feedback_result["preferences"]
        print("Preferences updated:", preferences)
    else:
        print(feedback_result["message"])


requirements = ["gaming", "battery"]
budget = 50000
use_case = "gaming"

results = find_products(
    category="laptop",
    budget=budget,
    requirements=requirements,
    use_case=use_case,
    preferences=preferences,
)

print("\n===== PayPilot AI Recommendations =====\n")

if not results:
    print("No matching products found. Try changing your budget or requirements.")

else:
    for index, product in enumerate(results, start=1):
        score = calculate_product_score(
            product,
            requirements,
            use_case,
        )

        reasons = explain_recommendation(
            product,
            requirements,
            budget,
            use_case,
        )

        print(f"{index}. {product['name']}")
        print(f"   Price: ₹{product['price']}")
        print(f"   Rating: {product['rating']}/5")
        print(f"   Suitability Score: {score}/100")
        print("   Why recommended:")

        for reason in reasons:
            print(f"   - {reason}")

        print()