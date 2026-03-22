---
name: riverpod-scoping
description: Scope Riverpod providers to a subtree using overrides and dependencies; page-specific behavior, ListView optimization, avoiding passing family parameters. Use when changing provider behavior for one page or widget, or when optimizing rebuilds. Use this skill when the user asks about scoping providers or provider scope.
---

# Riverpod — Scoping providers

## Instructions

**Scoping** means changing a provider's behavior for only part of the app by overriding it in a **non-root** ProviderScope. Use cases: page-specific customization (e.g. theme for one page), performance (e.g. rebuild only the item that changed in a ListView), or avoiding passing family parameters through the tree.

**Note:** Scoping is complex and may be reworked in future Riverpod versions. Use with care.

### Opt-in: dependencies

By default you cannot scope a provider. Opt in by setting **dependencies** on the provider. The first scoped provider usually has `dependencies: const []`.

```dart
final currentItemIdProvider = Provider<String?>(
  dependencies: const [],
  (ref) => null,
);
```

### Listening to a scoped provider

Use ref.watch/ref.read as usual. If another **provider** listens to a scoped provider, that listening provider must list the scoped provider in its **dependencies**:

```dart
final currentItemProvider = FutureProvider<Item?>(
  dependencies: [currentItemIdProvider],
  (ref) async {
    final currentItemId = ref.watch(currentItemIdProvider);
    if (currentItemId == null) return null;
    return fetchItem(id: currentItemId);
  },
);
```

Only scoped providers need to be listed in dependencies; non-scoped providers do not.

### Setting the scoped value: overrides

Use **overrides** on a ProviderScope that wraps the subtree where the scoped value should apply:

```dart
ProviderScope(
  overrides: [
    currentItemIdProvider.overrideWithValue('123'),
  ],
  child: const DetailPageView(),
)
```

That way the detail page sees `'123'` as the current item ID without it being passed down manually. See riverpod-overrides for override syntax.
