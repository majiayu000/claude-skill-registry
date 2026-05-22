---
name: riverpod-migration
description: Migrate Riverpod from StateNotifier to Notifier/AsyncNotifier, from ChangeNotifier to AsyncNotifier, or upgrade from 0.13/0.14/1.0; ref.onDispose, family, lifecycle, riverpod migrate CLI. Use when the user asks about migrating from StateNotifier, from ChangeNotifier, upgrading Riverpod 0.13 to 0.14, 0.14 to 1.0, or Riverpod migration guides.
---

# Riverpod — Migration guides

## Instructions

This skill points to detailed migration guides for different scenarios. Use the reference file that matches your case.

### When to use which guide

| Scenario | Reference |
|----------|-----------|
| **From StateNotifier** to Notifier / AsyncNotifier | [migration_from_state_notifier.md](reference/migration_from_state_notifier.md) |
| **From ChangeNotifier** to AsyncNotifier | [migration_from_change_notifier.md](reference/migration_from_change_notifier.md) |
| **Upgrade 0.13.x → 0.14.x** (StateNotifierProvider syntax, watch(provider) vs provider.state) | [migration_0_13_0_14.md](reference/migration_0_13_0_14.md) |
| **Upgrade 0.14.x → 1.0** (ScopedReader → WidgetRef, useProvider → ref.watch, StateProvider) | [migration_0_14_1_0.md](reference/migration_0_14_1_0.md) |

For **Riverpod 2.0 → 3.0** see the **riverpod-3-0-migration** skill.

### Common themes

- **StateNotifier → Notifier/AsyncNotifier:** Put init logic in `build`; use `ref.onDispose` instead of overloading `dispose`; no `mounted`—use cancellation (e.g. Completer or HTTP cancel token). Consumers stay the same (ref.watch, methods on notifier).
- **ChangeNotifier → AsyncNotifier:** Replace `isLoading`/`hasError`/manual try-catch with `AsyncValue`; single `state`; mutations by reassigning `state`.
- **CLI:** For 0.14 and 1.0 upgrades you can run `dart pub global activate riverpod_cli` then `riverpod migrate` in the project (do not upgrade Riverpod manually first; the tool will suggest version and changes).

Open the relevant reference file for step-by-step instructions and code examples.
