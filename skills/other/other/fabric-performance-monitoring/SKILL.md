---
name: fabric-performance-monitoring
description: Monitor and optimize Microsoft Fabric capacity, Spark compute, and workload performance. Use when asked to check capacity utilization, diagnose throttling (HTTP 430), monitor Spark VCore consumption, analyze CU usage, review Monitoring Hub jobs, query Fabric REST APIs for capacity health, generate performance reports, tune Spark resource profiles, investigate concurrency limits, or optimize Fabric SKU sizing. Supports PowerShell, T-SQL, and REST API workflows.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric Performance Monitoring

Toolkit for monitoring, diagnosing, and optimizing Microsoft Fabric capacity and workload performance across Spark, Data Warehouse, Lakehouse, and Pipeline workloads.

## When to Use This Skill

- Checking Fabric capacity utilization or CU consumption
- Diagnosing throttling errors (HTTP 430 / TooManyRequestsForCapacity)
- Monitoring Spark VCore usage and concurrency limits
- Querying Fabric REST APIs for capacity and workspace health
- Generating capacity performance reports
- Tuning Spark resource profiles (readHeavy, writeHeavy, balanced)
- Investigating job failures in the Monitoring Hub
- Analyzing autoscale billing vs capacity-based billing
- Reviewing background vs interactive operation patterns
- Planning capacity SKU sizing or rightsizing

## Prerequisites

- PowerShell 7+ with Az.Fabric module installed
- Microsoft Entra ID app registration with Fabric API permissions
- Fabric Capacity Admin or Workspace Admin role
- Fabric Capacity Metrics app installed (for visual monitoring)

## Core Concepts

### Capacity Units and Spark VCores

One Capacity Unit (CU) equals two Apache Spark VCores. Fabric capacity is shared across all workspaces assigned to it, and Spark VCores are shared among notebooks, Spark job definitions, and lakehouses within those workspaces.

### Operation Types

Fabric classifies operations as interactive (on-demand, like DAX queries) or background (scheduled, like refreshes and Spark jobs). Background operations are smoothed over a 24-hour period. All Spark operations are background operations.

### Throttling Behavior

When capacity is fully utilized, new Spark jobs receive HTTP 430 with `TooManyRequestsForCapacity`. With queueing enabled, pipeline-triggered and scheduled jobs enter a FIFO queue and retry automatically when capacity becomes available.

### Capacity SKU Limits

| SKU  | Spark VCores | Queue Limit |
|------|-------------|-------------|
| F2   | 4           | 4           |
| F4   | 8           | 4           |
| F8   | 16          | 8           |
| F16  | 32          | 16          |
| F32  | 64          | 32          |
| F64  | 128         | 64          |
| F128 | 256         | 128         |
| F256 | 512         | 256         |
| F512 | 1024        | 512         |

### Spark Resource Profiles

Fabric supports predefined Spark resource profiles for workload optimization. New workspaces default to `writeHeavy`. Available profiles: `readHeavy`, `writeHeavy`, `balanced`. When `writeHeavy` is used, VOrder is disabled by default and must be manually enabled.

## Step-by-Step Workflows

### Workflow 1: Capacity Health Check

Run the [capacity health check script](./scripts/Get-FabricCapacityHealth.ps1) to retrieve current capacity status, SKU details, and state.

```powershell
./scripts/Get-FabricCapacityHealth.ps1 -SubscriptionId "<sub-id>" -ResourceGroupName "<rg>" -CapacityName "<name>"
```

See [capacity-health-reference.md](./references/capacity-health-reference.md) for detailed API response schemas and interpretation guidance.

### Workflow 2: Spark Concurrency Analysis

Run the [Spark concurrency analyzer](./scripts/Get-FabricSparkConcurrency.ps1) to check active sessions, queued jobs, and throttling status.

```powershell
./scripts/Get-FabricSparkConcurrency.ps1 -WorkspaceId "<workspace-id>"
```

### Workflow 3: Monitoring Hub Job Audit

Run the [job audit script](./scripts/Get-FabricJobHistory.ps1) to retrieve recent job executions, durations, and failure details.

```powershell
./scripts/Get-FabricJobHistory.ps1 -WorkspaceId "<workspace-id>" -HoursBack 24
```

### Workflow 4: Generate Performance Report

Use the [performance report template](./templates/performance-report.sql) to query the SQL analytics endpoint for Lakehouse operation metrics, then generate a summary with the [report generator](./scripts/New-FabricPerformanceReport.ps1).

### Workflow 5: Autoscale vs Capacity Cost Analysis

See [cost-analysis-reference.md](./references/cost-analysis-reference.md) for guidance on comparing autoscale billing vs capacity-based models using Azure Cost Management.

## remediate

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| HTTP 430 errors | Capacity fully utilized | Scale SKU, cancel idle sessions, enable queueing |
| Jobs stuck in queue | All VCores consumed | Check Monitoring Hub, stop idle notebooks |
| Slow Spark startup | Using custom pool with cold start | Switch to starter pool for quick sessions |
| High CU consumption | Inefficient queries or unoptimized code | Review Capacity Metrics app, optimize DAX/Spark |
| Autoscale charges unexpected | Spark jobs billed independently | Check Azure Cost Analysis with Autoscale meter |
| VOrder disabled | writeHeavy profile active | Manually enable VOrder if read performance needed |

## References

- [Capacity Health Reference](./references/capacity-health-reference.md) - REST API schemas and interpretation
- [Cost Analysis Reference](./references/cost-analysis-reference.md) - Autoscale vs capacity billing comparison
- [Fabric Capacity Metrics App](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app)
- [Monitor Spark Capacity Consumption](https://learn.microsoft.com/en-us/fabric/data-engineering/monitor-spark-capacity-consumption)
- [Fabric REST API Documentation](https://learn.microsoft.com/en-us/rest/api/microsoftfabric/)
- [Concurrency Limits and Queueing](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-job-concurrency-and-queueing)
