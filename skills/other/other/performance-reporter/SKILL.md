---
name: performance-reporter
description: 'Use when generating SEO/GEO reports, traffic summaries, ranking reports, KPI dashboards, stakeholder updates, or monthly reports. SEO报告/绩效仪表盘'
version: "9.9.5"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when generating SEO/GEO performance reports, traffic summaries, ranking reports, stakeholder dashboards, SEO报告, 流量报告, 月报, 周报, or 汇报给老板."
argument-hint: "<domain> [date range]"
metadata:
  author: aaron-he-zhu
  version: "9.9.5"
  geo-relevance: "medium"
  tags:
    - seo
    - geo
    - seo-reporting
    - performance-report
    - kpi-dashboard
    - traffic-report
    - monthly-report
    - stakeholder-report
    - SEO报告
    - SEOレポート
    - SEO리포트
    - informe-seo
  triggers:
    # EN-formal
    - "generate SEO report"
    - "performance report"
    - "traffic report"
    - "SEO dashboard"
    # EN-casual
    - "monthly SEO report"
    - "show me my SEO results"
    - "report to my boss"
    # EN-question
    - "how is my SEO performing"
    # ZH-pro
    - "SEO报告"
    - "绩效仪表盘"
    - "流量报告"
    - "数据看板"
    # ZH-casual
    - "出SEO报告"
    - "汇报给老板"
    - "看看SEO数据"
    - "月报"
    - "出月报"
    - "周报"
    # JA
    - "SEOレポート"
    - "パフォーマンスレポート"
    # KO
    - "SEO 리포트"
    - "성과 보고서"
    # ES
    - "informe SEO"
    - "reporte de rendimiento"
    # PT
    - "relatório SEO"
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

- **Reads**: current metrics, previous baselines, alert thresholds, and reporting context from [CLAUDE.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CLAUDE.md) and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md) when available.
- **Writes**: a user-facing monitoring deliverable plus a reusable summary that can be stored under `memory/monitoring/`.
- **Promotes**: significant changes, confirmed anomalies, and follow-up actions to `memory/open-loops.md` and `memory/decisions.md`.
- **Next handoff**: use the `Next Best Skill` below when a change needs action.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

## Data Sources

All integrations optional (see [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md)). With tools connected, aggregates traffic from ~~analytics, search data from ~~search console, rankings/backlinks from ~~SEO tool, and AI visibility from ~~AI monitor. Without tools, ask user for analytics exports, Search Console data, ranking data, and KPIs.

## Instructions

When a user requests a performance report, use [references/report-output-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/report-output-templates.md) and cover:

1. **Define Report Parameters** -- Domain, period, comparison period, report type, audience, focus areas, and data freshness.
2. **Create Executive Summary** -- Overall rating, wins, watch areas, required actions, metrics at a glance (traffic, rankings, conversions, DA/authority, AI citations), and SEO ROI.
3. **Report Organic Traffic** -- Sessions, users, pageviews, engagement/bounce, trend visualization, source/device split, top pages.
4. **Report Keyword Rankings** -- Position ranges, distribution change, top improvements/declines, SERP features.
5. **Report GEO/AI Performance** -- AI citation overview, citations by topic, GEO wins, and optimization opportunities.
6. **Report Domain Authority (CITE)** -- Include CITE dimension scores and veto status when available; otherwise mark "Not yet evaluated."
7. **Report Content Quality (CORE-EEAT)** -- Include average scores and trends when available; otherwise mark "Not yet evaluated."
8. **Report Backlinks** -- Link profile summary, acquisition trend, notable links, competitive position.
9. **Report Content Performance** -- Publishing summary, top content, content needing attention, and content ROI.
10. **Generate Recommendations** -- Immediate, short-term, and long-term actions with priority, owner, expected impact, and next-period goals.
11. **Compile Full Report** -- Add table of contents, appendix, data sources, methodology, and glossary.

## Example

Sample output: an executive summary with overall status, metrics-at-a-glance for traffic/rankings/conversions/authority/AI citations, SEO ROI, and immediate/month/quarter actions with owners and dates.

## Tips for Success

Lead with insights, compare periods, state data freshness, include owner/deadline/impact for actions, tailor depth to audience, and track GEO/AI citation metrics when in scope.

### Save Results

Ask "Save these results?" If yes, write `memory/monitoring/YYYY-MM-DD-<topic>.md` with the headline finding, actionable items, and open loops.

## Reference Materials

- [Report Output Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/report-output-templates.md) -- Compact starter blocks for all 11 report sections
- [KPI Definitions](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/kpi-definitions.md) -- SEO/GEO metric definitions with benchmarks, thresholds, trend analysis, and attribution guidance
- [Report Templates by Audience](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/report-templates.md) -- Copy-ready templates for executive, marketing, technical, and client audiences

## Next Best Skill

Primary: [alert-manager](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/SKILL.md) -- turn reporting insights into ongoing monitoring rules.
