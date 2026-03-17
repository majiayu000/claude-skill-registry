---
name: fabric-data-factory-perf-remediate
description: Diagnose and resolve Microsoft Fabric Data Factory pipeline performance issues. Use when pipelines are slow, copy activities timeout, dataflows stall, activities are stuck, throughput is low, capacity is throttled, or jobs queue indefinitely. Covers copy activity tuning (parallelCopies, DIU, ITO, partitioning), pipeline monitoring via Monitoring Hub and workspace monitoring, Spark job queueing, capacity SKU limits, error code resolution, and dataflow optimization. Keywords include Fabric pipeline slow, copy activity performance, Data Factory throttling, pipeline timeout, activity stuck, TooManyRequestsForCapacity, HTTP 430, pipeline troubleshoot, dataflow performance, copy parallelism, intelligent throughput optimization.
license: Complete terms in LICENSE.txt
---
# Microsoft Fabric Data Factory Performance remediate

Systematic approach to diagnosing and resolving performance issues in Microsoft Fabric Data Factory pipelines, copy activities, and dataflows.

## When to Use This Skill

- Pipeline execution takes longer than expected
- Copy activities are slow or appear stuck
- Activities show "Not Started" status for extended periods
- Capacity throttling errors (HTTP 430, TooManyRequestsForCapacity)
- Throughput is lower than expected for copy operations
- Dataflow Gen2 refresh is slow or timing out
- Pipeline monitoring shows performance degradation over time
- Need to optimize parallelism, DIU, or partitioning settings

## Prerequisites

- Access to Microsoft Fabric workspace with Contributor or higher role
- Familiarity with the Fabric Monitoring Hub
- Understanding of Fabric capacity SKUs and their limits
- PowerShell 7+ for running diagnostic scripts

## Diagnostic Workflow

### Step 1: Identify the Bottleneck Category

Determine which category your issue falls into:

| Category            | Symptoms                                    | Start Here                                                                                |
| ------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Copy Activity Slow  | Low throughput, long transfer duration      | [copy-activity-tuning.md](./references/copy-activity-tuning.md)                              |
| Pipeline Stuck      | Activity shows In Progress with no movement | [pipeline-stuck-resolution.md](./references/pipeline-stuck-resolution.md)                    |
| Capacity Throttling | HTTP 430 errors, jobs queued                | [capacity-throttling-guide.md](./references/capacity-throttling-guide.md)                    |
| Dataflow Slow       | Dataflow Gen2 refresh takes too long        | [dataflow-optimization.md](./references/dataflow-optimization.md)                            |
| Spark Job Queue     | Jobs stuck in "Not Started" status          | [capacity-throttling-guide.md](./references/capacity-throttling-guide.md#spark-job-queueing) |

### Step 2: Collect Diagnostics

Run the [diagnostic script](./scripts/Get-FabricPipelineDiagnostics.ps1) to gather baseline metrics:

```powershell
./scripts/Get-FabricPipelineDiagnostics.ps1 -WorkspaceId "<guid>" -PipelineName "MyPipeline"
```

Or manually collect from the Monitoring Hub:

1. Open Fabric portal and navigate to Monitoring Hub
2. Filter by pipeline name and time range
3. Select the run details (glasses icon) for the slow run
4. Capture the Duration Breakdown for copy activities
5. Note the queue time, transfer time, and pre/post-copy script duration

### Step 3: Apply Targeted Fixes

Based on the bottleneck category, apply the appropriate optimization from the reference guides.

## Quick Fixes for Common Issues

### Copy Activity Running Slowly

1. Set **Intelligent Throughput Optimization** to `Maximum` (or custom 4-256)
2. Configure **Degree of Copy Parallelism** based on source type
3. Enable **Partition Option** for SQL sources (Dynamic Range or Physical)
4. Pre-calculate partition upper/lower bounds to avoid overhead
5. Enable **Staging** when sink is Fabric Warehouse

### Pipeline Activity Stuck

1. Cancel the stuck activity and retry
2. Check source/sink connectivity and credentials
3. Verify Fabric capacity is not in throttled state
4. Review if payload exceeds 896 KB limit
5. Check for connection timeout or network interruption

### Capacity Throttling (HTTP 430)

1. Check current Spark concurrency against SKU limits
2. Cancel unnecessary active Spark jobs via Monitoring Hub
3. Consider upgrading to a larger capacity SKU
4. Distribute pipeline trigger times to avoid burst load
5. Use job queueing for non-interactive Spark workloads

### Dataflow Gen2 Performance

1. Reduce data volume with query folding and filters
2. Avoid unnecessary data type conversions
3. Minimize the number of transformation steps
4. Use staging for large datasets
5. Check for connector-specific throttling

## Capacity SKU Quick Reference

| SKU   | Max Spark Cores | Queue Limit    | Equivalent Power BI |
| ----- | --------------- | -------------- | ------------------- |
| F2    | Limited         | 4              | -                   |
| F4    | Limited         | 4              | -                   |
| F8    | Limited         | 8              | -                   |
| F16   | Limited         | 16             | -                   |
| F32   | Limited         | 32             | -                   |
| F64   | Standard        | 64             | P1                  |
| F128  | Standard        | 128            | P2                  |
| F256  | Standard        | 256            | P3                  |
| F512  | Standard        | 512            | P4                  |
| F1024 | Large           | 1024           | -                   |
| F2048 | Large           | 2048           | -                   |
| Trial | P1 equiv        | N/A (no queue) | P1                  |

## Copy Activity Performance Settings Reference

| Setting                             | Property                      | Range                                                              | Recommendation                                       |
| ----------------------------------- | ----------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------- |
| Intelligent Throughput Optimization | `dataIntegrationUnits`      | Auto, Standard (64), Balanced (128), Maximum (256), Custom (4-256) | Start with Auto, increase for large datasets         |
| Degree of Copy Parallelism          | `parallelCopies`            | 1-256                                                              | Auto for most; limit to 32 for Fabric Warehouse sink |
| Partition Option                    | Source settings               | None, Physical, Dynamic Range                                      | Use Dynamic Range for large SQL tables               |
| Enable Staging                      | `enableStaging`             | true/false                                                         | Required for Fabric Warehouse sink                   |
| Source Retry Count                  | `sourceRetryCount`          | Integer                                                            | Set 2-3 for transient failures                       |
| Fault Tolerance                     | `enableSkipIncompatibleRow` | true/false                                                         | Enable for non-critical loads                        |

## Error Code Quick Reference

| Error                      | Meaning                          | Action                                |
| -------------------------- | -------------------------------- | ------------------------------------- |
| HTTP 430                   | Capacity compute limit reached   | Reduce concurrent jobs or upgrade SKU |
| Payload too large          | Activity config exceeds 896 KB   | Reduce parameter sizes                |
| TooManyRequestsForCapacity | Spark compute or API rate limit  | Cancel active jobs or wait            |
| Connection timeout         | Source/sink unreachable          | Check network, credentials, firewall  |
| Deflate64 unsupported      | Compression format not supported | Re-compress with deflate algorithm    |

## Monitoring Setup

Enable workspace monitoring for ongoing performance analysis:

1. Go to **Workspace Settings** > **Monitoring**
2. Add a Monitoring Eventhouse and enable **Log workspace activity**
3. Query the `ItemJobEventLogs` table with KQL for pipeline-level insights

Example KQL query for failure trends:

```kql
ItemJobEventLogs
| where ItemKind == "Pipeline"
| summarize count() by JobStatus
```

See [workspace-monitoring-setup.md](./references/workspace-monitoring-setup.md) for detailed configuration.

## References

- [Copy Activity Tuning Guide](./references/copy-activity-tuning.md)
- [Pipeline Stuck Resolution](./references/pipeline-stuck-resolution.md)
- [Capacity Throttling Guide](./references/capacity-throttling-guide.md)
- [Dataflow Optimization](./references/dataflow-optimization.md)
- [Workspace Monitoring Setup](./references/workspace-monitoring-setup.md)
- [remediate Runbook Template](./templates/remediate-runbook.md)

## External Resources

- [Fabric Data Factory Pipeline Troubleshoot Guide](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-troubleshoot-guide)
- [Copy Activity Performance and Scalability Guide](https://learn.microsoft.com/en-us/fabric/data-factory/copy-activity-performance-and-scalability-guide)
- [Copy Activity Performance with SQL Databases](https://learn.microsoft.com/en-us/fabric/data-factory/copy-performance-sql-databases)
- [Monitor Pipeline Runs](https://learn.microsoft.com/en-us/fabric/data-factory/monitor-pipeline-runs)
