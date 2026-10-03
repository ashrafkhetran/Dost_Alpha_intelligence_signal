"""Admin integration readiness panel."""

import streamlit as st

from components.layout import page_heading


def render() -> None:
    """Explain backend integration readiness without inventing admin metrics."""
    page_heading("OPERATIONS", "Admin Console", "Operational surfaces for sources, models, users, and revenue.")
    st.warning("Admin operations are not wired to a backend. This panel is a build-readiness view, not a live admin system.")
    integrations = [
        ("RSS source registry", "Not connected", "Add authenticated source management and polling jobs."),
        ("AI model routing", "Not connected", "Configure provider adapters and per-model budgets."),
        ("User and access management", "Not connected", "Add OAuth/email auth and role-based access control."),
        ("Stripe subscriptions", "Not connected", "Create signed webhook handling and entitlement sync."),
        ("Revenue analytics", "Not connected", "Build from verified Stripe events, never sample figures."),
    ]
    for name, state, detail in integrations:
        st.markdown(f'<div class="admin-row"><div><strong>{name}</strong><p>{detail}</p></div>'
                    f'<span class="admin-status">{state}</span></div>', unsafe_allow_html=True)
