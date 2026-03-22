---
name: riverpod-eager-initialization
description: Eagerly initialize Riverpod providers at app startup by watching them in a root Consumer; handle loading/error in the initializer, AsyncValue.requireValue. Use when a provider must be ready before the rest of the app is used. Use this skill when the user asks about eager initialization or preloading providers.
---

# Riverpod — Eager initialization

## Instructions

Providers are **lazy** by default: they initialize on first use. There is no built-in "eager" flag (for tree-shaking). To force early initialization, **watch** the provider at the root of your app so it stays alive and runs immediately.

### Approach

Place a **Consumer** (or ConsumerWidget) directly under **ProviderScope** that only watches the providers you want to initialize and returns your real app as **child**:

```dart
void main() {
  runApp(ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const _EagerInitialization(child: MaterialApp());
  }
}

class _EagerInitialization extends ConsumerWidget {
  const _EagerInitialization({required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.watch(myProvider);  // Eagerly initialize
    return child;
  }
}
```

Only the initializer widget rebuilds when the provider changes; **child** is unchanged so Flutter does not rebuild the rest of the tree unless something else is listening.

### Async: loading and error

If the provider is async, handle loading/error in the initializer (e.g. show CircularProgressIndicator or error until ready, then return child). Other widgets can use **AsyncValue.requireValue** to read the data without pattern matching; if they run before the value is ready, it throws with a clear message.

Put the initializer in a shared widget (e.g. MyApp) so tests can reuse the same setup by using that widget.
