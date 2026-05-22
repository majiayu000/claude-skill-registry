---
name: fabric-pyspark-perf-remediate
description: Diagnose and resolve Apache Spark performance issues in Microsoft Fabric notebooks and Spark Job Definitions. Use when PySpark jobs are slow, notebooks take too long, Spark stages are skewed, shuffles are excessive, out-of-memory errors occur, Delta Lake writes are slow, or Fabric capacity is throttled. Covers data skew, shuffle optimization, broadcast joins, partition tuning, VOrder, Optimized Write, resource profiles, autotune, native execution engine, small file compaction, and Spark UI interpretation. Keywords include slow notebook, OOM, spill, shuffle, skew, broadcast, repartition, coalesce, OPTIMIZE, VACUUM, Z-ORDER, checkpoint, cache, persist, executor memory, driver memory, spark.sql.shuffle.partitions, autoBroadcastJoinThreshold, maxPartitionBytes, Fabric capacity throttling, CU utilization.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric PySpark Performance remediate

Systematic guide for diagnosing and resolving Apache Spark performance problems in Microsoft Fabric Data Engineering workloads, including notebooks, Spark Job Definitions, and pipeline activities.

## When to Use This Skill

Activate when encountering any of these scenarios:

- PySpark notebook cells take unexpectedly long to execute
- Spark Job Definitions exceed expected duration or fail with timeouts
- Out-of-memory (OOM) errors on driver or executors
- Excessive shuffle read/write in Spark UI stage details
- Data skew causing individual tasks to run much longer than peers
- Delta Lake table writes are slow or produce many small files
- Fabric capacity utilization is high or jobs are queued/throttled
- Need to choose between resource profiles (readHeavy vs writeHeavy)
- Deciding whether to enable autotune, native execution engine, or Optimized Write
- Interpreting Spark UI metrics (stages, tasks, storage, SQL plan)

## Prerequisites

- Access to a Microsoft Fabric workspace with Data Engineering/Science experience
- Fabric capacity (F2 or higher) with Spark compute enabled
- Familiarity with PySpark DataFrames and Spark SQL
- Access to Spark UI via the Monitoring Hub or notebook session details

## Quick Diagnostic Workflow

Follow this triage sequence to identify the root cause:

1. **Check capacity status** - Is the Fabric capacity throttled or overloaded? See Monitoring Hub for queued jobs and CU utilization.
2. **Identify the slow stage** - Open Spark UI, find the stage with the longest duration, and check task-level metrics.
3. **Classify the bottleneck** - Use the decision matrix below to categorize the issue.
4. **Apply targeted fix** - Follow the relevant reference guide for your bottleneck type.
5. **Validate improvement** - Re-run the job and compare Spark UI metrics before and after.

## Bottleneck Decision Matrix

Use these indicators to classify your performance issue:

**Shuffle Bottleneck**: Shuffle read/write bytes are large (>1 GB per stage), many tasks in the stage, high GC time. Fix with broadcast joins, reduced shuffle partitions, or pre-partitioned data. See [shuffle-and-join-optimization.md](./references/shuffle-and-join-optimization.md).

**Data Skew**: One or few tasks take 10x longer than median, input size per task is highly uneven, some tasks process GBs while others process MBs. Fix with salting, repartitioning, or adaptive query execution. See [data-skew-resolution.md](./references/data-skew-resolution.md).

**Memory Pressure / OOM**: Executor lost errors, "Container killed by YARN for exceeding memory limits", excessive GC time (>10% of task time), disk spill. Fix with memory configuration, caching strategy, or partition sizing. See [memory-and-spill-tuning.md](./references/memory-and-spill-tuning.md).

**Small Files / Delta Compaction**: Write operations produce thousands of small Parquet files, reads are slow due to file listing overhead, table maintenance never run. Fix with OPTIMIZE, Optimized Write, or streaming trigger intervals. See [delta-table-optimization.md](./references/delta-table-optimization.md).

**Capacity / Compute Sizing**: Jobs queued for long periods, capacity utilization consistently above 80%, throttling messages in monitoring. Fix with pool sizing, resource profiles, or autoscale billing. See [fabric-compute-tuning.md](./references/fabric-compute-tuning.md).

## Key Spark Configuration Quick Reference

### Session-Level Overrides (Notebook Cell 1)

```python
# Shuffle partition count - default is 200, tune to data volume
spark.conf.set("spark.sql.shuffle.partitions", "auto")

# Broadcast join threshold - default 10MB, increase for medium tables
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "50m")

# Max partition bytes - default 128MB, increase for fewer larger partitions
spark.conf.set("spark.sql.files.maxPartitionBytes", "256m")

# Enable Optimized Write for Delta
spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")

# Enable autotune (preview, Runtime 1.1/1.2 only)
spark.conf.set("spark.ms.autotune.enabled", "true")

# Enable native execution engine
spark.conf.set("spark.native.enabled", "true")

# VOrder for read-optimized scenarios (Power BI, SQL endpoint)
spark.conf.set("spark.sql.parquet.vorder.default", "true")
```

### Fabric Resource Profiles

| Profile | Best For | VOrder | Key Behavior |
|---------|----------|--------|--------------|
| `writeHeavy` | ETL, ingestion, streaming | Off | Optimized throughput for writes (new workspace default) |
| `readHeavyForSpark` | Interactive queries, EDA | On | Optimized for Spark read operations |
| `readHeavyForPBI` | Power BI, SQL endpoint | On | Optimized for downstream BI consumption |

Resource profiles are set at the environment level in Workspace Settings > Data Engineering/Science > Spark Settings.

### Autotune Details

Autotune automatically adjusts three key configurations per query using ML:

| Setting | Default | What Autotune Optimizes |
|---------|---------|------------------------|
| `spark.sql.shuffle.partitions` | 200 | Partition count for shuffles |
| `spark.sql.autoBroadcastJoinThreshold` | 10 MB | Broadcast join size threshold |
| `spark.sql.files.maxPartitionBytes` | 128 MB | Max bytes per read partition |

**Requirements**: Runtime 1.1 or 1.2, not compatible with high concurrency mode or private endpoints. Needs 20-25 iterations to learn optimal config. Targets repetitive queries running >15 seconds.

## Diagnostic Scripts

Run these in a Fabric notebook to gather performance data:

- [spark_health_check.py](./scripts/spark_health_check.py) - Comprehensive session diagnostics including configuration, pool info, and Delta table stats
- [identify_skew.py](./scripts/identify_skew.py) - Detect data skew in a DataFrame by analyzing partition sizes
- [delta_table_health.py](./scripts/delta_table_health.py) - Analyze Delta table file sizes, history, and maintenance status

## Notebook Templates

- [perf_baseline_template.py](./templates/perf_baseline_template.py) - Template for establishing performance baselines with timing instrumentation

## Common Anti-Patterns

**Collecting large datasets to the driver**: `df.collect()` or `df.toPandas()` on large DataFrames causes OOM. Use `.limit()`, `.take()`, or write to Delta instead.

**Using `repartition()` before write when Optimized Write is available**: Optimized Write handles partition optimization automatically, making explicit `repartition()` calls redundant and expensive.

**Never running OPTIMIZE on Delta tables**: Over time, append-heavy tables accumulate small files. Schedule `OPTIMIZE` (and optionally `VACUUM`) as maintenance.

**Caching DataFrames that are used only once**: `.cache()` or `.persist()` consume memory/storage. Only cache DataFrames referenced multiple times in the same session.

**Using Python UDFs instead of native Spark functions**: Python UDFs serialize data between JVM and Python, causing major overhead. Prefer `pyspark.sql.functions` or Pandas UDFs for vectorized operations.

**Ignoring partition pruning**: Reading Delta tables without filter predicates on partition columns forces full table scans. Always filter on partition columns when possible.

## remediate Quick Fixes

**Problem**: Notebook hangs on first cell.
**Fix**: Check if the Spark session is waiting for cluster allocation. Verify capacity is not fully utilized in Monitoring Hub. Consider starter pools for faster spin-up.

**Problem**: `java.lang.OutOfMemoryError: Java heap space` on driver.
**Fix**: Reduce `collect()` size, increase driver memory in environment settings, or switch to writing results to a table instead of returning to the driver.

**Problem**: Stage with 200 tasks where 1 task takes 30 minutes and rest take 30 seconds.
**Fix**: Classic data skew. See [data-skew-resolution.md](./references/data-skew-resolution.md) for salting and repartitioning techniques.

**Problem**: Write operation produces 10,000+ small files.
**Fix**: Enable Optimized Write: `spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")`. Run `OPTIMIZE` on the table afterward. See [delta-table-optimization.md](./references/delta-table-optimization.md).

**Problem**: Job ran fine last week but is slow now.
**Fix**: Check Delta table history for data volume growth. Run `DESCRIBE HISTORY table_name` and check `OPTIMIZE` history. Also check if workspace resource profile changed.

## References

- [Shuffle and Join Optimization](./references/shuffle-and-join-optimization.md)
- [Data Skew Resolution](./references/data-skew-resolution.md)
- [Memory and Spill Tuning](./references/memory-and-spill-tuning.md)
- [Delta Table Optimization](./references/delta-table-optimization.md)
- [Fabric Compute Tuning](./references/fabric-compute-tuning.md)
- [Spark UI Interpretation Guide](./references/spark-ui-guide.md)
