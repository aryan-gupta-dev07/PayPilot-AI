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
    """Create a standardized product object."""

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
        features=["16GB RAM", "512GB SSD", "Dedicated GPU", "good battery"],
        use_cases=["gaming", "performance"],
    ),
    create_product(
        name="Gaming Laptop B",
        category="laptop",
        price=52000,
        currency="INR",
        rating=4.5,
        features=["16GB RAM", "1TB SSD", "Dedicated GPU", "excellent battery"],
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
    """Search products by category."""

    return [
        product
        for product in PRODUCTS
        if product["category"].lower() == category.lower()
    ]


def _matches_requirement(
    product: dict[str, Any],
    requirement: str,
) -> bool:
    """Check whether a product satisfies a requirement."""

    requirement_text = " ".join(requirement.lower().split())

    if not requirement_text:
        return False

    product_name = product["name"].lower()

    features = [
        " ".join(feature.lower().split())
        for feature in product["features"]
    ]

    use_cases = [
        " ".join(use_case.lower().split())
        for use_case in product.get("use_cases", [])
    ]

    # Match battery-related wording against actual product features.
    if "battery" in requirement_text:
        return any(
            "battery" in feature
            for feature in features
        )

    # Storage requirements must match a complete feature.
    if "ssd" in requirement_text:
        return requirement_text in features

    # Match the complete phrase first.
    if (
        requirement_text in product_name
        or requirement_text in features
        or requirement_text in use_cases
    ):
        return True

    # Preserve keyword matching for other requirements.
    product_text = " ".join(
        [product_name, *features, *use_cases]
    )

    keywords = requirement_text.split()

    return any(
        keyword in product_text
        for keyword in keywords
    )


def filter_by_budget(
    products: list[dict[str, Any]],
    budget: float,
) -> list[dict[str, Any]]:
    """Return products within the user's budget."""

    if budget <= 0:
        raise ValueError("Budget must be greater than zero.")

    return [
        product
        for product in products
        if product["price"] <= budget
    ]


def match_requirements(
    products: list[dict[str, Any]],
    requirements: list[str],
) -> list[dict[str, Any]]:
    """Return products matching at least one requirement."""

    if not requirements:
        return products.copy()

    return [
        product
        for product in products
        if any(
            _matches_requirement(product, requirement)
            for requirement in requirements
        )
    ]


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

    matched_requirements = sum(
        1
        for requirement in requirements
        if _matches_requirement(product, requirement)
    )

    requirement_score = (
        matched_requirements / len(requirements)
        if requirements
        else 0.0
    )

    supported_use_cases = [
        item.lower()
        for item in product["use_cases"]
    ]

    use_case_score = (
        1.0
        if use_case
        and use_case.lower() in supported_use_cases
        else 0.0
    )

    rating_score = product["rating"] / 5.0

    preference_score = 0.0

    # Support list-based preferences as well as weighted dictionaries.
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

                    if preference == "battery_life":
                        match_score = (
                            1.0
                            if any(
                                "battery" in feature.lower()
                                for feature in product["features"]
                            )
                            else 0.0
                        )

                    elif preference == "performance":
                        match_score = (
                            1.0
                            if keyword and keyword in product_text
                            else 0.0
                        )

                    else:
                        match_score = (
                            1.0
                            if preference in product_text
                            else 0.0
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

    # 1. Explain the budget match.
    if product["price"] <= budget:
        reasons.append(
            f"Price ₹{product['price']} is within "
            f"your ₹{budget} budget."
        )
    else:
        reasons.append(
            f"Price ₹{product['price']} exceeds "
            f"your ₹{budget} budget."
        )

    # 2. Use the shared requirement-matching function.
    matched_requirements = [
        requirement
        for requirement in requirements
        if _matches_requirement(product, requirement)
    ]

    unmatched_requirements = [
        requirement
        for requirement in requirements
        if not _matches_requirement(product, requirement)
    ]

    if matched_requirements:
        reasons.append(
            "Matching requirements: "
            + ", ".join(matched_requirements)
            + "."
        )

    if unmatched_requirements:
        reasons.append(
            "Requirements not found in product data: "
            + ", ".join(unmatched_requirements)
            + "."
        )

    # 3. Check use-case compatibility.
    supported_use_cases = [
        item.strip().lower()
        for item in product["use_cases"]
    ]

    use_case_supported = (
        not use_case
        or use_case.strip().lower() in supported_use_cases
    )

    # 4. Determine the recommendation status.
    if product["price"] > budget or not use_case_supported:
        match_status = "No match"
    elif not requirements or len(matched_requirements) == len(requirements):
        match_status = "Full match"
    elif matched_requirements:
        match_status = "Partial match"
    else:
        match_status = "No match"

    reasons.append(
        f"Recommendation status: {match_status}."
    )

    # 5. Explain the use-case match.
    if use_case:
        if use_case_supported:
            reasons.append(
                f"Suitable use case: {use_case}."
            )
        else:
            reasons.append(
                f"Use case '{use_case}' is not listed "
                "for this product."
            )

    # 6. Report the available dataset rating.
    reasons.append(
        f"Customer rating in dataset: "
        f"{product['rating']}/5."
    )

    return reasons


def compare_products(
    product_a: dict[str, Any],
    product_b: dict[str, Any],
) -> dict[str, Any]:
    """Compare two products using their available data."""

    price_a = product_a["price"]
    price_b = product_b["price"]

    features_a = {
        feature.lower()
        for feature in product_a["features"]
    }

    features_b = {
        feature.lower()
        for feature in product_b["features"]
    }

    shared_features = sorted(features_a & features_b)
    only_a = sorted(features_a - features_b)
    only_b = sorted(features_b - features_a)

    if price_a < price_b:
        cheaper_product = product_a["name"]
    elif price_b < price_a:
        cheaper_product = product_b["name"]
    else:
        cheaper_product = "Same price"

    return {
        "product_a": product_a["name"],
        "product_b": product_b["name"],
        "price_difference": abs(price_a - price_b),
        "cheaper_product": cheaper_product,
        "shared_features": shared_features,
        "unique_features_a": only_a,
        "unique_features_b": only_b,
    }


def get_product_pros_and_cons(
    product: dict[str, Any],
    budget: float,
    requirements: list[str],
) -> dict[str, list[str]]:
    """Generate pros and cons using available product data."""

    pros = []
    cons = []

    if product["price"] <= budget:
        pros.append("Within your budget.")
    else:
        cons.append("Exceeds your budget.")

    # Use the same matching rules as scoring and explanations.
    for requirement in requirements:
        if _matches_requirement(product, requirement):
            pros.append(
                f"Matches requirement: {requirement}."
            )
        else:
            cons.append(
                f"Requirement not found: {requirement}."
            )

    if product["rating"] >= 4.5:
        pros.append("High customer rating in the dataset.")
    elif product["rating"] < 4.0:
        cons.append("Low customer rating in the dataset.")

    if not pros:
        pros.append(
            "No specific advantages identified from the supplied data."
        )

    if not cons:
        cons.append(
            "No specific disadvantages identified from the supplied data."
        )

    return {
        "pros": pros,
        "cons": cons,
    }


def get_comparison_summary(
    product_a: dict[str, Any],
    product_b: dict[str, Any],
) -> str:
    """Summarize the main differences between two products."""

    price_a = product_a["price"]
    price_b = product_b["price"]

    rating_a = product_a["rating"]
    rating_b = product_b["rating"]

    if price_a < price_b:
        price_summary = (
            f"{product_a['name']} is ₹{price_b - price_a} cheaper."
        )
    elif price_b < price_a:
        price_summary = (
            f"{product_b['name']} is ₹{price_a - price_b} cheaper."
        )
    else:
        price_summary = "Both products have the same price."

    if rating_a > rating_b:
        rating_summary = (
            f"{product_a['name']} has the higher dataset rating."
        )
    elif rating_b > rating_a:
        rating_summary = (
            f"{product_b['name']} has the higher dataset rating."
        )
    else:
        rating_summary = "Both products have the same dataset rating."

    return f"{price_summary} {rating_summary}"


def rank_products(
    products: list[dict[str, Any]],
    requirements: list[str],
    use_case: str | None = None,
    preferences: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    """Rank products by score, highest first."""

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
    constraints: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Find and rank products using the user's shopping intent."""

    products = search_products(category)

    # Step 1: Enforce the budget limit.
    products = filter_by_budget(
        products,
        budget,
    )

    # Enforce explicitly supported constraints
    for constraint in constraints or []:
        constraint_text = constraint.strip().lower()

        if constraint_text.startswith("must have "):
            requirement = constraint_text[len("must have "):].strip()

            products = [
                product
                for product in products
                if _matches_requirement(product, requirement)
            ]

        elif constraint_text.startswith("avoid "):
            unwanted = constraint_text[len("avoid "):].strip()

            products = [
                product
                for product in products
                if not _matches_requirement(product, unwanted)
            ]


    # Step 2: Enforce all specified requirements.
    products = [
        product
        for product in products
        if check_product_constraints(
            product=product,
            budget=budget,
            requirements=requirements,
            use_case=use_case,
        )["eligible"]
    ]

    # Step 3: Rank only eligible products.
    products = rank_products(
        products=products,
        requirements=requirements,
        use_case=use_case,
        preferences=preferences,
    )

    return products

def test_performance_preference_is_passed_to_ranking():
    results = find_products(
        category="laptop",
        budget=50000,
        requirements=["gaming"],
        use_case="gaming",
        preferences={"performance": 1.0},
    )

    assert results
    assert all(
        product["price"] <= 50000
        for product in results
    )

def check_product_constraints(
    product: dict[str, Any],
    budget: float,
    requirements: list[str],
    use_case: str | None = None,
) -> dict[str, Any]:
    """Check whether a product satisfies the user's constraints."""

    matched_requirements = [
        requirement
        for requirement in requirements
        if _matches_requirement(product, requirement)
    ]

    missing_requirements = [
        requirement
        for requirement in requirements
        if not _matches_requirement(product, requirement)
    ]

    budget_passed = product["price"] <= budget

    supported_use_cases = [
        item.strip().lower()
        for item in product.get("use_cases", [])
    ]

    use_case_passed = (
        not use_case
        or use_case.strip().lower() in supported_use_cases
    )

    eligible = (
        budget_passed
        and not missing_requirements
        and use_case_passed
    )

    return {
        "product": product["name"],
        "eligible": eligible,
        "budget_passed": budget_passed,
        "matched_requirements": matched_requirements,
        "missing_requirements": missing_requirements,
        "use_case_passed": use_case_passed,
    }

def generate_evidence_card(
    product: dict[str, Any],
    budget: float,
    requirements: list[str],
    use_case: str | None = None,
) -> dict[str, Any]:
    """Generate an evidence card using available product data."""

    check = check_product_constraints(
        product=product,
        budget=budget,
        requirements=requirements,
        use_case=use_case,
    )

    evidence = [
        {
            "check": "Budget",
            "status": "PASS" if check["budget_passed"] else "FAIL",
            "details": (
                f"Product price: {product['currency']} "
                f"{product['price']}; "
                f"budget: {product['currency']} {budget}"
            ),
        }
    ]

    for requirement in check["matched_requirements"]:
        evidence.append({
            "check": f"Requirement: {requirement}",
            "status": "MATCH",
            "details": "Matching feature found in product data.",
        })

    for requirement in check["missing_requirements"]:
        evidence.append({
            "check": f"Requirement: {requirement}",
            "status": "MISSING",
            "details": "Matching feature not found in product data.",
        })

    if use_case:
        evidence.append({
            "check": f"Use case: {use_case}",
            "status": (
                "PASS" if check["use_case_passed"] else "FAIL"
            ),
            "details": (
                "Supported by product data."
                if check["use_case_passed"]
                else "Not listed in supported product use cases."
            ),
        })

    return {
        "product": product["name"],
        "eligible": check["eligible"],
        "evidence_source": "Local sample product dataset",
        "evidence": evidence,
    }
