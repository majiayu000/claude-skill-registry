---
name: fabric-spark-compute-perf-remediate
description: >-
  Diagnose and resolve performance issues in Microsoft Fabric Delta Lake and Spark workloads.
  Use when remediate slow Spark notebooks, long-running Spark jobs, Delta table query
  degradation, small file problems, VOrder configuration, resource profile tuning, autotune
  configuration, capacity throttling (HTTP 430), session startup delays, executor memory
  errors, skewed partitions, or streaming ingestion bottlenecks. Covers Lakehouse, SQL
  analytics endpoint, Spark compute, environment configuration, Delta OPTIMIZE, VACUUM,
  Z-Order, bin-compaction, and Fabric capacity SKU sizing.
license: Complete terms in LICENSE.txt
---
# Fabric Delta Lake & Spark Performance remediate

Systematic remediate toolkit for diagnosing and resolving performance issues across
Microsoft Fabric Spark compute, Delta Lake tables, and Lakehouse workloads.

## When to Use This Skill

- Spark notebooks or jobs running slower than expected
- Delta table queries degrading over time (small file problem)
- Capacity throttling errors (HTTP 430 / TooManyRequestsForCapacity)
- Session startup taking minutes instead of seconds
- Out-of-memory errors on executors or drivers
- Streaming ingestion falling behind or producing small files
- VOrder or resource profile misconfiguration
- Deciding between read-heavy vs. write-heavy workload profiles
- Planning table maintenance (OPTIMIZE, VACUUM, Z-Order)
- Tuning autoscaling, dynamic executor allocation, or autotune

## Prerequisites

- Access to a Microsoft Fabric workspace with Data Engineering enabled
- Contributor or higher role on the workspace
- Fabric capacity (F2+) or Trial capacity
- PowerShell 7+ for diagnostic scripts
- PySpark for notebook-based diagnostics

## Triage: Identify the Symptom Category

Start by matching the observed symptom to one of these categories, then follow the linked
reference for the detailed workflow.

| Symptom                                  | Category              | Reference                                                  |
| ---------------------------------------- | --------------------- | ---------------------------------------------------------- |
| Notebook takes minutes to start          | Session Startup       | [session-startup.md](./references/session-startup.md)         |
| Queries slow, getting worse over time    | Delta Table Health    | [delta-table-health.md](./references/delta-table-health.md)   |
| HTTP 430 or "TooManyRequestsForCapacity" | Capacity Throttling   | [capacity-throttling.md](./references/capacity-throttling.md) |
| OOM errors, executor lost, task failed   | Memory & Compute      | [memory-compute.md](./references/memory-compute.md)           |
| Streaming lag, checkpoint delays         | Streaming Performance | [streaming-perf.md](./references/streaming-perf.md)           |
| Power BI reports slow against Lakehouse  | Read Optimization     | [read-optimization.md](./references/read-optimization.md)     |
| Spark job slow but no errors             | General Tuning        | [general-tuning.md](./references/general-tuning.md)           |

## Quick Diagnostic Checklist

Run through these checks before diving into detailed remediate.

### 1. Check Capacity and Concurrency

Verify your Fabric capacity SKU and current utilization. Each SKU has a queue limit
for concurrent Spark jobs:

| SKU   | Spark VCores | Queue Limit |
| ----- | ------------ | ----------- |
| F2    | 4            | 4           |
| F8    | 16           | 8           |
| F16   | 32           | 16          |
| F32   | 64           | 32          |
| F64   | 128          | 64          |
| F128  | 256          | 128         |
| Trial | 128          | No queueing |

If hitting queue limits, cancel idle jobs via the Monitoring Hub, scale the SKU, or
stagger job schedules.

### 2. Check Resource Profile

New Fabric workspaces default to the `writeHeavy` profile. Verify the active profile
matches your workload:

| Profile           | Best For                         | VOrder Default |
| ----------------- | -------------------------------- | -------------- |
| writeHeavy        | ETL, ingestion, batch writes     | Disabled       |
| readHeavyForSpark | Interactive Spark queries, EDA   | Enabled        |
| readHeavyForPBI   | Power BI Direct Lake, dashboards | Enabled        |

Mismatch is one of the most common performance issues. Read-heavy workloads on
the writeHeavy profile miss VOrder optimization entirely.

### 3. Check Delta Table Health

Run the [diagnostic script](./scripts/Diagnose-DeltaTableHealth.ps1) or execute in a
notebook:

```python
# Quick Delta table health check
from delta.tables import DeltaTable

dt = DeltaTable.forName(spark, "your_table_name")
history = dt.history()
history.select("version", "operation", "operationMetrics").show(20, truncate=False)
```

Look for: high version counts without OPTIMIZE, many small ADD operations, and
missing VACUUM runs.

### 4. Check Environment Configuration

Verify Spark compute settings in the attached environment:

```python
# Print active Spark configuration
for item in spark.sparkContext.getConf().getAll():
    print(f"{item[0]} = {item[1]}")
```

Key properties to verify:

- `spark.sql.parquet.vorder.default` — true for read workloads
- `spark.microsoft.delta.optimizeWrite.enabled` — true to reduce small files
- `spark.ms.autotune.enabled` — true to enable ML-based query tuning
- `spark.sql.adaptive.enabled` — true for adaptive query execution

### 5. Check Session Startup Time

Fabric Spark session startup depends on pool configuration:

| Scenario                              | Expected Startup          |
| ------------------------------------- | ------------------------- |
| Default settings, no custom libraries | 5–10 seconds             |
| Default + library dependencies        | 5–10 sec + 30 sec–5 min |
| High regional traffic                 | 2–5 minutes              |
| Private Links or Managed VNets        | 2–5 minutes              |
| High traffic + libraries + networking | 2–5 min + 30 sec–5 min  |

If consistently slow, check whether Private Links or Managed VNets are enabled
(these bypass Starter Pools).

## Key Configuration Properties

### VOrder (Read Optimization)

VOrder applies a special sort order to Parquet files at write time that dramatically
improves read performance for Power BI Direct Lake and SQL analytics endpoint queries.

Enable: `spark.sql.parquet.vorder.default = true`

Trade-off: Write operations take slightly longer. Enable only when read performance
matters more than write throughput.

### Native Execution Engine

Vectorized C++ engine that runs Spark SQL and DataFrame operations significantly
faster than the default JVM engine.

Enable: `spark.fabric.nativeExecution.enabled = true`

Compatible with Fabric Runtime 1.3+. Not all operations supported; the engine
falls back to JVM for unsupported operations transparently.

### Autotune

ML-based automatic Spark configuration tuning. Builds a model per query pattern
and optimizes settings iteratively over 20–25 runs.

Enable: `spark.ms.autotune.enabled = true`

Requirements: Fabric Runtime 1.1 or 1.2 only. Incompatible with high concurrency
mode and private endpoints. Targets queries running 15+ seconds.

### Optimized Write

Merges or splits partitions before writing to maximize file sizes and reduce small files.

Enable: `spark.microsoft.delta.optimizeWrite.enabled = true`

Trade-off: Adds a full shuffle before writes. Beneficial for append-heavy workloads;
may degrade performance if data is already well-partitioned.

## Available Scripts

| Script                                                                | Purpose                                       |
| --------------------------------------------------------------------- | --------------------------------------------- |
| [Diagnose-DeltaTableHealth.ps1](./scripts/Diagnose-DeltaTableHealth.ps1) | Assess Delta table health via Fabric REST API |
| [Get-SparkCapacityStatus.ps1](./scripts/Get-SparkCapacityStatus.ps1)     | Check capacity utilization and queue status   |
| [Invoke-TableMaintenance.ps1](./scripts/Invoke-TableMaintenance.ps1)     | Run OPTIMIZE + VACUUM via REST API            |

## Available Templates

| Template                                                            | Purpose                                        |
| ------------------------------------------------------------------- | ---------------------------------------------- |
| [perf-diagnostic-notebook.py](./templates/perf-diagnostic-notebook.py) | PySpark notebook for comprehensive diagnostics |

## remediate

| Problem                  | Likely Cause                         | Quick Fix                                      |
| ------------------------ | ------------------------------------ | ---------------------------------------------- |
| Queries slow, no errors  | Small files, missing VOrder          | Run OPTIMIZE with V-Order                      |
| Write jobs slow          | readHeavy profile on ETL workload    | Switch to writeHeavy profile                   |
| HTTP 430 errors          | Queue limit exceeded                 | Scale SKU or stagger jobs                      |
| OOM on executor          | Skewed partition or undersized nodes | Increase executor memory, check for skew       |
| Session takes 5+ minutes | Private Link/VNet or library install | Pre-install libraries, check networking        |
| Autotune not activating  | Wrong runtime or short queries       | Verify Runtime 1.1/1.2, queries must run 15s+  |
| Streaming falling behind | Too-frequent microbatches            | Increase trigger interval, use Optimized Write |

## References

- [Session Startup remediate](./references/session-startup.md)
- [Delta Table Health &amp; Maintenance](./references/delta-table-health.md)
- [Capacity Throttling &amp; SKU Sizing](./references/capacity-throttling.md)
- [Memory &amp; Compute Tuning](./references/memory-compute.md)
- [Streaming Performance Optimization](./references/streaming-perf.md)
- [Read Optimization (VOrder, Resource Profiles)](./references/read-optimization.md)
- [General Spark Tuning Guide](./references/general-tuning.md)
- [Microsoft Fabric Spark Compute Documentation](https://learn.microsoft.com/fabric/data-engineering/spark-compute)
- [Delta Lake Table Optimization and V-Order](https://learn.microsoft.com/fabric/data-engineering/delta-optimization-and-v-order)
- [Lakehouse Table Maintenance](https://learn.microsoft.com/fabric/data-engineering/lakehouse-table-maintenance)
