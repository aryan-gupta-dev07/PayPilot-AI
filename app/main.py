from tools.products import find_products

results = find_products(
    category="laptop",
    budget=50000,
    requirements=["gaming", "battery"],
)

print("Final recommendations:")

for index, product in enumerate(results, start=1):
    print(
        index,
        product["name"],
        "- ₹" + str(product["price"]),
        "- Rating:",
        product["rating"],
    )