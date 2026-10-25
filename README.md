# PayPilot AI 🛍️

## An AI-Powered Commerce Agent for Smarter Shopping and Payments

PayPilot AI helps users discover and compare products based on their budget, requirements, use case, and personal preferences.

## Features

- **Personalized Product Recommendations:** Find products that match your budget and needs.
- **Product Suitability Scoring:** Rank recommendations using product features and user preferences.
- **Recommendation Explanations:** Understand why a product is recommended.
- **Interactive Shopping Interface:** Enter your budget, use case, required features, and preferences through Streamlit.
- **FastAPI Backend:** Provides API endpoints for application health checks and checkout order creation.
- **PayPal Sandbox Integration:** Creates test checkout orders using PayPal Sandbox APIs.

## Tech Stack

- Python
- Streamlit
- FastAPI
- Uvicorn
- Requests
- OpenAI-compatible Python SDK for Groq integration
- PayPal Sandbox

## Project Structure

```text
PayPilot-AI/
├── app/
│   ├── agent/
│   ├── core/
│   ├── payments/
│   ├── tools/
│   ├── main.py
│   └── ui.py
├── tests/
├── evaluation_report.json
├── requirements.txt
└── README.md
