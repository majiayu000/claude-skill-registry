---
name: test
description: Run tests, analyze results, and produce a structured verdict.
---

# Test

The Test persona drives this workflow. Take test execution output, parse it into structured results, produce a clear verdict, and recommend next actions.

**Prerequisites:** Test output provided (pasted or from execution).

---

## Phase 1: Parse Output

Extract structured data from raw test output.

### Steps

1. Identify the test framework from output format
2. Extract total, passed, failed, skipped counts
3. For failures, extract test name, location, error message

---

## Phase 2: Produce Verdict

Classify the result and provide analysis.

### Verdict Criteria

| Verdict     | Criteria                                      |
| ----------- | --------------------------------------------- |
| **PASS**    | All tests pass, no critical warnings          |
| **PARTIAL** | Tests pass but with skipped tests or warnings |
| **FAIL**    | One or more test failures                     |

### Failure Analysis

For each failure:

1. Identify the failing test name
2. Extract the error message
3. Note the file and line if available
4. Analyze likely cause
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

- **Issue:** #<number> - <title> (if applicable)
- **Suite:** <test suite name>

## Test Results

| Suite | Total | Pass | Fail | Skip |
| ----- | ----- | ---- | ---- | ---- |
| ...   | ...   | ...  | ...  | ...  |

## Verdict: PASS | PARTIAL | FAIL

### Failures (if any)

| Test   | Error           | Location    | Likely Cause   |
| ------ | --------------- | ----------- | -------------- |
| <name> | <error message> | <file:line> | <likely cause> |

### Recommendations

- <next action>

## Next Step

<what comes next>

**Approval Required:** No
```

### ⛔ CHECKPOINT

**STOP.** Verify the verdict matches actual test output before reporting.

**Critical:** Never trust exit code alone. Parse and report actual counts.

---

## Error Handling

| Error                   | Recovery                                          |
| ----------------------- | ------------------------------------------------- |
| Unparseable output      | Report what was understood, flag unknown sections |
| Mixed framework output  | Process each framework section separately         |
| No test output provided | Ask user to run tests and paste output            |
