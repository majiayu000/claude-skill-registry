---
name: api-runtime-monitor
description: Monitors LTX API runtime performance, latency, error rates, and throughput. Alerts on performance degradation or errors.
tags: [monitoring, api, performance, latency, errors]
---

# API Runtime Monitor

## When to use

- "Monitor API latency"
- "Alert on API errors"
- "Track API throughput"
- "Monitor inference time"
- "Alert on API performance degradation"

## What it monitors

- **Latency**: Request processing time, inference time, queue time
- **Error rates**: % of failed requests, error types, error sources
- **Throughput**: Requests per hour/day, by endpoint/model
- **Performance**: P50/P95/P99 latency, success rate
- **Utilization**: API usage by org, model, resolution

## Steps

1. **Gather requirements from user:**
   - Which performance metric to monitor (latency, errors, throughput)
   - Alert threshold (e.g., "P95 latency > 30s", "error rate > 5%", "throughput drops > 20%")
   - Time window (hourly, daily)
   - Scope (all requests, specific endpoint, specific org)
   - Notification channel

2. **Read shared files:**
   - `shared/bq-schema.md` — GPU cost table (has API runtime data) and ltxvapi tables
   - `shared/metric-standards.md` — Performance metric patterns

3. **Identify data source:**
   - For LTX API: Use `ltxvapi_api_requests_with_be_costs` or `gpu_request_attribution_and_cost`
   - **Key columns explained:**
     - `request_processing_time_ms`: Total time from request submission to completion
     - `request_inference_time_ms`: GPU processing time (actual model inference)
     - `request_queue_time_ms`: Time waiting in queue before processing starts
     - `result`: Request outcome (success, failed, timeout, etc.)
     - `error_type`: Classification of errors (infrastructure vs applicative)
     - `endpoint`: API endpoint called (e.g., /generate, /upscale)
     - `model_type`: Model used (ltxv2, retake, etc.)
     - `org_name`: Customer organization making the request

4. **Write monitoring SQL:**
   - Query relevant performance metric
   - Calculate percentiles (P50, P95, P99) for latency
   - Calculate error rate (failed / total requests)
   - Compare against baseline

5. **Present to user:**
   - Show SQL query
   - Show example alert format with performance breakdown
   - Confirm threshold values

6. **Set up alert** (manual for now):
   - Document SQL
   - Configure notification to engineering team

## Reference files

| File | Read when |
|------|-----------|
| `shared/product-context.md` | LTX products and business context |
| `shared/bq-schema.md` | API tables and GPU cost table schema |
| `shared/metric-standards.md` | Performance metric patterns |
| `shared/event-registry.yaml` | Feature events (if analyzing event-driven metrics) |
| `shared/gpu-cost-query-templates.md` | GPU cost queries (if analyzing cost-related performance) |
| `shared/gpu-cost-analysis-patterns.md` | Cost analysis patterns (if analyzing cost-related performance) |

## Rules

- DO use APPROX_QUANTILES for percentile calculations (P50, P95, P99)
- DO separate errors by error_source (infrastructure vs applicative)
- DO filter by result = 'success' for success rate calculations
- DO break down by endpoint, model, and resolution for detailed analysis
- DO compare current performance against historical baseline
- DO alert engineering team for infrastructure errors, product team for applicative errors
- DO partition by dt for performance
