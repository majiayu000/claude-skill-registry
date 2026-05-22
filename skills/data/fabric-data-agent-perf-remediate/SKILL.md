---
name: fabric-data-agent-perf-remediate
description: >-
  Diagnose and resolve Microsoft Fabric Data Agent performance issues including slow query
  generation, capacity throttling (HTTP 430), Spark session startup delays, KQL/SQL/DAX query
  timeouts, data source misconfiguration, example query validation failures, resource profile
  tuning, VOrder optimization, autotune settings, and Lakehouse table maintenance. Use when
  asked to troubleshoot Fabric Data Agent response times, fix agent query accuracy, debug
  Operations Agent playbook performance, resolve capacity SKU limits, optimize Spark compute
  for agents, or diagnose Data Agent data source connection issues.
license: Complete terms in LICENSE.txt
---
# Fabric Data Agent Performance remediate

Systematic toolkit for diagnosing and resolving performance issues in Microsoft Fabric Data
Agents, Operations Agents, and their underlying Spark compute and data source infrastructure.

## When to Use This Skill

- Data Agent responses are slow or timing out
- Agent-generated SQL/KQL/DAX queries return errors or produce incorrect results
- Spark session startup takes longer than expected (>10 seconds)
- Capacity throttling errors (HTTP 430) during agent workloads
- Operations Agent playbooks fail to execute or trigger actions
- Data source connections are unreliable or stale
- Example queries fail validation against schema
- Resource profiles need tuning for agent-specific workloads
- Table maintenance (VOrder, bin-compaction, vacuum) is overdue
- Autoscale Billing configuration needs optimization

## Prerequisites

- **Access**: Fabric workspace Contributor or Admin role
- **Tools**: PowerShell 7+, Fabric REST API access (Microsoft Entra token)
- **Endpoints**: `https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items`
- **Monitoring**: Access to Fabric Admin Portal and Azure Cost Analysis
- **Optional**: Azure subscription admin for SKU resizing and Autoscale Billing

## Diagnostic Decision Tree

```
Agent performance issue reported
├── Slow response times?
│   ├── First query after idle? → Spark session startup (see Workflow 1)
│   ├── All queries slow? → Resource profile mismatch (see Workflow 2)
│   └── Intermittent slowness? → Capacity throttling (see Workflow 3)
├── Incorrect query results?
│   ├── Wrong tables/columns? → Data source instructions (see Workflow 4)
│   ├── SQL syntax errors? → Example query validation (see Workflow 5)
│   └── Stale data? → Lakehouse table maintenance (see Workflow 6)
├── Agent not responding?
│   ├── HTTP 430 errors? → Concurrency limits (see Workflow 3)
│   ├── Connection failures? → Data source config (see Workflow 4)
│   └── Operations Agent stuck? → Playbook/action config (see Workflow 7)
└── Cost concerns?
    ├── Unexpected charges? → Autoscale Billing audit (see Workflow 8)
    └── Over-provisioned? → SKU right-sizing (see Workflow 8)
```

## Step-by-Step Workflows

### Workflow 1: Spark Session Startup Delays

**Symptoms**: First query takes 2-5 minutes, subsequent queries are fast.

| Scenario                       | Expected Startup       |
| ------------------------------ | ---------------------- |
| Default, no custom libraries   | 5-10 seconds           |
| Default + library dependencies | 35 seconds - 5 minutes |
| High regional traffic          | 2-5 minutes            |
| Private Links / Managed VNet   | 2-5 minutes            |
| Network security + libraries   | 2.5-10 minutes         |

**Resolution steps**: See [workflow-spark-startup.md](./references/workflow-spark-startup.md)

### Workflow 2: Resource Profile Optimization

**Symptoms**: Consistently slow reads or writes across all agent queries.

| Profile               | Use Case                           | VOrder       | OptimizeWrite       |
| --------------------- | ---------------------------------- | ------------ | ------------------- |
| `writeHeavy`        | High-frequency ingestion (default) | Disabled     | Disabled            |
| `readHeavyForPBI`   | Power BI dashboard queries         | Enabled      | Enabled (1GB bin)   |
| `readHeavyForSpark` | Interactive Spark analytics        | Disabled     | Enabled (128MB bin) |
| `custom`            | User-defined workload tuning       | Configurable | Configurable        |

**Resolution steps**: See [workflow-resource-profiles.md](./references/workflow-resource-profiles.md)

### Workflow 3: Capacity Throttling (HTTP 430)

**Symptoms**: `TooManyRequestsForCapacity` errors, jobs queued or rejected.

| SKU  | Spark VCores | Queue Limit |
| ---- | ------------ | ----------- |
| F2   | 4            | 4           |
| F8   | 16           | 8           |
| F64  | 128          | 64          |
| F128 | 256          | 128         |
| F256 | 512          | 256         |

**Formula**: 1 Capacity Unit = 2 Spark VCores

**Resolution steps**: See [workflow-capacity-throttling.md](./references/workflow-capacity-throttling.md)

### Workflow 4: Data Source Configuration Issues

**Symptoms**: Agent queries wrong tables, returns irrelevant results, or fails to connect.

Data Agents use three configuration layers that all affect query quality:

1. **Agent Instructions** — Global routing rules (which data source for which topic)
2. **Data Source Instructions** — Schema context, table descriptions, column details
3. **Example Queries** — Few-shot SQL/KQL/DAX examples for query generation

**Resolution steps**: See [workflow-data-source-config.md](./references/workflow-data-source-config.md)

### Workflow 5: Example Query Validation

**Symptoms**: Agent ignores example queries, generates incorrect SQL/KQL syntax.

**Key rule**: The Fabric Data Agent only uses queries that contain valid SQL/KQL syntax AND
match the schema of the selected tables. Queries that fail validation are silently ignored.

**Resolution steps**: See [workflow-example-queries.md](./references/workflow-example-queries.md)

### Workflow 6: Lakehouse Table Maintenance

**Symptoms**: Queries over Delta tables are slow, small file problem, stale statistics.

Three maintenance operations available via REST API:

| Operation      | Purpose                                        |
| -------------- | ---------------------------------------------- |
| Bin-compaction | Consolidate small files into optimal sizes     |
| V-Order        | Optimize Parquet layout for read performance   |
| Vacuum         | Remove unreferenced files older than retention |

**Resolution steps**: See [workflow-table-maintenance.md](./references/workflow-table-maintenance.md)

### Workflow 7: Operations Agent Debugging

**Symptoms**: Operations Agent not triggering actions, playbook failures.

Operations Agent definition requires: goals, instructions, at least one KustoDatabase data
source, at least one PowerAutomateAction, and `shouldRun: true`.

**Resolution steps**: See [workflow-operations-agent.md](./references/workflow-operations-agent.md)

### Workflow 8: Autoscale Billing and SKU Right-Sizing

**Symptoms**: Unexpected costs, capacity contention between Spark and other workloads.

**Resolution steps**: See [workflow-autoscale-billing.md](./references/workflow-autoscale-billing.md)

## Available Scripts

| Script                                                                  | Purpose                                                     |
| ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| [Get-FabricAgentDiagnostics.ps1](./scripts/Get-FabricAgentDiagnostics.ps1) | Collect agent config, capacity state, and Spark metrics     |
| [Test-ExampleQueries.ps1](./scripts/Test-ExampleQueries.ps1)               | Validate example queries against data source schema         |
| [Invoke-TableMaintenance.ps1](./scripts/Invoke-TableMaintenance.ps1)       | Run bin-compaction, V-Order, and vacuum on Lakehouse tables |

## remediate Quick Reference

| Error             | Likely Cause                     | First Action                          |
| ----------------- | -------------------------------- | ------------------------------------- |
| HTTP 430          | Capacity VCore limit             | Check Monitoring Hub for active jobs  |
| Query timeout     | Resource profile mismatch        | Switch to `readHeavyForSpark`       |
| Wrong columns     | Missing data source instructions | Update schema descriptions            |
| Ignored examples  | Invalid SQL/KQL syntax           | Validate with Test-ExampleQueries.ps1 |
| 2-5 min startup   | Private Links or high traffic    | Check workspace networking config     |
| Stale results     | Missing table maintenance        | Run bin-compaction + V-Order          |
| Agent not running | `shouldRun: false`             | Check Operations Agent definition     |
| Autotune disabled | Runtime > 1.2 or HC mode         | Verify Fabric Runtime version         |

## References

- [Spark Startup Workflow](./references/workflow-spark-startup.md)
- [Resource Profile Workflow](./references/workflow-resource-profiles.md)
- [Capacity Throttling Workflow](./references/workflow-capacity-throttling.md)
- [Data Source Config Workflow](./references/workflow-data-source-config.md)
- [Example Query Workflow](./references/workflow-example-queries.md)
- [Table Maintenance Workflow](./references/workflow-table-maintenance.md)
- [Operations Agent Workflow](./references/workflow-operations-agent.md)
- [Autoscale Billing Workflow](./references/workflow-autoscale-billing.md)
