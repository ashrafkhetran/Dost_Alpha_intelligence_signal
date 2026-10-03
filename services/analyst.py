"""OpenRouter-backed Analyst (free models) grounded in live headlines, with a labeled no-key fallback."""

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
# Free by default. Gemma is fast and returns clean JSON; "openrouter/free" routes to
# any available free model; the others are fallbacks when one is rate-limited. Override with the
# OPENROUTER_MODEL secret (comma-separated list) to use different models.
DEFAULT_FREE_MODELS = [
    "google/gemma-4-31b-it:free",
    "openrouter/free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "qwen/qwen3.8-27b:free",
]
OPENROUTER_MODEL = DEFAULT_FREE_MODELS[0]
# Several free models "think" before answering, so leave room beyond the answer itself.
RESPONSE_FIELDS = {
    "summary": str,
    "insights": list,
    "risks": list,
    "opportunities": list,
    "actions": list,
    "priority_score": int,
}
RETRYABLE_STATUS = {404, 408, 429, 500, 502, 503, 504}


class AnalystProviderError(RuntimeError):
    """A provider request failed or returned an invalid Analyst response."""


def _secret(name: str) -> str:
    """Read a setting from the environment or Streamlit secrets without exposing it."""
    value = os.environ.get(name, "").strip()
    if value:
        return value
    try:
        import streamlit as st

        return str(st.secrets.get(name, "")).strip()
    except Exception:  # no secrets file, or running outside Streamlit
        return ""


def has_openrouter_api_key() -> bool:
    """True when a key is configured (value never exposed)."""
    return bool(_get_openrouter_api_key())


def _get_openrouter_api_key() -> str | None:
    return _secret("OPENROUTER_API_KEY") or None


def configured_models() -> list[str]:
    custom = [m.strip() for m in _secret("OPENROUTER_MODEL").split(",") if m.strip()]
    return custom or list(DEFAULT_FREE_MODELS)


def _extract_json(content: Any) -> Any:
    """Free models sometimes wrap JSON in prose or code fences; recover the object."""
    if not isinstance(content, str) or not content.strip():
        raise AnalystProviderError("OpenRouter returned an empty or non-text response.")
    text = content.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    raise AnalystProviderError("OpenRouter returned invalid JSON for the Analyst response.")


def _validate_response(content: Any) -> dict:
    """Parse and validate the structured JSON returned by the model."""
    result = _extract_json(content)
    if not isinstance(result, dict):
        raise AnalystProviderError("OpenRouter returned an invalid Analyst response object.")
    if isinstance(result.get("priority_score"), float):
        result["priority_score"] = round(result["priority_score"])
    for field, expected_type in RESPONSE_FIELDS.items():
        if not isinstance(result.get(field), expected_type):
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


def format_evidence(signals: list[dict]) -> str:
    """Numbered evidence block passed to the model so it can cite real stories."""
    return "\n".join(
        f"[{i}] {s['title']} ({s['source']}, {s['published']}) {s['summary'][:260]}"
        for i, s in enumerate(signals, 1)
    )


def _chat(
    messages: list[dict],
    api_key: str,
    transport: httpx.BaseTransport | None = None,
    models: list[str] | None = None,
    max_tokens: int = 4000,
    validate=None,
) -> tuple[Any, str]:
    """Call OpenRouter, falling back across free models. Returns (result, model)."""
    last_error: AnalystProviderError | None = None
    for model in models or configured_models():
        payload = {"model": model, "temperature": 0.2, "max_tokens": max_tokens, "messages": messages}
        try:
            with httpx.Client(timeout=httpx.Timeout(35.0, connect=8.0), transport=transport) as client:
                response = client.post(
                    OPENROUTER_URL,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://github.com/ashrafkhetran/Dost_Alpha_intelligence_signal",
                        "X-Title": "DOST ALPHA",
                    },
                    json=payload,
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            last_error = AnalystProviderError(
                f"OpenRouter request failed with HTTP {code}. "
                "Check the key, account balance, and selected model access."
            )
            if code in RETRYABLE_STATUS:
                continue
            raise last_error from exc
        except httpx.TimeoutException:
            last_error = AnalystProviderError("OpenRouter request timed out. Please try again.")
            continue
        except httpx.RequestError as exc:
            raise AnalystProviderError("Could not connect to OpenRouter. Check the network and try again.") from exc
        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError):
            last_error = AnalystProviderError("OpenRouter returned an unexpected response format.")
            continue
        try:
            return (validate(content) if validate else content), data.get("model", model)
        except AnalystProviderError as exc:
            last_error = exc
            continue
    raise last_error or AnalystProviderError("No OpenRouter model is configured.")


def _analyze_with_openrouter(
    question: str,
    api_key: str,
    transport: httpx.BaseTransport | None = None,
    evidence: list[dict] | None = None,
    models: list[str] | None = None,
) -> dict:
    """Request a structured analysis, grounded in live headlines when supplied."""
    grounded = bool(evidence)
    system = (
        "You are DOST ALPHA, a careful business intelligence analyst. "
        "Return ONLY one JSON object (no prose, no code fences) with string field summary; "
        "arrays of strings insights, risks, opportunities, actions; integer priority_score "
        "from 0 to 100; and array of integers citations. "
    )
    if grounded:
        system += (
            "Base the analysis on the numbered live headlines provided. Refer to them as [n] "
            "inside your sentences and list the numbers you used in citations. Do not invent "
            "facts that are not in the headlines; if the headlines are thin, say so in risks."
        )
    else:
        system += (
            "No live sources are attached: give general analysis, do not claim access to news "
            "or cite sources, set citations to [] and state material uncertainty in risks."
        )
    messages = [{"role": "system", "content": system}, {"role": "user", "content": question.strip()}]
    if grounded:
        messages.append({"role": "user", "content": "Live headlines:\n" + format_evidence(evidence)})
    result, model = _chat(messages, api_key, transport, models, validate=_validate_response)
    result["model"] = model
    result["evidence"] = []
    if grounded:
        cites = result.get("citations") if isinstance(result.get("citations"), list) else []
        result["evidence"] = [evidence[i - 1] for i in cites if isinstance(i, int) and 1 <= i <= len(evidence)]
        result["evidence"] = result["evidence"] or evidence[:5]
    return result


def analyze_question(question: str, evidence: list[dict] | None = None) -> dict:
    """Use OpenRouter when configured; otherwise return a labeled sample response."""
    if not question.strip():
        raise ValueError("Enter a research question before requesting an analysis.")
    api_key = _get_openrouter_api_key()
    if api_key:
        return _analyze_with_openrouter(question, api_key, evidence=evidence)

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
        "evidence": evidence[:5] if evidence else [],
    }


def _source_list(signals: list[dict]) -> str:
    return "### Sources\n" + "\n".join(
        f"- [{i}] {s['title']} ({s['source']}) {s['url']}" for i, s in enumerate(signals, 1)
    )


def extractive_brief(signals: list[dict]) -> str:
    """Deterministic brief built only from real headlines, used when no model is available."""
    if not signals:
        return SAMPLE_BRIEF
    idx = {s["id"]: i for i, s in enumerate(signals, 1)}

    def line(s: dict) -> str:
        return f"- {s['title']} [{idx[s['id']]}]"

    risks = [s for s in signals if s["sentiment"] == "Negative"][:3]
    opps = [s for s in signals if s["sentiment"] == "Positive"][:3]
    topics = ", ".join(sorted({s["topic"] for s in signals}))
    parts = [
        "### Executive summary",
        f"{len(signals)} high-scoring live stories across {topics}. Top signal: {signals[0]['title']} [1].",
        "",
        "### Key developments",
        *[line(s) for s in signals[:6]],
        "",
        "### Risks",
        *([line(s) for s in risks] or ["- No clearly negative stories among the top signals."]),
        "",
        "### Opportunities",
        *([line(s) for s in opps] or ["- No clearly positive stories among the top signals."]),
        "",
        "### Recommended actions",
        "1. Open the top three sources and confirm the facts before acting.",
        "2. Save the signals that touch your clients or projects and re-check them tomorrow.",
        "",
        _source_list(signals),
    ]
    return "\n".join(parts)


def generate_brief(
    brief_type: str, signals: list[dict], transport: httpx.BaseTransport | None = None
) -> tuple[str, str]:
    """Write a Markdown brief from live signals. Returns (markdown, method label)."""
    top = signals[:12]
    api_key = _get_openrouter_api_key()
    if api_key and top:
        messages = [
            {"role": "system", "content": (
                "You are DOST ALPHA, writing a concise executive intelligence brief in Markdown. "
                "Use exactly these sections as '### ' headings: Executive summary, Key developments, "
                "Risks, Opportunities, Recommended actions. Use '- ' bullets (a numbered list for actions). "
                "Every development must cite its numbered headline like [3]. Use only facts in the "
                "headlines. Plain, direct language, no hype, no em dashes. Under 450 words."
            )},
            {"role": "user", "content": f"Write a {brief_type}.\n\nLive headlines:\n{format_evidence(top)}"},
        ]
        try:
            text, model = _chat(messages, api_key, transport, max_tokens=4000)
            if isinstance(text, str) and "###" in text:
                return text.strip() + "\n\n" + _source_list(top), f"AI synthesis · {model}"
        except AnalystProviderError:
            pass
    if not top:
        return SAMPLE_BRIEF, "Sample content (live feeds unavailable)"
    return extractive_brief(top), "Extractive summary of live headlines (no AI)"
