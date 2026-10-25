from app.payments.paypal_client import create_order

try:
    order = create_order(amount="10.00", currency="USD")

    print("Order created successfully!")
    print("Order ID:", order.get("id"))
    print("Status:", order.get("status"))

    approval_link = next(
        (
            link["href"]
            for link in order.get("links", [])
            if link.get("rel") == "approve"
        ),
        None,
    )

    if approval_link:
        print("Approval link received: YES")
    else:
        print("Approval link received: NO")

except Exception as error:
    print("Order creation failed.")
    print("Error type:", type(error).__name__)
    print("Details:", str(error)[:500])
