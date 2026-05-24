---
description: Improves unit test coverage on demand — discovers testing gaps and generates tests that follow project conventions. Requires /optimus:init to have set up test infrastructure first. Conservative — only adds new test files, never refactors existing source code. Supports `deep` mode for iterative in-conversation test generation and `deep harness` mode for an automated multi-cycle unit-test + testability-refactor loop with fresh context per phase. Use when test coverage is low, after adding new code that lacks tests, or when you want an automated coverage-improvement harness.
disable-model-invocation: true
---

# Unit Test Coverage Improvement

Improve unit test coverage for existing code. Requires `/optimus:init` to have set up test infrastructure (framework, coverage tooling, testing docs) first. Conservative by design — only adds new test files, never refactors or restructures existing source code. If code is untestable as-is, it flags it rather than changing it. Refactoring is the domain of `/optimus:refactor`.

## Step 1: Pre-flight

### Parse invocation arguments

Extract from the user's arguments:
1. `deep` flag (present/absent)
2. `harness` keyword after `deep` (present/absent)
3. A number immediately after `deep` or `deep harness` → iteration cap (optional, default 5, hard cap 10)
4. Everything else → scope instructions (optional path)

Examples:
- `/optimus:unit-test` → normal mode, full project
- `/optimus:unit-test src/api` → normal mode, scoped
- `/optimus:unit-test deep` → deep mode (5 iterations)
- `/optimus:unit-test deep 3` → deep mode (3 iterations)
- `/optimus:unit-test deep src/api` → deep mode, scoped
- `/optimus:unit-test deep harness` → harness mode, 5 iterations
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

### Interactive deep mode activation

<!-- Deep-mode activation; keep behavior in sync with Step 2 of code-review/SKILL.md and refactor/SKILL.md. Unit-test places activation under Step 1 pre-flight, but the warning, confirmation, and state-init logic mirror those skills. -->

If the `deep` flag was detected in argument parsing (and `harness` keyword was NOT), activate deep mode. Deep mode loops discovery-and-write cycles (Steps 2–4) until tests converge or the iteration cap is reached.

Clamp the parsed iteration cap: if it exceeds 10, clamp to 10 and warn: "Iteration cap clamped to 10 (maximum)." If it is less than 1, clamp to 1 and warn: "Iteration cap clamped to 1 (minimum)." Default is 5 when no number is given.

Before proceeding, check whether a test command is available (from `.claude/CLAUDE.md`). If no test command exists, deep mode's auto-approve loop has no safety net — fall back to normal mode and warn: "Deep mode requires a test command for safe auto-approve. Falling back to normal mode — re-run `/optimus:init` to set up test infrastructure first." Set `deep-mode` to false. Then continue with the standard single-pass flow.

If a test command is available, warn the user:

> **Deep mode** runs up to [cap] iterative test-generation passes. Each iteration is a full discovery-and-write cycle — credit and time consumption multiplies with iteration count. Tests are generated automatically at each iteration without per-item approval. Untestable code that requires refactoring is flagged but not addressed; consider running `/optimus:refactor testability` first or `/optimus:unit-test deep harness` for an automated unit-test + refactor-testability loop. Each iteration also accumulates context — on large codebases, output quality may degrade in later iterations.
>
> Test command: `[test command from CLAUDE.md]`

Then use `AskUserQuestion` — header "Deep mode", question "Proceed with deep mode?":
- **Start deep mode** — "Run iterative test-generation until converged (max [cap] iterations)"
- **Normal mode** — "Single pass with manual plan approval instead"

Tell the user: *Tip: For large codebases or extended sessions, re-run with `/optimus:unit-test deep harness` to launch the external harness with fresh context per phase.*

If the user did not invoke with `deep`, skip this step.

If the user selects **Normal mode**, set `deep-mode` to false and continue with the standard single-pass flow.

If deep mode is confirmed, set `deep-mode` to true and initialize:

- Counters: `iteration-count` = 1, `total-added` = 0, `total-reverted` = 0, `accumulated-coverage-delta` = 0
- `accumulated-items` = empty list — each entry records **file** (test file path), **target** (the `file:function/class` being tested — one entry per covered symbol, so convergence matching is exact-match on this string), **iteration** (which iteration added it), and **status** (`pass` | `reverted — test failure` | `bug-found` | `abandoned`)
- `accumulated-untestable` = empty list — items the analyzer classifies as not-testable-without-refactoring across iterations
- `accumulated-bugs` = empty list — bugs discovered by test failures across iterations

Define the `[coverage-summary]` placeholder once: when the coverage tool is available, render as `<sign><abs(accumulated-coverage-delta)>pp` where `<sign>` is `+` for values ≥ 0 and `-` for negative (e.g. `+2.5pp`, `-1.0pp`). When the coverage tool is unavailable, render as `not measured`. Every downstream use (iteration-context block, iteration report, progress summary, cumulative report) applies this same rendering.

## Step 2: Discovery & Coverage Analysis (agent-assisted)

Delegate test infrastructure scanning, test execution, and coverage analysis to a reconnaissance agent to keep the main context clean for test writing.

For each subproject (or the single project):

Read `$CLAUDE_PLUGIN_ROOT/skills/unit-test/agents/shared-constraints.md` for agent constraints.
Read `$CLAUDE_PLUGIN_ROOT/skills/unit-test/agents/test-infrastructure-analyzer.md` for the full prompt template, scanning patterns, execution rules, and return format for the Test Infrastructure Analyzer Agent.

### Iteration context injection (interactive deep mode, iterations 2+)

If interactive deep mode is active and `iteration-count` > 1, prepend a concise context block to the agent prompt before the main instructions. Include:

- **Tests already added** — bullet list of `file → target` entries from `accumulated-items` with status `pass`, so the agent skips re-discovering the same targets.
- **Items previously reverted, abandoned, or bug-found** — bullet list from `accumulated-items` with status `reverted — test failure`, `abandoned`, or `bug-found`, so the agent does not re-propose them.
- **Untestable code already flagged** — bullet list from `accumulated-untestable`, so the agent does not re-flag them; focus new discovery on genuinely new items.
- **Cumulative coverage delta** — `[coverage-summary] so far`, so the agent has a sense of progress.

The goal is convergence: each iteration should propose **new** testable items, not duplicates. Keep the block under ~30 lines to limit context drift.

### Launch

Launch 1 `general-purpose` Agent tool call using the prompt from test-infrastructure-analyzer.md, prepended with the shared constraints (and the iteration context block, if applicable).

| Agent | Role | Runs when |
|-------|------|-----------|
| 1 — Test Infrastructure Analysis | Scan test files/frameworks/runners, run existing tests, measure coverage, classify code testability | Always |

Wait for the agent to complete.

**In interactive deep mode:** after the agent returns, append its newly-classified not-testable-without-refactoring entries (from the Testability Classification → Untestable section) to `accumulated-untestable`, skipping any already present from prior iterations.

### Stop gates (evaluated from agent results)

**If no test framework is detected** in the agent's Discovery Results, stop and report: "No test framework found. Run `/optimus:init` (or re-run it) to install a test framework and set up test infrastructure before using this skill." Do not proceed to test generation without a working framework.

**If the agent's Test Suite Execution reports failures**, stop. This skill does not fix failing tests or build-level issues by design. Print the matching message below (Conversation / Mode / Next skill per `$CLAUDE_PLUGIN_ROOT/references/skill-handoff.md`).

- **Fail - assertion** (tests compile and run, but some fail): print the quote below, then append a `### Bugs Discovered` section listing each failing test as `[test file] — [test name] — [one-line failure excerpt]` (prefix entries with repo name/path in multi-repo workspaces; omit the excerpt if the test runner output did not expose it).

  > Pre-existing tests are failing. A green baseline is required before adding new tests, and this skill does not modify existing tests or source code.
  >
  > **Next:** stay in this conversation (normal mode) and ask Claude to triage the failing tests listed in Bugs Discovered. Once the baseline is green, start a fresh conversation and re-run `/optimus:unit-test`.
  >
  > **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

- **Fail - build** (build/bootstrap failures): print the quote below and stop — no Bugs Discovered section (there are no per-test failures to list, only build errors the analyzer has already summarized).

  > The test runner cannot start or test files fail to compile. These are build-level issues, not test logic, and `/optimus:init` owns that repair path.
  >
  > **Next:** start a fresh conversation in normal mode and run `/optimus:init` — its health check will propose minimal fixes and re-run the suite. Once the build is healthy, start another fresh conversation and re-run `/optimus:unit-test`.
  >
  > **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

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

**Deep mode (harness or interactive)**: Skip the question — auto-select "Generate tests for all planned items" and proceed directly to Step 4. In interactive deep mode, the deep-mode loop sub-section at the end of Step 4 decides whether to iterate or finalize; in harness mode, Step 6 emits structured JSON and the external harness drives any further cycles.

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

**In deep mode**, track each item's outcome so the deep-mode loop below and its cumulative report have data to aggregate. Assign one of the following statuses per item: `pass` (passed in isolation — full-suite verification may still revert it), `abandoned` (3 fix attempts exhausted), or `bug-found` (failure revealed a pre-existing bug in source code). Append any bugs found to `accumulated-bugs`. The per-item appends into `accumulated-items` happen in the Deep mode loop subsection below, after Final verification has settled the `pass` vs `reverted — test failure` status for each entry.

### Final verification

After all tests are written, run the **full test suite** to ensure no regressions. Follow the verification protocol from `$CLAUDE_PLUGIN_ROOT/skills/init/references/verification-protocol.md` — run tests fresh, read complete output, and report actual results with evidence before claiming success.

**In deep mode:** if the full-suite run reveals that a newly-added test file causes regressions (either the new test itself failing under the full suite, or causing other tests to fail), revert that test file and promote its status from `pass` to `reverted — test failure` (to be appended by the Deep mode loop below). `abandoned` and `bug-found` statuses are not affected — only a `pass` is eligible for this promotion.

### Deep mode loop

<!-- Deep-mode iteration loop; keep structure in sync with code-review/SKILL.md Step 9 and refactor/SKILL.md Step 8 -->

**Normal mode and harness mode:** Skip this subsection — normal mode proceeds to Step 5; harness mode proceeds to Step 6.

**Interactive deep mode:** After Final verification above completes for this iteration:

1. Append this iteration's results to `accumulated-items` — **one entry per covered symbol** (a test file exercising 3 functions yields 3 entries). Each entry uses the schema defined in Step 1 state init (file, target, iteration, status), with status settled during Per-test workflow and Final verification.
2. Update `total-added` by the count of entries with status `pass`.
3. Update `total-reverted` by the count of entries with status `reverted — test failure`.
4. Compute `iteration-coverage-delta` as the difference between current coverage and coverage at the start of this iteration (use `0` if the coverage tool is unavailable), then add it to `accumulated-coverage-delta`.

Then check termination conditions in order; the first matching condition stops the loop:

1. **No new testable items discovered this iteration** (convergence) → stop. Filter the discovery agent's Testability Classification Testable section against `accumulated-items` using exact-match on the `file:function/class` portion (format set in Step 1 state init). If every Testable entry is already a `target` in `accumulated-items`, convergence is reached. Report: "Deep mode complete — converged on iteration [N] with no remaining testable items."
2. **No newly-written test passed verification** — at least one test was written this iteration AND `total-added` for this iteration is 0 (every attempt ended in `reverted — test failure`, `abandoned`, or `bug-found`) → stop. Report: "Deep mode stopped — all tests added in iteration [N] caused failures."
3. **Coverage plateau** — coverage tool is available AND `|iteration-coverage-delta| ≤ 0.5pp` → stop. Report: "Deep mode stopped — coverage plateau on iteration [N]."
4. **`iteration-count` >= the cap** → cap reached. Report: "Deep mode reached the iteration cap ([cap]). Remaining testable items may exist — continue in a fresh conversation: re-run `/optimus:unit-test deep`, increase the cap with `/optimus:unit-test deep [higher-cap]`, or narrow scope with `/optimus:unit-test deep <scope>`."
5. **Otherwise** → continue to the next pass.

**In every outcome (stop or continue)**, present the iteration report immediately after the termination/continuation message. Informational and non-blocking — no user prompt follows:

```
#### Iteration [N] — Report

Cumulative coverage: [coverage-summary]

| # | File | Target | Status |
|---|------|--------|--------|
[one row per accumulated-items entry where iteration == current — one entry per covered symbol, per Step 1 state init]
```

Column definitions:
- **#** — Sequential number within this iteration
- **File** — Test file path (or `—` for reverted/abandoned)
- **Target** — the `file:function/class` being tested (format set in Step 1 state init)
- **Status** — the entry's state-enum value: `pass`, `reverted — test failure`, `bug-found`, or `abandoned` (as defined in Step 1 state init)

If the loop will continue (condition 5), after the iteration report also show the progress summary: "Iteration [N] of up to [cap] — [total-added] tests added so far, [total-reverted] reverted, cumulative coverage [coverage-summary]. Starting next pass..." If the **next** iteration will be 3 or higher, append: "Note: context is accumulating — if output quality degrades, consider finishing in a fresh conversation." Then increment `iteration-count` and **return to Step 2** for the next discovery-and-write pass. Keep the same scope from Step 1.

After the loop ends (conditions 1–4 triggered), present a cumulative report in place of the Step 5 single-pass summary:

```
## Unit Test — Deep Mode Cumulative Report

**Summary:**
- Total iterations: [iteration-count]
- Total tests added: [total-added]
- Total tests reverted (failures): [total-reverted]
- Cumulative coverage delta: [coverage-summary]
- Final test status: pass / fail / not available

**All Tests Added:**

| # | Iter | File | Target | Status |
|---|------|------|--------|--------|
[one row per item from accumulated-items, across all iterations, ordered by iteration then sequence]

### Bugs Discovered
- [one bullet per entry in `accumulated-bugs`; omit this section if empty]

### Not Testable Without Refactoring
- [one bullet per entry in `accumulated-untestable`; omit this section if empty]
- To address these, run `/optimus:refactor testability` to prioritize testability improvements.
```

Then skip Step 5. Recommend running `/optimus:refactor testability` to prioritize testability improvements (or `/optimus:refactor` for balanced code quality review), or `/optimus:tdd` to continue development with test-driven workflow. Tell the user: **Tip:** for best results, start a fresh conversation for the next skill — each skill gathers its own context from scratch.

## Step 5: Summary

**Interactive deep mode:** Skip this step — the cumulative report rendered by the deep mode loop at the end of Step 4 replaces the single-pass summary below.

**Harness mode:** Skip this step — Step 6 emits the structured JSON output instead.

**Normal mode:** Report to the user:

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
