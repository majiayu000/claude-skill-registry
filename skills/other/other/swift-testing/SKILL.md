---
name: swift-testing
description: 'Expert guidance on Swift Testing best practices, patterns, and implementation. Use when developers mention: (1) Swift Testing, @Test, #expect, #require, or @Suite, (2) "use Swift Testing" or "modern testing patterns", (3) test doubles, mocks, stubs, spies, or fixtures, (4) unit tests, integration tests, or snapshot tests, (5) migrating from XCTest to Swift Testing, (6) TDD, Arrange-Act-Assert, or F.I.R.S.T. principles, (7) parameterized tests or test organization.'
---
# Swift Testing

## Overview

This skill provides expert guidance on Swift Testing, covering the modern Swift Testing framework, test doubles (mocks, stubs, spies), fixtures, integration testing, snapshot testing, and migration from XCTest. Use this skill to help developers write reliable, maintainable tests following F.I.R.S.T. principles and Arrange-Act-Assert patterns.

## Agent Behavior Contract (Follow These Rules)

1. Use Swift Testing framework (`@Test`, `#expect`, `#require`, `@Suite`) for all new tests, not XCTest.
2. Always structure tests with clear Arrange-Act-Assert phases.
3. Follow F.I.R.S.T. principles: Fast, Isolated, Repeatable, Self-Validating, Timely.
4. Use proper test double terminology per Martin Fowler's taxonomy (Dummy, Fake, Stub, Spy, SpyingStub, Mock).
5. Place fixtures close to models with `#if DEBUG`, not in test targets.
6. Place test doubles close to interfaces with `#if DEBUG`, not in test targets.
7. Prefer state verification over behavior verification - simpler, less brittle tests.
8. Use `#expect` for soft assertions (continue on failure) and `#require` for hard assertions (stop on failure).

## Quick Decision Tree

When a developer needs testing guidance, follow this decision tree:

1. **Starting fresh with Swift Testing?**
   - Read `references/test-organization.md` for suites, tags, traits
   - Read `references/async-testing.md` for async test patterns

2. **Need to create test data?**
   - Read `references/fixtures.md` for fixture patterns and placement
   - Read `references/test-doubles.md` for mock/stub/spy patterns

3. **Testing multiple inputs?**
   - Read `references/parameterized-tests.md` for parameterized testing

4. **Testing module interactions?**
   - Read `references/integration-testing.md` for integration test patterns

5. **Testing UI for regressions?**
   - Read `references/snapshot-testing.md` for snapshot testing setup

6. **Testing data structures or state?**
   - Read `references/dump-snapshot-testing.md` for text-based snapshot testing

7. **Migrating from XCTest?**
   - Read `references/migration-xctest.md` for migration guide

## Triage-First Playbook (Common Errors -> Next Best Move)

- "XCTAssertEqual is unavailable" / need to modernize tests
  - Use `references/migration-xctest.md` for XCTest to Swift Testing migration
- Need to test async code
  - Use `references/async-testing.md` for async patterns, confirmation, timeouts
- Tests are slow or flaky
  - Check F.I.R.S.T. principles, use proper mocking per `references/test-doubles.md`
- Need deterministic test data
  - Use `references/fixtures.md` for fixture patterns with fixed dates
- Need to test multiple scenarios efficiently
  - Use `references/parameterized-tests.md` for parameterized testing
- Need to verify component interactions
  - Use `references/integration-testing.md` for integration test patterns

## Core Syntax

### Basic Test

```swift
import Testing

@Test func basicTest() {
    #expect(1 + 1 == 2)
}
```

### Test with Description

```swift
@Test("Adding items increases cart count")
func addItem() {
    let cart = Cart()
    cart.add(item)
    #expect(cart.count == 1)
}
```

### Async Test

```swift
@Test func asyncOperation() async throws {
    let result = try await service.fetch()
    #expect(result.isValid)
}
```

## Arrange-Act-Assert Pattern

Structure every test with clear phases:

```swift
@Test func calculateTotal() {
    // Given
    let cart = ShoppingCart()
    cart.add(Item(price: 10))
    cart.add(Item(price: 20))

    // When
    let total = cart.calculateTotal()

    // Then
    #expect(total == 30)
}
```

## Assertions

### #expect - Soft Assertion

Continues test execution after failure:

```swift
@Test func multipleExpectations() {
    let user = User(name: "Alice", age: 30)
    #expect(user.name == "Alice")  // If fails, test continues
    #expect(user.age == 30)        // This still runs
}
```

### #require - Hard Assertion

Stops test execution on failure:

```swift
@Test func requireExample() throws {
    let user = try #require(fetchUser())  // Stops if nil
    #expect(user.name == "Alice")
}
```

### Error Testing

```swift
@Test func throwsError() {
    #expect(throws: ValidationError.self) {
        try validate(invalidInput)
    }
}

@Test func throwsSpecificError() {
    #expect(throws: ValidationError.emptyField) {
        try validate("")
    }
}
```

## F.I.R.S.T. Principles

| Principle | Description | Application |
|-----------|-------------|-------------|
| **Fast** | Tests execute in milliseconds | Mock expensive operations |
| **Isolated** | Tests don't depend on each other | Fresh instance per test |
| **Repeatable** | Same result every time | Mock dates, network, external deps |
| **Self-Validating** | Auto-report pass/fail | Use `#expect`, never rely on `print()` |
| **Timely** | Write tests alongside code | Use parameterized tests for edge cases |

## Test Double Quick Reference

Per [Martin Fowler's definition](https://martinfowler.com/articles/mocksArentStubs.html):

| Type | Purpose | Verification |
|------|---------|--------------|
| **Dummy** | Fill parameters, never used | N/A |
| **Fake** | Working implementation with shortcuts | State |
| **Stub** | Provides canned answers | State |
| **Spy** | Records calls for verification | State |
| **SpyingStub** | Stub + Spy combined (most common) | State |
| **Mock** | Pre-programmed expectations, self-verifies | Behavior |

**Important**: What Swift community calls "Mock" is usually a **SpyingStub**.

For detailed patterns, see `references/test-doubles.md`.

## Test Double Placement

Place test doubles **close to the interface**, not in test targets:

```swift
// In PersonalRecordsCore-Interface/Sources/...

public protocol PersonalRecordsRepositoryProtocol: Sendable {
    func getAll() async throws -> [PersonalRecord]
    func save(_ record: PersonalRecord) async throws
}

#if DEBUG
public final class PersonalRecordsRepositorySpyingStub: PersonalRecordsRepositoryProtocol {
    // Spy: Captured calls
    public private(set) var savedRecords: [PersonalRecord] = []

    // Stub: Configurable responses
    public var recordsToReturn: [PersonalRecord] = []
    public var errorToThrow: Error?

    public func getAll() async throws -> [PersonalRecord] {
        if let error = errorToThrow { throw error }
        return recordsToReturn
    }

    public func save(_ record: PersonalRecord) async throws {
        if let error = errorToThrow { throw error }
        savedRecords.append(record)
    }
}
#endif
```

## Fixtures

Place fixtures **close to the model**:

```swift
// In Sources/Models/PersonalRecord.swift

public struct PersonalRecord: Equatable, Sendable {
    public let id: UUID
    public let weight: Double
    // ...
}

#if DEBUG
extension PersonalRecord {
    public static func fixture(
        id: UUID = UUID(),
        weight: Double = 100.0
        // ... defaults for all properties
    ) -> PersonalRecord {
        PersonalRecord(id: id, weight: weight)
    }
}
#endif
```

For detailed patterns, see `references/fixtures.md`.

## Test Pyramid

```
        +-------------+
        |   UI Tests  |  5%  - End-to-end flows
        |   (E2E)     |
        +-------------+
        | Integration |  15% - Module interactions
        |    Tests    |
        +-------------+
        |    Unit     |  80% - Individual components
        |    Tests    |
        +-------------+
```

## Reference Files

Load these files as needed for specific topics:

- **`test-organization.md`** - Suites, tags, traits, parallel execution
- **`parameterized-tests.md`** - Testing multiple inputs efficiently
- **`async-testing.md`** - Async patterns, confirmation, timeouts, cancellation
- **`migration-xctest.md`** - Complete XCTest to Swift Testing migration guide
- **`test-doubles.md`** - Complete taxonomy with examples (Dummy, Fake, Stub, Spy, SpyingStub, Mock)
- **`fixtures.md`** - Fixture patterns, placement, and best practices
- **`integration-testing.md`** - Module interaction testing patterns
- **`snapshot-testing.md`** - UI regression testing with SnapshotTesting library
- **`dump-snapshot-testing.md`** - Text-based snapshot testing for data structures

## Best Practices Summary

1. **Use Swift Testing for new tests** - Modern syntax, better features
2. **Follow Arrange-Act-Assert** - Clear test structure
3. **Apply F.I.R.S.T. principles** - Fast, Isolated, Repeatable, Self-Validating, Timely
4. **Place fixtures near models** - With `#if DEBUG` guards
5. **Place test doubles near interfaces** - With `#if DEBUG` guards
6. **Prefer state verification** - Simpler, less brittle than behavior verification
7. **Use parameterized tests** - For testing multiple inputs efficiently
8. **Follow test pyramid** - 80% unit, 15% integration, 5% UI

## Verification Checklist (When You Write Tests)

- Tests follow Arrange-Act-Assert pattern
- Test names describe behavior, not implementation
- Fixtures use sensible defaults, not random values
- Test doubles are minimal (only stub what's needed)
- Async tests use proper patterns (async/await, confirmation)
- Tests are fast (mock expensive operations)
- Tests are isolated (no shared state)
- Tests are repeatable (no flaky date/time dependencies)

