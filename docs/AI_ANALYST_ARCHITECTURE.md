# AI Analyst architecture

## Current state

`services/analyst.py` can request structured JSON from OpenRouter when configured, or
return a deterministic sample answer otherwise. Neither route retrieves live sources or
provides citations. The UI labels both states. Treat all output as unverified.

## Proposed request flow

```mermaid
sequenceDiagram
  actor User
  participant UI as Analyst UI
  participant API as Analyst API
  participant ACL as Authorization and entitlements
  participant R as Retrieval
  participant DB as Evidence store
  participant M as Model adapter
  User->>UI: Submit scoped question
  UI->>API: Question + selected filters
  API->>ACL: Verify identity, tenant, plan, quota
  ACL-->>API: Authorized context
  API->>R: Retrieve permitted evidence
  R->>DB: Search filtered corpus
  DB-->>R: Dated source passages and metadata
  R-->>API: Ranked evidence with stable IDs
  API->>M: Question + bounded evidence context
  M-->>API: Structured answer with evidence IDs
  API->>API: Validate schema and citation references
  API-->>UI: Answer, citations, caveats, provenance
  UI-->>User: Inspect claim and original source
```

## Response contract

Return summary; key claims each mapped to one or more evidence IDs; risks/uncertainties;
recommended verification steps; retrieval time/window; model identifier; and an explicit
status (`grounded`, `partial`, `insufficient_evidence`, or `error`). Do not accept model
invented URLs or evidence identifiers. Resolve citations from server-side retrieved
records. If material claims lack support, abstain or label them as hypotheses.

## Quality and safety

- Defend against prompt injection in retrieved documents; source text is data, not
  instruction.
- Apply access filters before retrieval and test cross-tenant isolation.
- Limit input/output tokens, request rate, concurrency, retries, and cost per user.
- Evaluate citation entailment, completeness, freshness, contradiction handling,
  refusal/abstention, latency, and consistency using a reviewed test set.
- Version prompts, models, retrieval configuration, and evaluation results.
- Keep human review available for executive or high-impact reports.
- Never represent generated business analysis as guaranteed outcome or investment advice.

## Rollout

Begin with offline evaluation and internal review, then limited opt-in beta. Keep the
current sample mode visibly distinct; do not present it as live research. Gate general
availability on agreed evaluation thresholds and incident/cost controls.
