# Application audit

**Scope:** read-only review of the repository at the time these documents were created.
This is a codebase audit, not a live-site penetration test or verification of the
public Streamlit deployment.

## Executive summary

DOST ALPHA is a runnable, polished, multi-page Streamlit prototype. It demonstrates the
intended dark intelligence-terminal experience and several interaction patterns. It is
not yet a multi-user intelligence service: sample records and metrics are hard-coded,
user state is held in Streamlit session state, and identity, durable storage, ingestion,
retrieval, and billing are not connected.

## Observed implementation

| Area | What exists | Important boundary |
|---|---|---|
| UI and routing | `app.py`, `pages/`, `components/`, responsive dark CSS, nine destinations | One Streamlit process; no tenant-aware backend |
| Feed | Category, topic, text, and impact filters | Static `services/demo_data.py`; source URLs use `example.com` |
| Signal scoring | Validated weighted score and outlook helper in `services/scoring.py` | Formula is a prototype primitive; not trained or calibrated |
| Trend radar | Plotly chart from hard-coded category values | Values do not measure live momentum |
| Analyst | OpenRouter structured response when key is configured; deterministic response otherwise | Neither path has retrieval, live news grounding, or citations |
| Briefings | Sample template and Markdown, HTML, and PDF downloads | Content is illustrative, not generated from current intelligence |
| Personalization | Followed topics, saves, and settings in Streamlit session state | Not durable across browser sessions/devices |
| Plans | Free, Pro ($9), Alpha ($29) presentation | No checkout, subscription records, or entitlement enforcement |
| Admin | Integration-readiness panel | Not an operational admin system |
| Persistence | PostgreSQL + pgvector starting schema | No connected repository/migration runner observed |
| Deployment | Dockerfile and Streamlit configuration | No production secrets, database, worker, or release pipeline included |
| Tests | Service tests for scores, analyst response validation/errors, and PDF output | No end-to-end, auth, billing, ingestion, or deployed-system tests |

## Strengths

- Clear product premise and coherent page structure; UI and business logic are separated
  into pages, components, and services.
- Static/demo data and model output are explicitly labeled, avoiding a false claim of
  live market coverage.
- Analyst provider failures surface instead of silently returning sample answers.
- Structured model output is validated, external links are escaped in signal cards, and
  score inputs are range-checked.
- Starting schema, container, environment-variable template, and service tests provide
  useful foundations for staged implementation.

## Material risks and limitations

1. Do not market sample volumes, scores, timestamps, sources, or briefings as real-time
   intelligence.
2. A configured LLM can produce plausible but unsupported output; it is not grounded in
   a retrievable evidence corpus and emits no citations.
3. Session state is not an identity boundary, durable store, or authorization mechanism.
4. Plan labels do not limit access. There is no payment or subscription lifecycle.
5. The SQL file is a starting PostgreSQL schema, not a migration history or proof the
   schema has been applied. Billing and auth are not wired to it.
6. No operational controls for source licensing, takedowns, freshness, abuse, privacy,
   spend limits, or incident response were found in the prototype.

## Audit disposition

Keep the app as the UI prototype and preserve its explicit demo mode. Do not begin paid
launch or describe the app as a live intelligence terminal until source provenance,
retrieval quality, durable user identity, access control, billing correctness, and
operational monitoring have passed their launch gates. See the [gap analysis](GAP_ANALYSIS.md)
and [roadmap](FEATURE_ROADMAP.md).
