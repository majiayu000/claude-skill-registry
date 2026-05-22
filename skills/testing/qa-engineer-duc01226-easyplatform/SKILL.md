---
name: qa-engineer
description: Assist QA Engineers with test planning, test case generation from acceptance criteria, coverage analysis, and regression test identification. Use when creating test plans, generating test cases, analyzing test coverage, or identifying regression risks. Triggers on keywords like "test plan", "test cases", "test spec", "test coverage", "regression", "QA", "testing strategy", "edge cases".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite
---

# QA Engineer Assistant

Help QA Engineers create comprehensive test specifications, generate test cases from acceptance criteria, and ensure adequate test coverage.

---

## Core Capabilities

### 1. Test Planning
- Define test scope and strategy
- Identify test environments and data needs
- Plan regression test suites

### 2. Test Case Generation

#### From Acceptance Criteria
Convert GIVEN/WHEN/THEN to test cases:
```
AC: Given user is logged in
    When user clicks logout
    Then user is redirected to login page

TC: TC-AUTH-001: Successful logout
    Precondition: User authenticated
    Steps:
      1. Click logout button
      2. Observe redirect
    Expected: Login page displayed
    Evidence: {file}:{line}
```

### 3. Test Types

| Type | Purpose | When |
|------|---------|------|
| Unit | Single function | During dev |
| Integration | Component interaction | After merge |
| E2E | Full user flow | Before release |
| Regression | Existing functionality | Every sprint |
| Smoke | Critical paths | Every deploy |
| Performance | Load/stress | Pre-release |

### 4. Coverage Analysis
- Map test cases to requirements
- Identify coverage gaps
- Calculate coverage percentage

---

## Test Case Format

### Standard Format
```markdown
#### TC-{MOD}-{NNN}: {Descriptive title}
- **Priority:** P1 | P2 | P3
- **Type:** Positive | Negative | Boundary | Integration
- **Preconditions:** {Setup required}
- **Test Data:** {Data requirements}

**Steps:**
1. {Action step}
2. {Action step}
3. {Verification step}

**Expected Result:**
- {Observable outcome}

**Evidence:** `{FilePath}:{LineNumber}`
```

### Gherkin Format
```markdown
#### TC-{MOD}-{NNN}: {Title}
- **Priority:** P1
- **Type:** Positive

**Given** {precondition}
**And** {additional setup}
**When** {user action}
**Then** {expected outcome}
**And** {additional verification}

**Evidence:** `{FilePath}:{LineNumber}`
```

---

## Workflow Integration

### Creating Test Spec from PBI
When user runs `/test-spec {pbi-file}`:
1. Read PBI and acceptance criteria
2. Identify test scenarios (positive, negative, edge)
3. Create test specification structure
4. Save to `team-artifacts/test-specs/`

### Generating Test Cases
When user runs `/test-cases {test-spec-file}`:
1. Read test specification
2. Generate detailed test cases
3. Assign TC IDs (TC-{MOD}-{NNN})
4. Find code evidence for each case
5. Update test spec with cases

---

## Test ID Conventions

### Module Codes
| Module | Code |
|--------|------|
| TextSnippet | TXT |
| ExampleApp | EXP |
| Accounts | ACC |
| Common | COM |

### ID Format
```
TC-{MOD}-{NNN}

Examples:
TC-TXT-001  # TextSnippet test case 1
TC-EXP-015  # ExampleApp test case 15
TC-ACC-101  # Accounts integration test
TC-COM-201  # Common edge case
```

---

## Edge Case Categories

### Input Validation
- Empty/null values
- Boundary values (min, max, min-1, max+1)
- Invalid formats
- SQL injection attempts
- XSS payloads

### State-Based
- First use (empty state)
- Maximum capacity
- Concurrent access
- Session timeout

### Integration
- Service unavailable
- Network timeout
- Partial data response
- Rate limiting

---

## Evidence Requirements

**MANDATORY**: Every test case must have code evidence.

### Valid Evidence Formats
```
{RelativeFilePath}:{LineNumber}
{RelativeFilePath}:{StartLine}-{EndLine}
```

### Finding Evidence
1. Search for error messages in `ErrorMessage.cs`
2. Find validation logic in Command handlers
3. Locate frontend validation in components
4. Reference entity constraints

---

## Output Conventions

### File Naming
```
{YYMMDD}-qa-testspec-{feature-slug}.md
```

### Test Spec Structure
1. Overview
2. Test Summary (counts)
3. Functional Tests
4. Integration Tests
5. Edge Cases
6. Test Data Requirements
7. Regression Impact
8. Sign-Off

---

## Quality Checklist

Before completing QA artifacts:
- [ ] Every test case has TC-{MOD}-{NNN} ID
- [ ] Every test case has Evidence field with file:line
- [ ] Test summary counts match actual test cases
- [ ] At least 3 categories: positive, negative, edge
- [ ] Regression impact identified
- [ ] Test data requirements documented

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
