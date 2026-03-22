---
name: riverpod-offline
description: Persist Riverpod notifier state offline with Storage and persist(); riverpod_sqflite, JsonPersist, key, destroyKey, cache duration, testing with in-memory storage. Use when saving state across app restarts or offline. Use this skill when the user asks about offline persistence, persisting state, or Riverpod storage.
---

# Riverpod — Offline persistence (experimental)

## Instructions

**Offline persistence** stores provider state on device so it survives restarts and works offline. Riverpod is storage-agnostic; packages like **riverpod_sqflite** provide a **Storage** implementation. Only **Notifier**-based providers can be persisted. The feature is experimental.

### Creating a Storage

Install a package (e.g. riverpod_sqflite + sqflite) and create a Storage. With SQFlite:

```dart
final storageProvider = FutureProvider<Storage<String, String>>((ref) async {
  return JsonSqFliteStorage.open(
    join(await getDatabasesPath(), 'riverpod.db'),
  );
});
```

### Persisting a notifier

Inside the notifier's `build`, call **persist** with: the Storage (e.g. `ref.watch(storageProvider.future)`), a unique **key**, and **encode**/ **decode** for your state. Do not await persist; Riverpod handles it.

```dart
class TodoList extends AsyncNotifier<List<Todo>> {
  @override
  Future<List<Todo>> build() async {
    persist(
      ref.watch(storageProvider.future),
      key: 'todo_list',
      encode: (todos) => todos.map((todo) => {'task': todo.task}).toList(),
      decode: (json) => (json as List).map((todo) => Todo(task: todo['task'] as String)).toList(),
    );
    return fetchTodosFromServer();
  }
}
```

### Keys

- **Unique** across all persisted providers (same key = same row, risk of corruption).
- **Stable** across restarts (changing the key loses restored state).
- For **family** providers, include the parameter in the key.

### JsonPersist (code generation)

With riverpod_sqflite and codegen, use **@JsonPersist()** so key/encode/decode are generated:

```dart
@riverpod
@JsonPersist()
class TodoList extends _$TodoList {
  @override
  Future<List<Todo>> build() async {
    persist(ref.watch(storageProvider.future));
    return fetchTodosFromServer();
  }
}
```

### Cache duration

By default state is cached for a short time (e.g. 2 days). For long-lived data (e.g. user preferences), set **StorageOptions**:

```dart
persist(
  ref.watch(storageProvider.future),
  options: const StorageOptions(cacheTime: StorageCacheTime.unsafe_forever),
  // ...
);
```

If using forever, plan to delete or migrate data when the app changes; Riverpod does not do migrations.

### Destroy key (simple migration)

When the data shape changes, use **destroyKey** so old data is discarded:

```dart
options: const StorageOptions(destroyKey: '1.0'),
```

Bump the string in new releases; old persisted state is then ignored and the provider starts fresh.

### Waiting for decode

To initialize from persisted state instead of a network call, await the persist future:

```dart
await persist(ref.watch(storageProvider.future), key: 'todo_list', ...).future;
return state.value ?? <Todo>[];
```

### Testing

Override the storage provider with **Storage.inMemory()** so tests don't need a real database:

```dart
ProviderScope(
  overrides: [
    storageProvider.overrideWith((ref) => Storage<String, String>.inMemory()),
  ],
  child: const MyApp(),
)
```

For advanced migrations or custom storage strategies, you may still need to work with the database directly.
