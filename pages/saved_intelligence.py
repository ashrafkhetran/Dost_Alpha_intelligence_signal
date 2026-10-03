"""User's saved sample signals."""

import streamlit as st

from components.layout import page_heading
from components.signals import render_signal_card
from services.demo_data import SIGNALS


def render() -> None:
    """Display signals bookmarked in the current browser session."""
    page_heading("YOUR LIBRARY", "Saved Intelligence", "Keep important signals close to the decisions they inform.")
    saved_ids = st.session_state.saved_signals
    saved = [signal for signal in SIGNALS if signal["id"] in saved_ids]
    if not saved:
        st.markdown('<div class="empty-state"><span>▣</span><h3>Your library starts here</h3>'
                    '<p>Save a signal from the Intelligence Feed to revisit it later.</p></div>',
                    unsafe_allow_html=True)
        return
    for signal in saved:
        render_signal_card(signal, is_saved=True)
