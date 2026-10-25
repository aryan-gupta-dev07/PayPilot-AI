from app.payments.paypal_client import create_order

try:
    order = create_order(amount="10.00", currency="USD")

    print("Order created successfully!")
    print("Order ID:", order.get("id"))
    print("Status:", order.get("status"))
    print("Response fields:", list(order.keys()))
    print("Payment source:", order.get("payment_source"))
    print("Purchase Units:", order.get("purchase_units"))

    purchase_units = order.get("purchase_units") or []

    if purchase_units:
        unit = purchase_units[0]
        print("Currency:", unit.get("amount", {}).get("currency_code"))
        print("Merchant ID:", unit.get("payee", {}).get("merchant_id"))

    approval_link = next(
        (
            link["href"]
            for link in order.get("links", [])
            if link.get("rel") in ("approve", "payer-action")
        ),
        None,
    )

    if approval_link:
        print("Approval link:", approval_link)
    else:
        print("Approval link received: NO")

except Exception as error:
    print("Order creation failed.")
    print("Error type:", type(error).__name__)
    print("Details:", str(error)[:500])