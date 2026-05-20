---
name: riverpod-mutations
description: Use Riverpod mutations for UI-driven async operations like form submit; Mutation.run, MutationIdle/Pending/Success/Error, Mutation.reset, keyed mutations. Use when showing loading/error/success for a single action (e.g. submit button) without polluting provider state. Use this skill when the user asks about mutations, loading state for actions, or form submission with Riverpod.
---

# Riverpod — Mutations (experimental)

## Instructions

**Mutations** represent a single async operation the UI can react to (e.g. "add todo" in progress, succeeded, or failed). They keep loading/error/success out of your main provider state. The API is experimental and may change.

### Defining a mutation

Create a `Mutation<T>` instance (T is the result type, optional):

```dart
final addTodo = Mutation<Todo>();
```

Typically store it as a global or `static final` on a Notifier.

### Listening

Use ref.watch in a Consumer (or inside a provider) to drive the UI:

```dart
final addTodoState = ref.watch(addTodo);

// In build:
backgroundColor: switch (addTodoState) {
  MutationError() => const WidgetStatePropertyAll(Colors.red),
  _ => null,
},
if (addTodoState is MutationPending) ...[
  const SizedBox(width: 8),
  const CircularProgressIndicator(),
],
```

### States

- **MutationIdle** — Not started or reset.
- **MutationPending** — In progress.
- **MutationSuccess** — Succeeded; result available.
- **MutationError** — Failed; error available.

Use a `switch` on the state to handle each case.

### Triggering

Call **Mutation.run(ref, callback)**. The callback receives a transaction object (e.g. `tsx`) to access providers and must return a value of type T:

```dart
addTodo.run(ref, (tsx) async {
  final todoNotifier = tsx.get(todoNotifierProvider.notifier);
  final createdTodo = await todoNotifier.addTodo('Eat a cookie');
  return createdTodo;
});
```

Use `tsx.get(provider)` to keep providers alive for the duration of the mutation.

### Keyed mutations

Pass a key to have multiple instances (e.g. one mutation per list item):

```dart
ref.watch(deleteItemMutation(itemId));
deleteItemMutation(itemId).run(ref, (tsx) async { ... });
```

### Resetting

Mutations reset to Idle when they complete or when all listeners are removed. To reset manually:

```dart
addTodo.reset(ref);
```

See the official Riverpod docs for the latest mutation API and generics.
