# Implementation tasks

Ordered backlog. Tasks should be split into reviewed changes with acceptance tests; this
is not an authorization to launch all features without validation.

## Phase 0 — Product and data validation

- [ ] Interview each target segment and choose one initial decision workflow.
- [ ] Run a manually curated, explicitly labeled pilot briefing.
- [ ] Decide initial topics, source coverage, freshness target, and source-rights policy.
- [ ] Define signal, impact, confidence, velocity, opportunity, and correction semantics.
- [ ] Test proposed pricing and benefit comprehension.

## Phase 1 — Evidence foundation

- [ ] Define source connector interface and licensed-source registry.
- [ ] Build fetch, validation, normalization, canonical URL, deduplication, and retry jobs.
- [ ] Persist source documents and provenance via versioned database migrations.
- [ ] Add freshness, source health, correction, and takedown workflows.
- [ ] Define score calculation, version metadata, evaluation dataset, and user-facing
  explanations.
- [ ] Replace placeholder content only when the source pipeline passes quality gates.

## Phase 2 — Identity and durable workspace

- [ ] Select identity provider and define stable subject/account-link policy.
- [ ] Add authenticated backend context and role/tenant authorization.
- [ ] Persist preferences, saves, watchlists, and report ownership.
- [ ] Add user export/deletion and retention controls.
- [ ] Add cross-user isolation tests for every data-access path.

## Phase 3 — AI Analyst and briefings

- [ ] Implement permission-filtered retrieval and stable evidence IDs.
- [ ] Define structured claim/citation/uncertainty response schema and validation.
- [ ] Add prompt-injection safeguards, abstention, token/cost/rate limits.
- [ ] Build groundedness/citation/freshness evaluation and human review.
- [ ] Generate, store, and export cited briefs with provenance metadata.

## Phase 4 — Billing and launch readiness

- [ ] Finalize tier entitlements, usage windows, limits, cancellation, refunds, and terms.
- [ ] Implement server-created Stripe checkout and customer portal.
- [ ] Implement signed, idempotent, transactional webhook state reconciliation.
- [ ] Enforce entitlements at service boundaries and maintain a usage ledger.
- [ ] Test payment lifecycle, replay, failure, quota, and recovery cases.
- [ ] Add production CI, dependency/security scans, staging, monitoring, backups, restore,
  incident response, and rollback.

## Phase 5 — Validated expansion

- [ ] Add trend views grounded in documented time-series data.
- [ ] Add competitive intelligence and opportunity workflows after user validation.
- [ ] Design organizations, seats, shared workspaces, API access, and custom sources only
  after enterprise discovery.
