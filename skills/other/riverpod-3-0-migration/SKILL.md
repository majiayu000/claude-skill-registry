---
name: riverpod-3-0-migration
description: Migrate Riverpod from 2.0 to 3.0; automatic retry, paused listeners, legacy providers import, Ref simplification, FamilyNotifier removal, ProviderException, updateShouldNotify. Use when the user asks about Riverpod 3 migration, upgrading to Riverpod 3, or breaking changes in 3.0.
---

# Riverpod — Migrating from 2.0 to 3.0

For a full list of changes and highlights, see the official Riverpod docs (What's new in Riverpod 3.0). This skill summarizes the main migration steps.

## Automatic retry

Failing providers are **retried by default** in 3.0. To disable globally:

```dart
ProviderScope(retry: (retryCount, error) => null, child: MyApp())
// or ProviderContainer(retry: (retryCount, error) => null)
```

To disable per provider, pass **retry: (retryCount, error) => null** when defining the provider (or `@Riverpod(retry: ...)` with codegen). See riverpod-retry.

## Out-of-view providers are paused

Listeners in widgets that are not visible (e.g. off-screen) are **paused** by default. There is no global switch. To keep a subtree from pausing, wrap it in **TickerMode(enabled: true, child: ...)** so the Consumer(s) inside do not follow the pause behavior.

## Legacy providers (StateProvider, StateNotifierProvider, ChangeNotifierProvider)

These are **moved to a legacy import**. They are not removed but discouraged. To keep using them:

```dart
import 'package:flutter_riverpod/legacy.dart';
// or hooks_riverpod/legacy.dart, riverpod/legacy.dart
```

## Updates use ==

All providers now use **==** to filter updates (no longer **identical**). **StreamProvider** / **StreamNotifier** values are compared with ==. To customize, override **updateShouldNotify(previous, next)** on the Notifier (e.g. return true to always notify).

## ProviderObserver API change

Observer methods now receive a single **ProviderObserverContext** (with container, provider, and optional mutation) instead of separate (provider, value, container) parameters. Update signatures, e.g.:

- **didAddProvider(ProviderObserverContext context, Object? value)** (and similar for other callbacks).

## Ref simplified; Ref subclasses removed

- **Ref** no longer has a type parameter. Use **Ref** everywhere (e.g. replace **MyProviderRef** with **Ref** in codegen).
- **ProviderRef.state**, **Ref.listenSelf**, **FutureProviderRef.future** are **moved onto Notifier/AsyncNotifier**: use **Notifier.state**, **Notifier.listenSelf**, **AsyncNotifier.future** instead of on ref. If you need these, use a class-based Notifier/AsyncNotifier and call them on the notifier.

## AutoDispose type names removed

AutoDispose is still supported, but the separate type names (e.g. **AutoDisposeProvider**, **AutoDisposeNotifier**) are unified. Use **Provider**, **Notifier**, etc. with the same behavior. Migration: case-sensitive replace **AutoDispose** with a space (empty string) in type names.

## Family Notifier types removed

**FamilyNotifier**, **FamilyAsyncNotifier**, **FamilyStreamNotifier** are removed. Use **Notifier** / **AsyncNotifier** / **StreamNotifier** and pass the parameter via the **constructor** (and store it in a field). Remove the parameter from **build**; **build()** takes no family argument. Example:

- Before: `FamilyNotifier<int, String>` with `int build(String arg)`.
- After: `Notifier<int>` with constructor `MyNotifier(this.arg)` and `final String arg;`, and **int build()** using **arg**.

## ProviderException

When a provider throws, the exception is wrapped in **ProviderException**. If you catch the original type (e.g. **on NotFoundException**), change to **on ProviderException catch (e)** and check **e.exception is NotFoundException**. If you only use **AsyncValue** and **value.hasError** / **value.error**, no change needed.

## Summary

- Retry: disable via **retry** on scope/container or provider.
- Pause: use **TickerMode(enabled: true)** where you don’t want pausing.
- Legacy: use **flutter_riverpod/legacy.dart** (or equivalent) for StateProvider / StateNotifierProvider / ChangeNotifierProvider.
- Ref: use plain **Ref**; move **state** / **listenSelf** / **future** to Notifier/AsyncNotifier.
- AutoDispose: remove “AutoDispose” from type names.
- Family notifiers: use Notifier/AsyncNotifier with constructor argument; **build()** has no parameter.
- Errors: catch **ProviderException** and inspect **exception** when you need the original type.

For version highlights and more detail, see the official Riverpod documentation.
