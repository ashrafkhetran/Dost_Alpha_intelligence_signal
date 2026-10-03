"""Overview dashboard."""

import streamlit as st

from components.layout import page_heading
from components.signals import render_signal_card
from services.analyst import SAMPLE_BRIEF
from services.demo_data import SIGNALS


def render() -> None:
    """Render the intelligence overview."""
    page_heading("DEMO WORKSPACE · SAMPLE DATA", "Your intelligence, in focus", "A clear view of the signals shaping your market.")
    st.markdown(
        '<div class="hero-panel"><div class="hero-copy"><div class="hero-kicker">'
        '<span class="live-dot"></span> YOUR PERSONAL INTELLIGENCE TERMINAL</div>'
        '<h2>See what matters<br><span>before it moves.</span></h2>'
        '<p>Signal over noise. Intelligence over information.</p></div>'
        '<div class="hero-orbit"><div class="orbit orbit-outer"></div>'
        '<div class="orbit orbit-inner"></div><div class="orbit-core">◈</div>'
        '<span class="orbit-label orbit-label-one">AI · RISING</span>'
        '<span class="orbit-label orbit-label-two">12 SIGNALS</span></div></div>',
        unsafe_allow_html=True,
    )
    st.caption("Illustrative sample workspace · Live source monitoring is not connected yet.")

    metric_cols = st.columns(4)
    metrics = [
        ("SOURCES MONITORED", "1,247", "+18 this week", "cyan"),
        ("SIGNALS DETECTED", "97", "+12.4%", "violet"),
        ("OPPORTUNITIES", "12", "4 high conviction", "green"),
        ("AVG. CONFIDENCE", "86.2%", "Across sample signals", "amber"),
    ]
    for col, (label, value, note, tone) in zip(metric_cols, metrics):
        with col:
            st.markdown(
                f'<div class="metric-card metric-{tone}"><div>{label}</div>'
                f'<strong>{value}</strong><small>{note}</small></div>',
                unsafe_allow_html=True,
            )

    left, right = st.columns([1.55, 1])
    with left:
        st.markdown('<div class="section-title"><div><span>01 / SIGNAL STREAM</span>'
                    '<h2>Worth your attention</h2></div></div>', unsafe_allow_html=True)
        for signal in SIGNALS[:2]:
            render_signal_card(signal, signal["id"] in st.session_state.saved_signals)
    with right:
        st.markdown('<div class="section-title"><div><span>02 / EXECUTIVE BRIEF</span>'
                    '<h2>Today, distilled</h2></div></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="brief-panel"><div class="brief-tag">MORNING INTELLIGENCE · SAMPLE</div>'
            '<h3>AI infrastructure is shifting from model scale to deployment advantage.</h3>'
            '<p>Three sample signals point to a growing focus on inference efficiency, '
            'enterprise integration, and specialized AI tooling.</p>'
            '<div class="brief-divider"></div><div class="brief-takeaway">'
            '<span>THE TAKEAWAY</span><p>Watch the picks-and-shovels layer: teams that make '
            'deployment cheaper and safer may capture near-term demand.</p></div>'
            '<div class="brief-footer">3 DEVELOPMENTS <span>·</span> 2 OPPORTUNITIES</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("Generate executive brief", type="primary", width="stretch"):
            st.session_state.show_dashboard_brief = True
        if st.session_state.show_dashboard_brief:
            with st.expander("Sample executive brief", expanded=True):
                st.markdown(SAMPLE_BRIEF)
    st.markdown(
        '<div class="footnote">Sample content and metrics are illustrative only. '
        'No live sources or AI provider are connected.</div>',
        unsafe_allow_html=True,
    )
