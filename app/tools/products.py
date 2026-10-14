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
    """Return products matching the requested requirements."""

    if not requirements:
        return products.copy()

    matched_products = []

    battery_terms = {
        "battery",
        "long battery life",
        "good battery",
        "excellent battery",
        "long battery",
    }

    for product in products:
        product_name = product["name"].lower()
        features = [
            feature.lower()
            for feature in product["features"]
        ]
        use_cases = [
            use_case.lower()
            for use_case in product["use_cases"]
        ]

        product_text = " ".join(
            [product_name, *features, *use_cases]
        )

        matched = False

        for requirement in requirements:
            requirement_text = requirement.lower().strip()

            # Match storage specifications against features only.
            if "ssd" in requirement_text:
                normalized_requirement = " ".join(
                    requirement_text.split()
                )
                normalized_features = [
                    " ".join(feature.split())
                    for feature in features
                ]

                if normalized_requirement in normalized_features:
                    matched = True
                    break

                continue

            # Handle known battery wording variations.
            if requirement_text in battery_terms:
                if any(
                    "battery" in feature
                    for feature in features
                ):
                    matched = True
                    break

                continue

            # Exact phrase matching across individual fields.
            if (
                requirement_text in product_name
                or requirement_text in features
                or requirement_text in use_cases
            ):
                matched = True
                break

            # Retain keyword matching for other requirements.
            keywords = requirement_text.split()

            if any(
                keyword in product_text
                for keyword in keywords
            ):
                matched = True
                break

        if matched:
            matched_products.append(product)

    return matched_products    
    
def calculate_product_score(
    product: dict[str, Any],
    requirements: list[str],
    use_case: str | None = None,
    preferences: dict[str, float] | None = None,
) -> float:
    """Calculate a recommendation score for a product."""

    product_text = " ".join(
        [
            product["name"],
            *product["features"],
            *product["use_cases"],
        ]
    ).lower()

    requirement_score = (
        sum(
            1 for requirement in requirements
            if requirement.lower().strip() in product_text
        ) / len(requirements)
        if requirements else 0.0
    )

    use_case_score = (
        1.0
        if use_case and use_case.lower() in [
            item.lower() for item in product["use_cases"]
        ]
        else 0.0
    )

    rating_score = product["rating"] / 5.0

    preference_score = 0.0

    if isinstance(preferences, list):
        converted_preferences = {}

        for item in preferences:
            item = item.lower().strip()

            if "battery" in item:
                converted_preferences["battery_life"] = 1.0
            elif "performance" in item:
                converted_preferences["performance"] = 1.0
            elif "rating" in item or "review" in item:
                converted_preferences["rating"] = 1.0
            else:
                converted_preferences[item] = 1.0

        preferences = converted_preferences

    if preferences:
        preference_matches = {
            "battery_life": "battery",
            "performance": "performance",
            "rating": None,
        }

        total_priority = sum(preferences.values())

        if total_priority > 0:
            for preference, priority in preferences.items():
                if preference == "rating":
                    match_score = product["rating"] / 5.0
                else:
                    keyword = preference_matches.get(preference)

                    if preference in ("battery_life", "performance"):
                        match_score = (
                            1.0
                            if keyword and keyword in product_text
                            else 0.0
                        )
                    else:
                        match_score = (
                            1.0 if preference in product_text else 0.0
                        )

                preference_score += (
                    priority / total_priority
                ) * match_score
                
                
    if preferences:
        score = (
            0.40 * requirement_score
            + 0.25 * use_case_score
            + 0.15 * rating_score
            + 0.20 * preference_score
        )
    else:
        score = (
            0.50 * requirement_score
            + 0.3125 * use_case_score
            + 0.1875 * rating_score
        )

    return round(score, 4)

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
    preferences: dict[str, float] | None = None,
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
    preferences: dict[str, float] | None = None,
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