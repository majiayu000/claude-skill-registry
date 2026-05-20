---
name: usage-monitor
description: "Monitor LTX Studio product usage metrics with statistical anomaly detection. Detects data spikes (increases or decreases) in DAU, generations, and token consumption. Use when: (1) daily monitoring and detecting usage anomalies, (2) alerting on segment-specific changes, (3) investigating root causes of engagement shifts."
tags: [monitoring, usage, dau, generations, engagement, alerts]
---

# Usage Monitor

## 1. Overview (Why?)

This skill provides **autonomous usage monitoring** using statistical anomaly detection. It compares yesterday's metrics against the last 10 same-day-of-week data points (e.g., last 10 Mondays) and alerts when values deviate by 2 standard deviations from the mean.

**Problem solved**: Detect data spikes in usage — both increases and decreases — that indicate significant changes in user behavior, product adoption, feature launches, enterprise churn risk, or engagement shifts. Uses statistical thresholds that adapt to each segment's variance patterns.

## 2. Requirements (What?)

Monitor these outcomes autonomously:

- [ ] DAU spikes (increases or decreases) by segment (Enterprise Contract/Pilot, Heavy, Paying, Free)
- [ ] Image generation volume changes (both increases and decreases)
- [ ] Video generation volume changes
- [ ] Token consumption trends (spikes up or down)
- [ ] Alerts fire when values deviate beyond 2σ (increases or decreases)
- [ ] Weekend alerts suppressed for Enterprise (weekday-only monitoring)
- [ ] Root cause investigation identifies which orgs/tiers drove changes
- [ ] Results formatted with severity (NOTICE vs WARNING vs CRITICAL)

## 3. Progress Tracker

* [ ] Read shared knowledge (schema, metrics, segmentation)
* [ ] Run monitoring script for target date
* [ ] Analyze alerts by segment
* [ ] Investigate root cause (org-level for Enterprise, tier-level for others)
* [ ] Present findings with recommended actions

## 4. Implementation Plan

### Phase 1: Understand the Statistical Method

**Alert logic**: `|yesterday_value - μ| > 2σ`

Where:
- μ (mean) = average of last 10 same-day-of-week values
- σ (stddev) = standard deviation of last 10 same-day-of-week values
- z-score = (yesterday - μ) / σ

**Why 2 standard deviations?**
- Captures 95.4% of normal variance
- Auto-adapts to each segment's natural patterns
- Balances early detection with false positive reduction

**Severity levels**:
- NOTICE: `2 < |z| ≤ 3`
- WARNING: `3 < |z| ≤ 4.5`
- CRITICAL: `|z| > 4.5`

**Exceptions**:
- Enterprise weekends: Suppress (too few data points)

### Phase 2: Read Shared Knowledge

Before running monitoring, reference:
- **`shared/bq-schema.md`** — Segmentation CTEs (lines 441-516), table schema
- **`shared/metric-standards.md`** — DAU/WAU/MAU, generation metrics
- **`shared/product-context.md`** — LTX products, user types, business model
- **`shared/event-registry.yaml`** — Known events per feature, types, status

**Key data source**: `ltx-dwh-prod-processed.web.ltxstudio_agg_user_date`
- Partitioned by `dt` (DATE)
- Key columns: `lt_id`, `griffin_tier_name`, `num_tokens_consumed`, `num_generate_image`, `num_generate_video`
- LT team already excluded at table level

### Phase 3: Run Monitoring

Execute the combined monitoring script:

```bash
# Install dependency (one-time)
pip install google-cloud-bigquery

# Monitor yesterday (default)
python3 usage_monitor.py

# Monitor specific date
python3 usage_monitor.py --date yesterday
```

**What the script does**:
1. Executes BigQuery SQL with last 10 same-DOW calculations (70-day lookback)
2. Uses `ARRAY_AGG` with window frames to collect last 10 values
3. Calculates mean and stddev from arrays
4. Computes z-scores for each segment × metric
5. Alerts when `|z| > 2`
6. Suppresses Enterprise weekend alerts
7. Outputs formatted results with mean, stddev, z-score

**See**: `usage_monitor.py` for complete SQL query and alerting logic.

### Phase 4: Analyze Results

**When alerts fire**:

1. **Check severity**: CRITICAL (|z| > 4.5) requires immediate action, WARNING (|z| > 3) needs monitoring, NOTICE (|z| > 2) just alert
2. **Identify segment**: Which user segment is affected?
3. **Validate significance**:
   - Is stddev reasonable? (Not too small causing false positives)
   - Are there 10+ historical same-DOW data points?
   - Are there outliers in the last 10 values skewing the mean?
4. **Investigate root cause**:
   - **Enterprise**: Drill down to organization level with `investigate_root_cause.sql`
   - **Other segments**: Check tier distribution (Standard vs Pro vs Lite vs Free)

**Example alert output**:
```
⚠️ WARNING ALERTS (2):
  • Free - Tokens
    Current: 4,497,947 | Mean (μ): 3,068,455 | Std Dev (σ): 426,074
    Z-score: 3.36 (|z| > 3σ threshold)
    Change: +46.6% from mean
```

### Phase 5: Present Findings

Format findings with:
- **Summary**: Which segments alerted and direction (increase/decrease)
- **Severity**: CRITICAL, WARNING, or NOTICE
- **Statistical details**: Current value, mean, stddev, z-score, % change
- **Root cause**: For Enterprise, identify which orgs drove the change
- **Recommended actions**:
  - CRITICAL: Immediate investigation, contact account managers
  - WARNING: Monitor for persistence (alert repeats next day?)
  - Positive spikes: Investigate feature launches, product changes
  - Negative spikes: Investigate churn events, product issues

## 5. Constraints & Done

### DO NOT

- **DO NOT** use simplified segmentation — use exact CTEs from `shared/bq-schema.md` (lines 441-516)
- **DO NOT** alert on Enterprise weekends — exceptions apply
- **DO NOT** compare different days of week — always use same-DOW comparisons
- **DO NOT** use absolute thresholds — always use statistical baselines

### DO

- **DO** filter on `dt` partition column for performance
- **DO** use 2σ as alert threshold (95.4% confidence) for noticing purposes, 3σ for warnings
- **DO** calculate mean and stddev from last 10 same-DOW via `ARRAY_AGG`
- **DO** ensure 70-day lookback for 10+ same-DOW data points
- **DO** flag CRITICAL (|z| > 4.5) vs WARNING (|z| > 3) vs NOTICE (|z| > 2)
- **DO** investigate at org-level for Enterprise, tier-level for others
- **DO** include mean, stddev, z-score in all alerts
### Completion Criteria

✅ Script executed for target date
✅ Alerts fire with statistical details (mean, stddev, z-score)
✅ Severity levels applied correctly (WARNING/CRITICAL)
✅ Root cause investigation completed for alerts
✅ Findings presented with recommended actions
✅ Enterprise weekend suppression working
