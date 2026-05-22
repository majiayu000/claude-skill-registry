---
name: slo-designer
description: Design Service Level Objectives (SLOs) with SLIs, targets, alerting thresholds, and error budget calculations following Google SRE best practices. Use when defining reliability targets, designing SLOs, calculating error budgets, or establishing service level indicators.
license: MIT
metadata:
  version: 1.0.0
  model: claude-sonnet-4-5
  source: Google SRE Book
---

# SLO Designer

When this skill activates, you guide users through designing production-ready Service Level Objectives. Your role is to help identify critical user journeys, define measurable SLIs, set appropriate targets, and calculate error budgets.

## Triggers

Activate when the user:

- "Design SLOs for my service"
- "Define reliability targets"
- "Calculate error budget"
- "Set up service level objectives"
- "Define SLIs for this system"
- "SLO design for API"
- "What should my availability target be?"

## Core Concepts

| Term | Definition | Example |
|------|------------|---------|
| **SLI** | Service Level Indicator. Metric measuring service quality. | p99 latency, availability % |
| **SLO** | Service Level Objective. Target value for an SLI. | p99 < 200ms, 99.9% availability |
| **SLA** | Service Level Agreement. Contract with consequences. | 99.95% uptime or credits issued |
| **Error Budget** | Allowed failures before SLO breach. | 0.1% = 43 min/month downtime |
| **Burn Rate** | Speed of error budget consumption. | 2x burn = budget exhausted in 15 days |

## Common SLI Categories

### Availability

Percentage of successful requests.

```python
availability_sli = (successful_requests / total_requests) * 100
```

Good for: APIs, web services, databases.

### Latency

Response time percentiles (p50, p95, p99).

```python
latency_sli = percentile(response_times, 99)
```

Good for: User-facing endpoints, real-time systems.

### Throughput

Requests per second (RPS) or transactions.

```python
throughput_sli = requests_per_second / expected_baseline
```

Good for: Batch processing, high-volume systems.

### Error Rate

Percentage of 5xx responses.

```python
error_rate_sli = (error_responses / total_responses) * 100
```

Good for: APIs, microservices.

### Correctness

Percentage of correct results.

```python
correctness_sli = (correct_results / total_results) * 100
```

Good for: Data pipelines, ML inference, calculations.

## Process

```text
1. DISCOVERY          Identify critical user journeys
        |             What matters to users?
        v
2. SLI DEFINITION     Select measurable indicators
        |             How do we measure success?
        v
3. SLO TARGETS        Set achievable targets
        |             What should we promise?
        v
4. ERROR BUDGET       Calculate allowed failures
        |             How much can we fail?
        v
5. ALERTING           Define burn rate alerts
        |             When do we intervene?
        v
6. DOCUMENTATION      Generate SLO document
```

## Scripts

### calculate_error_budget.py

Calculate error budget for a given SLO target:

```bash
python3 .claude/skills/slo-designer/scripts/calculate_error_budget.py \
  --target 99.9 \
  --period monthly
```

**Arguments:**

| Argument | Required | Description |
|----------|----------|-------------|
| `--target` | Yes | SLO target percentage (e.g., 99.9) |
| `--period` | No | Time period: monthly, weekly, daily, quarterly (default: monthly) |
| `--format` | No | Output format: text, json, markdown (default: text) |

**Exit Codes:**

- 0: Success
- 1: Invalid arguments
- 2: Calculation error

### generate_slo_document.py

Generate a complete SLO document from configuration:

```bash
python3 .claude/skills/slo-designer/scripts/generate_slo_document.py \
  --config path/to/slo-config.yaml \
  --output docs/slo-document.md
```

## Question Framework

Use these questions to gather requirements:

### 1. Service Context

- What is the service name and purpose?
- Who are the primary users (internal, external, both)?
- What is the business criticality (revenue impact)?
- Are there existing SLAs or customer expectations?

### 2. User Journeys

- What are the 3-5 most critical user journeys?
- What actions must succeed for users to be satisfied?
- What is the acceptable response time for each journey?
- Which failures are most impactful?

### 3. Current State

- What metrics are already collected?
- What is the current availability (if known)?
- What are the current p50, p95, p99 latencies?
- What is the current error rate?

### 4. Infrastructure

- What is the deployment architecture?
- Are there external dependencies?
- What is the disaster recovery capability?
- What maintenance windows exist?

### 5. Targets

- What availability level is appropriate?
- What latency targets align with user expectations?
- How much error budget can the team responsibly manage?
- What alerting thresholds make sense?

## SLO Target Guidelines

| Service Type | Typical Availability | Latency (p99) | Error Rate |
|--------------|---------------------|---------------|------------|
| Consumer Web | 99.9% (43 min/month) | < 500ms | < 1% |
| Internal API | 99.5% (3.6 hr/month) | < 1s | < 2% |
| B2B Critical | 99.95% (22 min/month) | < 200ms | < 0.1% |
| Batch Jobs | 99% (7.3 hr/month) | N/A | < 5% |
| Real-time | 99.99% (4 min/month) | < 100ms | < 0.01% |

**Choosing a target:**

- Start conservative (lower targets are easier to meet)
- Consider external dependencies (chain reliability)
- Account for maintenance windows
- Leave margin from SLA (SLO should be tighter)

## Error Budget Table

| SLO Target | Error Budget | Monthly Downtime | Weekly Downtime |
|------------|--------------|------------------|-----------------|
| 99% | 1% | 7h 18m | 1h 41m |
| 99.5% | 0.5% | 3h 39m | 50m |
| 99.9% | 0.1% | 43m 50s | 10m |
| 99.95% | 0.05% | 21m 55s | 5m |
| 99.99% | 0.01% | 4m 23s | 1m |
| 99.999% | 0.001% | 26s | 6s |

## Burn Rate Alerting

Configure alerts based on budget consumption rate:

| Alert Severity | Burn Rate | Time to Exhaust | Action |
|----------------|-----------|-----------------|--------|
| Warning | 1x | 30 days | Monitor closely |
| Elevated | 2x | 15 days | Investigate |
| Urgent | 6x | 5 days | Prioritize fix |
| Critical | 14.4x | 2 days | Immediate action |
| Emergency | 36x | 20 hours | All hands |

**Multi-window alerting:**

```text
Alert if:
  burn_rate_1h > 14.4 AND burn_rate_6h > 6
  OR
  burn_rate_6h > 6 AND burn_rate_24h > 2
```

## Output Template

Generate this structure:

```markdown
# SLO Document: [Service Name]

## Service Overview
- **Name**: [Service name]
- **Owner**: [Team name]
- **Description**: [What the service does]
- **Business Criticality**: [Low/Medium/High/Critical]

## Critical User Journeys
1. [Journey 1]: [Description]
2. [Journey 2]: [Description]
3. [Journey 3]: [Description]

## Service Level Indicators

### SLI 1: Availability
- **Definition**: Percentage of successful HTTP requests
- **Measurement**: `sum(rate(http_requests_total{status!~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
- **Data Source**: Prometheus metrics

### SLI 2: Latency
- **Definition**: 99th percentile response time
- **Measurement**: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`
- **Data Source**: Prometheus metrics

## Service Level Objectives

| SLI | Target | Measurement Window | Rationale |
|-----|--------|-------------------|-----------|
| Availability | 99.9% | 30-day rolling | Industry standard for user-facing APIs |
| Latency (p99) | < 200ms | 30-day rolling | User research shows frustration above 200ms |

## Error Budgets

| SLO | Error Budget | Monthly Allowance | Current Consumption |
|-----|--------------|-------------------|---------------------|
| Availability 99.9% | 0.1% | 43 minutes | [Current] |
| Latency p99 < 200ms | 0.1% | 43 minutes | [Current] |

## Alerting Strategy

### Page-worthy Alerts (Critical)
- Burn rate > 14.4x for 1 hour AND > 6x for 6 hours
- Action: Immediate response required

### Ticket-worthy Alerts (Warning)
- Burn rate > 2x for 24 hours
- Action: Investigate within 1 business day

## Implementation Checklist
- [ ] Metrics collection configured
- [ ] SLO dashboard created
- [ ] Alerts configured
- [ ] Runbook documented
- [ ] Team trained on error budget policy
```

## Related Concepts

### SLO vs SLA

- **SLO**: Internal target. No contractual penalty.
- **SLA**: External contract. Financial consequences.
- **Best Practice**: SLO should be stricter than SLA to provide buffer.

### Error Budget Policy

When error budget is exhausted:

1. Freeze non-critical feature work
2. Prioritize reliability improvements
3. Conduct incident reviews
4. Address technical debt

When error budget is healthy:

1. Invest in new features
2. Accept more risk
3. Run experiments

## References

- [Google SRE Book - SLOs](https://sre.google/sre-book/service-level-objectives/)
- [The Art of SLOs](https://sre.google/workbook/slo-engineering/)
- [Implementing SLOs](https://sre.google/workbook/implementing-slos/)
