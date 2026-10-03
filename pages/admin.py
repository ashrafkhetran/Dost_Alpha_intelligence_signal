"""Admin integration readiness panel."""

import streamlit as st

from components.layout import page_heading
from services.analyst import has_openrouter_api_key


def render() -> None:
    """Explain backend integration readiness without inventing admin metrics."""
    page_heading("OPERATIONS", "Admin Console", "Operational surfaces for sources, models, users, and revenue.")
    st.info("Integration status for this deployment.")
    integrations = [
        ("RSS source registry", "Live", "Free public feeds in services/feeds.py (Google News, TechCrunch, HN, SEJ...). Edit SOURCES to add more."),
        ("AI model routing", "Live" if has_openrouter_api_key() else "Needs key", "OpenRouter free models with automatic fallback. Set OPENROUTER_API_KEY in secrets."),
        ("User and access management", "Not connected", "Add OAuth/email auth and role-based access control."),
        ("Payments", "Optional", "Free beta. Add a PAYMENT_LINK_PRO / PAYMENT_LINK_ALPHA secret (Payoneer, Gumroad, Lemon Squeezy) when ready."),
        ("Revenue analytics", "Not connected", "Build from verified Stripe events, never sample figures."),
    ]
    for name, state, detail in integrations:
        st.markdown(f'<div class="admin-row"><div><strong>{name}</strong><p>{detail}</p></div>'
                    f'<span class="admin-status">{state}</span></div>', unsafe_allow_html=True)
