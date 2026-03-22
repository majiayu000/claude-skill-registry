---
name: riverpod-containers
description: Use ProviderScope in Flutter and ProviderContainer in Dart for Riverpod; where provider state is stored, overrides, observers, testing with ProviderContainer.test. Use when setting up Riverpod in Flutter or pure Dart, understanding where state lives, or writing tests with a fresh container. Use this skill when the user asks about ProviderScope, ProviderContainer, or where Riverpod stores state.
---

# Riverpod — Containers / Scopes

## Instructions

Providers themselves hold **no state**. State is stored in a **ProviderContainer**. In Flutter you use the **ProviderScope** widget, which creates and exposes a container to the widget tree.

### Flutter: ProviderScope

Wrap your app at the root so widgets can read providers:

```dart
void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

After that, use Consumer / ConsumerWidget / ConsumerStatefulWidget to get a `ref` and call `ref.watch` / `ref.read`. You can also pass `overrides` or `observers` to ProviderScope.

### Pure Dart: ProviderContainer

In command-line or server-side Dart, create a container, use it, then dispose it:

```dart
void main() {
  final container = ProviderContainer();
  try {
    final sub = container.listen(counterProvider, (previous, next) {
      print('Counter changed from $previous to $next');
    });
    print('Counter starts at ${sub.read()}');
  } finally {
    container.dispose();
  }
}
```

### Why state lives in a container

- **Separation of concerns** — Only the provider (and ref) can change its state; the UI typically calls notifier methods.
- **Testing** — Each test can create a new container (e.g. `ProviderContainer.test()`) for a fresh state; no shared global state.
- **Configuration** — Overrides and observers are set on the container/scope. See riverpod-overrides and riverpod-observers.
- **Scoping** — The same provider can resolve to different state in different parts of the tree (advanced). See riverpod-scoping.

### Testing

Do not use `ProviderContainer()` directly in tests. Use **ProviderContainer.test()** so the container is disposed when the test ends:

```dart
test('Counter starts at 0 and can be incremented', () {
  final container = ProviderContainer.test();
  expect(container.read(counterProvider), 0);
  container.read(counterProvider.notifier).increment();
  expect(container.read(counterProvider), 1);
});
```

In widget tests, wrap the widget in `ProviderScope` and use `tester.container()` to get the container if needed (see riverpod-testing).
