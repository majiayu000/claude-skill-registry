---
name: aget-run-tests
description: Execute test suite and report results
archetype: developer
allowed-tools:
  - Bash
  - Read
  - Glob
---

# aget-run-tests

Execute test suites and report results. Supports unit tests, integration tests, and conformance tests with framework auto-detection.

## Instructions

When this skill is invoked:

1. **Detect Test Framework**
   - Check for pytest (pytest.ini, pyproject.toml)
   - Check for jest (package.json with jest)
   - Check for go test (go.mod)
   - Check for other common frameworks

2. **Execute Tests**
   - Run with appropriate verbosity
   - Capture timing information
   - Handle test scope (all, unit, integration, specific)

3. **Process Results**
   - Count pass/fail/skip
   - Capture failure details
   - Note coverage if available

4. **Report Findings**
   - Summary statistics
   - Failure details with location
   - Actionable next steps

## Execution Commands

```bash
# Python (pytest)
python3 -m pytest -v [path]

# JavaScript (jest)
npm test -- --verbose

# Go
go test -v ./...

# Python (unittest)
python3 -m unittest discover -v
```

## Output Format

```markdown
## Test Results

### Summary

| Metric | Value |
|--------|-------|
| Total | [N] |
| Passed | [N] |
| Failed | [N] |
| Skipped | [N] |
| Duration | [Xs] |
| Coverage | [N%] (if available) |

### Status: [PASS/FAIL]

### Failures (if any)

#### [Test Name]
- **File**: [path:line]
- **Expected**: [value]
- **Actual**: [value]
- **Error**: [message]

### Next Steps

1. [Action to fix failures]
```

## Constraints

- **C1**: NEVER modify test files during execution — test execution is read-only
- **C2**: NEVER suppress test failures — all failures must be visible
- **C3**: NEVER run tests with side effects without user consent — integration tests may modify state

## Related

- SKILL-022: aget-run-tests specification
- ONTOLOGY_developer.yaml: Test, Unit_Test, Test_Result concepts
- CAP-DEV-001: Test Execution capability
