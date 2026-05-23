---
name: ios-std
description: Coding standards for iOS apps (SwiftUI, MVVM, offline-first, push notifications).
---

## Purpose

Ensure consistent, testable, app store-ready iOS code. Complements stack, security, and NFR skills.

## Project structure

```
Features/<FeatureName>/
  View.swift
  ViewModel.swift
  (feature-specific helpers)
UIComponents/              # Shared UI primitives
Services/
  Persistence/             # SwiftData/CoreData boundary
  Notifications/           # Push notification handling
  Logging/                 # os.Logger wrapper
  Config/                  # Environment/config
Infrastructure/            # Routing, composition root, cross-cutting utilities
```

## Key conventions

### SwiftUI

- Views are small and composable; extract subviews when files grow
- State ownership: `@StateObject` for owned, `@ObservedObject` for injected
- No side effects in `body`; use `task`, `onAppear`, or explicit actions

### MVVM

- View models: `@MainActor`, expose state via `@Published`, intents as methods (`load()`, `didTapSave()`)
- Services injected via initializers
- View models never touch SwiftData/CoreData directly—use persistence boundary

### Persistence (offline-first)

- Single boundary: `PersistenceStore` protocol with `SwiftDataStore` implementation
- Schema changes require migration note
- User-generated content needs retention/cleanup strategy

### Notifications

- Isolated handling: permission flow, token registration, payload routing
- Treat all payload values as untrusted input

### Concurrency

- Mark view models `@MainActor` when they own UI state
- Handle cancellation explicitly in long-running operations

### Logging

- Use `os.Logger`
- Log events, not payloads; never log PII or tokens

### Naming

- Types/files: `PascalCase`
- Functions/vars: `camelCase`
- One primary type per file
- Feature folders: `PascalCase`

## Testing requirements

**Framework:** Swift Testing (`import Testing`, `@Test`, `#expect`). Do not use XCTest for unit tests.

TDD is mandatory — see `/shared-tdd` for the red-green-refactor workflow and evidence requirements.

**Test command:** `xcodebuild test` or run via Xcode.

### What to test

- Unit tests: view model logic, persistence store (in-memory double), notification routing
- UI tests: primary happy path, notification-to-screen flow when relevant
- Use `@Test(arguments:)` for parameterized tests instead of loops

### Test file conventions

| Source | Test |
|--------|------|
| `Features/Foo/FooViewModel.swift` | `Tests/Features/Foo/FooViewModelTests.swift` |
| `Services/Bar/BarService.swift` | `Tests/Services/Bar/BarServiceTests.swift` |

Test pattern: `@Test func methodName_condition_expected()` (no `test_` prefix)

## Output

For significant code changes, briefly note:

- Any deviation from these standards and why

## Reference

For detailed patterns and examples, see `reference/ios-std-reference.md`
