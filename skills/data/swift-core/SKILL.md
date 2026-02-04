---
name: swift-core
description: Swift 6 fundamentals for all Apple platforms. Use when implementing concurrency, architecture, testing, i18n, or performance optimization across iOS, macOS, iPadOS, watchOS, visionOS.
versions:
  swift: 6.2
  ios: 26
user-invocable: false
references: references/concurrency.md, references/architecture.md, references/testing.md, references/i18n.md, references/performance.md
related-skills: swiftui-core, solid-swift, ios, macos, ipados, watchos, visionos
---

# Swift Core

Swift 6 fundamentals shared across all Apple platforms.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing Swift patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Swift 6 docs via Context7/Exa
3. **mcp__apple-docs__search_apple_docs** - Check Swift concurrency patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Implementing async/await, actors, Sendable
- Designing app architecture (MVVM, Clean Architecture)
- Writing async tests with XCTest
- Localizing with String Catalogs
- Profiling with Instruments

### Why Swift Core

| Feature | Benefit |
|---------|---------|
| Actors | Thread-safe shared state without locks |
| @Observable | Simple reactive state (replaces ObservableObject) |
| String Catalogs | Automatic localization with Xcode 15+ |
| Instruments | Built-in performance profiling |

---

## Key Concepts

### Concurrency (Swift 6)
Modern async/await with strict concurrency checking. Actors provide thread-safe state, Sendable marks safe types.

### Architecture
MVVM with @Observable is the recommended pattern. Clean Architecture for complex apps with domain separation.

### Testing
XCTest with native async/await support. No need for expectations with async tests.

### Internationalization
String Catalogs are mandatory. All user-facing text must be localized.

### Performance
Profile with Instruments. Use lazy loading, avoid heavy work in view body.

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Async/await, actors, Sendable | [concurrency.md](references/concurrency.md) |
| MVVM, Clean Architecture, DI | [architecture.md](references/architecture.md) |
| XCTest, async tests, mocking | [testing.md](references/testing.md) |
| String Catalogs, localization | [i18n.md](references/i18n.md) |
| Instruments, optimization | [performance.md](references/performance.md) |

---

## Best Practices

1. **Actors for shared state** - Prefer actors over classes with locks
2. **@Observable over ObservableObject** - Simpler, better performance
3. **Structured concurrency** - async/await, no completion handlers
4. **String Catalogs** - ALL user-facing text must be localized
5. **Profile in Release** - Always profile with `-O` optimization
6. **Value types** - Prefer structs over classes
