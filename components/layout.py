"""Shared application chrome and navigation."""

import streamlit as st


NAVIGATION = [
    "Overview",
    "Intelligence Feed",
    "AI Analyst",
    "Trend Radar",
    "Executive Briefings",
    "Saved Intelligence",
    "Subscription",
    "Settings",
    "Admin Console",
]


def render_sidebar() -> str:
    """Render the primary navigation and return the active destination."""
    with st.sidebar:
        st.markdown(
            '<div class="brand-lockup"><span class="brand-mark">◈</span>'
            '<span><strong>DOST ALPHA</strong><small>INTELLIGENCE TERMINAL</small></span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="sidebar-label">WORKSPACE</div>', unsafe_allow_html=True)
        selected = st.radio(
            "Workspace navigation",
            NAVIGATION,
            label_visibility="collapsed",
            format_func=lambda item: {
                "Overview": "◫  Overview",
                "Intelligence Feed": "◉  Intelligence Feed",
                "AI Analyst": "✳  AI Analyst",
                "Trend Radar": "◎  Trend Radar",
                "Executive Briefings": "▤  Briefings",
                "Saved Intelligence": "▣  Saved Intelligence",
                "Subscription": "◇  Subscription",
                "Settings": "⚙  Settings",
                "Admin Console": "⌘  Admin Console",
            }[item],
        )
        st.markdown(
            '<div class="sidebar-workspace"><span class="live-dot"></span>'
            '<span>LIVE WORKSPACE</span><span class="workspace-plan">BETA</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-footer">Signal over noise.<br>'
            '<span>Intelligence over information.</span></div>',
            unsafe_allow_html=True,
        )
    return selected


def page_heading(eyebrow: str, title: str, description: str = "") -> None:
    """Render a consistent section heading."""
    subtitle = f'<p class="page-description">{description}</p>' if description else ""
    st.markdown(
        f'<div class="page-heading"><div class="eyebrow">{eyebrow}</div>'
        f'<h1>{title}</h1>{subtitle}</div>',
        unsafe_allow_html=True,
    )
