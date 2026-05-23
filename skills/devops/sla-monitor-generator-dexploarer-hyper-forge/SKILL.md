---
name: sla-monitor-generator
description: Generate SLA/SLO/SLI monitoring configurations for reliability tracking and error budget management. Activates for SLO setup, reliability targets, and error budget configuration.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# SLA Monitor Generator

Define and monitor Service Level Objectives (SLOs) and track error budgets.

## SLO Definition Example

```yaml
slos:
  - name: api-availability
    sli: 
      metric: http_requests_total
      filter: status < 500
    target: 99.9  # 99.9% availability
    window: 30d
    
  - name: api-latency
    sli:
      metric: http_request_duration_seconds
      percentile: 99
    target: 200  # 200ms at p99
    window: 30d

  - name: error-rate
    sli:
      metric: http_requests_total
      filter: status >= 500
    target: 0.1  # < 0.1% error rate
    window: 30d
```

## Prometheus AlertManager Rules

```yaml
groups:
  - name: slo-alerts
    rules:
      - alert: SLOBudgetBurnRate
        expr: |
          (
            1 - (sum(rate(http_requests_total{status!~"5.."}[5m])) 
                 / sum(rate(http_requests_total[5m])))
          ) > 0.001 * 14.4
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Fast burn rate detected - 2% budget in 1 hour"
```

## Best Practices
- ✅ Define SLIs based on user experience
- ✅ Set realistic SLO targets (99.9% not 100%)
- ✅ Track error budgets continuously
- ✅ Alert on burn rate, not just breaches
- ✅ Review and adjust SLOs quarterly
