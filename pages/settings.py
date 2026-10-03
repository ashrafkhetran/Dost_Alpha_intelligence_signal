"""Personalization preferences."""

import streamlit as st

from components.layout import page_heading

TOPICS = ["AI", "SEO", "Business", "Finance", "Healthcare", "Marketing", "Startups", "Technology", "Cybersecurity"]


def render() -> None:
    """Edit demo-session topic and notification preferences."""
    page_heading("PERSONALIZATION", "Settings", "Tune the signal stream to your work and interests.")
    st.info("Preferences are stored only in this Streamlit session. Sign-in and persistent profiles are not configured.")
    with st.form("preferences"):
        topics = st.multiselect("Topics to follow", TOPICS, default=st.session_state.followed_topics)
        keywords = st.text_input("Watch keywords", placeholder="e.g. inference, agentic workflows, zero-click")
        digest = st.selectbox("Email digest", ["Off", "Daily", "Weekly"])
        submitted = st.form_submit_button("Save preferences", type="primary")
    if submitted:
        st.session_state.followed_topics = topics
        st.session_state.watch_keywords = keywords
        st.session_state.digest_frequency = digest
        st.success("Preferences saved for this session.")
