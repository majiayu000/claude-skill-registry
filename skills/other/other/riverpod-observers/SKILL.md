---
name: riverpod-observers
description: Use ProviderObserver to log or debug Riverpod provider lifecycle; didUpdateProvider, ProviderScope observers, naming providers. Use when adding logging, analytics, or debugging for provider state changes. Use this skill when the user asks about ProviderObserver, logging Riverpod, or debugging provider updates.
---

# Riverpod — ProviderObservers

## Instructions

A **ProviderObserver** receives lifecycle events for providers (e.g. when a provider's value changes). Use it for logging, analytics, or debugging.

### Implementing an observer

Extend **ProviderObserver** and override the methods you need (e.g. **didUpdateProvider**). Pass instances to **ProviderScope** or **ProviderContainer** via the `observers` parameter.

### Example: logger

```dart
final class Logger extends ProviderObserver {
  @override
  void didUpdateProvider(
    ProviderObserverContext context,
    Object? previousValue,
    Object? newValue,
  ) {
    print('{"provider": "${context.provider}", "newValue": "$newValue"}');
  }
}

void main() {
  runApp(
    ProviderScope(
      observers: [Logger()],
      child: const MyApp(),
    ),
  );
}
```

### Naming providers

For clearer logs, give providers a **name**:

```dart
final myProvider = Provider<int>((ref) => 0, name: 'MyProvider');
```

With code generation, a name is usually assigned automatically.

### Note on mutations

If state is mutated in place (e.g. a List with ref.notifyListeners), `previousValue` and `newValue` in didUpdateProvider may be the same reference. For distinct values, clone before mutating.
