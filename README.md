# PayPilot AI

An AI-powered shopping assistant that recommends and compares products based on budget, requirements, use case, and personal preferences.

## Features

- Personalized product recommendations
- Product ranking and scoring
- Recommendation explanations
- Product comparison
- Product pros and cons
- Interactive Streamlit interface
- FastAPI backend
- PayPal Sandbox integration

## Tech Stack

- Python
- Streamlit
- FastAPI
- Groq API
- PayPal Sandbox
- Pytest

## Installation

Install the required dependencies:

    python -m pip install -r requirements.txt

## Environment Setup

Create a `.env` file in the project root:

    GROQ_API_KEY=your_groq_api_key
    PAYPAL_CLIENT_ID=your_paypal_sandbox_client_id
    PAYPAL_CLIENT_SECRET=your_paypal_sandbox_client_secret

Replace the placeholders with your own credentials. Never share your API keys or secrets.

## Run the Application

Start the Streamlit interface:

    python -m streamlit run app/ui.py

Start the FastAPI backend in a separate terminal:

    uvicorn app.payments.api:app --reload --port 8000

API documentation: http://localhost:8000/docs

## Run Tests

    python -m pytest -q

## Payment Status

PayPal Sandbox order creation is implemented. Checkout completion and payment capture have not yet been verified. Real payments are not supported by the current implementation.

## Project Status

The Streamlit interface and product recommendation flow have been tested. All automated tests pass in the development environment.