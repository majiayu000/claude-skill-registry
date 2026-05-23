---
name: asyncredux-dispatching-actions
description: Dispatch actions using all available methods: `dispatch()`, `dispatchAndWait()`, `dispatchAll()`, `dispatchAndWaitAll()`, and `dispatchSync()`. Covers dispatching from widgets via context extensions and from within other actions.
---

# Dispatching Actions

The foundational principle of AsyncRedux: **the only way to change the application state is by dispatching actions.** You can dispatch from widgets (via context extensions) or from within other actions.

## Five Dispatch Methods

### 1. dispatch()

The standard method that returns immediately. For synchronous actions, state updates before return; for async actions, the process begins and completes later.

```dart
dispatch(MyAction());
```

### 2. dispatchAndWait()

Returns a `Future` that completes when the action finishes and state changes, regardless of whether the action is sync or async. Returns an `ActionStatus` object.

```dart
var status = await dispatchAndWait(MyAction());
if (status.isCompletedOk) {
  Navigator.pop(context);
}
```

### 3. dispatchAll()

Dispatches multiple actions in parallel, returning the list of dispatched actions.

```dart
dispatchAll([BuyAction('IBM'), SellAction('TSLA')]);
```

### 4. dispatchAndWaitAll()

Dispatches actions in parallel and waits for all to complete.

```dart
await dispatchAndWaitAll([
  BuyAction('IBM'),
  SellAction('TSLA'),
]);
```

### 5. dispatchSync()

Like `dispatch()` but throws a `StoreException` if the action is asynchronous. Use when synchronous execution is mandatory.

```dart
dispatchSync(MyAction());
```

## Dispatching from Widgets

All dispatch methods are available as `BuildContext` extensions:

```dart
context.dispatch(Action());
context.dispatchAll([Action1(), Action2()]);
await context.dispatchAndWait(Action());
await context.dispatchAndWaitAll([Action1(), Action2()]);
context.dispatchSync(Action());
```

Example button implementation:

```dart
ElevatedButton(
  onPressed: () => context.dispatch(Increment()),
  child: Text('Increment'),
)
```

For async dispatch in callbacks:

```dart
ElevatedButton(
  onPressed: () async {
    var status = await context.dispatchAndWait(SaveAction());
    if (status.isCompletedOk) {
      Navigator.pop(context);
    }
  },
  child: Text('Save'),
)
```

## Dispatching from Within Actions

All dispatch methods are available inside actions via the `ReduxAction` base class:

```dart
class MyAction extends ReduxAction<AppState> {
  Future<AppState?> reduce() async {
    // Dispatch another action and wait for it
    await dispatchAndWait(LoadDataAction());

    // Dispatch without waiting
    dispatch(LogAction('Data loaded'));

    return state.copy(loaded: true);
  }
}
```

### Dispatching in before() and after()

You can dispatch actions in the `before()` and `after()` lifecycle methods:

```dart
class MyAction extends ReduxAction<AppState> {
  Future<AppState?> reduce() async {
    String description = await fetchData();
    return state.copy(description: description);
  }

  void before() => dispatch(BarrierAction(true));
  void after() => dispatch(BarrierAction(false));
}
```

## ActionStatus

The `dispatchAndWait()` method returns an `ActionStatus` object with useful properties:

```dart
var status = await dispatchAndWait(MyAction());

// Check completion state
status.isCompleted;       // Action finished executing
status.isCompletedOk;     // Completed without errors
status.isCompletedFailed; // Completed with errors

// Access error information
status.originalError;     // Error thrown by before/reduce
status.wrappedError;      // Error after wrapError() processing

// Check method completion
status.hasFinishedMethodBefore;
status.hasFinishedMethodReduce;
status.hasFinishedMethodAfter;
```

You can also access status directly from the action instance:

```dart
var action = MyAction();
await dispatchAndWait(action);
print(action.status.isCompletedOk);
```

## The notify Parameter

Dispatch methods accept an optional `notify` parameter (default `true`) that controls whether widgets rebuild on state changes:

```dart
// Dispatch without triggering widget rebuilds
dispatch(MyAction(), notify: false);
```

## Summary Table

| Method | Returns | Waits? | Use Case |
|--------|---------|--------|----------|
| `dispatch()` | `void` | No | Fire and forget |
| `dispatchAndWait()` | `Future<ActionStatus>` | Yes | Need to know when done |
| `dispatchAll()` | `List<ReduxAction>` | No | Multiple parallel actions |
| `dispatchAndWaitAll()` | `Future<void>` | Yes | Wait for all parallel actions |
| `dispatchSync()` | `void` | N/A | Enforce sync execution |

## References

URLs from the documentation:
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/basics/sync-actions
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/advanced-actions/action-status
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
- https://asyncredux.com/flutter/miscellaneous/advanced-waiting
