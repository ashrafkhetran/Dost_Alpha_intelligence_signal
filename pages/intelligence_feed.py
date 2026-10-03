"""Searchable, filterable intelligence stream built from live public feeds."""

import streamlit as st

from components.layout import page_heading
from components.signals import render_signal_card
from services.live import CACHE_MINUTES, get_signals, keyword_filter, refresh

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
PAGE_SIZE = 20


def render() -> None:
    """Render the live signal stream with topic, text, and impact filters."""
    page_heading("SIGNAL INTELLIGENCE", "Intelligence Feed", "Evidence-led developments, ranked by what could matter next.")
    signals, is_live, errors = get_signals()
    top = st.columns([4, 1])
    with top[0]:
        if is_live:
            st.success(
                f"Live feed: {len(signals)} stories from free public RSS sources (Google News, TechCrunch, "
                f"Hacker News, Search Engine Journal and more). Refreshes every {CACHE_MINUTES} minutes."
            )
        else:
            st.warning("Live feeds could not be reached right now, so sample stories are shown.")
    with top[1]:
        if st.button("↻ Refresh", width="stretch"):
            refresh()
            st.rerun()
    if errors:
        st.caption("Skipped sources this round: " + ", ".join(errors))

    controls = st.columns([1.3, 1.3, 1])
    with controls[0]:
        category = st.selectbox("Signal type", CATEGORIES)
    with controls[1]:
        query = st.text_input("Search signals", placeholder="Search topics, entities, sources…")
    with controls[2]:
        min_impact = st.slider("Minimum impact", min_value=0, max_value=100, value=0, step=5)

    followed = st.session_state.followed_topics
    results = [
        item for item in keyword_filter(signals)
        if (category == "All signals" or item["feed_category"] == category)
        and item["impact_score"] >= min_impact
        and (not query or query.casefold() in f"{item['title']} {item['summary']} {item['source']}".casefold())
        and (is_live or not followed or item["topic"] in followed)
    ]
    label = "LIVE SIGNALS" if is_live else "SAMPLE SIGNALS"
    st.markdown(f'<div class="result-count">{len(results)} {label}</div>', unsafe_allow_html=True)
    if not results:
        st.warning("No signals match these filters. Try lowering the impact threshold or following more topics in Settings.")
        return
    shown = st.session_state.get("feed_limit", PAGE_SIZE)
    for signal in results[:shown]:
        render_signal_card(signal, signal["id"] in st.session_state.saved_signals)
    if len(results) > shown and st.button(f"Show more ({len(results) - shown} left)"):
        st.session_state.feed_limit = shown + PAGE_SIZE
        st.rerun()
    st.caption("Scores are transparent heuristics: source quality, recency, high-impact entities, and how many other stories cover the same event.")
