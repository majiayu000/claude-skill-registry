---
name: riverpod-from-provider
description: Migrate from package:provider to Riverpod; ChangeNotifierProvider, ProxyProvider to ref.watch, context.watch to ref.watch, ConsumerWidget, incremental migration, family and autoDispose. Use when the user is migrating from Provider to Riverpod, or asks about Provider vs Riverpod, or how to replace ProxyProvider/ChangeNotifierProvider.
---

# Riverpod — Migrating from Provider

## Motivation

Riverpod was created as a successor to Provider, addressing InheritedWidget limitations:

- **Same type:** Provider can't have two `Provider<Item>` in the tree (only the nearest is found). Riverpod has no such limit; providers are identified by variable, not type.
- **Combining providers:** ProxyProvider is tedious and error-prone. In Riverpod, use **ref.watch** inside a provider to depend on others; composition is straightforward.
- **AsyncValue:** Riverpod can expose previous data while loading (e.g. show old list + loading indicator). Provider doesn't offer this cleanly.
- **Safety:** Provider can throw `ProviderNotFoundException` at runtime. Riverpod avoids this by design.
- **Disposal:** Provider can't react when consumers stop listening; scoping is tricky. Riverpod offers **autoDispose** and **ref.keepAlive** for clear lifecycle and caching.
- **Parameters:** Riverpod's **.family** gives type-safe, parameterized providers with per-parameter state; with autoDispose, state is disposed when unused. Equivalent in Provider is impractical.
- **Testing:** With Provider you must re-define providers per test. With Riverpod, override with **overrides** to mock.
- **Side effects:** Riverpod offers **ref.listen** for reacting to changes (e.g. navigation, snackbars). Provider has no built-in equivalent.

The main API change: use **ConsumerWidget** (and **WidgetRef**) instead of StatelessWidget, and **ref.watch** / **ref.read** instead of **context.watch** / **context.read**.

---

## Quickstart

- Read the Riverpod getting started guide (riverpod-getting-started) and try a small example.
- Migrate **incrementally**. You can run Provider and Riverpod side by side (use import aliases if needed).

### Start with ChangeNotifierProvider

Keep existing **ChangeNotifier** classes and wrap them in Riverpod's **ChangeNotifierProvider**:

```dart
final myNotifierProvider = ChangeNotifierProvider<MyNotifier>((ref) => MyNotifier());
```

Use **ProviderScope** at the root. Replace **context.watch** with **ref.watch** where this provider is used (e.g. in a ConsumerWidget). No need to convert every ChangeNotifier to a Notifier immediately.

### Start with leaves

Migrate providers that have no dependencies first (the "leaves"), then those that depend on them. Avoid migrating ProxyProviders until their dependencies are migrated.

### One provider at a time

Migrate and test one provider at a time. Full migration of a ChangeNotifier means: (1) convert to **Notifier** + **NotifierProvider**, (2) replace every **context.watch** for it with **ref.watch**.

### ProxyProvider → ref.watch

In Riverpod, combining providers is done with **ref.watch** inside another provider:

```dart
final labelProvider = Provider<String>((ref) {
  final userIdNotifier = ref.watch(userIdNotifierProvider);
  return 'The user ID is ${userIdNotifier.userId}';
});
```

For stateful combined objects (like ChangeNotifierProxyProvider), use **ref.listen** in the provider to react to another provider and update your notifier.

### Eager initialization

Riverpod providers are lazy. To warm data at startup, watch the provider at the root (e.g. in a Consumer under ProviderScope that returns your app as child). See riverpod-eager-initialization.

### Code generation

Code gen doesn't generate ChangeNotifierProvider. You can use a small extension (listenAndDisposeChangeNotifier) to expose ChangeNotifier with @riverpod during migration; once you switch to Notifier, remove the extension. See the official quickstart for the snippet.

---

## Provider vs Riverpod

### Defining providers

- **Provider:** Providers are widgets (e.g. inside MultiProvider).  
- **Riverpod:** Providers are top-level **final** variables. No widget tree for definitions. Add **ProviderScope** at the root of the app.

### Reading

- **Provider:** `context.watch<T>()`, `context.read<T>()`, `context.select<T,R>(...)`.  
- **Riverpod:** Use **ConsumerWidget** (or Consumer) to get **WidgetRef ref**; then **ref.watch(provider)**, **ref.read(provider)**, **ref.watch(provider.select(...))**.
- Use **watch** in build, **read** in event handlers. Same mental model as Provider.

### Consumer

Riverpod has **Consumer** with `(context, ref, child)`. No need for Consumer2, Consumer3, etc.: just multiple **ref.watch** calls in one builder.

### Scoping vs family + autoDispose

Provider uses scoping to destroy state or have per-page state. In Riverpod:

- **autoDispose** destroys state when there are no listeners (ref.onCancel / ref.onDispose).
- **.family** gives parameterized providers (one state per parameter). Use with autoDispose to avoid unbounded cache.

So: use **.family** for "state per X" and **.autoDispose** for "destroy when unused" instead of scoping.

See riverpod-getting-started, riverpod-providers, riverpod-family, and riverpod-auto-dispose for details.
