---
verified: true
lastVerifiedAt: 2026-02-18T21:55:39.677Z
name: tdd
description: Canon TDD for humans and AI agents. Use for production code changes by writing tests first, proving RED, implementing minimal GREEN, and refactoring safely.
version: 1.2
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
aliases: [testing-expert]
best_practices:
  - Keep a visible test scenario backlog and execute one scenario at a time
  - Prove RED before code changes and keep evidence in command output
  - Implement smallest GREEN patch that satisfies current failing test only
  - Use bounded repair loops and anti-test-hacking checks before completion
error_handling: strict
streaming: supported
---

# Test-Driven Development (TDD)

## Overview

This skill implements Canon TDD with AI-specific guardrails:

1. Build or update a scenario list.
2. Execute exactly one scenario as a runnable test.
3. Prove RED.
4. Implement minimum change for GREEN.
5. Optionally refactor.
6. Repeat until scenario list is empty.

## When to Use

Use for:

- New features
- Bug fixes
- Behavior changes
- Repository-scale patching driven by tests
- AI-assisted code generation where tests are executable specifications

Ask human approval before bypassing only for:

- Throwaway prototypes
- Purely declarative config edits with no execution path
- One-off migration scripts that will not be maintained

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If code was written first, discard and restart from RED.

## Canon Loop

### Step 0: Create/refresh scenario backlog

- Keep a short ordered list of test scenarios for this task.
- Prioritize by design signal and risk, not by implementation convenience.
- Add discovered scenarios during execution.

### Step 1: Pick exactly one scenario and write one runnable test

- One behavior per cycle.
- Use clear behavior names.
- Favor real collaborators; mock only external boundaries.

### Step 2: Prove RED

- Run the narrowest test command.
- Failure must be due to missing behavior, not syntax or setup errors.
- Record red evidence (test file and failing assertion message).

### Step 3: Implement minimum GREEN patch

- Implement only what current red test requires.
- No speculative APIs or unrelated cleanup.
- Keep patch bounded to current scenario.

### Step 4: Prove GREEN

- Re-run narrow test command.
- Run impacted suite (or package-level test set).
- Confirm no regressions.

### Step 5: Optional refactor

- Refactor only with green tests.
- Re-run the same test set after refactor.

### Step 6: Repeat until backlog empty

## AI-Assisted Guardrails

- Use tests as executable prompt context; keep prompts short and test-focused.
- Prefer deterministic tests (stable fixtures, no nondeterministic ordering).
- Use bounded repair loops: max 3 repair attempts per scenario before redesign.
- Run anti-test-hacking checks:
  - Verify changed assertions still express original requirement.
  - Add at least one negative test for bug-fix tasks.
- Ensure code does not branch on test-only artifacts.

## Memory Acceleration Layer

Use lightweight memory only to reduce repeated setup and triage:

- preferred repo-local test/lint/format commands
- recurring failure signatures and short fix summaries
- recurring anti-pattern reminders
- reusable scenario templates

Reference: `references/tdd-memory-profile.md`

Hard rules:

- memory never bypasses RED proof
- memory never changes Canon sequence
- keep profile bounded and low-noise

## Repository-Scale and Class-Level Guidance

- For repository-scale work, decompose by failing test cluster and assign one cluster per loop.
- For class-level synthesis, derive a method dependency order and implement one method at a time with method-level public tests.
- Keep long-context pressure low by limiting each loop to one scenario and one patch objective.

## Verification Checklist

- [ ] Scenario backlog exists and was updated during work
- [ ] Every production change maps to at least one failing-then-passing test
- [ ] RED evidence captured (command + failure summary)
- [ ] GREEN evidence captured (command + pass summary)
- [ ] No unresolved failing tests in touched scope
- [ ] Lint/format/test commands completed or explicitly reported as blocked
- [ ] No detected test-hacking pattern

## Pre-Completion Commands (Project-Scoped)

Use the project's actual commands. Typical sequence:

```bash
# 1) targeted test
pnpm test <target>
# 2) impacted suite
pnpm test
# 3) lint
pnpm lint
# 4) format check
pnpm format:check
```

If the repo uses different scripts, replace these with local equivalents and report exactly what ran.

## Rationalization Countermeasures

- "I will add tests later" -> stop and write current red test.
- "This is too small to test" -> write one minimal behavior test.
- "I already manually tested" -> manual runs do not replace executable regression tests.
- "I spent too long to delete pre-test code" -> sunk cost; restart from RED.

## Related Files

- `references/research-requirements.md`
- `references/tdd-memory-profile.md`
- `testing-anti-patterns.md`
- `rules/tdd.md`
- `templates/implementation-template.md`

## Research Basis

This skill is aligned with:

- Martin Fowler TDD (Dec 11, 2023)
- Kent Beck Canon TDD (Dec 11, 2023)
- Rafique & Misic meta-analysis, IEEE TSE DOI:10.1109/TSE.2012.28
- LLM4TDD (arXiv:2312.04687)
- Test-Driven Development for Code Generation (arXiv:2402.13521)
- Tests as Prompt (arXiv:2505.09027)
- SWE-Flow (arXiv:2506.09003)
- TDFlow (arXiv:2510.23761)
- Scaling TDD from Functions to Classes (arXiv:2602.03557)

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

Assume interruption: if it is not in memory, it did not happen.
