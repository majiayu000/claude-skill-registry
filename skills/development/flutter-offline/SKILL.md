---
description: "Flutter offline support: local storage, caching, sync strategies, conflict resolution. Use when implementing offline-first features or data synchronization."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter Offline Support

## Storage Options

| Storage | Use Case |
|---------|----------|
| SharedPreferences | Key-value settings |
| Hive | Structured data, large datasets |
| SQLite | Complex queries, relations |

## SharedPreferences

```dart
class SettingsRepository {
  late final SharedPreferences _prefs;
  Future<void> init() async => _prefs = await SharedPreferences.getInstance();
  bool get isDarkMode => _prefs.getBool('darkMode') ?? false;
  Future<void> setDarkMode(bool v) => _prefs.setBool('darkMode', v);
}
```

## Hive

```dart
@HiveType(typeId: 0)
class Event {
  @HiveField(0) final String id;
  @HiveField(1) final String title;
  @HiveField(2) final bool isSynced;
}

class EventsLocalRepo {
  Box<Event> get _box => Hive.box<Event>('events');
  List<Event> getAll() => _box.values.toList();
  Future<void> save(Event e) => _box.put(e.id, e);
}
```

## Offline-First Pattern

```dart
Future<List<Event>> getEvents() async {
  final cached = _local.getAll();
  if (cached.isNotEmpty) {
    _refreshFromApi();  // Background refresh
    return cached;
  }
  if (await _connectivity.isConnected) {
    return _fetchAndCache();
  }
  return [];
}
```

## Network Detection

```dart
class ConnectivityService {
  Stream<bool> get onConnectivityChanged =>
    Connectivity().onConnectivityChanged.map(
      (r) => r.any((c) => c != ConnectivityResult.none));
}
```

## Sync Queue

```dart
class SyncQueue {
  Future<void> enqueue(SyncOperation op) async {
    await _queue.put(op.id, op);
    _trySync();
  }

  Future<void> _trySync() async {
    if (!await _connectivity.isConnected) return;
    for (final op in _queue.values.where((o) => o.status == SyncStatus.pending)) {
      try {
        await _execute(op);
        await _queue.delete(op.id);
      } catch (e) {
        await _queue.put(op.id, op.copyWith(status: SyncStatus.failed));
      }
    }
  }
}
```

## Optimistic Updates

```dart
Future<void> updateEvent(String id, String title) async {
  final current = state.valueOrNull ?? [];
  // 1. Optimistic update
  state = AsyncData(current.map((e) => e.id == id ? e.copyWith(title: title) : e).toList());
  try {
    await _repo.update(id, title: title);
  } catch (e) {
    state = AsyncData(current);  // Revert
    rethrow;
  }
}
```

## Related Skills
- **flutter-api-patterns**: API layer
- **flutter-development**: Architecture
