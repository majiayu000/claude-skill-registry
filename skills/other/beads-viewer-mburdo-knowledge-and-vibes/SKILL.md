---
name: beads-viewer
description: Graph analysis with bv (Beads Viewer). Use when analyzing the task graph, finding blockers, getting recommendations, checking critical path, or when the user mentions "bv", "graph", "dependencies", or "what should I work on".
---

# Beads Viewer (bv)

Graph analysis layer for the Beads task graph. Precomputes metrics like PageRank and critical path.

## When This Applies

| Signal | Action |
|--------|--------|
| "What should I work on?" | `bv --robot-triage` |
| Need single best task | `bv --robot-next` |
| Multi-agent partitioning | `bv --robot-triage --robot-triage-by-track` |
| Risk/hygiene check | `bv --robot-alerts` |
| Finding blockers | `bv --robot-blocker-chain` |

---

## CRITICAL RULE

**Always use `--robot-*` flags. Never run bare `bv`.**

Bare `bv` launches a TUI that will hang AI agents.

---

## Session Kickoff

```bash
# Default (fast)
bv --robot-next                    # Single best next task

# Full triage bundle
bv --robot-triage                  # Blockers, quick wins, commands
```

---

## Multi-Agent Partitioning

```bash
# Split work by parallel tracks
bv --robot-triage --robot-triage-by-track

# Track details + what each task unblocks
bv --robot-plan
```

---

## Risk & Hygiene

Use before starting "big" work:

```bash
bv --robot-alerts                  # Stale issues, blocking cascades, drift
bv --robot-suggest                 # Duplicates, missing deps, cycle breaks
```

---

## Debugging & Analysis

```bash
# What changed recently?
bv --robot-diff --diff-since HEAD~5

# Historical state
bv --as-of HEAD~10 --robot-triage

# Blocker analysis
bv --robot-blocker-chain bd-123

# Impact analysis before refactor
bv --robot-impact path/to/file1,path/to/file2
bv --robot-file-relations path/to/core_file
```

---

## Handoff / Audit Trail

```bash
bv --robot-history --bead-history bd-123
```

---

## Semantic Search

```bash
bv --search "your query" --robot-search
```

---

## Graph Metrics Explained

| Metric | Meaning | Use For |
|--------|---------|---------|
| **PageRank** | Foundational blockers | Tasks that enable many others |
| **Betweenness** | Bottlenecks | Must pass through these |
| **Critical Path** | Longest dependency chain | Overall timeline |

---

## Keeping bv Current

```bash
bv --check-update && bv --update --yes
```

---

## Quick Reference

```bash
bv --robot-next              # Single best task (fast)
bv --robot-triage            # Full recommendations
bv --robot-triage --robot-triage-by-track   # Multi-agent
bv --robot-plan              # Execution order
bv --robot-alerts            # Risk signals
bv --robot-suggest           # Hygiene suggestions
bv --robot-blocker-chain ID  # Why is this blocked?
```

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Run bare `bv` | Launches TUI, hangs agent |
| Ignore `--robot-alerts` | Miss stale/risky work |
| Skip before big work | Miss blocking cascades |

---

## See Also

- `beads-cli/` — Task management with `bd`
- `advance/` — Full bead lifecycle (claiming, working, closing)
