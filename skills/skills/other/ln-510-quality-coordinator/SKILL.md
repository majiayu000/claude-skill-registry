---
name: ln-510-quality-coordinator
description: "Coordinates code quality checks: ln-511 code quality, ln-512 tech debt cleanup, ln-513 agent review, ln-514 regression. Sequential pipeline, returns results to ln-500."
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Quality Coordinator

Sequential coordinator for code quality pipeline. Invokes 4 workers in index order (511 -> 512 -> 513 -> 514) and returns aggregated results to ln-500.

## Purpose & Scope
- Invoke ln-511-code-quality-checker (metrics, MCP Ref, static analysis)
- Invoke ln-512-tech-debt-cleaner (auto-fix safe findings from ln-511)
- Invoke ln-513-agent-reviewer (external agent reviews on cleaned code)
- Run Criteria Validation (Story dependencies, AC-Task Coverage, DB Creation Principle)
- Run linters from tech_stack.md
- Invoke ln-514-regression-checker (test suite after all changes)
- Return aggregated quality results to ln-500-story-quality-gate
- **No verdict determination** — ln-500 decides final Gate verdict

## When to Use
- **Invoked by ln-500-story-quality-gate** Phase 2
- All implementation tasks in Story status = Done

## Workflow

### Phase 1: Discovery

1) Auto-discover team/config from `docs/tasks/kanban_board.md`
2) Load Story + task metadata from Linear (no full descriptions)

**Fast-track mode:** When invoked with `--fast-track` flag (readiness 10/10), run Phase 2 with `--skip-mcp-ref` (metrics + static only, no MCP Ref), skip Phase 3 (ln-512), Phase 4 (ln-513). Run Phase 5 (criteria), Phase 6 (linters), Phase 7 (ln-514).

**Input:** Story ID from ln-500-story-quality-gate

### Phase 2: Code Quality (delegate to ln-511 — ALWAYS runs)

> **MANDATORY STEP:** ln-511 invocation required in ALL modes.
> **Full gate:** ln-511 runs everything (metrics + MCP Ref + static analysis).
> **Fast-track:** ln-511 runs with `--skip-mcp-ref` (metrics + static analysis only — catches complexity, DRY, dead code without expensive MCP Ref calls).

1) **Invoke ln-511-code-quality-checker** via Skill tool
   - Full: ln-511 runs code metrics, MCP Ref validation (OPT/BP/PERF), static analysis
   - Fast-track: ln-511 runs code metrics + static analysis only (skips OPT-, BP-, PERF- MCP Ref checks)
   - Returns verdict (PASS/CONCERNS/ISSUES_FOUND) + code_quality_score + issues list
2) **If ln-511 returns ISSUES_FOUND** -> aggregate issues, continue (ln-500 decides action)

**Invocation:**
```
# Full gate:
Skill(skill: "ln-511-code-quality-checker", args: "{storyId}")
# Fast-track:
Skill(skill: "ln-511-code-quality-checker", args: "{storyId} --skip-mcp-ref")
```

### Phase 3: Tech Debt Cleanup (delegate to ln-512 — SKIP if --fast-track)

> **MANDATORY STEP (full gate):** ln-512 invocation required. Safe auto-fixes only (confidence >=90%).
> **Fast-track:** SKIP this phase.

1) **Invoke ln-512-tech-debt-cleaner** via Skill tool
   - ln-512 consumes findings from ln-511 output (passed via coordinator context)
   - Filters to auto-fixable categories (unused imports, dead code, deprecated aliases)
   - Applies safe fixes, verifies build integrity, creates commit
2) **If ln-512 returns BUILD_FAILED** -> all changes reverted, aggregate issue, continue

**Invocation:**
```
Skill(skill: "ln-512-tech-debt-cleaner", args: "{storyId}")
```

### Phase 4: Agent Review (delegate to ln-513 — SKIP if --fast-track)

> **MANDATORY STEP (full gate):** ln-513 invocation required. Returns SKIPPED gracefully if agents unavailable.
> **Fast-track:** SKIP this phase.

1) **Invoke ln-513-agent-reviewer** via Skill tool
   - ln-513 runs external agents (Codex + Gemini) in parallel on cleaned code
   - Critically verifies each suggestion, debates if disagreeing
   - Returns filtered suggestions with confidence scoring
2) **Merge suggestions into issues list** (same prefixes: SEC-, PERF-, MNT-, ARCH-, BP-, OPT-)
3) **If verdict = SUGGESTIONS with area=security or area=correctness** -> escalate aggregate to CONCERNS

**Invocation:**
```
Skill(skill: "ln-513-agent-reviewer", args: "{storyId}")
```

### Phase 5: Criteria Validation

**MANDATORY READ:** Load `references/criteria_validation.md`

| Check | Description | Fail Action |
|-------|-------------|-------------|
| #1 Story Dependencies | No forward deps within Epic | [DEP-] issue |
| #2 AC-Task Coverage | STRONG/WEAK/MISSING scoring | [COV-]/[BUG-] issue |
| #3 DB Creation Principle | Schema scope matches Story | [DB-] issue |

### Phase 6: Linters
**MANDATORY READ:** `shared/references/ci_tool_detection.md` (Discovery Hierarchy + Command Registry)

1) Detect lint/typecheck commands per ci_tool_detection.md discovery hierarchy
2) Run all detected checks (timeouts per guide: 2min linters, 5min typecheck)
3) **If any check fails** -> aggregate issues, continue

### Phase 7: Regression Tests (delegate to ln-514)

1) **Invoke ln-514-regression-checker** via Skill tool
   - Runs full test suite, reports PASS/FAIL
   - Runs AFTER ln-512 changes to verify nothing broke
2) **If regression FAIL** -> aggregate issues, continue

**Invocation:**
```
Skill(skill: "ln-514-regression-checker", args: "{storyId}")
```

### Phase 8: Return Results

Return aggregated results to ln-500:

```yaml
quality_check: PASS | CONCERNS | ISSUES_FOUND
code_quality_score: {0-100}
agent_review: CODE_ACCEPTABLE | SUGGESTIONS | SKIPPED
criteria_validation: PASS | FAIL
linters: PASS | FAIL
tech_debt_cleanup: CLEANED | NOTHING_TO_CLEAN | BUILD_FAILED | SKIPPED
regression: PASS | FAIL
issues:
  - {id: "SEC-001", severity: high, finding: "...", source: "ln-511"}
  - {id: "OPT-001", severity: medium, finding: "...", source: "ln-513"}
  - {id: "DEP-001", severity: medium, finding: "...", source: "criteria"}
  - {id: "LINT-001", severity: low, finding: "...", source: "linters"}
```

**TodoWrite format (mandatory):**
```
- Invoke ln-511-code-quality-checker (in_progress)
- Invoke ln-512-tech-debt-cleaner (pending)
- Invoke ln-513-agent-reviewer (pending)
- Criteria Validation (Story deps, AC coverage, DB schema) (pending)
- Run linters from tech_stack.md (pending)
- Invoke ln-514-regression-checker (pending)
- Return results to ln-500 (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 2 | ln-511-code-quality-checker | Shared (Skill tool) — code metrics, MCP Ref, static analysis |
| 3 | ln-512-tech-debt-cleaner | Shared (Skill tool) — auto-fix safe findings from ln-511 |
| 4 | ln-513-agent-reviewer | Shared (Skill tool) — external agent reviews on cleaned code |
| 7 | ln-514-regression-checker | Shared (Skill tool) — full test suite after all changes |

**All workers:** Invoke via Skill tool — workers see coordinator context. Sequential execution: 511 -> 512 -> 513 -> 514.

**Anti-Patterns:**
- Running mypy, ruff, pytest directly instead of invoking ln-511/ln-514
- Running agent reviews directly instead of invoking ln-513
- Auto-fixing code directly instead of invoking ln-512
- Marking steps as completed without invoking the actual skill
- Determining final verdict (that's ln-500's responsibility)

## Critical Rules
- Return all results to ln-500; do NOT determine verdict
- Single source of truth: rely on Linear metadata for tasks
- Language preservation in comments (EN/RU)
- Do not create tasks or change statuses; ln-500 decides next actions

## Definition of Done
- ln-511 invoked (ALWAYS — full or `--skip-mcp-ref` in fast-track), code quality score returned
- ln-512 invoked (or skipped if --fast-track), tech debt cleanup results returned
- ln-513 invoked (or skipped if --fast-track), agent review results returned
- Criteria Validation completed (3 checks)
- Linters executed
- ln-514 invoked, regression results returned
- Aggregated results returned to ln-500

## Reference Files
- Criteria Validation: `references/criteria_validation.md`
- Gate levels: `references/gate_levels.md`
- Workers: `../ln-511-code-quality-checker/SKILL.md`, `../ln-512-tech-debt-cleaner/SKILL.md`, `../ln-513-agent-reviewer/SKILL.md`, `../ln-514-regression-checker/SKILL.md`
- Caller: `../ln-500-story-quality-gate/SKILL.md`
- Test planning (separate coordinator): `../ln-520-test-planner/SKILL.md`
- Tech stack/linters: `docs/project/tech_stack.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-09
