from app.agent.planner import extract_intent

from app.tools.products import (
    find_products,
    calculate_product_score,
    explain_recommendation,
    compare_products,
    get_product_pros_and_cons,
    get_comparison_summary,
    generate_evidence_card,
)

from app.core.preferences import get_user_preferences
from app.core.feedback import process_user_feedback


def display_recommendations(
    results,
    requirements,
    budget,
    use_case,
    preferences,
):
    print("\n===== PayPilot AI Recommendations =====\n")

    if not results:
        print(
            "No matching products found. "
            "Try changing your budget or requirements."
        )
        return

    for index, product in enumerate(results, start=1):
        score = calculate_product_score(
            product,
            requirements,
            use_case,
            preferences=preferences,
        )

        score_out_of_100 = round(score * 100, 2)

        reasons = explain_recommendation(
            product,
            requirements,
            budget,
            use_case,
        )

        print(f"{index}. {product['name']}")
        print(f"   Price: Rs. {product['price']}")
        print(f"   Rating: {product['rating']}/5")
        print(f"   Suitability Score: {score_out_of_100}/100")

        evidence_card = generate_evidence_card(
            product=product,
            budget=budget,
            requirements=requirements,
            use_case=use_case,
        )

        print("\n   --- Evidence Card ---")
        print(
            f"   Constraint Guard: "
            f"{'ELIGIBLE' if evidence_card['eligible'] else 'NOT ELIGIBLE'}"
        )
        print(f"   Evidence Source: {evidence_card['evidence_source']}")

        for item in evidence_card["evidence"]:
            print(
                f"   - {item['check']}: "
                f"{item['status']} — {item['details']}"
            )

        print("   --- End Evidence Card ---")

        print("   Why recommended:")

        for reason in reasons:
            print(f"   - {reason}")

        details = get_product_pros_and_cons(
            product=product,
            budget=budget,
            requirements=requirements,
        )

        print("   Pros:")
        for pro in details["pros"]:
            print(f"   - {pro}")

        print("   Cons:")
        for con in details["cons"]:
            print(f"   - {con}")

        print()

    if len(results) >= 2:
        product_a = results[0]
        product_b = results[1]

        comparison = compare_products(
            product_a,
            product_b,
        )

        print("===== Product Comparison =====")
        print(f"Product A: {comparison['product_a']}")
        print(f"Product B: {comparison['product_b']}")
        print(
            f"Price difference: "
            f"Rs. {comparison['price_difference']}"
        )
        print(
            f"Cheaper option: "
            f"{comparison['cheaper_product']}"
        )

        print("\nShared features:", comparison["shared_features"])
        print(
            f"{product_a['name']} unique features:",
            comparison["unique_features_a"],
        )
        print(
            f"{product_b['name']} unique features:",
            comparison["unique_features_b"],
        )

        print("\n===== Comparison Summary =====")
        print(get_comparison_summary(product_a, product_b))


def main():
    preferences = get_user_preferences()
    preferences.update(intent_preferences)

    print("\n===== PayPilot AI Shopping Assistant =====")

    user_request = input(
        "\nDescribe the product you want: "
    ).strip()

    if not user_request:
        print("Please enter a shopping request.")
        return

    try:
        intent = extract_intent(user_request)
    except (ValueError, TypeError) as error:
        print(f"Could not understand your request: {error}")
        return
    except Exception as error:
        print(f"Could not process your request: {error}")
        return

    category = intent.get("category")
    budget = intent.get("budget")
    use_case = intent.get("use_case")
    requirements = intent.get("requirements", [])
    preferences_from_intent = intent.get("preferences", [])
    constraints = intent.get("constraints", [])

    # Convert intent preferences into ranking preferences
    intent_preferences = {}

    for item in preferences_from_intent:
        if not isinstance(item, str):
            continue

        item = item.lower().strip()

        if "battery" in item:
            intent_preferences["battery_life"] = 1.0
        elif "performance" in item:
            intent_preferences["performance"] = 1.0
        elif "rating" in item or "review" in item:
            intent_preferences["rating"] = 1.0

    # Validate intent constraints
    if not isinstance(constraints, list) or not all(
        isinstance(item, str) for item in constraints
    ):
        print("Constraints must be a list of text values.")
        return

    if not isinstance(category, str) or not category.strip():
        print("Please specify a product category, such as laptop.")
        return

    if (
        not isinstance(budget, (int, float))
        or isinstance(budget, bool)
        or budget <= 0
    ):
        print("Please provide a valid positive budget.")
        return

    if not isinstance(requirements, list):
        print("Requirements must be a list.")
        return

    if use_case is not None and not isinstance(use_case, str):
        print("The use case must be text.")
        return

    if not all(isinstance(item, str) for item in requirements):
        print("Each requirement must be text.")
        return

    requirements = [
        item.strip()
        for item in requirements
        if item.strip()
    ]

    print("\n===== Extracted Shopping Intent =====")
    print(f"Category: {category}")
    print(f"Budget: Rs. {budget}")
    print(f"Use case: {use_case or 'Not specified'}")
    print(f"Requirements: {requirements}")

    # Display user constraints
    if constraints:
        print("\nUser constraints:")
        for constraint in constraints:
            print(f"- {constraint}")

    results = find_products(
        category=category,
        budget=budget,
        requirements=requirements,
        use_case=use_case,
        preferences={**preferences, **intent_preferences},
        constraints=constraints,
    )

    if not results:
        print(
            "\nNo matching products found. "
            "Try changing your budget or requirements."
        )
        return

    print("\n===== Initial Recommendations =====")

    display_recommendations(
        results=results,
        requirements=requirements,
        budget=budget,
        use_case=use_case,
        preferences=preferences,
    )

    feedback = input(
        "\nWant to adjust your preferences? "
        "(e.g. prioritize battery life more, "
        "prioritize performance less, or press Enter to finish): "
    ).strip()

    if not feedback:
        print("\nNo preference changes requested.")
        return

    try:
        feedback_result = process_user_feedback(feedback)
    except ValueError as error:
        print(f"\nFeedback error: {error}")
        return

    if not feedback_result["updated"]:
        print(f"\n{feedback_result['message']}")
        return

    preferences = feedback_result["preferences"]

    print("\n===== Updated Preferences =====")
    print(preferences)

    updated_results = find_products(
        category=category,
        budget=budget,
        requirements=requirements,
        use_case=use_case,
        preferences=preferences,
        constraints=constraints,
    )

    print("\n===== Updated Recommendations =====")

    display_recommendations(
        results=updated_results,
        requirements=requirements,
        budget=budget,
        use_case=use_case,
        preferences=preferences,
    )

    print("\n===== Feedback Adaptation Summary =====")
    print(
        f"Updated preference: "
        f"{feedback_result['preference']}"
    )
    print(
        f"New priority: "
        f"{feedback_result['priority']}"
    )
    print("Recommendations recalculated using updated preferences.")


if __name__ == "__main__":
    main()
