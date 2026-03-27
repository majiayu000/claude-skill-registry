---
name: session-trends
description: Analyze trends across session metrics. Computes windowed aggregates, deltas, and compares against MEMORY.md findings. Use periodically for progress tracking.
argument-hint: "[--window 7d|30d|all] [--project NAME] [--compare MEMORY.md]"
disable-model-invocation: true
---

# Session Trends

Analyze trends from the metrics ledger. Computes windowed aggregates,
fingerprint distributions, and compares against MEMORY.md baselines.

## Requirements

Requires `.claude/session-metrics/metrics.jsonl` from `/session-scan`.

## Usage

```
/session-trends                          # All windows (7d, 30d, all)
/session-trends --window 30d             # Specific window only
/session-trends --project enaia          # Filter by project
/session-trends --compare MEMORY.md      # Compare against memory baseline
```

## Pipeline

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:

- **`--window WINDOW`**: Time window — `7d`, `30d`, or `all` (default: show all three)
- **`--project NAME`**: Filter metrics by project name
- **`--compare PATH`**: Path to MEMORY.md for baseline comparison
  (default: auto-detect from `.claude/` project memory)

### Step 2: Read Metrics Ledger

Read `.claude/session-metrics/metrics.jsonl`.

If empty or missing:

> No metrics found. Run `/session-scan` first.

If `--project` specified, filter entries by project field.

### Step 3: Compute Trends via Python

```bash
python3 .claude/skills/session-scan/references/compute-metrics.py \
  --trends .claude/session-metrics/metrics.jsonl \
  --memory {MEMORY_PATH}
```

Capture the JSON output.

### Step 4: Display Trend Report

Format the JSON output as a readable report:

#### Overview

```
Total sessions: {N} ({backfilled} backfilled from v1)
Date range: {earliest} to {latest}
```

#### Window Comparison

```
| Metric                  | 7 days | 30 days | All time |
|-------------------------|--------|---------|----------|
| Sessions                | 12     | 45      | 165      |
| Avg friction            | 0.28   | 0.24    | 0.22     |
| Max friction            | 0.72   | 0.72    | 0.89     |
| Avg opportunity         | 0.35   | 0.30    | 0.28     |
| Tier 2 eligible         | 40%    | 33%     | 30%      |
| Plugin adoption         | 12%    | 10%     | 8%       |
```

#### Fingerprint Distribution

```
| Type          | 7d  | 30d | All  |
|---------------|-----|-----|------|
| bug-fix       | 4   | 15  | 52   |
| feature       | 3   | 12  | 48   |
| exploration   | 2   | 8   | 30   |
| maintenance   | 1   | 5   | 18   |
| review        | 1   | 3   | 10   |
| refactoring   | 1   | 2   | 7    |
```

#### MEMORY.md Comparison (if --compare)

Compare measured values against MEMORY.md claims:

```
| MEMORY.md Claim              | Measured    | Match? |
|------------------------------|-------------|--------|
| Plugin adoption: 8-12%       | 10.2%       | Yes    |
| Minimal friction in 40+ of 74| 68% smooth  | Yes    |
```

### Step 5: Write trends.json

Write computed trends to `.claude/session-metrics/trends.json`.

### Step 6: Suggest Actions

Based on trends:

- If friction is **increasing**: "Friction trending up — run `/session-deep-dive --from-scan` to investigate"
- If plugin adoption is **growing**: "Plugin adoption growing — check which commands drive value"
- If many Tier 2 eligible: "{N} sessions need deep analysis"

## Output Files

| File | Purpose |
|------|---------|
| `.claude/session-metrics/trends.json` | Computed trend data |

## Common Queries

See `references/trend-queries.md` for interpreting specific trend patterns.

## Iron Laws

1. **ALWAYS use Python for computation** — no manual aggregation
2. **NEVER modify metrics.jsonl** — read-only for trends
3. **ALWAYS show window comparison** — single numbers lack context
