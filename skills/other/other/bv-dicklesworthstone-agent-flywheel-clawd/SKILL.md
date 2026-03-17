---
name: bv
description: "Beads Viewer - Graph-aware triage engine for Beads projects. Computes PageRank, betweenness, critical path, and cycles. Use --robot-* flags for AI agents."
---

# BV - Beads Viewer

A graph-aware triage engine for Beads projects (`.beads/beads.jsonl`). Computes 9 graph metrics, generates execution plans, and provides deterministic recommendations. Human TUI for browsing; robot flags for AI agents.

## Why BV vs Raw Beads

| Capability | Raw beads.jsonl | BV Robot Mode |
|------------|-----------------|---------------|
| Query | "List all issues" | "List the top 5 bottlenecks blocking the release" |
| Context Cost | High (linear with issue count) | Low (fixed summary struct) |
| Graph Logic | Agent must compute | Pre-computed (PageRank, betweenness, cycles) |
| Safety | Agent might miss cycles | Cycles explicitly flagged |

Use BV instead of parsing beads.jsonl directly. It computes graph metrics deterministically.

## CRITICAL: Robot Mode for Agents

**Never run bare `bv`**. It launches an interactive TUI that blocks your session.

Always use `--robot-*` flags:

```bash
bv --robot-triage        # THE MEGA-COMMAND: start here
bv --robot-next          # Minimal: just the single top pick
bv --robot-plan          # Parallel execution tracks
bv --robot-insights      # Full graph metrics
```

## The 9 Graph Metrics

BV computes these metrics to surface hidden project dynamics:

| Metric | What It Measures | Key Insight |
|--------|------------------|-------------|
| **PageRank** | Recursive dependency importance | Foundational blockers |
| **Betweenness** | Shortest-path traffic | Bottlenecks and bridges |
| **HITS** | Hub/Authority duality | Epics vs utilities |
| **Critical Path** | Longest dependency chain | Keystones with zero slack |
| **Eigenvector** | Influence via neighbors | Strategic dependencies |
| **Degree** | Direct connection counts | Immediate blockers/blocked |
| **Density** | Edge-to-node ratio | Project coupling health |
| **Cycles** | Circular dependencies | Structural errors (must fix!) |
| **Topo Sort** | Valid execution order | Work queue foundation |

## Two-Phase Analysis

BV uses async computation with timeouts:

- **Phase 1 (instant):** degree, topo sort, density
- **Phase 2 (500ms timeout):** PageRank, betweenness, HITS, eigenvector, cycles

Always check `status` field in output. For large graphs (>500 nodes), some metrics may be `approx` or `skipped`.

## Robot Commands Reference

### Triage & Planning

```bash
bv --robot-triage              # Full triage: recommendations, quick_wins, blockers_to_clear
bv --robot-next                # Single top pick with claim command
bv --robot-plan                # Parallel execution tracks with unblocks lists
bv --robot-priority            # Priority misalignment detection
```

### Graph Analysis

```bash
bv --robot-insights            # Full metrics: PageRank, betweenness, HITS, cycles, etc.
bv --robot-label-health        # Per-label health: healthy|warning|critical
bv --robot-label-flow          # Cross-label dependency flow matrix
bv --robot-label-attention     # Attention-ranked labels
```

### History & Changes

```bash
bv --robot-history             # Bead-to-commit correlations
bv --robot-diff --diff-since <ref>  # Changes since ref
```

### Other Commands

```bash
bv --robot-burndown <sprint>   # Sprint burndown, scope changes
bv --robot-forecast <id|all>   # ETA predictions
bv --robot-alerts              # Stale issues, blocking cascades
bv --robot-suggest             # Hygiene: duplicates, missing deps, cycle breaks
bv --robot-graph               # Dependency graph export (JSON, DOT, Mermaid)
bv --export-graph <file.html>  # Self-contained interactive HTML visualization
```

## Scoping & Filtering

```bash
bv --robot-plan --label backend              # Scope to label's subgraph
bv --robot-insights --as-of HEAD~30          # Historical point-in-time
bv --recipe actionable --robot-plan          # Pre-filter: ready to work
bv --recipe high-impact --robot-triage       # Pre-filter: top PageRank
bv --robot-triage --robot-triage-by-track    # Group by parallel work streams
bv --robot-triage --robot-triage-by-label    # Group by domain
```

## Built-in Recipes

| Recipe | Purpose |
|--------|---------|
| `default` | All open issues sorted by priority |
| `actionable` | Ready to work (no blockers) |
| `high-impact` | Top PageRank scores |
| `blocked` | Waiting on dependencies |
| `stale` | Open but untouched for 30+ days |
| `triage` | Sorted by computed triage score |
| `quick-wins` | Easy P2/P3 items with no blockers |
| `bottlenecks` | High betweenness nodes |

## Robot Output Structure

All robot JSON includes:
- `data_hash` - Fingerprint of beads.jsonl (verify consistency)
- `status` - Per-metric state: `computed|approx|timeout|skipped`
- `as_of` / `as_of_commit` - Present when using `--as-of`

### --robot-triage Output

```json
{
  "quick_ref": { "open": 45, "blocked": 12, "top_picks": [...] },
  "recommendations": [
    { "id": "bd-123", "score": 0.85, "reason": "Unblocks 5 tasks", "unblock_info": {...} }
  ],
  "quick_wins": [...],
  "blockers_to_clear": [...],
  "project_health": { "distributions": {...}, "graph_metrics": {...} },
  "commands": { "claim": "bd claim bd-123", "view": "bv --bead bd-123" }
}
```

### --robot-insights Output

```json
{
  "bottlenecks": [{ "id": "bd-123", "value": 0.45 }],
  "keystones": [{ "id": "bd-456", "value": 12.0 }],
  "influencers": [...],
  "hubs": [...],
  "authorities": [...],
  "cycles": [["bd-A", "bd-B", "bd-A"]],
  "clusterDensity": 0.045,
  "status": { "pagerank": "computed", "betweenness": "computed", ... }
}
```

## jq Quick Reference

```bash
bv --robot-triage | jq '.quick_ref'                        # At-a-glance summary
bv --robot-triage | jq '.recommendations[0]'               # Top recommendation
bv --robot-plan | jq '.plan.summary.highest_impact'        # Best unblock target
bv --robot-insights | jq '.status'                         # Check metric readiness
bv --robot-insights | jq '.cycles'                         # Circular deps (must fix!)
bv --robot-label-health | jq '.results.labels[] | select(.health_level == "critical")'
```

## Agent Workflow Pattern

```bash
# 1. Start with triage
TRIAGE=$(bv --robot-triage)
NEXT_TASK=$(echo "$TRIAGE" | jq -r '.recommendations[0].id')

# 2. Check for cycles first (structural errors)
CYCLES=$(bv --robot-insights | jq '.cycles')
if [ "$CYCLES" != "[]" ]; then
  echo "Fix cycles first: $CYCLES"
fi

# 3. Claim the task
bd claim "$NEXT_TASK"

# 4. Work on it...

# 5. Close when done
bd close "$NEXT_TASK"
```

## TUI Views (for Humans)

When running `bv` interactively (not for agents):

| Key | View |
|-----|------|
| `l` | List view (default) |
| `b` | Kanban board |
| `g` | Graph view (dependency DAG) |
| `E` | Tree view (parent-child hierarchy) |
| `i` | Insights dashboard (6-panel metrics) |
| `h` | History view (bead-to-commit correlation) |
| `a` | Actionable plan (parallel tracks) |
| `f` | Flow matrix (cross-label dependencies) |
| `]` | Attention view (label priority ranking) |

## Integration with bd CLI

BV reads from `.beads/beads.jsonl` created by the `bd` CLI:

```bash
bd init                    # Initialize beads in project
bd create "Task title"     # Create a bead
bd list                    # List beads
bd ready                   # Show actionable beads
bd claim bd-123            # Claim a bead
bd close bd-123            # Close a bead
```

## Integration with Agent Mail

Use bead IDs as thread IDs for coordination:

```
file_reservation_paths(..., reason="bd-123")
send_message(..., thread_id="bd-123", subject="[bd-123] Starting...")
```

## Graph Export Formats

```bash
bv --robot-graph                              # JSON (default)
bv --robot-graph --graph-format=dot           # Graphviz DOT
bv --robot-graph --graph-format=mermaid       # Mermaid diagram
bv --robot-graph --graph-root=bd-123 --graph-depth=3  # Subgraph
bv --export-graph report.html                 # Interactive HTML
```

## Time Travel

Compare against historical states:

```bash
bv --as-of HEAD~10                    # 10 commits ago
bv --as-of v1.0.0                     # At tag
bv --as-of "2024-01-15"               # At date
bv --robot-diff --diff-since HEAD~30  # Changes in last 30 commits
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| TUI blocks agent | Use `--robot-*` flags only |
| Stale metrics | Check `status` field, results cached by `data_hash` |
| Missing cycles | Run `--robot-insights`, check `.cycles` |
| Wrong recommendations | Use `--recipe actionable` to filter to ready work |

## Performance Notes

- Phase 1 metrics (degree, topo, density): instant
- Phase 2 metrics (PageRank, betweenness, etc.): 500ms timeout
- Results cached by `data_hash`
- Prefer `--robot-plan` over `--robot-insights` when speed matters
