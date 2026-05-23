---
name: asyncredux-actions-no-state-change
description: Creates AsyncRedux (Flutter) actions that return null from reduce() to not change the state. Such actions can still do side effects, dispatch other actions, or do nothing. 
---

# Actions That Don't Change State

In AsyncRedux, returning a new state from reducers is **optional**. When you don't need to
modify the application state, return `null` to keep the current state unchanged.

## Basic Pattern

Return `null` from `reduce()` when no state modification is needed:

```dart
class MyAction extends ReduxAction<AppState> {
  AppState? reduce() {
    // Perform side effects here
    return null; // State remains unchanged
  }
}
```

## Conditional State Updates

Only update state when certain conditions are met:

```dart
class GetAmount extends ReduxAction<AppState> {
  Future<AppState?> reduce() async {
    int amount = await getAmount();
    if (amount == 0)
      return null; // No change needed
    else
      return state.copy(counter: state.counter + amount);
  }
}
```

## Coordinating Other Actions

Actions that dispatch other actions but don't modify state directly:

```dart
class InitAction extends ReduxAction<AppState> {
  AppState? reduce() {
    dispatch(ReadDatabaseAction());
    dispatch(StartTimersAction());
    dispatch(TurnOnListenersAction());
    return null; // This action doesn't change state itself
  }
}
```

## Triggering External Services

Call external services without modifying app state:

```dart
class SendNotification extends ReduxAction<AppState> {
  final String message;
  SendNotification(this.message);

  Future<AppState?> reduce() async {
    await notificationService.send(message);
    return null;
  }
}
```

## Navigation Actions

Trigger navigation as a side effect:

```dart
class GoToSettings extends ReduxAction<AppState> {
  AppState? reduce() {
    dispatch(NavigateAction.pushNamed('/settings'));
    return null;
  }
}
```

## Key Points

1. Actions that do return a new state can **also** do side effects and dispatch other actions.
2. **Return type matters**: Use `AppState?` for sync, `Future<AppState?>` for async
3. **Null means no change**: The store keeps its current state

## References

URLs from the documentation:

- https://asyncredux.com/flutter/basics/changing-state-is-optional
- https://asyncredux.com/flutter/basics/actions-and-reducers
- https://asyncredux.com/flutter/basics/sync-actions
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
