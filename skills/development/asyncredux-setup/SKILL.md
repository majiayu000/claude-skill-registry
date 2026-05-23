---
name: asyncredux-setup
description: Initialize, setup and configure AsyncRedux in a Flutter app. Use it whenever starting a new AsyncRedux project, or when the user requests.
---

# AsyncRedux Setup

## Adding the Dependency

Add AsyncRedux to your `pubspec.yaml`:

```yaml
dependencies:
  async_redux: ^25.6.1
```

Check [pub.dev](https://pub.dev/packages/async_redux) for the latest version.

## Creating the State Class

Create an immutable `AppState` class (in file `app_state.dart`) with:

* `copy()` method
* `==` equals method
* `hashCode` method
* `initialState()` static factory

If the app is new, and you don't have any state yet, create an empty `AppState`:

```dart
@immutable
class AppState {
  AppState();
  static AppState initialState() => AppState();
  AppState copy() => AppState();
  
  @override
  bool operator ==(Object other) =>
    identical(this, other) ||
    other is AppState && runtimeType == other.runtimeType;

  @override
  int get hashCode => 0;
}
```

If there is existing state, create the `AppState` that incorporates that state.
This is an example:

```dart
@immutable
class AppState {
  final String name;
  final int age;
  AppState({required this.name, required this.age});

  static AppState initialState() => AppState(name: "", age: 0);

  AppState copy({String? name, int? age}) => AppState(
    name: name ?? this.name,
    age: age ?? this.age,
  );
  
  @override
  bool operator ==(Object other) =>
    identical(this, other) ||
    other is AppState &&
      runtimeType == other.runtimeType &&
      name == other.name &&
      age == other.age;

  @override
  int get hashCode => Object.hash(name, age);
}

```

All fields must be `final` (immutable). Add additional helper methods as needed:

```dart
AppState withName(String name) => copy(name: name);
AppState withAge(int age) => copy(age: age);
```

## Creating the Store

Find the place where you initialize your app (usually in `main.dart`),
and import your `AppState` class (adapt the path as needed) and the AsyncRedux package:

```dart
import 'app_state.dart'; 
import 'package:async_redux/async_redux.dart';
```

Create the store with your initial state. Note that `PersistorDummy`,
`GlobalWrapErrorDummy`, and `ConsoleActionObserver` are provided by AsyncRedux for basic
setups. In the future these can be replaced with custom implementations as needed.

```dart
late Store store;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Create the persistor, and try to read any previously saved state.
  var persistor = PersistorDummy<AppState>();
  AppState? initialState = await persistor.readState();
  
  // If there is no saved state, create a new empty one and save it.
  if (initialState == null) {
    initialState = AppState.initialState();
    await persistor.saveInitialState(initialState);
  }
    
  // Create the store.
  store = Store<AppState>(
    initialState: initialState,
    persistor: persistor,
    globalWrapError: GlobalWrapErrorDummy(),    
    actionObservers: [ConsoleActionObserver()],
  );

  runApp(...);
}
```

## Wrapping with StoreProvider

Wrap your app with `StoreProvider` to make the store accessible.
Find the root of the widget tree of the app, and add it above `MaterialApp` (or
`CupertinoApp`, adapting as needed). Note you will need to import the `store` too.

```dart
import 'package:async_redux/async_redux.dart';

Widget build(context) {
  return StoreProvider<AppState>(
    store: store,
    child: MaterialApp( ... ),
  );
}
```

## Required Context Extensions

You **must** add this extension to your file containing `AppState` (this is required for
easier state access in widgets):

```dart
extension BuildContextExtension on BuildContext {
  AppState get state => getState<AppState>();

  AppState read() => getRead<AppState>();

  R select<R>(R Function(AppState state) selector) =>
      getSelect<AppState, R>(selector);

  R? event<R>(Evt<R> Function(AppState state) selector) =>
      getEvent<AppState, R>(selector);
}
```

## Required base action

Create file `app_action.dart` with this abstract class extending `ReduxAction<AppState>`:

```dart
/// All actions extend this class.
abstract class AppAction extends ReduxAction<AppState> {

ActionSelect get select => ActionSelect(state);
}

// Dedicated selector class to keep the base action clean.
class ActionSelect {
  final AppState state;
  ActionSelect(this.state);
}
```

## Update CLAUDE.md

Add the following information to the project's `CLAUDE.md`, so that all actions extend
this
base action:

```markdown
## Base Action

All actions should extend `AppAction` instead of `ReduxAction<AppState>`. 
There is a dedicated selector class called `ActionSelect` to keep the base action clean,
by namespacing selectors under `select` and enabling IDE autocompletion. Example:

  ```dart
  class ProcessItem extends AppAction {
    final String itemId;
    ProcessItem(this.itemId);
    
    @override
    AppState reduce() {
      // IDE autocomplete shows: select.findById, select.completed, etc.
      final item = select.findById(itemId);
      // ...
    }
  }
  ```

```
