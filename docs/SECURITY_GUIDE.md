# Security guide

This guide is an implementation baseline, not a security certification or penetration
test. The prototype is not configured for production multi-user or paid use.

## Assets and trust boundaries

Assets include account identities, prompts, preferences, saved intelligence, licensed
source material, reports, provider keys, billing references, and usage records. Trust
boundaries include browser/UI to backend, third-party feeds to ingestion, retrieved
content to the Analyst model, application to model/payment providers, and admin actions
to customer data.

## Minimum controls

- **Secrets:** secret manager, least-privilege keys, rotation, redaction, and scanning.
- **Identity:** maintained OIDC provider, verified claims, protected sessions, secure
  recovery, MFA for privileged access.
- **Authorization:** server-side role/tenant checks on every operation; deny by default;
  tests for horizontal and vertical privilege escalation.
- **Data:** TLS, encrypted storage/backups, minimization, retention/deletion, tested
  restore, approved source licensing.
- **Webhooks:** raw-body signature verification, event deduplication, replay protection,
  bounded parsing, transactional state updates.
- **AI:** prompt-injection defense, input/output limits, citation validation, retrieval
  ACLs, provider budgets, safe abstention, and sensitive-data policy.
- **Application:** dependency updates/scanning, output escaping, input validation,
  CSRF/rate limits where relevant, secure headers, error redaction.
- **Operations:** audit events for privileged changes, alerts, incident response, access
  reviews, vulnerability reporting and recovery drills.

## Launch gate

Complete a threat model; resolve high-risk findings; test auth, tenant isolation,
webhook replay, deletion, secrets handling, and AI retrieval boundaries; review privacy,
source rights, and applicable legal requirements. Do not place private credentials in
Streamlit widgets, source files, or client-visible output.
