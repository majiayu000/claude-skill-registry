---
name: asyncredux-testing-view-models
description: Test StoreConnector view-models in isolation. Covers creating view-models with `Vm.createFrom()`, testing view-model properties, testing callbacks that dispatch actions, and verifying state changes from callbacks.
---

# Testing View-Models in AsyncRedux

View-models created by `VmFactory` can be tested in isolation without building widgets. Use `Vm.createFrom()` to instantiate the view-model directly, then verify properties and execute callbacks.

## Creating a View-Model for Testing

Use `Vm.createFrom()` with a store and factory instance:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:async_redux/async_redux.dart';

test('view-model has correct properties', () {
  var store = Store<AppState>(
    initialState: AppState(name: 'Mary', counter: 5),
  );

  var vm = Vm.createFrom(store, CounterFactory());

  expect(vm.counter, 5);
  expect(vm.name, 'Mary');
});
```

**Important:** `Vm.createFrom()` can only be called once per factory instance. Create a new factory for each test.

## Testing View-Model Properties

Verify that the factory correctly transforms state into view-model properties:

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

class CounterFactory extends VmFactory<AppState, CounterConnector, CounterViewModel> {
  @override
  CounterViewModel fromStore() => CounterViewModel(
    counter: state.counter,
    description: 'Count is ${state.counter}',
    onIncrement: () => dispatch(IncrementAction()),
  );
}

test('factory transforms state correctly', () {
  var store = Store<AppState>(
    initialState: AppState(counter: 10),
  );

  var vm = Vm.createFrom(store, CounterFactory());

  expect(vm.counter, 10);
  expect(vm.description, 'Count is 10');
});
```

## Testing Callbacks That Dispatch Actions

When testing callbacks, invoke them and then use wait methods to verify actions were dispatched and state changed:

```dart
test('onIncrement dispatches IncrementAction', () async {
  var store = Store<AppState>(
    initialState: AppState(counter: 0),
  );

  var vm = Vm.createFrom(store, CounterFactory());

  // Invoke the callback
  vm.onIncrement();

  // Wait for the action to complete
  await store.waitActionType(IncrementAction);

  // Verify state changed
  expect(store.state.counter, 1);
});
```

## Wait Methods for Callback Testing

Several wait methods help verify callback behavior:

### waitActionType

Wait for a specific action type to finish:

```dart
test('callback dispatches expected action', () async {
  var store = Store<AppState>(initialState: AppState(name: ''));
  var vm = Vm.createFrom(store, UserFactory());

  vm.onSave('John');
  await store.waitActionType(SaveNameAction);

  expect(store.state.name, 'John');
});
```

### waitAllActionTypes

Wait for multiple action types to complete:

```dart
test('callback triggers multiple actions', () async {
  var store = Store<AppState>(initialState: AppState.initialState());
  var vm = Vm.createFrom(store, CheckoutFactory());

  vm.onCheckout();
  await store.waitAllActionTypes([ValidateCartAction, ProcessPaymentAction]);

  expect(store.state.orderCompleted, isTrue);
});
```

### waitAnyActionTypeFinishes

Wait for any matching action to finish, useful when testing actions that may or may not be dispatched:

```dart
test('refresh triggers data fetch', () async {
  var store = Store<AppState>(initialState: AppState.initialState());
  var vm = Vm.createFrom(store, DataFactory());

  vm.onRefresh();
  var action = await store.waitAnyActionTypeFinishes([FetchDataAction]);

  expect(action, isA<FetchDataAction>());
  expect(store.state.data, isNotEmpty);
});
```

### waitCondition

Wait for state to meet a specific condition:

```dart
test('loading completes when data is fetched', () async {
  var store = Store<AppState>(initialState: AppState(isLoading: false, data: null));
  var vm = Vm.createFrom(store, DataFactory());

  vm.onLoad();
  await store.waitCondition((state) => state.data != null);

  expect(store.state.isLoading, isFalse);
  expect(store.state.data, isNotNull);
});
```

### waitAllActions

Wait until no actions are in progress:

```dart
test('all actions complete', () async {
  var store = Store<AppState>(initialState: AppState.initialState());
  var vm = Vm.createFrom(store, BatchFactory());

  vm.onProcessBatch();
  await store.waitAllActions([]);

  expect(store.state.batchProcessed, isTrue);
});
```

## Testing Callbacks with Action Status

Verify that callbacks dispatch actions that succeed or fail appropriately:

```dart
test('save callback handles errors', () async {
  var store = Store<AppState>(
    initialState: AppState(data: ''),
  );

  var vm = Vm.createFrom(store, FormFactory());

  // Trigger save with invalid data
  vm.onSave('');

  // dispatchAndWait returns ActionStatus, but when testing callbacks,
  // use waitActionType and check store.errors
  await store.waitActionType(SaveAction);

  // Check if action failed
  expect(store.errors, isNotEmpty);
});
```

## Testing Async Callbacks

Async callbacks work the same way - wait for the dispatched actions:

```dart
class UserFactory extends VmFactory<AppState, UserConnector, UserViewModel> {
  @override
  UserViewModel fromStore() => UserViewModel(
    user: state.user,
    onRefresh: () => dispatch(FetchUserAction()),
  );
}

test('onRefresh loads user data', () async {
  var store = Store<AppState>(
    initialState: AppState(user: null),
  );

  var vm = Vm.createFrom(store, UserFactory());

  vm.onRefresh();
  await store.waitActionType(FetchUserAction);

  expect(store.state.user, isNotNull);
});
```

## Testing with Mocked Actions

Use `MockStore` to mock actions triggered by callbacks:

```dart
test('callback with mocked dependency', () async {
  var store = MockStore<AppState>(
    initialState: AppState(data: null),
    mocks: {
      // Mock the API call to return test data
      FetchDataAction: (action, state) => state.copy(data: 'mocked data'),
    },
  );

  var vm = Vm.createFrom(store, DataFactory());

  vm.onFetch();
  await store.waitActionType(FetchDataAction);

  expect(store.state.data, 'mocked data');
});
```

## Testing onInit and onDispose Lifecycle

Use `ConnectorTester` to test lifecycle callbacks without building widgets:

```dart
class MyScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) => StoreConnector<AppState, MyViewModel>(
    vm: () => MyFactory(),
    onInit: (store) => store.dispatch(StartPollingAction()),
    onDispose: (store) => store.dispatch(StopPollingAction()),
    builder: (context, vm) => MyWidget(vm: vm),
  );
}

test('onInit dispatches StartPollingAction', () async {
  var store = Store<AppState>(initialState: AppState.initialState());
  var connectorTester = store.getConnectorTester(MyScreen());

  connectorTester.runOnInit();
  var action = await store.waitAnyActionTypeFinishes([StartPollingAction]);

  expect(action, isA<StartPollingAction>());
});

test('onDispose dispatches StopPollingAction', () async {
  var store = Store<AppState>(initialState: AppState.initialState());
  var connectorTester = store.getConnectorTester(MyScreen());

  connectorTester.runOnDispose();
  var action = await store.waitAnyActionTypeFinishes([StopPollingAction]);

  expect(action, isA<StopPollingAction>());
});
```

## Complete Test Example

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:async_redux/async_redux.dart';

// View-Model
class TodoViewModel extends Vm {
  final List<String> todos;
  final bool isLoading;
  final void Function(String) onAddTodo;
  final void Function(int) onRemoveTodo;
  final VoidCallback onRefresh;

  TodoViewModel({
    required this.todos,
    required this.isLoading,
    required this.onAddTodo,
    required this.onRemoveTodo,
    required this.onRefresh,
  }) : super(equals: [todos, isLoading]);
}

// Factory
class TodoFactory extends VmFactory<AppState, TodoConnector, TodoViewModel> {
  @override
  TodoViewModel fromStore() => TodoViewModel(
    todos: state.todos,
    isLoading: state.isLoading,
    onAddTodo: (text) => dispatch(AddTodoAction(text)),
    onRemoveTodo: (index) => dispatch(RemoveTodoAction(index)),
    onRefresh: () => dispatch(FetchTodosAction()),
  );
}

void main() {
  group('TodoFactory', () {
    late Store<AppState> store;

    setUp(() {
      store = Store<AppState>(
        initialState: AppState(todos: [], isLoading: false),
      );
    });

    test('creates view-model with correct initial properties', () {
      var vm = Vm.createFrom(store, TodoFactory());

      expect(vm.todos, isEmpty);
      expect(vm.isLoading, isFalse);
    });

    test('onAddTodo dispatches AddTodoAction', () async {
      var vm = Vm.createFrom(store, TodoFactory());

      vm.onAddTodo('Buy milk');
      await store.waitActionType(AddTodoAction);

      expect(store.state.todos, contains('Buy milk'));
    });

    test('onRemoveTodo dispatches RemoveTodoAction', () async {
      store = Store<AppState>(
        initialState: AppState(todos: ['Task 1', 'Task 2'], isLoading: false),
      );
      var vm = Vm.createFrom(store, TodoFactory());

      vm.onRemoveTodo(0);
      await store.waitActionType(RemoveTodoAction);

      expect(store.state.todos, ['Task 2']);
    });

    test('onRefresh fetches todos', () async {
      var vm = Vm.createFrom(store, TodoFactory());

      vm.onRefresh();
      await store.waitCondition((state) => !state.isLoading);

      expect(store.state.todos, isNotEmpty);
    });
  });
}
```

## Test Organization

Follow the recommended naming convention for test files:

- Widget: `todo_screen.dart`
- Connector: `todo_screen_connector.dart`
- State tests: `todo_screen_STATE_test.dart`
- Connector tests: `todo_screen_CONNECTOR_test.dart`
- Presentation tests: `todo_screen_PRESENTATION_test.dart`

Connector tests focus on view-model logic - verifying properties are correctly derived from state and callbacks dispatch appropriate actions.

## References

URLs from the documentation:
- https://asyncredux.com/flutter/testing/testing-the-view-model
- https://asyncredux.com/flutter/testing/testing-oninit-ondispose
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
- https://asyncredux.com/flutter/testing/test-files
- https://asyncredux.com/flutter/testing/mocking
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/connector/store-connector
- https://asyncredux.com/flutter/connector/advanced-view-model
- https://asyncredux.com/flutter/connector/connector-pattern
- https://asyncredux.com/flutter/miscellaneous/advanced-waiting
