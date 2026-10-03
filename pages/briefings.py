"""Executive briefing generation and export."""

import html

import streamlit as st

from components.layout import page_heading
from services.analyst import SAMPLE_BRIEF
from services.export import render_brief_pdf

BRIEF_TYPES = ["Morning Brief", "Weekly Brief", "Executive Brief", "Industry Brief", "AI Brief", "Business Brief", "SEO Brief", "Startup Brief"]


def render() -> None:
    """Generate a sample briefing and offer Markdown and HTML exports."""
    page_heading("DECISION SUPPORT", "Executive Briefings", "Concise, structured context for your next decision.")
    st.info("Briefs currently use illustrative sample content. Live source synthesis and PDF export are not connected.")
    col, button_col = st.columns([2, 1])
    with col:
        brief_type = st.selectbox("Briefing format", BRIEF_TYPES)
    with button_col:
        st.write("")
        st.write("")
        generate = st.button("Generate sample brief", type="primary", width="stretch")
    if generate:
        st.session_state["brief_type"] = brief_type

    if st.session_state.get("brief_type"):
        title = st.session_state["brief_type"]
        markdown = f"# {title} — DOST ALPHA\n\n{SAMPLE_BRIEF}"
        st.markdown(f"### {title}")
        st.markdown(SAMPLE_BRIEF)
        st.download_button("Download Markdown", markdown, file_name="dost-alpha-brief.md", mime="text/markdown")
        html_report = (
            "<!doctype html><html><head><meta charset='utf-8'><title>"
            + html.escape(title)
            + "</title></head><body><main><h1>"
            + html.escape(title)
            + "</h1><pre>"
            + html.escape(SAMPLE_BRIEF)
            + "</pre></main></body></html>"
        )
        st.download_button("Download HTML", html_report, file_name="dost-alpha-brief.html", mime="text/html")
        pdf_report = render_brief_pdf(title, SAMPLE_BRIEF)
        st.download_button("Download PDF", pdf_report, file_name="dost-alpha-brief.pdf", mime="application/pdf")
