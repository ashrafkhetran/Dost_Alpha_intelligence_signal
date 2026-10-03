"""Unit tests for deterministic, provider-independent service logic."""

import json

import httpx
import pytest

from services.analyst import (
    AnalystProviderError,
    OPENROUTER_URL,
    _analyze_with_openrouter,
    analyze_question,
)
from services.export import render_brief_pdf
from services.scoring import classify_outlook, weighted_signal_score


def test_weighted_signal_score_returns_weighted_percentage() -> None:
    assert weighted_signal_score(1, 1, 1, 1) == 100
    assert weighted_signal_score(0, 0, 0, 0) == 0
    assert weighted_signal_score(1, 0, 0, 0) == 25


def test_weighted_signal_score_rejects_out_of_range_factors() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        weighted_signal_score(1.1, 0, 0, 0)


@pytest.mark.parametrize(
    ("impact", "sentiment", "expected"),
    [
        (85, "positive", "Opportunity"),
        (85, "neutral", "Watch"),
        (40, "positive", "Watch"),
        (90, "negative", "Risk"),
    ],
)
def test_signal_outlook_uses_impact_and_sentiment(
    impact: float, sentiment: str, expected: str
) -> None:
    assert classify_outlook(impact, sentiment) == expected


def test_signal_outlook_rejects_invalid_values() -> None:
    with pytest.raises(ValueError, match="Impact score"):
        classify_outlook(101, "positive")
    with pytest.raises(ValueError, match="Sentiment"):
        classify_outlook(50, "uncertain")


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("What matters for SEO?", "Search visibility"),
        ("What should founders watch?", "narrow, measurable workflow"),
        ("What's happening in AI?", "deployment economics"),
    ],
)
def test_analyst_returns_topic_relevant_sample(
    question: str, expected: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("services.analyst._get_openrouter_api_key", lambda: None)
    response = analyze_question(question)
    assert expected in response["summary"]
    assert response["source"] == "sample"
    assert 0 <= response["priority_score"] <= 100
    assert response["insights"] and response["risks"] and response["actions"]


def test_analyst_uses_openrouter_and_validates_structured_response() -> None:
    expected = {
        "summary": "A concise analysis.",
        "insights": ["Insight one."],
        "risks": ["Risk one."],
        "opportunities": ["Opportunity one."],
        "actions": ["Action one."],
        "priority_score": 72,
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == OPENROUTER_URL
        assert request.headers["Authorization"] == "Bearer test-secret"
        payload = json.loads(request.content)
        assert payload["model"] == "google/gemma-4-31b-it:free"
        assert payload["messages"][1]["content"] == "What matters for AI?"
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": json.dumps(expected)}}]},
        )

    response = _analyze_with_openrouter(
        "What matters for AI?",
        "test-secret",
        transport=httpx.MockTransport(handler),
    )
    assert response["source"] == "openrouter"
    assert response["summary"] == expected["summary"]


def test_analyst_surfaces_provider_errors_without_sample_fallback() -> None:
    transport = httpx.MockTransport(lambda _request: httpx.Response(401))
    with pytest.raises(AnalystProviderError, match="HTTP 401"):
        _analyze_with_openrouter("Question", "bad-key", transport=transport)


def test_analyst_rejects_malformed_provider_json() -> None:
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(
            200,
            json={"choices": [{"message": {"content": '{"summary": "missing fields"}'}}]},
        )
    )
    with pytest.raises(AnalystProviderError, match="insights"):
        _analyze_with_openrouter("Question", "test-secret", transport=transport)


def test_analyst_requires_a_question(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("services.analyst._get_openrouter_api_key", lambda: None)
    with pytest.raises(ValueError, match="research question"):
        analyze_question("  ")


def test_brief_pdf_export_returns_valid_pdf_bytes() -> None:
    pdf = render_brief_pdf("Sample Brief", "### Executive summary\nA sample summary.")
    assert pdf.startswith(b"%PDF-")
    assert len(pdf) > 500
