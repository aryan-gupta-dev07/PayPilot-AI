import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"


def get_access_token() -> str:
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("PayPal Sandbox credentials are missing.")

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v1/oauth2/token",
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        timeout=20,
    )
    response.raise_for_status()

    return response.json()["access_token"]


def create_order(amount: str, currency: str = "USD") -> dict:
    token = get_access_token()

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": amount,
                    },
                    "payee": {
                        "email_address": "sb-wrr1r53470389@business.example.com"
                    },
                }
            ],
            "payment_source": {
                "paypal": {
                    "experience_context": {
                        "user_action": "PAY_NOW",
                        "return_url": "http://localhost:8000/payment/success",
                        "cancel_url": "http://localhost:8000/payment/cancel",
                    }
                }
            },
        },
        timeout=20,
    )

    response.raise_for_status()
    return response.json()


def get_order(order_id: str) -> dict:
    """Retrieve the current status of a PayPal Sandbox order."""
    token = get_access_token()

    response = requests.get(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    response.raise_for_status()

    return response.json()


def capture_order(order_id: str) -> dict:
    """Capture an approved order, without recapturing completed orders."""
    order = get_order(order_id)
    status = order.get("status")

    if status == "COMPLETED":
        return order

    if status != "APPROVED":
        raise ValueError(
            f"Order is not approved for capture. Current status: {status}"
        )

    token = get_access_token()

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={},
        timeout=20,
    )
    response.raise_for_status()

    return response.json()