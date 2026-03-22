---
name: riverpod-auto-dispose
description: Enable automatic disposal of Riverpod providers when they have no listeners; keepAlive, onDispose, invalidate, ref.keepAlive. Use when preventing memory leaks, caching only while used, or cleaning up resources when a provider is no longer needed. Use this skill when the user asks about auto-dispose, keepAlive, or when to dispose Riverpod state.
---

# Riverpod — Automatic disposal

## Instructions

With **automatic disposal** enabled, Riverpod destroys a provider's state when it has no listeners for one frame. This frees memory and stops work (e.g. network requests) when the provider is no longer used.

### Enabling

- **Code generation:** Enabled by default. Disable with `@Riverpod(keepAlive: true)`.
- **Manual:** Add `isAutoDispose: true` when creating the provider (e.g. `Provider.autoDispose(...)` or `FutureProvider.autoDispose(...)`).

```dart
// Codegen: disable auto-dispose
@Riverpod(keepAlive: true)
String helloWorld(Ref ref) => 'Hello world!';

// Manual: enable
final helloWorldProvider = Provider<String>(
  isAutoDispose: true,
  (ref) => 'Hello world!',
);
```

When a provider has **parameters** (family), enable auto-dispose to avoid caching every parameter combination forever and causing memory leaks.

### When disposal runs

Riverpod counts listeners (from ref.watch, ref.listen, etc.). When the count reaches zero, it waits one frame; if still zero, **ref.onCancel** runs, then the state is destroyed and **ref.onDispose** runs.

### Reacting to disposal: ref.onDispose

Register a callback when the state is destroyed (e.g. close a StreamController):

```dart
final provider = StreamProvider<int>((ref) {
  final controller = StreamController<int>();
  ref.onDispose(controller.close);
  return controller.stream;
});
```

Do not trigger side effects that modify other providers inside onDispose. You can call onDispose multiple times. Other lifecycles: **ref.onCancel** (last listener removed), **ref.onResume** (new listener added after cancel).

### Forcing destruction: ref.invalidate

From a widget or another provider, call **ref.invalidate(provider)** to destroy the current state. If the provider is still listened to, it will recompute; otherwise it stays destroyed until read again.

```dart
onPressed: () => ref.invalidate(someProvider),
```

For family providers you can invalidate one parameter combination or all (see riverpod-family and docs).

### Keeping state alive: ref.keepAlive

When auto-dispose is enabled, you can call **ref.keepAlive()** to prevent disposal until the next recomputation. Use to keep successful results alive while allowing failed or unused state to be disposed. The return value can be called to revert to automatic disposal. If the provider is recomputed, auto-dispose is re-enabled.

### Caching for a duration

Riverpod does not provide a built-in "cache for X seconds". You can implement it with a Timer and ref.keepAlive, or use ref.onCancel/onResume to dispose after a period of no listeners.
