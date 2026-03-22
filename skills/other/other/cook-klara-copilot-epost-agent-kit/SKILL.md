---
name: cook
description: (ePost) Use when user says "implement", "build", "add a feature", "cook", "make this work", or "continue the plan" — dispatches platform-aware feature implementation for web, iOS, Android, or backend
user-invocable: true
context: fork
agent: epost-fullstack-developer
metadata:
  argument-hint: "[feature description or plan file]"
---

# Cook — Unified Implementation Command

Implement features with automatic platform detection.

## Step 0 — Active Plan Resolution (when args are empty)

**If `$ARGUMENTS` is empty**, resolve the active plan before asking the user for a task:

1. Run: `node .claude/scripts/get-active-plan.cjs`
2. **If result ≠ `none`**: read the plan's `plan.md`, identify the first phase with `status: pending`, and implement it — no need to ask the user what to do.
3. **If result = `none`**: scan `plans/*/plan.md` for the most recently created plan with `status: pending` (plans just created by `/plan` that haven't been activated yet). Sort by directory name descending; take the first match.
4. **If still nothing**: ask the user for a task description.

When a plan is found via step 3 (frontmatter scan), run `node .claude/scripts/set-active-plan.cjs <plan-dir>` to activate it before proceeding.

## Step 1 — Flag Override

If `$ARGUMENTS` starts with `--fast`: skip auto-detection, load `references/fast-mode.md` and execute directly. Remaining args are the task description.
If `$ARGUMENTS` starts with `--parallel`: skip auto-detection, load `references/parallel-mode.md` and execute directly. Remaining args are the task description.
Otherwise: continue to Platform Detection.

## Aspect Files

| File | Purpose |
|------|---------|
| `references/fast-mode.md` | Direct implementation — skip plan question, implement immediately |
| `references/parallel-mode.md` | Parallel implementation for multi-module features |

## Platform Detection

Detect platform per `skill-discovery` protocol.

## Complexity → Variant

- Single file or clear task → fast (skip plan question)
- Multi-file, one module → fast
- Multi-module or unknowns → parallel
- Has existing plan in ./plans/ → follow plan
- Plan with 3+ independent tasks → consider subagent-driven mode (see `subagent-driven-development` skill)

## Execution

Route to the detected platform agent with feature description and platform context.

<feature>$ARGUMENTS</feature>

**IMPORTANT:** Analyze the skills catalog and activate the skills needed for the detected platform.
