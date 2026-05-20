---
name: analytics
description: Activate for marketing analytics, KPI tracking, reporting dashboards, attribution analysis, and performance optimization. Use when analyzing campaign data, creating reports, or measuring marketing ROI.
license: MIT
---

# Marketing Analytics

Performance measurement, reporting, and data-driven optimization.

## When to Use

- Campaign performance analysis
- KPI dashboard creation
- Attribution modeling
- ROI calculation
- A/B test analysis
- Funnel optimization
- Report generation

## Core Capabilities

### KPI Framework
Load: `references/marketing-kpis.md`

### Reporting Templates
Load: `references/report-templates.md`

### Attribution Models
Load: `references/attribution-models.md`

### Analysis Workflows
Load: `references/analysis-workflows.md`

## Quick Reference

**Core Marketing KPIs:**
| Category | Metrics |
|----------|---------|
| Acquisition | CAC, CPL, Traffic |
| Engagement | CTR, Time on Site, Bounce |
| Conversion | CVR, ROAS, Revenue |
| Retention | LTV, Churn, NPS |

**Reporting Cadence:**
- Daily: Spend, impressions, clicks
- Weekly: Conversions, ROI by channel
- Monthly: Full funnel, trends
- Quarterly: Strategic review

## Workflow

### Campaign Analysis
1. Define success metrics
2. Pull data from sources
3. Calculate key ratios
4. Compare to benchmarks
5. Identify patterns
6. Generate insights
7. Recommend actions

### A/B Test Analysis
1. Check sample size
2. Calculate statistical significance
3. Compare conversion rates
4. Determine winner
5. Document learnings

## Report Output

**Activate:** `assets-organizing` skill for report file paths

Reports go to `assets/reports/analytics/` with naming `{date}-{report-type}.md`

**Template:** `references/report-templates.md`

Reports include:
- Mermaid.js charts (pie, bar, flowchart)
- Prioritized recommendations table
- Actionable next steps with owners

## Google Analytics 4 API

### Setup
```bash
npm install @google-analytics/admin @google-analytics/data
```

Credentials: `.claude/secrets/ga_service_account.json` or `google_client_secret.json`

### Scripts
| Script | Purpose |
|--------|---------|
| `scripts/ga-config-loader.cjs` | Load credentials from .claude/secrets |
| `scripts/ga-list-accounts.cjs` | List GA4 accounts & properties |
| `scripts/ga-run-report.cjs` | Run custom reports |
| `scripts/ga-auth-setup.cjs` | OAuth authentication setup |

### Quick Usage
```bash
# List accounts
node .claude/skills/analytics/scripts/ga-list-accounts.cjs --summaries

# Run report
node .claude/skills/analytics/scripts/ga-run-report.cjs \
  --property=PROPERTY_ID \
  --dimensions=country,city \
  --metrics=activeUsers,sessions
```

### API References
- `references/ga-admin-api.md` - Admin API (property config)
- `references/ga-data-api.md` - Data API (reporting)

## Agent Integration

**Primary Agents:** data-analyst, campaign-manager, growth-specialist

**Data Sources:** GA4, Ads platforms, CRM, Email tools

## Best Practices

1. Track leading indicators, not just lagging
2. Compare apples to apples (same timeframes)
3. Statistical significance before conclusions
4. Attribution ≠ causation
5. Report insights, not just numbers
6. Automate recurring reports
