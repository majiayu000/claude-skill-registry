---
name: roadmap
description: >
  Synthesize project documentation and codebase into comprehensive roadmap status, gaps analysis,
  and blockers. Use when assessing project health, identifying blockers, tracking progress,
  comparing plan vs reality, documenting risks, or planning next milestones.
  Triggers: "roadmap", "project status", "blockers", "risks", "progress", "next milestone",
  "gaps", "what's done".
argument-hint: "[--deep] status | gaps | next [--force] | delta | blockers | risks | update [--incremental] | specs | plan [scaffold|show|sync]"
allowed-tools: Read, Glob, Grep, Write, Bash
---

# Roadmap Analyst

Synthesize project documentation and codebase state into actionable status reports.

## Context Discovery

Run the shared context discovery protocol in [CONTEXT_DISCOVERY.md](../../references/CONTEXT_DISCOVERY.md). Use the scan depth appropriate for the mode:

| Mode | Required Phases | Scan Depth |
|------|----------------|------------|
| `plan show` | 1 (config) | None — reads `{plan_file}` directly |
| `specs` | 1, 5 | Light — config + doc scan for spec files |
| `gaps` | 1, 3, 5 | Light — config, rich context, docs |
| `delta` | 1, 5, 7 | Medium — config, docs, codebase scan |
| `next` (cached) | 1 (config) | None — reads cached file + git drift check |
| `next` (recalc) | 1-7 | Thorough — full protocol |
| `status`, `blockers`, `risks` | 1-7 | Thorough — full protocol |
| `update`, `update --incremental` | 1-7 | Thorough — full protocol |
| `plan scaffold`, `plan sync` | 1-7 | Thorough — full protocol |

Store results for analysis below.

## Arguments

Parse from `$ARGUMENTS`:

| Mode | Description |
|------|-------------|
| `status` | Overall dashboard — modules, phases, completion + drift detection |
| `gaps` | Gap analysis status — open/closed/in-progress with evidence |
| `next` | Prioritized recommendations with caching and smart merge. Saves to `{output_dir}/next-actions.md`. Returns cached results if <3 feat/fix commits and status doc unchanged; otherwise merge-based recalculation that preserves uncompleted items and user additions. Add `--force` to recalculate (still merges; delete file manually for clean slate) |
| `delta` | What changed since last assessment (read-only comparison) |
| `blockers` | Blocking chain analysis with critical path |
| `risks` | Risk register with likelihood/impact scoring |
| `update` | Git-aware status doc update (Phase A: what shipped + Phase B: full scan + auto-chains `plan sync`). Add `--incremental` for post-sprint targeted edits only |
| `specs` | Spec pipeline verification against codebase. Cross-references `{plan_file}` for phase linkage if available |
| `plan` | Project plan lifecycle — `scaffold` (create), `show` (read), `sync` (update). Defaults to `show` if plan exists, `scaffold` if not |
| _(none)_ | Full dashboard (combines status + gaps + next) |

## Module Maturity Scale

Rate each module using the shared vocabulary in [MATURITY_SCALE.md](../../references/MATURITY_SCALE.md).

## Mode Execution

### `status`

Produce a status dashboard with module maturity table, then detail: What's working, What's planned, What's missing.

After producing the dashboard, run drift detection: if 3+ feat/fix commits exist since last `{status_file}` update, append a staleness notice suggesting `/roadmap update`.

### `gaps`

Cross-reference all gap analysis documents. For each gap: original report, current status (Open/In Progress/Closed), evidence of closure.

### `next`

Prioritized recommendations with git-aware caching and smart merge. See [WORKFLOW.md](WORKFLOW.md) § `next` for the full merge protocol.

Key behaviors:
- Saves recommendations to `{output_dir}/next-actions.md`
- Returns cached results if <3 feat/fix commits and status doc unchanged since last calculation
- On recalculation, merges new recommendations with existing items — preserves uncompleted items, removes items with completion evidence
- User-added items in `### User-Added` section always preserved across recalculations
- Shows merge diff preview with `+`/`-`/`~`/`=` markers before writing (confirmation required)
- Combines: unclosed gaps, unstarted specs, maturity imbalances, plan backlog themes

### `delta`

Compare the status document against current codebase state. Highlight: new files/modules, closed gaps, new issues, migration count changes.

### `blockers`

Trace blocking chains. For each blocker: what it blocks, who owns it, what's needed to unblock. Identify critical path (longest chain).

### `risks`

Risk register with Likelihood (H/M/L) x Impact (H/M/L) scoring and suggested mitigations.

### `update`

Git-aware status document update. See [WORKFLOW.md](WORKFLOW.md) § `update` for the full Phase A (git history scan) + Phase B (codebase scan + write) protocol.

Key behaviors:
- Shows "What Shipped" summary before scanning
- Diff preview with `+`/`-`/`~` markers, requires confirmation before writing
- Checks CHANGELOG.md for gaps (offers to add entries)
- Auto-chains into `plan sync` when phase/spec status changes detected
- Next `/roadmap next` will detect status doc changes and trigger merge-based recalculation (preserves uncompleted items)
- `--incremental` variant: surgical targeted edits only (skips Phase B full scan)

### `specs`

Spec pipeline verification — verify status against codebase evidence, not just what the spec says. If `{plan_file}` exists, cross-reference to show which phase each spec belongs to and flag unlinked specs.

### `plan`

Consolidated project plan lifecycle. Read `plan_file` from `.arkhe.yaml` (default: `docs/PROJECT-PLAN.md`).

| Subcommand | Description |
|------------|-------------|
| `scaffold` | Create initial PROJECT-PLAN.md using hybrid linking algorithm — see [WORKFLOW.md](WORKFLOW.md) § `plan scaffold` |
| `show` | Read-only summary with timeline, progress stats, active phases, drift detection |
| `sync` | Git-aware update with auto-detected links — see [WORKFLOW.md](WORKFLOW.md) § `plan sync` |
| _(none)_ | Default to `show` if plan exists; `scaffold` if not |

## Output Rules

- **Evidence-based** — every claim backed by a file path, migration, or component
- **Tabular** — use tables for at-a-glance status; prose for analysis
- **Actionable** — always end with recommended next actions
- **Honest** — distinguish between "verified working" and "files exist but untested"
- `update` and `plan scaffold`/`plan sync` show unified diff preview and require explicit confirmation before writing
- `--deep` reports are saved by default to `{output_dir}/reports/`; user can opt out

## Deep Mode (`--deep`)

When `$ARGUMENTS` contains `--deep`, run the full multi-agent pipeline with **parallel cross-perspective analysis**. Three Sonnet agents analyze the project simultaneously from PM, Architect, and Roadmap perspectives, then a synthesizer merges findings and surfaces contradictions.

See [WORKFLOW.md](WORKFLOW.md) § Deep Pipeline for the 5-phase execution protocol.

Phase 4 produces a **Confidence Scoreboard** table with independent scores per finding. Findings below 70 are removed; 70-89 are tagged `[NEEDS VALIDATION]`.

**Patterns applied**: Pipeline, Supervisor-Worker, Parallel Execution, Confession, Confidence-Gated Completion.

## Lane Discipline

See the Roadmap Analyst section of [LANE_DISCIPLINE.md](../../references/LANE_DISCIPLINE.md). Stay in your lane.

## References

- [WORKFLOW.md](WORKFLOW.md) — Detailed discovery and mode workflows
- [EXAMPLES.md](EXAMPLES.md) — Usage examples
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues and fixes
