---
name: asyncredux-persistence
description: Implement local state persistence using Persistor. Covers creating a custom Persistor class, implementing `readState()`, `persistDifference()`, `deleteState()`, using LocalPersist helper, throttling saves, and pausing/resuming persistence with app lifecycle.
---

## Overview

AsyncRedux provides state persistence by passing a `persistor` object to the Store. This maintains app state on disk, enabling restoration between sessions.

## Store Initialization with Persistor

At startup, read any existing state from disk, create default state if none exists, then initialize the store:

```dart
var persistor = MyPersistor();

var initialState = await persistor.readState();

if (initialState == null) {
  initialState = AppState.initialState();
  await persistor.saveInitialState(initialState);
}

var store = Store<AppState>(
  initialState: initialState,
  persistor: persistor,
);
```

## The Persistor Abstract Class

The `Persistor<St>` base class defines these methods:

```dart
abstract class Persistor<St> {
  /// Read persisted state, or return null if none exists
  Future<St?> readState();

  /// Delete state from disk
  Future<void> deleteState();

  /// Save state changes. Provides both newState and lastPersistedState
  /// so you can compare them and save only the difference.
  Future<void> persistDifference({
    required St? lastPersistedState,
    required St newState
  });

  /// Convenience method for initial saves
  Future<void> saveInitialState(St state) =>
    persistDifference(lastPersistedState: null, newState: state);

  /// Controls save frequency. Return null to disable throttling.
  Duration get throttle => const Duration(seconds: 2);
}
```

## Creating a Custom Persistor

Extend the abstract class and implement the required methods:

```dart
class MyPersistor extends Persistor<AppState> {

  @override
  Future<AppState?> readState() async {
    // Read state from disk (e.g., from SharedPreferences, file, etc.)
    return null;
  }

  @override
  Future<void> deleteState() async {
    // Delete state from disk
  }

  @override
  Future<void> persistDifference({
    required AppState? lastPersistedState,
    required AppState newState,
  }) async {
    // Save state to disk.
    // You can compare lastPersistedState with newState to save only changes.
  }

  @override
  Duration get throttle => const Duration(seconds: 2);
}
```

## Throttling

The `throttle` getter controls how often state is saved. All changes within the throttle window are collected and saved in a single call. The default is 2 seconds.

```dart
// Save at most every 5 seconds
@override
Duration get throttle => const Duration(seconds: 5);

// Disable throttling (save immediately on every change)
@override
Duration? get throttle => null;
```

## Forcing Immediate Save

Dispatch `PersistAction()` to save immediately, bypassing the throttle:

```dart
store.dispatch(PersistAction());
```

## Pausing and Resuming Persistence

Control persistence with these store methods:

```dart
store.pausePersistor();           // Pause saving
store.persistAndPausePersistor(); // Save current state, then pause
store.resumePersistor();          // Resume saving
```

## App Lifecycle Integration

Pause persistence when the app goes to background and resume when it becomes active. Create an `AppLifecycleManager` widget:

```dart
class AppLifecycleManager extends StatefulWidget {
  final Widget child;

  const AppLifecycleManager({
    Key? key,
    required this.child,
  }) : super(key: key);

  @override
  _AppLifecycleManagerState createState() => _AppLifecycleManagerState();
}

class _AppLifecycleManagerState extends State<AppLifecycleManager>
    with WidgetsBindingObserver {

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState lifecycle) {
    store.dispatch(ProcessLifecycleChange_Action(lifecycle));
  }

  @override
  Widget build(BuildContext context) => widget.child;
}
```

Create an action to handle lifecycle changes:

```dart
class ProcessLifecycleChange_Action extends ReduxAction<AppState> {
  final AppLifecycleState lifecycle;

  ProcessLifecycleChange_Action(this.lifecycle);

  @override
  Future<AppState?> reduce() async {
    if (lifecycle == AppLifecycleState.resumed ||
        lifecycle == AppLifecycleState.inactive) {
      store.resumePersistor();
    } else if (lifecycle == AppLifecycleState.paused ||
        lifecycle == AppLifecycleState.detached) {
      store.persistAndPausePersistor();
    } else {
      throw AssertionError(lifecycle);
    }
    return null;
  }
}
```

Wrap your app with the lifecycle manager:

```dart
StoreProvider<AppState>(
  store: store,
  child: AppLifecycleManager(
    child: MaterialApp( ... ),
  ),
)
```

## LocalPersist Helper

The `LocalPersist` class simplifies disk operations for Android/iOS. It works with simple object structures containing only primitives, lists, and maps.

```dart
import 'package:async_redux/local_persist.dart';

// Create instance with a file name
var persist = LocalPersist("myFile");

// Save data
List<Object> simpleObjs = [
  'Hello',
  42,
  true,
  [100, 200, {"name": "John"}],
];
await persist.save(simpleObjs);

// Load data
List<Object> loaded = await persist.load();

// Append data
List<Object> moreObjs = ['more', 'data'];
await persist.save(moreObjs, append: true);

// File operations
int length = await persist.length();
bool exists = await persist.exists();
await persist.delete();

// JSON operations for single objects
await persist.saveJson(simpleObj);
Object? simpleObj = await persist.loadJson();
```

**Note:** `LocalPersist` only supports simple objects. For complex nested structures or custom classes, you need to implement serialization yourself (e.g., using JSON encoding with `toJson`/`fromJson` methods).

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/miscellaneous/persistence
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/miscellaneous/database-and-cloud
- https://asyncredux.com/flutter/intro
- https://asyncredux.com/flutter/testing/mocking
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/about
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/miscellaneous/advanced-waiting
