---
name: Kotlin Coroutines & Flow
description: Structured Concurrency, Flow patterns, and Asynchronous programming standards.
metadata:
  labels: [kotlin, coroutines, flow, async, concurrency]
  triggers:
    files: ['**/*.kt']
    keywords: [suspend, launch, async, flow, StateFlow, SharedFlow, Dispatchers]
---

# Kotlin Coroutines & Flow

## **Priority: P1 (HIGH)**

Standard for safe, structured asynchronous programming.

## Implementation Guidelines

- **Structured Concurrency**: Always launch coroutines within a `CoroutineScope` (e.g., `viewModelScope`, `lifecycleScope`). Never use `GlobalScope`.
- **Dispatchers**: Inject `DispatcherProvider` or `CoroutineDispatcher` to simplify testing. Do not hardcode `Dispatchers.IO` in classes.
- **Suspend Functions**: Mark blocking/long-running operations as `suspend`. They should be "main-safe" (handle their own context switching).
- **Flow**: Prefer `StateFlow` (state holder) and `SharedFlow` (events) over `LiveData`.
- **Collection**: Use `collectLatest` for restartable upstream updates. Use `flowWithLifecycle` in UI.
- **Error Handling**: Use `CoroutineExceptionHandler` for top-level launch, `try/catch` for code blocks within coroutines.

## Anti-Patterns

- **GlobalScope**: Leaks memory and breaks structure.
- **Blocking Calls**: Never use `Thread.sleep` or blocking I/O in coroutines. Use `delay` or proper suspend functions.
- **Async/Await Abuse**: Don't use `async` unless you need parallel execution. Use linear code in `launch`.
- **Mutable State in Flow**: Don't expose `MutableStateFlow` publicly. Cast to `StateFlow`.

## Code

For detailed `ViewModel` + `StateFlow` and `Parallel Async` examples:
[references/advanced-patterns.md](references/advanced-patterns.md)

```kotlin
// Structured Scope + Main-safe Suspend
viewModelScope.launch {
    val data = withContext(Dispatchers.IO) { repo.fetch() }
    _state.value = UiState.Success(data)
}
```

## Related Topics

best-practices | language | android
