---
name: test_driven_agent
description: An advanced testing protocol that enforces TDD (Test Driven Development) and self-healing tests.
allowed-tools: Bash, Read, Edit, Write
---

# Test Driven Agent Protocol

## 1. The Red-Green-Refactor Cycle

1.  **Red**: Write a test that fails (demonstrating the bug or missing feature).
    - _Agent Note_: If fixing a bug, YOU MUST reproduce it with a test first.
2.  **Green**: Write the minimal code to pass the test.
3.  **Refactor**: Clean up the code while ensuring tests still pass.

## 2. Test Coverage Requirements

- **Happy Path**: The "standard" usage case.
- **Sad Path**: Error states, network failures, invalid inputs.
- **Edge Cases**: Empty lists, max values, concurrent actions.

## 3. Self-Healing Mandate

If a test fails after your changes:

- **DO NOT** delete the test.
- **DO NOT** comment out the assertion.
- **DO NOT** change the test expectation to match the buggy result (unless the spec changed).
- **DO**: Fix the implementation logic until the test passes.

## 4. Integration vs Unit

- **Unit**: Mock external dependencies (Supabase, API). Fast, isolated.
- **Integration**: Test the hook or service with realistic (mocked) data flows.

## 5. Verification Checklist

- [ ] Did I write a test case for this requirement?
- [ ] Did I run `npm test <filename>`?
- [ ] Did I check specifically for regression in related headers/components?
