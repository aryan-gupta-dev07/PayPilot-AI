from typing import Any


def create_product(
    name: str,
    category: str,
    price: float,
    currency: str,
    rating: float,
    features: list[str],
    use_cases: list[str],
) -> dict[str, Any]:
    """
    Create a standardized product object.
    """

    return {
        "name": name,
        "category": category,
        "price": price,
        "currency": currency,
        "rating": rating,
        "features": features,
        "use_cases": use_cases,
    }
    
PRODUCTS = [
    create_product(
        name="Gaming Laptop A",
        category="laptop",
        price=48000,
        currency="INR",
        rating=4.3,
        features=["16GB RAM", "512GB SSD", "good battery"],
        use_cases=["gaming", "performance"],
    ),

    create_product(
        name="Gaming Laptop B",
        category="laptop",
        price=52000,
        currency="INR",
        rating=4.5,
        features=["16GB RAM", "1TB SSD", "excellent battery"],
        use_cases=["gaming", "performance"],
    ),

    create_product(
        name="Student Laptop C",
        category="laptop",
        price=42000,
        currency="INR",
        rating=4.4,
        features=["16GB RAM", "512GB SSD", "long battery"],
        use_cases=["study", "work"],
    ),

    create_product(
        name="Budget Laptop D",
        category="laptop",
        price=35000,
        currency="INR",
        rating=4.1,
        features=["8GB RAM", "512GB SSD", "good battery"],
        use_cases=["study", "work"],
    ),

    create_product(
        name="Performance Laptop E",
        category="laptop",
        price=65000,
        currency="INR",
        rating=4.6,
        features=["16GB RAM", "1TB SSD", "high performance"],
        use_cases=["gaming", "performance"],
    ),
]

def search_products(category: str) -> list[dict[str, Any]]:
    """
    Search products by category.
    """

    return [
        product
        for product in PRODUCTS
        if product["category"].lower() == category.lower()
    ]
    
def filter_by_budget(
    products: list[dict[str, Any]],
    budget: float,
) -> list[dict[str, Any]]:
    """
    Return products that are within the user's budget.
    """

    return [
        product
        for product in products
        if product["price"] <= budget
    ]
    
def match_requirements(
    products: list[dict[str, Any]],
    requirements: list[str],
) -> list[dict[str, Any]]:
    """
    Return products matching at least one requirement.
    """

    if not requirements:
        return products.copy()

    matched_products = []

    for product in products:
        product_text = " ".join(
            [
                product["name"],
                *product["features"],
                *product["use_cases"],
            ]
        ).lower()

        matched = any(
            requirement.lower() in product_text
            for requirement in requirements
        )

        if matched:
            matched_products.append(product)

    return matched_products

def calculate_product_score(
    product: dict[str, Any],
    requirements: list[str],
    use_case: str | None = None,
) -> float:
    """
    Calculate a baseline product suitability score out of 100.
    """

    product_text = " ".join(
        [
            product["name"],
            *product["features"],
            *product["use_cases"],
        ]
    ).lower()

    if requirements:
        matched_count = sum(
            1
            for requirement in requirements
            if requirement.lower() in product_text
        )

        requirement_score = (
            matched_count / len(requirements)
        ) * 100
    else:
        requirement_score = 100

    if use_case:
        use_case_score = (
            100
            if use_case.lower() in [
                item.lower() for item in product["use_cases"]
            ]
            else 0
        )
    else:
        use_case_score = 100

    rating_score = (product["rating"] / 5) * 100

    final_score = (
        requirement_score * 0.50
        + use_case_score * 0.30
        + rating_score * 0.20
    )

    return round(final_score, 2)

def explain_recommendation(
    product: dict[str, Any],
    requirements: list[str],
    budget: float,
    use_case: str | None = None,
) -> list[str]:
    """Explain why a product matches the user's requirements."""

    reasons = []

    if product["price"] <= budget:
        reasons.append(
            f"Price ₹{product['price']} is within your ₹{budget} budget."
        )

    product_text = " ".join(
        [
            product["name"],
            *product["features"],
            *product["use_cases"],
        ]
    ).lower()

    matched_requirements = [
        requirement
        for requirement in requirements
        if requirement.lower() in product_text
    ]

    if matched_requirements:
        reasons.append(
            "Matching requirements: "
            + ", ".join(matched_requirements)
            + "."
        )

    if use_case and use_case.lower() in [
        item.lower() for item in product["use_cases"]
    ]:
        reasons.append(f"Suitable use case: {use_case}.")

    reasons.append(f"Customer rating in dataset: {product['rating']}/5.")

    return reasons

def rank_products(
    products: list[dict[str, Any]],
    requirements: list[str],
    use_case: str | None = None,
) -> list[dict[str, Any]]:
    """
    Rank products by calculated suitability score.
    """

    return sorted(
        products,
        key=lambda product: calculate_product_score(
            product,
            requirements,
            use_case,
        ),
        reverse=True,
    )
    
def find_products(
    category: str,
    budget: float,
    requirements: list[str],
    use_case: str | None = None,
) -> list[dict[str, Any]]:
    """
    Find and rank products using the user's shopping intent.
    """

    products = search_products(category)

    products = filter_by_budget(products, budget)

    products = match_requirements(products, requirements)

    products = rank_products(
        products,
        requirements,
        use_case,
    )

    return products