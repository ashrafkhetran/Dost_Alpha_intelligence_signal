# DOST ALPHA documentation

**Signal Over Noise. Intelligence Over Information.**

This directory is the product, architecture, and delivery baseline for evolving the
existing Streamlit prototype into a trustworthy intelligence product. It distinguishes
verified current behavior from proposals; plans and architecture described here are not
claims that those integrations are already deployed.

## Start here

1. [Application audit](APPLICATION_AUDIT.md) — observed codebase and prototype limits.
2. [Gap analysis](GAP_ANALYSIS.md) — current state versus production requirements.
3. [Project vision](PROJECT_VISION.md) and [product strategy](PRODUCT_STRATEGY.md).
4. [Feature roadmap](FEATURE_ROADMAP.md) and [implementation tasks](IMPLEMENTATION_TASKS.md).
5. [Technical architecture](TECHNICAL_ARCHITECTURE.md), [API plan](API_DOCUMENTATION.md),
   and [database schema](DATABASE_SCHEMA.md).
6. [Wireframes](WIREFRAMES.md), [mockup descriptions](UI_MOCKUPS.md), and
   [UI/UX guidelines](UI_UX_GUIDELINES.md).
7. [Deployment guide](DEPLOYMENT_GUIDE.md) and [security guide](SECURITY_GUIDE.md).

## Document index

| Document | Purpose |
|---|---|
| [APPLICATION_AUDIT.md](APPLICATION_AUDIT.md) | Code-backed application audit |
| [GAP_ANALYSIS.md](GAP_ANALYSIS.md) | Current/proposed capability comparison |
| [PROJECT_VISION.md](PROJECT_VISION.md) | Mission, audience, positioning, principles |
| [PRODUCT_STRATEGY.md](PRODUCT_STRATEGY.md) | Product bets, validation, success metrics |
| [BUSINESS_MODEL.md](BUSINESS_MODEL.md) | Revenue hypotheses and monetization |
| [SUBSCRIPTION_MODEL.md](SUBSCRIPTION_MODEL.md) | Proposed tiers and entitlement rules |
| [UI_UX_GUIDELINES.md](UI_UX_GUIDELINES.md) | Interaction patterns and wireframes |
| [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) | Visual tokens and component guidance |
| [FEATURE_ROADMAP.md](FEATURE_ROADMAP.md) | Phases, gates, and sequencing |
| [COMPETITOR_ANALYSIS.md](COMPETITOR_ANALYSIS.md) | Positioning landscape and research caveats |
| [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) | Current and target system boundaries |
| [AI_ANALYST_ARCHITECTURE.md](AI_ANALYST_ARCHITECTURE.md) | Retrieval-grounded analyst design |
| [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) | Existing schema review and proposed evolution |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Proposed API contract (not implemented) |
| [AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md) | Identity and authorization implementation guide |
| [STRIPE_INTEGRATION.md](STRIPE_INTEGRATION.md) | Billing and webhook implementation guide |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Prototype and production deployment outline |
| [SECURITY_GUIDE.md](SECURITY_GUIDE.md) | Threats, controls, and launch requirements |
| [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md) | Planned operational console |
| [CHANGELOG.md](CHANGELOG.md) | Documentation and product change history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributor workflow and quality expectations |
| [WIREFRAMES.md](WIREFRAMES.md) | Low-fidelity workspace wireframes |
| [UI_MOCKUPS.md](UI_MOCKUPS.md) | Screen-by-screen visual mockup descriptions |
| [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) | Mermaid system, analyst, and billing flows |
| [IMPLEMENTATION_TASKS.md](IMPLEMENTATION_TASKS.md) | Ordered implementation backlog |

An editable architecture diagram is provided at
[`diagrams/DOST_ALPHA_Architecture.drawio`](diagrams/DOST_ALPHA_Architecture.drawio).
The root [`DOST_ALPHA_Flowchart.drawio`](../DOST_ALPHA_Flowchart.drawio) is the
pre-existing prototype flowchart.

## Status vocabulary

- **Implemented:** present in the checked-in prototype.
- **Planned:** design or integration guidance only; do not infer deployed behavior.
- **Decision required:** a product, legal, or technical choice that needs validation.

No authentication, durable multi-user persistence, live source ingestion, production
retrieval, Stripe checkout, or paid entitlements are implemented in this prototype.
