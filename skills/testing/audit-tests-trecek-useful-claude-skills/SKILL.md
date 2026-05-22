---
name: audit-tests
description: Audit the test suite for useless tests, consolidation opportunities, over-mocking, weak assertions, and other test quality issues. Use when user says "audit tests", "audit test suite", "review tests", or "test quality check". Generates an improvement plan in temp/ with explanations for each proposed change.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: audit-tests] Auditing test suite...'"
          once: true
---

# Test Suite Audit Skill

Audit the test suite to identify useless tests, consolidation opportunities, quality issues, and tests that don't validate what they claim. Produces an actionable improvement plan with explanations.

## When to Use

- User says "audit tests", "audit test suite", "review tests"
- User wants "test quality check" or "test cleanup"
- User asks to "find useless tests" or "consolidate tests"

## Critical Constraints

**NEVER:**
- Modify any source or test code files
- Flag tests as useless without reading and understanding them
- Recommend removing tests that guard against real regressions
- Recommend changes that would reduce meaningful coverage

**ALWAYS:**
- Use subagents for parallel exploration
- Read both the test AND the code it tests before judging
- Provide file paths, line numbers, and an explanation for each finding
- Write the improvement plan to `temp/audit-tests/test_audit_{YYYY-MM-DD_HHMMSS}.md`
- Categorize findings by issue type and severity

---

## Issue Categories

### Category 1: Useless Tests (HIGH)

Tests that provide no meaningful coverage. They pass regardless of whether the code works correctly.

**What to look for:**
- Tests that assert always-true conditions (e.g., `assert result is not None` when the function never returns None)
- Tests that verify tautologies (e.g., confirming an enum member is a valid enum member)
- Tests whose assertions would pass even if the code under test were completely broken
- Tests with no assertions at all (just call a function and check it doesn't crash)
- Tests in "testing mode" that bypass the logic they claim to test

### Category 2: Redundant / Consolidatable Tests (MEDIUM)

Tests that duplicate each other or could be combined without losing coverage.

**What to look for:**
- Multiple tests asserting the exact same behavior with trivially different inputs (candidates for parameterization)
- Identical fixtures or setup code defined in multiple places
- Tests in different files that exercise the same code path
- Contract tests that duplicate what unit tests already cover
- Integration tests that only exercise unit-level logic (no actual integration)

### Category 3: Over-Mocked Tests (HIGH)

Tests that mock so aggressively they no longer test real behavior. The test validates the mock wiring, not the production code.

**What to look for:**
- Tests that mock the system under test (mocking the handler inside a handler test)
- Auto-mocked database/IO layers where the test then only verifies mock call counts
- Tests that patch internal module functions instead of external boundaries
- Dependency injection tests that only verify args are passed through
- Tests where removing the production code entirely would still pass

### Category 4: Weak Assertions (HIGH)

Tests that have assertions too loose to catch real bugs.

**What to look for:**
- Inequality assertions where exact values are known (e.g., `assert count >= 2` when it should be `== 3`)
- Substring checks where full string comparison is appropriate
- `assert result` (truthy check) when specific value/type should be verified
- Mock call verification without checking call arguments
- Tests that check collection length but not contents

### Category 5: Misleading Tests (MEDIUM)

Tests whose name, docstring, or structure misrepresents what they actually verify.

**What to look for:**
- Test name says "error handling" but doesn't verify the error path
- Docstring describes behavior the test doesn't actually assert
- Test claims to verify integration but mocks all dependencies
- Exception tests that don't verify the exception was actually raised or caught
- Tests named for edge cases that actually test the happy path

### Category 6: Stale / Outdated Tests (MEDIUM)

Tests that no longer align with the current codebase.

**What to look for:**
- Tests for deprecated or removed functionality
- Tests that reference old file paths, class names, or module structure
- Fixtures marked as deprecated that are still defined
- Tests that are always skipped or conditionally disabled
- Tests whose setup creates state the production code no longer uses

### Category 7: Fixture Issues (LOW)

Problems in test fixtures that make tests harder to understand and maintain.

**What to look for:**
- Same fixture defined in multiple places with slight variations
- Deeply nested fixture chains where the dependency graph is unclear
- `autouse=True` fixtures where a significant portion of tests in scope don't need them. Assess the usage ratio: if more than ~30% of tests don't need the fixture, it should be explicit instead of autouse. The more expensive the fixture, the lower the tolerance for unnecessary execution.
- Overly complex fixtures (50+ lines of mock configuration)
- Dead fixtures that no test references
- Tests that create temporary files/directories directly instead of using test framework fixtures (e.g., pytest's `tmp_path`)
- Tests that manually set up resources the framework provides as fixtures

### Category 8: Misclassified Tests (LOW)

Tests placed in the wrong directory or category.

**What to look for:**
- Unit-level tests in integration directories (no multi-component interaction)
- Tests in contract/specification directories that duplicate standard unit tests
- Integration tests that could be unit tests (everything is mocked anyway)

### Category 9: Oversized Files (MEDIUM)

Test files or supporting files exceeding 1000 lines. Flag files approaching the threshold (800+) as warnings.

---

## Audit Workflow

### Step 1: Launch Parallel Subagents

Spawn subagents to explore different areas of the test suite. Divide by **test directory/module**, not by issue category — each subagent should assess all issue categories within its area.

Each subagent should read test files AND the corresponding production code to judge whether the test is meaningful. For each finding, note the file, line range, issue category, and a brief explanation of why it's a problem and what should change.

### Step 2: Consolidate and Deduplicate

After subagents complete:
1. Merge findings across subagents
2. Deduplicate (same test flagged from different angles)
3. Cross-reference fixture issues across test configuration files
4. Identify patterns that repeat across the codebase (systemic issues vs. one-offs)

### Step 3: Generate Improvement Plan

Write a structured plan to: `temp/audit-tests/test_audit_{YYYY-MM-DD_HHMMSS}.md`

Organize the plan into phases grouped by issue type. Each finding must include:
- **File path and line range**
- **Issue category and severity**
- **Explanation**: What the test does, why it's a problem, and what the concrete improvement is
- **Action**: Remove, consolidate, strengthen assertion, reduce mocking, relocate, etc.

Include a summary table at the top with counts by category.

### Step 4: Terminal Summary

Output a summary including:
- Plan file location
- Total findings by category and severity
- Top systemic issues (patterns that appear across many files)
- Estimated test count reduction from consolidation
- Next steps

---

## Exclusions

Do NOT flag:
- Tests that guard against known regressions (even if they look simple)
- Property-based tests (different testing philosophy)
- Test utilities and helper functions in test support directories
- Test infrastructure and safety mechanisms
- Tests that are intentionally minimal as smoke tests
- Shared fixtures in centralized test configuration
