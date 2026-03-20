---
name: review-test
description: Comprehensive test suite review. Fills coverage gaps, identifies missing fuzz tests, and audits test quality — in that order.
model: opus
---

# Test Review - Comprehensive Test Suite Review

Three-phase review: fill coverage gaps, identify fuzz testing opportunities, then audit test quality. Each phase runs its own analysis → present → select → implement → verify cycle.

## Philosophy

**Tests are a system, not a checklist.** Coverage gaps, missing fuzz tests, and bad tests are different facets of the same problem: the test suite isn't doing its job. This workflow addresses all three in a deliberate order — add what's missing first, then clean up what's broken.

## Workflow Overview

```
┌──────────────────────────────────────────────────┐
│                  TEST REVIEW                      │
├──────────────────────────────────────────────────┤
│  1. Determine scope                               │
│  2. Phase 1: Coverage gaps                        │
│  3. Phase 2: Fuzz coverage                        │
│  4. Phase 3: Test quality audit                   │
│  5. Summary + optional commit                     │
└──────────────────────────────────────────────────┘
```

## Workflow Details

### 1. Determine Scope

**Ask the user:** "What should I review?"

Present these options:
- **Entire project**: Review all source and test files (default)
- **Specific directory**: A path like `src/`, `pkg/`, `lib/`
- **Specific files**: Individual source files
- **Recent changes**: Files modified on the current branch (via `git diff`)

**Default:** Entire project.

**If the project is large** (many source files), suggest narrowing scope. The user can always re-run on a different scope.

This scope applies to all three phases.

---

## Phase 1: Coverage Gaps

Fill missing test coverage, prioritized by risk.

### 1a. Detect/Obtain Coverage Data

Follow this waterfall — stop at the first step that produces a usable report.

**Step A: Check for existing coverage artifacts**

Search for coverage files in common locations:

| Format       | Files to search for                                                              |
|--------------|----------------------------------------------------------------------------------|
| Go           | `coverage.out`, `cover.out`, `c.out`                                             |
| lcov         | `lcov.info`, `coverage/lcov.info`                                                |
| Istanbul/nyc | `coverage/coverage-summary.json`, `coverage/coverage-final.json`, `.nyc_output/` |
| coverage.py  | `coverage.xml`, `coverage.json`, `htmlcov/`                                      |
| JaCoCo       | `target/site/jacoco/jacoco.xml`, `build/reports/jacoco/*/jacoco.xml`             |
| Cobertura    | `coverage.xml`, `cobertura.xml`                                                  |

If a report is found, verify it's reasonably recent (warn if older than the most recent source change). Use the report and proceed.

**Step B: Detect coverage command**

If no report exists, detect how to generate one:

1. `Makefile` with a `cover` or `coverage` target → `make cover` (or `make coverage`)
2. `package.json` with a `coverage` script → `npm run coverage`
3. `go.mod` present → `go test -coverprofile=coverage.out ./...`
4. `pyproject.toml` / `setup.cfg` / `pytest.ini` with coverage config → `pytest --cov --cov-report=json`
5. `Cargo.toml` → `cargo tarpaulin --out json` (or `cargo llvm-cov --json`)
6. `build.gradle` / `build.gradle.kts` → `gradle jacocoTestReport`

Run the command and verify it produces a report. If it fails, ask the user for the correct command.

**Step C: Ask the user**

If no coverage tooling is detected: "What command generates a coverage report for this project?"

**Step D: Manual analysis fallback**

If no coverage tooling is available, proceed with manual analysis. The agent will read source and test files to identify gaps by inspection.

**Note:** In manual analysis mode, quantitative coverage improvement is unavailable.

**Store:** the coverage command (if any) and baseline coverage percentage.

### 1b. Analyze Coverage Gaps

**Assess scope size** with Glob.

**Small scope (roughly ≤15 source files):** Spawn a single `qa-test-coverage-reviewer` agent with the full scope and coverage data.

**Large scope (roughly >15 source files):** Partition by directory or module. Spawn multiple `qa-test-coverage-reviewer` agents **in parallel**, each with a focused partition and relevant coverage data.

Merge findings into a single list ordered by priority tier (CRITICAL → HIGH → LOW). Collect REFACTOR-FOR-TESTABILITY suggestions separately — these are presented at the end of the workflow, not here.

**Prompt for each agent:**

```
Analyze test coverage gaps.
Scope: [partition or full scope]
Mode: [coverage report / coverage command / manual analysis]
Coverage data: [file path or "manual analysis — no data"]

Identify:
- Untested code paths prioritized by risk (CRITICAL / HIGH / LOW)
- Code that is structurally hard to test (REFACTOR-FOR-TESTABILITY suggestions)

Return structured findings with ADD recommendations and refactoring suggestions.
```

**If no significant gaps found:** Report "No significant coverage gaps found" and proceed to Phase 2.

### 1c. Present Findings and User Selection

Display findings as a numbered list grouped by priority tier. Hold back refactoring suggestions for the end of the workflow.

**Example:**

```
## Phase 1: Coverage Gap Analysis

Overall coverage: 68.3% lines (baseline)

### CRITICAL (2 found)
1. [ADD] auth.go:ValidateJWT (lines 45-72) — JWT validation error paths untested
   Risk: Invalid tokens could bypass authentication
2. [ADD] payment.go:ChargeCard (lines 88-120) — Retry and failure logic untested
   Risk: Silent charge failures or double charges

### HIGH (3 found)
3. [ADD] parser.go:ParseConfig (lines 30-55) — Malformed input handling untested
4. [ADD] api.go:CreateUser (lines 15-40) — Duplicate email conflict untested
5. [ADD] middleware.go:RateLimit (lines 22-45) — Limit exceeded path untested

### LOW (2 found)
6. [ADD] config.go:Defaults (lines 5-12) — Default value coverage
7. [ADD] router.go:RegisterRoutes (lines 8-25) — Route registration

Select which gaps to fill (e.g., "1-5" or "all"):
```

Use `AskUserQuestion` with multi-select. If more than ~10 findings, batch by tier.

### 1d. Implement Selected Tests

**Detect appropriate SME and spawn based on project language:**
- Go: `swe-sme-golang`
- Dockerfile: `swe-sme-docker`
- Makefile: `swe-sme-makefile`
- GraphQL: `swe-sme-graphql`
- Ansible: `swe-sme-ansible`
- Zig: `swe-sme-zig`

**For languages without a dedicated SME:** implement directly as orchestrator.

**Group findings by target test file**, then spawn one SME agent per file **in parallel**. Findings targeting the same test file go to the same agent.

**Prompt each SME agent with:**

```
Write tests to fill the following coverage gaps in [source file].
Target test file: [test file]

Gaps to cover:
1. [function_name (lines N-M)]: [what is untested]
   Should verify: [specific test description from analyst]

Guidelines:
- Write focused tests targeting the specific untested code paths.
- Follow the project's existing test conventions and framework.
- Test behavior, not implementation details.
- Cover the error/edge cases identified in the gap analysis.
- Each test should have a clear name indicating what it verifies.
- If existing test helpers or fixtures are available, use them.
```

### 1e. Verify

Run the test suite. Confirm new tests pass and existing tests still pass.

**If failures:** Report which tests failed. For new test failures, attempt one fix. For existing test failures, report to user. Let user decide how to proceed.

### 1f. Re-run Coverage

**If a coverage command was established:** Re-run it and display before/after comparison:

```
## Coverage Improvement

              Before    After     Change
Lines         68.3%     78.1%     +9.8%
```

**If manual analysis mode:** Skip with: "No coverage tooling available — cannot measure improvement quantitatively."

---

## Phase 2: Fuzz Coverage

Identify functions that should have fuzz tests.

### 2a. Analyze Fuzz Gaps

Spawn a single `qa-test-fuzz-reviewer` agent with the full scope.

```
Analyze fuzz testing coverage.
Scope: [full scope from step 1]

Identify:
- Whether fuzz testing infrastructure exists
- Functions that are good fuzz candidates but lack fuzz tests
```

### 2b. Handle Infrastructure Check

**If the agent reports no fuzz infrastructure:**

Report to the user:

```
## Phase 2: Fuzz Coverage

No fuzz testing infrastructure detected for [language].

To enable fuzz testing, consider: [tooling recommendation from agent]

Skipping fuzz analysis. Proceeding to Phase 3.
```

Proceed to Phase 3. Do not attempt to set up fuzz tooling.

**If the agent reports no candidates or all candidates are covered:**

```
## Phase 2: Fuzz Coverage

Fuzz infrastructure detected: [tooling]
No fuzz coverage gaps found. [brief explanation]

Proceeding to Phase 3.
```

Proceed to Phase 3.

### 2c. Present Findings and User Selection

Display fuzz candidates as a numbered list grouped by priority.

**Example:**

```
## Phase 2: Fuzz Coverage

Fuzz infrastructure: native testing.F (Go 1.22)
Existing fuzz tests: 2

### HIGH (2 found)
1. [ADD] parser.go:ParseConfig — Parses user-provided YAML config
   Input: arbitrary []byte
   Should verify: no panics, returns error on invalid input
2. [ADD] protocol.go:DecodeMessage — Decodes wire protocol messages
   Input: arbitrary []byte
   Should verify: no panics, bounded output size

### MEDIUM (1 found)
3. [ADD] template.go:Render — Renders user-provided templates
   Input: arbitrary string
   Should verify: no panics, no infinite loops

### Already covered
- parser.go:ParseJSON — fuzz test in parser_test.go:FuzzParseJSON
- auth.go:ParseToken — fuzz test in auth_test.go:FuzzParseToken

Select which fuzz tests to add (e.g., "1-3" or "all"):
```

Use `AskUserQuestion` with multi-select.

### 2d. Implement Selected Fuzz Tests

Same SME dispatch as Phase 1. Group by target test file, spawn in parallel.

**Prompt each SME agent with:**

```
Write fuzz tests for the following functions in [source file].
Target test file: [test file]

Fuzz targets:
1. [function_name]: [what to fuzz]
   Input type: [what to generate]
   Should verify: [properties to check]

Guidelines:
- Use the project's fuzz testing framework ([framework name]).
- Each fuzz test should target one function.
- Check the properties specified (no panics, round-trip consistency, etc.).
- Follow existing fuzz test conventions if any exist in the project.
- Keep the fuzz target function focused — minimize setup, maximize input coverage.
```

### 2e. Verify

Run the test suite (not the fuzz tests themselves — those run indefinitely). Confirm fuzz test functions compile and pass their seed corpus if any.

**If failures:** Same handling as Phase 1.

---

## Phase 3: Test Quality Audit

Identify and fix bad tests across the entire test suite, including tests written in Phases 1 and 2.

### 3a. Scan for Quality Issues

**Assess scope size** with Glob (count test files in scope).

**Small scope (roughly ≤15 test files):** Spawn a single `qa-test-reviewer` agent.

**Large scope (roughly >15 test files):** Partition by directory or module. Spawn multiple `qa-test-reviewer` agents **in parallel**, each with a focused partition.

Merge findings into a single list. Deduplicate overlaps at partition boundaries.

**Prompt for each agent:**

```
Review the test suite for quality issues.
Scope: [partition or full scope]

Look for:
- Tautological tests (can't fail)
- Brittle tests (coupled to implementation, weak assertions when stronger ones exist)
- Redundant tests (duplicate coverage — informational only, no action recommended)
- False confidence tests (don't verify what they claim)
- Missing coverage (important gaps only)
- Test smells (structural problems)
- Inconsistent assertion strategies (mixed error checking approaches, varied assertion styles)

Return structured findings with recommended actions (DELETE, REWRITE, ADD, SIMPLIFY).
Redundant tests should be reported as informational only (no action recommended).
```

**If no issues found:** Report "No test quality issues found" and proceed to summary.

### 3b. Present Findings and User Selection

Display findings as a numbered list grouped by category.

**Example:**

```
## Phase 3: Test Quality Audit

### Tautological (2 found)
1. [DELETE] model_test.go:TestUserStruct — Checks struct field existence
2. [DELETE] config_test.go:TestDefaultConfig — Asserts hardcoded values against themselves

### Brittle (2 found)
3. [REWRITE] api_test.go:TestCreateUserError — Exact error string match
4. [REWRITE] handler_test.go:TestNotFound — Asserts full JSON response body

### Redundant (1 noted — informational, no action)
- [INFO] math_test.go:TestAddVariants — 5 cases hitting same code path

### Missing Coverage (1 found)
5. [ADD] auth.go:RevokeToken — No tests for revocation path

Select which items to address (e.g., "1-5" or "all"):
```

Use `AskUserQuestion` with multi-select.

### 3c. Implement Selected Changes

Same SME dispatch as Phases 1 and 2. **Group findings by file**, spawn one SME per file **in parallel**.

**Prompt each SME agent with:**

```
The test auditor identified the following issues in [file]. Implement the recommended changes.

DELETE findings (remove these tests — but if you believe a test has value, rewrite it instead):
[List of DELETE items for this file]

REWRITE/SIMPLIFY findings (fix these tests):
[List of REWRITE/SIMPLIFY items for this file]

ADD findings (write new tests):
[List of ADD items for this file]

Guidelines:
- Focus on testing observable behavior rather than implementation details.
- Follow the project's existing test conventions.
- Keep tests simple and readable.
- For DELETE items: if the test covers real behavior that could regress, rewrite it rather than deleting it. Only delete tests that are genuinely self-fulfilling or completely orphaned.
```

### 3d. Verify

Run the test suite. Confirm all changes are clean.

**If failures:** Same handling as Phase 1.

---

## 5. Summary

Present a combined summary of all three phases, plus any refactoring suggestions collected in Phase 1.

```
## Test Review Complete

### Phase 1: Coverage Gaps
- Tests added: N
- Coverage: XX% → YY% (+Z%)

### Phase 2: Fuzz Coverage
- Fuzz tests added: N
- [or: "Skipped — no fuzz infrastructure"]

### Phase 3: Test Quality Audit
- Tests deleted: N
- Tests rewritten: N
- Tests added: N

### Net Change
- Total tests added: N
- Total tests removed: N
- Net: +/-N

### Refactoring for Testability (informational)
[Refactoring suggestions from Phase 1 coverage analyst, if any]

1. [file:function] — [problem]
   Suggestion: [what to refactor]
   Would enable testing: [what becomes testable]

These suggestions are not implemented by this workflow. Use /refactor
or address them manually.

### Files Modified
- [file]: [what changed]
```

**Ask user if they want to commit.** If yes, create a commit:

```bash
git add [specific files]
git commit -m "$(cat <<'EOF'
test: comprehensive test suite review

[Brief description: added N coverage tests, N fuzz tests,
deleted N bad tests, rewrote N brittle tests]
Coverage: XX% → YY%

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Agent Coordination

**Phase 1 analysis:** Spawn `qa-test-coverage-reviewer` agent(s). For large scopes, partition and run in parallel.
**Phase 2 analysis:** Spawn single `qa-test-fuzz-reviewer` agent.
**Phase 3 analysis:** Spawn `qa-test-reviewer` agent(s). For large scopes, partition and run in parallel.
**Implementation (all phases):** Parallel by file. Group findings by target file, spawn one SME per file.

**Fresh instances:** Every agent spawn is a fresh instance. No state carried between invocations.

**State to maintain (as orchestrator):**
- Scope (shared across all phases)
- Coverage command and baseline metrics
- User selections for each phase
- Implementation results per phase
- Refactoring suggestions (held for final summary)
- Running totals for summary

## Abort Conditions

**Abort workflow:**
- User interrupts
- No source files found in scope

**Do NOT abort for:**
- Coverage command failure (fall back to manual analysis)
- Phase 2 finding no fuzz infrastructure (skip phase, continue)
- Individual SME failures (report and continue)
- Test suite failures after changes (report and let user decide)
- Any single phase finding no issues (report and continue to next phase)
