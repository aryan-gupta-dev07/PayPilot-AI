import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

client_id = os.getenv("PAYPAL_CLIENT_ID")
client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

if not client_id or not client_secret:
    raise ValueError("PayPal Sandbox credentials are missing from .env")

url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

try:
    response = requests.post(
        url,
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials"},
        timeout=20,
    )

    if response.status_code == 200:
        print("SUCCESS: PayPal Sandbox connection established.")
        print("Access token received (value hidden).")
    else:
        print("FAILED: PayPal returned status:", response.status_code)
        print("Response:", response.text[:500])

except requests.RequestException as error:
    print("CONNECTION ERROR:", str(error))
