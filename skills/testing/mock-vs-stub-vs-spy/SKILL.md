---
name: mock-vs-stub-vs-spy
description: Stubs provide canned responses to calls made during tests Use when writing and organizing tests. Testing category skill.
metadata:
  category: Testing
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_test_doubles
---

# Mock vs Stub vs Spy

Stubs provide canned responses to calls made during tests. Mocks verify that specific interactions occurred. Spies wrap real implementations to track calls while executing real behavior. Use stubs for dependencies that return data. Use mocks when verifying the code under test calls dependencies correctly. Prefer stubs over mocks—test behavior, not implementation.