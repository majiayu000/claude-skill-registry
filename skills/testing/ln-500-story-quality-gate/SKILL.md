---
name: ln-500-story-quality-gate
description: Story quality validation coordinator with gates
---

---
name: ln-500-story-quality-gate
description: Story-level quality orchestrator. Pass 1: code quality -> regression -> manual testing (fail fast). Pass 2: verify tests/coverage -> mark Story Done. Auto-discovers team/config.
---

# Story Quality Gate

Two-pass Story review that fails fast, creates needed fix/refactor/test tasks, and finalizes the Story only after tests are verified.

## Purpose & Scope
- Pass 1 (after impl tasks Done): run code-quality, lint, regression, and manual testing; if all pass, create/confirm test task; otherwise create targeted fix/refactor tasks and stop.
- Pass 2 (after test task Done): verify tests/coverage/priority limits and close Story to Done or create fix tasks.
- Delegates work to 341/342/343 workers and ln-510-test-planner; invoked by ln-410-story-executor.

## When to Use
- Pass 1: all implementation tasks Done; test task missing or not Done.
- Pass 2: test task exists and is Done.
- Explicit `pass` parameter can force 1 or 2; otherwise auto-detect by test task status.

## Workflow (concise)
- **Phase 1 Discovery:** Auto-discover team/config; select Story; load Story + task metadata (no descriptions), detect test task status.
- **Pass 1 flow (fail fast):**
  1) Invoke ln-501-code-quality-checker. If issues -> create refactor task (Backlog), stop.
  2) Run all linters from tech_stack.md. If fail -> create lint-fix task, stop.
  3) Invoke ln-502-regression-checker. If fail -> create regression-fix task, stop.
  4) Invoke ln-503-manual-tester. If fail -> create bug-fix task, stop.
  5) If all passed: if no test task exists, auto-call ln-510-test-planner (autoApprove) to create test task; if test task exists and Done, jump to Pass 2; if exists but not Done, report status and stop.
- **Pass 2 flow (after test task Done):**
  1) Load Story/test task; read test plan/results and manual testing comment from Pass 1.
  2) Verify limits and priority: Priority ≤15; E2E 2-5, Integration 0-8, Unit 0-15, total 10-28; tests focus on business logic (no framework/DB/library tests).
  3) Ensure Priority ≤15 scenarios and Story AC are covered by tests; infra/docs updates present.
  4) If pass -> mark Story Done in Linear; minimal kanban cleanup if needed. If fail -> create fix tasks (Backlog) and stop; ln-410 will loop.

**TodoWrite format (mandatory):**
Add pass steps to todos before starting:
```
Pass 1:
- Invoke ln-501-code-quality-checker (in_progress)
- Run linters from tech_stack.md (pending)
- Invoke ln-502-regression-checker (pending)
- Invoke ln-503-manual-tester (pending)
- Create/verify test task via ln-510 (pending)

Pass 2:
- Verify test task coverage (in_progress)
- Mark Story Done (pending)
```
Mark each as in_progress when starting, completed when done. On failure, mark remaining as skipped.

## Critical Rules
- Early-exit: any failure creates a specific task and stops Pass 1/2.
- Single source of truth: rely on Linear metadata for tasks; kanban is updated by workers/ln-410.
- Task creation via skills only (ln-510/ln-301); this skill never edits tasks directly.
- Pass 2 only runs when test task is Done; otherwise return error/status.
- Language preservation in comments (EN/RU).

## Definition of Done
- Pass 1: 341 pass OR refactor task created; linters pass OR lint-fix task created; 342 pass OR regression-fix task created; 343 pass OR bug-fix task created; if all pass, test task created (if missing) or status reported; exits.
- Pass 2: test task verified (priority/limits/coverage/infra/docs); Story set to Done in Linear (if pass) or fix tasks created (if fail); kanban minimally cleaned if needed.
- Summary/comment posted in Linear for actions taken.

## Reference Files
- Workers: `../ln-501-code-quality-checker/SKILL.md`, `../ln-502-regression-checker/SKILL.md`, `../ln-503-manual-tester/SKILL.md`
- Test planning: `../ln-510-test-planner/SKILL.md`
- Tech stack/linters: `docs/project/tech_stack.md`

---
**Version:** 3.0.0 (Condensed passes and fail-fast actions)
**Last Updated:** 2025-12-23
