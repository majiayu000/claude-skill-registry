---
name: fabric-rti-perf-remediate
description: Diagnose and resolve performance issues in Microsoft Fabric Real-Time Intelligence including Eventhouse, KQL databases, Eventstream, and ingestion pipelines. Use when asked to troubleshoot slow KQL queries, high Eventhouse CPU or memory, ingestion latency or failures, Eventstream throughput problems, capacity throttling (HTTP 430), cache policy tuning, materialized view lag, or Always-On configuration. Covers workspace monitoring, Fabric Capacity Metrics app, query optimization, and streaming diagnostics.
license: Complete terms in LICENSE.txt
---
# Fabric Real-Time Intelligence Performance remediate

Systematic toolkit for diagnosing and resolving performance issues across the Microsoft Fabric Real-Time Intelligence stack: Eventhouse, KQL databases, Eventstream, ingestion pipelines, and capacity management.

## When to Use This Skill

- Eventhouse queries running slowly or timing out
- Ingestion latency or failures into KQL databases
- Eventstream throughput bottlenecks or backlog growth
- Capacity throttling errors (HTTP 430, TooManyRequestsForCapacity)
- High CPU, memory, or cache utilization on Eventhouse
- Materialized view lag or freshness issues
- Always-On and minimum consumption sizing decisions
- Workspace monitoring setup and dashboard interpretation
- KQL query optimization for Real-Time Intelligence workloads

## Prerequisites

- Microsoft Fabric workspace with Contributor or higher permissions
- Workspace monitoring enabled (for query/ingestion logs)
- Fabric Capacity Metrics app installed (for capacity-level analysis)
- KQL Queryset or Eventhouse query editor access

## Step-by-Step Workflows

### Workflow 1: Diagnose Slow KQL Queries

1. **Enable workspace monitoring** if not already active. See [workspace-monitoring.md](./references/workspace-monitoring.md)
2. **Identify expensive queries** using the diagnostic script:
   Run [diagnose-slow-queries.kql](./scripts/diagnose-slow-queries.kql) against the monitoring Eventhouse
3. **Analyze query patterns** — filter by Top CPU Time, Top Duration, or Memory Peak
4. **Apply KQL optimization rules** from [kql-optimization.md](./references/kql-optimization.md)
5. **Validate improvement** by re-running the query and comparing duration/CPU metrics

### Workflow 2: Troubleshoot Ingestion Issues

1. **Check ingestion results logs** using [diagnose-ingestion.kql](./scripts/diagnose-ingestion.kql)
2. **Review Eventstream data insights** — check IncomingMessages, OutgoingMessages, BackloggedInputEvents, and WatermarkDelay metrics
3. **Identify failure patterns** — deserialization errors, schema mismatches, throttling
4. **Apply throughput tuning** per [ingestion-remediate.md](./references/ingestion-remediate.md)
5. **Validate pipeline health** by monitoring runtime logs on source and destination nodes

### Workflow 3: Resolve Capacity Throttling

1. **Open the Fabric Capacity Metrics app** — filter to your capacity and workspace
2. **Check Eventhouse UpTime CU consumption** — identify if a single Eventhouse dominates
3. **Run capacity diagnostics** using [diagnose-capacity.kql](./scripts/diagnose-capacity.kql)
4. **Evaluate sizing options**: Always-On minimum consumption, cache policy adjustments, or SKU upgrade
5. **Apply recommendations** from [capacity-and-sizing.md](./references/capacity-and-sizing.md)

## remediate Quick Reference

| Symptom                     | First Check                                    | Script                                                        |
| --------------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| Slow queries                | Workspace Monitoring → EH Queries tab         | [diagnose-slow-queries.kql](./scripts/diagnose-slow-queries.kql) |
| Query throttling (HTTP 430) | Capacity Metrics app → CU utilization         | [diagnose-capacity.kql](./scripts/diagnose-capacity.kql)         |
| Ingestion failures          | Eventstream → Runtime logs tab                | [diagnose-ingestion.kql](./scripts/diagnose-ingestion.kql)       |
| High ingestion latency      | Eventstream → Data insights → WatermarkDelay | [diagnose-ingestion.kql](./scripts/diagnose-ingestion.kql)       |
| Materialized view stale     | `.show materialized-views` command           | [diagnose-slow-queries.kql](./scripts/diagnose-slow-queries.kql) |
| Cold storage scans          | Cache policy vs query time range               | [diagnose-capacity.kql](./scripts/diagnose-capacity.kql)         |
| Eventhouse wake-up latency  | Always-On setting disabled                     | [capacity-and-sizing.md](./references/capacity-and-sizing.md)    |
| Eventstream backlog growing | Throughput setting mismatch                    | [ingestion-remediate.md](./references/ingestion-remediate.md)    |

## References

- [KQL Query Optimization Guide](./references/kql-optimization.md) — Best practices for writing performant KQL
- [Ingestion remediate Guide](./references/ingestion-remediate.md) — Eventstream, batching, and streaming diagnostics
- [Capacity and Sizing Guide](./references/capacity-and-sizing.md) — Always-On, cache policies, CU consumption
- [Workspace Monitoring Setup](./references/workspace-monitoring.md) — Enabling and using monitoring tables and dashboards
- [KQL Best Practices (Microsoft)](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/best-practices)
- [Eventhouse Compute Observability](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/eventhouse-compute-observability)
- [Eventstream Monitoring](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/event-streams/monitor)
- [Fabric Capacity Metrics App](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app)
