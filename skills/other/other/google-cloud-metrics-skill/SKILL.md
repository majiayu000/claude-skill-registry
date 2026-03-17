---
name: cloud-metrics
description: Query Google Cloud Monitoring metrics using the cloud_metrics.py tool. Use when users ask about GCP metrics, Cloud Monitoring, Kubernetes metrics (CPU, memory, network), container resource usage, or need to export monitoring data. Triggers on requests like "show me CPU usage", "list available metrics", "describe this metric", "top memory consumers", or any Google Cloud Monitoring queries.
---

# Cloud Metrics

Query GCP Monitoring API using the bundled `cloud_metrics.py` script.

## Prerequisites

Requires GCP authentication. Verify with:
```bash
gcloud auth application-default print-access-token
```

If not authenticated:
```bash
gcloud auth application-default login
```

## Quick Reference

```bash
# Run with uv (handles dependencies automatically)
uv run scripts/cloud_metrics.py <command> [options]

# Commands
query     # Query metric data
describe  # Show metric labels and filter examples
list      # List available metrics
```

## Common Workflows

### Find top resource consumers

```bash
# Top 10 CPU consumers
uv run scripts/cloud_metrics.py query -p PROJECT -m kubernetes.io/container/cpu/core_usage_time --top 10 --stats

# Top memory users with latest values
uv run scripts/cloud_metrics.py query -p PROJECT -m kubernetes.io/container/memory/used_bytes --top 20 --latest
```

### Explore available metrics

```bash
# List all kubernetes metrics
uv run scripts/cloud_metrics.py list -p PROJECT --prefix kubernetes.io

# Describe a metric (shows available labels for filtering)
uv run scripts/cloud_metrics.py describe -p PROJECT -m kubernetes.io/container/cpu/core_usage_time
```

### Query with filters and aggregation

```bash
# Filter by namespace
uv run scripts/cloud_metrics.py query -p PROJECT -m kubernetes.io/container/cpu/core_usage_time \
  -f 'resource.labels.namespace_name="production"'

# Aggregate across containers, group by namespace
uv run scripts/cloud_metrics.py query -p PROJECT -m kubernetes.io/container/cpu/core_usage_time \
  --reducer REDUCE_SUM --group-by namespace_name

# Specific time range
uv run scripts/cloud_metrics.py query -p PROJECT -m kubernetes.io/container/cpu/core_usage_time \
  --start 2025-01-01T00:00:00Z --end 2025-01-01T12:00:00Z
```

### Export data

```bash
# JSON output (for jq processing)
uv run scripts/cloud_metrics.py query -p PROJECT -m kubernetes.io/container/cpu/core_usage_time \
  --output json --stats | jq '.[] | select(.stats.max > 0.5)'

# CSV output
uv run scripts/cloud_metrics.py query -p PROJECT -m kubernetes.io/container/cpu/core_usage_time \
  --output csv --latest > cpu_usage.csv
```

## Key Options

| Option | Description |
|--------|-------------|
| `-p, --project` | GCP project ID (required) |
| `-m, --metric` | Metric type (required for query/describe) |
| `-f, --filter` | Filter expression (repeatable) |
| `-d, --duration` | Time range: `30m`, `1h`, `7d` (default: 1h) |
| `--aligner` | ALIGN_RATE, ALIGN_MEAN, ALIGN_SUM, ALIGN_MAX, ALIGN_MIN, ALIGN_DELTA |
| `--reducer` | REDUCE_SUM, REDUCE_MEAN, REDUCE_MAX, REDUCE_COUNT, REDUCE_PERCENTILE_99/95/50 |
| `--group-by` | Label to group by when using reducer |
| `--top N` | Show only top N series by max value |
| `--stats` | Show statistics (min, max, avg, p50, p95, p99) |
| `--latest` | Show only latest value per series |
| `-o, --output` | `table` (default), `json`, `csv` |

## Common Metric Types

| Metric | Description |
|--------|-------------|
| `kubernetes.io/container/cpu/core_usage_time` | CPU usage (use ALIGN_RATE) |
| `kubernetes.io/container/memory/used_bytes` | Memory usage |
| `kubernetes.io/container/restart_count` | Container restarts |
| `kubernetes.io/pod/network/received_bytes_count` | Network RX |
| `kubernetes.io/pod/network/sent_bytes_count` | Network TX |
| `compute.googleapis.com/instance/cpu/utilization` | VM CPU utilization |
| `compute.googleapis.com/instance/disk/read_bytes_count` | Disk reads |
