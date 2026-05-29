---
name: minion-metrics
description: >
  View analytics and performance data for minions.
  Shows success rates, latency, and session history.
allowed-tools: Bash, Read
---

# Minion Metrics

View performance analytics for minion operations.

## Command

```bash
source .venv/bin/activate && python scripts/minions.py --json metrics
```

## What It Shows

- Total tasks and success rate
- Today's activity
- Performance by model
- Latency stats
- Recent sessions

## Example Output

```
=== Minion Metrics ===
Total tasks: 47
Success rate: 91%
Today: 12 tasks

By model:
  qwen2.5-coder:7b: 35 tasks, avg 4.2s
  deepseek-coder:1.3b: 12 tasks, avg 2.1s

Recent:
  20260112-143012: polish src/foo.py ✓
  20260112-142856: sweep llm_gc/ ✓
```

## Options

```bash
# Limit events
python scripts/minions.py --json metrics --limit 20
```

## Data Location

Metrics stored at `~/.minions/metrics.json`
