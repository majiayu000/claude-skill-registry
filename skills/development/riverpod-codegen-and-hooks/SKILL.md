---
name: riverpod-codegen-and-hooks
description: Use Riverpod code generation (@riverpod, riverpod_generator) and hooks (hooks_riverpod, HookConsumerWidget, flutter_hooks with Riverpod). Use when the user asks about @riverpod, code generation, riverpod_generator, when to use codegen, or using flutter_hooks with Riverpod (HookConsumerWidget, HookConsumer).
---

# Riverpod — Code generation and hooks

## Code generation

Code generation is **optional** in Riverpod. It changes the syntax for defining providers: you write an annotated function or class and the generator produces the provider. Use it if you already use code generation (e.g. Freezed, json_serializable); otherwise the extra build step may not be worth it. See riverpod-getting-started for setup (build_runner, riverpod_generator).

### Benefits

- Clearer syntax: no manual provider type (Provider vs FutureProvider etc.); Riverpod infers it.
- Parameters: any parameters (named, optional, defaults) instead of a single family parameter.
- Stateful hot-reload for Riverpod code.
- Better debugging via generated metadata.

### Syntax

**Functional provider** (sync):

```dart
@riverpod
String example(Ref ref) {
  return 'foo';
}
```

**Class-based provider** (sync, with methods for side effects):

```dart
@riverpod
class Example extends _$Example {
  @override
  String build() => 'foo';
  // Add methods to mutate state
}
```

**Async:** Use `Future`/`FutureOr`/`Stream`; async functions get AsyncValue and loading/error handling automatically. **Auto-dispose:** On by default with codegen. Disable with `@Riverpod(keepAlive: true)`.

```dart
@riverpod
String example1(Ref ref) => 'foo';

@Riverpod(keepAlive: true)
String example2(Ref ref) => 'foo';
```

**Parameters:** Add parameters to the function (consistent == required):

```dart
@riverpod
Future<User> fetchUser(Ref ref, {required int userId}) async {
  final json = await http.get('api/user/$userId');
  return User.fromJson(json);
}
```

Manual equivalent would be `FutureProvider.autoDispose.family<User, int>(...)`. See riverpod-providers and riverpod-family for concepts.

---

## Hooks

**Hooks** come from [flutter_hooks] (separate from Riverpod). They are for **local** widget state (e.g. TextEditingController, AnimationController) and can replace StatefulWidget or builder nesting. Use them only if you want hooks; they are not required for Riverpod. Newcomers should avoid hooks at first.

### Using hooks and Riverpod together

You need both **flutter_hooks** and **hooks_riverpod**. Then either:

**Option 1: HookConsumerWidget** — One base class that supports both hooks and ref:

```dart
class Example extends HookConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final counter = useState(0);
    final value = ref.watch(myProvider);
    return Text('Hello $counter $value');
  }
}
```

**Option 2: HookConsumer** — Builder that combines HookBuilder + Consumer (works with flutter_riverpod only if you nest them; hooks_riverpod provides HookConsumer):

```dart
return HookConsumer(
  builder: (context, ref, child) {
    final counter = useState(0);
    final value = ref.watch(myProvider);
    return Text('Hello $counter $value');
  },
);
```

**Option 3:** Nest `Consumer` and `HookBuilder` (no hooks_riverpod needed).

### Rules of hooks

- Use hooks only in the **build** method of a widget that extends **HookWidget** (or HookConsumerWidget).
- Do not use hooks conditionally or in loops; call order must be stable.

See riverpod-consumers for Ref in widgets and the official docs for full codegen/hooks details.
