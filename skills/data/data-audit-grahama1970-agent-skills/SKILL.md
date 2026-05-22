---
name: data-audit
description: >
  Report on data completeness for the SPARTA QRA pipeline (Control -> URL -> Knowledge -> QRA).
  Queries DuckDB to show coverage percentages at each stage.
triggers:
  - audit sparta
  - check coverage
  - data completeness
  - pipeline status
metadata:
  short-description: SPARTA data completeness auditor.
  project-path: /home/graham/workspace/experiments/pi-mono/.agent/skills/data-audit

provides:
  - data-audit
composes:
  - create-figure
  - task-monitor
---

# Data Audit

Audits the SPARTA pipeline data coverage.

## Usage

```bash
# Run full audit
.agent/skills/data-audit/run.sh

# Run for specific run ID (points to specific DB path if needed)
.agent/skills/data-audit/run.sh --run-id <run-id>
```

## Logic

Connects to SPARTA DuckDB and calculates coverage for:

1. **Controls**: Base set.
2. **URLs**: Controls mapped to at least one URL.
3. **Knowledge**: Controls mapped to URLs that have extracted chunks.
4. **QRA**: Controls that have generated QRA pairs.

## Visualization

After generating coverage data, offer to visualize via `/create-figure`:

```bash
# Pipeline coverage as stacked bar chart
create-figure metrics --input audit.json --output coverage.png --type bar --title "SPARTA Pipeline Coverage"

# Coverage heatmap by category
create-figure heatmap --input audit.json --output coverage-heatmap.png
```

**When to offer:** After presenting coverage percentages, ask: "Want me to chart the pipeline coverage?"
