---
name: prd-v08-monitoring-setup
description: >
  Define monitoring strategy, metrics collection, and alerting thresholds during PRD v0.8 Deployment & Ops.
  Triggers on requests to set up monitoring, define alerts, or when user asks "what should we monitor?",
  "alerting strategy", "observability", "metrics", "SLOs", "dashboards", "monitoring setup".
  Outputs MON- entries with monitoring rules and alert configurations.
---

# Monitoring Setup

Position in workflow: v0.8 Runbook Creation → **v0.8 Monitoring Setup** → v0.9 GTM Strategy

## Purpose

Define what to measure, when to alert, and how to visualize system health—creating the observability foundation that enables rapid incident detection and resolution.

## Core Concept: Monitoring as Early Warning

> Monitoring is not about collecting data—it is about **detecting problems before users do**. Every metric should answer: "Is this working? If not, what's broken?"

## Monitoring Layers

| Layer | What to Measure | Why It Matters |
|-------|-----------------|----------------|
| **Infrastructure** | CPU, memory, disk, network | System health foundation |
| **Application** | Latency, errors, throughput | User-facing performance |
| **Business** | Signups, conversions, revenue | Product health |
| **User Experience** | Page load, interaction time | Real user impact |

## Execution

1. **Define SLOs (Service Level Objectives)**
   - What uptime do we promise?
   - What latency is acceptable?
   - What error rate is tolerable?

2. **Identify key metrics per layer**
   - Infrastructure: Resource utilization
   - Application: RED metrics (Rate, Errors, Duration)
   - Business: KPI- from v0.3 and v0.9
   - User: Core Web Vitals, journey completion

3. **Set alert thresholds**
   - Warning: Investigate soon
   - Critical: Act immediately
   - Base on SLOs and historical data

4. **Map alerts to runbooks**
   - Every critical alert → RUN- procedure
   - No alert without action path

5. **Design dashboards**
   - Overview: System health at a glance
   - Deep-dive: Per-service details
   - Business: KPI tracking

6. **Create MON- entries** with full traceability

## MON- Output Template

```
MON-XXX: [Monitoring Rule Title]
Type: [Metric | Alert | Dashboard | SLO]
Layer: [Infrastructure | Application | Business | User Experience]
Owner: [Team responsible for this metric/alert]

For Metric Type:
  Name: [metric.name.format]
  Description: [What this measures]
  Unit: [count | ms | percentage | bytes]
  Source: [Where this comes from]
  Aggregation: [avg | sum | p50 | p95 | p99]
  Retention: [How long to keep data]

For Alert Type:
  Metric: [MON-YYY or metric name]
  Condition: [Threshold expression]
  Window: [Time window for evaluation]
  Severity: [Critical | Warning | Info]
  Runbook: [RUN-XXX to follow when fired]
  Notification:
    - Channel: [Slack, PagerDuty, Email]
    - Recipients: [Team or individuals]
  Silencing: [When to suppress, e.g., maintenance windows]

For Dashboard Type:
  Purpose: [What questions this answers]
  Audience: [Who uses this dashboard]
  Panels: [List of visualizations]
  Refresh: [How often to update]

For SLO Type:
  Objective: [What we promise]
  Target: [Percentage, e.g., 99.9%]
  Window: [Rolling 30 days]
  Error Budget: [How much downtime allowed]
  Alerting: [When error budget is at risk]

Linked IDs: [API-XXX, UJ-XXX, KPI-XXX, RUN-XXX related]
```

**Example MON- entries:**

```
MON-001: API Request Latency (p95)
Type: Metric
Layer: Application
Owner: Backend Team

Name: api.request.latency.p95
Description: 95th percentile response time for all API endpoints
Unit: ms
Source: Application APM (Datadog/New Relic)
Aggregation: p95
Retention: 90 days

Linked IDs: API-001 to API-020
```

```
MON-002: High Latency Alert
Type: Alert
Layer: Application
Owner: Backend Team

Metric: MON-001 (api.request.latency.p95)
Condition: > 500ms
Window: 5 minutes
Severity: Warning
Runbook: RUN-006 (Performance Degradation Investigation)

Notification:
  - Channel: Slack #backend-alerts
  - Recipients: Backend on-call

Silencing: During scheduled deployments (DEP-002 windows)

Linked IDs: MON-001, RUN-006, DEP-002
```

```
MON-003: Critical Latency Alert
Type: Alert
Layer: Application
Owner: Backend Team

Metric: MON-001 (api.request.latency.p95)
Condition: > 2000ms
Window: 2 minutes
Severity: Critical
Runbook: RUN-006 (Performance Degradation Investigation)

Notification:
  - Channel: PagerDuty
  - Recipients: Backend on-call, Tech Lead

Silencing: None (always alert on critical)

Linked IDs: MON-001, RUN-006
```

```
MON-004: API Availability SLO
Type: SLO
Layer: Application
Owner: Platform Team

Objective: API endpoints return non-5xx response
Target: 99.9%
Window: Rolling 30 days
Error Budget: 43.2 minutes/month

Alerting:
  - 50% budget consumed → Warning to engineering
  - 75% budget consumed → Critical, freeze non-essential deploys
  - 100% budget consumed → Incident review required

Linked IDs: API-001 to API-020, DEP-003
```

```
MON-005: System Health Dashboard
Type: Dashboard
Layer: Infrastructure + Application
Owner: Platform Team

Purpose: Quick health check for on-call engineers
Audience: On-call, engineering leadership
Panels:
  - API Request Rate (last 1h)
  - API Latency (p50, p95, p99)
  - Error Rate by Endpoint
  - Active Alerts
  - Database Connection Pool
  - CPU/Memory by Service
Refresh: 30 seconds

Linked IDs: MON-001, MON-002, MON-003
```

## The RED Method (Application Monitoring)

For each service, measure:

| Metric | What It Measures | Alert Threshold |
|--------|------------------|-----------------|
| **Rate** | Requests per second | Anomaly detection |
| **Errors** | Failed requests / total | >1% warning, >5% critical |
| **Duration** | Request latency (p95, p99) | >500ms warning, >2s critical |

## The USE Method (Infrastructure Monitoring)

For each resource (CPU, memory, disk, network):

| Metric | What It Measures | Alert Threshold |
|--------|------------------|-----------------|
| **Utilization** | % of capacity used | >80% warning, >95% critical |
| **Saturation** | Queue depth, waiting | >0 for critical resources |
| **Errors** | Error count/rate | Any errors = investigate |

## SLO Framework

| Tier | Availability | Latency (p95) | Use For |
|------|--------------|---------------|---------|
| **Tier 1** | 99.99% (52 min/yr) | <100ms | Payment, auth |
| **Tier 2** | 99.9% (8.7 hr/yr) | <500ms | Core features |
| **Tier 3** | 99% (3.6 days/yr) | <2s | Background jobs |

## Alert Severity Matrix

| Severity | User Impact | Response Time | Notification |
|----------|-------------|---------------|--------------|
| **Critical** | Service unusable | <5 min | PagerDuty (wake up) |
| **Warning** | Degraded experience | <30 min | Slack (business hours) |
| **Info** | No immediate impact | Next day | Dashboard/log |

## Dashboard Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Answer questions** | Each panel answers "Is X working?" |
| **Hierarchy** | Overview → Service → Component |
| **Context** | Show thresholds, comparisons |
| **Actionable** | Link to runbooks from alerts |
| **Fast** | Quick load, auto-refresh |

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Alert fatigue** | Too many alerts, team ignores | Tune thresholds, remove noise |
| **No runbook link** | Alert fires, no one knows what to do | Every alert → RUN- |
| **Vanity metrics** | "1 million requests!" without context | Focus on user-impacting metrics |
| **Missing baselines** | No historical comparison | Establish baselines before launch |
| **Over-monitoring** | 500 metrics, can't find signal | Focus on RED/USE fundamentals |
| **Under-monitoring** | "We'll add monitoring later" | Monitoring ships with code |

## Quality Gates

Before proceeding to v0.9 GTM Strategy:

- [ ] SLOs defined for critical services (MON- SLO type)
- [ ] RED metrics configured for application layer
- [ ] USE metrics configured for infrastructure layer
- [ ] Critical alerts linked to RUN- procedures
- [ ] Overview dashboard created for on-call
- [ ] Alert notification channels configured
- [ ] Baseline metrics established from staging

## Downstream Connections

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **On-Call Team** | MON- alerts trigger response | MON-003 → page engineer |
| **v0.9 Launch Metrics** | MON- provides baseline data | MON-001 baseline → KPI-010 target |
| **Post-Mortems** | MON- data for incident analysis | "MON-005 showed spike at 14:32" |
| **Capacity Planning** | MON- trends inform scaling | USE metrics → infrastructure planning |
| **DEP- Rollback** | MON- thresholds trigger rollback | MON-002 breach → DEP-003 rollback |

## Detailed References

- **Monitoring stack examples**: See `references/monitoring-stack.md`
- **MON- entry template**: See `assets/mon-template.md`
- **SLO calculation guide**: See `references/slo-guide.md`
- **Dashboard best practices**: See `references/dashboard-guide.md`
