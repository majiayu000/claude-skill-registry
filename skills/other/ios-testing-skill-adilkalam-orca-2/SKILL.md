---
name: ios-testing-skill
description: >
  Skill describing modern iOS testing patterns: Swift Testing vs XCTest,
  XCUITest best practices, and OS 5.2 expectations for coverage and flakiness.
---

# iOS Testing Skill – Swift Testing, XCTest, XCUITest

This skill centralizes iOS testing guidance so that testing agents and gates
can stay lean while following consistent patterns.

It is used by:
- `ios-testing-specialist`
- `ios-ui-testing-specialist`
- `ios-verification`
- `ios-architect` / `ios-builder` when planning or implementing tests.

## Core Concepts

- **Swift Testing vs XCTest**
  - Prefer Swift Testing for Swift 6+ targets where available.
  - Maintain parity when migrating from XCTest; do not regress coverage.
  - Use `@Test` and `#expect/#require` with clear naming and tagging.

- **Unit vs Integration vs UI**
  - Unit tests: small, isolated; no network/DB unless explicitly integration.
  - Integration tests: limited external dependencies; deterministic configs.
  - UI tests (XCUITest): page objects, accessibility identifiers, async-safe waits.

- **Testing SwiftData Models**
  - Use ModelContainer with `isStoredInMemoryOnly: true` for tests
  - Test @Relationship cascade deletes verify dependent data is removed
  - Verify FetchDescriptor queries return expected results
  - Use @MainActor for SwiftData operations in async tests
  - Test unique constraints (@Attribute(.unique)) enforce uniqueness

- **Testing SwiftUI Atoms**
  - Use `AtomTestContext` for isolated atom testing
  - Override atoms with `.override()` for dependency injection
  - Test computed atoms (ValueAtom) derive correct values from dependencies
  - Verify StateAtom mutations trigger dependent atom updates
  - Test atom dependency graphs with `graphDescription()`

## Context7 Libraries

Agents using this skill MAY consult:

- `os2-ios-testing`
  - Swift Testing patterns and examples,
  - XCTest/XCUITest structure and migration guidance,
  - Flakiness mitigation strategies and CI integration tips.

- `/websites/developer_apple_swiftdata` (via Context7)
  - In-memory ModelContainer patterns for testing
  - Testing @Relationship cascade rules
  - Async/await patterns with @MainActor
  - FetchDescriptor query testing

- `/ra1028/swiftui-atom-properties` (via Context7)
  - AtomTestContext for isolated state testing
  - Mocking atoms with .override() for dependency injection
  - Testing atom dependency graphs
  - Verifying computed atoms derive correct values

## Usage Pattern

1. When designing a test strategy:
   - Decide which layers to cover (unit/integration/UI),
   - Choose Swift Testing vs XCTest based on project/tooling,
   - Define critical paths, error cases, and edge cases up front.

2. When implementing tests:
   - Keep tests deterministic and fast by default,
   - Use tags/traits for slow/critical suites,
   - Structure UI tests around page objects and accessibility identifiers.

3. When testing data persistence (SwiftData):
   - Always use in-memory ModelContainer in tests
   - Test cascade deletes remove dependent data
   - Verify unique constraints throw on duplicates
   - Test relationship integrity (one-to-many, many-to-one)
   - Use @MainActor for async SwiftData tests

4. When testing state management (Atoms):
   - Use AtomTestContext to isolate atom behavior
   - Override dependency atoms with .override() for mocking
   - Test computed atoms recalculate when dependencies change
   - Verify StateAtom mutations propagate to watchers
   - Test atom cleanup when watchers are removed

5. When acting as a gate (verification/quality):
   - Look for coverage of happy paths + failure/edge states,
   - Call out flakiness risks (sleep-based waits, environment dependence),
   - Recommend incremental improvements, not full rewrites, unless required.
   - Verify SwiftData tests use in-memory containers
   - Verify Atom tests use AtomTestContext, not real app state

This skill ensures iOS agents talk about testing in a consistent way and know
when to consult context7 for deeper patterns and examples.

