---
name: integration-test-strategy
description: "Test real interactions between components: API endpoints with databases, services with external APIs Use when writing and organizing tests. Testing category skill."
metadata:
  category: Testing
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_integration_test_strategy
---

# Integration Test Strategy

Test real interactions between components: API endpoints with databases, services with external APIs. Use test databases or in-memory databases for data layer tests. Mock only external services you don't control. Test error handling across boundaries. Integration tests are slower than unit tests—focus them on critical paths and component boundaries.