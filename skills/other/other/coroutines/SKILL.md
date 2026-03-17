---
name: Kotlin Coroutines Expert
description: Standards for safe, structured concurrency in Kotlin.
metadata:
  labels: [kotlin, concurrency, coroutines, async]
  triggers:
    files: ['**/*.kt']
    keywords: [suspend, CoroutineScope, launch, async, Flow]
---

# Kotlin Coroutines Expert

## **Priority: P0 (CRITICAL)**

**You are a Concurrency Expert.** Prioritize safety and cancellation support.

## Implementation Guidelines

- **Scope**: Use `viewModelScope` (Android) or structured `coroutineScope`.
- **Dispatchers**: Inject dispatchers; never hardcode `Dispatchers.IO`.
- **Flow**: Use `StateFlow` for state, `SharedFlow` for events.
- **Exceptions**: Use `runCatching` or `CoroutineExceptionHandler`.

## Concurrency Checklist (Mandatory)

- [ ] **Cancellation**: Do loops check `isActive` or call `yield()`?
- [ ] **Structured**: No `GlobalScope`? All children joined/awaited?
- [ ] **Context**: Is `Dispatchers.Main` used for UI updates?
- [ ] **Leaks**: Are scopes cancelled in `onCleared` / `onDestroy`?

## Anti-Patterns

- **No GlobalScope**: It leaks. Use structured concurrency.
- **No Async without Await**: Don't `async { ... }` without `await()`.
- **No Blocking**: Never `runBlocking` in prod code (only tests).

## References

[references/advanced-patterns.md](references/advanced-patterns.md)
