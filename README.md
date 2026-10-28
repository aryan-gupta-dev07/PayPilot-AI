🛍️ PayPilot AI

An AI-powered shopping assistant for smarter purchasing decisions.

PayPilot AI recommends and compares products based on users' budgets, requirements, use cases, and personal preferences.

✨ Features

- 🤖 AI-powered product recommendations using Groq API
- 📊 Product ranking and scoring
- 💡 Recommendation explanations
- ⚖️ Product comparison, pros, and cons
- 🖥️ Interactive Streamlit interface
- ⚙️ FastAPI backend
- 💳 PayPal Sandbox checkout and payment capture
- 🧪 Automated testing with Pytest

🛠️ Tech Stack

Python · Streamlit · FastAPI · Groq API · PayPal Sandbox · Requests · Pytest

🚀 Installation

python -m pip install -r requirements.txt 
Clone the repository and install dependencies:

git clone 
cd PayPilot-AI
python -m pip install -r requirements.txt

🔐 Environment Setup

Create a ".env" file in the project root:

GROQ_API_KEY=your_groq_api_key
PAYPAL_CLIENT_ID=your_paypal_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_paypal_sandbox_client_secret

Use your own credentials and never publish API keys or secrets.

▶️ Run the Application

Streamlit interface:

python -m streamlit run app/ui.py

FastAPI backend (in a separate terminal):

python -m uvicorn app.payments.api:app --reload --port 8000

API documentation: "http://localhost:8000/docs"

Health check: "http://localhost:8000/health"

💳 PayPal Sandbox

- Creates checkout orders and generates approval links.
- Supports order capture and status verification.
- A Sandbox test order returned "COMPLETED".

Note: This integration is for Sandbox testing only. Production payments are not configured or verified.

🧪 Testing

Run the automated test suite:

python -m pytest -q

All tests passed in the latest reported test run.

📌 Project Status

The shopping assistant, product recommendation flow, FastAPI backend, and PayPal Sandbox integration have been implemented. The checkout capture flow was tested successfully in Sandbox.

---

Built with Python, Streamlit, FastAPI, Groq, and PayPal Sandbox.
