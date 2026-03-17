---
name: bv
description: "Beads Viewer - graph-aware triage engine for Beads issue tracker with 9 graph metrics (PageRank, betweenness, HITS, etc.), dependency-aware planning, and purpose-built robot protocol for AI agents."
---

# BV - Beads Viewer

A high-performance TUI and graph-aware triage engine for the [Beads](https://github.com/steveyegge/beads) issue tracker. Treats your project as a **Directed Acyclic Graph (DAG)**, computing 9 graph-theoretic metrics to surface hidden dependencies, bottlenecks, and optimal work ordering.

## CRITICAL: Robot Mode Required for AI Agents

**NEVER run bare `bv`** - it launches an interactive TUI that blocks your session!

```bash
# WRONG - blocks terminal with TUI
bv

# CORRECT - JSON output for agents
bv --robot-triage
bv --robot-plan
bv --robot-insights
```

**Always use `--robot-*` flags for machine-readable output.**

---

## Quick Reference for AI Agents

### The Mega-Command: Start Here

```bash
# THE SINGLE ENTRY POINT - returns everything you need
bv --robot-triage
```

**Returns:**
- `quick_ref`: at-a-glance counts + top 3 picks
- `recommendations`: ranked actionable items with scores, reasons, unblock info
- `quick_wins`: low-effort high-impact items
- `blockers_to_clear`: items that unblock the most downstream work
- `project_health`: status/type/priority distributions, graph metrics
- `commands`: copy-paste shell commands for next steps

### Minimal Alternative

```bash
# Just the single top pick + claim command
bv --robot-next
```

---

## Why Use BV

### Graph Intelligence vs. List Thinking

Traditional trackers treat issues as a flat list sorted by priority. BV sees your project as a **dependency graph** and answers questions like:

| Traditional Question | BV's Graph-Aware Answer |
|---------------------|------------------------|
| "What's highest priority?" | "What unblocks the most work?" |
| "What should I work on?" | "What's on the critical path with zero slack?" |
| "Is this issue important?" | "What's its PageRank? Betweenness? Does it bridge clusters?" |
| "Are we making progress?" | "Did we resolve cycles? Is density improving?" |

### Use Cases

```bash
# "What should I work on next?"
bv --robot-triage | jq '.recommendations[0]'

# "What's blocking the most progress?"
bv --robot-triage | jq '.blockers_to_clear'

# "Can multiple agents work in parallel?"
bv --robot-plan | jq '.tracks'

# "Are there circular dependencies?" (structural bugs!)
bv --robot-insights | jq '.Cycles'

# "What changed since last release?"
bv --robot-diff --diff-since v1.0.0
```

---

## The 9 Graph Metrics

BV computes these metrics to surface hidden project dynamics:

| # | Metric | What It Measures | Actionable Insight |
|---|--------|------------------|-------------------|
| 1 | **PageRank** | Recursive dependency importance | Foundational blockers |
| 2 | **Betweenness** | Shortest-path traffic | Bottlenecks & bridges |
| 3 | **HITS Hubs** | Dependency aggregators | Epics/milestones |
| 4 | **HITS Authorities** | Depended-on utilities | Core infrastructure |
| 5 | **Critical Path** | Longest dependency chain | Zero-slack keystones |
| 6 | **Eigenvector** | Influence via neighbors | Strategic dependencies |
| 7 | **Degree** | Direct connection counts | Immediate blockers/blocked |
| 8 | **Density** | Edge-to-node ratio | Project coupling health |
| 9 | **Cycles** | Circular dependencies | Structural bugs (must fix!) |

### Understanding the Metrics

**PageRank (Foundational Blocks)**
High PageRank = bedrock of your project. Rarely user-facing features; usually schemas, core libraries, or architectural decisions. Breaking them breaks the graph.

**Betweenness (Gatekeepers)**
High betweenness = choke point. Might be an API contract both mobile and server teams wait on. Delay here doesn't just block one thread—it prevents sub-teams from synchronizing.

**HITS (Epics vs. Utilities)**
- **High Hub Score**: Epics/Product Features that aggregate many dependencies
- **High Authority Score**: Utilities that provide value to many consumers

**Critical Path (Keystones)**
Any delay on keystone tasks translates 1:1 into project delivery delay. These have zero "slack."

**Cycles (Structural Bugs)**
Circular dependencies are logical impossibilities. They indicate:
- Misclassified dependencies
- Missing intermediate tasks
- Scope confusion (should be merged)

---

## Command Reference

### Triage & Planning

```bash
# THE MEGA-COMMAND: comprehensive triage
bv --robot-triage

# Minimal: just the top pick
bv --robot-next

# Parallel execution tracks (for multi-agent work)
bv --robot-plan

# Priority misalignment detection
bv --robot-priority
```

### Graph Analysis

```bash
# Full metrics: PageRank, betweenness, HITS, eigenvector, critical path, cycles
bv --robot-insights

# Label-based analysis
bv --robot-label-health           # Per-label health (healthy|warning|critical)
bv --robot-label-flow             # Cross-label dependencies, bottleneck labels
bv --robot-label-attention        # Attention-ranked labels
bv --robot-label-attention --attention-limit=5
```

### History & Change Tracking

```bash
# Bead-to-commit correlations
bv --robot-history
bv --robot-history --bead-history BV-123   # Single bead focus
bv --robot-history --min-confidence 0.7     # High-confidence only

# Changes since a reference point
bv --robot-diff --diff-since HEAD~10
bv --robot-diff --diff-since v1.0.0
bv --robot-diff --diff-since "2024-01-01"
```

### Sprint & Forecasting

```bash
# Sprint burndown
bv --robot-burndown "Sprint 42"

# ETA predictions with dependency-aware scheduling
bv --robot-forecast all
bv --robot-forecast BV-123

# Alerts: stale issues, blocking cascades, priority mismatches
bv --robot-alerts

# Hygiene suggestions: duplicates, missing deps, cycle breaks
bv --robot-suggest
```

### Graph Export

```bash
# JSON (default)
bv --robot-graph

# Graphviz DOT (for rendering)
bv --robot-graph --graph-format=dot

# Mermaid (for docs)
bv --robot-graph --graph-format=mermaid

# Focused subgraph
bv --robot-graph --graph-root=BV-123 --graph-depth=3

# Interactive HTML visualization
bv --export-graph graph.html
bv --export-graph sprint.html --graph-title "Sprint 42"
```

### Scoping & Filtering

```bash
# Scope to label's subgraph
bv --robot-plan --label backend

# Historical point-in-time analysis
bv --robot-insights --as-of HEAD~30
bv --robot-insights --as-of v1.0.0
bv --robot-insights --as-of "2024-01-15"

# Pre-filter with recipes
bv --recipe actionable --robot-plan    # Ready to work (no blockers)
bv --recipe high-impact --robot-triage # Top PageRank scores
bv --recipe bottlenecks --robot-plan   # High betweenness nodes

# Group triage output
bv --robot-triage --robot-triage-by-track  # By parallel work streams
bv --robot-triage --robot-triage-by-label  # By domain
```

### Export & Reporting

```bash
# Markdown report with Mermaid diagrams
bv --export-md report.md

# Static site for stakeholder sharing
bv --pages                              # Interactive wizard
bv --export-pages ./dashboard           # Local export
bv --export-pages ./bv-pages --pages-title "Sprint 42 Status"
bv --preview-pages ./dir                # Preview locally
```

---

## Understanding Robot Output

### All Robot JSON Includes

| Field | Purpose |
|-------|---------|
| `data_hash` | Fingerprint of beads.jsonl (verify consistency across calls) |
| `status` | Per-metric state: `computed\|approx\|timeout\|skipped` + elapsed_ms |
| `as_of` / `as_of_commit` | Present when using `--as-of`; contains ref and resolved SHA |

### Two-Phase Analysis

BV uses async computation with intelligent timeouts:

| Phase | Metrics | Latency | Notes |
|-------|---------|---------|-------|
| **Phase 1** | Degree, topo sort, density | Instant | Always available |
| **Phase 2** | PageRank, betweenness, HITS, eigenvector, cycles | 500ms timeout | Check `status` flags |

**For large graphs (>500 nodes):** Some Phase 2 metrics may be `approx` or `skipped`. Always check the `status` field.

### Caching

Results are cached by `data_hash`. Repeat calls with unchanged beads.jsonl return instantly.

---

## jq Quick Reference

```bash
# At-a-glance summary
bv --robot-triage | jq '.quick_ref'

# Top recommendation
bv --robot-triage | jq '.recommendations[0]'

# Best unblock target
bv --robot-plan | jq '.plan.summary.highest_impact'

# Check metric readiness
bv --robot-insights | jq '.status'

# Find circular dependencies (MUST FIX!)
bv --robot-insights | jq '.Cycles'

# Critical labels needing attention
bv --robot-label-health | jq '.results.labels[] | select(.health_level == "critical")'

# All bottleneck issues
bv --robot-insights | jq '.bottlenecks'
```

---

## Response Shapes

### Triage Response

```json
{
  "quick_ref": {
    "total_open": 42,
    "actionable": 15,
    "blocked": 12,
    "top_picks": ["BV-123", "BV-456", "BV-789"]
  },
  "recommendations": [
    {
      "id": "BV-123",
      "title": "Refactor auth module",
      "score": 0.85,
      "reasons": ["High PageRank", "Unblocks 5 tasks"],
      "unblocks": ["BV-200", "BV-201", "BV-202", "BV-203", "BV-204"]
    }
  ],
  "quick_wins": [...],
  "blockers_to_clear": [...],
  "project_health": {
    "status_distribution": {...},
    "priority_distribution": {...},
    "graph_density": 0.045,
    "cycle_count": 0
  },
  "commands": {
    "claim_top": "bd update BV-123 --status in_progress"
  },
  "data_hash": "abc123...",
  "status": {...}
}
```

### Plan Response

```json
{
  "plan": {
    "tracks": [
      {
        "track_id": "track-A",
        "reason": "Auth system dependency chain",
        "items": [
          { "id": "AUTH-001", "priority": 1, "unblocks": ["AUTH-002", "AUTH-003"] }
        ]
      }
    ],
    "summary": {
      "total_actionable": 8,
      "total_blocked": 12,
      "highest_impact": "AUTH-001",
      "impact_reason": "Unblocks 3 tasks"
    }
  },
  "data_hash": "...",
  "status": {...}
}
```

### Insights Response

```json
{
  "bottlenecks": [{ "id": "CORE-123", "value": 0.45 }],
  "keystones": [{ "id": "API-001", "value": 12.0 }],
  "influencers": [{ "id": "AUTH-007", "value": 0.82 }],
  "hubs": [{ "id": "EPIC-100", "value": 0.67 }],
  "authorities": [{ "id": "UTIL-050", "value": 0.91 }],
  "cycles": [["TASK-A", "TASK-B", "TASK-A"]],
  "clusterDensity": 0.045,
  "stats": {
    "pageRank": {...},
    "betweenness": {...},
    "eigenvector": {...},
    "hubs": {...},
    "authorities": {...},
    "inDegree": {...},
    "outDegree": {...},
    "criticalPathScore": {...},
    "topologicalOrder": [...]
  },
  "status": {
    "pageRank": { "state": "computed", "elapsed_ms": 12 },
    "betweenness": { "state": "computed", "elapsed_ms": 45 },
    "cycles": { "state": "computed", "elapsed_ms": 8 }
  }
}
```

---

## Recipe System

BV ships with 11 pre-configured recipes for common workflows:

| Recipe | Purpose |
|--------|---------|
| `default` | All open issues sorted by priority |
| `actionable` | Ready to work (no blockers) |
| `recent` | Updated in last 7 days |
| `blocked` | Waiting on dependencies |
| `high-impact` | Top PageRank scores |
| `stale` | Open but untouched for 30+ days |
| `triage` | Sorted by computed triage score |
| `closed` | Recently closed issues |
| `release-cut` | Closed in last 14 days (for changelogs) |
| `quick-wins` | Easy P2/P3 items with no blockers |
| `bottlenecks` | High betweenness nodes |

```bash
bv --recipe actionable --robot-plan
bv --recipe high-impact --robot-triage
bv --recipe bottlenecks --robot-insights
```

---

## Hybrid Semantic Search

BV supports text + graph metric hybrid search:

```bash
# Default text-only search
bv --search "login oauth"

# Hybrid mode with preset
bv --search "login oauth" --search-mode hybrid --search-preset impact-first

# Custom weights
bv --search "login oauth" --search-mode hybrid \
  --search-weights '{"text":0.4,"pagerank":0.2,"status":0.15,"impact":0.1,"priority":0.1,"recency":0.05}'

# Robot JSON output
bv --search "login oauth" --search-mode hybrid --robot-search
```

**Presets:** `default`, `bug-hunting`, `sprint-planning`, `impact-first`, `text-only`

**Environment defaults:**
- `BV_SEARCH_MODE` (text|hybrid)
- `BV_SEARCH_PRESET`
- `BV_SEARCH_WEIGHTS` (JSON string)

---

## Time-Travel: Snapshot Diffing

Compare project state across git history:

```bash
# View state at any git reference
bv --as-of HEAD~10
bv --as-of v1.0.0
bv --as-of "2024-01-15"
bv --as-of abc1234  # commit SHA

# Diff changes
bv --robot-diff --diff-since HEAD~10
bv --robot-diff --diff-since v1.0.0
```

**What gets tracked:**
- Issues: New, Closed, Reopened, Removed, Modified
- Fields: Title, Status, Priority, Tags, Dependencies
- Graph: New Cycles, Resolved Cycles
- Metrics: Δ PageRank, Δ Betweenness, Δ Density

---

## History View: Git Correlation

BV correlates beads with commits using multiple strategies:

| Strategy | Weight | How It Works |
|----------|--------|--------------|
| **Explicit Mentions** | 0.5 | Commit message contains bead ID |
| **Temporal Proximity** | 0.25 | Commit during bead's active lifecycle |
| **Co-Commit Analysis** | 0.15 | Files frequently modified together |
| **Path Matching** | 0.10 | File paths match bead's label scope |

```bash
# Full history report
bv --robot-history

# Single bead focus
bv --robot-history --bead-history BV-123

# Filter by confidence
bv --robot-history --min-confidence 0.7

# Time range
bv --robot-history --history-since "30 days ago"
```

---

## Interactive HTML Graph

Generate self-contained HTML visualizations:

```bash
bv --export-graph graph.html
bv --export-graph --graph-title "Q4 Sprint"
bv --export-graph --graph-include-closed
```

**Features:**
- Force-directed layout (pan, zoom, filter)
- Node size by PageRank/betweenness/critical-path
- Color by status (Open=green, Blocked=red, etc.)
- Full-text search
- Path finder (click two nodes to find shortest path)
- Docked/floating detail panel
- Light/dark mode
- Works offline, no server required

**Keyboard shortcuts:** `?` help, `F` fit all, `R` reset, `L` toggle light/dark, `P` path finder

---

## TUI Features (for Humans)

Launch with bare `bv`:

### Views

| Key | View | Description |
|-----|------|-------------|
| (default) | List | Split-view with list + details |
| `b` | Kanban Board | Columnar workflow view |
| `g` | Graph | ASCII/Unicode dependency visualization |
| `i` | Insights | 6-panel metrics dashboard |
| `h` | History | Git correlation timeline |

### Navigation

| Key | Action |
|-----|--------|
| `j/k` | Navigate up/down |
| `h/l` | Navigate left/right (in board/graph) |
| `Enter` | Open in $EDITOR |
| `Space` | Full-screen detail |
| `/` | Search |
| `Tab` | Cycle panels |
| `?` | Help |
| `q` | Quit |

### Filtering

| Key | Filter |
|-----|--------|
| `o` | Open only |
| `c` | Closed only |
| `r` | Ready (unblocked) |
| `F3` | By label |
| `F5/F6` | By time |

### Actions

| Key | Action |
|-----|--------|
| `E` | Export to Markdown |
| `C` | Copy issue as Markdown |
| `t` | Time-travel (compare to git ref) |
| `p` | Toggle priority hints overlay |
| `s` | Cycle sort mode |

---

## Composite Impact Scoring

BV computes multi-factor impact scores:

```
Impact = 0.30×PageRank + 0.30×Betweenness + 0.20×BlockerRatio + 0.10×Staleness + 0.10×PriorityBoost
```

When computed impact diverges from human-assigned priority, BV flags misalignment:

> ⚠️ **CORE-123** has Impact Score 0.85 but Priority P3.
> *Reason: High PageRank (foundational dependency) + High Betweenness (bottleneck)*
> **Recommendation:** Consider escalating to P1.

---

## Baseline & Drift Detection

```bash
# Check drift from baseline
bv --check-drift
# Exit codes: 0=OK, 1=critical, 2=warning

# Get baseline info
bv --baseline-info
```

Use `--check-drift` in CI/CD to catch quality regressions.

---

## Automation Hooks

Configure pre/post-export hooks in `.bv/hooks.yaml`:

```yaml
pre_export:
  - command: "validate-issues.sh"
    on_error: fail
post_export:
  - command: "notify-slack.sh"
    on_error: continue
    env:
      CHANNEL: "#dev"
```

Hook environment includes: `BV_EXPORT_PATH`, `BV_EXPORT_FORMAT`, `BV_ISSUE_COUNT`, `BV_TIMESTAMP`

---

## Performance Characteristics

| Operation | Latency |
|-----------|---------|
| Phase 1 metrics | Instant |
| Phase 2 metrics (<500 nodes) | <500ms |
| Phase 2 metrics (large graphs) | May timeout/approx |
| Cached repeat calls | Instant (by data_hash) |

Use `bv --profile-startup` for diagnostics.

---

## Integration with bd (Beads CLI)

BV reads from `.beads/beads.jsonl` created by `bd`:

```bash
# Initialize beads
bd init

# Create issues
bd create "Implement login" -t feature -p 1

# Update status
bd update BV-123 --status in_progress

# Close
bd close BV-123 --reason "Completed"
```

**Important:** `.beads/` is authoritative state. Always commit it with code changes.

---

## Ready-to-Paste AGENTS.md Blurb

```
## bv - Beads Viewer (Graph-Aware Triage Engine)

bv is a graph-aware triage engine for Beads projects (.beads/beads.jsonl). Instead of parsing JSONL or hallucinating graph traversal, use robot flags for deterministic, dependency-aware outputs with precomputed metrics (PageRank, betweenness, HITS, eigenvector, critical path, cycles, k-core).

**⚠️ CRITICAL: Use ONLY `--robot-*` flags. Bare `bv` launches an interactive TUI that blocks your session.**

### The Workflow: Start With Triage
bv --robot-triage        # THE MEGA-COMMAND: start here
bv --robot-next          # Minimal: just the single top pick

### Key Commands
| Command | Returns |
|---------|---------|
| `--robot-triage` | Ranked recommendations, quick wins, blockers to clear |
| `--robot-plan` | Parallel execution tracks with unblocks lists |
| `--robot-insights` | Full metrics: PageRank, betweenness, cycles |
| `--robot-label-health` | Per-label health (healthy\|warning\|critical) |

### jq Quick Reference
bv --robot-triage | jq '.recommendations[0]'   # Top pick
bv --robot-plan | jq '.plan.summary'           # Best unblock target
bv --robot-insights | jq '.Cycles'             # Circular deps (MUST FIX!)

**Performance:** Phase 1 instant, Phase 2 async (500ms timeout). Results cached by data_hash.
```

---

## Installation

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/beads_viewer/main/install.sh?$(date +%s)" | bash
```
