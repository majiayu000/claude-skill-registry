---
name: "flutter-caching-data"
description: "Implements caching strategies for Flutter apps to improve performance and offline support. Use when retaining app data locally to reduce network requests or speed up startup."
metadata:
  model: "models/gemini-3.1-pro-preview"
  last_modified: "Thu, 12 Mar 2026 22:19:54 GMT"

---
# Implementing Flutter Caching and Offline-First Architectures

## Contents
- [Selecting a Caching Strategy](#selecting-a-caching-strategy)
- [Implementing Offline-First Data Synchronization](#implementing-offline-first-data-synchronization)
- [Managing File System and SQLite Persistence](#managing-file-system-and-sqlite-persistence)
- [Optimizing UI, Scroll, and Image Caching](#optimizing-ui-scroll-and-image-caching)
- [Caching the FlutterEngine (Android)](#caching-the-flutterengine-android)
- [Workflows](#workflows)

## Selecting a Caching Strategy

Apply the appropriate caching mechanism based on the data lifecycle and size requirements.

*   **If storing small, non-critical UI states or preferences:** Use `shared_preferences`.
*   **If storing large, structured datasets:** Use on-device databases (SQLite via `sqflite`, Drift, Hive CE, or Isar).
*   **If storing binary data or large media:** Use file system caching via `path_provider`.
*   **If retaining user session state (navigation, scroll positions):** Implement Flutter's built-in state restoration to sync the Element tree with the engine.
*   **If optimizing Android initialization:** Pre-warm and cache the `FlutterEngine`.

## Implementing Offline-First Data Synchronization

Design repositories as the single source of truth, combining local databases and remote API clients. 

### Read Operations (Stream Approach)
Yield local data immediately for fast UI rendering, then fetch remote data, update the local cache, and yield the fresh data.

```dart
Stream<UserProfile> getUserProfile() async* {
  // 1. Yield local cache first
  final localProfile = await _databaseService.fetchUserProfile();
  if (localProfile != null) yield localProfile;

  // 2. Fetch remote, update cache, yield fresh data
  try {
    final remoteProfile = await _apiClientService.getUserProfile();
    await _databaseService.updateUserProfile(remoteProfile);
    yield remoteProfile;
  } catch (e) {
    // Handle network failure; UI already has local data
  }
}
```

### Write Operations
Determine the write strategy based on data criticality:
*   **If strict server synchronization is required (Online-only):** Attempt the API call first. Only update the local database if the API call succeeds.
*   **If offline availability is prioritized (Offline-first):** Write to the local database immediately. Attempt the API call. If the API call fails, flag the local record for background synchronization.

### Background Synchronization
Add a `synchronized` boolean flag to your data models. Run a periodic background task (e.g., via `workmanager` or a `Timer`) to push unsynchronized local changes to the server.

## Managing File System and SQLite Persistence

### File System Caching
Use `path_provider` to locate the correct directory. 
*   Use `getApplicationDocumentsDirectory()` for persistent data.
*   Use `getTemporaryDirectory()` for cache data the OS can clear.

```dart
Future<File> get _localFile async {
  final directory = await getApplicationDocumentsDirectory();
  return File('${directory.path}/cache.txt');
}
```

### SQLite Persistence
Use `sqflite` for relational data caching. Always use `whereArgs` to prevent SQL injection.

```dart
Future<void> updateCachedRecord(Record record) async {
  final db = await database;
  await db.update(
    'records',
    record.toMap(),
    where: 'id = ?',
    whereArgs: [record.id], // NEVER use string interpolation here
  );
}
```

## Optimizing UI, Scroll, and Image Caching

### Image Caching
Image I/O and decompression are expensive. 
*   Use the `cached_network_image` package to handle file-system caching of remote images.
*   **Custom ImageProviders:** If implementing a custom `ImageProvider`, override `createStream()` and `resolveStreamForKey()` instead of the deprecated `resolve()` method.
*   **Cache Sizing:** The `ImageCache.maxByteSize` no longer automatically expands for large images. If loading images larger than the default cache size, manually increase `ImageCache.maxByteSize` or subclass `ImageCache` to implement custom eviction logic.

### Scroll Caching
When configuring caching for scrollable widgets (`ListView`, `GridView`, `Viewport`), use the `scrollCacheExtent` property with a `ScrollCacheExtent` object. Do not use the deprecated `cacheExtent` and `cacheExtentStyle` properties.

```dart
// Correct implementation
ListView(
  scrollCacheExtent: const ScrollCacheExtent.pixels(500.0),
  children: // ...
)

Viewport(
  scrollCacheExtent: const ScrollCacheExtent.viewport(0.5),
  slivers: // ...
)
```

### Widget Caching
*   Avoid overriding `operator ==` on `Widget` objects. It causes O(N²) behavior during rebuilds.
*   **Exception:** You may override `operator ==` *only* on leaf widgets (no children) where comparing properties is significantly faster than rebuilding, and the properties rarely change.
*   Prefer using `const` constructors to allow the framework to short-circuit rebuilds automatically.

## Caching the FlutterEngine (Android)

To eliminate the non-trivial warm-up time of a `FlutterEngine` when adding Flutter to an existing Android app, pre-warm and cache the engine.

1. Instantiate and pre-warm the engine in the `Application` class.
2. Store it in the `FlutterEngineCache`.
3. Retrieve it using `withCachedEngine` in the `FlutterActivity` or `FlutterFragment`.

```kotlin
// 1. Pre-warm in Application class
val flutterEngine = FlutterEngine(this)
flutterEngine.navigationChannel.setInitialRoute("/cached_route")
flutterEngine.dartExecutor.executeDartEntrypoint(DartEntrypoint.createDefault())

// 2. Cache the engine
FlutterEngineCache.getInstance().put("my_engine_id", flutterEngine)

// 3. Use in Activity/Fragment
startActivity(
  FlutterActivity.withCachedEngine("my_engine_id").build(this)
)
```
*Note: You cannot set an initial route via the Activity/Fragment builder when using a cached engine. Set the initial route on the engine's navigation channel before executing the Dart entrypoint.*

## Workflows

### Workflow: Implementing an Offline-First Repository
Follow these steps to implement a robust offline-first data layer.

- [ ] **Task Progress:**
  - [ ] Define the data model with a `synchronized` boolean flag (default `false`).
  - [ ] Implement the local `DatabaseService` (SQLite/Hive) with CRUD operations.
  - [ ] Implement the remote `ApiClientService` for network requests.
  - [ ] Create the `Repository` class combining both services.
  - [ ] Implement the read method returning a `Stream<T>` (yield local, fetch remote, update local, yield remote).
  - [ ] Implement the write method (write local, attempt remote, update `synchronized` flag).
  - [ ] Implement a background sync function to process records where `synchronized == false`.
  - [ ] Run validator -> review errors -> fix (Test offline behavior by disabling network).

### Workflow: Pre-warming the Android FlutterEngine
Follow these steps to cache the FlutterEngine for seamless Android integration.

- [ ] **Task Progress:**
  - [ ] Locate the Android `Application` class (create one if it doesn't exist and register in `AndroidManifest.xml`).
  - [ ] Instantiate a new `FlutterEngine`.
  - [ ] (Optional) Set the initial route via `navigationChannel.setInitialRoute()`.
  - [ ] Execute the Dart entrypoint via `dartExecutor.executeDartEntrypoint()`.
  - [ ] Store the engine in `FlutterEngineCache.getInstance().put()`.
  - [ ] Update the target `FlutterActivity` or `FlutterFragment` to use `.withCachedEngine("id")`.
  - [ ] Run validator -> review errors -> fix (Verify no blank screen appears during transition).
