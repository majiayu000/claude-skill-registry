---
name: fabric-notebook-perf-remediate
description: Diagnose and resolve performance issues in Microsoft Fabric notebooks running Apache Spark. Use when notebooks are slow, Spark jobs are timing out, sessions hit HTTP 430 throttling errors, data skew causes straggling tasks, shuffle operations are inefficient, Delta Lake tables need optimization, V-Order configuration is needed, capacity utilization is high, OOM errors occur, or Spark Advisor warnings appear. Covers Spark session tuning, Native Execution Engine, autotune, custom Spark pools, partition optimization, and Monitoring Hub diagnostics.
license: Complete terms in LICENSE.txt
---

# Microsoft Fabric Notebook Performance remediate

Systematic toolkit for diagnosing, analyzing, and resolving performance bottlenecks in Microsoft Fabric notebooks powered by Apache Spark.

## When to Use This Skill

- Fabric notebook cells are running slowly or timing out
- Spark jobs are being throttled with HTTP 430 errors
- Capacity Metrics app shows high CU consumption
- Data skew is causing unbalanced task execution
- Shuffle operations are consuming excessive resources
- Delta Lake tables have degraded read/write performance
- OOM (Out of Memory) errors during notebook execution
- Spark Advisor shows warnings or errors in cell output
- Session startup is slow or sessions expire unexpectedly
- Pipeline-triggered notebooks are queued for extended periods

## Prerequisites

- Workspace Admin or Contributor role in the target Fabric workspace
- Access to the Fabric Monitoring Hub for your capacity
- Fabric Capacity Metrics app installed (for capacity-level analysis)
- Familiarity with PySpark or Spark SQL syntax

## remediate Decision Tree

Identify your symptom and follow the corresponding workflow.

| Symptom | Root Cause Category | Action |
|---------|-------------------|--------|
| Notebook cell runs for minutes on small data | Spark session config or query plan | See [Spark Session Tuning](./references/spark-session-tuning.md) |
| HTTP 430 error on job submission | Capacity exhausted, concurrency limit | See [Capacity and Throttling](#capacity-and-throttling) |
| One task takes 10x longer than others | Data skew | See [Data Skew Diagnosis](./references/data-skew-diagnosis.md) |
| Write operations are slow | V-Order overhead or small file problem | See [Delta Table Optimization](./references/delta-table-optimization.md) |
| OOM / executor lost errors | Memory pressure, partition sizing | See [Memory and Partition Tuning](#memory-and-partition-tuning) |
| Session expired / timed out | Idle timeout settings | See [Common Errors](./references/common-errors.md) |
| Notebook queued, never starts | Queue limits for SKU | See [Capacity and Throttling](#capacity-and-throttling) |

## Quick Wins Checklist

Apply these optimizations first — they resolve the majority of performance issues.

1. **Enable Native Execution Engine (NEE)** — delivers 2x–5x improvement:

```python
spark.conf.set("spark.native.enabled", "true")
```

2. **Enable Autotune** for adaptive configuration:

```python
spark.conf.set("spark.ms.autotune.enabled", "true")
```

3. **Right-size shuffle partitions** — default 200 is often wrong:

```python
# For datasets under 1 GB
spark.conf.set("spark.sql.shuffle.partitions", "20")
# For datasets 1-10 GB
spark.conf.set("spark.sql.shuffle.partitions", "100")
# For datasets over 10 GB, leave default or increase
```

4. **Enable Adaptive Query Execution (AQE)**:

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
```

5. **Use DataFrame APIs instead of RDDs** — enables Catalyst optimizer and Tungsten engine.

6. **Break complex query chains** into staged intermediate writes to reduce Catalyst plan complexity. See [Common Errors](./references/common-errors.md#excessive-query-complexity).

Run the [notebook health check script](./scripts/notebook-health-check.py) to audit your current session configuration.

## Capacity and Throttling

Each Fabric SKU maps to a fixed number of Spark VCores (1 CU = 2 Spark VCores). When all VCores are consumed, new jobs receive HTTP 430 errors.

| SKU | Spark VCores | Queue Limit |
|-----|-------------|-------------|
| F2 | 4 | 4 |
| F8 | 16 | 8 |
| F64 / P1 | 128 | 64 |
| F128 / P2 | 256 | 128 |
| F256 / P3 | 512 | 256 |

**Resolution steps:**

1. Open the **Monitoring Hub** and cancel idle or unnecessary Spark sessions.
2. Stop sessions you are not actively using — default idle timeout is 20 minutes.
3. Reduce executor count in custom Spark pools to free VCores for parallel jobs.
4. Enable **Autoscale Billing for Spark** for bursty workloads — jobs use dedicated serverless resources instead of consuming capacity CUs.
5. For pipeline-triggered notebooks, leverage job queueing (FIFO). Queue expiry is 24 hours.

> Queueing is not supported for interactive notebook jobs or Fabric trial capacities.

## Memory and Partition Tuning

OOM errors typically stem from oversized partitions or insufficient executor memory.

**Diagnose with Spark UI:**

1. Open the cell's Spark job progress indicator.
2. Click **Resources** tab to view executor usage graph.
3. Check the Spark Advisor light-bulb icon for memory warnings.

**Tune partitions:**

```python
# Check current partition count
df.rdd.getNumPartitions()

# Repartition for parallelism (increases partitions)
df = df.repartition(200)

# Coalesce to reduce partitions (avoids full shuffle)
df = df.coalesce(50)

# Adjust max partition bytes for reads
spark.conf.set("spark.sql.files.maxPartitionBytes", "128m")
```

**Tune task memory:**

```python
# For memory-intensive tasks causing OOM
spark.conf.set("spark.task.cpus", "2")  # More memory per task

# For CPU-bound tasks needing more parallelism
spark.conf.set("spark.task.cpus", "0.5")  # More concurrent tasks
```

## Monitoring and Diagnostics

### In-Notebook Monitoring

- **Spark job progress bar** — real-time per-cell execution status
- **Resources tab** — executor allocation and resource usage line chart (Spark 3.4+)
- **Spark Advisor** — Info/Warning/Error recommendations per cell (expand via light-bulb icon)

### Monitoring Hub

Navigate to Monitoring Hub to view all active Spark applications across your workspace. Key actions: cancel sessions, view executor count, check job duration, identify queued jobs.

### Capacity Metrics App

Filter by item type (Notebook, Lakehouse, Spark Job Definition) to see CU consumption per job. Use the Multi metric ribbon chart to identify capacity spikes over time.

**Formula:** CU consumption = Total Spark VCores / 2 × duration

## Spark Pool Configuration

### Starter Pools (Default)

Session initialization in 5–10 seconds, pre-configured, no manual setup. Good for development and small workloads.

### Custom Spark Pools

Configure via Workspace Settings → Data Engineering/Science → Spark Settings:

| Scenario | Node Size | Guidance |
|----------|-----------|----------|
| Transform-heavy with shuffles and joins | Large (16–64 cores) | Maximize per-node memory |
| Bursty or unpredictable jobs | Medium + Autoscale | Let cluster grow/shrink dynamically |
| Many small parallel jobs | Small/Medium | Use `mssparkutils.notebook.runMultiple()` |
| Development / exploration | Small, single node | Driver and executor share 1 VM |
| ML / distributed training | Many medium/large nodes | Maximize parallelism |

Enable **Customize compute configurations for items** in Workspace Settings → Pool tab to allow per-notebook pool overrides.

## Resource Profiles

Use predefined Spark resource profiles to auto-configure for your workload type:

| Profile | Best For |
|---------|----------|
| `Default` | General-purpose workloads |
| `readHeavyforSpark` / `ReadHeavy` | Interactive queries, dashboards (enables V-Order) |
| Write-heavy | Data ingestion pipelines (V-Order disabled by default) |

## Library Management Impact

Library installation in Fabric environments takes 5–15 minutes during publishing. For interactive development, use inline installation (`%pip install`) to avoid environment republish delays. However, inline commands are turned off by default in pipeline runs due to dependency tree instability.

| Method | Session Impact | Pipeline Safe |
|--------|---------------|---------------|
| Environment libraries | None (pre-installed) | Yes |
| Inline `%pip install` | Current session only | No |
| Inline `install.packages()` (R) | Current session only | No |

## References

- [Spark Session Tuning](./references/spark-session-tuning.md) — NEE, autotune, session configs, resource profiles
- [Data Skew Diagnosis](./references/data-skew-diagnosis.md) — Identifying skew, AQE, salting, repartitioning
- [Delta Table Optimization](./references/delta-table-optimization.md) — V-Order, OPTIMIZE, VACUUM, ZORDER
- [Common Errors](./references/common-errors.md) — Error messages, timeouts, connectivity, excessive query complexity
- [Notebook Health Check Script](./scripts/notebook-health-check.py) — PySpark diagnostic script
- [Spark Config Template](./templates/spark-config-template.py) — Starter configuration cell
