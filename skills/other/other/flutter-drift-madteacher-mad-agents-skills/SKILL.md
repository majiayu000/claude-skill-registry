---
name: flutter-drift
description: Complete guide for using drift database library in Flutter applications. Use when building Flutter apps that need local SQLite database storage with type-safe queries, reactive streams, migrations, and efficient CRUD operations. Includes setup with drift_flutter package, StreamBuilder integration, Provider/Riverpod patterns, and Flutter-specific database management for mobile, web, and desktop platforms.
metadata:
  author: Stanislav [MADTeacher] Chernyshev
  version: "1.0"
---

# Flutter Drift

Comprehensive guide for using drift database library in Flutter applications.

## Overview

Flutter Drift skill provides complete guidance for implementing persistent local storage in Flutter apps using the drift library. Drift is a reactive persistence library for Flutter built on SQLite, offering type-safe queries, auto-updating streams, schema migrations, and cross-platform support.

## Quick Start

Add dependencies to `pubspec.yaml`:

```yaml
dependencies:
  drift: ^2.30.0
  drift_flutter: ^0.2.8
  path_provider: ^2.1.5

dev_dependencies:
  drift_dev: ^2.30.0
  build_runner: ^2.10.4
```

Define database:

```dart
@DriftDatabase(tables: [TodoItems])
class AppDatabase extends _$AppDatabase {
  AppDatabase([QueryExecutor? e])
      : super(
          e ??
              driftDatabase(
                name: 'app_db',
                native: const DriftNativeOptions(
                  databaseDirectory: getApplicationSupportDirectory,
                ),
                web: DriftWebOptions(
                  sqlite3Wasm: Uri.parse('sqlite3.wasm'),
                  driftWorker: Uri.parse('drift_worker.js'),
                ),
              ),
        );

  @override
  int get schemaVersion => 1;
}
```

Run code generator:

```bash
dart run build_runner build
```

## Reference Files

See detailed documentation for each topic:

- [setup.md](references/setup.md) - Flutter-specific setup with drift_flutter
- [tables.md](references/tables.md) - Table definitions, columns, constraints
- [queries.md](references/queries.md) - SELECT, WHERE, JOIN, aggregations
- [writes.md](references/writes.md) - INSERT, UPDATE, DELETE, transactions
- [streams.md](references/streams.md) - Reactive stream queries
- [migrations.md](references/migrations.md) - Database schema migrations
- [flutter-ui.md](references/flutter-ui.md) - Flutter UI integration patterns

## Common Patterns

### Reactive Todo List with StreamBuilder

```dart
class TodoList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final database = Provider.of<AppDatabase>(context);

    return StreamBuilder<List<TodoItem>>(
      stream: select(database.todoItems).watch(),
      builder: (context, snapshot) {
        final todos = snapshot.data ?? [];
        return ListView.builder(
          itemCount: todos.length,
          itemBuilder: (context, index) {
            final todo = todos[index];
            return ListTile(
              title: Text(todo.title),
              trailing: Checkbox(
                value: todo.isCompleted,
                onChanged: (value) {
                  database.update(database.todoItems).replace(
                    TodoItem(
                      id: todo.id,
                      title: todo.title,
                      isCompleted: value ?? false,
                    ),
                  );
                },
              ),
            );
          },
        );
      },
    );
  }
}
```

### Add Item with Form

```dart
Future<void> showAddTodoDialog(BuildContext context) async {
  final controller = TextEditingController();
  final database = Provider.of<AppDatabase>(context);

  await showDialog(
    context: context,
    builder: (context) {
      return AlertDialog(
        title: const Text('Add Todo'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(labelText: 'Title'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () async {
              if (controller.text.isNotEmpty) {
                await database.into(database.todoItems).insert(
                  TodoItemsCompanion.insert(title: controller.text),
                );
                if (context.mounted) {
                  Navigator.pop(context);
                }
              }
            },
            child: const Text('Add'),
          ),
        ],
      );
    },
  );

  controller.dispose();
}
```

### Provider Setup

```dart
final databaseProvider = Provider<AppDatabase>((ref) {
  final database = AppDatabase();
  ref.onDispose(database.close);
  return database;
});
```

### Database Migration

```dart
@override
MigrationStrategy get migration {
  return MigrationStrategy(
      onUpgrade: stepByStep(
        from1To2: (m, schema) async {
          await m.addColumn(schema.todoItems, schema.todoItems.dueDate);
        },
      ),
    );
}
```

## Platform-Specific Setup

### Mobile (Android/iOS/macOS/Windows/Linux)

Uses `drift_flutter` with `getApplicationSupportDirectory`.

### Web

Place `sqlite3.wasm` and `drift_worker.js` in `web/` folder.

### Isolate Sharing

```dart
AppDatabase.defaults(): super(
  driftDatabase(
    name: 'app_db',
    native: DriftNativeOptions(
      shareAcrossIsolates: true,
    ),
  ),
);
```

## Testing

Use in-memory database for tests:

```dart
AppDatabase createTestDatabase() {
  return AppDatabase(NativeDatabase.memory());
}
```

## Best Practices

1. **Use drift_flutter** for easy database setup across platforms
2. **StreamBuilder** for reactive UI updates
3. **Provider/Riverpod** for database access management
4. **Close database** on app/widget dispose
5. **Use migrations** when schema changes
6. **Index columns** used in WHERE clauses
7. **Limit stream query size** for performance
8. **Use transactions** for multi-step operations
9. **Debounce user input** for search/filter
10. **Handle loading/error states** in UI

## Troubleshooting

### Build Fails

```bash
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

### Migration Errors

```bash
dart run drift_dev schema validate
dart run drift_dev make-migrations
```

### Stream Not Updating

Ensure operations go through drift APIs, not raw SQLite.
