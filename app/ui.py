import streamlit as st

from app.tools.products import (
    find_products,
    calculate_product_score,
    explain_recommendation,
)
from app.core.preferences import get_user_preferences


st.set_page_config(
    page_title="PayPilot AI",
    page_icon="🛍️",
    layout="wide",
)

st.title("🛍️ PayPilot AI")
st.subheader("Your AI Agent for Smarter Shopping")

st.write(
    "Find products that match your budget, needs, and preferences."
)

st.divider()

with st.form("shopping_form"):
    category = st.selectbox(
        "Product category",
        ["laptop", "phone"],
    )

    budget = st.number_input(
        "Your budget (INR)",
        min_value=1000,
        max_value=500000,
        value=50000,
        step=1000,
    )

    use_case = st.selectbox(
        "Use case",
        ["Gaming", "Study", "Programming", "Office", "Everyday use"],
    )

    requirements_text = st.text_input(
        "Required features",
        placeholder="good battery, 16GB RAM",
    )

    preferences_text = st.text_input(
        "Preferences",
        placeholder="high performance, good battery",
    )

    submitted = st.form_submit_button("Find Best Products")

if submitted:
    requirements = [
        item.strip()
        for item in requirements_text.split(",")
        if item.strip()
    ]

    preferences = get_user_preferences().copy()

    for item in preferences_text.lower().split(","):
        item = item.strip()

        if "battery" in item:
            preferences["battery_life"] = 1.0
        elif "performance" in item:
            preferences["performance"] = 1.0
        elif "rating" in item:
            preferences["rating"] = 1.0

    try:
        results = find_products(
            category=category,
            budget=budget,
            requirements=requirements,
            use_case=use_case.lower(),
            preferences=preferences,
            constraints=[],
        )

        if not results:
            st.warning(
                "No matching products found. "
                "Try changing your budget or requirements."
            )
        else:
            st.success(f"Found {len(results)} matching product(s).")
            st.header("Your Recommendations")

            for index, product in enumerate(results, start=1):
                score = calculate_product_score(
                    product,
                    requirements,
                    use_case.lower(),
                    preferences=preferences,
                )

                reasons = explain_recommendation(
                    product,
                    requirements,
                    budget,
                    use_case.lower(),
                )

                with st.container(border=True):
                    st.subheader(f"{index}. {product['name']}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Price",
                            f"₹{product['price']:,.0f}",
                        )

                    with col2:
                        st.metric(
                            "Suitability Score",
                            f"{score * 100:.2f}/100",
                        )

                    st.write(f"**Rating:** {product['rating']}/5")
                    st.write("**Why recommended?**")

                    for reason in reasons:
                        st.write(f"- {reason}")

    except Exception as error:
        st.error(
            "Could not generate recommendations. "
            "Please check the application logs."
        )
        print(f"Recommendation error: {error}")

st.divider()
st.caption("PayPilot AI | AI Commerce Agent")
