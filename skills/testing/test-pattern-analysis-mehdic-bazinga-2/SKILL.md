---
name: test-pattern-analysis
description: Analyze existing tests to identify patterns, fixtures, and conventions before writing new tests
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Test Pattern Analysis Skill

You are the test-pattern-analysis skill. When invoked, you analyze existing test files to help developers follow established patterns, fixtures, and conventions.

## When to Invoke This Skill

**Invoke this skill when:**
- Before writing new tests
- Developer needs to follow existing test conventions
- Looking for reusable fixtures or utilities
- Understanding test framework and patterns
- Ensuring consistency with existing tests

**Do NOT invoke when:**
- No existing tests in project
- First tests being written (no patterns yet)
- Fixing typos in tests
- Emergency bug fixes (skip pattern analysis)

---

## Your Task

When invoked:
1. Execute the test pattern analysis script
2. Read the generated analysis report
3. Return a summary to the calling agent

---

## Step 1: Execute Test Pattern Analysis Script

Use the **Bash** tool to run the pre-built analysis script:

```bash
python3 .claude/skills/test-pattern-analysis/analyze_tests.py
```

This script will:
- Detect test framework (pytest, jest, go test, JUnit)
- Find and analyze existing test files
- Identify common fixtures and test utilities
- Extract test naming conventions
- Find similar tests for reference
- Generate `bazinga/artifacts/{SESSION_ID}/skills/test_patterns.json`

---

## Step 2: Read Generated Report

Use the **Read** tool to read:

```bash
bazinga/artifacts/{SESSION_ID}/skills/test_patterns.json
```

Extract key information:
- `framework` - Detected test framework
- `common_fixtures` - Reusable test fixtures
- `test_patterns` - Structure patterns (AAA, Given-When-Then)
- `similar_tests` - Related existing tests
- `suggested_tests` - Recommended test cases
- `coverage_target` - Project coverage standard
- `utilities` - Test helper functions

---

## Step 3: Return Summary

Return a concise summary to the calling agent:

```
Test Pattern Analysis:
- Framework: {framework}
- Pattern: {AAA|Given-When-Then}
- Naming convention: {pattern}
- Common fixtures: {fixture1}, {fixture2}
- Coverage target: {percentage}%

Suggested test cases:
1. {test case 1}
2. {test case 2}
3. {test case 3}

Similar tests to reference:
- {file1}: {test_name}
- {file2}: {test_name}

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/test_patterns.json
```

---

## Example Invocation

**Scenario: Writing Tests for Password Reset**

Input: Developer needs to write tests for new password reset feature

Expected output:
```
Test Pattern Analysis:
- Framework: pytest
- Pattern: AAA (Arrange-Act-Assert)
- Naming convention: test_<function>_<scenario>_<expected>
- Common fixtures: test_client, test_db, test_user
- Coverage target: 80%

Suggested test cases:
1. test_password_reset_valid_email_sends_token
2. test_password_reset_invalid_email_returns_error
3. test_password_reset_expired_token_returns_error
4. test_password_reset_rate_limiting_prevents_abuse

Similar tests to reference:
- tests/test_auth.py: test_login_valid_credentials_returns_token
- tests/test_email.py: test_send_email_valid_address_succeeds

Reusable fixtures:
- test_client (conftest.py): Flask test client
- test_user (conftest.py): Create test user in database
- mock_email_service (conftest.py): Mock email sending

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/test_patterns.json
```

**Scenario: No Tests Found**

Input: Developer trying to analyze patterns in project with no tests

Expected output:
```
Test Pattern Analysis:
- Framework: detected (pytest)
- Pattern: N/A

No existing tests found. Cannot extract patterns.

Recommendations:
1. Start with standard pytest conventions
2. Use AAA (Arrange-Act-Assert) pattern
3. Name tests: test_<function>_<scenario>_<expected>
4. Target 80% code coverage
5. Create conftest.py for shared fixtures

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/test_patterns.json
```

---

## Error Handling

**If no test files found:**
- Return: "No existing tests found. Cannot extract patterns. Developer should create tests from scratch using framework defaults."

**If no fixtures found:**
- Return: "No common fixtures found. Developer may need to create setup functions."

**If framework detection fails:**
- Try to infer from file patterns
- Return: "Could not detect test framework. Please specify framework."

**If no similar tests found:**
- Return: "No similar tests found. Suggest generic test patterns (happy path, error cases, edge cases)."

---

## Notes

- The script handles all framework detection and pattern extraction
- Focuses on reusable patterns that save developer time
- Prioritizes fixtures and utilities that can be reused
- Suggests comprehensive test cases including edge cases
- Ensures naming conventions are followed for consistency
