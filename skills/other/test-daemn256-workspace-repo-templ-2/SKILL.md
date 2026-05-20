---
name: test
description: Run tests, analyze results, and produce a structured verdict
---

# Test

Uses **Test** persona. Take test execution output, parse it into structured results, produce a clear verdict, and recommend next actions.

**Prerequisites:** Test output provided (pasted or from execution)

---

## Phase 1: Parse Output

### Extract Structured Data

1. Identify the test framework from output format
2. Extract total, passed, failed, skipped counts
3. For failures, extract:
   - Test name
   - File and line location
   - Error message

### Output

```markdown
## Context Anchors

- **Phase:** 1 — Parse Output
- **Framework:** <detected framework>

## Execution Summary

| Metric  | Count |
| ------- | ----- |
| Total   | <N>   |
| Passed  | <N>   |
| Failed  | <N>   |
| Skipped | <N>   |

## Next Step

Continue to verdict.

**Approval Required:** No
```

---

## Phase 2: Produce Verdict

### Classify and Analyze

1. Apply verdict criteria:

| Verdict     | Criteria                                      |
| ----------- | --------------------------------------------- |
| **PASS**    | All tests pass, no critical warnings          |
| **PARTIAL** | Tests pass but with skipped tests or warnings |
| **FAIL**    | One or more test failures                     |

2. For failures, analyze likely cause
3. Suggest remediation approach

### Failure Analysis

For each failure:

1. Identify the failing test name
2. Extract the error message
3. Note the file and line if available
4. Analyze likely cause based on error type
5. Suggest remediation approach

### Common Failure Patterns

| Pattern            | Likely Cause                             |
| ------------------ | ---------------------------------------- |
| Assertion failed   | Logic error or incorrect expectation     |
| Null reference     | Missing setup or unexpected null         |
| Timeout            | Async issue or infinite loop             |
| Connection refused | External dependency unavailable          |
| Not found          | Missing file, resource, or configuration |

### Output

```markdown
## Context Anchors

- **Issue:** #<number> (if applicable)
- **Test suite:** <name>

## Execution Summary

| Metric  | Count |
| ------- | ----- |
| Total   | <N>   |
| Passed  | <N>   |
| Failed  | <N>   |
| Skipped | <N>   |

## Verdict: <PASS | PARTIAL | FAIL>

<one paragraph summary>

## Failure Details (if any)

| Test   | Location    | Error     | Likely Cause |
| ------ | ----------- | --------- | ------------ |
| <name> | <file:line> | <message> | <analysis>   |

## Recommendations

- <next step 1>
- <next step 2>

## Next Step

<action based on verdict>

**Approval Required:** No
```

### ⛔ CHECKPOINT

**STOP.** Verify the verdict matches actual test output before reporting.

**Critical:** Never trust exit code alone. Parse and report actual counts.

---

## Phase 3: TDD Workflow

### Write Tests First

1. Read the ticket and implementation plan to understand what is being built
2. Write failing tests that define the expected behavior
3. Confirm tests fail for the right reason (not setup errors)
4. Hand off to Implementer — tests define the contract
5. Resume after implementation to verify tests pass

---

## Phase 4: Coverage Analysis

### Assess Test Coverage

1. Run the coverage tool specified in `workspace.config.yaml`
2. Identify untested paths — not just line coverage, but branch and error coverage
3. Flag high-risk untested areas (auth, validation, data transforms)
4. Report coverage delta if a baseline exists

---

## Error Handling

| Error                   | Recovery                                          |
| ----------------------- | ------------------------------------------------- |
| Unparseable output      | Report what was understood, flag unknown sections |
| Mixed framework output  | Process each framework section separately         |
| No test output provided | Ask user to run tests and paste output            |
