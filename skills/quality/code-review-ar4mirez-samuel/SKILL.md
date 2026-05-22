---
name: code-review
description: |
  Pre-commit code quality review workflow. Use before committing changes to verify
  code quality, security, testing coverage, and adherence to project conventions.
  Supports both automated checking and interactive review modes.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Code Review Workflow

Systematic validation of code against all guardrails before committing. Supports both automated checking and interactive review modes.

---

## When to Use

| Trigger | Mode | Description |
|---------|------|-------------|
| **Pre-Commit** | Automated | Before any commit |
| **PR Review** | Interactive | During pull request review |
| **Feature Complete** | Both | After FEATURE/COMPLEX mode completion |
| **Code Handoff** | Interactive | Before transferring ownership |
| **Quality Gate** | Automated | CI/CD pipeline integration |

---

## Review Modes

### Automated Mode
Quick validation against all guardrails. Returns pass/fail/warning status.

**Best for**: Pre-commit checks, CI/CD integration, quick validation.

### Interactive Mode
Guided review with questions and confirmations. Deeper analysis.

**Best for**: PR reviews, complex changes, code handoffs.

---

## Prerequisites

Before starting review:

- [ ] Code is in a reviewable state (compiles, runs)
- [ ] All files to review are identified
- [ ] Access to test results (if available)
- [ ] Access to coverage reports (if available)

---

## Review Process

```
Phase 1: Code Quality Guardrails
    ↓
Phase 2: Security Guardrails
    ↓
Phase 3: Testing Guardrails
    ↓
Phase 4: Git Hygiene
    ↓
Phase 5: Report Generation
```

---

## Phase 1: Code Quality Guardrails

### 1.1 Function Length Check

**Guardrail**: No function exceeds 50 lines

```
Check: Count lines in each function/method
Pass: All functions ≤ 50 lines
Warn: Functions 40-50 lines (approaching limit)
Fail: Any function > 50 lines
```

**If Failed**:
- Identify functions exceeding limit
- Suggest extraction points for helper functions
- Recommend refactoring approach

### 1.2 File Length Check

**Guardrail**: No file exceeds 300 lines (components: 200, tests: 300, utils: 150)

```
Check: Count lines in each file
Pass: Files within limits
Warn: Files at 80%+ of limit
Fail: Files exceeding limits
```

**File Type Limits**:
| Type | Limit | 80% Warning |
|------|-------|-------------|
| Components | 200 | 160 |
| Tests | 300 | 240 |
| Utilities | 150 | 120 |
| Other | 300 | 240 |

### 1.3 Cyclomatic Complexity

**Guardrail**: Complexity ≤ 10 per function

```
Check: Analyze control flow (if, for, while, switch, &&, ||)
Pass: All functions ≤ 10
Warn: Functions 8-10
Fail: Any function > 10
```

**Complexity Calculation**:
- Start with 1
- +1 for each: if, elif, for, while, case, catch, &&, ||, ?:

### 1.4 Type Signatures

**Guardrail**: All exported functions have type signatures

```
Check: Verify exported functions have types
Pass: All exports typed
Warn: Internal functions missing types
Fail: Exported functions missing types
```

### 1.5 Documentation

**Guardrail**: All exported functions have documentation

```
Check: Verify docstrings/JSDoc on exports
Pass: All exports documented
Warn: Documentation exists but incomplete
Fail: Exported functions undocumented
```

### 1.6 Code Hygiene

**Guardrails**:
- No magic numbers (use named constants)
- No commented-out code
- No TODO without issue reference
- No dead code (unused imports, variables, functions)

```
Check: Scan for violations
Pass: None found
Warn: Minor violations (1-2 magic numbers)
Fail: Multiple violations
```

---

## Phase 2: Security Guardrails

### 2.1 Input Validation

**Guardrail**: All user inputs validated before processing

```
Check: Identify input sources (API params, form data, URL params)
Pass: All inputs validated with schema or type checks
Warn: Validation exists but not comprehensive
Fail: Raw user input used directly
```

**Input Sources to Check**:
- Request body/params
- Query strings
- Headers
- File uploads
- Environment variables from user

### 2.2 Database Queries

**Guardrail**: All queries use parameterized statements

```
Check: Scan for SQL/query construction
Pass: All queries parameterized
Fail: String concatenation in queries
```

**Red Flags**:
```javascript
// FAIL: String concatenation
`SELECT * FROM users WHERE id = ${id}`

// PASS: Parameterized
db.query('SELECT * FROM users WHERE id = $1', [id])
```

### 2.3 Secrets Detection

**Guardrail**: No secrets in code

```
Check: Scan for secret patterns
Pass: No secrets detected
Fail: Hardcoded secrets found
```

**Patterns to Detect**:
- API keys (`sk_live_`, `pk_live_`, `api_key=`)
- Passwords (`password=`, `passwd=`)
- Tokens (`token=`, `bearer`)
- Connection strings with credentials
- Private keys (`-----BEGIN RSA PRIVATE KEY-----`)

### 2.4 File Path Validation

**Guardrail**: All file operations validate paths

```
Check: Identify file operations
Pass: Path validation/sanitization present
Fail: Direct user input in file paths
```

**Red Flags**:
```javascript
// FAIL: Directory traversal possible
fs.readFile(userInput)

// PASS: Validated
const safePath = path.join(baseDir, path.basename(userInput))
```

### 2.5 Async Operations

**Guardrail**: All async operations have timeout/cancellation

```
Check: Identify async calls (fetch, DB queries, external APIs)
Pass: Timeouts configured
Warn: Some operations without timeout
Fail: No timeout handling
```

---

## Phase 3: Testing Guardrails

### 3.1 Coverage Thresholds

**Guardrail**: >80% business logic, >60% overall

```
Check: Review coverage report
Pass: Meets thresholds
Warn: 70-80% business / 50-60% overall
Fail: Below thresholds
```

### 3.2 Test Existence

**Guardrail**: All public APIs have unit tests

```
Check: Map public functions to test files
Pass: All public APIs tested
Warn: Most tested (>80%)
Fail: Significant gaps (<80%)
```

### 3.3 Regression Tests

**Guardrail**: Bug fixes include regression tests

```
Check: If fix, verify test added
Pass: Regression test present
Fail: No regression test for bug fix
```

### 3.4 Edge Cases

**Guardrail**: Edge cases explicitly tested

```
Check: Review test cases for boundaries
Pass: Null, empty, boundary values tested
Warn: Some edge cases missing
Fail: No edge case testing
```

**Required Edge Cases**:
- Null/undefined inputs
- Empty strings/arrays
- Boundary values (0, -1, MAX_INT)
- Invalid types
- Concurrent access (if applicable)

### 3.5 Test Independence

**Guardrail**: No test interdependencies

```
Check: Tests can run in any order
Pass: Tests isolated
Fail: Tests depend on execution order
```

---

## Phase 4: Git Hygiene

### 4.1 Commit Message Format

**Guardrail**: `type(scope): description` (conventional commits)

```
Check: Verify commit message format
Pass: Follows convention
Fail: Non-conventional format
```

**Valid Types**: feat, fix, docs, refactor, test, chore, perf, ci

### 4.2 Atomic Commits

**Guardrail**: One logical change per commit

```
Check: Review commit scope
Pass: Single logical change
Warn: Related changes (acceptable)
Fail: Unrelated changes bundled
```

### 4.3 Sensitive Data

**Guardrail**: No sensitive data in commits

```
Check: Scan staged files
Pass: No sensitive data
Fail: Secrets, credentials, or PII found
```

---

## Phase 5: Report Generation

### 5.1 Automated Report Format

```markdown
## Code Review Report

**Date**: 2025-01-15
**Files Reviewed**: 12
**Status**: ⚠️ WARNINGS (3 issues)

### Summary
| Category | Status | Issues |
|----------|--------|--------|
| Code Quality | ✅ Pass | 0 |
| Security | ⚠️ Warn | 2 |
| Testing | ✅ Pass | 0 |
| Git Hygiene | ⚠️ Warn | 1 |

### Issues Found

#### Security Warnings
1. **Missing timeout** in `src/api/fetch.ts:42`
   - External API call without timeout
   - Recommendation: Add 30s timeout

2. **Input validation** in `src/routes/users.ts:15`
   - Query parameter used without validation
   - Recommendation: Add Zod schema

#### Git Hygiene Warnings
1. **Large commit scope**
   - 8 files changed across 3 features
   - Recommendation: Split into separate commits

### Passed Checks
- ✅ All functions ≤ 50 lines
- ✅ All files within size limits
- ✅ No secrets detected
- ✅ Coverage at 82%
- ✅ Commit message format correct
```

### 5.2 Interactive Report Format

Interactive mode includes prompts:

```markdown
## Interactive Review: src/api/users.ts

### Function: createUser (lines 15-45)

**Observations**:
- 30 lines (within limit)
- Complexity: 6 (acceptable)
- Missing error handling for database failure

**Questions**:
1. Should we add explicit error handling for DB failures?
2. Should the validation schema be extracted to a separate file?

**Your Response**: [awaiting input]
```

---

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
# .github/workflows/code-review.yml
name: Code Review Checks

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Function Length Check
        run: |
          # Check no function > 50 lines
          # Implementation depends on language

      - name: Security Scan
        run: |
          # Run secret detection
          # Run input validation check

      - name: Coverage Check
        run: |
          npm test -- --coverage
          # Verify thresholds
```

---

## Checklist

### Pre-Commit (Automated)
- [ ] All functions ≤ 50 lines
- [ ] All files within size limits
- [ ] Complexity ≤ 10
- [ ] No secrets in code
- [ ] Inputs validated
- [ ] Tests pass
- [ ] Coverage meets thresholds
- [ ] Commit message follows convention

### PR Review (Interactive)
- [ ] All automated checks pass
- [ ] Code is understandable
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] No premature optimization
- [ ] No over-engineering
- [ ] Documentation updated
- [ ] Tests cover new functionality

---

## Related Workflows

- [security-audit.md](../../workflows/security-audit.md) - Deeper security analysis
- [testing-strategy.md](../../workflows/testing-strategy.md) - Comprehensive test planning
- [refactoring.md](../../workflows/refactoring.md) - When review identifies debt
- [troubleshooting.md](../../workflows/troubleshooting.md) - When review finds issues
