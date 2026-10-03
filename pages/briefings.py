"""Executive briefings synthesized from live signals, with Markdown/HTML/PDF export."""

import html
from datetime import datetime, timezone

import streamlit as st

from components.layout import page_heading
from services.analyst import generate_brief, has_openrouter_api_key
from services.export import render_brief_pdf
from services.live import get_signals, keyword_filter

BRIEF_TYPES = {
    "Morning Brief": None,
    "Weekly Brief": None,
    "Executive Brief": None,
    "AI Brief": "AI",
    "SEO Brief": "SEO",
    "Startup Brief": "Startups",
    "Business Brief": "Business",
    "Marketing Brief": "Marketing",
    "Cybersecurity Brief": "Cybersecurity",
}


def render() -> None:
    """Generate a brief from live sources and offer Markdown, HTML, and PDF downloads."""
    page_heading("DECISION SUPPORT", "Executive Briefings", "Concise, structured context for your next decision.")
    signals, is_live, _ = get_signals()
    if is_live and has_openrouter_api_key():
        st.success("Briefs are written by a free AI model from today's live headlines, with every source listed. PDF export works.")
    elif is_live:
        st.info("Briefs are built from today's live headlines (no AI key set, so they are extractive summaries). PDF export works.")
    else:
        st.warning("Live feeds are unreachable right now, so the brief uses sample content.")

    col, button_col = st.columns([2, 1])
    with col:
        brief_type = st.selectbox("Briefing format", list(BRIEF_TYPES))
    with button_col:
        st.write("")
        st.write("")
        generate = st.button("Generate brief", type="primary", width="stretch")
    if generate:
        topic = BRIEF_TYPES[brief_type]
        pool = keyword_filter([s for s in signals if not topic or s["topic"] == topic] or signals)
        with st.spinner("Writing your brief…"):
            body, method = generate_brief(brief_type, pool)
        st.session_state["brief"] = {"title": brief_type, "body": body, "method": method,
                                     "date": datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")}

    brief = st.session_state.get("brief")
    if not brief:
        return
    title = f"{brief['title']} · {brief['date']}"
    st.markdown(f"### {title}")
    st.caption(f"Method: {brief['method']}")
    st.markdown(brief["body"])
    markdown = f"# {title} · DOST ALPHA\n\n{brief['body']}"
    c1, c2, c3 = st.columns(3)
    c1.download_button("Download Markdown", markdown, file_name="dost-alpha-brief.md", mime="text/markdown", width="stretch")
    html_report = (
        "<!doctype html><html><head><meta charset='utf-8'><title>" + html.escape(title)
        + "</title></head><body><main><h1>" + html.escape(title) + "</h1><pre style='white-space:pre-wrap'>"
        + html.escape(brief["body"]) + "</pre></main></body></html>"
    )
    c2.download_button("Download HTML", html_report, file_name="dost-alpha-brief.html", mime="text/html", width="stretch")
    footer = "DOST ALPHA  |  " + ("Live-source briefing" if is_live else "Illustrative sample briefing")
    c3.download_button("Download PDF", render_brief_pdf(title, brief["body"], footer), file_name="dost-alpha-brief.pdf",
                       mime="application/pdf", width="stretch")
