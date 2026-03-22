---
name: mindshare
description: "Mindshare tracking primitive using Kaito MCP tools. Use this skill to check mindshare trends for an entity or narrative. Triggers on phrases like 'mindshare for SOL', 'how is the AI narrative trending', 'mindshare trend for Hyperliquid', 'which narratives are gaining share', 'mindshare comparison'. This is a primitive skill — it fetches mindshare data via kaito_mindshare, kaito_narrative_mindshare, or kaito_mindshare_delta and presents trend analysis. Can be called standalone or composed into workflow skills (social-listening, strategy, investigation). Do NOT use for sentiment (sentiment skill), content search (search skill), or user profiling (user-profile skill)."
---

# Mindshare Skill (Primitive)

Track mindshare trends for entities or narratives using Kaito MCP tools.

## Parameters

- **entity** *(required)*: One of:
  - **token**: An entity/project (e.g. `HYPE`, `SOL`, `ETH`) — uses `kaito_mindshare`
  - **narrative**: A Kaito narrative ID (e.g. `AI`, `DeFi`, `L2`) — uses `kaito_narrative_mindshare`
- **time_range** *(optional)*: Period to analyze (default: 12 months for entities, flexible for narratives)
- **delta** *(optional)*: If true, also fetch `kaito_mindshare_delta` for recent changes

When called standalone, confirm parameters with the user first. When called by a workflow skill, parameters are passed directly.

### Valid Narrative IDs (case-sensitive)

AI, DeFi, Stablecoin, L2, RWA, ZK, Meme, DePIN, SocialFi

Known invalid narrative IDs (use `kaito_advanced_search` with keyword as fallback): perp dex, prediction markets, privacy, restaking, NFT, gaming, liquid staking, robotics.

---

## Workflow

### For Entity Mindshare

Call `kaito_mindshare` with:
- token: `<TOKEN>`
- start_date: `<range_start>` (default: 12 months ago)
- end_date: `<today>`

If all-zero results returned, switch from ticker to full project name (e.g. `HYPE` → `HYPERLIQUID`) and retry.

Optionally call `kaito_mindshare_delta` for a quick snapshot of recent change.

### For Narrative Mindshare

Call `kaito_narrative_mindshare` with:
- narrative: `<NARRATIVE_ID>` (case-sensitive)
- start_date: `<range_start>`
- end_date: `<today>`

### Analysis

Present:
- **Trend chart** — weekly averages over the time range, current level highlighted
- **Historical context** — where current value sits vs high/low/average for the period
- **Rank interpretation** (for entities):
  - Top 10 = dominant
  - Top 20 = strong
  - Top 50 = moderate
  - > 50 = weak
- **Movement** (for narratives):
  - % change = (last day - first day) / first day × 100
  - Surging: >= +10% relative change
  - Fading: <= -10% relative change
  - Stable: within ±10%

---

## Output Format

When used standalone:

```
Mindshare: [ENTITY] | [TIME RANGE]

Trend: [weekly averages, current level]
Current: [value] ([rank interpretation if entity])
12m High: [value] | Low: [value] | Avg: [value]
Movement: [% change, surging/fading/stable]
```

When called by a workflow skill, return the structured data for the workflow to integrate.

---

## Key Rules

- **If all-zero data for a ticker, switch to full name** — Kaito indexes some entities by name rather than ticker. All-zero means the ticker isn't matched.
- **Narrative IDs are case-sensitive** — use exactly: AI, DeFi, Stablecoin, L2, RWA, ZK, Meme, DePIN, SocialFi. Mismatched casing returns empty results silently.
- **Rank context is relative** — Top 10 = dominant, Top 20 = strong, Top 50 = moderate, >50 = weak. Always provide this context so users can calibrate.
- **For narrative mindshare, calculate % change** — raw numbers need the surging/fading/stable classification to be actionable.
- **Always present historical context** — current value alone is meaningless without the 12-month high/low/average for comparison.
