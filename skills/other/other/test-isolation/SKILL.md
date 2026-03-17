---
name: test-isolation
description: Tests must not depend on execution order or state from other tests Use when writing and organizing tests. Testing category skill.
metadata:
  category: Testing
  priority: high
  is-built-in: true
  session-guardian-id: builtin_test_isolation
---

# Test Isolation

Tests must not depend on execution order or state from other tests. Reset state in beforeEach, use fresh instances, avoid global state. Each test should set up its own prerequisites. Isolated tests can run in parallel, fail independently, and are easier to debug. Mock external dependencies so unit tests don't require databases, APIs, or file systems.