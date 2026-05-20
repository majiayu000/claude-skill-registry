---
name: "flutter-working-with-databases"
description: "Manages local data persistence using SQLite or other database solutions. Use when a Flutter app needs to store, query, or synchronize large amounts of structured data on the device."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:19:15 GMT"

---
# Architecting the Data Layer

## Contents
- [Core Architecture](#core-architecture)
- [Services Implementation](#services-implementation)
- [Repository Implementation](#repository-implementation)
- [Caching Strategies](#caching-strategies)
- [Workflows](#workflows)
- [Examples](#examples)

## Core Architecture

Construct the data layer as the Single Source of Truth (SSOT) for all application data. In an MVVM architecture, the data layer represents the Model. Never update application data outside of this layer. 

Separate the data layer into two distinct components: **Repositories** and **Services**.

### Repositories
*   Act as the SSOT for a specific domain entity.
*   Contain business logic for data mutation, polling, caching, and offline synchronization.
*   Transform raw data models (API/DB models) into Domain Models (clean data classes containing only what the UI needs).
*   Inject Services as private members to prevent the UI layer from bypassing the repository.

### Services
*   Act as stateless wrappers around external data sources (HTTP clients, SQLite databases, platform plugins).
*   Perform no business logic or data transformation beyond basic JSON serialization.
*   Return raw data models or `Result` wrappers to the calling repository.

## Services Implementation

### Database Services (SQLite)
Use databases to persist and query large amounts of structured data locally. 
*   Add `sqflite` and `path` packages to `pubspec.yaml`.
*   Use the `path` package to define the storage location on disk safely across platforms.
*   Define table schemas using constants to prevent typos.
*   Use `id` as the primary key with `AUTOINCREMENT` to improve query and update times.
*   Always use `whereArgs` in SQL queries to prevent SQL injection (e.g., `where: 'id = ?', whereArgs: [id]`).

### API Services
*   Wrap HTTP calls (e.g., using the `http` package) in dedicated client classes.
*   Return asynchronous response objects (`Future` or `Stream`).
*   Handle raw JSON serialization at this level, returning API-specific data models.

## Repository Implementation

### Domain Models
*   Define immutable data classes (using `freezed` or `built_value`) for Domain Models.
*   Strip out backend-specific fields (like metadata or pagination tokens) that the UI does not need.

### Offline-First Synchronization
Combine local and remote data sources within the repository to provide seamless offline support.

*   **If reading data:** Return a `Stream` that immediately yields the cached local data from the Database Service, performs the network request via the API Service, updates the Database Service, and then yields the fresh data.
*   **If writing data (Online-only):** Attempt the API Service mutation first. If successful, update the Database Service.
*   **If writing data (Offline-first):** Update the Database Service immediately. Attempt the API Service mutation. If the network fails, flag the local database record as `synchronized: false` and queue a background synchronization task.

## Caching Strategies

Select the appropriate caching strategy based on the data payload:
*   **Small Key-Value Data:** Use `shared_preferences` for simple app configurations, theme settings, or user preferences.
*   **Large Datasets:** Use relational (`sqflite`, `drift`) or non-relational (`hive_ce`, `isar_community`) on-device databases.
*   **Images:** Use the `cached_network_image` package to automatically cache remote images to the device's file system.
*   **API Responses:** Implement lightweight remote caching within the API Service or Repository using in-memory maps or temporary file storage.

## Workflows

### Workflow: Implementing a New Data Feature
Copy and track this checklist when adding a new data entity to the application.

- [ ] **Task Progress**
  - [ ] Define the Domain Model (immutable, UI-focused).
  - [ ] Define the API/DB Models (raw data structures).
  - [ ] Create or update the Service(s) to handle raw data fetching/storage.
  - [ ] Create the Repository interface (abstract class).
  - [ ] Implement the Repository, injecting the required Service(s) as private dependencies.
  - [ ] Map raw Service models to the Domain Model within the Repository.
  - [ ] Expose Repository methods to the View Model.
  - [ ] Run validator -> review errors -> fix.

### Workflow: Implementing SQLite Persistence
Follow this sequence to add a new SQLite table and integrate it.

- [ ] **Task Progress**
  - [ ] Add `sqflite` and `path` dependencies.
  - [ ] Define table name and column constants.
  - [ ] Update the `onCreate` or `onUpgrade` method in the Database Service to execute the `CREATE TABLE` statement.
  - [ ] Implement `insert`, `query`, `update`, and `delete` methods in the Database Service.
  - [ ] Inject the Database Service into the target Repository.
  - [ ] Ensure the Repository calls `database.open()` before executing queries.

## Examples

### Offline-First Repository Implementation
This example demonstrates a Repository coordinating between a Database Service and an API Service using a Stream for offline-first reads.

```dart
import 'dart:async';

class TodoRepository {
  TodoRepository({
    required DatabaseService databaseService,
    required ApiClientService apiClientService,
  })  : _databaseService = databaseService,
        _apiClientService = apiClientService;

  final DatabaseService _databaseService;
  final ApiClientService _apiClientService;

  /// Yields local data immediately, then fetches remote data, updates local, and yields fresh data.
  Stream<List<Todo>> observeTodos() async* {
    // 1. Yield local cached data first
    final localTodos = await _databaseService.getAllTodos();
    if (localTodos.isNotEmpty) {
      yield localTodos.map((model) => Todo.fromDbModel(model)).toList();
    }

    try {
      // 2. Fetch fresh data from API
      final remoteTodos = await _apiClientService.fetchTodos();
      
      // 3. Update local database
      await _databaseService.replaceAllTodos(remoteTodos);
      
      // 4. Yield fresh data
      yield remoteTodos.map((model) => Todo.fromApiModel(model)).toList();
    } on Exception catch (e) {
      // Handle network errors (UI will still have local data)
      // Log error or yield a specific error state if required
    }
  }

  /// Offline-first write: Save locally, then attempt remote sync.
  Future<void> createTodo(Todo todo) async {
    final dbModel = todo.toDbModel().copyWith(isSynced: false);
    
    // 1. Save locally immediately
    await _databaseService.insertTodo(dbModel);

    try {
      // 2. Attempt remote sync
      final apiModel = await _apiClientService.postTodo(todo.toApiModel());
      
      // 3. Mark as synced locally
      await _databaseService.updateTodo(
        dbModel.copyWith(id: apiModel.id, isSynced: true)
      );
    } on Exception catch (_) {
      // Leave as isSynced: false for background sync task to pick up later
    }
  }
}
```

### SQLite Database Service Implementation
Demonstrates safe query construction using `whereArgs`.

```dart
class DatabaseService {
  static const String _tableName = 'todos';
  static const String _colId = 'id';
  static const String _colTask = 'task';
  static const String _colIsSynced = 'is_synced';

  Database? _database;

  Future<void> open() async {
    if (_database != null) return;
    
    final dbPath = join(await getDatabasesPath(), 'app_database.db');
    _database = await openDatabase(
      dbPath,
      version: 1,
      onCreate: (db, version) {
        return db.execute(
          'CREATE TABLE $_tableName('
          '$_colId INTEGER PRIMARY KEY AUTOINCREMENT, '
          '$_colTask TEXT, '
          '$_colIsSynced INTEGER)'
        );
      },
    );
  }

  Future<void> updateTodo(TodoDbModel todo) async {
    await _database!.update(
      _tableName,
      todo.toMap(),
      where: '$_colId = ?',
      whereArgs: [todo.id], // Prevents SQL injection
    );
  }
}
```
