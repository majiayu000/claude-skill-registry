---
name: ln-502-regression-checker
description: Worker that runs existing tests to catch regressions. Auto-detects framework, reports pass/fail. No status changes or task creation.
---

# Regression Checker

Runs the existing test suite to ensure no regressions after implementation changes.

## Purpose & Scope
- Detect test framework (pytest/jest/vitest/go test/etc.) and test dirs.
- Execute full suite; capture results for Story quality gate.
- Return PASS/FAIL with counts/log excerpts; never modifies Linear or kanban.

## When to Use
- **Invoked by ln-500-story-quality-gate** Pass 1 (after ln-501)
- Code quality check passed
- Before test planning pipeline (ln-510)

## Workflow (concise)
1) Auto-discover framework and test locations from repo config/files.
2) **Read `docs/project/runbook.md`** — get exact test commands, Docker setup, environment variables. Use commands from runbook, NOT guessed commands.
3) Build appropriate test command; run with timeout (~5m); capture stdout/stderr.
4) Parse results: passed/failed counts; key failing tests.
5) Output verdict JSON (PASS or FAIL + failures list) and add Linear comment.

## Critical Rules
- No selective test runs; run full suite.
- Do not fix tests or change status; only report.
- Language preservation in comment (EN/RU).

## Definition of Done
- Framework detected; command executed.
- Results parsed; verdict produced with failing tests (if any).
- Linear comment posted with summary.

## Reference Files
- Risk-based limits used downstream: `../ln-510-test-planner/references/risk_based_testing_guide.md`

---
**Version:** 3.1.0 (Added mandatory runbook.md reading before test execution)
**Last Updated:** 2026-01-09
