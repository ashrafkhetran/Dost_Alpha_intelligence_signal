# Feature roadmap

This roadmap is an implementation proposal, not a delivery promise. Each phase ends
with a decision gate; validate value and operational readiness before broadening scope.

## Phase 0 — Validate the problem (now)

- Interview founders, operators, SEO practitioners, and analysts separately.
- Operate a manually curated sample briefing with explicit source attribution.
- Test the core job, terminology, source trust, and proposed prices.
- Define source licensing and initial coverage boundary.

**Gate:** repeated target-user use and evidence that a narrow workflow is valuable.

## Phase 1 — Trustworthy intelligence foundation

- Select and approve initial sources; build ingestion, normalization, canonicalization,
  deduplication, provenance, refresh status, and takedown support.
- Introduce PostgreSQL migrations and durable source/signal/report records.
- Define score semantics, score explanations, and human review/evaluation.
- Keep all prototype fixtures clearly marked as demo.

**Gate:** source freshness, duplicate handling, reproducible scoring, and user-visible
evidence pass acceptance tests.

## Phase 2 — Identity and personal workspace

- Integrate managed identity and server-side authorization.
- Persist preferences, saved signals, watchlists, and reports with tenant isolation.
- Add account deletion/export and privacy retention policies.

**Gate:** authorization tests prove cross-account data access is denied.

## Phase 3 — Evidence-grounded Analyst and briefings

- Build permission-aware retrieval and citation-bearing answer schema.
- Add groundedness/citation evaluation, abstention, provider budgets and audit metadata.
- Generate briefings from cited evidence; support reviewed exports and source inspection.

**Gate:** evaluation suite establishes an agreed citation-support threshold and safe
abstention behavior before general access.

## Phase 4 — Paid plans and operational readiness

- Implement Stripe Checkout/Portal and idempotent webhook reconciliation.
- Enforce persisted entitlements and usage limits server-side.
- Add monitoring, cost controls, support workflows, runbooks, backups, restore, and
  release rollback.

**Gate:** test-mode lifecycle and failure scenarios pass; privacy, legal, security, and
support reviews are complete.

## Phase 5 — Expansion

- Add validated trend radar, opportunity workflows, more sources, and team collaboration.
- Consider enterprise API, custom sources, SSO, and white-label only with customer demand.

**Gate:** core product retains users and source/model costs support sustainable margins.

## Prioritization

Fix trust and data provenance before adding more AI features. Resolve identity and
authorization before billing. Resolve billing correctness before launching paid plans.
