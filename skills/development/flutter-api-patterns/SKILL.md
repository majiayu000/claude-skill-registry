---
description: "Flutter API patterns: repository pattern, error handling, retry logic, pagination, caching. Use when implementing data layer or handling API errors."
version: "1.0.0"
updated: "2026-01-07"
---

# Flutter API Patterns

## Architecture (3-Layer)

```
Presentation → Domain (Repository) → Data (API)
```

## API Layer

```dart
class EventsApi {
  final SupabaseClient _client;
  EventsApi(this._client);

  Future<List<Map<String, dynamic>>> getOpenEvents() async {
    return await _client
        .from(Event.table_name)
        .select('${Event.c_id}, ${Event.c_title}')
        .eq(Event.c_status, 'open');
  }
}
```

## Repository Layer

```dart
class EventsRepository {
  final EventsApi _api;

  Future<List<Event>> getOpenEvents() async {
    try {
      final data = await _api.getOpenEvents();
      return data.map((j) => Event.fromEntity(EventEntity.fromJson(j))).toList();
    } on PostgrestException catch (e) {
      throw RepositoryError.database(e.message, code: e.code);
    }
  }
}
```

## Error Handling

```dart
@freezed
sealed class RepositoryError with _$RepositoryError implements Exception {
  const factory RepositoryError.database(String message, {String? code}) = DatabaseError;
  const factory RepositoryError.network(String message) = NetworkError;
  const factory RepositoryError.auth(String message) = AuthError;
  const factory RepositoryError.notFound(String message) = NotFoundError;
}
```

## Retry Logic

```dart
Future<T> withRetry<T>({
  required Future<T> Function() operation,
  int maxAttempts = 3,
}) async {
  int attempts = 0;
  Duration delay = const Duration(seconds: 1);
  while (true) {
    try {
      return await operation();
    } catch (e) {
      if (++attempts >= maxAttempts) rethrow;
      await Future.delayed(delay);
      delay *= 2;
    }
  }
}
```

## Pagination

```dart
Future<PaginatedResponse> getEventsPaginated({String? cursor, int limit = 20}) async {
  var query = _client.from(Event.table_name).select().limit(limit + 1);
  if (cursor != null) query = query.lt(Event.c_createdAt, cursor);
  final items = await query;
  final hasMore = items.length > limit;
  if (hasMore) items.removeLast();
  return PaginatedResponse(items: items, hasMore: hasMore);
}
```

## Related Skills
- **flutter-development**: Architecture
- **flutter-query-testing**: Query validation
- **flutter-offline**: Offline support
