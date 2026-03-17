---
name: avoid-test-interdependence
description: Never assume tests run in a specific order Use when writing and organizing tests. Testing category skill.
metadata:
  category: Testing
  priority: high
  is-built-in: true
  session-guardian-id: builtin_avoid_test_interdependence
---

# Avoid Test Interdependence

Never assume tests run in a specific order. Don't rely on data created by previous tests. Each test should create its own test data and clean up if needed. Use beforeEach for common setup rather than sequential tests. If you find yourself thinking "this test must run after that one," redesign your tests. This enables parallel execution and prevents cascading failures.