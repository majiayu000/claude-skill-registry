---
name: spec-kit-tasks
description: Use when an approved Spec Kit `plan.md` + `spec.md` must be decomposed into dependency-ordered `tasks.md`, or when `tasks.md` is missing/stale after planning or reconciliation changes.
---

# Spec Kit Tasks

Generate an implementation-ready `tasks.md` from Spec Kit design artifacts.

## When to Use

- `plan.md` and `spec.md` exist and you need executable tasks for implementation.
- `tasks.md` is missing, stale, or not aligned with current plan/spec artifacts (including post-`spec-kit-reconcile` updates).
- You need user-story-scoped task phases with clear dependency and parallelization signals.

## When Not to Use

- The feature spec is missing (`spec-kit-specify` first).
- High-impact ambiguity still blocks design decisions (`spec-kit-clarify` first).
- Technical design artifacts are not finalized (`spec-kit-plan` first).
- You are executing tasks rather than generating them (`spec-kit-implement`).

## Router Fit

- Primary route from `spec-kit` after `spec-kit-plan`.
- Must complete before `spec-kit-implement`.
- Supports `spec-kit-analyze` and `spec-kit-reconcile` by producing structured implementation intent.

## Preconditions

- Run from repository root (or a subdirectory inside it).
- Active feature context resolves to one `specs/<feature>/` directory.
- `plan.md` exists and reflects the latest approved design.

## Workflow

1. Resolve feature paths and prerequisite gate:

   - Run `scripts/check-prerequisites.sh --json` exactly once.
   - Parse `FEATURE_DIR` and `AVAILABLE_DOCS`.
   - Derive:
     - `FEATURE_SPEC = FEATURE_DIR/spec.md`
     - `IMPL_PLAN = FEATURE_DIR/plan.md`
     - `TASKS = FEATURE_DIR/tasks.md`
   - If `spec.md` is missing, stop and route to `spec-kit-specify` then `spec-kit-plan`.

2. Load generation inputs:

   - Required: `plan.md`, `spec.md`.
   - Optional (when present): `research.md`, `data-model.md`, `contracts/`, `quickstart.md`.
   - Template preference:
     - `{REPO_ROOT}/templates/tasks-template.md`
     - `{REPO_ROOT}/.specify/templates/tasks-template.md`
     - fallback: `assets/tasks-template.md`

3. Extract planning context:

   - From `plan.md`: stack, architecture, constraints, project structure.
   - From `spec.md`: prioritized user stories, acceptance criteria, independent test intent.
   - From optional docs: shared entities, external interfaces, and setup decisions.

4. Build task phases:

   - Phase 1: Setup.
   - Phase 2: Foundational prerequisites blocking all stories.
   - Phase 3+: one phase per user story in priority order.
   - Final phase: Polish/cross-cutting concerns.

5. Generate tasks in strict checklist format:

   - Required pattern: `- [ ] T### [P?] [US#?] Action with file path`.
   - Include `[US#]` only for user-story phases.
   - Include `[P]` only when tasks can run safely in parallel.
   - Include exact file paths in every implementation/test task description.
   - Add test tasks only when explicitly requested by spec/user.

6. Validate coverage and ordering before writing:

   - Every user story has independently testable tasks.
   - Dependencies are explicit and respect phase order.
   - Every task matches format requirements (checkbox, ID, labels, file path).
   - No orphaned entities/contracts without mapped tasks.

7. Write `tasks.md`:

   - Preserve heading order from the selected template.
   - Replace template placeholders and sample content with concrete feature tasks.

8. Report completion:

   - Absolute `tasks.md` path.
   - Total task count and per-story counts.
   - Parallel opportunities.
   - Suggested MVP slice (typically first priority story).
   - Readiness handoff for `spec-kit-implement`.

## Task Format Guidance

### Format Components

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox).
2. **Task ID**: Sequential number (`T001`, `T002`, `T003`, ...) in execution order.
3. **`[P]` marker**: Include ONLY if the task is parallelizable (different files, no dependencies on incomplete tasks).
4. **`[Story]` label**: REQUIRED for user story phase tasks only.
   - Format: `[US1]`, `[US2]`, `[US3]`, etc. (maps to user stories from `spec.md`)
   - Setup phase: no story label
   - Foundational phase: no story label
   - User story phases: MUST have story label
   - Polish phase: no story label
5. **Description**: Clear action with exact file path.

### Examples

- CORRECT: `- [ ] T001 Create project structure per implementation plan`
- CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- WRONG: `- [ ] Create User model` (missing Task ID and Story label)
- WRONG: `T001 [US1] Create model` (missing checkbox)
- WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- WRONG: `- [ ] T001 [US1] Create model` (missing file path)

## Output

- `tasks.md` under the active feature directory with dependency-ordered, story-scoped tasks.
- Completion summary with task counts, dependency highlights, and MVP recommendation.

## Key Rules

- Organize tasks by user story so each story can be implemented and validated independently.
- Keep task granularity implementation-ready: no vague one-liners and no giant umbrella tasks.
- Preserve execution truth in IDs and dependency order (`T001`, `T002`, ...).
- Treat foundational work as blocking unless it is explicitly independent and parallel-safe.
- Never invent tests by default; include test work only when requested.

## Common Mistakes

- Generating tasks from `spec.md` alone without using `plan.md` constraints.
- Copying sample tasks from the template instead of replacing them.
- Missing file paths or story labels in user-story phases.
- Marking conflicting tasks as `[P]` even though they touch the same files/dependencies.
- Producing tasks that cannot satisfy each story's independent test criteria.

## References

- `references/spec-kit-workflow.dot` for where task generation fits in the full Spec Kit sequence.
- `scripts/check-prerequisites.sh`
- `assets/tasks-template.md`
- `https://github.com/github/spec-kit/blob/9111699cd27879e3e6301651a03e502ecb6dd65d/templates/commands/tasks.md`
