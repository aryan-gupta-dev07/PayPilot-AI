from app.tools.products import find_products


def test_recommendations_respect_budget_and_use_case():
    results = find_products(
        category="laptop",
        budget=50000,
        requirements=[],
        use_case="gaming",
    )

    assert results, "Expected gaming laptop recommendations"

    for product in results:
        assert product["price"] <= 50000
        assert "gaming" in [
            item.lower() for item in product["use_cases"]
        ]


def test_recommendations_are_sorted_by_suitability_score():
    from app.tools.products import calculate_product_score

    results = find_products(
        category="laptop",
        budget=50000,
        requirements=["16GB RAM"],
        use_case="gaming",
    )

    scores = [
        calculate_product_score(
            product,
            requirements=["16GB RAM"],
            use_case="gaming",
        )
        for product in results
    ]

    assert scores == sorted(scores, reverse=True)