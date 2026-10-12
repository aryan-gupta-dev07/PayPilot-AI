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
    Return products matching at least one requirement keyword.
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

        matched = False

        for requirement in requirements:
            requirement_text = requirement.lower().strip()

            if requirement_text in product_text:
                matched = True
                break

        if matched:
            matched_products.append(product)

    return matched_products

def calculate_product_score(
    product: dict[str, Any],
    requirements: list[str],
    use_case: str | None = None,
    preferences: list[str] | None = None,
) -> float:
    """
    Calculate product suitability using requirements,
    use case, rating, and user preferences.
    """

    product_text = " ".join(
        [
            product["name"],
            *product["features"],
            *product["use_cases"],
        ]
    ).lower()

    # 1. Requirement matching score
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

    # 2. Use-case score
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

    # 3. Rating score
    rating_score = (product["rating"] / 5) * 100

    # 4. Preference score
    preferences = preferences or []

    if preferences:
        matched_preferences = sum(
            1
            for preference in preferences
            if preference.lower() in product_text
        )

        preference_score = (
            matched_preferences / len(preferences)
        ) * 100
    else:
        preference_score = 0

    # 5. Weighted final score
    final_score = (
        requirement_score * 0.40
        + use_case_score * 0.25
        + rating_score * 0.15
        + preference_score * 0.20
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
    preferences: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Rank products using requirements, use case,
    rating, and user preferences.
    """

    return sorted(
        products,
        key=lambda product: calculate_product_score(
            product=product,
            requirements=requirements,
            use_case=use_case,
            preferences=preferences,
        ),
        reverse=True,
    )

def find_products(
    category: str,
    budget: float,
    requirements: list[str],
    use_case: str | None = None,
    preferences: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Find and rank products using the user's shopping intent.
    """

    # Step 1: Find products in the requested category
    products = search_products(category)

    # Step 2: Remove products above the budget
    products = filter_by_budget(products, budget)

    # Step 3: Match products against requirements
    products = match_requirements(products, requirements)

    # Step 4: Filter by use case when one is specified
    if use_case:
        products = [
            product
            for product in products
            if use_case.lower() in [
               item.lower() for item in product["use_cases"]
            ]
        ]

    # Step 5: Rank products using all scoring factors
    products = rank_products(
        products=products,
        requirements=requirements,
        use_case=use_case,
        preferences=preferences,
    )
    
    return products