---
name: asyncredux-testing-basics
description: Write unit tests for AsyncRedux actions using the Store directly. Covers creating test stores with initial state, using `dispatchAndWait()`, checking state after actions, verifying action errors via ActionStatus, and testing async actions.
---

# Testing AsyncRedux Actions

The recommended approach for testing AsyncRedux is to use the `Store` directly rather than the deprecated `StoreTester`. This provides a clean, straightforward testing pattern.

## Creating a Test Store

Create a store with test-specific initial state:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:async_redux/async_redux.dart';

void main() {
  test('should increment counter', () async {
    // Create store with initial state
    var store = Store<AppState>(
      initialState: AppState(counter: 0, name: ''),
    );

    // Test your actions here
  });
}
```

For test isolation, create a fresh store in each test:

```dart
void main() {
  late Store<AppState> store;

  setUp(() {
    store = Store<AppState>(
      initialState: AppState.initialState(),
    );
  });

  tearDown(() {
    store.shutdown();
  });

  // Tests go here
}
```

## Basic Test Pattern: Dispatch, Wait, Expect

Use `dispatchAndWait()` to dispatch an action and wait for it to complete:

```dart
test('SaveNameAction updates the name', () async {
  var store = Store<AppState>(
    initialState: AppState(name: ''),
  );

  await store.dispatchAndWait(SaveNameAction('John'));

  expect(store.state.name, 'John');
});
```

## Testing Async Actions

Async actions work the same way - `dispatchAndWait()` returns only when the action fully completes:

```dart
class FetchUserAction extends ReduxAction<AppState> {
  final String userId;
  FetchUserAction(this.userId);

  Future<AppState?> reduce() async {
    var user = await api.fetchUser(userId);
    return state.copy(user: user);
  }
}

test('FetchUserAction loads user data', () async {
  var store = Store<AppState>(
    initialState: AppState(user: null),
  );

  await store.dispatchAndWait(FetchUserAction('123'));

  expect(store.state.user, isNotNull);
  expect(store.state.user!.id, '123');
});
```

## Testing Multiple Actions in Parallel

Use `dispatchAndWaitAll()` to dispatch multiple actions and wait for all to complete:

```dart
test('can buy and sell stocks in parallel', () async {
  var store = Store<AppState>(
    initialState: AppState(portfolio: Portfolio.empty()),
  );

  await store.dispatchAndWaitAll([
    BuyAction('IBM', quantity: 10),
    SellAction('TSLA', quantity: 5),
  ]);

  expect(store.state.portfolio.holdings['IBM'], 10);
  expect(store.state.portfolio.holdings['TSLA'], isNull);
});
```

## Verifying Action Errors with ActionStatus

`dispatchAndWait()` returns an `ActionStatus` object that lets you verify if an action succeeded or failed:

```dart
test('SaveAction fails with invalid data', () async {
  var store = Store<AppState>(
    initialState: AppState.initialState(),
  );

  var status = await store.dispatchAndWait(SaveAction(amount: -100));

  expect(status.isCompletedFailed, isTrue);
  expect(status.isCompletedOk, isFalse);
});
```

### ActionStatus Properties

- **`isCompleted`**: Whether the action finished executing
- **`isCompletedOk`**: True if action finished without errors (both `before()` and `reduce()` completed successfully)
- **`isCompletedFailed`**: True if action threw an error
- **`originalError`**: The error thrown by `before()` or `reduce()`
- **`wrappedError`**: The error after `wrapError()` processing
- **`hasFinishedMethodBefore`**: Whether `before()` completed
- **`hasFinishedMethodReduce`**: Whether `reduce()` completed
- **`hasFinishedMethodAfter`**: Whether `after()` completed

## Testing UserException Errors

Test that actions throw appropriate `UserException` errors:

```dart
class TransferMoney extends ReduxAction<AppState> {
  final double amount;
  TransferMoney(this.amount);

  AppState? reduce() {
    if (amount <= 0) {
      throw UserException('Amount must be positive.');
    }
    return state.copy(balance: state.balance - amount);
  }
}

test('TransferMoney throws UserException for invalid amount', () async {
  var store = Store<AppState>(
    initialState: AppState(balance: 1000),
  );

  var status = await store.dispatchAndWait(TransferMoney(0));

  expect(status.isCompletedFailed, isTrue);

  var error = status.wrappedError;
  expect(error, isA<UserException>());
  expect((error as UserException).msg, 'Amount must be positive.');
});
```

## Testing Multiple Errors with Error Queue

When multiple actions fail, check the store's error queue:

```dart
test('multiple actions can fail', () async {
  var store = Store<AppState>(
    initialState: AppState.initialState(),
  );

  await store.dispatchAndWaitAll([
    InvalidAction1(),
    InvalidAction2(),
  ]);

  // Check errors in the store's error queue
  expect(store.errors.length, 2);
});
```

## Conditional Navigation After Action Success

A common pattern is navigating only after an action succeeds:

```dart
test('navigate only on successful save', () async {
  var store = Store<AppState>(
    initialState: AppState.initialState(),
  );

  var status = await store.dispatchAndWait(SaveAction(data: validData));

  expect(status.isCompletedOk, isTrue);
  // In real code: if (status.isCompletedOk) Navigator.pop(context);
});
```

## Testing State Unchanged on Error

When an action throws, state should remain unchanged:

```dart
test('state unchanged when action fails', () async {
  var store = Store<AppState>(
    initialState: AppState(counter: 5),
  );

  var initialState = store.state;

  await store.dispatchAndWait(FailingAction());

  // State should not have changed
  expect(store.state.counter, 5);
  expect(store.state, initialState);
});
```

## Using MockStore for Dependency Isolation

Use `MockStore` to mock specific actions in tests:

```dart
test('with mocked dependency action', () async {
  var store = MockStore<AppState>(
    initialState: AppState.initialState(),
    mocks: {
      // Disable the action (don't run it)
      FetchFromServerAction: null,

      // Or replace with custom state modification
      FetchFromServerAction: (action, state) =>
        state.copy(data: 'mocked data'),
    },
  );

  await store.dispatchAndWait(ActionThatDependsOnFetch());

  expect(store.state.data, 'mocked data');
});
```

## Advanced Wait Methods for Complex Tests

For complex async scenarios, use these additional wait methods:

```dart
// Wait for a specific state condition
await store.waitCondition((state) => state.isLoaded);

// Wait for all given action types to complete
await store.waitAllActionTypes([LoadAction, ProcessAction]);

// Wait for any action of given types to finish
await store.waitAnyActionTypeFinishes([LoadAction]);

// Wait until no actions are in progress
await store.waitAllActions([]);
```

## Test File Organization

Recommended naming convention for test files:

- Widget: `my_feature.dart`
- State tests: `my_feature_STATE_test.dart`
- Connector tests: `my_feature_CONNECTOR_test.dart`
- Presentation tests: `my_feature_PRESENTATION_test.dart`

## Complete Test Example

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:async_redux/async_redux.dart';

void main() {
  group('IncrementAction', () {
    late Store<AppState> store;

    setUp(() {
      store = Store<AppState>(
        initialState: AppState(counter: 0),
      );
    });

    test('increments counter by 1', () async {
      await store.dispatchAndWait(IncrementAction());
      expect(store.state.counter, 1);
    });

    test('increments counter multiple times', () async {
      await store.dispatchAndWait(IncrementAction());
      await store.dispatchAndWait(IncrementAction());
      await store.dispatchAndWait(IncrementAction());
      expect(store.state.counter, 3);
    });

    test('handles concurrent increments', () async {
      await store.dispatchAndWaitAll([
        IncrementAction(),
        IncrementAction(),
        IncrementAction(),
      ]);
      expect(store.state.counter, 3);
    });
  });

  group('FetchDataAction', () {
    test('succeeds with valid response', () async {
      var store = Store<AppState>(
        initialState: AppState(data: null),
      );

      var status = await store.dispatchAndWait(FetchDataAction());

      expect(status.isCompletedOk, isTrue);
      expect(store.state.data, isNotNull);
    });

    test('fails gracefully on error', () async {
      var store = Store<AppState>(
        initialState: AppState(data: null),
      );

      var status = await store.dispatchAndWait(
        FetchDataAction(simulateError: true),
      );

      expect(status.isCompletedFailed, isTrue);
      expect(status.wrappedError, isA<UserException>());
      expect(store.state.data, isNull); // State unchanged
    });
  });
}
```

## References

URLs from the documentation:
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
- https://asyncredux.com/flutter/testing/test-files
- https://asyncredux.com/flutter/testing/mocking
- https://asyncredux.com/flutter/testing/testing-user-exceptions
- https://asyncredux.com/flutter/advanced-actions/action-status
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/miscellaneous/advanced-waiting
