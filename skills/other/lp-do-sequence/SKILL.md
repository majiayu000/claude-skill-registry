---
name: lp-do-sequence
description: Topologically sort plan tasks into correct implementation order, preserve stable task IDs by default, and add explicit dependency/blocker metadata to enable parallel subagent execution.
---

# Sequence Plan

Analyze an existing plan's tasks, determine correct implementation order based on dependencies and file overlap, preserve task IDs by default, and add explicit blocking relationships so `/lp-do-build` can dispatch parallel subagents safely.

## Operating Mode

**PLAN EDITING ONLY**

**Allowed:** read plan files, read source files listed in `Affects` to verify overlap, edit the plan document (task ordering, numbering, dependency fields, summary table, parallelism guide).

**Not allowed:** implementation code changes, creating new tasks, changing task scope/acceptance/confidence, deleting tasks.

## When to Use

Run `/lp-do-sequence` when:

- A plan has been created or updated via `/lp-do-plan` and tasks need correct execution ordering
- Tasks were added in phases/batches and the implementation order isn't optimized
- You want to enable parallel subagent execution for `/lp-do-build` by making blocking relationships explicit
- A `/lp-do-replan` added or removed tasks and the numbering/dependencies need cleanup
- Planning or replanning decomposed tasks: run this after all structural edits and before build handoff/resume

Do **not** use `/lp-do-sequence` if:

- The plan doesn't exist yet -> use `/lp-do-plan`
- Tasks need scope/confidence changes -> use `/lp-do-replan`
- You want to build tasks -> use `/lp-do-build`

## Fast Path (with argument)

**If user provides a slug** (e.g., `/lp-do-sequence design-system`):
- Read `docs/plans/<slug>/plan.md` directly (legacy fallback: `docs/plans/<slug>-plan.md`)
- Skip discovery

## Discovery Path (no argument)

If no argument provided, scan for Active plans in this order and present a table:

1. Canonical: `docs/plans/*/plan.md`
2. Legacy fallback (read-only compatibility): `docs/plans/*-plan.md`

```markdown
## Plans Available for Sequencing

| Slug | Title | Task Count | Status |
|------|-------|------------|--------|
| design-system | Design System Plan | 24 | Active |

Enter a slug to sequence.
```

## Inputs

- The plan doc: `docs/plans/<feature-slug>/plan.md` (legacy fallback: `docs/plans/<feature-slug>-plan.md`)
- Source files referenced in `Affects` fields (read-only, for overlap analysis)

## Outputs

- Updated plan doc with tasks reordered, stable IDs preserved, `Depends on`/`Blocks` updated, Task Summary table updated, Parallelism Guide added.

## ID Policy

- **Default:** preserve existing TASK-IDs (stable IDs).
- **Optional:** renumber only when user explicitly requests it.
- Dependencies and references target stable IDs to avoid breaking build logs, confidence notes, and checkpoint chains.

## Workflow

### Step 1: Parse Tasks

Read the plan and extract every task (skip completed, deferred, and superseded tasks). For each task, capture:

- **Current ID** (e.g., `DS-30`, `TASK-05`)
- **Type** (IMPLEMENT, SPIKE, INVESTIGATE, DECISION, CHECKPOINT)
- **Explicit dependencies** (`Depends on` field — task IDs)
- **Affects** (file paths — both primary and `[readonly]`)
- **Phase** (if tasks are organized by phase)
- **Effort** (S, M, L)
- **Status** (Pending, In-Progress, Blocked, etc.)

### Steps 2–6: Dependency Graph, Sort, and Parallel Groups

Load `modules/seq-algorithm.md`. Run all algorithm steps:
- Step 2: Build Dependency Graph (explicit, file-overlap, phase ordering)
- Step 3: Topological Sort (Kahn's algorithm / DFS; detect cycles → STOP if found)
- Step 4: ID Handling (stable by default; rename map if requested)
- Step 5: Update Dependencies and Add Blockers
- Step 6: Identify Parallel Execution Groups → Parallelism Guide

### Steps 7–9 + Edge Cases: Plan Update, Validation, Completion

Load `modules/seq-plan-update.md`. Apply all plan edits:
- Step 7: Update plan document (summary table, task sections, phase headers, Parallelism Guide)
- Step 8: Validate (no orphan references, no cycles, completed tasks untouched)
- Step 9: Completion Summary
- Edge cases: completed tasks, deferred tasks, in-progress tasks, range dependencies

## Quality Checks

- [ ] Stable IDs preserved (or explicit renumber mode was requested and applied consistently)
- [ ] No orphaned task references in active sections
- [ ] Every `Depends on` reference points to a valid task ID
- [ ] Every `Blocks` field is the correct inverse of `Depends on`
- [ ] No circular dependencies exist
- [ ] File-overlap dependencies identified and documented
- [ ] Parallelism Guide correctly groups non-conflicting tasks into waves
- [ ] Completed and deferred tasks are untouched
- [ ] Task Summary table matches the new ordering

## Completion Messages

**Success:**
> "Plan sequenced. N tasks reordered into K execution waves (max parallelism: P). Critical path: W waves. Stable IDs preserved (or explicit renumber map applied). Ready for `/lp-do-build`."

**Cycle detected:**
> "Cannot sequence — circular dependency detected between TASK-A and TASK-B. Run `/lp-do-replan` to resolve the cycle before sequencing."

**No changes needed:**
> "Plan is already correctly sequenced. No reordering required."

## Notes

`/lp-do-sequence` is a **supporting utility** — it is invoked automatically by `/lp-do-plan` and `/lp-do-replan` after structural edits. You can also invoke it standalone whenever you need to refresh task ordering without changing scope or confidence.
