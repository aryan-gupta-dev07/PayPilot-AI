from app.tools.products import PRODUCTS, match_requirements
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