---
name: Testing
description: Standards for Component Test Harnesses and TestBed.
metadata:
  labels: [angular, testing, harness, testbed]
  triggers:
    files: ['**/*.spec.ts']
    keywords: [TestBed, ComponentFixture, TestHarness, provideHttpClientTesting]
---

# Testing

## **Priority: P1 (HIGH)**

## Principles

- **Harnesses**: Always use `ComponentTestHarness` (Angular Material Harnesses) to interact with components. Avoid querying DOM/CSS selectors directly.
- **Provider Mocks**: Use `provideHttpClientTesting()` instead of mocking `HttpClient` manually.
- **Signal Testing**: Signals update synchronously. No need for `fakeAsync` usually.

## Guidelines

- **Avoid logic**: Tests should just assert inputs and outputs.
- **Spectator**: Consider using libraries like `@ngneat/spectator` for cleaner boilerplate if allowed.

## References

- [Harness Pattern](references/harness-pattern.md)
