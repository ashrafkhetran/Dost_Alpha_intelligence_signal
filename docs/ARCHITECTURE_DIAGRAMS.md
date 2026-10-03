# Architecture diagrams

Mermaid diagrams here are design proposals. The [editable Draw.io diagram](diagrams/DOST_ALPHA_Architecture.drawio)
shows the same target boundaries. The existing app remains the prototype described in
the [audit](APPLICATION_AUDIT.md).

## System context

```mermaid
flowchart TB
  USER[Professional user] --> WEB[Streamlit workspace]
  WEB --> APP[Authenticated application services]
  APP --> IDP[Identity provider]
  APP --> DB[(PostgreSQL + vector search)]
  APP --> QUEUE[Background job queue]
  QUEUE --> INGEST[Ingestion / normalization workers]
  INGEST --> SOURCES[Approved feeds and licensed sources]
  INGEST --> DB
  APP --> ANALYST[Retrieval-grounded analyst]
  ANALYST --> DB
  ANALYST --> MODEL[Model provider]
  STRIPE[Stripe] --> HOOK[Signed webhook handler]
  HOOK --> APP
  OPS[Monitoring / audit / alerts] --- APP
  OPS --- INGEST
```

## Signal lifecycle

```mermaid
flowchart LR
  A[Approved source] --> B[Fetch with rate and rights policy]
  B --> C[Validate and normalize]
  C --> D{Duplicate?}
  D -- Yes --> E[Link source to existing record]
  D -- No --> F[Store immutable source evidence]
  E --> G[Cluster and extract candidate signal]
  F --> G
  G --> H[Score with versioned rules]
  H --> I[Quality and provenance review]
  I --> J[Publish with freshness and citations]
  I --> K[Quarantine / correct / takedown]
```

## Paid entitlement

```mermaid
flowchart LR
  U[Authenticated user] --> C[Checkout request]
  C --> P[Server selects configured Price]
  P --> S[Stripe hosted checkout]
  S --> W[Signed webhook]
  W --> V[Verify signature + dedupe event]
  V --> DB[(Persist subscription state)]
  DB --> E[Entitlement resolver]
  E --> F[Protected feature]
  S -. Redirect is not authority .-> F
```
