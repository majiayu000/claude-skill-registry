---
name: spec-kit-implement
description: Use when approved Spec Kit `tasks.md` must be executed into implementation changes, or when task execution is blocked by sequencing/checklist gates before feature completion.
---

# Spec Kit Implement

Execute approved feature tasks in dependency order and keep `tasks.md` status accurate.

## When to Use

- `tasks.md` exists and you need to execute it phase-by-phase to deliver the feature.
- Implementation work has started, but task sequencing, checklist gates, or progress tracking is inconsistent.
- You need deterministic execution behavior before handoff or release readiness checks.

## When Not to Use

- `tasks.md` does not exist yet (`spec-kit-tasks` first).
- You are still writing or revising requirements/design artifacts (`spec-kit-specify`, `spec-kit-clarify`, `spec-kit-plan`).
- You need read-only consistency analysis rather than execution (`spec-kit-analyze`).
- You need coordinated artifact remediation after gaps are discovered (`spec-kit-reconcile`).

## Router Fit

- Primary route from `spec-kit` after `spec-kit-tasks`.
- Requires planning + task artifacts for the active feature branch.
- Routes execution-discovered artifact drift to `spec-kit-reconcile`.

## Preconditions

- Run from repository root (or a subdirectory inside it).
- Active feature context resolves to a single `specs/<feature>/` directory.
- `tasks.md` reflects the current approved `plan.md`.

## Workflow

1. Resolve feature artifacts and enforce implementation gate:

   - Run `scripts/check-prerequisites.sh --json --require-tasks --include-tasks` exactly once.
   - Parse `FEATURE_DIR` and `AVAILABLE_DOCS`.
   - Derive:
     - `TASKS = FEATURE_DIR/tasks.md`
     - `IMPL_PLAN = FEATURE_DIR/plan.md`
   - If prerequisites fail:
     - missing `tasks.md`: stop and route to `spec-kit-tasks`
     - missing `plan.md`: stop and route to `spec-kit-plan`

2. Enforce checklist gate when checklists exist:

   - If `FEATURE_DIR/checklists/` exists, scan all checklist files.
   - If any unchecked items remain, stop and ask whether to proceed anyway.
   - Continue only after explicit user approval.

3. Load execution context:

   - Required: `tasks.md`, `plan.md`.
   - Optional (when present): `data-model.md`, `contracts/`, `research.md`, `quickstart.md`.
   - Use these artifacts as source of truth; do not invent scope beyond them.

4. Verify ignore-file coverage for active tooling:

   - Check relevant ignore files (`.gitignore`, `.dockerignore`, `.eslintignore`, `.prettierignore`, etc.).
   - Add only missing critical patterns; preserve existing user/project conventions.

5. Parse `tasks.md` into an execution plan before running tasks:

   - Extract phase boundaries and phase intent (setup/foundational, user-story phases, polish).
   - Extract per-task fields: task ID, description, file path, `[P]` marker, and optional `[US#]` label.
   - Build dependency order from task IDs, phase ordering, and explicit sequencing notes.
   - Treat this parsed structure as execution truth for progress and failure handling.

6. Execute tasks in phase order:

   - Respect ordering and dependency constraints from `tasks.md`.
   - Run `[P]` tasks in parallel only when there is no file overlap or dependency coupling.
   - Follow tests-before-implementation ordering where test tasks exist.
   - Complete each phase before moving to the next:
     - setup/foundational work first,
     - then user-story phases in priority order,
     - polish and cross-cutting validation last.

7. Track progress and failures continuously:

   - After each completed task, mark it `[X]` in `tasks.md` immediately.
   - Halt on critical sequential task failures and report the blocking context.
   - For parallel batches, keep successful items moving and report failed tasks with next actions.

8. Run completion checks:

   - All required tasks are complete.
   - Implementation aligns with `spec.md`/`plan.md` intent.
   - Required tests/validation pass per project constraints.
   - If gaps remain (for example missing wiring, acceptance mismatch, integration drift), route to `spec-kit-reconcile` with a concrete gap report.

9. Report implementation result:

   - Absolute path to `tasks.md`.
   - Completed vs remaining task counts.
   - Checklist gate outcome (if used).
   - Final status and recommended next step.

## Output

- Updated `tasks.md` completion state for the active feature.
- Implementation progress summary with blockers/failures (if any).
- Final readiness signal for post-implementation verification/review.

## Key Rules

- Treat `tasks.md` ordering as execution truth.
- Never mark a task `[X]` before its work and validations are complete.
- Do not run `[P]` tasks concurrently when they touch the same files or dependent resources.
- Stop and reroute when prerequisite artifacts are missing or invalid.
- Do not patch spec/plan/tasks ad hoc during execution; use `spec-kit-reconcile` for structured remediation.

## Common Mistakes

- Starting implementation with stale or missing `tasks.md`.
- Skipping checklist acknowledgment when unresolved checklist items exist.
- Forgetting immediate `[X]` updates in `tasks.md`, causing drift between reality and artifact state.
- Running `[P]` tasks together despite file/dependency conflicts.
- Continuing past critical sequential failures instead of stopping and reporting.
- Editing `spec.md`/`plan.md`/`tasks.md` informally during implementation instead of routing remediation through `spec-kit-reconcile`.

## References

- `references/spec-kit-implement-flow.dot` for implementation execution logic workflow
- `references/spec-kit-workflow.dot` for overall context of how the implementation fits into the Spec Kit process.
- `scripts/check-prerequisites.sh`
- `https://github.com/github/spec-kit/blob/9111699cd27879e3e6301651a03e502ecb6dd65d/templates/commands/implement.md`
