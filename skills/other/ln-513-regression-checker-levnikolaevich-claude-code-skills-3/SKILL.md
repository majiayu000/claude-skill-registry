---
name: ln-513-regression-checker
description: "Runs existing test suite to catch regressions after implementation changes. Use when Story needs regression verification. No status changes."
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Regression Checker

**Type:** L3 Worker
**Category:** 5XX Quality

Runs the existing test suite to ensure no regressions after implementation changes.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Story Resolution Chain.
**Status filter:** To Review

## Purpose & Scope
- Detect test framework (pytest/jest/vitest/go test/etc.) and test dirs.
- Execute full suite; capture stdout/stderr for Story quality gate.
- Return PASS/FAIL with counts/log excerpts; never modifies Linear or kanban.
- Preserve full stdout/stderr output for downstream log analysis.

## When to Use
- After code quality checks pass
- Code quality check passed

## Workflow

### Phase 0: Resolve Inputs

**MANDATORY READ:** Load `references/input_resolution_pattern.md`, `references/ci_tool_detection.md`

1. **Resolve storyId:** Run Story Resolution Chain per guide (status filter: [To Review]).

### Phase 1: Execute Tests

**MANDATORY READ:** Load `references/output_normalization.md`

Read target project files if they exist: `docs/project/infrastructure.md`, `docs/project/runbook.md`

1) Auto-discover test framework per ci_tool_detection.md Command Registry (Test Frameworks section).
2) Get service endpoints, port allocation from infrastructure.md. Get exact test commands, Docker setup, environment variables from runbook.md. Runbook commands take priority over auto-detection (per ci_tool_detection.md Discovery Hierarchy).
3) Build appropriate test command; run with timeout (5min per ci_tool_detection.md); capture stdout/stderr.
4) Parse results: passed/failed counts; key failing tests.
5) **Normalize + group failures:** Apply `references/output_normalization.md` §1-§3 to test output. Group failing tests by error category (Import/Module, Assertion, Timeout, Type, Connection, Runtime). Report grouped: e.g., "3 Import errors in auth/, 2 Assertion mismatches in payment/".
6) Output verdict JSON (PASS or FAIL + grouped failures list) and add Linear comment.

## Critical Rules
- No selective test runs; run full suite.
- Do not fix tests or change status; only report.
- Language preservation in comment (EN/RU).

## Runtime Summary Artifact

**MANDATORY READ:** Load `references/quality_summary_contract.md`, `references/quality_worker_runtime_contract.md`

Runtime profile:
- family: `quality-worker`
- worker: `ln-513`
- summary kind: `quality-worker`
- payload fields used by coordinators: `worker`, `status`, `verdict`, `issues`, `warnings`, `artifact_path`

Invocation rules:
- standalone: omit `runId` and `summaryArtifactPath`
- managed: pass both `runId` and exact `summaryArtifactPath`
- always write the validated summary before terminal outcome

**Monitor (2.1.98+):** For test suite commands expected >30s, use `Monitor`. Fallback: `Bash(run_in_background=true)`.

## Definition of Done

- [ ] Framework detected; command executed
- [ ] Results parsed; verdict produced with failing tests (if any)
- [ ] Tracker comment posted with summary

## Reference Files
- Risk-based limits used downstream: `references/risk_based_testing_guide.md`
- **CI tool detection:** `references/ci_tool_detection.md`
- **Output normalization:** `references/output_normalization.md`
- **Pytest patterns:** `references/pytest_configuration.md`

---
**Version:** 3.1.0
**Last Updated:** 2026-01-09
