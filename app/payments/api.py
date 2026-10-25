from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.payments.paypal_client import create_order


app = FastAPI(title="PayPilot AI Checkout")


class CheckoutRequest(BaseModel):
    amount: str = Field(pattern=r"^\d+\.\d{2}$")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/create-order")
def create_checkout_order(request: CheckoutRequest):
    try:
        order = create_order(
            amount=request.amount,
            currency="USD",
        )

        approval_url = next(
            (
                link["href"]
                for link in order.get("links", [])
                if link.get("rel") in ("approve", "payer-action")
            ),
            None,
        )

        if not approval_url:
            raise HTTPException(
                status_code=502,
                detail="PayPal approval link was not returned.",
            )

        return {
            "order_id": order["id"],
            "status": order["status"],
            "approval_url": approval_url,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Could not create PayPal Sandbox order.",
        )


@app.get("/payment/success")
def payment_success():
    return {
        "message": "Returned from PayPal Sandbox.",
        "note": "Payment has not been verified or captured yet.",
    }


@app.get("/payment/cancel")
def payment_cancel():
    return {
        "message": "PayPal checkout was cancelled.",
    }