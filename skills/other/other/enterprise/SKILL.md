---
name: enterprise-monitor
description: Monitors enterprise account health, usage, and contract compliance. Alerts on low engagement, quota breaches, or churn risk.
tags: [monitoring, enterprise, accounts, contracts]
---

# Enterprise Monitor

## When to use

- "Monitor enterprise account usage"
- "Monitor enterprise churn risk"
- "Alert when enterprise account is inactive"

## What it monitors

- **Account usage**: DAU, WAU, MAU per enterprise org
- **Token consumption**: Usage vs contracted quota, historical consumption trends
- **User activation**: % of seats active
- **Engagement**: Video generations, image generations, downloads per org
- **Churn signals**: Declining usage, inactive users

## Steps

1. **Gather requirements from user:**
   - Which enterprise org(s) to monitor (or all)
   - Alert threshold based on historical usage of each account (e.g., "usage drops > 30% vs their baseline", "MAU below their 30-day average", "< 50% of contracted quota")
   - Time window (weekly, monthly)
   - Notification channel (Slack, email, Linear issue)

2. **Read shared files:**
   - `shared/product-context.md` — LTX products, enterprise business model, user types
   - `shared/bq-schema.md` — Enterprise user segmentation queries
   - `shared/metric-standards.md` — Enterprise metrics, quota tracking
   - `shared/event-registry.yaml` — Feature events (if analyzing engagement)
   - `shared/gpu-cost-query-templates.md` — GPU cost queries (if analyzing infrastructure costs)
   - `shared/gpu-cost-analysis-patterns.md` — Cost analysis patterns (if analyzing infrastructure costs)

3. **Identify enterprise users:**
   - Use enterprise segmentation CTE from bq-schema.md (lines 441-461)
   - Apply McCann split (McCann_NY vs McCann_Paris)
   - Exclude Lightricks and Popular Pays

4. **Write monitoring SQL:**
   - Query org-level usage metrics
   - Set baseline for each org based on their historical usage (e.g., 30-day average, 90-day trend)
   - Compare current usage against org-specific baseline or contracted quota
   - Flag orgs below threshold or showing decline
   - Flag meaningful drops for power users (users with top usage within each org)

5. **Present to user:**
   - Show SQL query
   - Show example alert format with org name and metrics
   - Confirm threshold values and alert logic

6. **Set up alert** (manual for now):
   - Document SQL
   - Configure notification to customer success team

## Rules

- DO use EXACT enterprise segmentation CTE from bq-schema.md without modification
- DO apply McCann split (McCann_NY vs McCann_Paris)
- DO exclude Lightricks and Popular Pays from enterprise orgs
- DO break out pilot vs contracted accounts
- DO NOT alert on free/self-serve users — this agent is enterprise-only
- DO include org name in alert for easy customer success follow-up
