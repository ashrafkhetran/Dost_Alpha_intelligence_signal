"""User's saved signals (live or sample) for this session."""

import streamlit as st

from components.layout import page_heading
from components.signals import render_signal_card
from services.demo_data import SIGNALS


def render() -> None:
    """Display signals bookmarked in the current browser session."""
    page_heading("YOUR LIBRARY", "Saved Intelligence", "Keep important signals close to the decisions they inform.")
    registry = {s["id"]: s for s in SIGNALS} | st.session_state.get("signal_registry", {})
    saved = [registry[i] for i in st.session_state.saved_signals if i in registry]
    if not saved:
        st.markdown('<div class="empty-state"><span>▣</span><h3>Your library starts here</h3>'
                    '<p>Save a signal from the Intelligence Feed to revisit it later.</p></div>',
                    unsafe_allow_html=True)
        return
    st.caption("Saved items last for this browser session. Download them to keep a copy.")
    export = "\n".join(f"- {s['title']} ({s['source']}, {s['published']}) {s['url']}" for s in saved)
    st.download_button("Download saved list", export, file_name="dost-alpha-saved.md", mime="text/markdown")
    for signal in saved:
        render_signal_card(signal, is_saved=True)
