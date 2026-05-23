---
name: asyncredux-wait-condition
description: Use `waitCondition()` inside actions to pause execution until state meets criteria. Covers waiting for price thresholds, coordinating between actions, and implementing conditional workflows.
---

# Waiting for State Conditions with waitCondition()

The `waitCondition()` method pauses execution until the application state satisfies a specific condition. It's available on both the `Store` and `ReduxAction` classes.

## Method Signature

```dart
Future<ReduxAction<St>?> waitCondition(
  bool Function(St) condition, {
  bool completeImmediately = true,
  int? timeoutMillis,
});
```

**Parameters:**
- **condition**: A function that takes the current state and returns `true` when the desired condition is met
- **completeImmediately**: If `true` (default), completes immediately when the condition is already satisfied. If `false`, waits for a state change to meet the condition
- **timeoutMillis**: Maximum time to wait (defaults to 10 minutes). Set to `-1` to disable timeout

**Returns:** The action that triggered the condition to become true, or `null` if condition was already met.

## Basic Usage Inside an Action

Use `waitCondition()` when your action needs to wait for a prerequisite state before proceeding:

```dart
class AddAppointmentAction extends ReduxAction<AppState> {
  final String title;
  final DateTime date;

  AddAppointmentAction({required this.title, required this.date});

  @override
  Future<AppState?> reduce() async {
    // Ensure calendar exists before adding appointment
    if (state.calendar == null) {
      dispatch(CreateCalendarAction());

      // Wait until calendar is available
      await waitCondition((state) => state.calendar != null);
    }

    // Now safe to add the appointment
    return state.copy(
      calendar: state.calendar!.addAppointment(
        Appointment(title: title, date: date),
      ),
    );
  }
}
```

## Waiting for Value Thresholds

Wait for numeric values to reach specific thresholds:

```dart
class ExecuteTradeAction extends ReduxAction<AppState> {
  final double targetPrice;

  ExecuteTradeAction(this.targetPrice);

  @override
  Future<AppState?> reduce() async {
    // Wait until stock price reaches target
    await waitCondition((state) => state.stockPrice >= targetPrice);

    // Execute the trade at or above target price
    return state.copy(
      tradeExecuted: true,
      executionPrice: state.stockPrice,
    );
  }
}
```

## Coordinating Between Actions

Use `waitCondition()` to coordinate dependent actions:

```dart
class ProcessOrderAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    // Dispatch parallel data loading
    dispatch(LoadInventoryAction());
    dispatch(LoadPricingAction());

    // Wait for both to complete
    await waitCondition((state) =>
      state.inventoryLoaded && state.pricingLoaded
    );

    // Both are now available - proceed with order processing
    final total = calculateTotal(state.inventory, state.pricing);
    return state.copy(orderTotal: total);
  }
}
```

## Implementing Conditional Workflows

Create multi-step workflows that wait for user input or external events:

```dart
class CheckoutWorkflowAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    // Step 1: Wait for cart to be ready
    await waitCondition((state) => state.cart.isNotEmpty);

    // Step 2: Start payment processing
    dispatch(InitiatePaymentAction());

    // Step 3: Wait for payment confirmation
    await waitCondition((state) =>
      state.paymentStatus == PaymentStatus.confirmed ||
      state.paymentStatus == PaymentStatus.failed
    );

    if (state.paymentStatus == PaymentStatus.failed) {
      throw UserException('Payment failed. Please try again.');
    }

    // Step 4: Complete the order
    return state.copy(orderCompleted: true);
  }
}
```

## Using the Return Value

`waitCondition()` returns the action that caused the condition to become true:

```dart
class MonitorPriceAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    // Wait for price change and get the action that changed it
    final triggeringAction = await waitCondition(
      (state) => state.price > 100,
    );

    // Can inspect which action triggered the condition
    if (triggeringAction is PriceUpdateAction) {
      print('Price updated by: ${triggeringAction.source}');
    }

    return state.copy(alertTriggered: true);
  }
}
```

## Using completeImmediately Parameter

Control behavior when the condition is already met:

```dart
class WaitForNewDataAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    // completeImmediately: false means wait for a NEW state change
    // even if condition is currently satisfied
    await waitCondition(
      (state) => state.dataVersion > 0,
      completeImmediately: false,  // Wait for fresh data
    );

    return state.copy(dataProcessed: true);
  }
}
```

## Setting Timeouts

Prevent indefinite waiting with custom timeouts:

```dart
class TimeSensitiveAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    try {
      // Wait maximum 5 seconds for condition
      await waitCondition(
        (state) => state.isReady,
        timeoutMillis: 5000,
      );
    } catch (e) {
      // Timeout exceeded - handle gracefully
      throw UserException('Operation timed out. Please try again.');
    }

    return state.copy(processed: true);
  }
}
```

## Using waitCondition() from the Store

In tests or widgets, call `waitCondition()` directly on the store:

```dart
// In a test
test('waits for data to load', () async {
  var store = Store<AppState>(initialState: AppState.initial());

  store.dispatch(LoadDataAction());

  // Wait for loading to complete
  await store.waitCondition((state) => state.isLoaded);

  expect(store.state.data, isNotNull);
});
```

## Testing with waitCondition()

`waitCondition()` is useful in tests to wait for expected state:

```dart
test('processes order after inventory loads', () async {
  var store = Store<AppState>(
    initialState: AppState(inventoryLoaded: false),
  );

  // Start the process
  store.dispatch(ProcessOrderAction());

  // Simulate inventory loading
  await Future.delayed(Duration(milliseconds: 100));
  store.dispatch(LoadInventoryCompleteAction());

  // Wait for order processing to complete
  await store.waitCondition((state) => state.orderProcessed);

  expect(store.state.orderTotal, greaterThan(0));
});
```

## Comparison with Other Wait Methods

| Method | Use Case |
|--------|----------|
| `waitCondition()` | Wait for state to satisfy a predicate |
| `dispatchAndWait()` | Wait for a specific action to complete |
| `waitAllActions([])` | Wait for all current actions to finish |
| `waitActionType()` | Wait for an action of a specific type |

## Common Patterns

### Wait for Initialization

```dart
class AppStartupAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    dispatch(LoadUserAction());
    dispatch(LoadSettingsAction());
    dispatch(LoadCacheAction());

    // Wait for all initialization to complete
    await waitCondition((state) =>
      state.user != null &&
      state.settings != null &&
      state.cacheReady
    );

    return state.copy(appReady: true);
  }
}
```

### Wait for User Confirmation

```dart
class DeleteAccountAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    // Show confirmation dialog
    dispatch(ShowConfirmationDialogAction(
      message: 'Are you sure you want to delete your account?',
    ));

    // Wait for user response
    await waitCondition((state) =>
      state.confirmationResult != null
    );

    if (state.confirmationResult != true) {
      return null; // User cancelled
    }

    // Proceed with deletion
    await api.deleteAccount();
    return state.copy(accountDeleted: true);
  }
}
```

## References

URLs from the documentation:
- https://asyncredux.com/flutter/miscellaneous/wait-condition
- https://asyncredux.com/flutter/miscellaneous/advanced-waiting
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
