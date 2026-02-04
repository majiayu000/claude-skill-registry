---
name: ln-500-story-quality-gate
description: "Story-level quality orchestrator with 4-level Gate (PASS/CONCERNS/FAIL/WAIVED) and Quality Score. Pass 1: code quality -> regression -> manual testing. Pass 2: verify tests/coverage -> calculate NFR scores -> mark Story Done. Use when user requests quality gate for Story or when ln-400 delegates quality check."
---

# Story Quality Gate

Two-pass Story review with 4-level Gate verdict, Quality Score calculation, and NFR validation (security, performance, reliability, maintainability).

## Purpose & Scope
- Pass 1 (after impl tasks Done): run code-quality, lint, regression, and manual testing; if all pass, create/confirm test task; otherwise create targeted fix/refactor tasks and stop.
- Pass 2 (after test task Done): verify tests/coverage/priority limits, calculate Quality Score and NFR validation, close Story to Done or create fix tasks.
- Delegates work to ln-501/ln-502 workers and ln-510-test-planner.

## 4-Level Gate Model

| Level | Meaning | Action |
|-------|---------|--------|
| **PASS** | All checks pass, no issues | Story → Done |
| **CONCERNS** | Minor issues, acceptable risk | Story → Done with comment noting concerns |
| **FAIL** | Blocking issues found | Create fix tasks, return to ln-400 |
| **WAIVED** | Issues acknowledged by user | Story → Done with waiver reason documented |

**Verdict calculation:** `FAIL` if any check fails. `CONCERNS` if minor issues exist. `PASS` if all clean.

## Quality Score

Formula: `Quality Score = 100 - (20 × FAIL_count) - (10 × CONCERN_count)`

| Score Range | Status | Action |
|-------------|--------|--------|
| 90-100 | ✅ Excellent | PASS |
| 70-89 | ⚠️ Acceptable | CONCERNS (proceed with notes) |
| 50-69 | ❌ Below threshold | FAIL (create fix tasks) |
| <50 | 🚨 Critical | FAIL (urgent priority) |

## NFR Validation

Evaluate 4 non-functional requirement dimensions:

| NFR | Checks | Issue Prefix |
|-----|--------|--------------|
| **Security** | Auth, input validation, secrets exposure | SEC- |
| **Performance** | N+1 queries, caching, response times | PERF- |
| **Reliability** | Error handling, retries, timeouts | REL- |
| **Maintainability** | DRY, SOLID, cyclomatic complexity | MNT- |

Additional prefixes: `TEST-` (coverage gaps), `ARCH-` (architecture issues), `DOC-` (documentation gaps), `DEP-` (Story/Task dependencies), `COV-` (AC coverage quality), `DB-` (database schema), `AC-` (AC validation)

**NFR verdict per dimension:** PASS / CONCERNS / FAIL

## When to Use
- Pass 1: all implementation tasks Done; test task missing or not Done.
- Pass 2: test task exists and is Done.
- Explicit `pass` parameter can force 1 or 2; otherwise auto-detect by test task status.

## Workflow (concise)
- **Phase 1 Discovery:** Auto-discover team/config; select Story; load Story + task metadata (no descriptions), detect test task status.
- **Pass 1 flow (fail fast):**
  1) Invoke ln-501-code-quality-checker. If issues -> create refactor task (Backlog), stop.
  1.5) **Criteria Validation (Story-level checks)** - see `references/criteria_validation.md`:
     - Check #1: Story Dependencies (no forward deps within Epic) - if FAIL → create [DEP-] task, stop.
     - Check #2: AC-Task Coverage Quality (STRONG/WEAK/MISSING scoring) - if FAIL/CONCERNS → create [BUG-]/[COV-] tasks, stop.
     - Check #3: Database Creation Principle (schema scope matches Story) - if FAIL → create [DB-] task, stop.
  2) Run all linters from tech_stack.md. If fail -> create lint-fix task, stop.
  3) Invoke ln-502-regression-checker. If fail -> create regression-fix task, stop.
  4) Invoke ln-510-test-planner (orchestrates: ln-511-test-researcher → ln-512-manual-tester → ln-513-auto-test-planner). If manual testing fails -> create bug-fix task, stop. If all passed -> test task created/updated.
  5) If test task exists and Done, jump to Pass 2; if exists but not Done, report status and stop.
- **Pass 2 flow (after test task Done):**
  1) Load Story/test task; read test plan/results and manual testing comment from Pass 1.
  2) Verify limits and priority: Priority ≤15; E2E 2-5, Integration 0-8, Unit 0-15, total 10-28; tests focus on business logic (no framework/DB/library tests).
  3) Ensure Priority ≤15 scenarios and Story AC are covered by tests; infra/docs updates present.
  4) **Calculate Quality Score and NFR validation** (see formulas above):
     - Run NFR checks per dimensions table
     - Assign issue prefixes: SEC-, PERF-, REL-, MNT-, TEST-, ARCH-, DOC-
     - Calculate Quality Score
  5) **Determine Gate verdict** per 4-Level Gate Model above

**TodoWrite format (mandatory):**
Add pass steps to todos before starting:
```
Pass 1:
- Invoke ln-501-code-quality-checker (in_progress)
- Pass 1.5: Criteria Validation (Story deps, AC coverage, DB schema) (pending)
- Run linters from tech_stack.md (pending)
- Invoke ln-502-regression-checker (pending)
- Invoke ln-510-test-planner (research + manual + auto tests) (pending)

Pass 2:
- Verify test task coverage (in_progress)
- Mark Story Done (pending)
```
Mark each as in_progress when starting, completed when done. On failure, mark remaining as skipped.

## Worker Invocation (MANDATORY)

| Step | Worker | Context | Rationale |
|------|--------|---------|-----------|
| Code Quality | ln-501-code-quality-checker | **Separate** (Task tool) | Independent analysis, focused on DRY/KISS/YAGNI |
| Regression | ln-502-regression-checker | **Shared** (direct Skill tool) | Needs Story context and previous check results |
| Test Planning | ln-510-test-planner | **Shared** (direct Skill tool) | Needs full Gate context for test planning |

**ln-501 invocation (Separate Context):**
```
Task(description: "Code quality check via ln-501",
     prompt: "Execute ln-501-code-quality-checker. Read skill from ln-501-code-quality-checker/SKILL.md. Story: {storyId}",
     subagent_type: "general-purpose")
```

**ln-501 result contract (Task tool return):**
Task tool returns worker's final message. Parse for YAML block:
- `verdict: PASS | CONCERNS | ISSUES_FOUND`
- `quality_score: 0-100`
- `issues: [{id, severity, finding, action}]`
- If verdict = ISSUES_FOUND → create refactor task (Backlog), stop Pass 1.

**ln-502 and ln-510:** Invoke via direct Skill tool — workers see Gate context.

**Note:** ln-510 orchestrates the full test pipeline (ln-511 research → ln-512 manual → ln-513 auto tests).

**❌ FORBIDDEN SHORTCUTS (Anti-Patterns):**
- Running `mypy`, `ruff`, `pytest` directly instead of invoking ln-501/ln-502
- Doing "minimal quality check" (just linters) and skipping ln-510 test planning
- Asking user "Want me to run the full skill?" after doing partial checks
- Marking steps as "completed" in todo without invoking the actual skill
- Any command execution that should be delegated to a worker skill

**✅ CORRECT BEHAVIOR:**
- Use `Skill(skill: "ln-50X-...")` for EVERY step — NO EXCEPTIONS
- Wait for each skill to complete before proceeding
- If skill fails → create fix task → STOP (fail fast)
- Never bypass skills with "I'll just run the command myself"

**ZERO TOLERANCE:** If you find yourself running quality commands directly (mypy, ruff, pytest, curl) instead of invoking the appropriate skill, STOP and use Skill tool instead.

## Critical Rules
- Early-exit: any failure creates a specific task and stops Pass 1/2.
- Single source of truth: rely on Linear metadata for tasks; kanban is updated by workers/ln-400.
- Task creation via skills only (ln-510/ln-301); this skill never edits tasks directly.
- Pass 2 only runs when test task is Done; otherwise return error/status.
- Language preservation in comments (EN/RU).

## Definition of Done
- Pass 1: ln-501 pass OR refactor task created; linters pass OR lint-fix task created; ln-502 pass OR regression-fix task created; ln-510 pipeline pass (research + manual + auto tests) OR bug-fix task created; test task created/updated; exits.
- Pass 2: test task verified (priority/limits/coverage/infra/docs); Quality Score calculated; NFR validation completed; Gate verdict determined (PASS/CONCERNS/FAIL/WAIVED).
- **Gate output format:**
  ```yaml
  gate: PASS | CONCERNS | FAIL | WAIVED
  quality_score: {0-100}
  nfr_validation:
    security: PASS | CONCERNS | FAIL
    performance: PASS | CONCERNS | FAIL
    reliability: PASS | CONCERNS | FAIL
    maintainability: PASS | CONCERNS | FAIL
  issues: [{id: "SEC-001", severity: high|medium|low, finding: "...", action: "..."}]
  ```
- Story set to Done (PASS/CONCERNS/WAIVED) or fix tasks created (FAIL); comment with gate verdict posted.

## Reference Files
- Criteria Validation: `references/criteria_validation.md` (Story deps, AC coverage quality, DB schema checks from ln-310)
- Gate levels: `references/gate_levels.md` (detailed scoring rules and thresholds)
- Workers: `../ln-501-code-quality-checker/SKILL.md`, `../ln-502-regression-checker/SKILL.md`
- Test planning orchestrator: `../ln-510-test-planner/SKILL.md` (coordinates ln-511/512/513)
- Tech stack/linters: `docs/project/tech_stack.md`

---
**Version:** 6.0.0 (BREAKING: Added Pass 1.5 Criteria Validation with 3 checks from ln-310 - Story dependencies, AC-Task Coverage Quality (STRONG/WEAK/MISSING), Database Creation Principle. New issue prefixes: DEP-, COV-, DB-, AC-. Closes validation-execution gap at Story level per BMAD Method best practices.)
**Last Updated:** 2026-02-03
