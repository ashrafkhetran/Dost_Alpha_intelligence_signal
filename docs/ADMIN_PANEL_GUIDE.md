# Admin panel guide

The current Admin Console is a readiness view and explicitly says integrations are not
connected. It is not an operational panel.

## Planned capabilities

- Source registry: enable/disable approved sources, refresh status, rights/retention
  metadata, errors, and takedown handling.
- Pipeline operations: job health, queue age, retries, deduplication, and replay controls.
- AI operations: provider/model configuration, spend caps, latency, groundedness
  evaluation, prompt/version rollout.
- Access support: user/org status, roles, deletion/export requests, and support actions.
- Billing support: verified subscription state, webhook event history, and reconciliation.
- Product health: service reliability, freshness, quality, cost, and support metrics.

## Authorization and audit

Restrict admin access with a separate permission, MFA, least privilege, and revalidation
for sensitive actions. Record actor, action, target, timestamp, request ID, and outcome;
never log secrets or unnecessary user content. Use confirmation and reversible actions
where possible. Do not let UI visibility replace backend authorization.

## Initial operational workflow

Review alert → inspect status/evidence → use documented repair/retry procedure → record
the incident/change → verify downstream freshness and customer impact. Separate support
read access from write/admin operations. Add customer-visible status and escalation paths
before claiming service guarantees.

Do not expose raw licensed source text, secrets, full prompts, payment details, or
cross-tenant data in the console.
