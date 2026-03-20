---
description: Improves unit test coverage on demand — discovers testing gaps and generates tests that follow project conventions. Requires /optimus:init to have set up test infrastructure first. Conservative — only adds new test files, never refactors existing source code. Use when test coverage is low or after adding new code that lacks tests.
disable-model-invocation: true
---

# Unit Test Coverage Improvement

Improve unit test coverage for existing code. Requires `/optimus:init` to have set up test infrastructure (framework, coverage tooling, test-guardian agent, testing docs) first. Conservative by design — only adds new test files, never refactors or restructures existing source code. If code is untestable as-is, it flags it rather than changing it. Refactoring is the domain of `/optimus:refactor`.

## Step 1: Pre-flight

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, process each repo independently: run Steps 1–6 inside each repo that has `.claude/CLAUDE.md`. Report results per repo. If no repos have been initialized, suggest running `/optimus:init` first from the workspace root.

Check that `.claude/CLAUDE.md` exists. If it doesn't, stop and recommend running `/optimus:init` first — the project needs baseline context before test generation can be effective.

Beyond the init check, identify which guideline documents are available — they directly affect the quality of everything this skill does:

| Document | Role | Effect on skill |
|----------|------|-----------------|
| `coding-guidelines.md` | Primary quality reference | Tests follow naming conventions, code structure, quality standards |
| `testing.md` | Testing conventions | Framework, runner commands, mocking patterns, file organization |
| `.claude/CLAUDE.md` | Project overview | Tech stack signals, test runner commands |

**Monorepo path note:** Read the "Monorepo Scoping Rule" section of `$CLAUDE_PLUGIN_ROOT/skills/init/references/constraint-doc-loading.md` for doc layout and scoping rules. When generating tests for a subproject, load that subproject's `testing.md`, not another subproject's.

The skill operates differently depending on what exists:
- **All three docs** — matches existing conventions precisely
- **CLAUDE.md + coding-guidelines (no testing.md)** — derives conventions from the codebase
- **CLAUDE.md only (no guidelines either)** — still works, but with less project-specific guidance

### Scope

Parse optional path argument (e.g., `/optimus:unit-test src/api`) to limit scope. If no path is specified, default to the full project.

For monorepos and multi-repo workspaces, detect project structure using the same approach as `/optimus:init` — reference `$CLAUDE_PLUGIN_ROOT/skills/init/SKILL.md` Step 1 for detection logic (multi-repo workspace detection, workspace configs, manifest scanning, supporting signals). Process each project/repo independently.

## Step 2: Discovery

For each subproject (or the single project), scan for:

- **Existing test files** — `*.test.*`, `*.spec.*`, `*_test.*`, `__tests__/`, `tests/`, `test/`, `spec/`
- **Test framework** — configuration files and manifest dependencies (jest, vitest, mocha, pytest, junit, xunit, rspec, gtest, etc.)
- **Test runner commands** — from `testing.md`, `CLAUDE.md`, `package.json` scripts, `Makefile`, `Cargo.toml`, etc.
- **Coverage tooling** — whether coverage measurement is already configured and available

**Exclude git submodules:** Skip directories containing a `.git` *file* (not directory) — these are submodules pointing to external repositories and should not be scanned for test targets or test files.

Present a summary table to the user:

```
## Discovery Summary

| Property | Status |
|----------|--------|
| Test framework | [framework name] / Not detected |
| Test files found | [N] files |
| Test runner command | [command] / Not found |
| Coverage tooling | [tool name] / Not configured |
```

**If no test framework is detected**, stop and report: "No test framework found. Run `/optimus:init` (or re-run it) to install a test framework and set up test infrastructure before using this skill." Do not proceed to test generation without a working framework.

## Step 3: Coverage Analysis and Achievable Threshold Estimation

Before writing any tests:

1. **Run existing test suite.** If tests fail:
   - **Test assertion failures** (tests compile and run, but some fail) — stop and report. A clean baseline is required before adding new tests. Report failing tests in the Step 6 "Bugs Discovered" section.
   - **Build/bootstrap failures** — stop and report. Test infrastructure should have been verified by `/optimus:init`. Recommend re-running `/optimus:init` to fix build-level issues.

2. **Measure baseline coverage:**
   - If coverage tooling is available → run coverage and record baseline numbers
   - If coverage tooling is NOT configured → do heuristic gap analysis (source files vs test files by naming convention)

3. **Estimate achievable coverage** without requiring risky refactoring:
   - **Testable code** — pure functions, exported APIs, business logic with clear inputs/outputs, utility modules, data transformations
   - **Untestable without refactoring** — hardcoded dependencies, tightly coupled modules, inline DB/HTTP calls without injection, deeply nested side effects, global state mutations

4. **Present to the user:**

```
## Coverage Analysis

- Current coverage: [X]%
- Estimated achievable without refactoring: ~[Y]%
- Gap requiring structural changes: ~[Z]%

The remaining ~[Z]% would require structural changes (dependency injection,
repository pattern extraction, etc.) — that's the domain of /optimus:refactor.
```

This sets clear expectations and reinforces the conservative constraint.

## Step 4: Test Generation Plan

Create a prioritized list, **capped at 10 items per run**:

1. **Exported/public functions and classes** — API surface, highest value
2. **Pure functions and utility modules** — easiest to test, highest ROI
3. **Business logic with clear inputs/outputs** — core functionality
4. **Complex branching logic** — high cyclomatic complexity, most likely to have bugs
5. **Internal/private helpers** — lower priority, test through public API when possible

**Skip** (flag in summary, don't attempt):
- Code that's untestable without refactoring
- Generated code (protobuf, OpenAPI, ORM migrations)
- Migration files
- Declarative configuration
- Thin wrappers with no logic

Present the plan, then use `AskUserQuestion` — header "Plan", question "How would you like to proceed with the test generation plan?":
- **Approve all** — "Generate tests for all planned items"
- **Selective** — "Choose specific items by number"
- **Skip** — "No tests — keep the plan as reference"

If the user selects **Selective**, ask which item numbers to proceed with (e.g., "1, 3, 5").

## Step 5: Test Writing

### Quality standards

Tests must follow:
- `coding-guidelines.md` for quality standards (naming, structure, clarity)
- `testing.md` for testing conventions (framework idioms, file naming, directory structure)
- `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/testing-anti-patterns.md` for mocking discipline — prefer real code over mocks, never assert on mock behavior, mock only external services or non-deterministic dependencies
- Existing test files for concrete patterns to replicate: import style, assertion library, file naming convention, directory placement, shared fixtures (conftest/setup files, factories, beforeAll/setUp blocks), and describe/it or class/method test organization. Extract these patterns **before writing the first test** and apply them consistently to all generated tests.

### Before writing each test

Answer these gate questions — fix any "no" before proceeding:

1. **File placement** — Does a test file for this module already exist? If yes, add tests there instead of creating a new file. New files must follow the naming convention from `testing.md` (typically `test_<module_name>` or `<module_name>.test`).
2. **Fixtures and helpers** — Do existing test files or shared setup files (conftest.py, test helpers, factories) already provide fixtures for the data this test needs? Use them instead of creating private helpers that duplicate existing setup.
3. **Mocking and assertion discipline** — apply the gate questions from `$CLAUDE_PLUGIN_ROOT/skills/tdd/references/testing-anti-patterns.md` (already referenced in Quality standards above).
4. **Setup duplication** — apply the DRY principle from `coding-guidelines.md` to test setup: repeated setup should be extracted to shared fixtures (setUp/beforeEach, conftest, factories).

### Conservative constraint

**Only add new test files.** Never refactor or modify existing source code — refactoring is the domain of `/optimus:refactor`. If a function can't be tested without changing its signature or extracting dependencies, flag it in the summary instead of changing it.

### Per-test workflow

For each approved item:
1. Write the test file
2. Self-review against the "Before writing each test" checklist above — fix any violations before running
3. Run it immediately
4. If the test fails:
   - Fix the **test** (not the source code) — max 3 fix attempts
   - If still failing after 3 attempts, flag as untestable and move on
   - If the failure reveals an actual **bug in existing code**, report the bug but do not fix it
5. Move to the next item

### Final verification

After all tests are written, run the **full test suite** to ensure no regressions. Follow the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — run tests fresh, read complete output, and report actual results with evidence before claiming success.

## Step 6: Summary

Report to the user:

```
## Unit Test Summary

### Coverage
- Coverage tooling: [tool name / not configured]
- Before: [X]% → After: [Y]%
- Achievable target (without refactoring): ~[Z]%

### Tests Created
| # | File | Target | Status |
|---|------|--------|--------|
| 1 | src/__tests__/auth.test.ts | auth module exports | ✓ Pass |
| 2 | src/__tests__/validate.test.ts | validation utilities | ✓ Pass |
| ... | ... | ... | ... |

### Bugs Discovered
- [List of bugs found in existing code — reported, not fixed]

### Not Testable Without Refactoring
- [List of code flagged as untestable — with brief explanation of what structural change would be needed]
- To address these, run `/optimus:refactor` to review and restructure the code first.
```

For multi-repo workspaces, present results per repo (one summary block per repo) and include the repo name/path in each section header.

Recommend running `/optimus:refactor` to review code quality, or `/optimus:tdd` to continue development with test-driven workflow.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.
