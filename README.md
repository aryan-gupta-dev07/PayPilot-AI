PayPilot AI – Intelligent AI Commerce Agent

Overview

PayPilot AI is an AI-powered commerce agent designed to make online shopping more intelligent, personalized, and efficient.

It uses Large Language Models (LLMs), structured product data, and specialized tools to understand user requirements, discover relevant products, compare alternatives, and generate personalized product recommendations.

The system focuses on helping users make informed purchasing decisions through conversational AI and explainable product rankings.

Key Features

- Natural Language Understanding: Understands shopping requirements expressed in everyday language.
- AI-Powered Product Discovery: Identifies products relevant to user requirements.
- Intelligent Product Comparison: Compares product alternatives and highlights their advantages and disadvantages.
- Personalized Recommendations: Uses user preferences to improve product rankings.
- Dynamic Preference Updates: Adjusts recommendations when user preferences change.
- Explainable Recommendations: Provides reasons behind product recommendations.
- Conversational Shopping Experience: Supports interactive shopping through an AI-powered interface.
- PayPal Sandbox Integration: Supports testing of payment-related workflows in the PayPal Sandbox environment.

Technology Stack

Component| Technology
Programming Language| Python
AI / LLM Integration| Groq API
LLM Interface| OpenAI-compatible API
Backend| FastAPI
Frontend| Streamlit
Payment Integration| PayPal Sandbox
Environment Configuration| python-dotenv
HTTP Requests| Requests

Project Architecture

PayPilot-AI/
│
├── app/
│   ├── agent/
│   ├── core/
│   ├── payments/
│   ├── tools/
│   ├── main.py
│   ├── ui.py
│   └── __init__.py
│
├── tests/
│
├── evaluation_report.json
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore

Main Components

- "app/agent/": AI agent planning and LLM-related functionality.
- "app/core/": Core application functionality.
- "app/payments/": Payment-related integration.
- "app/tools/": Product and supporting tools.
- "app/main.py": CLI application entry point.
- "app/payments/api.py": FastAPI backend entry point.
- "app/ui.py": Streamlit user interface.
- "tests/": Automated project tests.
- "evaluation_report.json": Project evaluation results.

Prerequisites

Before running the project, ensure that you have:

- Python installed.
- Git installed.
- A Groq API key.
- PayPal Sandbox credentials for payment-related testing.

Installation and Setup

1. Clone the Repository

git clone https://github.com/aryan-gupta-dev07/PayPilot-AI.git

2. Navigate to the Project Directory

cd PayPilot-AI

3. Create a Virtual Environment

python -m venv .venv

4. Activate the Virtual Environment

Windows:

.venv\Scripts\activate

Linux / macOS:

source .venv/bin/activate

5. Install Dependencies

pip install -r requirements.txt

Environment Configuration

Create a ".env" file in the project root directory.

Add the following environment variables:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_configured_groq_model

PAYPAL_CLIENT_ID=your_paypal_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_paypal_sandbox_client_secret

Replace the placeholder values with your own credentials.

Important:

- Never upload your actual API keys or credentials to GitHub.
- Use PayPal Sandbox credentials for testing.
- Keep the ".env" file private.

Running the Application

Start the Streamlit Application

From the project root directory, with the virtual environment activated, execute:

.venv\Scripts\python.exe -m streamlit run app\ui.py

Streamlit will display a local application URL in the terminal.

Open that URL in your browser to interact with PayPilot AI.

Backend

The project also includes a FastAPI backend in "app/payments/api.py".

.venv\Scripts\python.exe -m uvicorn app.payments.api:app --reload

The backend can be accessed through its configured API endpoints when running with the project's supported server configuration.

Testing

The project includes automated tests in the "tests/" directory.

To run the test suite, install pytest if it is not already available:

pip install pytest

Then execute:

pytest -q

PayPal Sandbox Integration

PayPilot AI includes PayPal Sandbox integration for testing payment-related functionality.

The Sandbox environment allows developers and evaluators to test payment workflows without processing real-money transactions.

Use valid Sandbox credentials when testing payment functionality.

Security and Privacy

- API credentials are configured through environment variables.
- Sensitive credentials should never be committed to version control.
- Payment testing should use the PayPal Sandbox environment.
- The application should be configured with appropriate credentials before testing integrations.

Project Evaluation

The project includes an evaluation report and automated tests to assess its functionality.

The evaluation focuses on areas such as:

- Product discovery.
- Product ranking.
- Recommendation relevance.
- Preference-aware behavior.
- Handling of unsupported shopping requests.

Refer to "evaluation_report.json" for the available evaluation results.

Future Improvements

- Expanded product catalog integrations.
- More advanced recommendation strategies.
- Improved personalization.
- Additional commerce tool integrations.
- Enhanced evaluation across diverse shopping scenarios.

License

This project is licensed under the MIT License.

See the "LICENSE" file for details.

Repository

GitHub: https://github.com/aryan-gupta-dev07/PayPilot-AI
