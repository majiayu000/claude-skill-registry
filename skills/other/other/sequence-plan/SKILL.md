---
name: sequence-plan
description: Topologically sort plan tasks into correct implementation order, renumber sequentially, and add explicit dependency/blocker metadata to enable parallel subagent execution.
---

# Sequence Plan

Analyze an existing plan's tasks, determine correct implementation order based on dependencies and file overlap, renumber tasks sequentially, and add explicit blocking relationships so `/build-feature` can dispatch parallel subagents safely.

## Operating Mode

**PLAN EDITING ONLY**

**Allowed:** read plan files, read source files listed in `Affects` to verify overlap, edit the plan document (task ordering, numbering, dependency fields, summary table, parallelism guide).

**Not allowed:** implementation code changes, creating new tasks, changing task scope/acceptance/confidence, deleting tasks.

## When to Use

Run `/sequence-plan` when:

- A plan has been created or updated via `/plan-feature` and tasks need correct execution ordering
- Tasks were added in phases/batches and the implementation order isn't optimized
- You want to enable parallel subagent execution for `/build-feature` by making blocking relationships explicit
- A `/re-plan` added or removed tasks and the numbering/dependencies need cleanup
- Planning or re-planning decomposed tasks (split into precursor chains/subtasks): run this after all structural edits and before build handoff/resume

Do **not** use `/sequence-plan` if:

- The plan doesn't exist yet -> use `/plan-feature`
- Tasks need scope/confidence changes -> use `/re-plan`
- You want to build tasks -> use `/build-feature`

## Fast Path (with argument)

**If user provides a slug** (e.g., `/sequence-plan design-system`):
- Read `docs/plans/<slug>-plan.md` directly
- Skip discovery

## Discovery Path (no argument)

If no argument provided, scan `docs/plans/*-plan.md` for Active plans and present a table:

```markdown
## Plans Available for Sequencing

| Slug | Title | Task Count | Status |
|------|-------|------------|--------|
| design-system | Design System Plan | 24 | Active |

Enter a slug to sequence.
```

## Inputs

- The plan doc: `docs/plans/<feature-slug>-plan.md`
- Source files referenced in `Affects` fields (read-only, for overlap analysis)

## Outputs

- Updated plan doc with:
  - Tasks reordered and renumbered
  - `Depends on` fields updated with new task IDs
  - `Blocks` field added to each task (inverse of `Depends on`)
  - Task Summary table updated with new ordering
  - Parallelism Guide section added

## Workflow

### 1) Parse Tasks

Read the plan and extract every task (skip completed, deferred, and superseded tasks). For each task, capture:

- **Current ID** (e.g., `DS-30`, `TASK-05`)
- **Type** (IMPLEMENT, INVESTIGATE, DECISION)
- **Explicit dependencies** (`Depends on` field — task IDs)
- **Affects** (file paths — both primary and `[readonly]`)
- **Phase** (if tasks are organized by phase)
- **Effort** (S, M, L)
- **Status** (Pending, In-Progress, Blocked, etc.)

### 2) Build Dependency Graph

Construct a directed acyclic graph (DAG) of task dependencies from three sources, in priority order:

#### a) Explicit dependencies (highest priority)

If task B says `Depends on: TASK-A`, add edge A -> B.

#### b) File-overlap dependencies (implicit)

If task A and task B both list the same file as **primary** in `Affects`, they cannot safely run in parallel. Determine ordering by:

1. **Infrastructure before consumers** — tasks that create/define types, schemas, tokens, or shared modules come before tasks that consume them
2. **Smaller scope first** — S-effort before M-effort before L-effort when both touch the same file, unless logic dictates otherwise
3. **Foundation before features** — if both tasks modify `index.ts` (barrel file), the task adding foundational exports goes first

When file overlap creates an implicit dependency, add it to the `Depends on` field with a comment: `(file overlap: <path>)`.

#### c) Phase ordering (soft preference)

Tasks in earlier phases are preferred before later phases, but this is a **soft** constraint — it can be overridden when a later-phase task has no dependencies and can run in parallel with earlier-phase work.

### 3) Topological Sort

Sort tasks using topological ordering (Kahn's algorithm or DFS-based):

1. Tasks with no dependencies come first
2. Among tasks with equal dependency depth, prefer:
   - INVESTIGATE/DECISION before IMPLEMENT (they unblock others)
   - Lower phase number
   - Smaller effort (S before M before L)
   - Alphabetical by description (stable tiebreak)
3. Detect cycles — if found, report them and STOP (cycles indicate a planning error that needs `/re-plan`)

### 4) Renumber Tasks

Assign new sequential IDs using the plan's domain prefix:

- If original IDs use a domain prefix (e.g., `DS-`), preserve it: `DS-01`, `DS-02`, ...
- If original IDs use `TASK-`, continue with that: `TASK-01`, `TASK-02`, ...
- Use zero-padded two-digit numbers: `-01`, `-02`, ... `-99`

Build a **rename map** (`old ID -> new ID`) for updating all cross-references.

### 5) Update Dependencies and Add Blockers

For each task:

- **Update `Depends on`**: Replace old task IDs with new IDs using the rename map
- **Add `Blocks` field**: The inverse of `Depends on`. If TASK-03 depends on TASK-01, then TASK-01 blocks TASK-03. Format: `Blocks: TASK-03, TASK-07`
- If a task has no dependencies: `Depends on: -`
- If a task blocks nothing: `Blocks: -`

### 6) Identify Parallel Execution Groups

Analyze the DAG to identify which tasks can run concurrently. A **parallel group** is a set of tasks that:

- Share no dependencies between each other
- Have all their prerequisites completed (or share the same prerequisites)
- Do not modify overlapping files

Produce a **Parallelism Guide** showing execution waves:

```markdown
## Parallelism Guide

Execution waves for subagent dispatch. Tasks within a wave can run in parallel.
Tasks in a later wave require all blocking tasks from earlier waves to complete.

| Wave | Tasks | Prerequisites | Notes |
|------|-------|---------------|-------|
| 1 | TASK-01, TASK-02, TASK-03 | - | Independent foundation tasks |
| 2 | TASK-04, TASK-05 | Wave 1: TASK-01 | TASK-04 needs TASK-01; TASK-05 needs TASK-01 |
| 3 | TASK-06 | Wave 2: TASK-04 | Sequential bottleneck |
| 4 | TASK-07, TASK-08 | Wave 3: TASK-06 | Both need TASK-06 |

**Max parallelism:** 3 (Wave 1)
**Critical path:** TASK-01 -> TASK-04 -> TASK-06 -> TASK-07 (4 waves)
**Total tasks:** 8
```

### 7) Update the Plan Document

Apply all changes to the plan file:

#### a) Task Summary Table

Rewrite the table with new IDs, correct ordering, and updated `Depends on`:

```markdown
## Task Summary

| Task ID | Type | Description | Confidence | Effort | Status | Depends on | Blocks |
|---|---|---|---:|---|---|---|---|
| DS-01 | IMPLEMENT | ... | 92% | S | Pending | - | DS-05, DS-10 |
| DS-02 | IMPLEMENT | ... | 90% | M | Pending | - | DS-06 |
```

#### b) Task Sections

- Reorder task sections (`### TASK-XX: ...`) to match new numbering
- Update all task IDs in headers and body text
- Update `Depends on` fields with new IDs
- Add `Blocks` field after `Depends on` in each task
- Update any cross-references in Notes/references fields

#### c) Phase Headers (preserve or restructure)

- If phases are still meaningful groupings after reordering, preserve phase headers
- If reordering makes phases misleading, replace phase headers with a simpler structure and note the original phase in each task's metadata

#### d) Add Parallelism Guide

Insert the Parallelism Guide section after the Task Summary table.

### 8) Validate

After editing, verify:

- Every task ID in any `Depends on` or `Blocks` field exists in the plan
- No circular dependencies
- Completed/deferred tasks were not renumbered or moved (they stay in their historical section)
- The rename map accounts for all references (grep old IDs — should find zero matches in active tasks)

### 9) Completion Summary

Report what changed:

```markdown
## Sequencing Complete

**Plan:** docs/plans/<slug>-plan.md
**Tasks sequenced:** N active tasks reordered and renumbered
**Rename map:**
- DS-30 -> DS-01
- DS-35 -> DS-02
- ...

**Dependency changes:**
- N explicit dependencies preserved
- M implicit dependencies added (file overlap)
- No cycles detected

**Parallel execution:**
- K execution waves identified
- Max parallelism: P tasks in wave N
- Critical path length: W waves

Ready for `/build-feature`.
```

## Handling Edge Cases

### Completed Tasks

Tasks with status `Complete (YYYY-MM-DD)` are **not reordered or renumbered**. They stay in their historical section. If an active task depends on a completed task, the dependency is noted as satisfied: `Depends on: DS-61 (complete)`.

### Deferred Tasks

Tasks with status `Deferred` are **not included** in the sequencing. They stay in the Deferred section. Note them in the Parallelism Guide footer.

### In-Progress Tasks

Tasks with status `In-Progress` are included in sequencing but flagged:

```markdown
> **Note:** TASK-03 is currently In-Progress. Its position in the sequence reflects its dependencies, not a suggestion to restart it.
```

### Tasks with Ranges in Dependencies

Some tasks use range syntax (e.g., `DS-73–DS-77`). Expand these to explicit lists during renumbering: `Depends on: DS-10, DS-11, DS-12, DS-13, DS-14`.

## Quality Checks

- [ ] All active tasks have been assigned new sequential IDs
- [ ] The rename map is complete (no orphaned old IDs in active sections)
- [ ] Every `Depends on` reference points to a valid task ID
- [ ] Every `Blocks` field is the correct inverse of `Depends on`
- [ ] No circular dependencies exist
- [ ] File-overlap dependencies have been identified and documented
- [ ] Parallelism Guide correctly groups non-conflicting tasks into waves
- [ ] Completed and deferred tasks are untouched
- [ ] Task Summary table matches the new ordering
- [ ] Critical path is identified

## Completion Messages

**Success:**
> "Plan sequenced. N tasks reordered into K execution waves (max parallelism: P). Critical path: W waves. Rename map applied. Ready for `/build-feature`."

**Cycle detected:**
> "Cannot sequence — circular dependency detected between TASK-A and TASK-B. Run `/re-plan` to resolve the cycle before sequencing."

**No changes needed:**
> "Plan is already correctly sequenced. No reordering required."
