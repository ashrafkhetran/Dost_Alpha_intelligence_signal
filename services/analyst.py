"""OpenRouter-backed Analyst with a clearly labeled no-key demo response."""

import json
import os
from typing import Any

import httpx

SAMPLE_BRIEF = (
    "### Executive summary\n"
    "Sample signals suggest AI product advantage is shifting toward reliable deployment, "
    "cost control, and workflow ownership rather than model capability alone.\n\n"
    "### Key insights\n"
    "- Inference economics and latency are increasingly part of product positioning.\n"
    "- Narrow, accountable agent workflows are a clearer adoption wedge than broad autonomy.\n"
    "- Governance requirements can shape enterprise buying and vendor selection.\n\n"
    "### Risks\n"
    "- Sample signals are directional and are not evidence of verified market-wide demand.\n"
    "- Vendor claims and short-term attention can distort apparent momentum.\n\n"
    "### Opportunities\n"
    "- Explore evaluation, observability, and data-governance needs around production deployments.\n"
    "- Look for vertical workflows with measurable outcomes and clear human escalation.\n\n"
    "### Recommended actions\n"
    "1. Validate willingness to pay with target buyers before committing product resources.\n"
    "2. Track deployment cost, security posture, and workflow completion as separate indicators."
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-4o-mini"
RESPONSE_FIELDS = {
    "summary": str,
    "insights": list,
    "risks": list,
    "opportunities": list,
    "actions": list,
    "priority_score": int,
}


class AnalystProviderError(RuntimeError):
    """A provider request failed or returned an invalid Analyst response."""


def has_openrouter_api_key() -> bool:
    """Check configured environment and Streamlit secrets without exposing them."""
    if os.environ.get("OPENROUTER_API_KEY", "").strip():
        return True
    try:
        import streamlit as st
        from streamlit.errors import StreamlitSecretNotFoundError

        return bool(st.secrets.get("OPENROUTER_API_KEY", "").strip())
    except StreamlitSecretNotFoundError:
        return False


def _get_openrouter_api_key() -> str | None:
    """Read the OpenRouter key from the environment or local Streamlit secrets."""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    try:
        import streamlit as st
        from streamlit.errors import StreamlitSecretNotFoundError

        return st.secrets.get("OPENROUTER_API_KEY", "").strip() or None
    except StreamlitSecretNotFoundError:
        return None


def _validate_response(content: Any) -> dict:
    """Parse and validate the structured JSON returned by the model."""
    if not isinstance(content, str):
        raise AnalystProviderError("OpenRouter returned an empty or non-text response.")
    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise AnalystProviderError("OpenRouter returned invalid JSON for the Analyst response.") from exc
    if not isinstance(result, dict):
        raise AnalystProviderError("OpenRouter returned an invalid Analyst response object.")
    for field, expected_type in RESPONSE_FIELDS.items():
        value = result.get(field)
        if not isinstance(value, expected_type):
            raise AnalystProviderError(f"OpenRouter Analyst response is missing a valid {field!r} field.")
    for field in ("insights", "risks", "opportunities", "actions"):
        if not all(isinstance(item, str) and item.strip() for item in result[field]):
            raise AnalystProviderError(f"OpenRouter Analyst response contains invalid items in {field!r}.")
    if not 0 <= result["priority_score"] <= 100:
        raise AnalystProviderError("OpenRouter Analyst priority score must be between 0 and 100.")
    if not result["summary"].strip():
        raise AnalystProviderError("OpenRouter Analyst summary cannot be empty.")
    result["source"] = "openrouter"
    return result


def _analyze_with_openrouter(
    question: str,
    api_key: str,
    transport: httpx.BaseTransport | None = None,
) -> dict:
    """Request a structured analysis from the configured OpenRouter model."""
    payload = {
        "model": OPENROUTER_MODEL,
        "temperature": 0.2,
        "max_tokens": 1100,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are DOST ALPHA, a careful business intelligence analyst. "
                    "Return one JSON object with string fields summary; arrays of strings "
                    "insights, risks, opportunities, actions; and integer priority_score "
                    "from 0 to 100. Be concise, distinguish general analysis from verified "
                    "facts, do not claim access to live news, retrieval, or citations. "
                    "State material uncertainty in risks."
                ),
            },
            {"role": "user", "content": question.strip()},
        ],
    }
    try:
        with httpx.Client(
            timeout=httpx.Timeout(45.0, connect=10.0),
            transport=transport,
        ) as client:
            response = client.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "X-Title": "DOST ALPHA",
                },
                json=payload,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise AnalystProviderError(
            f"OpenRouter request failed with HTTP {exc.response.status_code}. "
            "Check the key, account balance, and selected model access."
        ) from exc
    except httpx.TimeoutException as exc:
        raise AnalystProviderError("OpenRouter request timed out. Please try again.") from exc
    except httpx.RequestError as exc:
        raise AnalystProviderError("Could not connect to OpenRouter. Check the network and try again.") from exc

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise AnalystProviderError("OpenRouter returned an unexpected response format.") from exc
    return _validate_response(content)


def analyze_question(question: str) -> dict:
    """Use OpenRouter when configured; otherwise return a labeled sample response."""
    if not question.strip():
        raise ValueError("Enter a research question before requesting an analysis.")
    api_key = _get_openrouter_api_key()
    if api_key:
        return _analyze_with_openrouter(question, api_key)

    subject = question.strip().rstrip("?").lower()
    if "seo" in subject or "search" in subject:
        focus = "Search visibility is shifting toward useful, authoritative answers across traditional and conversational discovery."
        opportunity = "Audit high-intent pages for clear evidence, freshness, structured information, and first-party expertise."
    elif "startup" in subject or "founder" in subject or "saas" in subject:
        focus = "The strongest sample opportunity is a narrow, measurable workflow with a clear economic buyer."
        opportunity = "Interview buyers about repetitive, high-cost tasks where human review remains valuable."
    else:
        focus = "Sample signals point to deployment economics, trusted workflows, and operational governance as themes to monitor."
        opportunity = "Map one high-friction workflow where faster, safer AI deployment creates measurable value."
    return {
        "summary": focus,
        "insights": [
            "Deployment reliability and unit economics may differentiate products beyond model access.",
            "Trust controls and source quality influence whether teams expand usage.",
            "Early attention is a hypothesis to validate, not proof of durable demand.",
        ],
        "risks": [
            "This prototype response is not grounded in retrieved or live evidence.",
            "Market momentum can be noisy; validate against primary sources and buyer behavior.",
        ],
        "opportunities": [opportunity, "Track adoption and customer outcomes over time before scaling investment."],
        "actions": [
            "Identify two primary sources and one customer signal to validate this theme.",
            "Set a measurable test with an owner, baseline, and review date.",
        ],
        "priority_score": 78,
        "source": "sample",
    }
