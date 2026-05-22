---
name: analyze-test-failures
description: 'This skill should be used when the user asks to "analyze failing tests", "debug test failures", "investigate test errors", or provides specific failing test cases to examine. Analyzes failing test cases with a balanced, investigative approach to determine whether failures indicate test issues or genuine bugs.'
version: "1.0.0"
last_updated: "2026-01-25"
python_compatibility: "3.11+"
user-invocable: true
argument-hint: "<test_file_or_test_name>"
---

# Analyze Test Failures

Analyze failing test cases with a balanced, investigative approach.

## Context

When tests fail, there are two primary possibilities:

1. **False positive**: The test itself is incorrect
2. **True positive**: The test discovered a genuine bug

Assuming tests are wrong by default is a dangerous anti-pattern that defeats the purpose of testing.

## Analysis Process

### 1. Initial Analysis

- Read the failing test carefully, understanding its intent
- Examine the test's assertions and expected behavior
- Review the error message and stack trace

### 2. Investigate the Implementation

- Check the actual implementation being tested
- Trace through the code path that leads to the failure
- Verify that implementation matches documented behavior

### 3. Apply Critical Thinking

For each failing test, ask:

- What behavior is the test trying to verify?
- Is this behavior clearly documented or implied by the API design?
- Does the current implementation actually provide this behavior?
- Could this be an edge case the implementation missed?

### 4. Make a Determination

Classify the failure as one of:

| Classification         | Meaning                           |
| ---------------------- | --------------------------------- |
| **Test Bug**           | Test's expectations are incorrect |
| **Implementation Bug** | Code doesn't behave as it should  |
| **Ambiguous**          | Intended behavior is unclear      |

### 5. Document Reasoning

Provide clear explanation including:

- Evidence supporting the conclusion
- Specific mismatch between expectation and reality
- Recommended fix (to test or implementation)

## Example Analyses

### Example 1: Ambiguous Behavior

**Scenario**: Test expects `calculateDiscount(100, 0.2)` to return 20, but it returns 80

**Analysis**:

- Test assumes function returns discount amount
- Implementation returns price after discount
- Function name is ambiguous

**Determination**: Ambiguous
**Recommendation**: Check documentation or clarify intended behavior

### Example 2: Implementation Bug

**Scenario**: Test expects `validateEmail("user@example.com")` to return true, but it returns false

**Analysis**:

- Test provides a valid email format
- Implementation regex is missing support for dots in domain
- Other valid emails also fail

**Determination**: Implementation Bug
**Recommendation**: Fix the regex to properly validate email addresses per RFC standards

### Example 3: Test Bug

**Scenario**: Test expects `divide(10, 0)` to return 0, but it throws an error

**Analysis**:

- Test assumes division by zero returns 0
- Implementation throws DivisionByZeroError
- Standard mathematical behavior is to treat as undefined/error

**Determination**: Test Bug
**Recommendation**: Update test to expect an error, not 0

## Output Format

For each failing test, provide:

```text
Test: [test name/description]
Failure: [what failed and how]

Investigation:
- Test expects: [expected behavior]
- Implementation does: [actual behavior]
- Root cause: [why they differ]

Determination: [Test Bug | Implementation Bug | Ambiguous]

Recommendation:
[Specific fix to either test or implementation]
```

## Key Principles

- NEVER automatically assume the test is wrong
- ALWAYS consider that the test might have found a real bug
- When uncertain, lean toward investigating the implementation
- Tests are often your specification - they define expected behavior
- A failing test is a gift - it's either catching a bug or clarifying requirements

## Related Skills

- **test-failure-mindset**: Set investigative approach for session
- **comprehensive-test-review**: Full test suite review
