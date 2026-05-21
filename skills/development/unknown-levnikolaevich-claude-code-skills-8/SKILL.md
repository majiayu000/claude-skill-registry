---
name: ln-022-researchgraph
description: "Indexes and queries project research graphs backed by hex-research MCP. Use for hypotheses, goals, benchmark runs, evidence depth, derived goal metrics, lineage, generated research maps, and graph audits."
license: MIT
allowed-tools: Read, Grep, Glob, Bash, mcp__hex-research__verify_index, mcp__hex-research__index_hypotheses, mcp__hex-research__find_hypotheses, mcp__hex-research__inspect_hypothesis, mcp__hex-research__find_evidence, mcp__hex-research__find_runs, mcp__hex-research__trace_lineage, mcp__hex-research__analyze_topology, mcp__hex-research__audit_orphans, mcp__hex-research__inspect_goal, mcp__hex-research__trace_goal_tree, mcp__hex-research__audit_goal_alignment, mcp__hex-research__analyze_progress, mcp__hex-research__analyze_proposed, mcp__hex-research__export_canvas, mcp__hex-research__export_research_map
---

> **Paths:** File paths are relative to this skill directory.

# Research Graph

**Type:** Standalone Utility
**Category:** 0XX Dev Environment

Indexes and queries canonical project research files through `hex-research-mcp`: hypotheses, goals, tasks, sources, source library entries, benchmark run manifests, evidence links, derived goal metrics, lineage, generated research maps, and audit gaps.

## Mandatory Read

**MANDATORY READ:** Load `references/researchgraph_mcp_usage.md`

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `project_path` | yes | args or CWD | Project root containing research graph files |
| `command` | no | args | Specific action: `audit`, `inspect H##`, `goal G##`, `runs`, `evidence`, `lineage`, `progress`, `proposed`, `canvas` |

## When to Use

Use this skill when the project has any of:
- `docs/hypotheses/*.md`
- `docs/goals/*.md`
- `benchmark/runs/*/manifest.yaml`

Use it when the user asks about research status, live or pending hypotheses, goal readiness, benchmark evidence, source quality, evidence depth, proposal readiness, implementation gaps, drift, field-level changes, or a visual/generated research map.

Do not use this skill for code symbol ownership, call graphs, references, or edit blast radius. Use `ln-021-codegraph` or host `hex-graph` policy for semantic code questions.

## MCP Availability

Use `hex-research` when available. If unavailable, manually read the split research files with `Glob/Grep/Read`, answer from direct file evidence, and mark confidence as degraded.

Treat `STALE` as actionable graph debt or missing project metadata, not as a tool failure. Treat `INVALID` from `verify_index` as diagnostic unless a write/index operation fails.

## Workflow

### Phase 1: Detect Graph Layout

Check for the canonical layout:
- `docs/hypotheses/*.md`
- `docs/goals/*.md`
- `benchmark/runs/*/manifest.yaml`

If none exist, stop and report that the project does not expose a research graph yet. Do not invent hypotheses or goals.

### Phase 2: Verify or Index

Start read-only:
```
verify_index({ path: "{project_path}" })
```

Rebuild only when the index is missing, stale, explicitly requested, or the task requires current graph state:
```
index_hypotheses({ path: "{project_path}" })
```

The local index is stored under `.hex-skills/researchgraph/` in the target project.

### Phase 3: Route Intent

| User intent | Tool |
|-------------|------|
| live, pending, rejected, mixed, not-started hypotheses | `find_hypotheses` |
| inspect `H##` | `inspect_hypothesis` |
| inspect `G##` or goal status | `inspect_goal` |
| evidence, sources, benchmark proof | `find_evidence` |
| targeted or comprehensive benchmark runs | `find_runs` |
| parent/child hypothesis chain | `trace_lineage` |
| graph hubs, disconnected nodes, shape | `analyze_topology` |
| missing goals, sources, task gaps, drift | `audit_orphans` |
| goal tree | `trace_goal_tree` |
| goal readiness, derived metrics, and metric coverage | `inspect_goal`, `audit_goal_alignment` |
| source quality or evidence depth | `inspect_hypothesis`, `find_evidence`, `analyze_proposed` |
| changed research files and field-level deltas in current diff | `analyze_progress` |
| readiness of proposed next hypotheses | `analyze_proposed` |
| JSON Canvas export | `export_canvas` |
| generated `docs/research-map.md` export | `export_research_map` |

### Phase 4: Present Results

Report:
1. tool status (`OK`, `STALE`, `INVALID`, `ERROR`)
2. key hypotheses/goals/runs with IDs
3. actionable graph debt separately from tool failures
4. follow-up tool calls when the graph points to a narrower next question

For `export_canvas` and `export_research_map`, run dry-run first. Write only after dry-run output is useful and the user requested the file. Treat split files as canonical; generated `research-map.md` is not a second manual source of truth.

## Manual Fallback

When MCP is unavailable:
1. Read `docs/goals/*.md` and `docs/hypotheses/*.md` frontmatter first.
2. Read `benchmark/runs/*/manifest.yaml` only after narrowing by H/G IDs or status.
3. Prefer exact IDs (`H04`, `G1`) over broad scans.
4. State that lineage, topology, and drift findings are manual approximations.

## Definition of Done

- [ ] Graph layout detected or absence reported
- [ ] Index verified or rebuilt when needed
- [ ] User intent routed to the smallest relevant tool
- [ ] `STALE` / graph debt separated from MCP/tool failure
- [ ] Manual fallback confidence stated when MCP was unavailable
- [ ] Canvas writes use dry-run before write

---
**Version:** 0.1.0
**Last Updated:** 2026-05-08
