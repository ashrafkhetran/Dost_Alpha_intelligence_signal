"""Streamlit-facing data access: cached live signals with a labeled sample fallback."""

from __future__ import annotations

import streamlit as st

from services.demo_data import SIGNALS as SAMPLE_SIGNALS
from services.feeds import SOURCES, fetch_signals

CACHE_MINUTES = 20


@st.cache_data(ttl=CACHE_MINUTES * 60, show_spinner="Pulling live intelligence from public feeds…")
def _cached_fetch(topics: tuple[str, ...]) -> tuple[list[dict], list[str]]:
    return fetch_signals(list(topics))


def get_signals() -> tuple[list[dict], bool, list[str]]:
    """Return (signals, is_live, feed_errors) for the user's followed topics.

    Every signal shown is also registered in session state so Saved Intelligence
    can display it later, even after the live feed has refreshed.
    """
    topics = tuple(sorted(t for t in st.session_state.get("followed_topics", []) if t in SOURCES)) or tuple(SOURCES)
    try:
        signals, errors = _cached_fetch(topics)
    except Exception as exc:  # network down or feeds unreachable
        signals, errors = [], [f"Live feeds unavailable: {type(exc).__name__}"]
    is_live = bool(signals)
    if not is_live:
        signals = SAMPLE_SIGNALS
    registry = st.session_state.setdefault("signal_registry", {})
    for s in signals:
        registry[s["id"]] = s
    return signals, is_live, errors


def refresh() -> None:
    _cached_fetch.clear()


def source_count() -> int:
    topics = [t for t in st.session_state.get("followed_topics", []) if t in SOURCES] or list(SOURCES)
    return sum(len(SOURCES[t]) for t in topics)


def keyword_filter(signals: list[dict]) -> list[dict]:
    """Boost signals that match the user's watch keywords to the top."""
    raw = st.session_state.get("watch_keywords", "") or ""
    words = [w.strip().casefold() for w in raw.split(",") if w.strip()]
    if not words:
        return signals
    hit = lambda s: any(w in f"{s['title']} {s['summary']}".casefold() for w in words)
    return [s for s in signals if hit(s)] + [s for s in signals if not hit(s)]
