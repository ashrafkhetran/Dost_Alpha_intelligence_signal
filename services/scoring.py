"""Transparent normalized scoring primitives for future ingestion pipelines."""


def weighted_signal_score(
    source_quality: float,
    velocity: float,
    impact: float,
    corroboration: float,
) -> float:
    """Combine normalized [0, 1] signal factors into a 0-100 score."""
    factors = (source_quality, velocity, impact, corroboration)
    if any(not 0 <= value <= 1 for value in factors):
        raise ValueError("All signal factors must be between 0 and 1.")
    score = (
        0.25 * source_quality
        + 0.30 * velocity
        + 0.30 * impact
        + 0.15 * corroboration
    )
    return round(score * 100, 1)


def classify_outlook(impact_score: float, sentiment: str) -> str:
    """Classify a sample signal as opportunity, watch, or risk."""
    if not 0 <= impact_score <= 100:
        raise ValueError("Impact score must be between 0 and 100.")
    normalized_sentiment = sentiment.casefold()
    if normalized_sentiment not in {"positive", "neutral", "negative"}:
        raise ValueError("Sentiment must be positive, neutral, or negative.")
    if normalized_sentiment == "negative":
        return "Risk"
    if normalized_sentiment == "positive" and impact_score >= 70:
        return "Opportunity"
    return "Watch"
