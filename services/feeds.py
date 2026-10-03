"""Live intelligence ingestion from free, public RSS/Atom feeds.

No wire-service account is needed. Sources are public feeds (Google News topic
searches, Hacker News, and publisher feeds). Scores are transparent heuristics
built from recency, source quality, topic relevance, and cross-source
corroboration, so every number on a card can be explained.
"""

from __future__ import annotations

import hashlib
import html
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
from xml.etree import ElementTree

import httpx

from services.scoring import weighted_signal_score

USER_AGENT = "Mozilla/5.0 (compatible; DOST-ALPHA/1.0; +https://github.com/ashrafkhetran/Dost_Alpha_intelligence_signal)"


def google_news(query: str) -> str:
    """Google News RSS search URL (free, no key)."""
    return f"https://news.google.com/rss/search?q={quote_plus(query)}+when:7d&hl=en-US&gl=US&ceid=US:en"


# topic -> list of (source label, feed url, quality 0..1)
SOURCES: dict[str, list[tuple[str, str, float]]] = {
    "AI": [
        ("Google News · AI", google_news('"artificial intelligence" OR "generative AI" OR OpenAI OR Anthropic'), 0.70),
        ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/", 0.80),
        ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", 0.75),
    ],
    "Technology": [
        ("Hacker News", "https://hnrss.org/frontpage?points=150", 0.70),
        ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab", 0.80),
    ],
    "Startups": [
        ("TechCrunch Startups", "https://techcrunch.com/category/startups/feed/", 0.80),
        ("Google News · Startups", google_news("startup funding round OR seed round OR Series A"), 0.65),
    ],
    "SEO": [
        ("Google News · SEO", google_news('"SEO" OR "Google core update" OR "AI Overviews"'), 0.70),
        ("Search Engine Roundtable", "https://www.seroundtable.com/index.xml", 0.80),
        ("Google Search Central", "https://developers.google.com/search/blog/feed.xml", 0.95),
    ],
    "Marketing": [
        ("Google News · Marketing", google_news('"digital marketing" OR "social media marketing" OR "Google Ads"'), 0.65),
        ("Search Engine Journal", "https://www.searchenginejournal.com/feed/", 0.75),
    ],
    "Business": [
        ("Google News · Business", google_news("business strategy OR acquisition OR earnings"), 0.65),
    ],
    "Finance": [
        ("Google News · Markets", google_news("stock market OR interest rates OR inflation"), 0.65),
    ],
    "Cybersecurity": [
        ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews", 0.75),
        ("Krebs on Security", "https://krebsonsecurity.com/feed/", 0.85),
    ],
    "Healthcare": [
        ("Google News · Health tech", google_news('"health tech" OR "digital health" OR "AI in healthcare"'), 0.65),
    ],
}

CATEGORY_RULES = [
    ("Critical Signals", "CRITICAL SIGNAL", ("breach", "vulnerability", "lawsuit", "ban", "outage", "recall", "zero-day", "ransomware", "fine", "probe", "layoff")),
    ("AI Breakthroughs", "AI BREAKTHROUGH", ("model", "launch", "release", "benchmark", "open-source", "agent", "gpt", "claude", "gemini", "llama")),
    ("Startup Watch", "STARTUP WATCH", ("raises", "funding", "seed", "series a", "series b", "startup", "valuation", "yc ")),
    ("Corporate Intelligence", "CORPORATE INTEL", ("acquire", "acquisition", "merger", "earnings", "ceo", "partnership", "deal")),
    ("Market Movers", "MARKET MOVERS", ("market", "stocks", "shares", "price", "rates", "google", "update", "algorithm")),
    ("Hidden Opportunities", "HIDDEN OPPORTUNITY", ("opportunity", "demand", "growth", "underserved", "gap", "new tool")),
]

POSITIVE = {"launch", "launches", "raises", "growth", "record", "wins", "beats", "improves", "expands", "breakthrough", "partnership", "surge", "gains", "boost", "opens", "approves", "new"}
NEGATIVE = {"breach", "lawsuit", "falls", "drops", "cuts", "layoffs", "layoff", "ban", "fine", "warning", "decline", "risk", "outage", "hack", "probe", "loses", "delay", "crash", "vulnerability", "slump"}
HIGH_IMPACT = {"google", "openai", "microsoft", "apple", "nvidia", "amazon", "meta", "anthropic", "regulation", "eu", "billion", "core update", "acquisition", "fed"}

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")


def _clean(text: str | None, limit: int = 320) -> str:
    text = html.unescape(_TAG.sub(" ", text or ""))
    text = _WS.sub(" ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rsplit(" ", 1)[0] + "…"


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _child(node, *names: str) -> str | None:
    for name in names:
        for el in node.iter():
            if el.tag.split("}")[-1] == name:
                if name == "link" and el.get("href"):
                    return el.get("href")
                if el.text and el.text.strip():
                    return el.text
    return None


def parse_feed(xml_text: str) -> list[dict]:
    """Parse RSS 2.0 or Atom XML into raw entries."""
    root = ElementTree.fromstring(xml_text)
    items = [el for el in root.iter() if el.tag.split("}")[-1] in ("item", "entry")]
    entries = []
    for item in items:
        title = _clean(_child(item, "title"), 200)
        link = (_child(item, "link") or "").strip()
        if not title or not link.startswith("http"):
            continue
        entries.append({
            "title": title,
            "url": link,
            "summary": _clean(_child(item, "description", "summary", "content")),
            "published_at": _parse_date(_child(item, "pubDate", "published", "updated")),
            "publisher": _clean(_child(item, "source"), 60),
        })
    return entries


def _relative(dt: datetime | None, now: datetime) -> str:
    if not dt:
        return "Recent"
    minutes = max(0, int((now - dt).total_seconds() // 60))
    if minutes < 60:
        return f"{minutes} min ago"
    if minutes < 1440:
        return f"{minutes // 60} hours ago"
    days = minutes // 1440
    return "Yesterday" if days == 1 else f"{days} days ago"


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9][a-z0-9\-]+", text.casefold()))


def enrich(entry: dict, topic: str, source: str, quality: float, corroboration: int, now: datetime) -> dict:
    """Turn a raw feed entry into a scored signal card."""
    text = f"{entry['title']} {entry['summary']}".casefold()
    words = _words(text)
    pos, neg = len(words & POSITIVE), len(words & NEGATIVE)
    sentiment = "Negative" if neg > pos else "Positive" if pos > neg else "Neutral"

    age_h = (now - entry["published_at"]).total_seconds() / 3600 if entry["published_at"] else 48
    velocity_f = max(0.0, min(1.0, 1 - age_h / 168))  # fades over 7 days
    impact_hits = sum(1 for term in HIGH_IMPACT if term in text)
    impact_f = min(1.0, 0.45 + 0.15 * impact_hits + (0.1 if sentiment == "Negative" else 0))
    corroboration_f = min(1.0, corroboration / 4)

    signal_score = weighted_signal_score(quality, velocity_f, impact_f, corroboration_f)
    impact_score = round(impact_f * 100)
    confidence = round(min(97, 40 + quality * 35 + corroboration_f * 22))

    feed_category, category = "Emerging Trends", "EMERGING TRENDS"
    for fc, label, keys in CATEGORY_RULES:
        if any(k in text for k in keys):
            feed_category, category = fc, label
            break

    velocity = "Accelerating" if age_h < 12 else "Rising" if age_h < 48 else "Stable"
    business = "Critical" if impact_score >= 90 else "High" if impact_score >= 75 else "Medium" if impact_score >= 55 else "Low"
    publisher = entry.get("publisher") or source
    word_count = len(entry["summary"].split()) + 400
    return {
        "id": "live-" + hashlib.sha1(entry["url"].encode()).hexdigest()[:12],
        "title": entry["title"],
        "summary": entry["summary"] or "Open the source for the full story.",
        "category": category,
        "feed_category": feed_category,
        "topic": topic,
        "source": publisher if publisher == source else f"{publisher} · via {source}",
        "published": _relative(entry["published_at"], now),
        "published_at": entry["published_at"].isoformat() if entry["published_at"] else "",
        "reading_minutes": max(2, word_count // 220),
        "impact_score": impact_score,
        "signal_score": signal_score,
        "confidence_score": confidence,
        "velocity": velocity,
        "business_impact": business,
        "sentiment": sentiment,
        "url": entry["url"],
        "live": True,
    }


def _fetch(client: httpx.Client, url: str) -> list[dict]:
    response = client.get(url)
    response.raise_for_status()
    return parse_feed(response.text)


def fetch_signals(topics: list[str] | None = None, per_source: int = 12, timeout: float = 12.0) -> tuple[list[dict], list[str]]:
    """Fetch, de-duplicate, and score live signals. Returns (signals, errors)."""
    topics = [t for t in (topics or list(SOURCES)) if t in SOURCES] or list(SOURCES)
    jobs = [(topic, label, url, q) for topic in topics for (label, url, q) in SOURCES[topic]]
    now = datetime.now(timezone.utc)
    raw: list[tuple[str, str, float, dict]] = []
    errors: list[str] = []
    with httpx.Client(timeout=timeout, follow_redirects=True, headers={"User-Agent": USER_AGENT}) as client:
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = {pool.submit(_fetch, client, url): (topic, label, q) for topic, label, url, q in jobs}
            for future, (topic, label, q) in futures.items():
                try:
                    for entry in future.result()[:per_source]:
                        raw.append((topic, label, q, entry))
                except Exception as exc:  # one bad feed must not break the terminal
                    errors.append(f"{label}: {type(exc).__name__}")

    # corroboration = how many other stories share 3+ meaningful title words
    title_words = [{w for w in _words(e["title"]) if len(w) > 3} for *_, e in raw]
    signals, seen = [], set()
    for i, (topic, label, q, entry) in enumerate(raw):
        key = re.sub(r"\W+", "", entry["title"].casefold())[:80]
        if key in seen:
            continue
        seen.add(key)
        corroboration = sum(1 for j, other in enumerate(title_words) if j != i and len(title_words[i] & other) >= 3)
        signals.append(enrich(entry, topic, label, q, corroboration, now))
    signals.sort(key=lambda s: (s["signal_score"], s["published_at"]), reverse=True)
    return signals, errors


def topic_momentum(signals: list[dict]) -> dict[str, int]:
    """0-100 momentum per topic from live volume and average signal score."""
    if not signals:
        return {}
    by_topic: dict[str, list[float]] = {}
    for s in signals:
        by_topic.setdefault(s["topic"], []).append(s["signal_score"])
    peak = max(len(v) for v in by_topic.values())
    return {t: round(0.5 * (len(v) / peak) * 100 + 0.5 * (sum(v) / len(v))) for t, v in by_topic.items()}


def search(signals: list[dict], question: str, limit: int = 8) -> list[dict]:
    """Rank live signals by word overlap with a question (lightweight retrieval)."""
    q = {w for w in _words(question) if len(w) > 2}
    scored = []
    for s in signals:
        overlap = len(q & _words(f"{s['title']} {s['summary']} {s['topic']}"))
        if overlap:
            scored.append((overlap, s["signal_score"], s))
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return [s for *_, s in scored[:limit]] or signals[:limit]
