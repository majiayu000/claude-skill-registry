---
name: riverpod-providers
description: Declare and use Riverpod providers (Provider, FutureProvider, StreamProvider, NotifierProvider, AsyncNotifierProvider, StreamNotifierProvider); unmodifiable vs modifiable, top-level declaration, Ref, Notifier build method. Use when creating providers, choosing provider type, writing Notifier classes, or understanding Riverpod state. Use this skill whenever the user asks about Riverpod providers, provider types, or notifiers.
---

# Riverpod — Providers

## Instructions

Providers are the central feature of Riverpod: memoized functions that cache their result and let multiple widgets (or other providers) access the same value. They are declared as **top-level** `final` variables. State lives in a **ProviderContainer** (or ProviderScope in Flutter), not in the provider itself.

### Provider variants

|              | Synchronous   | Future                 | Stream                  |
|--------------|---------------|------------------------|-------------------------|
| Unmodifiable | Provider      | FutureProvider         | StreamProvider          |
| Modifiable   | NotifierProvider | AsyncNotifierProvider | StreamNotifierProvider  |

- **Sync vs Future vs Stream**: Match the return type of your function (`int`, `Future<T>`, `Stream<T>`).
- **Unmodifiable**: Widgets only read the value. Use for computed or fetched data.
- **Modifiable**: Expose a Notifier with a `build()` method and custom methods; widgets call `ref.read(provider.notifier).someMethod()`. Use when the UI must update state.

Pick the type based on what you want to return; the provider type follows naturally. FutureProvider / AsyncNotifierProvider are the most common.

### Creating a provider (unmodifiable / functional)

**Manual:**

```dart
final userProvider = FutureProvider<User>((ref) async {
  final response = await http.get('https://api.example.com/user/123');
  return User.fromJson(response.body);
});
```

**Code generation:** Annotate a top-level function with `@riverpod`. First parameter must be `Ref ref`. The generated provider name is `functionNameProvider`.

```dart
@riverpod
Future<User> user(Ref ref) async {
  final response = await http.get('https://api.example.com/user/123');
  return User.fromJson(response.body);
}
```

Modifiers: `.autoDispose` (or `@Riverpod(keepAlive: true)` to disable) and `.family` for parameters. See riverpod-auto-dispose and riverpod-family.

### Creating a provider (modifiable / Notifier)

**Manual:** Use a NotifierProvider (or AsyncNotifierProvider / StreamNotifierProvider) with a Notifier class that extends `Notifier<T>`, `AsyncNotifier<T>`, or `StreamNotifier<T>`. Override `build()`; do not put logic in the constructor (ref/state are not available yet). Public methods are called via `ref.read(provider.notifier).method()`.

```dart
final counterProvider = NotifierProvider<CounterNotifier, int>(CounterNotifier.new);

class CounterNotifier extends Notifier<int> {
  @override
  int build() => 0;

  void increment() => state++;
}
```

**Code generation:** Annotate a class that extends `_$ClassName`. Override `build()`; add custom methods. Same rule: no logic in the constructor.

```dart
@riverpod
class CounterNotifier extends _$CounterNotifier {
  @override
  int build() => 0;

  void increment() => state++;
}
```

### Using providers

1. **Flutter:** Wrap the app in `ProviderScope`. Use Consumer, ConsumerWidget, or ConsumerStatefulWidget to get a `ref` and call `ref.watch(provider)` or `ref.read(provider)`.
2. **Dart only:** Create a `ProviderContainer()`, then `container.read(provider)` or `container.listen(...)`. Call `container.dispose()` when done.
3. **Inside another provider:** Use the `Ref` passed to the provider function (or `this.ref` in a Notifier) to `ref.watch` / `ref.read` other providers.

Example in a widget:

```dart
return Consumer(
  builder: (context, ref, _) {
    final helloWorld = ref.watch(helloWorldProvider);
    return Text(helloWorld);
  },
);
```

You can declare multiple providers that return the same type; they are independent. For more detail on Ref, containers, modifiers, and notifier rules, see [reference.md](reference.md).
