---
name: tdd-cycle
description: Run a full RED-GREEN-REFACTOR TDD workflow for a feature. Accepts a feature description, task ID, or spec section as input. Presents a plan for confirmation then runs autonomously through all TDD phases.
argument-hint: <feature-description|task-id|spec-section>
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TaskGet, TaskList, TaskUpdate
---

# TDD Cycle Skill

Run a full RED-GREEN-REFACTOR Test-Driven Development workflow for a feature. This skill drives the entire TDD lifecycle: understand the feature, write failing tests, confirm they fail (RED), implement minimal code to make them pass (GREEN), then refactor while keeping tests green (REFACTOR).

**CRITICAL: Complete ALL 7 phases.** The workflow is not complete until Phase 7: Report is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Core Principles

1. **Tests before implementation** -- Write tests first. The tests define what the code should do. Implementation follows from tests, not the other way around.
2. **Minimal implementation** -- Write only the code needed to make failing tests pass. No extra features, no premature optimization, no speculative abstractions.
3. **Regression protection** -- Existing tests must continue passing at every phase. Zero tolerance for regressions.
4. **Phase gate enforcement** -- Each phase must complete and verify before the next begins. RED verification is mandatory. GREEN verification is mandatory.
5. **Behavior over implementation** -- Tests verify what code does (inputs, outputs, side effects), not how it does it internally.
6. **Autonomous after plan confirmation** -- The user confirms the plan once in Phase 3. After that, the entire RED-GREEN-REFACTOR cycle runs without interruption.

## AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Plan confirmation -> AskUserQuestion
- Framework selection -> AskUserQuestion
- Clarifying questions -> AskUserQuestion
- Error recovery options -> AskUserQuestion

Text output should only be used for presenting information, summaries, and progress updates.

**NEVER do this** (asking via text output):
```
Should I proceed with this plan?
1. Yes
2. No, modify it
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "TDD Plan Confirmation"
      question: "Review the TDD plan above. Ready to proceed?"
      options:
        - label: "Proceed"
          description: "Run the full RED-GREEN-REFACTOR cycle autonomously"
        - label: "Modify plan"
          description: "Adjust tests, scope, or approach before starting"
        - label: "Cancel"
          description: "Cancel the TDD workflow"
      multiSelect: false
```

---

## Phase 1: Parse Input

**Goal:** Determine the input type and resolve context.

Analyze `$ARGUMENTS` to determine the operating mode.

### Input Type Detection

**Feature Description** -- triggered when input is:
- Free-text describing a feature (e.g., "add user login with email and password")
- A file path to source code that needs TDD treatment (e.g., `src/auth/login.py`)

**Task ID** -- triggered when input is:
- A numeric ID, possibly prefixed with `#` or `task-` (e.g., `5`, `#5`, `task-5`)

**Spec Section** -- triggered when input is:
- A spec file path with optional section reference (e.g., `specs/SPEC-feature.md Section 5.1`)

### Context Resolution

**Feature Description:**
1. Record the feature description for use in Phase 3 (Plan)
2. Use Glob/Grep to find existing related code if a file path is provided
3. Determine the target module and directory

**Task ID:**
1. Use `TaskGet` to retrieve the full task details
2. Extract acceptance criteria (Functional, Edge Cases, Error Handling)
3. Check `metadata.spec_path` for the source spec
4. Record the task's description, requirements, and blocked-by/blocks relationships

**Spec Section:**
1. Read the spec file
2. Locate the referenced section
3. Extract acceptance criteria, user stories, and edge cases from the section

### Error Cases

**No input provided:**
```yaml
AskUserQuestion:
  questions:
    - header: "TDD Input"
      question: "What would you like to run TDD for?"
      options:
        - label: "Feature description"
          description: "Describe the feature to build test-first"
        - label: "Task ID"
          description: "Run TDD for a Claude Code Task"
        - label: "Spec section"
          description: "Run TDD from a spec's acceptance criteria"
        - label: "Retrofit existing code"
          description: "Add tests to existing untested code"
      multiSelect: false
```

Then prompt for the specific value based on the selection.

**Invalid task ID:**
```
ERROR: Task #{id} not found.

Available tasks:
{List first 5 pending/in-progress tasks from TaskList}

Usage: /tdd-cycle <feature-description|task-id|spec-section>
```

**Invalid spec path:**
```
ERROR: Spec file not found: {path}

Did you mean one of these?
{List matching files from Glob search for similar names}

Usage: /tdd-cycle <spec-path>
```

---

## Phase 2: Understand

**Goal:** Load project conventions, detect the test framework, and explore the relevant codebase.

### Step 1: Load Project Conventions

Read project-level conventions:
```
Read: CLAUDE.md
Read: .claude/agent-alchemy.local.md (if it exists)
```

Load cross-plugin skills for language and project awareness:
```
Read: ${CLAUDE_PLUGIN_ROOT}/../core-tools/skills/language-patterns/SKILL.md
Read: ${CLAUDE_PLUGIN_ROOT}/../core-tools/skills/project-conventions/SKILL.md
```

Apply their guidance when writing tests and implementation code.

### Step 2: Load TDD Configuration

Read TDD settings from `.claude/agent-alchemy.local.md` if it exists:

```yaml
tdd:
  framework: auto                    # auto | pytest | jest | vitest
  coverage-threshold: 80             # Minimum coverage percentage (0-100)
  strictness: normal                 # strict | normal | relaxed
  test-review-threshold: 70          # Minimum test quality score (0-100)
  test-review-on-generate: false     # Run test-reviewer after generate-tests
```

Record the TDD strictness level (default: `normal` if not configured).
Record the framework override (default: `auto` -- use detection chain).
Record the coverage threshold (default: `80` -- clamp to 0-100 if out of range).

**Error handling:**
- If the settings file does not exist, use defaults for all settings.
- If the YAML frontmatter is malformed, use defaults and log a warning.
- If `tdd.framework` is set to an unrecognized value, fall back to auto-detection.

### Step 3: Detect Test Framework

Follow the framework detection chain to identify the project's test framework.

**Priority 1 -- Config Files (High Confidence):**

*Python:*
- `pyproject.toml` with `[tool.pytest.ini_options]` or `[tool.pytest]` -> pytest
- `setup.cfg` with `[tool:pytest]` -> pytest
- `pytest.ini` exists -> pytest
- `conftest.py` at project root or in `tests/` -> pytest

*TypeScript/JavaScript:*
- `vitest.config.*` exists -> Vitest (takes priority)
- `jest.config.*` exists -> Jest
- `package.json` with `vitest` in dependencies/devDependencies -> Vitest
- `package.json` with `jest` in dependencies/devDependencies -> Jest
- `package.json` with `"jest": {}` config section -> Jest

**Priority 2 -- Existing Test Files (Medium Confidence):**
- `test_*.py` or `*_test.py` -> pytest
- `*.test.ts` / `*.spec.ts` with `vitest` imports -> Vitest
- `*.test.ts` / `*.spec.ts` with `jest` imports or no explicit imports -> Jest

**Priority 3 -- Settings Fallback (Low Confidence):**
- Check `.claude/agent-alchemy.local.md` for `tdd.framework`

**Priority 4 -- User Prompt Fallback:**

If all detection methods fail:
```yaml
AskUserQuestion:
  questions:
    - header: "Test Framework"
      question: "No test framework was detected in this project. Which framework should be used?"
      options:
        - label: "pytest"
          description: "Python testing framework (recommended for Python projects)"
        - label: "Jest"
          description: "JavaScript/TypeScript testing framework"
        - label: "Vitest"
          description: "Vite-native testing framework (modern alternative to Jest)"
        - label: "Other"
          description: "A different framework (tests may need manual adjustment)"
      multiSelect: false
```

### Step 4: Load Test Pattern References

Read framework-specific patterns and templates:
```
Read: ${CLAUDE_PLUGIN_ROOT}/skills/generate-tests/references/test-patterns.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/generate-tests/references/framework-templates.md
```

### Step 5: Explore Codebase

1. Use `Glob` to find files related to the feature scope
2. Use `Grep` to locate relevant symbols, functions, and patterns
3. Read existing test files to understand test conventions (naming, structure, fixtures, assertion style)
4. Identify where new test files and implementation files should be placed
5. Read 2-3 representative existing test files if available to match project test style

### Step 6: Snapshot Existing Test State

Run the existing test suite and record the baseline:
- Total tests, pass count, fail count
- List any pre-existing failures (these are not your responsibility to fix)
- This baseline is used in Phases 4 (RED) and 5 (GREEN) to separate new results from existing state

**Python (pytest):**
```bash
pytest --tb=short -q 2>&1 || true
```

**TypeScript (Jest/Vitest):**
```bash
npx jest --no-coverage 2>&1 || true
npx vitest run --reporter=verbose 2>&1 || true
```

Record the baseline: `{total} tests, {passed} passed, {failed} failed`

---

## Phase 3: Plan

**Goal:** Present the TDD plan to the user and get a single confirmation before running autonomously.

### Build the TDD Plan

Based on the parsed input and codebase exploration, construct a plan covering:

1. **Feature scope**: What behavior will be implemented
2. **Tests to write**: List of test cases with descriptive names, organized by category:
   - Functional tests (core behavior)
   - Edge case tests (boundary conditions)
   - Error handling tests (failure scenarios)
3. **Test file location**: Where test files will be created
4. **Implementation approach**: What source files will be created or modified
5. **Coverage target**: Expected coverage percentage
6. **Strictness level**: RED phase enforcement level (from settings)

### Present Plan

Present the plan as a formatted summary:

```
## TDD Plan: {feature name}

**Framework**: {pytest | Jest | Vitest}
**Strictness**: {strict | normal | relaxed}
**Coverage Target**: {percentage}%

### Tests to Write

**Functional:**
- test_{behavior_1}: {description}
- test_{behavior_2}: {description}

**Edge Cases:**
- test_{edge_case_1}: {description}

**Error Handling:**
- test_{error_1}: {description}

### Test Files
- {test_file_path_1}

### Implementation Files
- {source_file_path_1} (create / modify)

### Approach
{Brief description of the implementation strategy}
```

### Confirm Plan

Use `AskUserQuestion` to get confirmation:

```yaml
AskUserQuestion:
  questions:
    - header: "TDD Plan Confirmation"
      question: "Review the TDD plan above. Ready to proceed with the RED-GREEN-REFACTOR cycle?"
      options:
        - label: "Proceed"
          description: "Run the full TDD cycle autonomously — no further interruptions"
        - label: "Modify plan"
          description: "Adjust the test plan before starting"
        - label: "Cancel"
          description: "Cancel this TDD workflow"
      multiSelect: false
```

**If "Modify plan"**: Ask what changes are needed via `AskUserQuestion`, update the plan, and present again for confirmation.

**If "Cancel"**: Stop the workflow and inform the user.

**If "Proceed"**: Continue to Phase 4. From this point forward, the workflow runs autonomously without user interaction.

---

## Phase 4: RED Phase

**Goal:** Write failing tests from requirements, then run the test suite to confirm all new tests fail.

**CRITICAL: After plan confirmation, this phase and all subsequent phases run autonomously. Do NOT prompt the user for input.**

### Load TDD Workflow Reference

Read the TDD workflow reference for phase definitions and verification rules:
```
Read: ${CLAUDE_PLUGIN_ROOT}/skills/tdd-cycle/references/tdd-workflow.md
```

### Step 1: Write Failing Tests

Write the test files planned in Phase 3:

1. **Convert requirements to test cases**: Each acceptance criterion becomes one or more test assertions
2. **Follow project test conventions**: Match existing test file naming, directory structure, assertion style, and fixture patterns
3. **Write behavior-driven tests**: Test what the code should do, not how it does it. Focus on inputs, outputs, and observable side effects
4. **Use the AAA pattern**: Arrange (setup), Act (execute), Assert (verify)
5. **Include edge case tests**: Boundary conditions, null/empty inputs, error scenarios
6. **Use descriptive test names**:
   - pytest: `test_<function>_<scenario>_<expected_result>`
   - Jest/Vitest: `describe("<unit>", () => { it("should <behavior> when <condition>", ...) })`

**IMPORTANT**: Do NOT write any implementation code during this step. Only write test files.

### Step 2: Run Tests -- Confirm RED

Run the full test suite:

**Python:**
```bash
pytest --tb=short -q 2>&1
```

**TypeScript:**
```bash
npx jest --no-coverage 2>&1
npx vitest run --reporter=verbose 2>&1
```

### Step 3: Verify RED State

Compare results against the Phase 2 baseline to isolate new test results.

**Expected outcome**: ALL new tests fail with appropriate errors (ImportError, ModuleNotFoundError, AttributeError, AssertionError, etc.)

**Apply strictness level:**

| Strictness | If new tests pass | Action |
|------------|-------------------|--------|
| **strict** | ANY new test passes | Abort workflow. Report which tests passed and likely cause |
| **normal** | Some new tests pass | Log warning. Investigate: is implementation already present? Are tests too weak? Continue after investigation |
| **relaxed** | Any outcome | Log results and continue regardless |

### Edge Case: Tests Pass Immediately

If some or all new tests pass before implementation:

1. **Check if implementation already exists**: Search for existing code that satisfies the tests
2. **If implementation exists**: Log a warning to the user. If ALL tests pass, skip to Phase 6 (REFACTOR). If partial, proceed to Phase 5 (GREEN) for remaining tests
3. **If tests are too weak**: Strengthen the tests to properly verify new behavior, then re-run RED
4. **Log the finding** for the Phase 7 report

---

## Phase 5: GREEN Phase

**Goal:** Implement the minimal code necessary to make all failing tests pass.

### Step 1: Implement Minimally

Write only the code needed to make the current failing tests pass:

1. **Follow existing patterns**: Match the codebase's coding style, error handling approach, and module organization
2. **Work incrementally**: Address one test (or small group of related tests) at a time when possible
3. **No test modifications**: Do NOT change the tests written in Phase 4. If a test is genuinely wrong, document the issue explicitly
4. **Handle errors at boundaries**: Add error handling that the tests verify, but do not add speculative error handling
5. **Follow project conventions**: Read `CLAUDE.md` rules, match naming, match file organization

### Implementation Order

Follow dependency-aware order:
1. Data layer (models, schemas, types)
2. Service layer (business logic, utilities)
3. API/Interface layer (endpoints, handlers, UI components)
4. Configuration (env vars, config files)

### Step 2: Run Tests -- Confirm GREEN

Run the full test suite:

```bash
pytest --tb=short -q 2>&1          # Python
npx jest --no-coverage 2>&1        # Jest
npx vitest run --reporter=verbose 2>&1  # Vitest
```

### Step 3: Verify GREEN State

**Expected outcome**: ALL tests pass (new tests + existing baseline tests).

- **ALL new tests MUST pass**: Every test from Phase 4 should now pass
- **NO regressions**: Compare against the Phase 2 baseline. No previously-passing test should now fail

### If Tests Fail

1. Identify the failing test and the root cause
2. Fix the IMPLEMENTATION (not the tests) to make it pass
3. Re-run the full suite
4. Repeat until all tests pass (up to 5 iterations)
5. If after 5 iterations tests still fail, report FAIL with specific details

### Edge Case: Regression Detected

If a previously-passing test now fails:
- This is a regression introduced by the implementation
- Fix the implementation to resolve the regression WITHOUT breaking new tests
- This takes priority over making new tests pass

### Edge Case: Implementation Cannot Make Tests Pass

If reasonable iteration cannot satisfy all tests:
1. Check for contradictory requirements
2. Check for missing dependencies or infrastructure
3. Report **FAIL** with:
   - Which tests fail and their error messages
   - What was attempted
   - Recommendations for resolution

---

## Phase 6: REFACTOR Phase

**Goal:** Clean up the implementation while keeping all tests green.

### Step 1: Identify Refactoring Opportunities

Look for:
- Code duplication
- Unclear naming
- Overly complex logic
- Missing abstractions (only when justified)
- Missing type annotations (if the project uses them)
- Dead code or unused imports

### Step 2: Refactor Incrementally

For each refactoring change:

1. Make one small, focused change
2. Run the full test suite immediately after the change
3. **If tests break: REVERT the change immediately.** Do not try to fix both the refactor and the test simultaneously
4. Continue with the next refactoring opportunity

### Step 3: Verify Tests Remain GREEN

After all refactoring is complete, run the full test suite one final time to confirm:
- Same pass count as Phase 5
- No regressions
- No behavior changes -- only structural improvements

### Edge Case: Refactor Breaks Tests

If a refactoring change causes test failures:
1. **Revert** the specific change immediately
2. Run tests to confirm they pass after reverting
3. Try a different refactoring approach if the improvement is important
4. If no safe refactoring is possible, stop refactoring and proceed to Phase 7
5. Report as **PARTIAL** -- code works (GREEN verified) but was not fully refactored

---

## Phase 7: Report

**Goal:** Present final TDD results to the user.

### Collect Results

Gather results from all phases:
- Phase 2 baseline: existing test state
- Phase 4 RED: which tests failed, any unexpected passes
- Phase 5 GREEN: all tests passing, iteration count
- Phase 6 REFACTOR: changes made, any reverted refactoring

### Run Coverage (If Available)

Attempt to run coverage tools:

**Python:**
```bash
pytest --cov --cov-report=term-missing -q 2>&1
```

**TypeScript:**
```bash
npx jest --coverage 2>&1
npx vitest run --coverage 2>&1
```

If coverage tools are available, include the coverage percentage in the report. If not, skip coverage reporting.

### Report Format

Present the final report:

```
## TDD Cycle Complete: {feature name}

**Status**: {PASS | PARTIAL | FAIL}
**Strictness**: {strict | normal | relaxed}

### Phase Results

| Phase | Status | Details |
|-------|--------|---------|
| Understand | Complete | Framework: {name}, Baseline: {n} tests |
| RED | {Verified/Warning} | {n}/{total} new tests failed as expected |
| GREEN | {Verified/Failed} | {pass}/{total} tests pass, {regressions} regressions |
| REFACTOR | {Complete/Partial/Skipped} | {changes made or reason skipped} |

### Test Results

**New tests written**: {count}
**All tests passing**: {total pass}/{total run}
**Pre-existing failures**: {count} (not addressed)
**Regressions**: {count}
**Coverage**: {percentage}% (or N/A if coverage tools unavailable)

### Files Created/Modified

| File | Action | Description |
|------|--------|-------------|
| {test_file} | Created | {n} tests for {feature} |
| {source_file} | Created/Modified | {brief description} |

### TDD Compliance

- RED verified: {Yes/No/Warning}
- GREEN verified: {Yes/No}
- Refactored: {Yes/No/Partial}

{If PARTIAL or FAIL:}
### Issues

- {description of what went wrong}

### Recommendations

- {suggestion for resolution}
```

### Status Determination

| Condition | Status |
|-----------|--------|
| All phases complete, all tests pass | **PASS** |
| GREEN verified, REFACTOR failed (reverted) | **PARTIAL** |
| GREEN verified, some edge/error criteria issues | **PARTIAL** |
| Some new tests fail after implementation | **FAIL** |
| RED phase abort (strict mode) | **FAIL** |
| Implementation cannot make tests pass | **FAIL** |

### SDD Pipeline Integration

If this TDD cycle was invoked with a task ID:
- **PASS**: Update the task status to `completed` via `TaskUpdate`
- **PARTIAL or FAIL**: Leave the task as `in_progress` for the orchestrator to decide on retry

---

## Integration Modes

### Standalone Mode

The user provides a feature description or file path directly:

```
/tdd-cycle add user login with email and password validation
/tdd-cycle src/auth/login.py
```

The skill runs the full workflow: Parse Input -> Understand -> Plan -> RED -> GREEN -> REFACTOR -> Report.

### SDD Pipeline Mode

The skill receives a task ID from `execute-tdd-tasks` or is invoked by the user with a task ID:

```
/tdd-cycle #5
/tdd-cycle task-12
```

The skill:
1. Loads task details via `TaskGet`
2. Extracts acceptance criteria for test generation
3. Runs the full TDD workflow
4. Updates task status via `TaskUpdate` on completion

### Retrofit Mode

The user provides an existing source file to add tests to:

```
/tdd-cycle --retrofit src/utils/helpers.py
```

Retrofit mode differs from standard TDD:
1. **Skip RED**: Implementation already exists, so tests may pass immediately
2. **Generate characterization tests**: Analyze existing code to document current behavior
3. **Use relaxed strictness**: Override strictness to `relaxed` since tests passing during RED is expected
4. **Run tests**: Verify characterization tests pass against existing code
5. **Report coverage**: Show what percentage of the existing code is now covered

Detection: If the input references an existing source file AND the file already contains implementation code (not just stubs), default to retrofit mode. Alternatively, the `--retrofit` flag explicitly enables this mode.

---

## Error Handling

### No Test Framework Detected

If framework detection reaches the user prompt fallback and the user selects "Other":

```
WARNING: Unsupported framework selected. Generating tests using the closest
supported framework ({inferred}). Generated tests may need manual adjustment
for your specific framework.
```

### Invalid Input

If the input cannot be parsed as any supported type:

```
ERROR: Could not understand the input: {input}

Usage: /tdd-cycle <feature-description|task-id|spec-section>

Examples:
  /tdd-cycle add user authentication with OAuth2
  /tdd-cycle #5
  /tdd-cycle specs/SPEC-auth.md Section 5.1
  /tdd-cycle --retrofit src/auth/login.py
```

### Test Suite Errors

If the test runner itself fails (not test failures, but runner crashes):
1. Check for missing dependencies
2. Check for configuration errors
3. Report the error with the full output
4. Suggest resolution steps

---

## Settings

The following settings in `.claude/agent-alchemy.local.md` affect the TDD cycle:

```yaml
tdd:
  framework: auto                    # auto | pytest | jest | vitest
  coverage-threshold: 80             # Minimum coverage percentage (0-100)
  strictness: normal                 # strict | normal | relaxed
```

| Setting | Default | Used In |
|---------|---------|---------|
| `tdd.framework` | `auto` | Phase 2 (framework detection fallback) |
| `tdd.coverage-threshold` | `80` | Phase 7 (coverage reporting target) |
| `tdd.strictness` | `normal` | Phase 4 (RED phase enforcement) |

See `tdd-tools/README.md` for the full settings reference.

---

## Reference Files

- `references/tdd-workflow.md` -- TDD phase definitions (RED-GREEN-REFACTOR), verification rules, strictness levels, edge case handling
