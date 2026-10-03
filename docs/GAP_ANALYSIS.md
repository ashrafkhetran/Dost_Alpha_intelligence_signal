# Gap analysis

| Capability | Prototype today | Needed for production | Priority |
|---|---|---|---|
| Intelligence data | Hard-coded sample signals; placeholder links | Licensed/approved sources, ingestion, dedupe, provenance, freshness, takedown workflow | P0 |
| Signal scoring | Deterministic weighted helper | Documented features, calibration, explainability, confidence validation, drift review | P0 |
| Analyst | Optional OpenRouter call without retrieval | Permission-aware retrieval, citations, evaluation, limits, uncertainty, audit trail | P0 |
| User identity | No sign-in | Identity provider, account lifecycle, session security, tenant isolation | P0 |
| Persistence | In-memory/session state | Migrations, production database, backup/restore, durable preferences and reports | P0 |
| Plans | Static comparison | Entitlement catalog, usage accounting, checkout, verified webhook lifecycle | P1 |
| API/workers | Not present | Authenticated API, async jobs, retries, rate limits, scheduled ingestion | P1 |
| Briefings | Fixed sample text with file export | Evidence-grounded generation, saved report ownership, provenance and retention | P1 |
| Admin | Readiness display | RBAC, source operations, audit logs, support-safe user controls | P1 |
| Delivery | Dockerfile only | CI, deployment environments, secrets, migrations, monitoring, rollback, incident playbooks | P1 |
| Quality | Service unit tests | Integration, tenant authorization, webhook replay, retrieval evaluation, accessibility | P1 |
| Enterprise | Plan placeholder | Team seats, organization isolation, policy controls, API keys, contracts and support | P2 |

## Product gaps

- Validate that users value prioritized signals and evidence more than a larger news
  volume before investing in breadth.
- Define what "confidence", "impact", "velocity", and "opportunity" mean, how they are
  calculated, and when they are unavailable.
- Specify source update expectations, geographic/language coverage, licensing, and
  corrections.
- Reconcile the stated Free cap of five reports/month with the app's current
  non-persistent sample briefing behavior.
- Validate willingness to pay and the proposed prices with interviews and a manually
  operated pilot; do not treat competitor positioning as pricing evidence.

## Architecture gaps

- Separate user-facing Streamlit interaction from durable services and background work
  when scale or reliability requires it.
- Add schema migrations, transaction boundaries, tenant scoping, backups, and tested
  restore procedures.
- Add an entitlement service as the single source of access truth; never gate only in UI.
- Protect model and feed providers with budgets, timeouts, retries, and observability.
- Establish a documented service-level objective only after operational baselines exist.

## Release criteria

Before inviting paid users: verified citations for every evidence-based analyst claim;
source rights review; identity and authorization tests; billing lifecycle/webhook replay
tests; durable storage and restore test; abuse/spend limits; privacy and terms review;
alerting, rollback, and support playbooks; and explicit product limits/disclosures.
