---
name: performance-reporter
description: 'Generate SEO/GEO dashboards: rankings, traffic, backlinks, AI visibility for stakeholders. SEO报告/绩效仪表盘'
version: "9.1.0"
license: Apache-2.0
compatibility: "Claude Code, skills.sh, ClawHub, Vercel Labs, Cursor, Windsurf, Codex CLI, Amp, Gemini CLI, Kimi Code, Qwen Code, CodeBuddy"
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when generating SEO performance reports, traffic summaries, ranking reports, or stakeholder-facing dashboards."
argument-hint: "<domain> [date range]"
metadata:
  author: aaron-he-zhu
  version: "9.1.0"
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
    - "看看数据"
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


Creates comprehensive SEO and GEO performance reports combining multiple metrics into actionable insights, executive summaries, and visual data presentations for stakeholder communication.

## What This Skill Does

Aggregates SEO/GEO data sources, generates executive summaries and visual reports, benchmarks against goals and competitors, calculates ROI, and provides prioritized recommendations.

## Quick Start

Start with one of these prompts. Finish with a short handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Generate Performance Report

```
Create an SEO performance report for [domain] for [time period]
```

### Executive Summary

```
Generate an executive summary of SEO performance for [month/quarter]
```

### Specific Report Types

```
Create a GEO visibility report for [domain]
```

```
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

When a user requests a performance report:

1. **Define Report Parameters** -- Domain, report period, comparison period, report type (Monthly/Quarterly/Annual), audience (Executive/Technical/Client), focus areas.

2. **Create Executive Summary** -- Overall performance rating, key wins/watch areas/action required, metrics at a glance table (traffic, rankings, conversions, DA, AI citations), SEO ROI calculation.

3. **Report Organic Traffic Performance** -- Traffic overview (sessions, users, pageviews, bounce rate), traffic trend visualization, traffic by source/device, top performing pages.

4. **Report Keyword Rankings** -- Rankings overview by position range, distribution change visualization, top improvements and declines, SERP feature performance.

5. **Report GEO/AI Performance** -- AI citation overview, citations by topic, GEO wins, optimization opportunities.

6. **Report Domain Authority (CITE Score)** -- If a CITE audit has been run, include CITE dimension scores (C/I/T/E) with period-over-period trends and veto status. If no audit exists, note as "Not yet evaluated."

7. **Content Quality (CORE-EEAT Score)** -- If content-quality-auditor has been run, include average scores across all 8 CORE-EEAT dimensions with trends. If no audit exists, note as "Not yet evaluated."

8. **Report Backlink Performance** -- Link profile summary, weekly link acquisition, notable new links, competitive position.

9. **Report Content Performance** -- Publishing summary, top performing content, content needing attention, content ROI.

10. **Generate Recommendations** -- Immediate/short-term/long-term actions with priority, expected impact, and owner. Goals for next period.

11. **Compile Full Report** -- Combine all sections with table of contents, appendix (data sources, methodology, glossary).

   > **Reference**: See [references/report-output-templates.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/report-output-templates.md) for complete output templates for all 11 report sections.

## Example

**User**: "Create a monthly SEO report for cloudhosting.com for January 2025"

**Output** (abbreviated -- full report uses templates from all 11 steps):

```markdown
# CloudHosting SEO & GEO Performance Report — January 2025

## Executive Summary — Overall Performance: Good

| Metric | Jan 2025 | Dec 2024 | Change | Target | Status |
|--------|----------|----------|--------|--------|--------|
| Organic Traffic | 52,100 | 45,200 | +15.3% | 50,000 | On track |
| Keywords Top 10 | 87 | 79 | +8 | 90 | Watch |
| Organic Conversions | 684 | 612 | +11.8% | 700 | Watch |
| Domain Rating | 54 | 53 | +1 | 55 | Watch |
| AI Citations | 18 | 12 | +50.0% | 20 | Watch |

**SEO ROI**: $8,200 invested / $41,040 organic revenue = 400%

**Immediate**: Fix 37 crawl errors on /pricing/ pages
**This Month**: Optimize mobile LCP; publish 3 AI Overview comparison pages
**This Quarter**: Build Wikidata entry for CloudHost Inc.
```

## Tips for Success

1. **Lead with insights** - Start with what matters, not raw data
2. **Visualize data** - Charts and graphs improve comprehension
3. **Compare periods** - Context makes data meaningful
4. **Include actions** - Every report should drive decisions
5. **Customize for audience** - Executives need different info than technical teams
6. **Track GEO metrics** - AI visibility is increasingly important


### Save Results

Ask "Save these results?" If yes, write a dated summary to `memory/monitoring/YYYY-MM-DD-<topic>.md` with headline finding, actionable items, and open loops.

## Reference Materials

- [Report Output Templates](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/report-output-templates.md) — Complete output templates for all 11 report sections
- [KPI Definitions](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/kpi-definitions.md) — SEO/GEO metric definitions with benchmarks, good ranges, warning thresholds, trend analysis, and attribution guidance
- [Report Templates by Audience](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/performance-reporter/references/report-templates.md) — Copy-ready templates for executive, marketing, technical, and client audiences

## Next Best Skill

Primary → [alert-manager](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/monitor/alert-manager/SKILL.md) to turn reporting insights into ongoing monitoring rules.
