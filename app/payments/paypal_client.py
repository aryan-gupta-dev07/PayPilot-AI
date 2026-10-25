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
                    }
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

    if not response.ok:
        print("PayPal error response:", response.text)

    response.raise_for_status()
    return response.json()
