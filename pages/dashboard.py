"""Overview dashboard."""

import html

import streamlit as st

from components.layout import page_heading
from components.signals import render_signal_card
from services.analyst import generate_brief
from services.feeds import topic_momentum
from services.live import get_signals, keyword_filter, source_count


def render() -> None:
    """Render the intelligence overview."""
    signals, is_live, errors = get_signals()
    signals = keyword_filter(signals)
    momentum = topic_momentum(signals) if is_live else {}
    lead_topic = max(momentum, key=momentum.get) if momentum else "AI"
    page_heading("LIVE WORKSPACE" if is_live else "DEMO WORKSPACE · SAMPLE DATA", "Your intelligence, in focus", "A clear view of the signals shaping your market.")
    st.markdown(
        '<div class="hero-panel"><div class="hero-copy"><div class="hero-kicker">'
        '<span class="live-dot"></span> YOUR PERSONAL INTELLIGENCE TERMINAL</div>'
        '<h2>See what matters<br><span>before it moves.</span></h2>'
        '<p>Signal over noise. Intelligence over information.</p></div>'
        '<div class="hero-orbit"><div class="orbit orbit-outer"></div>'
        '<div class="orbit orbit-inner"></div><div class="orbit-core">◈</div>'
        f'<span class="orbit-label orbit-label-one">{lead_topic.upper()} · RISING</span>'
        f'<span class="orbit-label orbit-label-two">{len(signals)} SIGNALS</span></div></div>',
        unsafe_allow_html=True,
    )
    st.caption("Live public feeds, refreshed every 20 minutes." if is_live else "Live feeds unreachable right now · showing sample data.")

    metric_cols = st.columns(4)
    opportunities = [x for x in signals if x["sentiment"] == "Positive" and x["impact_score"] >= 70]
    risks = [x for x in signals if x["sentiment"] == "Negative"]
    avg_conf = sum(x["confidence_score"] for x in signals) / max(1, len(signals))
    metrics = [
        ("SOURCES MONITORED", str(source_count() - len(errors)), f"{len(errors)} skipped" if errors else "all responding", "cyan"),
        ("SIGNALS DETECTED", str(len(signals)), "last 7 days" if is_live else "sample", "violet"),
        ("OPPORTUNITIES", str(len(opportunities)), f"{len(risks)} risks flagged", "green"),
        ("AVG. CONFIDENCE", f"{avg_conf:.1f}%", "heuristic, see feed notes", "amber"),
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
        for signal in signals[:3]:
            render_signal_card(signal, signal["id"] in st.session_state.saved_signals)
    with right:
        st.markdown('<div class="section-title"><div><span>02 / EXECUTIVE BRIEF</span>'
                    '<h2>Today, distilled</h2></div></div>', unsafe_allow_html=True)
        top = signals[0]
        st.markdown(
            '<div class="brief-panel"><div class="brief-tag">'
            + ("TODAY'S TOP SIGNAL · LIVE" if is_live else "MORNING INTELLIGENCE · SAMPLE")
            + f'</div><h3>{html.escape(top["title"])}</h3>'
            f'<p>{html.escape(top["summary"][:220])}</p>'
            '<div class="brief-divider"></div><div class="brief-takeaway">'
            f'<span>THE TAKEAWAY</span><p>{lead_topic} has the strongest momentum right now. '
            f'{len(opportunities)} opportunities and {len(risks)} risks in today’s stream.</p></div>'
            f'<div class="brief-footer">{html.escape(top["source"])}</div></div>',
            unsafe_allow_html=True,
        )
        if st.button("Generate executive brief", type="primary", width="stretch"):
            with st.spinner("Writing your brief…"):
                st.session_state.dashboard_brief = generate_brief("Executive Brief", signals)
        if st.session_state.get("dashboard_brief"):
            body, method = st.session_state.dashboard_brief
            with st.expander(f"Executive brief · {method}", expanded=True):
                st.markdown(body)
    st.markdown(
        '<div class="footnote">Stories come from free public RSS feeds. Scores are transparent heuristics, '
        'not verified facts. Open the source before acting.</div>',
        unsafe_allow_html=True,
    )
