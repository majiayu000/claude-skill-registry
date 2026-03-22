---
name: dispatch
description: Use when an approved plan exists (plan.md + tasks.md) and you need to execute it. Dispatches subagents per task with two-stage review and progress tracking.
effort: high
argument-hint: "[spec-NNN or --resume]"
---



# Dispatch

## Purpose

Execution engine for approved plans. Reads plan.md and tasks.md, dispatches one subagent per task (fresh context), runs two-stage review on each deliverable, and tracks progress. If stuck: STOP and re-plan.

## When to Use

- After `/ai-plan` produces an approved plan
- To resume execution: `/ai-dispatch --resume`
- Never without an approved plan (run `/ai-plan` first)

## Process

1. **Load plan** -- read `specs/spec.md` -> `specs/plan.md`
2. **Load decisions** -- read `decision-store.json` for constraints
3. **Build DAG** -- parse task dependencies, identify parallel groups
4. **Execute phase by phase** -- for each phase:
   a. Dispatch one subagent per task (fresh context window)
   b. Each subagent receives: task description, file scope, boundaries, constraints
   c. Run two-stage review on deliverable (see below)
   d. Update task status in tasks.md
   e. Check phase gate before advancing
5. **Track progress** -- update tasks.md checkboxes after each task
6. **Report completion** -- summary of all tasks, any concerns raised

## Task Statuses

| Status | Meaning | Action |
|--------|---------|--------|
| `DONE` | Task completed, reviews passed | Check off, advance |
| `DONE_WITH_CONCERNS` | Completed but reviewer flagged issues | Check off, log concerns for follow-up |
| `NEEDS_CONTEXT` | Agent needs information not in the plan | Pause, ask user, then resume |
| `BLOCKED` | Cannot proceed (dependency, access, ambiguity) | STOP execution, re-plan |

## Two-Stage Review

Every task deliverable goes through two reviews before marking DONE:

### Stage 1: Spec Compliance

- Does the deliverable match the task description?
- Does it satisfy the acceptance criteria from spec.md?
- Are all file scope boundaries respected (no out-of-scope changes)?

### Stage 2: Code Quality

- Stack validation passes (ruff, tsc, cargo check, etc.)
- No new lint warnings introduced
- Test coverage maintained or improved
- No governance advisory warnings from guard

If either stage fails: fix and re-review (max 2 retries per stage).

## DAG Construction

**Independent** (can run in parallel):
- Different file scopes with no overlap
- No producer-consumer relationship
- Different modules with no shared state

**Dependent** (must serialize):
- Task B reads files Task A creates
- Task B depends on Task A's output
- Both modify governance artifacts (`.ai-engineering/` must serialize)
- Plan explicitly orders them

## Subagent Context

Each subagent receives a focused context window:

```yaml
task: T-2.1
description: "Implement the parse_config function"
agent: build
scope:
  files: ["src/config.py", "tests/test_config.py"]
  boundaries: ["Do NOT modify src/main.py", "Do NOT touch hooks/"]
constraints:
  - "Follow existing ConfigParser pattern in src/base_config.py"
  - "TDD: test files from T-2.0 are IMMUTABLE"
gate:
  post: ["ruff check", "pytest tests/test_config.py"]
```

## Stuck Protocol

If a task fails after 2 retries:

1. Mark task as BLOCKED with reason
2. Check if other tasks in the phase can proceed independently
3. If phase is blocked entirely: STOP execution
4. Report to user: what failed, what was tried, options (re-plan, skip, manual fix)

Never loop silently. Never retry the same approach more than twice.

## Progress Tracking

Update tasks.md in real-time:

```markdown
- [x] T-1.1: Create config module @build -- DONE
- [x] T-1.2: Add validation logic @build -- DONE_WITH_CONCERNS (perf warning)
- [ ] T-2.1: Write integration tests @build -- IN PROGRESS
- [ ] T-2.2: Security scan @verify -- PENDING
```

## Common Mistakes

- Dispatching without an approved plan.
- Giving subagents the entire codebase context (scope them tightly).
- Skipping the two-stage review.
- Continuing past a BLOCKED task without user input.
- Modifying test files from a RED phase during a GREEN phase task.

## Integration

- **Called by**: user directly (after `/ai-plan` approval)
- **Calls**: `ai-build agent` (build tasks), `/ai-verify` (scan tasks), `/ai-guard` (gate checks)
- **Transitions to**: `/ai-commit` (after all tasks DONE), or back to `/ai-plan` (if re-plan needed)

$ARGUMENTS
