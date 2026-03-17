---
name: fabric-dataflows-perf-remediation
description: Diagnose and resolve Microsoft Fabric Dataflow Gen2 performance issues including slow refresh times, Fast Copy optimization, query folding failures, staging bottlenecks, gateway latency, incremental refresh tuning, capacity throttling, and data destination write performance. Use when troubleshooting dataflow refresh failures, optimizing Dataflow Gen2 execution time, debugging Power Query mashup engine performance, resolving staging Lakehouse or Warehouse compute issues, configuring Fast Copy connectors, fixing insufficient permissions errors, monitoring dataflow refresh history, or automating dataflow health checks via REST API and PowerShell.
license: Complete terms in LICENSE.txt
---

# Dataflows Gen2 Performance Troubleshooting

Systematic diagnostic workflows for identifying and resolving performance issues in Microsoft Fabric Dataflow Gen2 workloads covering data movement, transformation execution, staging configuration, and destination write optimization.

## When to Use This Skill

- Dataflow Gen2 refresh takes longer than expected
- Fast Copy is not being utilized or is failing
- Query folding indicators show red or yellow steps
- Staging-to-destination data movement is a bottleneck
- Gateway-connected dataflows have high latency
- Incremental refresh is slower than full refresh
- Capacity throttling affects dataflow execution
- Refresh failures with permission or connector errors
- Need to automate dataflow monitoring and health checks
- Migrating from Dataflow Gen1 and seeing performance regressions

## Prerequisites

- Microsoft Fabric workspace with Data Factory enabled
- Contributor or higher role on the workspace
- PowerShell 7+ with Az.Accounts module for automation scripts
- Access to Fabric Monitoring Hub for refresh history analysis
- Fabric Capacity Metrics app access for CU consumption review

---

## Quick Diagnosis: Symptom-to-Solution Map

| Symptom | Likely Cause | Jump To |
|---------|-------------|---------|
| Refresh takes 2x+ longer than Gen1 | Delta Parquet output overhead or staging misconfiguration | [Consideration 5 in Performance Guide](./references/performance-optimization-guide.md#gen1-vs-gen2-runtime) |
| Fast Copy not activating | Unsupported connector or non-foldable transforms | [Fast Copy Diagnostics](#fast-copy-diagnostics) |
| "Insufficient permissions for staging artifacts" | Creator token expired (90+ days) | [Common Errors](#common-refresh-errors) |
| Slow design-time previews | Large dataset loaded in editor | [Design-Time Optimization](#design-time-optimization) |
| Staging-to-Lakehouse write is slow | Extra data hop through staging Warehouse | [Staging Strategy](#staging-strategy-decision-tree) |
| Gateway dataflows are slow | All transforms running on gateway host | [Gateway Optimization](#gateway-performance) |
| Incremental refresh slower than full | Too many small buckets creating overhead | [Incremental Refresh Tuning](#incremental-refresh-tuning) |
| HTTP 430 / capacity throttled | Concurrent Spark jobs exhausting CUs | [Capacity Management](#capacity-and-throttling) |

---

## Diagnostic Workflow

### Step 1: Check Refresh History

1. Open the Fabric workspace and locate the dataflow
2. Select the ellipsis (...) > **Recent runs**
3. Review the refresh history for status, duration, and type
4. Select a specific refresh **Start time** to drill into details
5. Examine the **Tables** section for per-entity timing
6. Examine the **Activities** section for destination write timing
7. Download **detailed logs** (bottom-left button) for deep analysis
8. Download **CSV** of refresh runs for trend analysis

Key metrics to capture: total duration, per-table duration, bytes read/written, rows read/written, engine type (Mashup vs CopyActivity vs SQL DW).

### Step 2: Identify the Bottleneck Component

Dataflow Gen2 has three performance-critical components:

```
[Data Source] --> [Dataflow Engine] --> [Data Destination]
     |                  |                      |
  Connectors    Mashup / Fast Copy /      Lakehouse /
  + Gateway     SQL DW Compute            Warehouse /
                                          SQL Database
```

- **Data Source**: Connector speed, network latency, gateway throughput
- **Dataflow Engine**: Query folding, staging, Fast Copy, Mashup engine
- **Data Destination**: Write performance, Delta Parquet conversion

### Step 3: Apply Targeted Optimization

Based on the bottleneck identified, follow the relevant section below.

---

## Fast Copy Diagnostics

Fast Copy provides up to 9x faster ingestion for supported scenarios.

### Supported Connectors

ADLS Gen2, Azure Blob Storage, Azure SQL DB, Lakehouse, PostgreSQL, On-premises SQL Server, Warehouse, Oracle, Snowflake, SQL Database in Fabric.

### Fast Copy Indicators

| Indicator | Meaning | Action |
|-----------|---------|--------|
| Green | Step supported by Fast Copy | No action needed |
| Yellow | Some steps may support Fast Copy | Split query at boundary |
| Red | Step NOT supported by Fast Copy | Move to referenced query |

### When Fast Copy Is Disabled

- Transformations beyond: select columns, change types, rename, remove columns (for file sources)
- Non-supported connector in use
- "Require Fast Copy" set on incompatible query (causes failure)
- Destination is not Lakehouse (stage first, then reference)

### Query Splitting Pattern for Fast Copy

1. Remove any red-indicator steps and the destination from the original query
2. Verify remaining steps show green indicators
3. Right-click the query > **Enable staging**
4. Right-click again > **Reference** to create a new query
5. Add back transformations and destination to the referenced query
6. Publish and refresh — first query uses Fast Copy, second uses SQL DW compute

See [Performance Optimization Guide](./references/performance-optimization-guide.md#fast-copy-deep-dive) for detailed walkthrough.

---

## Staging Strategy Decision Tree

```
Is destination a Warehouse?
├── YES → Staging REQUIRED (enabled by default)
│         Write goes directly via SQL DW compute
│         This is the optimal path for Warehouse destinations
└── NO → Is destination a Lakehouse?
    ├── YES with staging enabled → Data moves:
    │   Source → Staging LH → Staging WH → Lakehouse
    │   ⚠ CONSIDER: Disable staging to avoid extra hop
    │   OR: Switch destination to Warehouse instead
    └── YES with staging disabled → Data writes directly
        Source → Lakehouse (via Mashup engine)
        ✓ Fewer hops, but no SQL DW compute for transforms
```

**Key Decision**: If your transforms fold to the source, disable staging for Lakehouse destinations. If transforms are complex (joins, aggregations), either enable staging or switch to Warehouse destination.

---

## Design-Time Optimization

When working with large datasets in the dataflow editor:

1. **Use parameters for date filtering**: Create a `DesignDateFilter` parameter to limit preview data during authoring, then adjust to full range before publish
2. **Switch to Schema view**: Select **Schema view** in the editor toolbar to see structure without loading data
3. **Limit preview rows**: Keep preview data small during development

---

## Gateway Performance

When using on-premises data gateway:

1. **Split dataflows**: Separate data movement (gateway → cloud) from transformations
2. **First dataflow**: Use Fast Copy for high-throughput transfer from on-premises to Lakehouse/Warehouse staging
3. **Second dataflow**: Apply transformations using cloud compute on the staged data
4. **Gateway version**: Must be 3000.214.2+ for Fast Copy support; keep within last 6 supported versions
5. **Detailed logs**: Not yet supported for on-premises gateway refreshes (supported for cloud/VNet gateways)

---

## Incremental Refresh Tuning

If incremental refresh is slower than full refresh:

1. **Increase bucket size**: Reduce total bucket count to lower partition management overhead
2. **Evaluate data volume**: For small datasets, full refresh may outperform incremental
3. **Concurrency control**: Adjust max concurrent requests in dataflow settings if source can't handle defaults
4. **Monitor bucket efficiency**: Check if most buckets process zero rows (indicates over-partitioning)

---

## Capacity and Throttling

### Dataflow Gen2 Compute Meters

| Engine | When Used | Billing Basis |
|--------|-----------|---------------|
| Standard Compute (Mashup) | Staging disabled or non-foldable queries | Query evaluation time |
| High Scale Compute (SQL DW) | Staging enabled | Lakehouse + Warehouse duration |
| Fast Copy | Supported connectors with Fast Copy enabled | Copy job duration |

All operations are **background operations** smoothed over 24 hours.

### CU Consumption Formula (Standard Compute)

```
If QueryDuration < 600s:
  CU_seconds = QueryDuration × 12
Else:
  CU_seconds = (QueryDuration - 600) × 1.5 + 600 × 12
```

### Reducing Capacity Impact

1. Avoid inefficient Power Query logic (expensive merges and sorts)
2. Maximize query folding to push work to source systems
3. Disable staging for small data volumes or simple transforms
4. Don't refresh more frequently than source data updates
5. Use data destinations instead of dataflow connectors for consumption

---

## Common Refresh Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| "Insufficient permissions for staging artifacts" | Creator inactive 90+ days or left org | Have creator log in to Fabric; if gone, open support ticket |
| "Expression.Error: import matches no exports" | Unsupported connector in Premium workspace | Check connector compatibility list |
| "Gateway version not supported" | On-premises gateway out of support | Update to latest gateway version |
| "Staging lakehouse couldn't be found" | CI/CD branch workspace missing staging | Create a new Dataflow Gen2 in workspace to trigger staging creation |
| Validation failure on save | Query schema can't be determined in 10 min | Simplify query or check source connectivity |

---

## Modern Evaluator (Preview)

The Modern Evaluator engine can provide significant performance improvements:

- **Large data volumes**: Shorter processing time, reduced memory usage
- **Complex transformations**: Improved execution plans for joins across large tables
- **Frequent schedules**: Cumulative time savings across multiple daily runs

Enable via dataflow settings. Monitor results after enabling — some connectors may not yet be fully optimized.

---

## Automation and Monitoring

Run the [Dataflow Health Check Script](./scripts/Get-DataflowHealthReport.ps1) to programmatically audit dataflow configurations and recent refresh performance across a workspace.

Run the [Dataflow Refresh Monitor Script](./scripts/Watch-DataflowRefresh.ps1) to poll and track active refresh status in real-time.

See [REST API Reference](./references/dataflow-rest-api-reference.md) for complete API documentation covering CRUD operations, scheduling, refresh triggering, and monitoring.

See [Performance Optimization Guide](./references/performance-optimization-guide.md) for deep-dive scenarios including Fast Copy benchmarks, staging architecture patterns, and query folding analysis techniques.

---

## References

- [Performance Optimization Guide](./references/performance-optimization-guide.md) — Deep-dive optimization scenarios
- [Dataflow REST API Reference](./references/dataflow-rest-api-reference.md) — API operations for automation
- [Get-DataflowHealthReport.ps1](./scripts/Get-DataflowHealthReport.ps1) — Workspace health audit
- [Watch-DataflowRefresh.ps1](./scripts/Watch-DataflowRefresh.ps1) — Real-time refresh monitor
- [Microsoft Learn: Best Practices for Dataflow Gen2 Performance](https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-performance-best-practices)
- [Microsoft Learn: Fast Copy in Dataflow Gen2](https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-fast-copy)
- [Microsoft Learn: View Refresh History and Monitor Dataflows](https://learn.microsoft.com/en-us/fabric/data-factory/dataflows-gen2-monitor)
- [Microsoft Learn: Dataflow Gen2 Pricing](https://learn.microsoft.com/en-us/fabric/data-factory/pricing-dataflows-gen2)
