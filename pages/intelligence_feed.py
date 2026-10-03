"""Searchable, filterable intelligence stream."""

import streamlit as st

from components.layout import page_heading
from components.signals import render_signal_card
from services.demo_data import SIGNALS

CATEGORIES = [
    "All signals",
    "Critical Signals",
    "AI Breakthroughs",
    "Market Movers",
    "Corporate Intelligence",
    "Startup Watch",
    "Emerging Trends",
    "Hidden Opportunities",
]


def render() -> None:
    """Render the sample signal stream with topic, text, and impact filters."""
    page_heading("SIGNAL INTELLIGENCE", "Intelligence Feed", "Evidence-led developments, ranked by what could matter next.")
    st.info("Demo feed: sample stories only. Connect RSS sources to ingest live intelligence.")
    controls = st.columns([1.3, 1.3, 1])
    with controls[0]:
        category = st.selectbox("Signal type", CATEGORIES)
    with controls[1]:
        query = st.text_input("Search signals", placeholder="Search topics, entities, sources…")
    with controls[2]:
        min_impact = st.slider("Minimum impact", min_value=0, max_value=100, value=0, step=5)

    followed = st.session_state.followed_topics
    results = [
        item for item in SIGNALS
        if (category == "All signals" or item["feed_category"] == category)
        and item["impact_score"] >= min_impact
        and (not query or query.casefold() in " ".join(str(value) for value in item.values()).casefold())
        and (not followed or item["topic"] in followed)
    ]
    st.markdown(f'<div class="result-count">{len(results)} SAMPLE SIGNALS</div>', unsafe_allow_html=True)
    if not results:
        st.warning("No sample signals match these filters. Try lowering the impact threshold or following more topics.")
    for signal in results:
        render_signal_card(signal, signal["id"] in st.session_state.saved_signals)
