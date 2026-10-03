# Subscription model

All tiers below are proposed. The prototype shows Free, Pro, and Alpha cards but has no
authentication, checkout, usage ledger, or enforced plan entitlements.

| Tier | Proposed price | Proposed value |
|---|---:|---|
| Free | $0 | 5 reports/month, basic intelligence feed, limited AI summaries |
| Pro | $9/month | Unlimited reports, advanced signals, trend radar, PDF exports, saved reports |
| Alpha | $29/month | AI Analyst, executive briefings, opportunity detection, deep research, competitive intelligence, watchlists, priority processing |
| Enterprise | Custom | Team seats, shared intelligence, custom sources, API access, white-label reports |

## Entitlement model

Represent access as named capabilities and limits, not plan-name checks in page code.
Example keys: `reports.monthly_limit`, `analyst.enabled`, `watchlists.limit`,
`exports.pdf`, `sources.custom`, `api.enabled`, `seats.limit`. Resolve from persisted,
server-owned subscription state on every protected operation.

## Usage and lifecycle rules to decide

- Define report counting (successful generation, not retries), timezone, reset period,
  and behavior at limit.
- Define fair-use controls for "unlimited" generation and model cost protection.
- Define grace periods, payment failure, cancellation effective date, refunds, trial,
  proration, and plan changes.
- Enterprise terms, seat changes, and access on contract expiry require explicit policy.

## Upgrade journey

Feature explanation → transparent tier comparison → authenticated hosted checkout →
verified payment event → persisted entitlement → confirmation and receipt. Checkout
redirect alone must never grant paid capabilities. See [Stripe integration](STRIPE_INTEGRATION.md).

## Launch guardrail

Validate tier value and willingness to pay before publicly committing to these prices.
Show taxes, currency, billing interval, renewal, cancellation, and applicable limits.
