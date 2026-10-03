"""DOST ALPHA Streamlit entry point."""

from pathlib import Path

import streamlit as st

from components.layout import render_sidebar
from pages import (
    admin,
    ai_analyst,
    briefings,
    dashboard,
    intelligence_feed,
    saved_intelligence,
    settings,
    subscription,
    trend_radar,
)

ROOT = Path(__file__).parent

st.set_page_config(
    page_title="DOST ALPHA — Intelligence Terminal",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"<style>{(ROOT / 'assets' / 'styles.css').read_text(encoding='utf-8')}</style>",
    unsafe_allow_html=True,
)

if "saved_signals" not in st.session_state:
    st.session_state.saved_signals = []
if "followed_topics" not in st.session_state:
    st.session_state.followed_topics = ["AI", "Startups", "Technology"]
if "show_dashboard_brief" not in st.session_state:
    st.session_state.show_dashboard_brief = False

page = render_sidebar()

pages = {
    "Overview": dashboard.render,
    "Intelligence Feed": intelligence_feed.render,
    "AI Analyst": ai_analyst.render,
    "Trend Radar": trend_radar.render,
    "Executive Briefings": briefings.render,
    "Saved Intelligence": saved_intelligence.render,
    "Subscription": subscription.render,
    "Settings": settings.render,
    "Admin Console": admin.render,
}
pages[page]()
