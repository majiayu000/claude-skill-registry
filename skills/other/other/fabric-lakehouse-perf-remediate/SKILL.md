---
name: fabric-lakehouse-perf-remediate
description: Diagnose and resolve Microsoft Fabric Lakehouse performance issues including slow Spark queries, small file problems, Delta table fragmentation, V-Order configuration, table maintenance (OPTIMIZE, VACUUM, Z-Order), SQL analytics endpoint tuning, Direct Lake performance, resource profile selection, autotune configuration, capacity throttling, and streaming ingestion optimization. Use when asked to troubleshoot Fabric Lakehouse slowness, optimize Delta tables, fix small file problems, configure Spark settings, run table maintenance, or improve query performance in notebooks or pipelines.
license: Complete terms in LICENSE.txt
---

# Fabric Lakehouse Performance remediate

Systematic toolkit for diagnosing and resolving performance issues in Microsoft Fabric Lakehouse environments. Covers Delta table health, Spark compute tuning, query optimization, and automated maintenance workflows.

## When to Use This Skill

- Lakehouse queries are running slowly or timing out
- Delta tables have accumulated many small files (small file problem)
- Spark notebooks or jobs are underperforming
- Direct Lake semantic models have cold-start or transcoding delays
- SQL analytics endpoint queries are slow
- Table maintenance (OPTIMIZE, VACUUM) needs to be scheduled or automated
- V-Order, Z-Order, or resource profile configuration is needed
- Capacity throttling or concurrency issues are suspected
- Streaming ingestion is creating fragmented Delta tables

## Prerequisites

- Microsoft Fabric workspace with Lakehouse items
- Contributor or higher workspace role
- Fabric capacity (F2 or above) or Trial capacity
- For REST API automation: Microsoft Entra token for Fabric service
- For Spark commands: Access to Fabric notebooks or Spark Job Definitions

## Quick Diagnosis Checklist

When a user reports Lakehouse performance issues, work through these areas in order:

1. **Identify the symptom** — Slow reads, slow writes, capacity throttling, or query timeouts
2. **Check Delta table health** — File count, file sizes, V-Order status, partition layout
3. **Review Spark configuration** — Resource profile, autotune, shuffle partitions
4. **Inspect capacity utilization** — Concurrency limits, burst capacity, throttling
5. **Evaluate maintenance history** — When was OPTIMIZE/VACUUM last run?
6. **Assess data patterns** — Streaming vs batch, read-heavy vs write-heavy

## Symptom-to-Action Map

| Symptom | Root Cause | Action |
|---------|-----------|--------|
| Slow reads across all engines | Small files, no V-Order | Run OPTIMIZE VORDER, switch to readHeavy profile |
| Slow Spark queries only | Wrong shuffle partitions | Enable autotune or tune manually |
| Slow Power BI Direct Lake | Too many Parquet files/row groups | Run OPTIMIZE, check guardrail limits |
| Slow SQL analytics endpoint | Files under 400 MB, too many small files | OPTIMIZE with maxRecordsPerFile=2M |
| Write performance degraded | V-Order enabled on write-heavy workload | Switch to writeHeavy resource profile |
| Capacity throttled | Too many concurrent Spark jobs | Review concurrency limits, enable optimistic admission |
| Storage growing unexpectedly | VACUUM not running | Schedule VACUUM with 7-day retention |
| Streaming creates tiny files | No batching or trigger interval | Add processingTime trigger, run periodic OPTIMIZE |

## Core Optimization Operations

### 1. Table Maintenance Commands

Run in a Fabric notebook (Spark SQL):

```sql
-- Basic OPTIMIZE (bin-compaction)
OPTIMIZE lakehouse_name.schema_name.table_name;

-- OPTIMIZE with V-Order
OPTIMIZE lakehouse_name.schema_name.table_name VORDER;

-- OPTIMIZE with Z-Order on frequently filtered columns
OPTIMIZE lakehouse_name.schema_name.table_name ZORDER BY (column_name);

-- OPTIMIZE with both Z-Order and V-Order
OPTIMIZE lakehouse_name.schema_name.table_name ZORDER BY (column_name) VORDER;

-- OPTIMIZE specific partitions only
OPTIMIZE lakehouse_name.schema_name.table_name WHERE date_key >= '2025-01-01' VORDER;

-- VACUUM with default 7-day retention
VACUUM lakehouse_name.schema_name.table_name;

-- VACUUM with custom retention (requires safety check disabled)
VACUUM lakehouse_name.schema_name.table_name RETAIN 168 HOURS;
```

### 2. Resource Profile Configuration

Set at environment level or runtime. See [resource-profiles.md](./references/resource-profiles.md) for details.

```python
# Check current profile
spark.conf.get('spark.fabric.resourceProfile')

# Switch to read-heavy for Spark queries
spark.conf.set("spark.fabric.resourceProfile", "readHeavyForSpark")

# Switch to read-heavy for Power BI Direct Lake
spark.conf.set("spark.fabric.resourceProfile", "readHeavyForPBI")

# Switch to write-heavy for ETL/ingestion
spark.conf.set("spark.fabric.resourceProfile", "writeHeavy")
```

### 3. V-Order Control

```python
# Check current V-Order setting
spark.conf.get('spark.sql.parquet.vorder.default')

# Enable V-Order for read-heavy workloads
spark.conf.set('spark.sql.parquet.vorder.default', 'true')

# Disable V-Order for write-heavy ingestion
spark.conf.set('spark.sql.parquet.vorder.default', 'false')
```

### 4. Autotune Configuration

```sql
-- Enable autotune for automatic Spark SQL tuning
SET spark.ms.autotune.enabled=TRUE;

-- Disable autotune
SET spark.ms.autotune.enabled=FALSE;
```

Autotune adjusts three key settings per query: `spark.sql.shuffle.partitions`, `spark.sql.autoBroadcastJoinThreshold`, and `spark.sql.files.maxPartitionBytes`. Requires 20-25 iterations to learn optimal settings. Only works on Runtime 1.1 and 1.2. Not compatible with high concurrency mode or private endpoints.

### 5. SQL Analytics Endpoint Optimization

For best SQL analytics endpoint performance, target ~2 million rows and ~400 MB per Parquet file:

```python
# Before data changes
spark.conf.set("spark.sql.files.maxRecordsPerFile", 2000000)

# Perform data operations (inserts, updates, deletes)
# ...

# After data changes, set max file size and optimize
spark.conf.set("spark.databricks.delta.optimize.maxFileSize", 4294967296)
```

Then run OPTIMIZE on the affected tables.

## REST API Automation

Automate table maintenance via the Fabric REST API. See [rest-api-maintenance.md](./references/rest-api-maintenance.md) for full details.

**Endpoint:**
```
POST https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{lakehouseId}/jobs/instances?jobType=TableMaintenance
```

**Request body:**
```json
{
  "executionData": {
    "tableName": "my_table",
    "schemaName": "dbo",
    "optimizeSettings": {
      "vOrder": "true",
      "zOrderBy": ["frequently_filtered_column"]
    },
    "vacuumSettings": {
      "retentionPeriod": "7.01:00:00"
    }
  }
}
```

**Monitor status:**
```
GET https://api.fabric.microsoft.com/v1/workspaces/{workspaceId}/items/{lakehouseId}/jobs/instances/{operationId}
```

## Streaming Ingestion Best Practices

When streaming data into a Lakehouse, prevent small file proliferation:

1. **Set processing time triggers** to batch events into larger writes
2. **Use Optimized Write** (`spark.microsoft.delta.optimizeWrite.enabled = true`)
3. **Partition wisely** — low-cardinality columns only (< 100-200 distinct values)
4. **Schedule periodic OPTIMIZE** — daily or more often for high-frequency streams
5. **Combine repartition() with partitionBy()** for optimal in-memory and on-disk layout

```python
# Example: Streaming with batching and partitioning
rawData = df \
  .writeStream \
  .format("delta") \
  .option("checkpointLocation", "Files/checkpoint") \
  .outputMode("append") \
  .partitionBy("date_key") \
  .trigger(processingTime="1 minute") \
  .toTable("my_streaming_table")
```

## Available Scripts

- [Invoke-FabricTableMaintenance.ps1](./scripts/Invoke-FabricTableMaintenance.ps1) — PowerShell script to automate table maintenance via REST API across multiple tables
- [Get-DeltaTableHealth.ps1](./scripts/Get-DeltaTableHealth.ps1) — PowerShell script to assess Delta table health metrics via Fabric REST API

## Available Templates

- [maintenance-notebook.py](./templates/maintenance-notebook.py) — PySpark notebook template for comprehensive table maintenance
- [perf-diagnostic-notebook.py](./templates/perf-diagnostic-notebook.py) — PySpark notebook template for diagnosing performance issues

## Detailed References

- [Resource Profiles](./references/resource-profiles.md) — Complete guide to Fabric Spark resource profile selection and configuration
- [REST API Maintenance](./references/rest-api-maintenance.md) — Automating table maintenance with Fabric REST API and PowerShell
- [Delta Table Health](./references/delta-table-health.md) — Assessing and monitoring Delta table file layout, V-Order status, and partition health
- [Concurrency and Capacity](./references/concurrency-capacity.md) — Understanding Spark job admission, throttling, burst capacity, and autoscale billing

## remediate

| Issue | Cause | Fix |
|-------|-------|-----|
| OPTIMIZE command not recognized | Running in SQL analytics endpoint | Use Fabric notebook with Spark runtime |
| VACUUM fails with retention error | Retention < 7 days without safety override | Set `spark.databricks.delta.retentionDurationCheck.enabled=false` |
| Autotune not activating | Query too short (< 15 seconds) or wrong runtime | Use Runtime 1.1/1.2, ensure queries exceed 15s |
| Table maintenance API returns 409 | Another maintenance job running on same table | Wait for completion, jobs on different tables run in parallel |
| V-Order not applied after OPTIMIZE | Session/table property mismatch | Use `OPTIMIZE table VORDER` explicitly |
| Capacity throttled during maintenance | Maintenance consuming too many cores | Schedule during off-peak, reduce concurrent jobs |

## Key Decision Framework

```
Is the workload primarily reads or writes?
├── Read-heavy (dashboards, queries, analytics)
│   ├── Power BI Direct Lake → readHeavyForPBI profile + OPTIMIZE VORDER
│   └── Spark analytics → readHeavyForSpark profile + enable autotune
├── Write-heavy (ETL, ingestion, streaming)
│   └── writeHeavy profile + periodic OPTIMIZE + VACUUM on schedule
└── Mixed workload
    ├── Separate environments for read vs write paths
    └── Use runtime spark.conf.set() to switch profiles per notebook
```
