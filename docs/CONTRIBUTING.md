# Contributing

## Before changing code

Read the [application audit](APPLICATION_AUDIT.md), relevant architecture guide, and
the [roadmap](FEATURE_ROADMAP.md). Confirm whether behavior is implemented, demo-only,
or planned. Preserve clear demo/data provenance labels.

## Development workflow

1. Create a focused change with an explicit user outcome.
2. Keep UI, components, and business logic in their existing layers unless an approved
   architecture change is needed.
3. Add/update tests for the exact behavior, including validation and failure states.
4. Run targeted tests and relevant lint/type/build checks.
5. Update directly affected docs and changelog where appropriate.
6. Review accessibility, privacy, licensing, secret handling, and tenant authorization
   implications before merging.

## Quality expectations

- Never introduce fake metrics, placeholder citations presented as real, or success-shaped
  provider fallbacks.
- Validate external input and model output; surface actionable errors.
- Do not commit credentials, customer data, or licensed content.
- Keep database changes in versioned migrations once a migration system is selected.
- Test billing and authorization server-side; a disabled/hidden button is not enforcement.
- Keep changes small enough to review and provide reproducible verification steps.

## Documentation updates

Mark proposals as planned until implemented and verified. Date time-sensitive
competitor/pricing claims and cite public sources. Do not claim compliance, security
certification, live data coverage, or production readiness without evidence.
