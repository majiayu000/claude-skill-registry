---
name: Swift Testing
description: Standards for XCTest, Async Tests, and Test Organization
metadata:
  labels: [swift, testing, xctest, async-testing]
  triggers:
    files: ['**/*Tests.swift']
    keywords: ['XCTestCase', 'XCTestExpectation', 'XCTAssert']
---

# Swift Testing Standards

## **Priority: P0**

## Implementation Guidelines

### XCTest Framework

- **Standard Naming**: Prefix test methods with `test` (e.g., `testUserLoginSuccessful`).
- **Setup/Teardown**: Use `setUpWithError()` and `tearDownWithError()` for environment management.
- **Assertions**: Use specific assertions: `XCTAssertEqual`, `XCTAssertNil`, `XCTAssertTrue`, etc.

### Async Testing

- **Async/Await**: Mark test methods as `async` and use `await` directly inside them.
- **Expectations**: Use `XCTestExpectation` for callback-based or delegate-based async logic.
- **Timeout**: Always set reasonable timeouts for expectations to avoid hanging CI.

### Test Organization

- **Unit Tests**: Focus on logic isolation using mocks/stubs for dependencies.
- **UI Tests**: Test user flows using `XCUIApplication` and accessibility identifiers.
- **Coverage**: Aim for high coverage on critical business logic and state transitions.

## Anti-Patterns

- **Thread Sleeps**: `**No Thread.sleep**: Use expectations or await.`
- **Force Unwrapping in Tests**: `**No user!**: Use XCTUnwrap(user) for better failure messages.`
- **Missing Assertions**: `**Tests must assert**: A test that only runs code is not a test.`

## References

- [XCTest Patterns & Async Tests](references/implementation.md)
