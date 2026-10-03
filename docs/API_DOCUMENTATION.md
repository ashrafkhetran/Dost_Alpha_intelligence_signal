# API documentation (planned)

No application HTTP API is implemented in this repository. These endpoints describe a
future backend contract; they are not callable endpoints today.

## Conventions

- HTTPS only; authenticated requests use the backend's verified identity context.
- JSON request/response; UTC ISO-8601 timestamps; opaque UUIDs.
- Cursor pagination, bounded page size, stable ordering, request IDs, and consistent
  error envelopes.
- Never trust client-provided `user_id`, plan, entitlement, or citation URL.

## Proposed routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/v1/signals` | Filter/paginate authorized intelligence |
| GET | `/v1/signals/{signal_id}` | Signal plus source provenance |
| PUT/DELETE | `/v1/saved-signals/{signal_id}` | Save or remove a user's signal |
| GET/PUT | `/v1/preferences` | Read/update personal topics and digest settings |
| POST | `/v1/analyst-runs` | Submit a bounded, entitlement-checked analysis |
| GET | `/v1/analyst-runs/{run_id}` | Retrieve run status, answer, and evidence |
| POST | `/v1/reports` | Create a supported briefing |
| GET | `/v1/reports/{report_id}` | Retrieve an owned report |
| POST | `/v1/billing/checkout-session` | Create hosted checkout using server-owned price mapping |
| POST | `/v1/webhooks/stripe` | Verify and process Stripe events |

## Example Analyst request

```json
{
  "question": "What should SEO teams monitor this week?",
  "topic_ids": ["seo"],
  "time_range": {"from": "2026-09-26T00:00:00Z", "to": "2026-10-03T00:00:00Z"}
}
```

The backend should validate length, filters, permissions, and quota. An accepted request
may return `202 Accepted` with a run ID if asynchronous.

## Error envelope

```json
{
  "error": {
    "code": "insufficient_evidence",
    "message": "There is not enough current evidence for this question.",
    "request_id": "opaque-request-id"
  }
}
```

Use appropriate 400/401/403/404/409/422/429/5xx status codes. Avoid disclosing whether
another user's private record exists. Keep webhook signature errors distinct in logs,
not in publicly verbose responses.
