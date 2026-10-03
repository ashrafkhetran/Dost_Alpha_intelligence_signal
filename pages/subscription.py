"""Subscription tiers and checkout placeholder."""

import streamlit as st

from components.layout import page_heading

PLANS = [
    ("FREE", "$0", "Get oriented.", ["5 reports / month", "Basic signal summaries", "Limited categories"]),
    ("PRO", "$9", "See the patterns.", ["Unlimited reports", "Advanced filters", "Trend analysis", "PDF export", "Saved reports"]),
    ("ALPHA", "$29", "Act with conviction.", ["AI Analyst mode", "Executive briefings", "Opportunity detection", "Deep research", "Daily intelligence", "Priority processing"]),
]


def render() -> None:
    """Show product tiers without simulating payment completion."""
    page_heading("PLANS & ACCESS", "Choose your signal advantage", "Start with clarity. Upgrade when intelligence becomes mission-critical.")
    st.info("Checkout is not connected. No payment method will be collected in this prototype.")
    columns = st.columns(3)
    for column, (name, price, description, features) in zip(columns, PLANS):
        with column:
            featured = name == "ALPHA"
            st.markdown(
                f'<div class="plan-card {"plan-featured" if featured else ""}">'
                f'<div class="plan-name">{name}</div><div class="plan-price">{price}'
                f'<span>/ month</span></div><p>{description}</p><div class="plan-divider"></div>'
                + "".join(f'<div class="plan-feature"><span>✓</span>{feature}</div>' for feature in features)
                + "</div>",
                unsafe_allow_html=True,
            )
            if st.button("Current plan" if name == "FREE" else f"Explore {name}", key=f"plan-{name}", width="stretch", disabled=name == "FREE"):
                st.warning("Stripe Checkout is a planned integration; this prototype does not create subscriptions.")
