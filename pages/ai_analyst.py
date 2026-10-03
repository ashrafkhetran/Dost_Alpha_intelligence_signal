"""Analyst workspace: free OpenRouter models grounded in live headlines."""

import html

import streamlit as st

from components.layout import page_heading
from services.analyst import AnalystProviderError, analyze_question, has_openrouter_api_key
from services.feeds import search
from services.live import get_signals

EXAMPLES = ["What are today's AI opportunities?", "What should SaaS founders watch?", "What matters today for SEO?"]


def render() -> None:
    """Render the analyst prompt and grounded intelligence response."""
    page_heading("RESEARCH WORKSPACE", "AI Analyst", "Turn a focused question into a decision-ready brief.")
    live_model = has_openrouter_api_key()
    signals, is_live, _ = get_signals()
    if live_model and is_live:
        st.success("Live analysis: a free OpenRouter model reads the most relevant live headlines and cites them.")
    elif live_model:
        st.info("Model connected, but live feeds are unreachable, so answers are general analysis without sources.")
    else:
        st.warning(
            "No model key found. Add OPENROUTER_API_KEY in Streamlit Cloud → App settings → Secrets "
            "(a free OpenRouter key works; no card needed). Showing example answers until then."
        )
    st.markdown(
        '<div class="analyst-intro"><span class="analyst-symbol">✳</span>'
        '<div><h3>What deserves your attention?</h3><p>Ask a question about a market, '
        'company, technology, or opportunity.</p></div></div>',
        unsafe_allow_html=True,
    )
    chip_cols = st.columns(len(EXAMPLES))
    for col, example in zip(chip_cols, EXAMPLES):
        if col.button(example, key=f"chip-{example}", width="stretch"):
            st.session_state.analyst_prompt = example
    prompt = st.text_input(
        "Research question",
        key="analyst_prompt",
        placeholder="e.g. What matters today for SEO?",
        label_visibility="collapsed",
    )
    if st.button("Analyze question", type="primary", disabled=not prompt.strip()):
        st.session_state.pop("analyst_response", None)
        evidence = search(signals, prompt) if is_live else None
        with st.spinner("Reading the signals…"):
            try:
                st.session_state["analyst_response"] = analyze_question(prompt, evidence)
            except AnalystProviderError as exc:
                st.error(f"{exc} Free models are sometimes busy; try again in a minute.")

    response = st.session_state.get("analyst_response")
    if not response:
        return
    if response["source"] == "openrouter":
        grounded = "GROUNDED IN LIVE HEADLINES" if response.get("evidence") else "NO LIVE SOURCES"
        label = f"MODEL ANALYSIS · {html.escape(str(response.get('model', '')))} · {grounded}"
    else:
        label = "EXAMPLE ANSWER · NOT MODEL-GENERATED"
    st.markdown(f'<div class="analysis-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f"### Executive summary\n{response['summary']}")
    left, right = st.columns(2)
    with left:
        st.markdown("#### Key insights")
        for item in response["insights"]:
            st.markdown(f"- {item}")
        st.markdown("#### Opportunities")
        for item in response["opportunities"]:
            st.markdown(f"- {item}")
    with right:
        st.markdown("#### Risks to watch")
        for item in response["risks"]:
            st.markdown(f"- {item}")
        st.markdown("#### Recommended actions")
        for item in response["actions"]:
            st.markdown(f"- {item}")
    priority_label = "Model-estimated priority" if response["source"] == "openrouter" else "Example priority score"
    st.progress(response["priority_score"] / 100, text=f"{priority_label} · {response['priority_score']}/100")
    if response.get("evidence"):
        st.markdown("#### Sources read")
        for i, s in enumerate(response["evidence"], 1):
            st.markdown(f"{i}. [{s['title']}]({s['url']}) · {s['source']} · {s['published']}")
    st.caption("AI output can be wrong. Open the sources and confirm anything you plan to act on.")
