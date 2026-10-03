# UI/UX guidelines

## Experience goals

Create a premium, dark-first research workspace that scans quickly, explains its
evidence, and remains calm under dense information. A dashboard is a navigation shell,
not the product: each surface should help a user answer a real question.

## Information hierarchy

1. Scope and freshness (topic, time range, data status).
2. What changed (signal headline and concise summary).
3. Why it matters (impact hypothesis and audience relevance).
4. Evidence (source, date, link, corroboration, claim-level citations).
5. Uncertainty and next verification step.

## Core flows

- **Discover:** overview → feed filters → signal detail/source → save/watch.
- **Research:** scoped question → retrieval-backed answer → inspect citations → follow-up.
- **Brief:** choose audience and period → preview evidence-backed draft → edit/export/save.
- **Upgrade:** request gated capability → see relevant benefit/limit → compare tiers →
  hosted checkout → confirmed access.

## Interaction rules

- Use explicit loading, empty, stale, and failure states; never imply current data if
  sources have not refreshed.
- Preserve filters when navigating back; offer reset and clear-filter affordances.
- Use source links that identify publisher and date; distinguish primary from secondary.
- Display scores with labels, scale, explanation, and a non-color status cue.
- Require confirmation for destructive account or watchlist actions.
- Do not make external links or HTML content trust boundaries implicit.
- Provide keyboard support, visible focus, readable contrast, semantic headings, and
  chart summaries/table alternatives.

## Wireframes

See [WIREFRAMES.md](WIREFRAMES.md) for low-fidelity layouts. See [UI_MOCKUPS.md](UI_MOCKUPS.md)
for screen tone and states. Those specifications guide future implementation and do not
imply the current prototype has these production interactions.

## Core test scenarios

Test new-user orientation, no matching signals, stale or unavailable source, model
timeout, unsupported analyst answer, free-tier limit, failed payment, cancel/rejoin,
small screens, keyboard-only navigation, and screen-reader source/citation comprehension.
