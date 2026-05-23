---
name: diagnose-clickhouse-clusters
description: Diagnose ClickHouse cluster health and provide concrete remediation.
metadata:
  author: System
---

# Tools

- `collect_cluster_status`: modes `snapshot` (default) | `windowed`
  - Collection only — diagnosis and recommendations are produced by this skill.
  - For charts, delegate to the `visualization` skill; never emit chart specs directly.

# Workflow

1. Always call `collect_cluster_status` before any health assessment.
2. Use `status_analysis_mode="windowed"` for bounded-time questions (e.g., "past 3 hours"); keep the same window in follow-up calls.
3. Base all findings solely on `collect_cluster_status` output.

# Severity Thresholds

| Level | Replication Lag | Disk Usage |
|---|---|---|
| CRITICAL | > 300s | > 90% |
| WARNING | > 60s | > 80% |

# Output Format

1. **`### Summary`** — print this heading, then:

   | Status | Nodes with Issues | Checks Run | Timestamp |
   |--------|-------------------|------------|-----------|
   | 🟢 OK / 🟠 WARNING / 🔴 CRITICAL | N | comma-separated category names (e.g., `parts, replication, disk`) | ISO8601 |

2. **`### Findings by Category`** — print this heading, then a markdown table with one row per category returned by the tool, in stable order:

   | Category | Status | Key Metrics | Top Outlier / Scope | Notes |
   |----------|--------|-------------|----------------------|-------|

   Rules:
   - Status: emoji + text (e.g., `🟠 WARNING`), never emoji-only.
   - Key Metrics: 1–2 values, single-line, semicolon-separated (e.g., `max_parts_per_partition=533 (>500)`).
   - Notes: remaining metrics as compact `key=value` items, single-line.
   - Wrap identifiers in backticks (e.g., `` `db.table` ``).
   - No outlier → set `Top Outlier / Scope` to `-`.
   - No multi-line content inside cells.

3. **Recommendations** — max 3 items: title + reason + SQL/command if applicable.

# Rules

- Never give a health opinion without calling `collect_cluster_status` first.
- Never assume schema or table names; use only tool output.
- Never write custom health-check SQL; the tool is the source of truth.
