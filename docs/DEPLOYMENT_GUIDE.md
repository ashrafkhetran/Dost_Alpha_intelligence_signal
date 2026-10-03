# Deployment guide

## Current prototype

The checked-in `Dockerfile` packages the Streamlit app on port 8501 and includes a
Streamlit health check. The app can also be run locally using the root `README.md`
instructions. Deployment does not configure a database, authentication, source feeds,
worker, Stripe, or secret values.

## Production deployment sequence

1. Choose an environment and hosting model; isolate development, staging, and production.
2. Pin and scan dependencies; build an immutable container and produce an SBOM.
3. Configure HTTPS, domain, health/readiness checks, resource limits, and restricted
   network access.
4. Provision managed PostgreSQL, backups, encryption, private connectivity, and tested
   restore procedures.
5. Store provider credentials in the platform secret manager. Never commit real secrets
   or use `.streamlit/secrets.toml` in a public repository.
6. Apply reviewed, versioned migrations before deploying app/worker versions that
   depend on them.
7. Deploy the web process and background workers separately; configure safe job retries,
   dead-letter visibility, and concurrency limits.
8. Configure approved source connectors, rights and refresh schedules only after review.
9. Configure model provider limits and Stripe webhook endpoint in test mode; test all
   lifecycle scenarios before production keys.
10. Enable metrics, logs, alerts, rollback, support, and incident runbooks.

## Release checks

- Automated unit/integration/security tests pass; secrets scan is clean.
- Health endpoint and user-critical flows work in staging.
- Database backup can be restored; migration and rollback/recovery procedures are known.
- Auth boundaries, tenant scoping, entitlements, webhook replay, and quotas pass tests.
- No sample data is labeled as live; error and stale states are visible.
- Responsible owner approves release and has rollback access.

## Operations

Monitor uptime, request/job errors, ingestion freshness, citation quality, model spend,
webhook lag, database saturation, and support reports. Establish SLOs from observed
baselines and maintain a rollback path. Streamlit Cloud may suit a demonstration; select
production hosting based on the required API, worker, data residency, network, and
operational controls.
