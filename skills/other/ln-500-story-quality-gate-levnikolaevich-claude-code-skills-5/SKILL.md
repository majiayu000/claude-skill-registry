---
name: ln-500-story-quality-gate
description: "Story-level quality orchestrator with 4-level Gate (PASS/CONCERNS/FAIL/WAIVED) and Quality Score. Delegates to ln-510 (quality) and ln-520 (tests), calculates final verdict."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Story Quality Gate

Thin orchestrator that coordinates quality checks and test planning, then determines final Story verdict.

## Purpose & Scope
- Invoke ln-510-quality-coordinator for code quality checks
- Invoke ln-520-test-planner for test planning (if needed)
- Calculate Quality Score and NFR validation
- Determine 4-level Gate verdict (PASS/CONCERNS/FAIL/WAIVED)
- Mark Story as Done or create fix tasks
- Delegates ALL work — never runs checks directly

## 4-Level Gate Model

| Level | Meaning | Action |
|-------|---------|--------|
| **PASS** | All checks pass, no issues | Story -> Done |
| **CONCERNS** | Minor issues, acceptable risk | Story -> Done with comment noting concerns |
| **FAIL** | Blocking issues found | Create fix tasks, return to ln-400 |
| **WAIVED** | Issues acknowledged by user | Story -> Done with waiver reason documented |

**Verdict calculation:** `FAIL` if any check fails. `CONCERNS` if minor issues exist. `PASS` if all clean.

## Quality Score

Formula: `Quality Score = 100 - (20 x FAIL_count) - (10 x CONCERN_count)`

| Score Range | Status | Action |
|-------------|--------|--------|
| 90-100 | Excellent | PASS |
| 70-89 | Acceptable | CONCERNS (proceed with notes) |
| 50-69 | Below threshold | FAIL (create fix tasks) |
| <50 | Critical | FAIL (urgent priority) |

## NFR Validation

| NFR | Checks | Issue Prefix |
|-----|--------|--------------|
| **Security** | Auth, input validation, secrets exposure | SEC- |
| **Performance** | N+1 queries, caching, response times | PERF- |
| **Maintainability** | DRY, SOLID, cyclomatic complexity, error handling | MNT- |

Additional prefixes: `TEST-` (coverage gaps), `ARCH-` (architecture), `DOC-` (documentation), `DEP-` (dependencies), `COV-` (AC coverage), `DB-` (database schema), `AC-` (AC validation)

## When to Use
- All implementation tasks in Story are Done
- User requests quality gate for Story
- ln-400-story-executor delegates quality check

## Workflow

### Phase 1: Discovery

1) Auto-discover team/config from `docs/tasks/kanban_board.md`
2) Load Story + task metadata from Linear (no full descriptions)
3) Detect test task status (exists? Done?)

### Phase 2: Fast-Track Decision

Stories with high readiness (validated pre-execution) can skip expensive checks.

```
IF readiness_score available in CONTEXT:
  IF readiness_score == 10:
    fast_track = true
  ELSE:
    fast_track = false
ELSE:
  fast_track = false    # No readiness data — full gate
```

**Fast-track matrix (readiness == 10):**

| Component | Full Gate | Fast-Track | Why |
|-----------|-----------|------------|-----|
| ln-514 regression tests | RUN | RUN | Always critical, cheap |
| Linters | RUN | RUN | Cheap, catches formatting |
| Criteria Validation (3 checks) | RUN | RUN | Cheap, validates AC coverage |
| ln-511 metrics + static analysis | RUN | **RUN** | **Catches complexity/DRY/dead code that per-task review misses** |
| ln-511 MCP Ref (OPT-, BP-, PERF-) | RUN | **SKIP** | Expensive external calls |
| ln-513 agent review | RUN | **SKIP** | Expensive external calls |
| ln-520 test planning | RUN | **SKIP** | Redundant for pre-validated |
| NFR validation | All dims | **Security only** | Perf/Maintainability less critical |

### Phase 3: Quality Checks (delegate to ln-510)

1) **Invoke ln-510-quality-coordinator** via Skill tool
   - Pass: Story ID (+ `--fast-track` flag if fast_track == true)
   - Full: ln-510 runs: code quality (ln-511) -> criteria validation -> linters -> regression (ln-514)
   - Fast-track: ln-510 runs: code metrics + static (ln-511 `--skip-mcp-ref`) -> criteria -> linters -> regression (ln-514) — skips MCP Ref/ln-513
2) **If ln-510 returns FAIL:**
   - Create fix/refactor tasks via ln-301
   - Stop — return to ln-400

### Phase 4: Test Planning (delegate to ln-520)

1) **IF fast_track: SKIP Phase 4 entirely** (proceed to Phase 5)
2) Check test task status:
   - **No test task** -> invoke ln-520-test-planner to create
   - **Test task exists, not Done** -> report status, stop
   - **Test task Done** -> proceed to Phase 5

2) **Invoke ln-520-test-planner** via Skill tool (if needed)
   - Pass: Story ID
   - ln-520 runs: research (ln-521) -> manual testing (ln-522) -> auto test planning (ln-523)

### Phase 5: Test Verification (after test task Done)

1) Load test task from Linear
2) Verify limits and priority:
   - Priority ≥15 scenarios covered
   - Each test passes Usefulness Criteria (no numerical targets)
   - Tests focus on business logic (no framework/DB/library tests)
3) Verify Story AC coverage by tests
4) Check infra/docs updates present

### Phase 6: Final Verdict

1) **Calculate Quality Score** (see formula above)
2) **Run NFR checks** per dimensions table (fast_track: Security only; full: all dimensions)
3) **Assign issue prefixes:** SEC-, PERF-, MNT-, TEST-, ARCH-, DOC-
4) **Determine Gate verdict** per 4-Level Gate Model
5) Post Linear comment with gate verdict
6) **If FAIL:** Record root cause analysis — classify each failure (missing_context | wrong_pattern | unclear_ac | doc_gap | test_gap). Append to `docs/project/architecture_health.md` under `## Root Cause Log` (create section if missing). Format: `| {date} | {story_id} | {issue_id} | {classification} | {action_taken} |`
7) Update Story status (Done for PASS/CONCERNS/WAIVED, or create fix tasks for FAIL)

**TodoWrite format (mandatory):**
```
- Invoke ln-510-quality-coordinator (in_progress)
- Check test task status (pending)
- Invoke ln-520-test-planner (pending, if needed)
- Verify test coverage (pending)
- Calculate Quality Score + NFR (pending)
- Determine verdict + update Story (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Purpose |
|-------|--------|---------|
| 2 | ln-510-quality-coordinator | Code quality + criteria + linters + regression |
| 3 | ln-520-test-planner | Research + manual testing + auto test planning |

**Invocation:**
```
Skill(skill: "ln-510-quality-coordinator", args: "{storyId}")
Skill(skill: "ln-520-test-planner", args: "{storyId}")
```

**Anti-Patterns:**
- Running mypy, ruff, pytest directly instead of invoking ln-510
- Running web searches or creating bash scripts instead of invoking ln-520
- Marking steps as completed without invoking the actual skill
- Any direct command execution that should be delegated

## Critical Rules
- Early-exit: any failure creates a specific task and stops
- Single source of truth: rely on Linear metadata for tasks
- Task creation via ln-301 only; this skill never edits tasks directly
- Test verification only runs when test task is Done
- Language preservation in comments (EN/RU)

## Definition of Done
- ln-510 quality checks: pass OR fix tasks created
- Test task status checked; ln-520 invoked if needed
- Test coverage verified (when test task Done)
- Quality Score calculated; NFR validation completed
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
- Story set to Done (PASS/CONCERNS/WAIVED) or fix tasks created (FAIL)
- Root cause analysis recorded in architecture_health.md for every FAIL verdict
- Comment with gate verdict posted

## Reference Files
- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Quality coordinator:** `../ln-510-quality-coordinator/SKILL.md`
- **Test planner:** `../ln-520-test-planner/SKILL.md`
- **Risk-based testing:** `shared/references/risk_based_testing_guide.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-09
