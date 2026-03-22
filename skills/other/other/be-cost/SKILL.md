---
name: be-cost-monitoring
description: Monitor and analyze backend GPU costs for LTX API and LTX Studio. Use when analyzing cost trends, detecting anomalies, breaking down costs by endpoint/model/org/process, monitoring utilization, or investigating cost efficiency drift.
tags: [monitoring, costs, gpu, infrastructure, alerts]
compatibility:
  - BigQuery access (ltx-dwh-prod-processed)
  - bq CLI or BigQuery console
---

# Backend Cost Monitoring

## When to use

- "Monitor GPU costs"
- "Analyze cost trends (daily/weekly/monthly)"
- "Detect cost anomalies or spikes"
- "Break down API costs by endpoint/model/org"
- "Break down Studio costs by process/workspace"
- "Compare API vs Studio cost distribution"
- "Investigate cost-per-request efficiency drift"
- "Monitor GPU utilization and idle costs"
- "Alert on cost budget breaches"
- "Day-over-day or week-over-week cost comparisons"

## Steps

### 1. Gather Requirements

Ask the user:
- **What to monitor**: Total costs, cost by product/feature, cost efficiency, utilization, anomalies
- **Scope**: LTX API, LTX Studio, or both? Specific endpoint/org/process?
- **Time window**: Daily, weekly, monthly? How far back?
- **Analysis type**: Trends, comparisons (DoD/WoW), anomaly detection, breakdowns
- **Alert threshold** (if setting up alerts): Absolute ($X/day) or relative (spike > X% vs baseline)

### 2. Read Shared Knowledge

Before writing SQL:
- **`shared/product-context.md`** — LTX products and business context
- **`shared/bq-schema.md`** — GPU cost table schema (lines 418-615)
- **`shared/metric-standards.md`** — GPU cost metric patterns (section 13)
- **`shared/event-registry.yaml`** — Feature events (if analyzing feature-level costs)
- **`shared/gpu-cost-query-templates.md`** — 11 production-ready SQL queries
- **`shared/gpu-cost-analysis-patterns.md`** — Analysis workflows and benchmarks

Key learnings:
- Table: `ltx-dwh-prod-processed.gpu_costs.gpu_request_attribution_and_cost`
- Partitioned by `dt` (DATE) — always filter for performance
- `cost_category`: inference (requests), idle, overhead, unused
- Total cost = `row_cost + attributed_idle_cost + attributed_overhead_cost` (inference rows only)
- For infrastructure cost: `SUM(row_cost)` across all categories

### 3. Run Query Templates

**If user didn't specify anything:** Run all 11 query templates from `shared/gpu-cost-query-templates.md` to provide comprehensive cost overview.

**If user specified specific analysis:** Select appropriate template:

| User asks... | Use template |
|-------------|-------------|
| "What are total costs?" | Daily Total Cost (API + Studio) |
| "Break down API costs" | API Cost by Endpoint & Model |
| "Break down Studio costs" | Studio Cost by Process |
| "Yesterday vs day before" | Day-over-Day Comparison |
| "This week vs last week" | Week-over-Week Comparison |
| "Detect cost spikes" | Anomaly Detection (Z-Score) |
| "GPU utilization breakdown" | Utilization by Cost Category |
| "Cost efficiency by model" | Cost per Request by Model |
| "Which orgs cost most?" | API Cost by Organization |

See `shared/gpu-cost-query-templates.md` for all 11 query templates.

### 4. Execute Query

Run query using:
```bash
bq --project_id=ltx-dwh-explore query --use_legacy_sql=false --format=pretty "
<query>
"
```

Or use BigQuery console with project `ltx-dwh-explore`.

### 5. Analyze Results

**For cost trends:**
- Compare current period vs baseline (7-day avg, prior week, prior month)
- Calculate % change and flag significant shifts (>15-20%)

**For anomaly detection:**
- Flag days with Z-score > 2 (cost or volume deviates > 2 std devs from rolling avg)
- Investigate root cause: specific endpoint/model/org, error rate spike, billing type change

**For breakdowns:**
- Identify top cost drivers (endpoint, model, org, process)
- Calculate cost per request to spot efficiency issues
- Check failure costs (wasted spend on errors)

### 6. Present Findings

Format results with:
- **Summary**: Key finding (e.g., "GPU costs spiked 45% yesterday")
- **Root cause**: What drove the change (e.g., "LTX API /v1/text-to-video requests +120%")
- **Breakdown**: Top contributors by dimension
- **Recommendation**: Action to take (investigate org X, optimize model Y, alert team)

### 7. Set Up Alert (if requested)

For ongoing monitoring:
1. Save SQL query
2. Set up in BigQuery scheduled query or Hex Thread
3. Configure notification threshold
4. Route alerts to Slack channel or Linear issue

## Schema Reference

For detailed table schema including all dimensions, columns, and cost calculations, see `references/schema-reference.md`.

## Reference Files

| File | Read when |
|------|-----------|
| `references/schema-reference.md` | GPU cost table dimensions, columns, and cost calculations |
| `shared/bq-schema.md` | Understanding GPU cost table schema (lines 418-615) |
| `shared/metric-standards.md` | GPU cost metric SQL patterns (section 13) |
| `shared/gpu-cost-query-templates.md` | Selecting query template for analysis (11 production-ready queries) |
| `shared/gpu-cost-analysis-patterns.md` | Interpreting results, workflows, benchmarks, investigation playbooks |

## Rules

### Query Best Practices

- **DO** always filter on `dt` partition column for performance
- **DO** filter `cost_category = 'inference'` for request-level analysis
- **DO** exclude Lightricks team requests with `is_lt_team IS FALSE` for customer-facing cost analysis
- **DO** include LT team requests only when analyzing total infrastructure spend or debugging
- **DO** use `ltx-dwh-explore` as execution project
- **DO** calculate cost per request with `SAFE_DIVIDE` to avoid division by zero
- **DO** compare against baseline (7-day avg, prior period) for trends
- **DO** round cost values to 2 decimal places for readability

### Cost Calculation

- **DO** sum all three cost columns (row_cost + attributed_idle + attributed_overhead) for fully loaded cost per request
- **DO** use `SUM(row_cost)` across all rows for total infrastructure cost
- **DO NOT** sum row_cost + attributed_* across all cost_categories (double-counting)
- **DO NOT** mix inference and non-inference rows in same aggregation without filtering

### Analysis

- **DO** flag anomalies with Z-score > 2 (cost or volume deviation > 2 std devs)
- **DO** investigate failure costs (wasted spend on errors)
- **DO** break down by endpoint/model for API, by process for Studio
- **DO** check cost per request trends to spot efficiency degradation
- **DO** validate results against total infrastructure spend

### Alerts

- **DO** set thresholds based on historical baseline, not absolute values
- **DO** alert engineering team for cost spikes > 30% vs baseline
- **DO** include cost breakdown and root cause in alerts
- **DO** route API cost alerts to API team, Studio alerts to Studio team
