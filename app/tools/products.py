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
    Return products that match at least one user requirement.
    """

    matched_products = []

    for product in products:
        product_text = (
            product["name"] + " "
            + " ".join(product["features"]) + " "
            + " ".join(product["use_cases"])
        ).lower()

        if any(requirement.lower() in product_text for requirement in requirements):
            matched_products.append(product)

    return matched_products

def rank_products(
    products: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Rank products using rating and requirement match information.
    """

    return sorted(
        products,
        key=lambda product: product["rating"],
        reverse=True,
    )
    
def find_products(
    category: str,
    budget: float,
    requirements: list[str],
) -> list[dict[str, Any]]:
    """
    Find and rank products based on category, budget, and requirements.
    """

    products = search_products(category)

    products = filter_by_budget(products, budget)

    products = match_requirements(products, requirements)

    products = rank_products(products)

    return products            