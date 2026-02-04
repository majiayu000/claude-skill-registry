---
name: better-bug-fix
description: Bug-fixing workflow that starts by writing a failing test to reproduce the bug, then uses subagents to propose fixes and verifies with passing tests. Use when a user reports a bug, asks to fix a bug, or wants a regression test first.
---

# Better Bug Fix

Follow a test-first debugging workflow that proves the bug and validates the fix.

## Workflow

1. Triage and scope the bug.
   - Restate the symptom and expected behavior in one sentence.
   - Identify the affected area (files, module, API, UI).

2. Write a minimal failing test first.
   - Add the smallest test that reproduces the bug.
   - Prefer existing test frameworks and patterns in the repo.
   - If no tests exist, create a minimal repro harness as close as possible to existing structure.

3. Run tests to confirm failure.
   - Execute the narrowest test command that includes the new test.
   - Record the failing output or error signature.

4. Delegate fixes to subagents.
   - Spawn 2-3 subagents with clear ownership of investigation/fix ideas.
   - Ask each to propose a fix and the rationale, referencing the failing test.
   - Keep their scopes non-overlapping (e.g., data flow, edge cases, API contract).

5. Implement the best fix.
   - Apply the most plausible fix based on test and codebase conventions.
   - Keep the change minimal and focused on the bug.

6. Prove the fix.
   - Re-run the failing test(s) and any relevant nearby tests.
   - Ensure the new test passes and no regressions are introduced.

7. Report clearly.
   - Explain the root cause, the test added, and why the fix works.
   - Call out any remaining risks or follow-ups.

## Guardrails

- Do not attempt a fix before a reproducing test exists.
- If a test cannot be written, explicitly explain why and propose the closest alternative (repro script or manual steps).
- Avoid refactors unless necessary to make the test feasible.
- Keep changes small; prefer surgical fixes.

## Subagent Prompt Template

Use this template when spawning subagents:

"""

You are a subagent investigating a bug. The reproducing test is failing. Please:

1. Identify the likely root cause in the code.
2. Propose a minimal fix.
3. Note any tradeoffs or additional tests to add.

**Stay within your assigned scope.**

"""
