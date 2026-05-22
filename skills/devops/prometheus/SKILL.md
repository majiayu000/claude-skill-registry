---
name: prometheus
description: Prometheus ops skill for metrics instrumentation, scraping configuration, alerting (Alertmanager), dashboarding (Grafana), SLO/SLA monitoring, and troubleshooting missing/incorrect metrics. Use for tasks like designing alert rules, improving observability, and building production monitoring runbooks.
---

# prometheus

Use this skill for Prometheus + Alertmanager + Grafana 监控体系建设与运维。

## Defaults / assumptions to confirm

- Deployment: kube-prometheus-stack / standalone
- Alert routing: Alertmanager receivers (Slack/WeCom/PagerDuty)
- Metrics source: app exporters, node-exporter, kube-state-metrics
- Naming conventions and label cardinality constraints

## Workflow

1) Understand what to measure
- Identify golden signals: latency, traffic, errors, saturation.
- Map business KPIs and critical user journeys to technical indicators.

2) Instrumentation guidance
- Prefer stable metric names and bounded label sets.
- Avoid high-cardinality labels (user_id, request_id, raw URLs).
- Use histograms for latency (p50/p95/p99 via `histogram_quantile`).

3) Scraping configuration
- Confirm scrape targets (ServiceMonitor/PodMonitor or static configs).
- Ensure relabeling rules are correct; set scrape intervals/timeouts appropriately.

4) Alert design (practical)
- Alerts should be actionable and low-noise.
- Use multi-window multi-burn-rate for SLO alerts where applicable.
- Add `for:` to avoid flapping; include runbook links in annotations.

5) Dashboarding
- Provide per-service dashboards: RPS, p95 latency, error rate, resource usage.
- Add drill-down: by route group, instance, and dependency.

6) Troubleshooting checklist
- Missing metrics: target down, wrong labels, scrape failures, RBAC/network issues.
- Wrong metrics: unit mismatch, counter resets, histogram buckets incorrect.
- High load: cardinality explosion, too frequent scrapes, heavy queries.

## Outputs

- Metrics plan: required metrics, labels, and thresholds.
- Alert rules: PromQL + severity + routing + runbook.
- Grafana dashboard layout and key panels.
- Runbook: symptom → checks → mitigation → rollback.

