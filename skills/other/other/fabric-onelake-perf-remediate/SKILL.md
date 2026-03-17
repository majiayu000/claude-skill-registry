---
name: fabric-onelake-perf-remediate
description: Diagnose and resolve Microsoft Fabric OneLake performance issues including slow queries, cold cache latency, small file problems, Delta table fragmentation, V-Order optimization, Spark throttling, capacity SKU sizing, and cross-region data access. Use when remediate OneLake read/write performance, lakehouse query slowness, Direct Lake fallback, table maintenance failures, Spark concurrency limits, warehouse cold starts, or optimizing Delta parquet file layouts. Supports PowerShell, T-SQL, and Spark SQL diagnostic workflows.
license: Complete terms in LICENSE.txt
---
# OneLake Performance remediate

Systematic diagnostic and remediation toolkit for Microsoft Fabric OneLake performance issues. Covers the full stack from capacity-level throttling down to individual Delta table file layout problems.

## When to Use This Skill

- OneLake read or write operations are slow or timing out
- Lakehouse or warehouse queries have unexpectedly high latency
- Spark jobs are being throttled with HTTP 430 errors
- Delta tables have accumulated many small files (small file problem)
- Direct Lake semantic models are falling back to DirectQuery
- Cold cache performance is significantly slower than warm cache
- Cross-region data access is adding network latency
- V-Order is not applied or needs to be enabled/disabled
- Table maintenance (OPTIMIZE, VACUUM) is failing or not improving performance
- Capacity utilization is high and jobs are queuing

## Prerequisites

- Microsoft Fabric workspace with Contributor or higher role
- Access to the Monitoring Hub in the Fabric portal
- PowerShell 7+ with Az.Fabric module (for automation scripts)
- Familiarity with Spark SQL or T-SQL for diagnostic queries

## Diagnostic Decision Tree

Follow this sequence to isolate the root cause:

```
1. Is the issue capacity-level? → Check Spark VCore utilization and queue depth
2. Is the issue cold cache? → Check data_scanned_remote_storage_mb
3. Is the issue file layout? → Check small file count and V-Order status
4. Is the issue cross-region? → Verify data and capacity are co-located
5. Is the issue query design? → Check string column widths, partition pruning
```

## Step-by-Step Workflows

### Workflow 1: Diagnose Capacity Throttling

When Spark jobs fail with HTTP 430 (TooManyRequestsForCapacity):

1. Open the **Monitoring Hub** in the Fabric portal
2. Check active Spark sessions against your SKU's VCore limit (1 CU = 2 Spark VCores)
3. Review the queue depth against your SKU's queue limit (see [capacity-sku-reference.md](./references/capacity-sku-reference.md))
4. Cancel unnecessary jobs or scale up the capacity SKU
5. For burst workloads, use the [spark-capacity-check.ps1](./scripts/spark-capacity-check.ps1) script to monitor utilization

### Workflow 2: Resolve Cold Cache Latency

When first query execution is significantly slower than subsequent runs:

1. Query the `queryinsights.exec_requests_history` view
2. Check the `data_scanned_remote_storage_mb` column — non-zero indicates cold start
3. Do NOT judge performance on first execution; measure subsequent runs
4. For pre-warming strategies and diagnostic queries, see [cold-cache-diagnostics.md](./references/cold-cache-diagnostics.md)

### Workflow 3: Fix Small File Problem

When Delta tables have hundreds or thousands of small Parquet files:

1. Run the [table-health-check.ps1](./scripts/table-health-check.ps1) script to assess file counts and sizes
2. Apply OPTIMIZE to consolidate files (target: 128 MB–1 GB per file)
3. Apply V-Order for read-optimized workloads
4. Schedule recurring maintenance — see [table-maintenance-workflow.md](./references/table-maintenance-workflow.md)

### Workflow 4: Optimize V-Order Configuration

When choosing between read-heavy and write-heavy resource profiles:

1. Identify your dominant workload pattern (ingestion vs. analytics)
2. New Fabric workspaces default to `writeHeavy` profile (V-Order disabled)
3. For Power BI / interactive queries, switch to `readHeavyForSpark` or `readHeavyForPBI`
4. Apply V-Order at session, table, or OPTIMIZE command level
5. See [v-order-decision-guide.md](./references/v-order-decision-guide.md) for detailed configuration

### Workflow 5: Diagnose Cross-Region Latency

When data in OneLake or external storage is in a different region than Fabric capacity:

1. Verify the Fabric capacity region in the Admin portal
2. Check shortcut destinations — are they in the same region?
3. For ADLS Gen2 or S3 shortcuts, confirm storage account region
4. Keep large fact tables co-located; small dimension tables tolerate cross-region
5. Use the [region-latency-test.ps1](./scripts/region-latency-test.ps1) script to measure impact

### Workflow 6: Direct Lake Fallback Investigation

When Direct Lake models fall back to DirectQuery instead of reading from OneLake:

1. Check if the semantic model has been framed (refreshed) recently
2. Verify Delta tables are V-Ordered for optimal transcoding
3. Check table row counts against the SKU guardrails
4. Review column data types — large string columns degrade performance
5. See [direct-lake-remediate.md](./references/direct-lake-remediate.md)

## remediate Quick Reference

| Symptom                      | Likely Cause                 | First Action                                  |
| ---------------------------- | ---------------------------- | --------------------------------------------- |
| HTTP 430 errors              | Capacity VCores exhausted    | Check Monitoring Hub, cancel idle sessions    |
| First query very slow        | Cold cache / node resume     | Check `data_scanned_remote_storage_mb`      |
| All queries slow             | Small files / no V-Order     | Run table health check script                 |
| Queries slow after migration | Wrong resource profile       | Switch to appropriate read/write profile      |
| Shortcuts slow               | Cross-region data access     | Verify region co-location                     |
| Direct Lake fallback         | Table not framed / too large | Check framing status and SKU guardrails       |
| VACUUM fails                 | Retention period too short   | Set retention >= 7 days                       |
| Streaming ingestion slow     | Schema enforcement overhead  | Consider Eventhouse with OneLake availability |

## References

- [Capacity SKU Reference](./references/capacity-sku-reference.md) — VCore limits, queue limits, node configurations
- [Cold Cache Diagnostics](./references/cold-cache-diagnostics.md) — T-SQL diagnostic queries and pre-warming
- [Table Maintenance Workflow](./references/table-maintenance-workflow.md) — OPTIMIZE, VACUUM, and scheduling
- [V-Order Decision Guide](./references/v-order-decision-guide.md) — When to enable/disable, resource profiles
- [Direct Lake remediate](./references/direct-lake-remediate.md) — Fallback investigation, framing, transcoding

## Available Scripts

- [spark-capacity-check.ps1](./scripts/spark-capacity-check.ps1) — Monitor Spark VCore utilization and queue depth
- [table-health-check.ps1](./scripts/table-health-check.ps1) — Assess Delta table file counts, sizes, and V-Order status
- [region-latency-test.ps1](./scripts/region-latency-test.ps1) — Measure cross-region OneLake access latency
- [run-table-maintenance.ps1](./scripts/run-table-maintenance.ps1) — Execute table maintenance via Fabric REST API

## Templates

- [diagnostic-report.md](./templates/diagnostic-report.md) — Template for documenting performance investigation findings
