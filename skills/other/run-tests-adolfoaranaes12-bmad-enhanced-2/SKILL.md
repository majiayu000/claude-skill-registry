---
name: run-tests
description: Execute tests with coverage analysis using bmad-commands, identify coverage gaps, and suggest missing tests. This skill should be used for test execution and quality validation.
acceptance:
  - tests_executed: "All matching tests successfully executed"
  - coverage_generated: "Coverage report generated successfully"
  - gaps_identified: "Coverage gaps analyzed and categorized"
  - suggestions_provided: "Missing test suggestions provided (if gaps exist)"
inputs:
  scope:
    type: string
    required: true
    description: "Test scope: task_id, file_path, or '--all'"
    validation: "Must be valid task ID, file path, or '--all'"
  coverage:
    type: boolean
    required: false
    description: "Generate coverage report"
    default: true
  framework:
    type: string
    required: false
    description: "Test framework (auto-detect or explicit: jest, pytest, junit, gtest, cargo, go)"
    default: "auto"
outputs:
  tests_passed:
    type: boolean
    description: "Whether all tests passed"
  total_tests:
    type: number
    description: "Total number of tests executed"
  passed_tests:
    type: number
    description: "Number of tests that passed"
  failed_tests:
    type: number
    description: "Number of tests that failed"
  coverage_percent:
    type: number
    description: "Overall test coverage percentage"
  coverage_gaps:
    type: array
    description: "List of identified coverage gaps with criticality"
telemetry:
  emit: "skill.run-tests.completed"
  track:
    - scope
    - framework
    - total_tests
    - passed_tests
    - failed_tests
    - coverage_percent
    - duration_ms
    - gaps_count
---

# Run Tests Skill

## Purpose

Execute tests, generate coverage reports, analyze coverage gaps, and suggest missing tests to improve code quality and test completeness.

**Core Capabilities:**
- Test execution via bmad-commands
- Coverage report generation and analysis
- Gap identification with criticality assessment
- Missing test suggestions with concrete examples

## Prerequisites

- Test framework configured (Jest, Pytest, JUnit, Google Test, Cargo, Go Test, or any custom framework)
- Tests written for the code being tested
- bmad-commands skill available at `.claude/skills/bmad-commands/`
- Project dependencies installed

**Framework Support:**
- **Auto-detection:** Automatically detects Jest, Pytest, JUnit, GTest, Cargo, Go Test
- **Explicit:** Specify framework with `--framework <name>`
- **Custom:** Add custom frameworks via `.claude/config.yaml` (see bmad-commands/FRAMEWORK-EXTENSION-GUIDE.md)

---

## Workflow

### Step 0: Determine Test Scope

**Action:** Parse input and identify which tests to run.

**Scope Types:** Task-based (extract keywords → pattern → find tests), File-based (find corresponding test file), All tests (run all **/*.test.*)

**See:** `references/templates.md#step-0-scope-determination-templates` for complete examples

---

### Step 1: Execute Tests

**Action:** Use bmad-commands to run tests.

**Execute:** `python .claude/skills/bmad-commands/scripts/run_tests.py --path . --framework auto --output json`

**Parse Response:** Extract success, outputs (passed, total_tests, coverage_percent, failures), telemetry, errors

**If tests fail:** Report failed tests with details, suggest fixes, do not proceed with coverage analysis

**See:** `references/templates.md#step-1-test-execution-templates` for complete response formats and error handling

---

### Step 2: Generate Coverage Report

**Action:** Parse coverage data and generate reports.

**Coverage Metrics:** Statements, Branches, Functions, Lines (each with covered/total/percent)

**Generate Report:** Parse coverage JSON, create text table, check thresholds (≥80% for each metric)

**See:** `references/templates.md#step-2-coverage-report-templates` for complete formats and threshold checking

---

### Step 3: Analyze Coverage Gaps

**Action:** Identify uncovered code and categorize by criticality.

**Gap Categories:** Error Handling (High), Edge Cases (Medium), Rare Branches (Low)

**Criticality Levels:**
- **Critical:** Security, payments, data deletion, auth (Must Test)
- **High:** Error handling, business logic, state transitions (Should Test)
- **Medium:** Logging, non-critical errors, minor edge cases (Nice to Test)
- **Low:** Debug code, dev-only code, trivial getters (Optional)

**See:** `references/templates.md#step-3-gap-analysis-templates` for complete examples and assessment criteria

---

### Step 4: Suggest Missing Tests

**Action:** Generate concrete test suggestions for coverage gaps.

**For each gap:** File/line, criticality, reason, concrete test example

**Prioritization:** Focus on HIGH (3-5 suggestions), then MEDIUM (2-3), LOW optional

**See:** `references/templates.md#step-4-test-suggestion-templates` for complete suggestion formats with test code

---

### Step 5: Present Summary

**Action:** Provide comprehensive test execution summary.

**Summary Includes:**
- Scope, framework, duration, test results (passed/failed/total)
- Coverage report with thresholds (statements, branches, functions, lines)
- Coverage gaps categorized by priority (CRITICAL/HIGH/MEDIUM/LOW)
- Test suggestions with estimated time and coverage gain
- Next steps and recommendations

**See:** `references/templates.md#step-5-complete-summary-templates` for formatted output examples

---

## Output

Return structured JSON with test results, coverage data, gaps array (file, lines, criticality, category), test suggestions, and telemetry

**See:** `references/templates.md#complete-json-output-format` for full structure

---

## Error Handling

**No tests found:** Verify test files exist, check scope pattern | **Tests failing:** Report failures with details, suggest fixes | **Coverage below threshold:** Identify gaps, suggest missing tests | **Framework not configured:** Verify installation and configuration

**See:** `references/templates.md#error-templates` for complete error messages and solutions

---

## Common Scenarios

**Tests passing + good coverage (≥80%):** Report success, highlight optional improvements | **Tests passing + low coverage (<80%):** Identify critical gaps, suggest HIGH priority tests | **Tests failing:** Report failures, suggest fixes, do not proceed with coverage analysis

---

## Best Practices

Run tests frequently | Prioritize quality over coverage % | Test what matters (business logic, errors, edge cases) | Keep tests fast (mock dependencies) | Use meaningful test names

**See:** `references/best-practices.md` for detailed testing best practices

---

## Routing Guidance

**Use this skill when:**
- Need to execute tests for implemented code
- Need coverage analysis
- Want to identify test gaps
- Need to validate implementation quality

**Always use after:**
- Feature implementation (`implement-feature`)
- Bug fixes (`fix-bug`)
- Code refactoring (`refactor-code`)

**Before:**
- Creating pull requests
- Deploying to production
- Code reviews

---

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats, complete examples, JSON structures, CI/CD integration
- **test-execution-guide.md**: Test configuration and execution details
- **coverage-analysis-guide.md**: Coverage parsing and threshold checking
- **gap-analysis-guide.md**: Analyzing uncovered code and categorization
- **test-suggestions.md**: Missing test suggestion templates
- **best-practices.md**: Testing and coverage best practices

---

*Part of BMAD Enhanced Development Suite*
