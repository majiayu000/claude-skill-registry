---
name: test-failure-mindset
description: 'This skill should be used when encountering failing tests or when the user asks about "test failure analysis", "debugging tests", "why tests fail", or needs to set a balanced investigative approach for test failures. Establishes mindset that treats test failures as valuable signals requiring investigation, not automatic dismissal.'
version: "1.0.0"
last_updated: "2026-01-25"
python_compatibility: "3.11+"
user-invocable: true
---

# Test Failure Analysis Mindset

Establish a balanced investigative approach for all test failures encountered in this session.

## Core Principle

Tests are specifications - they define expected behavior. When they fail, it's a critical moment requiring balanced investigation, not automatic dismissal.

## Dual Hypothesis Approach

Always consider both possibilities when a test fails:

| Hypothesis A                    | Hypothesis B             |
| ------------------------------- | ------------------------ |
| Test expectations are incorrect | Implementation has a bug |
| Test is outdated                | Test caught a regression |
| Test has wrong assumptions      | Test found an edge case  |

## Investigation Protocol

For EVERY test failure:

### 1. Pause and Read

- Understand what the test is trying to verify
- Read its name, comments, and assertions carefully
- Check the test's history (git blame) for context

### 2. Trace the Implementation

- Follow the code path that leads to the failure
- Understand actual behavior vs. expected behavior
- Check if recent changes affected this code path

### 3. Consider the Context

- Is this testing a documented requirement?
- Would current behavior surprise a user?
- What would be the impact of each possible fix?

### 4. Make a Reasoned Decision

| Situation               | Action                             |
| ----------------------- | ---------------------------------- |
| Implementation is wrong | Fix the bug                        |
| Test is wrong           | Fix test AND document why          |
| Unclear                 | Seek clarification before changing |

### 5. Learn from the Failure

- What can this teach about the system?
- Should additional tests cover related cases?
- Is there a pattern being missed?

## Red Flags (Dangerous Patterns)

- 🚫 Immediately changing tests to match implementation
- 🚫 Assuming implementation is always correct
- 🚫 Bulk-updating tests without individual analysis
- 🚫 Removing "inconvenient" test cases
- 🚫 Adding mock/stub workarounds instead of fixing root causes

## Good Practices

- ✅ Treat each test failure as a potential bug discovery
- ✅ Document analysis in comments when fixing tests
- ✅ Write clear test names that explain intent
- ✅ When changing a test, explain why the original was wrong
- ✅ Consider adding more tests when finding ambiguity

## Example Responses

**Good**: "I see test_user_validation is failing. Let me trace through the validation logic to understand if this is catching a real bug or if the test's expectations are incorrect."

**Bad**: "The test is failing so I'll update it to match what the code does."

## Remember

Every test failure is an opportunity to:

- Discover and fix a bug before users do
- Clarify ambiguous requirements
- Improve system understanding
- Strengthen the test suite

**The goal is NOT to make tests pass quickly. The goal IS to ensure the system behaves correctly.**

## Related Skills

- **analyze-test-failures**: Detailed analysis of specific test failures
- **comprehensive-test-review**: Full test suite review
