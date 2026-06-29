---
name: performance-reporter
description: 'Use when the user asks to "generate an SEO report" or "出月报"; builds multi-metric stakeholder reports and dashboards spanning traffic, rankings, authority, and content progress. Not for raw ranking deltas — use rank-tracker. SEO报告/绩效仪表盘'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when generating multi-metric SEO/GEO performance reports, traffic summaries, stakeholder dashboards, SEO报告, 流量报告, 月报, 周报, or 汇报给老板. Not for raw ranking deltas — use rank-tracker."
argument-hint: "<domain> [date range]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  geo-relevance: "medium"
---

# Performance Reporter

Aggregates SEO/GEO data, builds stakeholder reports, benchmarks goals/competitors, calculates ROI, and turns deltas into prioritized recommendations.

## Quick Start

```text
Create an SEO performance report for [domain] for [time period]
Generate an executive summary of SEO performance for [month/quarter]
Create a GEO visibility report for [domain]
Generate a content performance report
```

## Skill Contract

**Expected output**: a delta summary, alert/report output, and a short handoff summary ready for `memory/monitoring/`.

- **Reads**: current and prior-period metrics across traffic/rankings/authority/content, report audience, date range, and any user-provided or tool data.
- **Writes**: a user-facing monitoring deliverable plus a reusable summary that can be stored under `memory/monitoring/`.
- **Promotes**: significant changes, confirmed anomalies, follow-up actions, and pending decisions to `memory/open-loops.md`.
- **Done when**: each in-scope section (traffic, rankings, GEO, authority, backlinks, content) is present or marked "Not yet evaluated"; every metric is source-tagged and compared to the prior period; and recommendations carry owner, priority, and expected impact.
- **Primary next skill**: use the `Next Best Skill` below when a change needs action.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](../../CONNECTORS.md)). With tools connected, aggregates traffic from ~~analytics, search data from ~~search console, rankings/backlinks from ~~SEO tool, and AI visibility from ~~AI monitor. Without tools, ask user for analytics exports, Search Console data, ranking data, and KPIs.

**Zero-dependency measurement loop**: every reported change should come from a computed delta, not an eyeballed estimate. Store each reporting period's KPIs and let the ledger compute period-over-period movement: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/connectors/ledger.py" record <domain> --source report --data '{"sessions": ..., "clicks": ..., ...}'`, then `ledger.py diff <domain> --source report` for the period delta and `ledger.py trend <domain> --source report --field <kpi>` for the trend line. Label every figure Measured / User-provided / Estimated accordingly, and attribute outcome movements against a control rather than to the latest change by default — see [references/measurement-protocol.md](../../references/measurement-protocol.md). See [scripts/connectors/README.md](../../scripts/connectors/README.md).

## Decision Gates

**Stop and ask the user when:**
- No reporting period or comparison period can be determined and none is in context — offer: (1) last 30 days vs prior 30, (2) last calendar month vs prior month, (3) a custom range. A period comparison is required, not optional.

**Continue silently (never stop for):**
- A section's source data is missing — mark that section "Not yet evaluated" and proceed; do not fabricate the metric.
- Audience not stated — default to the executive template and note the assumption.

## Instructions

When a user requests a performance report, use [Report Output Templates](references/report-output-templates.md) and cover:

1. **Define Report Parameters** — Domain, period, comparison period, report type, audience, focus areas, and data freshness.
2. **Create Executive Summary** — Overall rating, wins, watch areas, required actions, metrics at a glance (traffic, rankings, conversions, DA/authority, AI citations), and SEO ROI; tag each metric Measured / User-provided / Estimated.
3. **Report Organic Traffic** — Sessions, users, pageviews, engagement/bounce, trend visualization, source/device split, top pages, each figure source-tagged.
4. **Report Keyword Rankings** — Position ranges, distribution change, top improvements/declines, SERP features. For raw position-by-position deltas, defer to rank-tracker rather than recomputing here.
5. **Report GEO/AI Performance** — AI citation overview, citations by topic, GEO wins, and optimization opportunities.
6. **Report Domain Authority (CITE)** — Include CITE dimension scores and veto status when available; otherwise mark "Not yet evaluated."
7. **Report Content Quality (CORE-EEAT)** — Include average scores and trends when available; otherwise mark "Not yet evaluated."
8. **Report Backlinks** — Link profile summary, acquisition trend, notable links, competitive position.
9. **Report Content Performance** — Publishing summary, top content, content needing attention, and content ROI.
10. **Generate Recommendations** — Immediate, short-term, and long-term actions with priority, owner, expected impact, and next-period goals.
11. **Compile Full Report** — Add table of contents, appendix, data sources, methodology, and glossary.

Label every metric **Measured** (tool/export), **User-provided**, or **Estimated** (model inference); never present an estimate as measured; if a required metric is unavailable, mark it N/A — do not invent it. Likewise separate an **observed change** from a **plausible explanation** (corroborate before stating it as the cause), an **optimization opportunity**, and **follow-up** needing crawl/SERP/rank/audit — never report an unverified explanation as a confirmed cause.

## Example

Sample output: an executive summary with overall status, metrics-at-a-glance for traffic/rankings/conversions/authority/AI citations, SEO ROI, and immediate/month/quarter actions with owners and dates.

## Save Results

Ask "Save these results?" If yes, write to `memory/monitoring/` — see [Skill Contract](../../references/skill-contract.md) §Save Results Template.

## Reference Materials

- [Report Output Templates](references/report-output-templates.md) — Compact starter blocks for all 11 report sections
- [KPI Definitions](references/kpi-definitions.md) — SEO/GEO metric definitions with benchmarks, thresholds, trend analysis, and attribution guidance
- [Report Templates by Audience](references/report-templates.md) — Copy-ready templates for executive, marketing, technical, and client audiences

## Next Best Skill

Recurring monitoring needed → [alert-manager](../alert-manager/SKILL.md) — turn reporting insights into ongoing monitoring rules. One-off report → Terminal. Visited-set rule applies per [Skill Contract](../../references/skill-contract.md).
