---
name: riverpod-retry
description: Customize Riverpod automatic retry on provider failure; retry function, per-provider and global retry, disabling retry, ProviderException, awaiting retries. Use when a provider can fail transiently and should retry, or when you need to disable or customize retry logic. Use this skill when the user asks about retry, failed providers, or exponential backoff in Riverpod.
---

# Riverpod — Automatic retry

## Instructions

Riverpod **retries** providers when their computation throws. Retry can be customized per provider or globally.

### Default behavior

By default a provider is retried up to a limit (e.g. 10 times) with exponential backoff (e.g. 200ms to 6.4s). **Error** and **ProviderException** are not retried: Error indicates a bug; ProviderException means a dependency failed, so the dependent provider is not retried (the underlying one is).

### Custom retry function

A retry function has signature `Duration? Function(int retryCount, Object error)`. Return a **Duration** for the delay before the next retry, or **null** to stop.

```dart
Duration? myRetry(int retryCount, Object error) {
  if (retryCount >= 5) return null;
  if (error is ProviderException) return null;
  return Duration(milliseconds: 200 * (1 << retryCount));
}
```

### Where to set it

- **Per provider:** Pass `retry: myRetry` when defining the provider (or `@Riverpod(retry: myRetry)` with codegen).
- **Globally:** Pass `retry: myRetry` to **ProviderScope** or **ProviderContainer**.

```dart
// Global
ProviderScope(retry: myRetry, child: MyApp())

// Per provider (manual)
final myProvider = Provider<int>(retry: myRetry, (ref) => 0);
```

### Disabling retry

Return **null** always:

```dart
ProviderScope(retry: (retryCount, error) => null, child: MyApp())
```

### Awaiting async providers with retry

`ref.watch(myProvider.future)` (or equivalent) keeps waiting until either all retries are exhausted or the provider succeeds. So `await ref.watch(myProvider.future)` skips intermediate failures and completes when the provider finally succeeds or gives up.
