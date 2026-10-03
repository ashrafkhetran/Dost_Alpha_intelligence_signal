# Design system

## Brand

**DOST ALPHA — AI Intelligence Terminal**

**Signal Over Noise. Intelligence Over Information.**

Tone: composed, specific, evidence-led, candid about uncertainty. Avoid sensational
language, fake urgency, and faux-live indicators.

## Proposed visual tokens

| Token | Value | Intended use |
|---|---|---|
| Background | `#0B0F19` | App canvas |
| Surface | `#121826` | Panels and cards |
| Primary | `#7C3AED` | Main action and focus accent |
| Secondary | `#06B6D4` | Supporting data and links |
| Success | `#10B981` | Positive status (with text/icon) |
| Warning | `#F59E0B` | Caution/stale |
| Danger | `#EF4444` | Error/risk |
| Text | `#E8EDF5` | Main copy |

Current CSS also uses a brighter violet `#9b7bff` and other derived colors. Consolidate
tokens during UI implementation; verify contrast rather than assuming palette pairs
are accessible.

## Typography

- Headings: Inter Tight; clear scale and restrained tracking.
- Body: Inter; comfortable line height for summaries and source detail.
- Metrics: JetBrains Mono; tabular, labeled values.
- Use system fallbacks if external font loading fails.

## Components

- Signal card: category, headline, source/freshness, summary, score explanations, save,
  and source action.
- Evidence row: publisher, primary/secondary classification, publication and retrieval
  dates, cited claim, link.
- Score badge: numeric value, scale, definition, confidence and non-color cue.
- Brief panel: audience, reporting window, executive summary, sourced developments,
  implications, caveats, recommendations.
- Status banners: distinct sample, live, stale, partial, and error variants.
- Plan card: billing interval, capabilities, limits, cancellation, and contextual CTA.

## Layout and motion

Keep persistent navigation, generous page margins, compact mono metadata, and responsive
single-column fallbacks. Use motion only for focus/feedback; respect reduced-motion.
Charts must have labels and an accessible textual alternative. Don't use CSS selectors
or HTML injection as a substitute for accessible native controls.
