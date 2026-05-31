---
name: fixflow
description: "Execute coding tasks with a strict delivery workflow: build a full plan, implement one step at a time, run tests continuously, and commit by default after each step (`per_step`). Support explicit commit policy overrides (`final_only`, `milestone`) and optional BDD (Given/When/Then) when users ask for behavior-driven delivery or requirements are unclear."
---

# Fixflow

## Overview

Use this skill to deliver end-to-end engineering work in one run:
- Plan fully.
- Execute in strict sequence.
- Validate continuously.
- Use explicit commit policy (`per_step` default; `final_only`/`milestone` when requested).
- Add BDD behavior specs when requested or when requirements are ambiguous.

## Trigger Cues

Trigger this skill when the user asks for one or more of:
- Full plan + sequential execution.
- No backward compatibility.
- Test everything before handoff.
- Commit after completion or commit before each next step.
- Behavior-driven delivery (BDD) or acceptance scenarios.

## Workflow

### 1. Define Ready Criteria (DoR)

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

### 2. Build Complete Plan Before Editing

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

### 3. Add BDD/TDD Layer When Needed

Use BDD if user requests it, or if requirements are unclear.

#### 3.0 TDD Mode (RED -> GREEN -> IMPROVE)

When user requests TDD or test-driven delivery:

1. **RED** — Write a failing test first
   - Extract testable behavior from requirements
   - Write minimal test case asserting expected behavior
   - Run test, confirm it fails (red)
   - If test passes unexpectedly -> requirement already met or test is wrong

2. **GREEN** — Write minimal implementation
   - Write just enough code to make the test pass
   - No extra improvements, no "while I'm here" changes
   - Run test, confirm it passes (green)

3. **IMPROVE** — Refactor under green tests
   - Eliminate duplication, improve naming, simplify logic
   - Run tests after each refactor to confirm no regression
   - Refactoring must not change external behavior

Coverage target: 80% line coverage for new code, 100% for critical paths.

Trigger cues for TDD mode:
- User says "TDD", "test-driven", "test first"
- User says "write tests before code"
- Requirements are well-defined with clear inputs/outputs

For BDD Lite, Scenario Quality Checklist, Scenario Outline, and Test Layer mapping, see the shared reference:

> [`references/bdd-guide.md`](./references/bdd-guide.md)


### 4. Execute Step by Step

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

For `per_step` (default):
  - Stage only files for current step.
  - Run step-level checks.
  - Commit immediately after step checks pass.
  - Record step -> commit hash mapping.

### 5. Apply No-Backward-Compatibility Mode (When Requested)

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

### 6. Validate with Test Matrix (Verification Loop)

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

### 7. Commit and Handoff

> See shared delivery base: [`references/delivery-base.md`](./references/delivery-base.md)

## Guardrails

- Do not stop at planning when implementation is expected.
- Do not leave partially completed plan steps.
- Do not defer required testing when it can be run now.
- Do not default to `final_only`; use `per_step` unless user explicitly asks otherwise.
- Do not move to the next plan step before committing when `commit_policy = per_step`.
- Do not claim compatibility if user explicitly requested no compatibility work.
- Do not include unrelated pre-existing dirty files in commits.
- Do not hand off without concrete validation evidence.
