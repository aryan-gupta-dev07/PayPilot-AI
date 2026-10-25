from app.tools.products import PRODUCTS, match_requirements, explain_recommendation
from app.tools.products import find_products, calculate_product_score


def test_user_preferences_affect_recommendation_score():
    products = find_products(
        category="laptop",
        budget=50000,
        requirements=["gaming"],
        use_case="gaming",
        preferences=["512GB SSD"],
    )

    assert products

    top_product = products[0]

    assert "512GB SSD" in top_product["features"]


def test_exact_keyword_matching():
    results = match_requirements(PRODUCTS, ["battery"])

    assert len(results) == 4


def test_similar_meaning_different_wording():
    results = match_requirements(
        PRODUCTS,
        ["long battery life"],
    )

    assert len(results) == 4


def test_empty_requirements_return_all_products():
    results = match_requirements(PRODUCTS, [])

    assert len(results) == len(PRODUCTS)

def test_matching_preference_improves_product_score():
    product = {
        "name": "Laptop A",
        "category": "laptop",
        "price": 45000,
        "currency": "INR",
        "rating": 4.0,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    score_without_preference = calculate_product_score(
        product=product,
        requirements=["gaming"],
        use_case="gaming",
        preferences=[],
    )

    score_with_preference = calculate_product_score(
        product=product,
        requirements=["gaming"],
        use_case="gaming",
        preferences=["512GB SSD"],
    )

    assert score_with_preference > score_without_preference


from app.tools.products import rank_products


def test_preferences_can_change_product_ranking():
    product_a = {
        "name": "Laptop A",
        "category": "laptop",
        "price": 45000,
        "currency": "INR",
        "rating": 4.5,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    product_b = {
        "name": "Laptop B",
        "category": "laptop",
        "price": 45000,
        "currency": "INR",
        "rating": 4.5,
        "features": ["16GB RAM", "1TB SSD"],
        "use_cases": ["gaming"],
    }

    products = [product_a, product_b]

    ranked_products = rank_products(
        products=products,
        requirements=["gaming"],
        use_case="gaming",
        preferences=["1TB SSD"],
    )

    assert ranked_products[0]["name"] == "Laptop B"

def test_recommendations_never_exceed_budget():
    budget = 50000

    results = find_products(
        category="laptop",
        budget=budget,
        requirements=[],
        use_case=None,
    )

    assert results, "Expected at least one product within budget"

    for product in results:
        assert product["price"] <= budget


def test_no_products_for_unavailable_category():
    results = find_products(
        category="tablet",
        budget=50000,
        requirements=[],
        use_case=None,
    )

    assert results == []


def test_unrelated_requirement_does_not_match_products():
    results = find_products(
        category="laptop",
        budget=50000,
        requirements=["waterproof submarine"],
        use_case=None,
    )

    assert results == []

def test_products_with_better_rating_get_higher_score_when_other_factors_match():


    product_a = {
        "name": "Laptop A",
        "category": "laptop",
        "price": 45000,
        "currency": "INR",
        "rating": 4.0,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    product_b = {
        "name": "Laptop B",
        "category": "laptop",
        "price": 45000,
        "currency": "INR",
        "rating": 4.5,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    score_a = calculate_product_score(
        product_a,
        requirements=["16GB RAM"],
        use_case="gaming",
    )

    score_b = calculate_product_score(
        product_b,
        requirements=["16GB RAM"],
        use_case="gaming",
    )

    assert score_b > score_a

def test_exact_ssd_capacity_matching():
    from app.tools.products import match_requirements, PRODUCTS

    matched = match_requirements(PRODUCTS, ["1TB SSD"])
    names = [product["name"] for product in matched]

    assert names == ["Gaming Laptop B", "Performance Laptop E"]


def test_requirement_matching_is_case_insensitive():
    from app.tools.products import match_requirements, PRODUCTS

    matched = match_requirements(PRODUCTS, ["1tb ssd"])
    names = [product["name"] for product in matched]

    assert names == ["Gaming Laptop B", "Performance Laptop E"]


def test_unmatched_exact_requirement_returns_empty_list():
    from app.tools.products import match_requirements, PRODUCTS

    matched = match_requirements(
        PRODUCTS,
        ["16TB SSD"],
    )

    assert matched == []

def test_explanation_includes_budget_and_matching_requirement():
    product = {
        "name": "Gaming Laptop A",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM", "512GB SSD", "good battery"],
        "use_cases": ["gaming", "performance"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=["16GB RAM"],
        budget=50000,
        use_case="gaming",
    )

    assert any("within" in reason for reason in reasons)
    assert any("Matching requirements: 16GB RAM" in reason for reason in reasons)
    assert any("Suitable use case: gaming" in reason for reason in reasons)


def test_explanation_reports_unmatched_requirement():
    product = {
        "name": "Gaming Laptop A",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM", "512GB SSD", "good battery"],
        "use_cases": ["gaming", "performance"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=["OLED display"],
        budget=50000,
        use_case="gaming",
    )

    assert any("not found in product data: OLED display" in reason for reason in reasons)


def test_explanation_reports_over_budget():
    product = {
        "name": "Gaming Laptop A",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM", "512GB SSD", "good battery"],
        "use_cases": ["gaming", "performance"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=[],
        budget=40000,
        use_case="study",
    )

    assert any("exceeds" in reason for reason in reasons)
    assert any("not listed" in reason for reason in reasons)

import pytest

from app.tools.products import filter_by_budget


@pytest.mark.parametrize("budget", [0, -100, -5000])
def test_filter_by_budget_rejects_invalid_budget(budget):
    with pytest.raises(
        ValueError,
        match="Budget must be greater than zero.",
    ):
        filter_by_budget([], budget)

def test_match_requirements_returns_product_matching_any_requirement():
    from app.tools.products import match_requirements

    products = [
        {
            "name": "Test Laptop",
            "price": 40000,
            "rating": 4.2,
            "features": ["16GB RAM"],
            "use_cases": ["study"],
        }
    ]

    result = match_requirements(
        products,
        ["16GB RAM", "1TB SSD"],
    )

    assert len(result) == 1
    assert result[0]["name"] == "Test Laptop"

def test_match_requirements_returns_product_matching_all_requirements():
    from app.tools.products import match_requirements

    products = [
        {
            "name": "Complete Laptop",
            "price": 50000,
            "rating": 4.5,
            "features": ["16GB RAM", "1TB SSD"],
            "use_cases": ["gaming"],
        }
    ]

    result = match_requirements(
        products,
        ["16GB RAM", "1TB SSD"],
    )

    assert len(result) == 1
    assert result[0]["name"] == "Complete Laptop"

def test_match_requirements_returns_empty_when_nothing_matches():
    from app.tools.products import match_requirements

    products = [
        {
            "name": "Study Laptop",
            "price": 40000,
            "rating": 4.2,
            "features": ["16GB RAM", "512GB SSD"],
            "use_cases": ["study"],
        }
    ]

    result = match_requirements(
        products,
        ["1TB SSD"],
    )

    assert result == []

from app.tools.products import explain_recommendation


def test_explanation_reports_full_match():
    product = {
        "name": "Gaming Laptop",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM", "1TB SSD"],
        "use_cases": ["gaming"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=["16GB RAM", "1TB SSD"],
        budget=50000,
        use_case="gaming",
    )

    assert "Recommendation status: Full match." in reasons


def test_explanation_reports_partial_match():
    product = {
        "name": "Gaming Laptop",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM"],
        "use_cases": ["gaming"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=["16GB RAM", "1TB SSD"],
        budget=50000,
        use_case="gaming",
    )

    assert "Recommendation status: Partial match." in reasons


def test_explanation_reports_no_match():
    product = {
        "name": "Study Laptop",
        "price": 40000,
        "rating": 4.2,
        "features": ["8GB RAM", "512GB SSD"],
        "use_cases": ["study"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=["1TB SSD"],
        budget=50000,
    )

    assert "Recommendation status: No match." in reasons

def test_explanation_reports_no_match_for_unsupported_use_case():
    product = {
        "name": "Student Laptop",
        "price": 42000,
        "rating": 4.4,
        "features": ["16GB RAM", "1TB SSD"],
        "use_cases": ["study", "work"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=["16GB RAM", "1TB SSD"],
        budget=50000,
        use_case="gaming",
    )

    assert "Recommendation status: No match." in reasons
    assert (
        "Use case 'gaming' is not listed for this product."
        in reasons
    )


def test_explanation_reports_full_match_for_supported_use_case():
    product = {
        "name": "Gaming Laptop",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM", "1TB SSD"],
        "use_cases": ["gaming", "performance"],
    }

    reasons = explain_recommendation(
        product=product,
        requirements=["16GB RAM", "1TB SSD"],
        budget=50000,
        use_case="gaming",
    )

    assert "Recommendation status: Full match." in reasons
    assert "Suitable use case: gaming." in reasons

def test_higher_battery_priority_prefers_battery_product():
    from app.tools.products import calculate_product_score

    battery_product = {
        "name": "Laptop A",
        "price": 50000,
        "rating": 4.0,
        "features": ["16GB RAM", "long battery life"],
        "use_cases": ["study"],
    }

    performance_product = {
        "name": "Laptop B",
        "price": 50000,
        "rating": 4.0,
        "features": ["16GB RAM", "high performance"],
        "use_cases": ["study"],
    }

    battery_score = calculate_product_score(
        product=battery_product,
        requirements=[],
        use_case="study",
        preferences={
            "battery_life": 1.0,
            "performance": 0.0,
        },
    )

    performance_score = calculate_product_score(
        product=performance_product,
        requirements=[],
        use_case="study",
        preferences={
            "battery_life": 1.0,
            "performance": 0.0,
        },
    )

    assert battery_score > performance_score

def test_compare_products():
    from app.tools.products import compare_products

    product_a = {
        "name": "Laptop A",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    product_b = {
        "name": "Laptop B",
        "price": 52000,
        "rating": 4.5,
        "features": ["16GB RAM", "1TB SSD"],
        "use_cases": ["gaming"],
    }

    result = compare_products(product_a, product_b)

    assert result["cheaper_product"] == "Laptop A"
    assert result["price_difference"] == 4000
    assert "16gb ram" in result["shared_features"]
    assert "512gb ssd" in result["unique_features_a"]
    assert "1tb ssd" in result["unique_features_b"]


def test_get_product_pros_and_cons():
    from app.tools.products import get_product_pros_and_cons

    product = {
        "name": "Laptop A",
        "price": 48000,
        "rating": 4.5,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    result = get_product_pros_and_cons(
        product=product,
        budget=50000,
        requirements=["16GB RAM", "1TB SSD"],
    )

    assert "Within your budget." in result["pros"]
    assert "Matches requirement: 16GB RAM." in result["pros"]
    assert "Requirement not found: 1TB SSD." in result["cons"]


def test_compare_products():
    from app.tools.products import compare_products

    product_a = {
        "name": "Laptop A",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    product_b = {
        "name": "Laptop B",
        "price": 52000,
        "rating": 4.5,
        "features": ["16GB RAM", "1TB SSD"],
        "use_cases": ["gaming"],
    }

    result = compare_products(product_a, product_b)

    assert result["cheaper_product"] == "Laptop A"
    assert result["price_difference"] == 4000
    assert "16gb ram" in result["shared_features"]
    assert "512gb ssd" in result["unique_features_a"]
    assert "1tb ssd" in result["unique_features_b"]


def test_get_product_pros_and_cons():
    from app.tools.products import get_product_pros_and_cons

    product = {
        "name": "Laptop A",
        "price": 48000,
        "rating": 4.5,
        "features": ["16GB RAM", "512GB SSD"],
        "use_cases": ["gaming"],
    }

    result = get_product_pros_and_cons(
        product=product,
        budget=50000,
        requirements=["16GB RAM", "1TB SSD"],
    )

    assert "Within your budget." in result["pros"]
    assert "Matches requirement: 16GB RAM." in result["pros"]
    assert "Requirement not found: 1TB SSD." in result["cons"]


def test_get_comparison_summary():
    from app.tools.products import get_comparison_summary

    product_a = {
        "name": "Laptop A",
        "price": 48000,
        "rating": 4.3,
        "features": ["16GB RAM"],
        "use_cases": ["gaming"],
    }

    product_b = {
        "name": "Laptop B",
        "price": 52000,
        "rating": 4.5,
        "features": ["16GB RAM"],
        "use_cases": ["gaming"],
    }

    result = get_comparison_summary(product_a, product_b)

    assert "Laptop A is ₹4000 cheaper." in result
    assert "Laptop B has the higher dataset rating." in result
