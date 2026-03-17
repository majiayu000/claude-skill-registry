---
name: fabric-delta-spark-perf
description: Troubleshoot and optimize Delta Lake and Apache Spark performance in Microsoft Fabric. Use when diagnosing slow Spark jobs, small file problems, data skew, shuffle bottlenecks, out-of-memory errors, V-Order tuning, OPTIMIZE/VACUUM operations, partition strategy, resource profile selection (writeHeavy, readHeavyForSpark, readHeavyForPBI), autotune configuration, Native Execution Engine, broadcast joins, AQE (Adaptive Query Execution), or when Spark notebooks or Spark Job Definitions run slower than expected in Fabric Lakehouse workloads.
---

# Microsoft Fabric Delta Lake Spark Performance remediate

Systematic workflows for diagnosing and resolving Apache Spark and Delta Lake performance issues in Microsoft Fabric Lakehouse environments.

## When to Use This Skill

Activate when the user mentions any of the following:

- Spark job is slow, taking too long, or timing out
- Small file problem, too many small files, file fragmentation
- Data skew, straggler tasks, unbalanced partitions
- Out of memory (OOM) errors on driver or executor
- Shuffle spill, excessive shuffle read/write
- OPTIMIZE, VACUUM, bin-compaction, or table maintenance
- V-Order, Z-Order, or Parquet optimization
- Resource profiles: writeHeavy, readHeavyForSpark, readHeavyForPBI
- Autotune, Adaptive Query Execution (AQE), broadcast join thresholds
- Native Execution Engine configuration
- Streaming performance, microbatch tuning, checkpoint issues
- Spark pool sizing, autoscale, dynamic executor allocation
- Direct Lake performance tied to Delta table structure
- Capacity throttling, TooManyRequestsForCapacity errors

## Prerequisites

- Microsoft Fabric workspace with Data Engineering or Data Science experience
- Apache Spark notebooks or Spark Job Definitions
- Lakehouse with Delta tables
- Appropriate Fabric capacity SKU (F2 through F2048)

## Quick Diagnostic Workflow

When a user reports slow Spark performance, follow this triage sequence:

### Step 1: Identify the Symptom Category

| Symptom | Likely Root Cause | Jump To |
|---------|-------------------|---------|
| Job runs much longer than expected | Data skew or small files | Step 2 |
| OOM error on driver | `collect()`, `toPandas()`, or large broadcast | [diagnostic-checklist.md](./references/diagnostic-checklist.md#oom-errors) |
| OOM error on executor | Wide joins, large shuffles, insufficient memory | [diagnostic-checklist.md](./references/diagnostic-checklist.md#oom-errors) |
| Many tasks, most finish fast, few stragglers | Data skew | [diagnostic-checklist.md](./references/diagnostic-checklist.md#data-skew) |
| High shuffle read/write in Spark UI | Missing broadcast join or too many partitions | [diagnostic-checklist.md](./references/diagnostic-checklist.md#shuffle-bottlenecks) |
| Query reads thousands of small files | Small file problem, needs OPTIMIZE | Step 3 |
| Capacity throttled (HTTP 430) | Too many concurrent jobs for SKU | [spark-configurations.md](./references/spark-configurations.md#capacity-limits) |
| Streaming lag increasing | Microbatch interval or partition mismatch | [diagnostic-checklist.md](./references/diagnostic-checklist.md#streaming-performance) |

### Step 2: Check for Data Skew

Run the diagnostic script to detect skew in a target table:

```python
# Quick skew detection
df = spark.read.format("delta").table("your_table")
df.groupBy("partition_column") \
  .count() \
  .orderBy(F.desc("count")) \
  .show(20)
```

If the top partition has 10x+ more rows than the median, apply skew mitigation. See [diagnostic-checklist.md](./references/diagnostic-checklist.md#data-skew) for remediation steps.

### Step 3: Check File Health

```python
# Check file count and sizes for a Delta table
from delta.tables import DeltaTable
dt = DeltaTable.forName(spark, "your_table")
detail = spark.sql("DESCRIBE DETAIL your_table")
detail.select("numFiles", "sizeInBytes").show()

# Check for small files (< 32MB)
files_df = spark.sql("DESCRIBE DETAIL your_table")
```

If file count is high relative to data volume (e.g., >1000 files for <10GB), run OPTIMIZE. See [table-maintenance-guide.md](./references/table-maintenance-guide.md#optimize-command).

### Step 4: Verify Spark Configuration

Check that the environment has an appropriate resource profile:

```python
# Check current resource profile
print(spark.conf.get("spark.fabric.resourceProfile", "not set"))

# Check key write/read settings
configs = [
    "spark.sql.parquet.vorder.default",
    "spark.databricks.delta.optimizeWrite.enabled",
    "spark.databricks.delta.optimizeWrite.binSize",
    "spark.sql.shuffle.partitions",
    "spark.sql.autoBroadcastJoinThreshold",
    "spark.sql.files.maxPartitionBytes",
    "spark.databricks.optimizer.adaptive.enabled"
]
for c in configs:
    try:
        print(f"{c} = {spark.conf.get(c)}")
    except:
        print(f"{c} = (default)")
```

See [spark-configurations.md](./references/spark-configurations.md) for recommended values per workload type.

### Step 5: Apply Fix and Validate

After identifying the root cause, apply the appropriate fix from the references:

| Root Cause | Fix | Reference |
|------------|-----|-----------|
| Small files | Run OPTIMIZE with V-Order | [table-maintenance-guide.md](./references/table-maintenance-guide.md#optimize-command) |
| Stale files bloating storage | Run VACUUM with 7+ day retention | [table-maintenance-guide.md](./references/table-maintenance-guide.md#vacuum-command) |
| Data skew on joins | Enable AQE skew join + key salting | [diagnostic-checklist.md](./references/diagnostic-checklist.md#data-skew) |
| Wrong resource profile | Switch to appropriate profile | [spark-configurations.md](./references/spark-configurations.md#resource-profiles) |
| Driver OOM | Avoid `collect()`, increase driver memory | [diagnostic-checklist.md](./references/diagnostic-checklist.md#oom-errors) |
| Executor OOM | Increase executor memory, reduce partition size | [diagnostic-checklist.md](./references/diagnostic-checklist.md#oom-errors) |
| Excessive shuffling | Use broadcast joins for small tables | [diagnostic-checklist.md](./references/diagnostic-checklist.md#shuffle-bottlenecks) |
| V-Order not applied | Enable at table or session level | [table-maintenance-guide.md](./references/table-maintenance-guide.md#v-order) |

## Available Scripts

| Script | Purpose |
|--------|---------|
| [diagnose-delta-performance.py](./scripts/diagnose-delta-performance.py) | Automated diagnostic scan: file health, skew detection, config audit |
| [table-maintenance.py](./scripts/table-maintenance.py) | Run OPTIMIZE + VACUUM across all tables in a Lakehouse schema |

## Available Templates

| Template | Purpose |
|----------|---------|
| [notebook-performance-template.py](./templates/notebook-performance-template.py) | Starter notebook with performance best practices baked in |

## Key Principles

1. **Profile before optimizing** — Use Spark UI metrics and the diagnostic script before changing configurations. Most performance issues trace to data layout, not Spark settings.

2. **Match resource profile to workload** — Write-heavy ETL should use `writeHeavy` (V-Order off, stats collection off). Read-heavy analytics should use `readHeavyForSpark` or `readHeavyForPBI` (V-Order on, Optimized Write on).

3. **Right-size files first** — Target ~128MB–1GB per Parquet file. Use OPTIMIZE regularly for tables with frequent writes. Streaming tables need more frequent compaction.

4. **Partition wisely** — Only partition tables over 1TB. Use low-cardinality columns (< 200 distinct values). Over-partitioning creates the small file problem.

5. **Enable AQE** — Adaptive Query Execution handles skew joins, partition coalescing, and dynamic broadcast automatically. Keep it enabled.

6. **VACUUM safely** — Always retain at least 7 days. Shorter retention can break time travel and concurrent readers.

## References

- [Diagnostic Checklist](./references/diagnostic-checklist.md) — Step-by-step remediate for OOM, skew, shuffle, and streaming issues
- [Spark Configurations Guide](./references/spark-configurations.md) — Resource profiles, autotune, AQE, pool sizing, and capacity limits
- [Table Maintenance Guide](./references/table-maintenance-guide.md) — OPTIMIZE, VACUUM, V-Order, Z-Order, and Optimized Write deep dive
