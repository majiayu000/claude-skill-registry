---
name: data-pipeline
description: Orchestrate marketing data collection, transformation, and reporting workflows. Use when relevant to the task.
---

# data-pipeline

Orchestrate marketing data collection, transformation, and reporting workflows.

## Triggers

- "collect marketing data"
- "update metrics"
- "refresh analytics"
- "data pipeline"
- "sync marketing data"
- "pull campaign metrics"

## Purpose

This skill manages marketing data workflows by:
- Collecting data from multiple marketing platforms
- Transforming raw data into actionable metrics
- Aggregating cross-channel performance
- Generating automated reports
- Maintaining data quality and consistency

## Behavior

When triggered, this skill:

1. **Identifies data sources**:
   - List connected platforms
   - Check API credentials/access
   - Determine data freshness requirements

2. **Collects raw data**:
   - Pull metrics from each platform
   - Handle pagination and rate limits
   - Store raw data snapshots

3. **Transforms data**:
   - Normalize naming conventions
   - Calculate derived metrics
   - Apply attribution models
   - Aggregate across channels

4. **Validates data**:
   - Check for anomalies
   - Validate against thresholds
   - Flag data quality issues

5. **Stores and reports**:
   - Update data warehouse/storage
   - Generate summary reports
   - Trigger alerts if needed

## Supported Platforms

### Advertising Platforms

```yaml
advertising:
  google_ads:
    metrics:
      - impressions
      - clicks
      - cost
      - conversions
      - conversion_value
    dimensions:
      - campaign
      - ad_group
      - keyword
      - device
    refresh_frequency: 4h

  meta_ads:
    metrics:
      - impressions
      - reach
      - clicks
      - spend
      - conversions
    dimensions:
      - campaign
      - ad_set
      - ad
      - placement
    refresh_frequency: 4h

  linkedin_ads:
    metrics:
      - impressions
      - clicks
      - cost
      - leads
      - conversions
    dimensions:
      - campaign
      - creative
      - audience
    refresh_frequency: daily
```

### Analytics Platforms

```yaml
analytics:
  google_analytics:
    metrics:
      - sessions
      - users
      - pageviews
      - bounce_rate
      - conversions
      - revenue
    dimensions:
      - source_medium
      - campaign
      - landing_page
      - device
    refresh_frequency: 4h

  mixpanel:
    metrics:
      - events
      - unique_users
      - retention
      - funnel_conversion
    dimensions:
      - event_name
      - user_properties
    refresh_frequency: real-time

  amplitude:
    metrics:
      - events
      - users
      - retention
      - conversion
    dimensions:
      - event_type
      - user_segment
    refresh_frequency: real-time
```

### Email Platforms

```yaml
email:
  mailchimp:
    metrics:
      - sends
      - opens
      - clicks
      - bounces
      - unsubscribes
    dimensions:
      - campaign
      - list
      - segment
    refresh_frequency: 1h

  hubspot:
    metrics:
      - sends
      - opens
      - clicks
      - contacts_created
      - deals_influenced
    dimensions:
      - campaign
      - email_type
      - lifecycle_stage
    refresh_frequency: 1h

  sendgrid:
    metrics:
      - delivered
      - opens
      - clicks
      - bounces
      - spam_reports
    refresh_frequency: real-time
```

### Social Platforms

```yaml
social:
  instagram:
    metrics:
      - reach
      - impressions
      - engagement
      - followers
      - saves
      - shares
    dimensions:
      - post_type
      - content_category
    refresh_frequency: daily

  linkedin:
    metrics:
      - impressions
      - engagement
      - followers
      - clicks
    dimensions:
      - post_type
      - content_category
    refresh_frequency: daily

  twitter:
    metrics:
      - impressions
      - engagements
      - followers
      - retweets
      - likes
    refresh_frequency: 4h
```

## Data Transformation

### Metric Calculations

```yaml
derived_metrics:
  ctr:
    formula: clicks / impressions
    format: percentage
    description: Click-through rate

  cpc:
    formula: cost / clicks
    format: currency
    description: Cost per click

  cpm:
    formula: (cost / impressions) * 1000
    format: currency
    description: Cost per thousand impressions

  cpa:
    formula: cost / conversions
    format: currency
    description: Cost per acquisition

  roas:
    formula: revenue / cost
    format: ratio
    description: Return on ad spend

  conversion_rate:
    formula: conversions / clicks
    format: percentage
    description: Conversion rate

  engagement_rate:
    formula: engagements / impressions
    format: percentage
    description: Engagement rate
```

### Attribution Models

```yaml
attribution_models:
  last_click:
    description: 100% credit to last touchpoint
    use_case: Bottom-funnel optimization

  first_click:
    description: 100% credit to first touchpoint
    use_case: Top-funnel optimization

  linear:
    description: Equal credit across touchpoints
    use_case: Multi-touch awareness

  time_decay:
    description: More credit to recent touchpoints
    use_case: Typical purchase journey

  position_based:
    description: 40% first, 40% last, 20% middle
    use_case: Balanced attribution

  data_driven:
    description: ML-based credit assignment
    use_case: Advanced optimization
```

## Pipeline Configuration

```yaml
pipeline_config:
  name: marketing-data-pipeline
  schedule: "0 */4 * * *"  # Every 4 hours

  sources:
    - name: google_ads
      credentials: .aiwg/marketing/config/google-ads-creds.json
      date_range: last_30_days

    - name: google_analytics
      credentials: .aiwg/marketing/config/ga4-creds.json
      property_id: "123456789"

    - name: meta_ads
      credentials: .aiwg/marketing/config/meta-creds.json
      ad_account_id: "act_123456"

  transformations:
    - name: normalize_naming
      rules:
        - source: google_ads
          campaign_pattern: "^GA_"
        - source: meta_ads
          campaign_pattern: "^META_"

    - name: calculate_metrics
      metrics: [ctr, cpc, cpa, roas]

    - name: apply_attribution
      model: position_based
      lookback_window: 30

  output:
    - type: json
      path: .aiwg/marketing/data/
    - type: csv
      path: .aiwg/marketing/reports/
    - type: dashboard
      tool: internal

  alerts:
    - name: spend_anomaly
      condition: daily_spend > avg_spend * 1.5
      notify: [marketing-team]

    - name: conversion_drop
      condition: daily_conversions < avg_conversions * 0.5
      notify: [marketing-team, analytics]
```

## Data Quality Checks

```yaml
quality_checks:
  completeness:
    - all_platforms_reporting: true
    - date_gaps: none_allowed
    - metric_nulls: <5%

  consistency:
    - cross_platform_totals: ±5% variance
    - historical_trend: ±20% from avg
    - attribution_sum: 100%

  freshness:
    - max_age: 24h
    - preferred_age: 4h
    - alert_threshold: 12h

  anomaly_detection:
    - z_score_threshold: 3
    - min_data_points: 14
    - metrics_to_monitor:
      - spend
      - conversions
      - ctr
      - cpc
```

## Pipeline Report Format

```markdown
# Marketing Data Pipeline Report

**Run ID**: PIPE-2025-12-08-1400
**Status**: Completed with Warnings
**Duration**: 4m 32s
**Date Range**: 2025-11-08 to 2025-12-08

## Data Collection Summary

| Source | Status | Records | Freshness |
|--------|--------|---------|-----------|
| Google Ads | ✅ Success | 45,231 | 2h ago |
| Meta Ads | ✅ Success | 32,156 | 3h ago |
| Google Analytics | ✅ Success | 128,459 | 1h ago |
| Mailchimp | ⚠️ Partial | 5,234 | 6h ago |
| Instagram | ✅ Success | 1,847 | 4h ago |

## Data Quality

| Check | Status | Details |
|-------|--------|---------|
| Completeness | ✅ Pass | All platforms reporting |
| Consistency | ⚠️ Warning | GA vs Ads conversion ±8% |
| Freshness | ✅ Pass | All data <12h old |
| Anomaly | ✅ Pass | No anomalies detected |

## Aggregated Metrics

### Overall Performance (Last 30 Days)

| Metric | Value | vs Prior Period | vs Target |
|--------|-------|-----------------|-----------|
| Spend | $125,432 | +12% | On target |
| Impressions | 8.2M | +18% | +5% |
| Clicks | 156,234 | +15% | +8% |
| Conversions | 3,421 | +8% | -2% |
| Revenue | $342,100 | +22% | +12% |

### By Channel

| Channel | Spend | Conv | CPA | ROAS |
|---------|-------|------|-----|------|
| Paid Search | $45,230 | 1,234 | $36.67 | 3.2x |
| Paid Social | $38,450 | 987 | $38.95 | 2.8x |
| Email | $5,200 | 543 | $9.58 | 8.5x |
| Organic Social | $0 | 321 | - | - |
| Display | $36,552 | 336 | $108.79 | 1.2x |

### Attribution Report

| Attribution Model | Conv Distrib |
|-------------------|--------------|
| Paid Search | 42% |
| Email | 24% |
| Paid Social | 18% |
| Organic | 12% |
| Direct | 4% |

## Alerts & Issues

### ⚠️ Warning: Mailchimp Data Delay
- **Issue**: Email metrics 6h stale (threshold: 4h)
- **Impact**: Email performance may be underreported
- **Action**: Retry scheduled for next run

### ⚠️ Warning: Cross-Platform Variance
- **Issue**: GA conversions vs Ad platform conversions ±8%
- **Expected**: ±5% variance
- **Cause**: Likely attribution window differences
- **Action**: Review attribution settings

## Output Files

- Raw data: `.aiwg/marketing/data/raw/2025-12-08/`
- Transformed: `.aiwg/marketing/data/transformed/2025-12-08.json`
- Report: `.aiwg/marketing/reports/daily-2025-12-08.csv`
- Dashboard updated: Yes

## Next Scheduled Run

**Time**: 2025-12-08 18:00 UTC
**Expected Duration**: ~5 minutes
```

## Usage Examples

### Full Data Refresh

```
User: "Refresh marketing analytics"

Skill executes:
1. Connect to all platforms
2. Pull latest data
3. Transform and aggregate
4. Generate report

Output:
"Data Pipeline Complete

Sources Updated:
✅ Google Ads (45K records)
✅ Meta Ads (32K records)
✅ Google Analytics (128K records)
✅ Email platforms (5K records)

Key Metrics (Last 30 Days):
- Total Spend: $125,432 (+12%)
- Conversions: 3,421 (+8%)
- ROAS: 2.73x

Data Quality: 2 warnings
- Mailchimp data stale (6h)
- Cross-platform variance 8%

Report: .aiwg/marketing/reports/daily-2025-12-08.md"
```

### Specific Channel Data

```
User: "Pull email campaign metrics"

Skill executes:
1. Connect to email platforms
2. Pull campaign data
3. Calculate email-specific metrics

Output:
"Email Data Updated

Campaigns: 12 active
Total Sends: 245,000
Open Rate: 24.5% (industry avg: 21%)
Click Rate: 3.2% (industry avg: 2.5%)
Unsubscribe: 0.3%

Top Performer: Holiday Sale Email
- Opens: 32%
- Clicks: 5.1%
- Revenue: $45,230

Data saved: .aiwg/marketing/data/email/2025-12-08.json"
```

### Data Quality Check

```
User: "Check marketing data quality"

Skill validates:
- Completeness
- Consistency
- Freshness
- Anomalies

Output:
"Data Quality Report

✅ Completeness: All sources reporting
⚠️ Consistency: 8% variance in conversions
✅ Freshness: All data <12h old
✅ Anomalies: None detected

Issue Details:
- GA reports 3,421 conversions
- Ad platforms report 3,695 conversions
- Delta: 274 (7.4%)
- Likely cause: Attribution windows

Recommendation: Align attribution windows across platforms"
```

## Integration

This skill uses:
- `project-awareness`: Identify connected platforms
- `artifact-metadata`: Track pipeline runs

## Agent Orchestration

```yaml
agents:
  data_collection:
    agent: data-analyst
    focus: Platform connections and data extraction

  analysis:
    agent: marketing-analyst
    focus: Metric interpretation and insights

  reporting:
    agent: reporting-specialist
    focus: Report generation and visualization
```

## Configuration

### Platform Credentials

```yaml
credentials_config:
  storage: .aiwg/marketing/config/
  encryption: required
  rotation: 90_days

  platforms:
    google_ads:
      type: oauth2
      refresh_token: encrypted
    meta_ads:
      type: access_token
      expiry_check: true
    mailchimp:
      type: api_key
      scoped: marketing
```

### Scheduling

```yaml
schedule_config:
  full_refresh:
    cron: "0 */4 * * *"
    description: Every 4 hours

  daily_report:
    cron: "0 8 * * *"
    description: Daily at 8 AM

  weekly_summary:
    cron: "0 9 * * 1"
    description: Monday at 9 AM
```

## Output Locations

- Raw data: `.aiwg/marketing/data/raw/`
- Transformed data: `.aiwg/marketing/data/transformed/`
- Reports: `.aiwg/marketing/reports/`
- Pipeline logs: `.aiwg/marketing/logs/pipeline/`

## References

- Platform configs: .aiwg/marketing/config/
- Attribution models: docs/attribution-models.md
- Data dictionary: .aiwg/marketing/data/dictionary.md
