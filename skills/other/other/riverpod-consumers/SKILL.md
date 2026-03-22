---
name: riverpod-consumers
description: Use Riverpod Consumer, ConsumerWidget, and ConsumerStatefulWidget to read and watch providers in widgets; WidgetRef, builder ref parameter. Use when building widgets that need to access Riverpod providers, ref.watch or ref.read in the UI, or converting StatelessWidget to ConsumerWidget. Prefer this skill when the user asks how to use providers in Flutter widgets or why ConsumerWidget is required.
---

# Riverpod — Consumers

## Instructions

Consumers are widgets that give you a **Ref** (here, **WidgetRef**) so you can read and listen to providers. Without a Consumer, widgets cannot access the provider tree.

### Consumer (builder)

Use `Consumer` when you want to keep extending `StatelessWidget` or `StatefulWidget`. The builder callback receives `(context, ref, child)`.

```dart
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer(
      builder: (context, ref, _) {
        final value = ref.watch(myProvider);
        return Text(value.toString());
      },
    );
  }
}
```

### ConsumerWidget

Subclass `ConsumerWidget` instead of `StatelessWidget`. The `build` method receives `(BuildContext context, WidgetRef ref)`.

```dart
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final value = ref.watch(myProvider);
    return Text(value.toString());
  }
}
```

### ConsumerStatefulWidget + ConsumerState

When you need a `State` (e.g. for lifecycle or local state), use `ConsumerStatefulWidget` and `ConsumerState`. The state object has a `ref` property.

```dart
class MyWidget extends ConsumerStatefulWidget {
  @override
  ConsumerState<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends ConsumerState<MyWidget> {
  @override
  Widget build(BuildContext context) {
    final value = ref.watch(myProvider);
    return Text(value.toString());
  }
}
```

### Which to use

- **Consumer** — Use for everything if you prefer not to change your widget base class; slightly more verbose.
- **ConsumerWidget** — Recommended when you don't need State; one less nesting level.
- **ConsumerStatefulWidget** — Use when you need State (e.g. TabController, animations).

### Why not StatelessWidget + context.watch?

Riverpod does not use `BuildContext` to watch providers because that would break **auto-dispose** and other features that rely on knowing when a widget stops listening. Ref-based consumers allow reliable disposal and correct behavior. The hooks_riverpod package also offers HookConsumerWidget etc. for use with flutter_hooks. Enable riverpod_lint for IDE refactors (e.g. "Convert to ConsumerWidget").
