---
name: riverpod-refs
description: Use Ref and WidgetRef to read, watch, listen, invalidate, and refresh providers; onDispose and onCancel lifecycle; ref.read vs ref.watch vs ref.listen, ref.invalidate and ref.refresh. Use when interacting with Riverpod providers from widgets or other providers, when to use watch vs read, or when resetting provider state. Use this skill whenever the user asks about ref.watch, ref.read, ref.listen, ref.invalidate, or Riverpod lifecycle.
---

# Riverpod — Refs

## Instructions

**Ref** (and **WidgetRef** in widgets) is how you interact with providers: read state, listen to changes, reset state, and register lifecycle callbacks. Providers get a `Ref` as the first parameter of their function or as `this.ref` in a Notifier. Widgets get a **WidgetRef** via Consumer / ConsumerWidget / ConsumerState.

### Obtaining a Ref

- **Inside a provider:** First parameter of the provider function, or `ref` property in a Notifier.
- **Inside a widget:** Use a Consumer (builder gives `ref`), ConsumerWidget (`build(context, ref)`), or ConsumerStatefulWidget (state has `ref`). Pass `ref` to other functions if needed.

### Listening to state

- **ref.watch(provider)** — Declarative. Your widget/provider rebuilds when the provider changes. Use this by default in build methods.
- **ref.listen(provider, (prev, next) { ... })** — Imperative. Run side effects when the provider changes (e.g. show a dialog, navigate). Safe to use in build; for initState use `ref.listenManual` and manage the subscription.

```dart
// In a widget
final tick = ref.watch(tickProvider);
return Text('Tick: $tick');

// Side effect when provider changes
ref.listen(tickProvider, (previous, next) {
  print('Tick changed from $previous to $next');
});
```

### Reading without listening

- **ref.read(provider)** — Get current value without subscribing. Use in event handlers (e.g. onPressed), not to "optimize" by avoiding watch. For selective rebuilds use `ref.watch(provider.select((value) => ...))`.

```dart
onPressed: () {
  final tick = ref.read(tickProvider);
  print('Current tick: $tick');
}
```

### Resetting state

- **ref.invalidate(provider)** — Discard current state; provider will recompute on next read. If the provider is listened to, a new state is created.
- **ref.refresh(provider)** — Same as invalidate + read: invalidates and returns the new value. Use when you need the new value immediately.

```dart
ref.invalidate(tickProvider);
// or
final newTick = ref.refresh(tickProvider);
```

### Lifecycle: onDispose, onCancel

Inside a provider you can register callbacks:

- **ref.onDispose(callback)** — Called when the provider state is destroyed (e.g. auto-dispose or recomputation). Use to close StreamControllers, cancel timers, etc. Do not trigger side effects that modify other providers inside onDispose.
- **ref.onCancel(callback)** — Called when the last listener is removed (before dispose). **ref.onResume(callback)** — Called when a listener is added again after onCancel.

```dart
final provider = StreamProvider<int>((ref) {
  final controller = StreamController<int>();
  ref.onDispose(controller.close);
  return controller.stream;
});
```

You can call onDispose multiple times (e.g. one per disposable resource). Return value of onDispose/onCancel can be called to unregister. For more detail and select/listenManual, see [reference.md](reference.md).
