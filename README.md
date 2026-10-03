# DOST ALPHA

**AI Intelligence Terminal**  
*Signal Over Noise. Intelligence Over Information.*

Product, architecture, security, deployment, and implementation documentation:
[docs/README.md](docs/README.md).

## Project tree

```text
DOST_ALPHA/
├── app.py                       # Streamlit entry point and page router
├── assets/
│   └── styles.css               # Responsive dark terminal design system
├── components/
│   ├── __init__.py
│   ├── layout.py                # Sidebar, navigation, and page headings
│   └── signals.py               # Reusable, escaped signal card
├── database/
│   └── schema.sql               # PostgreSQL + pgvector initial schema
├── pages/
│   ├── __init__.py
│   ├── admin.py                 # Integration readiness console
│   ├── ai_analyst.py            # Transparent deterministic analyst prototype
│   ├── briefings.py             # Brief template and Markdown/HTML/PDF exports
│   ├── dashboard.py             # Overview and sample executive brief
│   ├── intelligence_feed.py     # Search, topic, and impact filters
│   ├── saved_intelligence.py    # Session-scoped saved signals
│   ├── settings.py              # Session-scoped personalization
│   ├── subscription.py          # Free / Pro / Alpha plan presentation
│   └── trend_radar.py           # Plotly sector radar and momentum view
├── services/
│   ├── __init__.py
│   ├── analyst.py               # Sample analysis and briefing text
│   ├── demo_data.py             # Clearly identified illustrative data
│   ├── export.py                # Printable PDF report export
│   └── scoring.py               # Validated score and outlook primitives
├── tests/
│   └── test_services.py         # Scoring, analyst, and export tests
├── .env.example                 # Integration variable names (no secrets)
├── .gitignore
├── .streamlit/config.toml       # Streamlit theme and server settings
├── Dockerfile
└── requirements.txt
```

DOST ALPHA turns source material into ranked, evidence-led intelligence. This workspace is the first runnable Streamlit prototype: it includes an interactive premium-style dashboard and sample signals, with every simulated metric and response explicitly labeled. The AI Analyst can call OpenRouter when configured, but has no retrieval or live-source connection. Live ingestion, user authentication, and payment processing are not implemented.

## OpenRouter key

The AI Analyst reads `OPENROUTER_API_KEY` from the environment or `.streamlit/secrets.toml`. A local secrets file is ignored by `.gitignore`; never commit it or paste keys into source code. The configured Analyst uses OpenRouter's chat-completions API with `openai/gpt-4o-mini` and returns validated structured JSON. If no key is configured, the clearly labeled sample Analyst remains available. Provider failures are shown to the user rather than replaced with sample output.

The model is not connected to retrieval or live news in this prototype, and it does not provide source citations. Treat generated analysis as unverified and check primary sources.

## Run locally

Python 3.10+ is recommended.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

These commands use the project's virtual environment directly, so they work even when the active `(base)` Conda environment does not have Streamlit installed. Alternatively, activate `.venv` first and then use `python -m streamlit run app.py`.

Run service tests with `python -m pytest`.

## Product and visual direction

- **Positioning:** a personal intelligence terminal for founders, investors, operators, SEO professionals, and researchers—not a chronological news reader.
- **Design:** dark-first surfaces (`#0B0F19`, `#121826`), restrained violet and cyan accents, compact mono labels for metrics, clear source/evidence hierarchy, and responsive cards.
- **Homepage:** hero promise and workspace state, sample signal metrics, prioritized intelligence cards, and a concise executive takeaway.
- **Sidebar:** persistent destinations for Overview, Intelligence Feed, AI Analyst, Trend Radar, Briefings, Saved Intelligence, Subscription, Settings, and Admin Console, plus an explicit demo-workspace marker.
- **Responsive behavior:** Streamlit columns reflow naturally; CSS reduces padding and hides the decorative orbit on narrow screens. Charts retain Plotly's responsive width.
- **Interaction:** feed search/category/impact/topic filters, in-session bookmarking, analyst question input, briefing Markdown/HTML/PDF downloads, topic preferences, and plan exploration.

## User flows

```text
DISCOVER
Dashboard → inspect ranked signals → open source → save signal → Saved Intelligence

RESEARCH
AI Analyst → ask a focused question → review summary / insights / risks / actions
          → validate against cited primary sources (required in production)

BRIEF
Choose briefing type → generate → review → export Markdown, HTML, or PDF

PERSONALIZE
Settings → choose topics and digest cadence → filtered Intelligence Feed

CONVERT
Free experience → plan comparison → hosted Stripe Checkout → signed webhook
               → persisted subscription entitlement → gated product capabilities
```

## Application architecture

```text
Streamlit presentation (app.py, pages/, components/)
              │
              ├── service interfaces (ingestion, scoring, retrieval, reporting)
              │        ├── RSS/custom feed connectors + scheduled workers
              │        ├── deduplication, entity extraction, trend scoring
              │        └── provider adapters (OpenAI / Anthropic / Gemini)
              │
              ├── PostgreSQL + pgvector (users, sources, signals, embeddings, reports)
              ├── Auth boundary (Google/GitHub OAuth or email identity)
              └── Stripe boundary (hosted checkout, signed webhooks, entitlements)
```

The prototype keeps view code in `pages/`, reusable UI in `components/`, provider-neutral business logic in `services/`, and the initial relational model in `database/`. Sample/demo services are deliberately isolated so a production adapter can replace them without labeling mock output as live intelligence. For a multi-user production system, run ingestion and long-running AI work in separate API/worker processes; do not rely on Streamlit session state as a database or job queue.

### Streamlit component map

| Surface | Responsibility |
|---|---|
| `components/layout.py` | Navigation and shared page heading |
| `components/signals.py` | Escaped, reusable intelligence-card markup and save interaction |
| `pages/dashboard.py` | Product overview and executive summary |
| `pages/intelligence_feed.py` | Personalized filtering and discovery |
| `pages/ai_analyst.py` | Research prompt and structured analysis |
| `pages/trend_radar.py` | Plotly radar and momentum scores |
| `pages/briefings.py` | Brief formats and Markdown/HTML/PDF export |
| `pages/saved_intelligence.py` | Saved intelligence library |
| `pages/subscription.py` | Plan comparison and upgrade entry point |
| `pages/settings.py` | Topics, watch keywords, digest preferences |
| `pages/admin.py` | Operational integration readiness |

## Data pipeline and signal quality

```text
RSS / licensed feeds / custom sources
  → validate and normalize records
  → deduplicate canonical URLs and near-duplicate text
  → extract entities and topic candidates
  → summarize with source citations
  → sentiment + event classification (uncertainty retained)
  → cluster recurrence and calculate velocity
  → score impact, source quality, corroboration, and confidence separately
  → personalize and rank signals
  → cited feed, analyst, and briefings
```

`services/scoring.py` is only a validated weighted-score primitive, not a trained market model. The illustrative weights are source quality 25%, velocity 30%, impact 30%, and corroboration 15%. Sample outlook colors label negative sentiment as **Risk**, high-impact positive signals as **Opportunity**, and other signals as **Watch**; this is a UI demonstration, not a validated recommendation engine. Calibrate and review classifications before using for investment or business decisions. Store model/provider versions and evidence links with generated reports.

## Subscription and Stripe integration plan

| Plan | Intended entitlements |
|---|---|
| Free — $0 | 5 reports/month, basic summaries, limited categories |
| Pro — $9/month | Unlimited reports, advanced filters, trend analysis, PDF export, saved reports |
| Alpha — $29/month | AI Analyst, executive briefings, opportunity detection, deep research, daily intelligence, priority processing |

Prices and features are a product proposal, not active billing. Production implementation should:

1. Create recurring Stripe Prices server-side and store their IDs in environment-backed configuration.
2. Start Stripe Checkout from an authenticated backend endpoint; never accept client-supplied price/role as authority.
3. Verify webhook signatures, persist event IDs for idempotency, and update subscription state transactionally.
4. Derive access from persisted entitlements and subscription status, not a UI selection or success redirect.
5. Handle renewals, cancellation, past-due states, refunds, and customer-portal changes; test in Stripe test mode.
6. Keep keys in a secret manager and expose no secret values in Streamlit/browser code.

## Database and identity

`database/schema.sql` provides an initial PostgreSQL model for users, source registry, normalized signals, source citations, user preferences, saved signals, reports, and Stripe subscription references. It enables pgvector for embeddings. The embedding size (1536) must match the selected embedding model; manage this and schema changes through versioned migrations in production.

Use an established OAuth/email identity provider or a backend auth service for Google, GitHub, and email login. Store provider identities and roles server-side; use secure session cookies, CSRF protections, verified email, account deletion, and role-based authorization. The current app has no sign-in and is intended for local single-user evaluation only.

## Mobile, accessibility, and conversion

- Keep one clear primary action per screen and a concise signal summary before detail.
- Preserve source attribution and separate fact, inference, confidence, and recommendation.
- Make compact metrics readable at mobile widths; avoid using color as the only risk cue.
- Conversion path: useful free overview → visible evidence and time saved → contextual upgrade prompt only when an Alpha/Pro capability is requested → transparent plan comparison → hosted secure checkout.
- Measure activation (first followed topic and saved signal), repeat use, brief completion, source-click rate, upgrade intent, and paid retention. Do not optimize on page views alone.
- Before charging, validate signal usefulness with target-user interviews and manually reviewed examples; document limits and cancellations clearly.

## Deployment

`Dockerfile` runs the Streamlit prototype on port 8501 and includes a health check. For deployment, set secrets in the hosting platform, pin and scan dependencies, use HTTPS, and configure a persistent production database and separate ingestion worker. Streamlit Cloud is suitable for a UI prototype; Railway or Render can host the container, API, workers, and database when configured. This scaffold does not deploy itself or include production credentials.

## Current limitations

- All stories, score values, and dashboard metrics are illustrative; source URLs point to a placeholder domain.
- No RSS collector, scheduler, deduplication pipeline, entity extraction, embeddings, or live data store is connected.
- Analyst and briefing content is a deterministic sample, not RAG or model output.
- Authentication, durable user preferences, subscriptions, Stripe, and admin operations are not implemented.
- Save state is per Streamlit session and is not durable across sessions/devices.
