---
name: 60-validate-tests-150
description: "[60] VALIDATE. Ensure new (staged and unstaged) changes are covered by tests at >70% and the full test suite is green. Use when asked to validate coverage for recent changes, add tests for modified code, or verify nothing else broke."
---

# Validate-Tests 150 Protocol

## Goal

Cover current uncommitted changes with meaningful tests at >70% coverage (including **the changed lines**) and confirm the entire test suite is green.

## Workflow

1. **Identify current changes**
   - Check staged and unstaged changes (`git status`).
   - List changed files (`git diff --name-only` and `git diff --name-only --staged`).
   - Focus testing on these files and their direct dependencies.

2. **Find the coverage command**
   - Check `package.json` scripts for `test`, `coverage`, or `ci`.
   - If unclear, search for Jest/Vitest config files and default coverage options.

3. **Run coverage**
   - Execute the project’s coverage command.
   - Save the exact overall percentage and per‑file coverage for changed files (lines/branches).
   - Passing tests ≠ coverage: verify that **the changed lines** are executed (use coverage reports to confirm).

4. **Prioritize targets**
   - Start with changed files that are <70% covered.
   - Prefer pure functions, utilities, and deterministic logic.

5. **Add tests**
   - Write tests that directly exercise the **changed logic/markup** and assert behavior, edge cases, and failure paths.
   - Prefer behavior- or structure-level assertions that map to the changed lines (e.g., DOM structure/classes for UI changes).
   - Avoid snapshot‑only tests unless behavior is visual and stable.

6. **Re‑run coverage**
   - Confirm each changed file is **> 70%** covered (lines/branches where available).
   - Confirm the **specific changed lines** are covered (use coverage reports or direct evidence in tests).
   - If coverage tooling only provides overall numbers, explain the limitation and justify how tests exercise the changed code.
   - If not met, repeat steps 4–6.

7. **Run full test suite**
   - Execute the standard full test command for the repo (not just a subset).
   - Ensure all tests are green.

8. **Run lint**
   - Execute the standard lint command for the repo.
   - Ensure lint is green and **fix lint errors** introduced or surfaced in the process.
   - Do not leave lint in a failing state.

9. **Run compile**
   - Execute the standard compile command for the repo `npm run compile` or `tsc --noEmit`
   - Ensure compile is green and **fix compile errors** introduced or surfaced in the process.
   - Do not leave compile in a failing state.

10. **Report**
   - Summarize added tests, coverage changes, and full test results.
   - Note any files intentionally excluded or skipped and why.

## Validation checklist

- [ ] Staged and unstaged changes identified.
- [ ] Coverage command found and recorded.
- [ ] Baseline coverage captured.
- [ ] Tests added for changed files and direct dependencies.
- [ ] Changed files are >70% covered (lines/branches where available).
- [ ] Full test suite executed.
- [ ] All tests are green.
- [ ] Lint executed and green.
- [ ] Compile executed and green.

## Output expectations

- Provide the command used to measure coverage, to run the full test suite, and to run lint.
- Provide before/after coverage numbers and per‑file coverage for changed files.
- Explicitly state how the **changed lines** are exercised by the tests.
- List which files were targeted and why.
- Confirm the final threshold is met for changed files, or report remaining gaps.
- Confirm all tests and lint are green.
- Confirm compile is green.
