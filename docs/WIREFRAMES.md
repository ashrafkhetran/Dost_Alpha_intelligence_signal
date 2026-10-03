# Wireframes

Low-fidelity product direction only. These are not pixel specifications or claims about
existing production capabilities.

## Global shell

```text
┌──────────────────┬────────────────────────────────────────────────────┐
│ ◈ DOST ALPHA     │ Workspace / freshness / account                    │
│ Overview         ├────────────────────────────────────────────────────┤
│ Intelligence     │ Page title              Time range   Scope         │
│ Analyst          │ Short explanation / data status                     │
│ Trend Radar      │                                                    │
│ Briefings        │ Main workspace                     Context panel    │
│ Saved            │                                                     │
│ Settings         │                                                     │
│                  │                                                    │
│ Plan · Help      │                                                    │
└──────────────────┴────────────────────────────────────────────────────┘
```

At narrow widths, navigation collapses behind an accessible menu and the context panel
moves below primary content.

## Overview

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Good morning · AI / Business · Updated [time] · [Change scope]       │
│ Your intelligence, in focus                        [Create a brief]   │
├──────────────────────────────────────────────────────────────────────┤
│ Critical signals [count] │ Emerging opportunities │ Watchlist moves  │
├────────────────────────────────────┬─────────────────────────────────┤
│ PRIORITIZED SIGNALS                │ MORNING BRIEF                   │
│ [source/date] [confidence]         │ Top development                  │
│ Headline / why it matters          │ Why it matters · What to verify   │
│ [Open evidence] [Save]             │ [Read briefing]                  │
│ ...                                │                                  │
└────────────────────────────────────┴─────────────────────────────────┘
```

Use real counts only when backed by the data store; otherwise show an explicit empty or
demo state.

## Intelligence feed

```text
┌──────────────────────────────────────────────────────────────────────┐
│ Intelligence Feed   [Search] [Topic] [Category] [Period] [Impact]    │
│ Active filters: ... [Clear]                     Sort: relevance/fresh│
├──────────────────────────────────────────────────────────────────────┤
│ Signal headline                           Impact / confidence / trend │
│ One-line interpretation · publisher · published · collected           │
│ Why surfaced · evidence count · freshness                              │
│ [Inspect sources] [Save] [Watch topic]                                 │
├──────────────────────────────────────────────────────────────────────┤
│ Evidence detail opens inline or in a side panel; original source link  │
└──────────────────────────────────────────────────────────────────────┘
```

## Analyst

```text
┌──────────────────────────────────────────────────────────────────────┐
│ AI Analyst · grounded in [N] sources through [time]                   │
│ [Ask a specific question................................] [Analyze]   │
│ Scope: [topics] [date window]     Budget/usage disclosure             │
├──────────────────────────────────────────────────────────────────────┤
│ Executive answer · evidence status                                    │
│ Claim 1 [1][2]      Claim 2 [3]                                       │
│ [1] source/date/excerpt/link      [Risks and unknowns]                 │
│ Next checks / follow-up                                             │
└──────────────────────────────────────────────────────────────────────┘
```

## Briefings and billing

Brief editor: briefing type, audience, time window, source coverage; preview with cited
developments, uncertainty, and recommendations; save/export actions only after content
validation. Upgrade flow: capability-specific plan explanation → limits and renewal terms
→ hosted checkout → confirmation after webhook-confirmed entitlement.
