---
name: test-one-thing
description: A test should have one reason to fail Use when writing and organizing tests. Testing category skill.
metadata:
  category: Testing
  priority: high
  is-built-in: true
  session-guardian-id: builtin_test_one_thing
---

# Test One Thing

A test should have one reason to fail. Use descriptive test names that explain the scenario and expected outcome (e.g., "shouldReturnNullWhenUserNotFound"). Avoid multiple assertions testing unrelated behaviors. If a test name requires "and," consider splitting it. This makes failures immediately understandable and pinpoints issues precisely.