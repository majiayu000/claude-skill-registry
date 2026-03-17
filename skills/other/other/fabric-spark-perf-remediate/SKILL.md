---
name: fabric-spark-perf-remediate
description: Diagnose and resolve Apache Spark performance issues in Microsoft Fabric. Use when asked to troubleshoot slow Spark notebooks, optimize Spark SQL queries, fix data skew or shuffle bottlenecks, tune spark.sql.shuffle.partitions or autoBroadcastJoinThreshold, configure resource profiles (writeHeavy, readHeavyForSpark, readHeavyForPBI), enable autotune, resolve HTTP 430 throttling errors, analyze Spark UI stages and executors, optimize Delta Lake writes with VOrder or Optimized Write, run table maintenance (bin-compaction, vacuum, Z-Order), fix small files problems, tune streaming throughput, or right-size Fabric Spark pools and capacity SKUs.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric Apache Spark Performance remediate

Systematic workflows for diagnosing, analyzing, and resolving Apache Spark performance problems in Microsoft Fabric Data Engineering and Data Science workloads.

## When to Use This Skill

Activate when encountering any of the following scenarios:

- Spark notebooks or jobs running slower than expected
- Capacity throttling errors (HTTP 430 / TooManyRequestsForCapacity)
- Data skew detected by Spark Advisor in notebook cells
- Excessive shuffle read/write in Spark UI stages
- Small files accumulation in Delta Lake tables
- Streaming ingestion throughput degradation
- Need to select or tune a Fabric Spark resource profile
- VOrder vs. Optimized Write decision-making
- Autotune configuration and validation
- Right-sizing Spark pools, node counts, or Fabric capacity SKUs

## Prerequisites

- Access to a Microsoft Fabric workspace with Data Engineering enabled
- Contributor or higher role on the workspace
- Familiarity with PySpark or Spark SQL
- PowerShell 7+ (for diagnostic scripts)
- Fabric REST API access token (for API-based diagnostics)

## Quick Diagnosis Decision Tree

Start here when a Spark job is slow:

1. **Is the job queued or throttled?** Check Monitoring Hub for HTTP 430.
   - Yes → See [Capacity and Concurrency Tuning](./references/spark-configuration-tuning.md#capacity-and-concurrency)
   - No → Continue

2. **Did the Spark Advisor flag warnings?** Check notebook cell indicators.
   - Data Skew detected → See [Data Skew Resolution](./references/spark-configuration-tuning.md#data-skew-resolution)
   - No warnings → Continue

3. **Is a single stage disproportionately slow?** Open Spark UI → Stages tab.
   - Yes, shuffle stage → See [Shuffle Optimization](./references/spark-configuration-tuning.md#shuffle-optimization)
   - Yes, scan stage → See [File Scan Optimization](./references/delta-lake-optimization.md#file-scan-optimization)
   - No → Continue

4. **Are executors underutilized?** Check Resources tab in monitoring detail.
   - High idle cores → See [Pool and Executor Sizing](./references/spark-configuration-tuning.md#pool-and-executor-sizing)
   - All cores busy → See [Partitioning Strategy](./references/spark-configuration-tuning.md#partitioning-strategy)

5. **Is the issue write-related?** Check write duration in Spark UI.
   - Yes → See [Delta Write Optimization](./references/delta-lake-optimization.md#delta-write-optimization)
   - No → See [General Spark SQL Tuning](./references/spark-configuration-tuning.md#spark-sql-tuning)

## Core Spark Configuration Quick Reference

These are the three settings Fabric Autotune manages automatically. If autotune is disabled, tune them manually:

| Setting | Default | Purpose | Tuning Guidance |
|---------|---------|---------|-----------------|
| `spark.sql.shuffle.partitions` | 200 | Partition count during joins/aggregations | Set to 2-3x total executor cores for your pool |
| `spark.sql.autoBroadcastJoinThreshold` | 10 MB | Max table size for broadcast joins | Increase to 100-256 MB for star-schema joins |
| `spark.sql.files.maxPartitionBytes` | 128 MB | Max bytes per file-read partition | Increase for large sequential scans, decrease for high parallelism |

## Resource Profiles Quick Reference

Fabric provides predefined profiles that bundle optimized Spark settings:

| Profile | Best For | VOrder | Key Characteristics |
|---------|----------|--------|---------------------|
| `writeHeavy` | ETL, batch ingestion, streaming | Disabled | Default for new workspaces; optimized write throughput |
| `readHeavyForSpark` | Interactive Spark queries, analytics | Enabled | Optimized read paths for Spark workloads |
| `readHeavyForPBI` | Power BI dashboards, DW queries | Enabled | Optimized for DirectLake and cross-engine reads |

Apply a profile at the environment level or override per-session:

```python
# Per-session override example
spark.conf.set("spark.fabric.resource.profile", "readHeavyForSpark")
```

## Autotune Quick Start

Enable autotune to let Fabric automatically optimize shuffle partitions, broadcast thresholds, and partition bytes:

```python
# Enable in a notebook session
spark.conf.set("spark.ms.autotune.enabled", "true")

# Or set in Environment > Spark Properties
# spark.ms.autotune.enabled = true
```

**Requirements**: Runtime 1.1 or 1.2 only. Not compatible with high concurrency mode or private endpoints. Needs 20-25 iterations to converge on optimal settings.

**Check autotune status** after a query:

```python
# View autotune decisions in Spark UI SQL tab
# Status values: QUERY_TUNING_SUCCEED, QUERY_TUNING_DISABLED,
#                QUERY_PATTERN_NOT_MATCH, QUERY_DURATION_TOO_SHORT
```

## Common Error Patterns

| Error / Symptom | Root Cause | Quick Fix |
|-----------------|------------|-----------|
| HTTP 430: TooManyRequestsForCapacity | All Spark VCores consumed | Cancel idle jobs in Monitoring Hub or upgrade SKU |
| Stage with 200 tasks, 1 task 100x slower | Data skew on join/group key | Add salting or use broadcast join |
| OOM on executor | Partition too large or broadcast too big | Increase partitions or lower broadcast threshold |
| Write takes >60% of total job time | Small files or missing optimization | Enable Optimized Write or run table maintenance |
| Streaming micro-batch latency increasing | Checkpoint overhead or partition mismatch | Tune trigger interval and Event Hub partitions |

## Step-by-Step Workflows

For detailed procedures, see the reference guides:

- [Spark Configuration Tuning](./references/spark-configuration-tuning.md) — Shuffle, broadcast, skew, pool sizing, capacity planning
- [Monitoring and Diagnostics](./references/monitoring-and-diagnostics.md) — Spark UI navigation, Monitoring Hub, APIs, log analysis
- [Delta Lake Optimization](./references/delta-lake-optimization.md) — VOrder, Optimized Write, table maintenance, partitioning, streaming

## Available Scripts

Run the [Fabric Spark diagnostics script](./scripts/Get-FabricSparkDiagnostics.ps1) to collect Spark application metrics via the Fabric REST API:

```powershell
./scripts/Get-FabricSparkDiagnostics.ps1 -WorkspaceId "<guid>" -Token "<bearer-token>"
```

## Available Templates

Use the [performance analysis notebook template](./templates/spark-perf-notebook.py) as a starting point for in-session diagnostics:

```python
# Paste into a Fabric notebook to analyze current session performance
```

## remediate

| Problem | Check | Resolution |
|---------|-------|------------|
| Autotune not activating | Runtime version, HC mode, private endpoint | Switch to Runtime 1.1/1.2, disable HC mode |
| Resource profile not applying | Environment publish status | Republish environment after profile change |
| Pool autoscale not scaling up | Capacity SKU limits | Verify VCore headroom in Capacity Metrics app |
| Table maintenance job stuck | Concurrent maintenance on same table | Wait for previous job or cancel via API |
| Notebook cell shows no Spark Advisor | Runtime < 3.4 | Upgrade to Spark 3.4+ runtime |

## References

- [Microsoft Fabric Spark Compute Overview](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-compute)
- [Autotune for Apache Spark in Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/autotune)
- [Concurrency Limits and Queueing](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-job-concurrency-and-queueing)
- [Spark Monitoring Overview](https://learn.microsoft.com/en-us/fabric/data-engineering/spark-monitoring-overview)
- [Delta Lake Table Optimization and V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order)
- [Resource Profile Configurations](https://learn.microsoft.com/en-us/fabric/data-engineering/resource-profile-configurations)
