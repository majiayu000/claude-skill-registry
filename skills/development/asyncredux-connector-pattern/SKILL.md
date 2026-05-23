---
name: asyncredux-connector-pattern
description: Implement the Connector pattern for separating smart and dumb widgets. Covers creating StoreConnector widgets, implementing VmFactory and Vm classes, building view-models, and optimizing rebuilds with view-model equality.
---

## Overview

The connector pattern separates store access logic from UI presentation. Instead of widgets directly accessing the store via `context.state` and `context.dispatch()`, a "smart" connector widget extracts store data and passes it to a "dumb" presentational widget through constructor parameters.

## Why Use the Connector Pattern?

1. **Testing simplification** - Test UI widgets without creating a Redux store by passing mock data
2. **Separation of concerns** - UI widgets focus on appearance; connectors handle business logic
3. **Reusability** - Presentational widgets function independently of Redux
4. **Code clarity** - Widget code is not cluttered with state access and transformation logic
5. **Optimized rebuilds** - Only rebuild when the view-model changes

## The Three Components

### 1. ViewModel (Vm)

Contains only the data the UI widget requires. Extends `Vm` and lists equality fields:

```dart
class CounterViewModel extends Vm {
  final int counter;
  final String description;
  final VoidCallback onIncrement;

  CounterViewModel({
    required this.counter,
    required this.description,
    required this.onIncrement,
  }) : super(equals: [counter, description]);
}
```

The `equals` list tells AsyncRedux which fields to compare when deciding whether to rebuild. Callbacks (like `onIncrement`) should NOT be included in `equals`.

### 2. VmFactory

Transforms store state into a view-model. Extends `VmFactory` and implements `fromStore()`:

```dart
class CounterFactory extends VmFactory<AppState, CounterConnector, CounterViewModel> {
  CounterFactory(connector) : super(connector);

  @override
  CounterViewModel fromStore() => CounterViewModel(
    counter: state.counter,
    description: state.description,
    onIncrement: () => dispatch(IncrementAction()),
  );
}
```

The factory has access to:
- `state` - The store state when the factory was created
- `dispatch()` - To dispatch actions from callbacks
- `dispatchSync()` - For synchronous dispatch
- `connector` - Reference to the parent connector widget

### 3. StoreConnector

Bridges the store and UI widget:

```dart
class CounterConnector extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, CounterViewModel>(
      vm: () => CounterFactory(this),
      builder: (BuildContext context, CounterViewModel vm) => CounterWidget(
        counter: vm.counter,
        description: vm.description,
        onIncrement: vm.onIncrement,
      ),
    );
  }
}
```

The "dumb" widget receives data through constructor parameters:

```dart
class CounterWidget extends StatelessWidget {
  final int counter;
  final String description;
  final VoidCallback onIncrement;

  const CounterWidget({
    required this.counter,
    required this.description,
    required this.onIncrement,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('$counter'),
        Text(description),
        ElevatedButton(
          onPressed: onIncrement,
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

## Rebuild Optimization

Each time an action changes the store state, `StoreConnector` compares the new view-model with the previous one. It only rebuilds if they differ (based on the `equals` list).

To prevent rebuilds even when state changes, use `notify: false`:

```dart
dispatch(MyAction(), notify: false);
```

## Advanced Factory Techniques

### Accessing Connector Properties

Pass data from the connector widget to the factory:

```dart
class UserConnector extends StatelessWidget {
  final int userId;
  const UserConnector({required this.userId});

  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, UserViewModel>(
      vm: () => UserFactory(this),
      builder: (context, vm) => UserWidget(user: vm.user),
    );
  }
}

class UserFactory extends VmFactory<AppState, UserConnector, UserViewModel> {
  UserFactory(connector) : super(connector);

  @override
  UserViewModel fromStore() => UserViewModel(
    // Access connector.userId here
    user: state.users.firstWhere((u) => u.id == connector.userId),
  );
}
```

### state vs currentState()

Inside the factory:
- `state` - The state when the factory was created (final, won't change)
- `currentState()` - The current store state at the moment of the call

These usually match, but diverge in callbacks after `dispatchSync()`:

```dart
@override
UserViewModel fromStore() => UserViewModel(
  onSave: () {
    dispatchSync(SaveAction());
    // state still has old value
    // currentState() has new value after SaveAction
  },
);
```

### Using the vm Getter in Callbacks

Access already-computed view-model fields in callbacks to avoid redundant calculations:

```dart
@override
UserViewModel fromStore() => UserViewModel(
  name: state.user.name,
  onSave: () {
    // Use vm.name instead of recalculating from state
    print('Saving user: ${vm.name}');
    dispatch(SaveAction(vm.name));
  },
);
```

**Note:** The `vm` getter is only available after `fromStore()` completes. Use it in callbacks, not during view-model construction.

### Base Factory Pattern

Create a base factory to reduce boilerplate:

```dart
abstract class BaseFactory<T extends StatelessWidget, Model extends Vm>
    extends VmFactory<AppState, T, Model> {
  BaseFactory(T connector) : super(connector);

  // Common getters
  User get user => state.user;
  Settings get settings => state.settings;
}

class MyFactory extends BaseFactory<MyConnector, MyViewModel> {
  MyFactory(connector) : super(connector);

  @override
  MyViewModel fromStore() => MyViewModel(
    user: user,  // Uses inherited getter
  );
}
```

## Nullable View-Models

When you cannot generate a valid view-model (e.g., data still loading), return null:

```dart
class HomeConnector extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, HomeViewModel?>(  // Nullable type
      vm: () => HomeFactory(this),
      builder: (BuildContext context, HomeViewModel? vm) {  // Nullable param
        return (vm == null)
          ? Text("User not logged in")
          : HomePage(user: vm.user);
      },
    );
  }
}

class HomeFactory extends VmFactory<AppState, HomeConnector, HomeViewModel?> {
  HomeFactory(connector) : super(connector);

  @override
  HomeViewModel? fromStore() {  // Nullable return
    return (state.user == null)
      ? null
      : HomeViewModel(user: state.user!);
  }
}
```

## Migrating from flutter_redux

If migrating from `flutter_redux`, you can use the `converter` parameter instead of `vm`:

```dart
class MyConnector extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, ViewModel>(
      converter: (store) => ViewModel.fromStore(store),
      builder: (context, vm) => MyWidget(name: vm.name),
    );
  }
}

class ViewModel extends Vm {
  final String name;
  final VoidCallback onSave;

  ViewModel({required this.name, required this.onSave})
    : super(equals: [name]);

  static ViewModel fromStore(Store<AppState> store) {
    return ViewModel(
      name: store.state.name,
      onSave: () => store.dispatch(SaveAction()),
    );
  }
}
```

Note: `vm` and `converter` are mutually exclusive. The `vm` approach is recommended for new code.

## Debugging Rebuilds

To observe when connectors rebuild, pass a `modelObserver` to the store:

```dart
var store = Store<AppState>(
  initialState: AppState.initialState(),
  modelObserver: DefaultModelObserver(),
);
```

Add `debug: this` to StoreConnector for connector type names in logs:

```dart
StoreConnector<AppState, ViewModel>(
  debug: this,
  vm: () => Factory(this),
  builder: (context, vm) => MyWidget(vm: vm),
);
```

Override `toString()` in your ViewModel for custom diagnostic output:

```dart
class MyViewModel extends Vm {
  final int counter;
  MyViewModel({required this.counter}) : super(equals: [counter]);

  @override
  String toString() => 'MyViewModel{counter: $counter}';
}
```

Console output shows rebuild information:
```
Model D:1 R:1 = Rebuild:true, Connector:MyWidgetConnector, Model:MyViewModel{counter: 5}
```

## Testing View-Models

Use `Vm.createFrom()` to test view-models in isolation:

```dart
test('view-model properties', () {
  var store = Store<AppState>(initialState: AppState(name: "Mary"));
  var vm = Vm.createFrom(store, MyFactory());

  expect(vm.name, "Mary");
});

test('view-model callbacks dispatch actions', () async {
  var store = Store<AppState>(initialState: AppState(name: "Mary"));
  var vm = Vm.createFrom(store, MyFactory());

  vm.onChangeName("Bill");
  await store.waitActionType(ChangeNameAction);
  expect(store.state.name, "Bill");
});
```

**Important:** `Vm.createFrom()` can only be called once per factory instance. Create a new factory for each test.

## Complete Example

```dart
// State
class AppState {
  final int counter;
  final String description;
  AppState({required this.counter, required this.description});
  AppState copy({int? counter, String? description}) => AppState(
    counter: counter ?? this.counter,
    description: description ?? this.description,
  );
}

// Action
class IncrementAction extends ReduxAction<AppState> {
  @override
  AppState reduce() => state.copy(counter: state.counter + 1);
}

// View-Model
class CounterViewModel extends Vm {
  final int counter;
  final String description;
  final VoidCallback onIncrement;

  CounterViewModel({
    required this.counter,
    required this.description,
    required this.onIncrement,
  }) : super(equals: [counter, description]);
}

// Factory
class CounterFactory extends VmFactory<AppState, CounterConnector, CounterViewModel> {
  CounterFactory(connector) : super(connector);

  @override
  CounterViewModel fromStore() => CounterViewModel(
    counter: state.counter,
    description: state.description,
    onIncrement: () => dispatch(IncrementAction()),
  );
}

// Connector (Smart Widget)
class CounterConnector extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, CounterViewModel>(
      vm: () => CounterFactory(this),
      builder: (context, vm) => CounterWidget(
        counter: vm.counter,
        description: vm.description,
        onIncrement: vm.onIncrement,
      ),
    );
  }
}

// Presentational Widget (Dumb Widget)
class CounterWidget extends StatelessWidget {
  final int counter;
  final String description;
  final VoidCallback onIncrement;

  const CounterWidget({
    required this.counter,
    required this.description,
    required this.onIncrement,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text('$counter', style: TextStyle(fontSize: 48)),
        Text(description),
        SizedBox(height: 20),
        ElevatedButton(
          onPressed: onIncrement,
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/connector/connector-pattern
- https://asyncredux.com/flutter/connector/store-connector
- https://asyncredux.com/flutter/connector/advanced-view-model
- https://asyncredux.com/flutter/connector/cannot-generate-view-model
- https://asyncredux.com/flutter/connector/migrating-from-flutter-redux
- https://asyncredux.com/flutter/testing/testing-the-view-model
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/miscellaneous/observing-rebuilds
