---
name: dart-drift
description: Complete guide for using drift database library in Dart applications (CLI, server-side, non-Flutter). Use when building Dart apps that need local SQLite database storage or PostgreSQL connection with type-safe queries, reactive streams, migrations, and efficient CRUD operations. Includes setup with sqlite3 package, PostgreSQL support with drift_postgres, connection pooling, and server-side patterns.
---

# Dart Drift

Comprehensive guide for using drift database library in Dart applications.

## Overview

Dart Drift skill provides complete guidance for implementing persistent storage in Dart applications (CLI tools, backend services, non-Flutter desktop apps) using the drift library. Drift is a reactive persistence library for Dart built on SQLite, with optional PostgreSQL support, offering type-safe queries, auto-updating streams, schema migrations, and cross-platform database connections.

## Quick Start

### SQLite Setup

Add dependencies to `pubspec.yaml`:

```yaml
dependencies:
  drift: ^2.30.0
  sqlite3: ^3.1.3

dev_dependencies:
  drift_dev: ^2.30.0
  build_runner: ^2.10.4
```

Define database:

```dart
@DriftDatabase(tables: [TodoItems])
class AppDatabase extends _$AppDatabase {
  AppDatabase(QueryExecutor e) : super(e);

  @override
  int get schemaVersion => 1;
}
```

Open database:

```dart
AppDatabase openConnection() {
  final file = File('db.sqlite');
  return AppDatabase(LazyDatabase(() async {
    final db = sqlite3.open(file.path);
    return NativeDatabase.createInBackground(db);
  }));
}
```

Run code generator:

```bash
dart run build_runner build
```

### PostgreSQL Setup

Add PostgreSQL dependencies:

```yaml
dependencies:
  drift: ^2.30.0
  postgres: ^3.5.9
  drift_postgres: ^1.3.1

dev_dependencies:
  drift_dev: ^2.30.0
  build_runner: ^2.10.4
```

Configure for PostgreSQL in `build.yaml`:

```yaml
targets:
  $default:
    builders:
      drift_dev:
        options:
          sql:
            dialects:
              - postgres
```

Open PostgreSQL connection:

```dart
import 'package:drift_postgres/drift_postgres.dart';

AppDatabase openPostgresConnection() {
  final endpoint = HostEndpoint(
      host: 'localhost',
      port: 5432,
      database: 'mydb',
      username: 'user',
      password: 'password',
    );

  return AppDatabase(
    PgDatabase(
      endpoint: endpoint,
    ),
  );
}
```

## Reference Files

See detailed documentation for each topic:

- [setup.md](references/setup.md) - Dart setup with sqlite3 or PostgreSQL
- [postgres.md](references/postgres.md) - PostgreSQL-specific features, connection pooling
- [tables.md](references/tables.md) - Table definitions, columns, constraints
- [queries.md](references/queries.md) - SELECT, WHERE, JOIN, aggregations
- [writes.md](references/writes.md) - INSERT, UPDATE, DELETE, transactions
- [streams.md](references/streams.md) - Reactive stream queries
- [migrations.md](references/migrations.md) - Database schema migrations

## Common Patterns

### CLI Application with SQLite

```dart
void main(List<String> args) async {
  final db = openConnection();

  final todos = await db.select(db.todoItems).get();
  print('Found ${todos.length} todos');

  await db.close();
}
```

### Backend Service with PostgreSQL

```dart
class TodoService {
  final AppDatabase db;

  TodoService(this.db);

  Future<List<TodoItem>> getAllTodos() async {
    return await db.select(db.todoItems).get();
  }

  Future<int> createTodo(String title) async {
    return await db.into(db.todoItems).insert(
      TodoItemsCompanion.insert(title: title),
    );
  }
}

void main() async {
  final pool = PgPool(
      PgEndpoint(
        host: 'localhost',
        port: 5432,
        database: 'mydb',
        username: 'user',
        password: 'password',
      ),
      settings: PoolSettings(maxSize: 10),
    );

  final db = AppDatabase(PgDatabase.opened(pool));
  final service = TodoService(db);

  final todoId = await service.createTodo('New task');
  print('Created todo with id: $todoId');

  final todos = await service.getAllTodos();
  print('Total todos: ${todos.length}');
}
```

### Connection Pooling

```dart
import 'package:postgres/postgres_pool.dart';

Future<AppDatabase> openPooledConnection() {
  final pool = PgPool(
      PgEndpoint(
        host: 'localhost',
        port: 5432,
        database: 'mydb',
        username: 'user',
        password: 'password',
      ),
      settings: PoolSettings(maxSize: 20),
    );

  return AppDatabase(PgDatabase.opened(pool));
}
```

### PostgreSQL-Specific Types

```dart
class Users extends Table {
  late final id = postgresUuid().autoGenerate()();
  late final name = text()();
  late final settings = postgresJson()();
  late final createdAt = dateTime().withDefault(
    FunctionCallExpression.currentTimestamp(),
  );
}
```

### In-Memory Testing

```dart
AppDatabase createTestDatabase() {
  return AppDatabase(NativeDatabase.memory());
}
```

### Transaction with Data Consistency

```dart
Future<void> transferTodo(int fromId, int toId) async {
  await db.transaction(() async {
    final fromTodo = await (db.select(db.todoItems)
      ..where((t) => t.id.equals(fromId))
      ).getSingle();

    await db.update(db.todoItems).write(
      TodoItemsCompanion(
        id: Value(toId),
        title: Value(fromTodo.title),
      ),
    );

    await db.delete(db.todoItems).go(fromId);
  });
}
```

## Platform-Specific Setup

### CLI/Desktop (macOS/Windows/Linux)

Uses `sqlite3` package with file-based storage.

### Server/Backend (PostgreSQL)

Uses `postgres` package with connection pooling.

### Testing

Uses in-memory database for fast unit tests.

## Testing

### Unit Tests

```dart
void main() {
  test('Insert and retrieve todo', () async {
    final db = createTestDatabase();
    final id = await db.into(db.todoItems).insert(
      TodoItemsCompanion.insert(title: 'Test todo'),
    );

    final todos = await db.select(db.todoItems).get();
    expect(todos.length, 1);
    expect(todos.first.title, 'Test todo');

    await db.close();
  });
}
```

### Integration Tests

```dart
void main() {
  test('PostgreSQL connection works', () async {
    final pool = PgPool(endpoint, settings: PoolSettings(maxSize: 5));
    final db = AppDatabase(PgDatabase.opened(pool));

    final id = await db.into(db.todoItems).insert(
      TodoItemsCompanion.insert(title: 'Test'),
    );

    expect(id, greaterThan(0));

    await db.close();
  });
}
```

## Best Practices

1. **Connection pooling** for PostgreSQL in production
2. **In-memory databases** for fast unit tests
3. **Transactions** for data consistency
4. **Connection timeouts** for robust server apps
5. **Schema migrations** with proper versioning
6. **Indexes** on frequently queried columns
7. **Prepared statements** (automatic in drift)
8. **Close connections** properly on shutdown
9. **Pool management** for backend services
10. **Error handling** for connection failures

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

### Connection Pool Exhausted

Increase pool size or reduce connection lifetime:

```dart
PoolSettings(
    maxSize: 20,
    maxLifetime: Duration(minutes: 5),
  )
```

### PostgreSQL Type Errors

Verify dialect is configured in `build.yaml`.
