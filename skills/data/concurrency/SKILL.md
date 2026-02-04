---
name: Android Concurrency
description: Standards for Coroutines, Flow, and Threading
metadata:
  labels: [android, concurrency, coroutines, flow]
  triggers:
    files: ['**/*.kt']
    keywords: ['suspend', 'viewModelScope', 'lifecycleScope', 'Flow']
---

# Android Concurrency Standards

## **Priority: P0**

## Implementation Guidelines

### Structured Concurrency

- **Scopes**: Always use `viewModelScope` (VM) or `lifecycleScope` (Activity/Fragment).
- **Dispatchers**: INJECT Dispatchers (`DispatcherProvider`) for testability. Do not hardcode `Dispatchers.IO`.

### Flow usage

- **Cold Streams**: Use `Flow` for data streams.
- **Hot Streams**: Use `StateFlow` (State) or `SharedFlow` (Events).
- **Collection**: Use `collectAsStateWithLifecycle()` (Compose) or `repeatOnLifecycle` (Views).

## Anti-Patterns

- **GlobalScope**: `**No GlobalScope**: Use structured scopes.`
- **Async/Await**: `**Avoid Async**: Prefer simple suspend functions unless parallel execution is needed.`

## References

- [Dispatcher Pattern](references/implementation.md)
