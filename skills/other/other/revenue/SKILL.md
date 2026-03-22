---
name: revenue-monitor
description: Monitors revenue metrics, tracks subscription changes, and alerts on revenue anomalies or threshold breaches.
tags: [monitoring, revenue, subscriptions]
---

# Revenue Monitor

## When to use

- "Monitor revenue trends"
- "Alert when revenue drops"
- "Track subscription churn"
- "Monitor MRR/ARR changes"
- "Alert on refund spikes"

## What it monitors

- **Revenue metrics**: MRR, ARR, daily revenue
- **Subscription metrics**: New subscriptions, cancellations, churns, renewals
- **Refunds**: Refund rate, refund amount
- **Tier changes**: Upgrades, downgrades
- **Enterprise contracts**: Contract value, renewals

## Steps

1. **Gather requirements from user:**
   - Which revenue metric to monitor
   - Alert threshold (e.g., "drop > 10%", "< $X per day")
   - Time window (daily, weekly, monthly)
   - Notification channel (Slack, email)

2. **Read shared files:**
   - `shared/bq-schema.md` — Subscription tables (ltxstudio_user_tiers_dates, etc.)
   - `shared/metric-standards.md` — Revenue metric definitions

3. **Write monitoring SQL:**
   - Query current metric value
   - Compare against historical baseline or threshold
   - Flag anomalies or breaches

4. **Present to user:**
   - Show SQL query
   - Show example alert format
   - Confirm threshold values

5. **Set up alert** (manual for now):
   - Document SQL in Hex or BigQuery scheduled query
   - Configure Slack webhook or notification

## Reference files

| File | Read when |
|------|-----------|
| `shared/bq-schema.md` | Writing SQL for subscription/revenue tables |
| `shared/metric-standards.md` | Defining revenue metrics |

## Rules

- DO use LTX Studio subscription tables from bq-schema.md
- DO exclude is_lt_team unless explicitly requested
- DO validate thresholds with user before setting alerts
- DO NOT hardcode dates — use rolling windows
- DO account for timezone differences in daily revenue calculations
