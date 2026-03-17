---
name: openspec-dev
description: Adapter for executing OpenSpec change proposals using subagent-driven-development. Parses OpenSpec structure, groups tasks by phase, and creates one PR per phase.
---

# OpenSpec Development Adapter

Converts OpenSpec change proposals into executable plans and delegates implementation to `superpowers:subagent-driven-development`.

## Prerequisites

- Active OpenSpec change with approved `proposal.md`
- Populated `tasks.md` with tasks organized by phase
- Clean git state on main branch

## Invocation

```
/openspec-dev <change-id> [phases]
```

**Arguments:**
- `<change-id>` — Required. The OpenSpec change directory name
- `[phases]` — Optional. Phase filter using numeric ranges (e.g., `1,3,5-7`)

**Examples:**
- `/openspec-dev add-launch-features` — Execute all phases
- `/openspec-dev add-launch-features 2` — Execute phase 2 only
- `/openspec-dev add-launch-features 1,3-5` — Execute phases 1, 3, 4, and 5

---

## Phase Filtering

When `[phases]` is provided, only matching phases from `tasks.md` are executed.

**Parsing rules:**
- Single number: `2` → phase 2 only
- Comma-separated: `1,3,5` → phases 1, 3, and 5
- Range with dash: `2-4` → phases 2, 3, and 4
- Mixed: `1,3-5,7` → phases 1, 3, 4, 5, and 7
- Whitespace ignored, duplicates removed, sorted ascending

**Phase numbering:** Phases are numbered by order in `tasks.md` (first `## Phase ...` = 1, second = 2, etc.)

**Error handling:**
- Invalid phase number (doesn't exist): Warn and skip, continue with valid phases
- Phase already complete (all tasks checked): Log "Phase N: No unchecked tasks, skipping"
- Malformed input (non-numeric, zero, negative): Error with usage example

---

## Workflow

```
Parse OpenSpec → Extract phases → Per phase: branch + subagent-driven-dev + PR
```

---

## Step 1: Parse OpenSpec Structure

Read and extract from `openspec/changes/<change-id>/`:

1. **proposal.md** — identify phases/milestones
2. **tasks.md** — extract tasks, group by phase
3. **Apply phase filter** (if `[phases]` provided):
   - Parse phase numbers from argument
   - Filter to only matching phases
   - Warn for non-existent phases
   - Log and skip phases with no unchecked tasks

```markdown
# Example tasks.md structure
## Phase 1: Core API
- [ ] Add user authentication endpoint
- [ ] Create data validation layer

## Phase 2: UI Components
- [ ] Build login form component
- [ ] Add dashboard layout
```

Extract unchecked tasks (`- [ ]`) grouped by their phase heading. When `[phases]` is specified, only process matching phases.

---

## Step 2: Execute Each Phase

For each phase with unchecked tasks:

### 2a. Create Phase Branch

```bash
git checkout main && git pull
git checkout -b feat/<change-id>-phase-N
```

### 2b. Prepare Plan for Subagent-Driven-Development

Convert phase tasks into a plan format:

```markdown
# Phase N: <Phase Name>

## Context
OpenSpec change: <change-id>
Spec reference: openspec/specs/<capability>/spec.md

## Tasks
1. <Task description from tasks.md>
2. <Task description from tasks.md>
...
```

### 2c. Invoke Subagent-Driven-Development

Follow the `superpowers:subagent-driven-development` workflow:
- Dispatch implementer subagent per task (sequential)
- Two-stage review: spec compliance → code quality
- Use TDD discipline throughout

The subagent-driven-development skill handles:
- Implementer prompts and self-review
- Spec compliance review
- Code quality review
- Retry loops for issues

### 2d. Create PR for Phase

When all phase tasks complete:

```bash
gh pr create \
  --title "feat(<change-id>): Phase N - <phase name>" \
  --body "## Summary
<bullet points of changes>

## OpenSpec Reference
- Change: openspec/changes/<change-id>/proposal.md
- Tasks: Phase N from tasks.md

## Test Coverage
<list of test files added/modified>"
```

---

## Step 3: Sync Progress to Source tasks.md

**Critical:** Keep `openspec/changes/<change-id>/tasks.md` updated as the source of truth.

### After Each Task Completes

When a task passes both reviews in subagent-driven-development:

1. Update the source file `openspec/changes/<change-id>/tasks.md`
2. Change `- [ ]` to `- [x]` for the completed task
3. Commit the update to the phase branch

```bash
# Example: mark task complete in source file
# In openspec/changes/add-launch-features/tasks.md:
# - [ ] Add user authentication endpoint  →  - [x] Add user authentication endpoint
git add openspec/changes/<change-id>/tasks.md
git commit -m "chore(openspec): mark task complete - <task description>"
```

### After Phase PR Created

Add PR reference to completed tasks:

```markdown
## Phase 1: Core API
- [x] Add user authentication endpoint (PR #142)
- [x] Create data validation layer (PR #142)
```

### Why This Matters

- **Resumability:** If execution stops mid-phase, progress isn't lost
- **Visibility:** Anyone can check `tasks.md` to see current status
- **Idempotency:** Re-running the skill skips already-completed tasks (`- [x]`)

---

## Step 4: Final Report

After all phases:

```markdown
## OpenSpec Development Complete: <change-id>

| Phase | Branch | PR | Status |
|-------|--------|-----|--------|
| Phase 1: Core API | feat/change-id-phase-1 | #142 | Ready |
| Phase 2: UI Components | — | — | Skipped (not in filter) |
| Phase 3: Tests | — | — | Skipped (already complete) |
| Phase 4: Docs | feat/change-id-phase-4 | #143 | Ready |

### Next Steps
- Review and merge PRs in phase order
- Run again if tasks were added or skipped
```

**Status values:**
- `Ready` — PR created, awaiting review
- `Skipped (not in filter)` — Phase excluded by `[phases]` argument
- `Skipped (already complete)` — All tasks in phase already checked

---

## Integration

This skill is a thin adapter that delegates to:

| Skill | Purpose |
|-------|---------|
| `superpowers:subagent-driven-development` | Task execution, reviews, retry loops |
| `superpowers:test-driven-development` | TDD discipline (used by implementers) |
| `superpowers:finishing-a-development-branch` | Final cleanup if needed |

**Do not duplicate** the implementation/review logic from subagent-driven-development.
