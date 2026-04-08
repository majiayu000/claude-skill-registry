---
name: roadmap
description: >
  Synthesize project documentation and codebase into comprehensive roadmap status, gaps analysis,
  and blockers. Use when assessing project health, identifying blockers, tracking progress,
  comparing plan vs reality, documenting risks, or planning next milestones.
  Triggers: "roadmap", "project status", "blockers", "risks", "progress", "next milestone",
  "gaps", "what's done".
argument-hint: "[--deep] status | gaps | next | delta | blockers | risks | update [--incremental] | specs | plan [scaffold|show|sync]"
allowed-tools: Read, Glob, Grep, Write, Bash
---

# Roadmap Analyst

Synthesize project documentation and codebase state into actionable status reports.

## Context Discovery

Run the shared context discovery protocol in [CONTEXT_DISCOVERY.md](../../references/CONTEXT_DISCOVERY.md). Execute all phases in order (use thorough scan mode for Phase 7). Store results for analysis below.

## Arguments

Parse from `$ARGUMENTS`:

| Mode | Description |
|------|-------------|
| `status` | Overall dashboard — modules, phases, completion |
| `gaps` | Gap analysis status — open/closed/in-progress |
| `next` | Prioritized next actions |
| `delta` | What changed since last assessment |
| `blockers` | Blocking chain analysis |
| `risks` | Risk register with likelihood/impact |
| `update` | Git-history-aware status document update (Phase A: what shipped + Phase B: full scan). Add `--incremental` for targeted post-sprint sync (Phase A + targeted edits only) |
| `specs` | Spec pipeline status verification |
| `plan` | Consolidated project plan — scaffold, show, or sync phases/specs/ADRs |
| _(none)_ | Full dashboard (combines status + gaps + next) |

## Module Maturity Scale

Rate each module using the shared vocabulary in [MATURITY_SCALE.md](../../references/MATURITY_SCALE.md).

## Mode Execution

### `status`

Produce a status dashboard:

| Module | Backend | Frontend | Maturity |
|--------|---------|----------|----------|

Then detail: What's working, What's planned, What's missing.

After producing the dashboard, check for documentation drift:

1. Find last modification of `{status_file}` via git: `git log -1 --format="%H %ai" -- {status_file}`
2. Count feature/fix commits since: `git log {hash}..HEAD --oneline --no-merges | grep -cE "^[a-f0-9]+ (feat|fix):"`
3. If 3 or more feat/fix commits exist since last update, append a notice at the end of the output:

```
⚠️  Documentation may be stale: {N} feature/fix commits since last status update ({date}).
Run `/roadmap update` to sync.
```

### `gaps`

Cross-reference all gap analysis documents. For each gap: original report, current status (Open/In Progress/Closed), evidence of closure.

### `next`

Prioritized recommendations combining: unclosed gaps, unstarted specs, module maturity imbalances, frontend-backend parity gaps.

### `delta`

Compare the status document against current codebase state. Highlight: new files/modules, closed gaps, new issues, migration count changes.

### `blockers`

Trace blocking chains. For each blocker: what it blocks, who owns it, what's needed to unblock.

### `risks`

Risk register:

| Risk | Likelihood | Impact | Score | Mitigation |
|------|-----------|--------|-------|------------|

### `update`

Generate an updated status document with git-history awareness. Two phases:

#### Phase A: Git History Scan

Before the codebase scan, analyze what changed since the last doc update:

1. Find last modification of `{status_file}`: `git log -1 --format="%H %ai" -- {status_file}`
2. If no previous commit found, skip Phase A (first-time setup — Phase B handles it)
3. List commits since: `git log {hash}..HEAD --oneline --no-merges`
4. Group by PR number (parse `(#NN)` from commit messages) and commit type (`feat:`, `fix:`, `docs:`, etc.)
5. For each feature/fix group, summarize:
   - Scope (new components, routes, hooks, test files — inferred from file paths in the diff)
   - Related specs (cross-reference `arkhe/specs/` changes in the commit range)
   - Related ADRs (new files in `docs/adr/` in the commit range)
6. Present a **"What Shipped"** summary to the user before proceeding to the full scan:

```
## What Shipped Since Last Update (2026-03-09, 10 commits ago)

1. Glossary Management + Dictionary Browser (PR #32, specs 022-025)
   - 6 components, 2 hooks, 5 test files, /dictionary route
2. App Header Unification (PR #33)
   - Refactored navigation components
3. skrebe.app Redirect (1aff903, ADR-0010)
   - New middleware + DNS config
```

This context feeds into Phase B so the codebase scan knows what to look for and can produce more accurate updates.

#### Phase B: Full Codebase Scan + Write (existing behavior, enhanced)

1. Run full context discovery + codebase scan (same as before)
2. Read existing status document
3. Preserve format and structure
4. Update all data points — now informed by the git history from Phase A:
   - Module maturity ratings
   - Phase completion entries (Phase A identifies which phases completed)
   - Spec pipeline entries (Phase A identifies which specs shipped)
   - ADR table entries (Phase A identifies new ADRs)
   - Test coverage section
   - Commit count and date
   - Risk register (close risks for shipped features)
5. Show diff preview and ask for confirmation
6. Write updated file to `{status_file}`
7. Also check CHANGELOG.md — if `[Unreleased]` is missing entries for shipped features from Phase A, suggest adding them after the status update is applied (don't auto-write CHANGELOG without explicit confirmation)
8. Report changes made

### `specs`

Spec pipeline verification:

| Spec | Title | Status | Evidence |
|------|-------|--------|----------|

Verify status against codebase, not just what the spec says.

### `plan`

Consolidated project plan — lifecycle management from scaffold to sync.

Read `plan_file` from `.arkhe.yaml` `roadmap:` section (default: `docs/PROJECT-PLAN.md`).

Parse subcommand from remaining arguments:

| Subcommand | Description |
|------------|-------------|
| `scaffold` | Create initial PROJECT-PLAN.md from existing project state |
| `show` | Display current plan as a consolidated view (read-only) |
| `sync` | Update plan document from current codebase + git state |
| _(none)_ | Default to `show` if plan doc exists; `scaffold` if it doesn't |

#### `plan scaffold`

Create the initial plan document by consolidating scattered planning artifacts.

1. **Context discovery** — run standard protocol (CONTEXT_DISCOVERY.md)
2. **Read existing docs** — read `{status_file}`, product roadmaps (`docs/**/roadmap.md`), backlogs (`docs/**/backlog.md`)
3. **Scan specs** — glob `{specs_dir}/*/spec.md`, extract: spec ID (directory name), title (first `#` heading), status (`Status:` field)
4. **Scan ADRs** — glob `docs/adr/[0-9]*.md`, extract: number (filename), title (first `#` heading), status
5. **Auto-detect phase mappings** — run the hybrid linking algorithm (see [WORKFLOW.md](WORKFLOW.md) § Hybrid Linking Algorithm)
6. **Present proposed plan** — show full document in chat with `[AUTO-LINKED]` markers on detected mappings, `[MANUAL]` on explicit matches, `[UNLINKED]` on unmapped items
7. **Confirm** — ask user to review linkages and approve; apply corrections
8. **Write** — write to `{plan_file}`

If `{plan_file}` already exists, warn and offer: overwrite, sync instead, or cancel.

#### `plan show`

Read-only consolidated view.

1. Read `{plan_file}` — if missing, suggest `scaffold`
2. Parse and present summary: timeline table, progress stats (phases done/total, specs linked/total, ADRs linked/total), active phases, next up
3. **Drift detection**: if plan doc was last committed >7 days ago and 3+ feat/fix commits exist since, append: `"⚠️ Plan may be stale. Run /roadmap plan sync to update."`

#### `plan sync`

Git-aware update of the plan document — follows the `update` mode's Phase A + Phase B pattern.

1. **Phase A: Git History Scan** — detect since last plan sync: new/modified specs, new ADRs, phase completion signals (feat: commits grouped by PR), backlog changes
2. **Phase B: Auto-detect new links** — run hybrid linking on any new specs/ADRs from Phase A
3. **Phase C: Diff and confirm** — show proposed changes as `+`/`-`/`~` markers; ask confirmation
4. **Phase D: Write** — update `{plan_file}` preserving user-edited sections

See [WORKFLOW.md](WORKFLOW.md) § `plan` for detailed execution protocol.

## Output Rules

- **Evidence-based** — every claim backed by a file path, migration, or component
- **Tabular** — use tables for at-a-glance status; prose for analysis
- **Actionable** — always end with recommended next actions
- **Honest** — distinguish between "verified working" and "files exist but untested"
- `update` and `plan scaffold`/`plan sync` show unified diff preview (using `+`/`-`/`~` markers) and require explicit confirmation before writing
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
