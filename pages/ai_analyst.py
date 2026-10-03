"""Demo analyst workspace with transparent provider boundaries."""

import streamlit as st

from components.layout import page_heading
from services.analyst import AnalystProviderError, analyze_question, has_openrouter_api_key


def render() -> None:
    """Render the analyst prompt and sample intelligence response."""
    page_heading("RESEARCH WORKSPACE", "AI Analyst", "Turn a focused question into a decision-ready brief.")
    live_model = has_openrouter_api_key()
    if live_model:
        st.info("OpenRouter is enabled. Responses are model-generated, but are not grounded in live news, retrieval, or source citations.")
    else:
        st.info("Demo mode: responses are deterministic examples. Configure OPENROUTER_API_KEY to enable model-generated analysis.")
    st.markdown(
        '<div class="analyst-intro"><span class="analyst-symbol">✳</span>'
        '<div><h3>What deserves your attention?</h3><p>Ask a question about a market, '
        'company, technology, or opportunity.</p></div></div>',
        unsafe_allow_html=True,
    )
    prompt = st.text_input(
        "Research question",
        placeholder="e.g. What matters today for SEO?",
        label_visibility="collapsed",
    )
    if st.button("Analyze question", type="primary", disabled=not prompt.strip()):
        st.session_state.pop("analyst_response", None)
        try:
            st.session_state["analyst_response"] = analyze_question(prompt)
        except AnalystProviderError as exc:
            st.error(str(exc))
    for example in ["What are today's AI opportunities?", "What should SaaS founders watch?", "What matters today for SEO?"]:
        st.markdown(f'<span class="prompt-chip">{example}</span>', unsafe_allow_html=True)

    response = st.session_state.get("analyst_response")
    if response:
        response_label = "OPENROUTER MODEL ANALYSIS · NO LIVE RETRIEVAL" if response["source"] == "openrouter" else "SAMPLE ANALYSIS · NOT MODEL-GENERATED"
        st.markdown(f'<div class="analysis-label">{response_label}</div>', unsafe_allow_html=True)
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
        priority_label = "Model-estimated priority" if response["source"] == "openrouter" else "Sample priority score"
        st.progress(response["priority_score"] / 100, text=f"{priority_label} · {response['priority_score']}/100")
        if response["source"] == "openrouter":
            st.caption("Model output may be inaccurate. Verify important claims against primary sources; this prototype does not use RAG or provide citations.")
        else:
            st.caption("The sample response is not grounded in current events or retrieved sources.")
