---
name: raven-dev
description: Raven development workflow for building, serving, testing, and debugging Swift WASM apps and Raven runtime changes.
---

# Raven Development Skill

Use this skill when working on Raven examples, runtime rendering behavior, DOMBridge event handling, or WASM dev loops.

## When To Use

- Build/test a Raven example app
- Reproduce browser-side rendering issues
- Debug DOM event handler wiring
- Validate a framework fix end-to-end in an example

## Core Workflow

1. Build phase (prefer app directory)

```bash
cd Examples/TodoApp
swift build --swift-sdk swift-6.2.3-RELEASE_wasm
```

2. Serve phase (from the WASM UI package root, prefer Raven CLI dev server)

```bash
cd Examples/TodoApp
raven dev
```

3. Validate in browser

- Open `http://localhost:8000/`
- Check console for runtime errors
- Verify UI renders expected state

4. Iterate quickly

- Use `python3 raven-dev.py` in `Examples/TodoApp` for automatic rebuild/reload loops.

## High-Value Debug Checks

- Browser cache mismatch:
  - compare current WASM checksum against served file
  - use versioned filenames/query params when needed
- DOM event handlers:
  - avoid dynamic JS property access for handler registries
  - prefer `JSClosure` storage in Swift dictionaries keyed by stable IDs
- Build scope:
  - build from example app directory to avoid unrelated target/tooling failures

## Safe DOMBridge Pattern

```swift
private var eventClosures: [UUID: JSClosure] = [:]

public func addEventListener(
    element: JSObject,
    event: String,
    handlerID: UUID,
    handler: @escaping @Sendable @MainActor () -> Void
) {
    let jsClosure = JSClosure { _ in
        Task { @MainActor in handler() }
        return .undefined
    }

    eventClosures[handlerID] = jsClosure
    _ = element.addEventListener!(event, jsClosure)
}
```

## Definition of Done

- Repro steps documented
- Relevant tests/builds pass
- Browser console is clean for changed path
- Output behavior verified in example app
