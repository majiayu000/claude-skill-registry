---
name: Swift Concurrency
description: Standards for async/await, Actors, Task Groups, and MainActor
metadata:
  labels: [swift, concurrency, async, await, actor]
  triggers:
    files: ['**/*.swift']
    keywords: ['async', 'await', 'actor', 'Task', 'MainActor']
---

# Swift Concurrency

## **Priority: P0**

## Implementation Guidelines

### async/await

- **Async Functions**: Mark with `async`, call with `await`.
- **Error Handling**: Combine with `throws` for async throwing functions.
- **No Completion Handlers**: Prefer `async` over callback-based APIs.

### Actors

- **Data Isolation**: Use `actor` for mutable state accessed from multiple tasks.
- **MainActor**: Annotate UI code with `@MainActor` for main thread execution.
- **Actor Isolation**: All actor properties/methods are isolated automatically.

### Task Management

- **Structured Concurrency**: Use `Task {}`, `async let`, `TaskGroup`.
- **Cancellation**: Check `Task.isCancelled`, propagate cancellation.
- **Detached Tasks**: Avoid `Task.detached` unless necessary.

## Anti-Patterns

- **Blocking Main Thread**: `**No synchronous work in @MainActor**: Use Task.`
- **Missing MainActor**: `**UI updates must be @MainActor**: Compiler error.`
- **Ignoring Cancellation**: `**Check Task.isCancelled**: Respect cancellation.`

## References

- [async/await & Actors](references/implementation.md)
