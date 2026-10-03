"""Reusable signal-card rendering."""

import html

import streamlit as st

from services.scoring import classify_outlook


def render_signal_card(signal: dict, is_saved: bool = False) -> None:
    """Render one sample intelligence signal and its evidence scores."""
    title = html.escape(signal["title"])
    summary = html.escape(signal["summary"])
    category = html.escape(signal["category"])
    source = html.escape(signal["source"])
    velocity = html.escape(signal["velocity"])
    sentiment = html.escape(signal["sentiment"])
    impact_label = html.escape(signal["business_impact"])
    outlook = classify_outlook(signal["impact_score"], signal["sentiment"])
    outlook_class = outlook.lower()
    safe_id = html.escape(signal["id"])
    velocity_class = signal["velocity"].lower().replace(" ", "-")
    impact_class = signal["business_impact"].lower()
    st.markdown(
        f'<article class="signal-card">'
        f'<div class="signal-card-top"><span class="signal-category">{category}</span>'
        f'<span class="outlook outlook-{outlook_class}">{outlook}</span>'
        f'<span class="velocity velocity-{velocity_class}">↗ {velocity}</span></div>'
        f'<h3>{title}</h3><p class="signal-summary">{summary}</p>'
        f'<div class="signal-source"><span>{source}</span><span>·</span>'
        f'<span>{html.escape(signal["published"])}</span><span>·</span>'
        f'<span>{signal["reading_minutes"]} min read</span></div>'
        f'<div class="signal-scores">'
        f'<div><span>IMPACT</span><strong>{signal["impact_score"]}</strong></div>'
        f'<div><span>SIGNAL</span><strong>{signal["signal_score"]}</strong></div>'
        f'<div><span>CONFIDENCE</span><strong>{signal["confidence_score"]}%</strong></div>'
        f'<div><span>BUSINESS IMPACT</span><strong class="impact-{impact_class}">'
        f'{impact_label}</strong></div></div>'
        f'<div class="signal-card-bottom"><span class="sentiment">Sentiment · {sentiment}</span>'
        f'<a href="{html.escape(signal["url"], quote=True)}" target="_blank" rel="noreferrer">'
        f'Open source ↗</a></div></article>',
        unsafe_allow_html=True,
    )
    if st.button(
        "Saved" if is_saved else "＋ Save signal",
        key=f"save-{safe_id}",
        help="Add this signal to Saved Intelligence",
    ):
        saved = st.session_state.saved_signals
        if is_saved:
            st.session_state.saved_signals = [item for item in saved if item != signal["id"]]
        else:
            st.session_state.saved_signals = [*saved, signal["id"]]
        st.rerun()
