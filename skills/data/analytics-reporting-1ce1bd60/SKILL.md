---
name: analytics-reporting
description: DevRel metrics, analytics dashboards, and program reporting
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 07-metrics-analyst
bond_type: PRIMARY_BOND
---

# DevRel Analytics & Reporting

Measure **program impact** with data-driven metrics and reporting.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - report_type: enum[pulse, monthly, quarterly, annual]
    - metrics_focus: array[string]
  optional:
    - date_range: object{start, end}
    - comparison_period: enum[wow, mom, yoy]
```

### Output
```yaml
output:
  report:
    summary: object
    visualizations: array[Chart]
    insights: array[string]
    recommendations: array[Action]
```

## Key Metrics Framework

### AAARRRP Model for DevRel

| Stage | Metrics |
|-------|---------|
| **Awareness** | Impressions, reach, brand mentions |
| **Acquisition** | Signups, registrations, first visits |
| **Activation** | First API call, tutorial completion |
| **Retention** | MAU, DAU, repeat usage |
| **Revenue** | Conversions, upgrades, pipeline |
| **Referral** | NPS, word-of-mouth, shares |
| **Product** | Feature adoption, feedback quality |

## Metrics by Category

### Community Metrics
```yaml
growth:
  - total_members
  - new_members_per_week
  - member_retention_30d

engagement:
  - daily_active_users
  - messages_per_day
  - questions_answered
  - response_time_avg
```

### Content Metrics
```yaml
reach:
  - page_views
  - unique_visitors
  - social_impressions

engagement:
  - time_on_page
  - scroll_depth
  - shares_and_saves

conversion:
  - cta_clicks
  - signups_from_content
  - doc_to_api_calls
```

### Event Metrics
```yaml
attendance:
  - registrations
  - show_up_rate
  - session_attendance

satisfaction:
  - nps_score
  - session_ratings
  - feedback_sentiment

business:
  - leads_generated
  - pipeline_influenced
```

## Dashboard Structure

```
Executive Dashboard
├── North Star Metric (primary KPI)
├── Funnel Overview
├── Weekly Trends
└── Key Highlights

Detailed Dashboards
├── Community Health
├── Content Performance
├── Event Analysis
└── Developer Journey
```

## Reporting Cadence

| Report | Frequency | Audience |
|--------|-----------|----------|
| Weekly pulse | Weekly | DevRel team |
| Monthly review | Monthly | Leadership |
| Quarterly OKR | Quarterly | Executives |
| Annual summary | Yearly | Company-wide |

## Attribution Challenges

Common issues:
- Multi-touch attribution
- Long sales cycles
- Indirect influence
- Data silos

Solutions:
- UTM parameters
- Developer surveys
- CRM integration
- Cohort analysis

## Retry Logic

```yaml
retry_patterns:
  data_incomplete:
    strategy: "Extend collection window"
    fallback: "Use available data with disclaimer"

  dashboard_error:
    strategy: "Refresh data sources"
    fallback: "Manual data pull"

  metric_anomaly:
    strategy: "Verify data integrity"
    fallback: "Flag for review"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Missing data | Gaps in metrics | Backfill or document |
| Wrong calculations | Audit reveals errors | Fix formula, rerun |
| Outdated dashboard | Stale data shown | Refresh pipeline |

## Debug Checklist

```
□ Data sources connected?
□ Date ranges correct?
□ Calculations verified?
□ Comparison periods aligned?
□ Visualizations rendering?
□ Insights actionable?
```

## Test Template

```yaml
test_analytics_reporting:
  unit_tests:
    - test_data_accuracy:
        assert: "Matches source systems"
    - test_calculations:
        assert: "Formulas correct"

  integration_tests:
    - test_dashboard_load:
        assert: "<5s load time"
```

## Observability

```yaml
metrics:
  - reports_generated: integer
  - dashboard_views: integer
  - data_freshness: duration
  - insight_accuracy: float
```

See `assets/` for dashboard templates.
