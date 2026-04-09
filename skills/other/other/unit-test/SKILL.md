---
description: Improves unit test coverage on demand — discovers testing gaps and generates tests that follow project conventions. Requires /optimus:init to have set up test infrastructure first. Conservative — only adds new test files, never refactors existing source code. Supports `deep harness` mode for an automated multi-cycle unit-test + testability-refactor loop with fresh context per phase. Use when test coverage is low, after adding new code that lacks tests, or when you want an automated coverage-improvement harness.
disable-model-invocation: true
---

# Unit Test Coverage Improvement

Improve unit test coverage for existing code. Requires `/optimus:init` to have set up test infrastructure (framework, coverage tooling, testing docs) first. Conservative by design — only adds new test files, never refactors or restructures existing source code. If code is untestable as-is, it flags it rather than changing it. Refactoring is the domain of `/optimus:refactor`.

## Step 1: Pre-flight

### Parse invocation arguments

Extract from the user's arguments:
1. `deep` flag (present/absent)
2. `harness` keyword after `deep` (present/absent)
3. A number immediately after `deep` or `deep harness` → cycle cap (optional, default 5, hard cap 10)
4. Everything else → scope instructions (optional path)

Examples:
- `/optimus:unit-test` → normal mode, full project
- `/optimus:unit-test src/api` → normal mode, scoped
- `/optimus:unit-test deep` → deep mode (5 cycles)
- `/optimus:unit-test deep 3` → deep mode (3 cycles)
- `/optimus:unit-test deep harness` → harness mode, 5 cycles
- `/optimus:unit-test deep harness 5 "src/api"` → harness mode, scoped

### Harness mode detection

**If system prompt contains `HARNESS_MODE_ACTIVE`:**
→ Read `$CLAUDE_PLUGIN_ROOT/references/coverage-harness-mode.md`
→ Follow the "Unit-Test Phase Execution" section
→ Skip user confirmation (no `AskUserQuestion`)
→ Skip loops — run Steps 2–4 exactly once, then output structured JSON and stop

**If `harness` keyword detected in arguments:**
→ Read `$CLAUDE_PLUGIN_ROOT/references/coverage-harness-mode.md` Skill-Triggered Invocation section
→ Pass: `max_cycles` (from step 1 parsing), `scope` (from step 1 parsing)
→ The invocation section will resolve the Python environment, build the terminal command pointing to `scripts/test-coverage-harness/main.py`, present it, and stop
→ Do NOT proceed to Step 2

### Pre-flight checks

Read `$CLAUDE_PLUGIN_ROOT/skills/init/references/multi-repo-detection.md` for workspace detection. If a multi-repo workspace is detected, process each repo independently: run Steps 1-5 inside each repo that has `.claude/CLAUDE.md`. Report results per repo. If no repos have been initialized, suggest running `/optimus:init` first from the workspace root.

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

## Step 2: Discovery & Coverage Analysis (agent-assisted)

Delegate test infrastructure scanning, test execution, and coverage analysis to a reconnaissance agent to keep the main context clean for test writing.

For each subproject (or the single project):

Read `$CLAUDE_PLUGIN_ROOT/skills/unit-test/agents/shared-constraints.md` for agent constraints.
Read `$CLAUDE_PLUGIN_ROOT/skills/unit-test/agents/test-infrastructure-analyzer.md` for the full prompt template, scanning patterns, execution rules, and return format for the Test Infrastructure Analyzer Agent.

Launch 1 `general-purpose` Agent tool call using the prompt from test-infrastructure-analyzer.md, prepended with the shared constraints.

| Agent | Role | Runs when |
|-------|------|-----------|
| 1 — Test Infrastructure Analysis | Scan test files/frameworks/runners, run existing tests, measure coverage, classify code testability | Always |

Wait for the agent to complete.

### Stop gates (evaluated from agent results)

**If no test framework is detected** in the agent's Discovery Results, stop and report: "No test framework found. Run `/optimus:init` (or re-run it) to install a test framework and set up test infrastructure before using this skill." Do not proceed to test generation without a working framework.

**If the agent's Test Suite Execution reports failures:**
- **Fail - assertion** (tests compile and run, but some fail) — stop and report. A clean baseline is required before adding new tests. Report failing tests in the Step 5 "Bugs Discovered" section.
- **Fail - build** (build/bootstrap failures) — stop and report. Test infrastructure should have been verified by `/optimus:init`. Recommend re-running `/optimus:init` to fix build-level issues.

### Present to user

From the agent's results, present the **Discovery Summary** and **Coverage Analysis** to the user. This sets clear expectations and reinforces the conservative constraint.

### Data carried forward

- **Test runner command** and **framework identity** → Step 4 (test execution and idioms)
- **Coverage tooling** → Step 5 (final measurement)
- **Testability classification** → Step 3 (plan prioritization — testable items become candidates, untestable items are skipped)
- **Baseline coverage** → Step 5 (before/after comparison)

## Step 3: Test Generation Plan

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

### User confirmation

**Deep mode (harness or interactive)**: Skip the question — auto-select "Generate tests for all planned items" and proceed directly to Step 4.

**Normal mode**: Present the plan, then use `AskUserQuestion` — header "Plan", question "How would you like to proceed with the test generation plan?":
- **Approve all** — "Generate tests for all planned items"
- **Selective** — "Choose specific items by number"
- **Skip** — "No tests — keep the plan as reference"

If the user selects **Selective**, ask which item numbers to proceed with (e.g., "1, 3, 5").

## Step 4: Test Writing

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

## Step 5: Summary

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
- To address these, run `/optimus:refactor testability` to prioritize testability improvements.
```

For multi-repo workspaces, present results per repo (one summary block per repo) and include the repo name/path in each section header.

Recommend running `/optimus:refactor testability` to prioritize testability improvements (or `/optimus:refactor` for balanced code quality review), or `/optimus:tdd` to continue development with test-driven workflow.

Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

## Step 6: Harness Output (harness mode only)

If running under `HARNESS_MODE_ACTIVE`, output structured JSON **instead** of the Step 5 markdown summary. Output it in a `json:harness-output` fenced block and then stop — do not loop, do not present recommendations, do not use `AskUserQuestion`.

````
```json:harness-output
{
  "iteration": <cycle number from progress file>,
  "phase": "unit-test",
  "coverage": {
    "tool": "<coverage tool name or null>",
    "before": <percentage or null>,
    "after": <percentage or null>,
    "delta": <percentage or null>
  },
  "tests_written": [
    {
      "file": "<test file path>",
      "target_file": "<source file being tested>",
      "target_description": "<what it tests>",
      "test_count": <number of test cases>,
      "status": "<pass | fail-fixed | fail-abandoned>",
      "failure_reason": "<reason or null>"
    }
  ],
  "untestable_code": [
    {
      "file": "<source file path>",
      "line": <start line>,
      "end_line": <end line>,
      "function": "<function or class name>",
      "barrier": "<hardcoded-dependency | tight-coupling | global-state | ...>",
      "barrier_description": "<brief explanation>",
      "suggested_refactoring": "<what refactoring would help>"
    }
  ],
  "bugs_discovered": [
    {
      "file": "<path>",
      "line": <line>,
      "description": "<bug behavior>",
      "severity": "<High | Medium | Low>"
    }
  ],
  "no_new_tests": <true if zero new tests were written>,
  "no_untestable_code": <true if no untestable code was found>,
  "no_coverage_gained": <true if coverage delta is zero or negative>
}
```
````
