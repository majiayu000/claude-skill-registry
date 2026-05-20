---
name: go-testing
description: "Handles all Golang testing tasks including running tests, writing new tests, and fixing test failures. Follows MCPSpy testing conventions with require for critical assertions and assert for non-critical ones."
---

# Go Testing Skill

Provides guidance and automation for Golang testing tasks in the MCPSpy project.

## Testing Philosophy

- Use `require` library for assertions that should stop test execution on failure
- Use `assert` library for non-critical assertions where test should continue
- Choose internal vs external package testing based on what needs to be tested
- Test internal functions by placing test files in the same package (no `_test` suffix)
- Avoid creating externally facing functions solely for testing purposes

## When to Use This Skill

- Running unit tests with `go test`
- Writing new test files and test cases
- Debugging and fixing failing tests
- Implementing test fixtures and mocks
- Improving test coverage for the MCPSpy project
