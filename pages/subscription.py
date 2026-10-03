"""Plans: free beta now, optional hosted payment links later (no Stripe or wire account needed)."""

import streamlit as st

from components.layout import page_heading
from services.analyst import _secret

PLANS = [
    ("FREE", "$0", "Get oriented.", ["Live intelligence feed", "Basic signal summaries", "Session bookmarks"]),
    ("PRO", "$9", "See the patterns.", ["Unlimited AI briefs", "Advanced filters", "Trend analysis", "PDF export", "Saved reports"]),
    ("ALPHA", "$29", "Act with conviction.", ["AI Analyst mode", "Executive briefings", "Opportunity detection", "Deep research", "Daily intelligence", "Priority processing"]),
]


def render() -> None:
    """Show tiers. Everything is open during beta; paid buttons appear only when a payment link is configured."""
    page_heading("PLANS & ACCESS", "Choose your signal advantage", "Start with clarity. Upgrade when intelligence becomes mission-critical.")
    contact = _secret("CONTACT_EMAIL")
    any_link = any(_secret(f"PAYMENT_LINK_{name}") for name, *_ in PLANS)
    if not any_link:
        st.success("Free beta: every feature, including AI Analyst, briefings and PDF export, is unlocked for now. No card needed.")
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
            link = _secret(f"PAYMENT_LINK_{name}")
            if name == "FREE":
                st.button("Current plan", key="plan-FREE", width="stretch", disabled=True)
            elif link:
                st.link_button(f"Get {name}", link, width="stretch", type="primary" if featured else "secondary")
            elif contact:
                st.link_button(f"Join {name} waitlist", f"mailto:{contact}?subject=DOST%20ALPHA%20{name}%20waitlist", width="stretch")
            else:
                st.button(f"{name} · included in beta", key=f"plan-{name}", width="stretch", disabled=True)
