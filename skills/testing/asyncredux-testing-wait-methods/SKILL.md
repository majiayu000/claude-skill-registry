---
name: asyncredux-testing-wait-methods
description: Use advanced wait methods for complex test scenarios. Covers `waitCondition()`, `waitAllActions()`, `waitActionType()`, `waitAllActionTypes()`, `waitAnyActionTypeFinishes()`, and the `completeImmediately` parameter.
---

# Advanced Wait Methods for Testing

When testing complex async scenarios in AsyncRedux, the basic `dispatchAndWait()` may not be sufficient. The store provides several advanced wait methods for fine-grained control over when tests proceed.

## Overview of Wait Methods

| Method | Purpose |
|--------|---------|
| `waitCondition()` | Wait until state meets a condition |
| `waitAllActions()` | Wait for specific actions to complete, or until no actions are in progress |
| `waitActionType()` | Wait until no action of a given type is in progress |
| `waitAllActionTypes()` | Wait until no actions of the given types are in progress |
| `waitAnyActionTypeFinishes()` | Wait until ANY action of given types finishes |
| `waitActionCondition()` | Low-level: wait until actions in progress meet a custom condition |

## waitCondition()

Waits until the state meets a given condition. Returns the action that triggered the state change.

```dart
Future<ReduxAction<St>?> waitCondition(
  bool Function(St) condition, {
  bool completeImmediately = true,  // Note: default is TRUE here
  int? timeoutMillis,
})
```

### Basic Usage

```dart
test('waitCondition waits for state to match', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  // Dispatch an async action that will change the state
  store.dispatch(IncrementActionAsync());

  // Wait until count becomes 2
  var action = await store.waitCondition((state) => state.count == 2);

  expect(store.state.count, 2);
  expect(action, isA<IncrementActionAsync>());
});
```

### Condition Already True

By default, if the condition is already true, the future completes immediately:

```dart
test('completes immediately when condition already true', () async {
  var store = Store<AppState>(initialState: AppState(count: 5));

  // Condition is already true - completes immediately
  await store.waitCondition((state) => state.count == 5);

  expect(store.state.count, 5);
});
```

### Using completeImmediately: false

To require that the condition must become true (not already be true):

```dart
test('throws when condition already true with completeImmediately: false', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  // This will throw because condition is already true
  expect(
    () => store.waitCondition(
      (state) => state.count == 1,
      completeImmediately: false,
    ),
    throwsA(isA<StoreException>()),
  );
});
```

## waitAllActions()

Waits for specific actions to finish, or waits until no actions are in progress (when passed an empty list or null).

```dart
Future<void> waitAllActions(
  List<ReduxAction<St>>? actions, {
  bool completeImmediately = false,  // Note: default is FALSE here
  int? timeoutMillis,
})
```

### Wait for All Actions to Complete

```dart
test('waitAllActions waits for all dispatched actions', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  var action1 = DelayedIncrementAction(10, delayMillis: 50);
  var action2 = DelayedIncrementAction(100, delayMillis: 100);
  var action3 = DelayedIncrementAction(1000, delayMillis: 20);

  // Dispatch actions in parallel
  store.dispatch(action1);
  store.dispatch(action2);
  store.dispatch(action3);

  expect(store.state.count, 1); // Not changed yet

  // Wait for all three actions to finish
  await store.waitAllActions([action1, action2, action3]);

  expect(store.state.count, 1 + 10 + 100 + 1000);
});
```

### Wait Until No Actions in Progress

Pass an empty list or null to wait until no actions are running:

```dart
test('waitAllActions with empty list waits for all to finish', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  store.dispatch(DelayedAction(10, delayMillis: 50));
  store.dispatch(DelayedAction(100, delayMillis: 100));
  store.dispatch(DelayedAction(1000, delayMillis: 20));

  expect(store.state.count, 1);

  // Wait until ALL actions finish (no actions in progress)
  await store.waitAllActions([]);

  expect(store.state.count, 1 + 10 + 100 + 1000);
});
```

### Selective Waiting

Wait for only some actions to finish, ignoring others:

```dart
test('wait for specific actions only', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  var action50 = DelayedAction(10, delayMillis: 50);
  var action100 = AnotherDelayedAction(100, delayMillis: 100);
  var action200 = SlowAction(100000, delayMillis: 200); // Very slow
  var action10 = DelayedAction(1000, delayMillis: 10);

  store.dispatch(action50);
  store.dispatch(action100);
  store.dispatch(action200); // We don't wait for this one
  store.dispatch(action10);

  // Wait for only the fast actions
  await store.waitAllActions([action50, action100, action10]);

  // The slow action hasn't finished yet
  expect(store.state.count, 1 + 10 + 100 + 1000);
});
```

## waitActionType()

Waits until no action of the given type is in progress. Returns the action that finished (or null if no action was in progress).

```dart
Future<ReduxAction<St>?> waitActionType(
  Type actionType, {
  bool completeImmediately = false,
  int? timeoutMillis,
})
```

### Basic Usage

```dart
test('waitActionType waits for action type to finish', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  store.dispatch(DelayedAction(1000, delayMillis: 10));

  expect(store.state.count, 1);

  // Wait for any DelayedAction to finish
  var action = await store.waitActionType(DelayedAction);

  expect(store.state.count, 1001);
  expect(action, isA<DelayedAction>());
});
```

### Checking Action Status

```dart
test('can check status of finished action', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  store.dispatch(ActionThatMayFail());

  var action = await store.waitActionType(ActionThatMayFail);

  expect(action?.status.isCompletedOk, isTrue);
  // Or check for errors:
  // expect(action?.status.originalError, isA<UserException>());
});
```

### Waiting for Multiple Types Sequentially

```dart
test('wait for multiple action types', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  store.dispatch(AnotherDelayedAction(123, delayMillis: 100));
  store.dispatch(DelayedAction(1000, delayMillis: 10));

  expect(store.state.count, 1);

  // DelayedAction finishes first (10ms)
  await store.waitActionType(DelayedAction);
  expect(store.state.count, 1001);

  // AnotherDelayedAction finishes later (100ms)
  await store.waitActionType(AnotherDelayedAction);
  expect(store.state.count, 1124);
});
```

## waitAllActionTypes()

Waits until ALL actions of the given types are NOT in progress.

```dart
Future<void> waitAllActionTypes(
  List<Type> actionTypes, {
  bool completeImmediately = false,
  int? timeoutMillis,
})
```

### Basic Usage

```dart
test('waitAllActionTypes waits for all types', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  store.dispatch(DelayedAction(10, delayMillis: 50));
  store.dispatch(AnotherDelayedAction(100, delayMillis: 100));
  store.dispatch(SlowAction(100000, delayMillis: 200));
  store.dispatch(DelayedAction(1000, delayMillis: 10));

  expect(store.state.count, 1);

  // Wait for DelayedAction and AnotherDelayedAction types only
  await store.waitAllActionTypes([DelayedAction, AnotherDelayedAction]);

  // SlowAction hasn't finished yet (200ms), but we didn't wait for it
  expect(store.state.count, 1 + 10 + 100 + 1000);
});
```

## waitAnyActionTypeFinishes()

**Important:** This method is different from the others. It waits until ANY action of the given types **finishes dispatching**, even if those actions weren't in progress when the method was called.

```dart
Future<ReduxAction<St>> waitAnyActionTypeFinishes(
  List<Type> actionTypes, {
  int? timeoutMillis,
})
```

### Use Case: Waiting for Nested Actions

This is useful when an action dispatches other actions internally, and you want to wait for one of those nested actions to finish:

```dart
test('waitAnyActionTypeFinishes waits for nested action', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  // StartAction dispatches DelayedAction internally
  store.dispatch(StartAction());

  // Wait for DelayedAction to finish (even though it wasn't dispatched yet)
  var action = await store.waitAnyActionTypeFinishes([DelayedAction]);

  expect(action, isA<DelayedAction>());
  expect(action.status.isCompletedOk, isTrue);
});
```

### Multiple Types - First One to Finish

```dart
test('returns first action type to finish', () async {
  var store = Store<AppState>(initialState: AppState());

  store.dispatch(ProcessStocksAction()); // Dispatches BuyAction or SellAction

  // Wait for either BuyAction or SellAction to finish
  var action = await store.waitAnyActionTypeFinishes([BuyAction, SellAction]);

  expect(action.runtimeType, anyOf(equals(BuyAction), equals(SellAction)));
});
```

## waitActionCondition()

Low-level method that waits until the set of in-progress actions meets a custom condition. This is what the other wait methods use internally.

```dart
Future<(Set<ReduxAction<St>>, ReduxAction<St>?)> waitActionCondition(
  bool Function(Set<ReduxAction<St>> actions, ReduxAction<St>? triggerAction) condition, {
  bool completeImmediately = false,
  String completedErrorMessage = "Awaited action condition was already true",
  int? timeoutMillis,
})
```

### Example: Custom Condition

```dart
test('waitActionCondition with custom condition', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  // Wait until no actions are in progress
  await store.waitActionCondition(
    (actions, triggerAction) => actions.isEmpty,
    completeImmediately: true,
  );
});
```

## The completeImmediately Parameter

This parameter controls behavior when the condition is already met when the method is called:

| Method | Default | When `true` | When `false` |
|--------|---------|-------------|--------------|
| `waitCondition` | `true` | Completes immediately | Throws `StoreException` |
| `waitAllActions` | `false` | Completes immediately | Throws `StoreException` |
| `waitActionType` | `false` | Completes immediately, returns `null` | Throws `StoreException` |
| `waitAllActionTypes` | `false` | Completes immediately | Throws `StoreException` |
| `waitActionCondition` | `false` | Completes immediately | Throws `StoreException` |

**Note:** `waitCondition` defaults to `true` because it's commonly used to check "is state ready?", where you want to proceed if it's already ready. The other methods default to `false` because they're typically used to wait for actions that should be in progress.

```dart
test('completeImmediately behavior', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  // waitCondition: completeImmediately defaults to TRUE
  await store.waitCondition((state) => state.count == 1); // OK, completes

  // waitAllActions: completeImmediately defaults to FALSE
  expect(
    () => store.waitAllActions([]), // No actions in progress
    throwsA(isA<StoreException>()),
  );

  // Use completeImmediately: true to allow it
  await store.waitAllActions([], completeImmediately: true); // OK
});
```

## Timeout Configuration

All wait methods support a `timeoutMillis` parameter. The default timeout is 10 minutes.

```dart
test('waitCondition with timeout', () async {
  var store = Store<AppState>(initialState: AppState(count: 1));

  // This condition will never be true, so it times out
  expect(
    () => store.waitCondition(
      (state) => state.count == 999,
      timeoutMillis: 10, // 10ms timeout
    ),
    throwsA(isA<TimeoutException>()),
  );
});
```

### Global Timeout Configuration

Modify `Store.defaultTimeoutMillis` to change the default for all wait methods:

```dart
void main() {
  // Set global default timeout to 30 seconds
  Store.defaultTimeoutMillis = 30 * 1000;

  // To disable timeout entirely, use -1
  Store.defaultTimeoutMillis = -1;
}
```

## Complete Test Example

```dart
import 'dart:async';
import 'package:async_redux/async_redux.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('Wait Methods', () {
    test('waitCondition waits for state change', () async {
      var store = Store<State>(initialState: State(1));

      // Dispatch async action
      store.dispatch(IncrementActionAsync());

      // Wait for state to change
      await store.waitCondition((state) => state.count == 2);

      expect(store.state.count, 2);
    });

    test('waitAllActions waits for all actions', () async {
      var store = Store<State>(initialState: State(1));

      store.dispatch(DelayedAction(10, delayMillis: 50));
      store.dispatch(DelayedAction(100, delayMillis: 100));
      store.dispatch(DelayedAction(1000, delayMillis: 20));

      await store.waitAllActions([]);

      expect(store.state.count, 1111);
    });

    test('waitActionType waits for specific type', () async {
      var store = Store<State>(initialState: State(1));

      store.dispatch(DelayedAction(1000, delayMillis: 10));

      var action = await store.waitActionType(DelayedAction);

      expect(store.state.count, 1001);
      expect(action?.status.isCompletedOk, isTrue);
    });

    test('waitAllActionTypes waits for multiple types', () async {
      var store = Store<State>(initialState: State(1));

      store.dispatch(DelayedAction(10, delayMillis: 50));
      store.dispatch(AnotherAction(100, delayMillis: 100));

      await store.waitAllActionTypes([DelayedAction, AnotherAction]);

      expect(store.state.count, 111);
    });

    test('waitAnyActionTypeFinishes waits for first finish', () async {
      var store = Store<State>(initialState: State(1));

      store.dispatch(DelayedAction(1, delayMillis: 10));

      var action = await store.waitAnyActionTypeFinishes([DelayedAction]);

      expect(action, isA<DelayedAction>());
      expect(action.status.isCompletedOk, isTrue);
    });
  });
}

// Test state and actions
class State {
  final int count;
  State(this.count);
}

class IncrementActionAsync extends ReduxAction<State> {
  @override
  Future<State> reduce() async {
    await Future.delayed(Duration(milliseconds: 10));
    return State(state.count + 1);
  }
}

class DelayedAction extends ReduxAction<State> {
  final int increment;
  final int delayMillis;

  DelayedAction(this.increment, {required this.delayMillis});

  @override
  Future<State> reduce() async {
    await Future.delayed(Duration(milliseconds: delayMillis));
    return State(state.count + increment);
  }
}

class AnotherAction extends DelayedAction {
  AnotherAction(int increment, {required int delayMillis})
      : super(increment, delayMillis: delayMillis);
}
```

## References

URLs from the documentation:
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/miscellaneous/wait-condition
- https://asyncredux.com/flutter/miscellaneous/advanced-waiting
- https://asyncredux.com/flutter/testing/mocking
- https://asyncredux.com/flutter/basics/dispatching-actions
