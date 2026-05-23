---
name: asyncredux-debugging
description: Debug AsyncRedux applications effectively. Covers printing state with store.state, checking actionsInProgress(), using ConsoleActionObserver, StateObserver for state change tracking, and tracking dispatchCount/reduceCount.
---

# Debugging AsyncRedux Applications

AsyncRedux provides several tools for debugging and monitoring your application's state, actions, and behavior during development.

## Inspecting Store State

Access the current state directly from the store:

```dart
// Direct state access
print(store.state);

// Access specific parts
print(store.state.user.name);
print(store.state.cart.items);
```

## Tracking Actions in Progress

Use `actionsInProgress()` to see which actions are currently being processed:

```dart
// Returns an unmodifiable Set of actions currently running
Set<ReduxAction<AppState>> inProgress = store.actionsInProgress();

// Check if any actions are running
if (inProgress.isEmpty) {
  print('No actions in progress');
} else {
  for (var action in inProgress) {
    print('Running: ${action.runtimeType}');
  }
}

// Get a copy of actions in progress
Set<ReduxAction<AppState>> copy = store.copyActionsInProgress();

// Check if specific actions match
bool matches = store.actionsInProgressEqualTo(expectedSet);
```

## Dispatch and Reduce Counts

Track how many actions have been dispatched and how many state reductions have occurred:

```dart
// Total actions dispatched since store creation
print('Dispatch count: ${store.dispatchCount}');

// Total state reductions performed
print('Reduce count: ${store.reduceCount}');
```

These counters are useful for:
- Verifying actions dispatched during tests
- Detecting unexpected dispatches
- Performance monitoring

## Console Action Observer

The built-in `ConsoleActionObserver` prints dispatched actions to the console with color formatting:

```dart
var store = Store<AppState>(
  initialState: AppState.initialState(),
  // Only enable in debug mode
  actionObservers: kReleaseMode ? null : [ConsoleActionObserver()],
);
```

Console output example:
```
I/flutter (15304): | Action MyAction
I/flutter (15304): | Action LoadUserAction(user32)
```

Actions appear in yellow (default) or green (for `WaitAction` and `NavigateAction`).

### Customizing Action Output

Override `toString()` in your actions to display additional information:

```dart
class LoginAction extends AppAction {
  final String username;
  LoginAction(this.username);

  @override
  Future<AppState?> reduce() async {
    // ...
  }

  @override
  String toString() => 'LoginAction(username: $username)';
}
```

### Custom Color Scheme

Customize the color scheme by modifying the static `color` callback:

```dart
ConsoleActionObserver.color = (action) {
  if (action is ErrorAction) return ConsoleActionObserver.red;
  if (action is NetworkAction) return ConsoleActionObserver.blue;
  return ConsoleActionObserver.yellow;
};
```

Available colors: `white`, `red`, `blue`, `yellow`, `green`, `grey`, `dark`.

## StateObserver for State Change Logging

Create a `StateObserver` to log state changes:

```dart
class DebugStateObserver implements StateObserver<AppState> {
  @override
  void observe(
    ReduxAction<AppState> action,
    AppState prevState,
    AppState newState,
    Object? error,
    int dispatchCount,
  ) {
    final changed = !identical(prevState, newState);

    print('--- Action #$dispatchCount: ${action.runtimeType} ---');
    print('State changed: $changed');

    if (changed) {
      // Log specific state changes
      if (prevState.user != newState.user) {
        print('  User changed: ${prevState.user} -> ${newState.user}');
      }
      if (prevState.counter != newState.counter) {
        print('  Counter changed: ${prevState.counter} -> ${newState.counter}');
      }
    }

    if (error != null) {
      print('  Error: $error');
    }
  }
}

// Configure store
var store = Store<AppState>(
  initialState: AppState.initialState(),
  stateObservers: kDebugMode ? [DebugStateObserver()] : null,
);
```

### Detecting State Changes

Use `identical()` to check if state actually changed:

```dart
bool stateChanged = !identical(prevState, newState);
```

This is efficient because AsyncRedux uses immutable state - if the reference is the same, no change occurred.

## Custom ActionObserver for Detailed Logging

Create an `ActionObserver` for detailed dispatch tracking:

```dart
class DetailedActionObserver implements ActionObserver<AppState> {
  final Map<ReduxAction, DateTime> _startTimes = {};

  @override
  void observe(
    ReduxAction<AppState> action,
    int dispatchCount, {
    required bool ini,
  }) {
    if (ini) {
      // Action started
      _startTimes[action] = DateTime.now();
      print('[START #$dispatchCount] ${action.runtimeType}');
    } else {
      // Action finished
      final startTime = _startTimes.remove(action);
      if (startTime != null) {
        final duration = DateTime.now().difference(startTime);
        print('[END #$dispatchCount] ${action.runtimeType} (${duration.inMilliseconds}ms)');
      } else {
        print('[END #$dispatchCount] ${action.runtimeType}');
      }
    }
  }
}
```

## Debugging Widget Rebuilds

Use `ModelObserver` with `DefaultModelObserver` to track which widgets rebuild:

```dart
var store = Store<AppState>(
  initialState: AppState.initialState(),
  modelObserver: DefaultModelObserver(),
);
```

Output format:
```
Model D:1 R:1 = Rebuild:true, Connector:MyWidgetConnector, Model:MyViewModel{data}.
Model D:2 R:2 = Rebuild:false, Connector:MyWidgetConnector, Model:MyViewModel{data}.
```

- `D`: Dispatch count
- `R`: Rebuild count
- `Rebuild`: Whether widget actually rebuilt
- `Connector`: The StoreConnector type
- `Model`: ViewModel with state summary

Enable detailed output by passing `debug: this` to StoreConnector:

```dart
StoreConnector<AppState, MyViewModel>(
  debug: this, // Enables connector name in output
  converter: (store) => MyViewModel.fromStore(store),
  builder: (context, vm) => MyWidget(vm),
)
```

## Checking Action Status in Widgets

Use context extensions to check action states:

```dart
Widget build(BuildContext context) {
  // Check if action is currently running
  if (context.isWaiting(LoadDataAction)) {
    return CircularProgressIndicator();
  }

  // Check if action failed
  if (context.isFailed(LoadDataAction)) {
    var exception = context.exceptionFor(LoadDataAction);
    return Text('Error: ${exception?.message}');
  }

  return Text('Data: ${context.state.data}');
}
```

## Waiting for Conditions in Tests

Use store wait methods for test debugging:

```dart
// Wait until state meets a condition
await store.waitCondition((state) => state.isLoaded);

// Wait for specific action types to complete
await store.waitAllActionTypes([LoadUserAction, LoadSettingsAction]);

// Wait for all actions to complete (empty list = wait for all)
await store.waitAllActions([]);

// Wait for action condition with access to actions in progress
await store.waitActionCondition((actionsInProgress, triggerAction) {
  return actionsInProgress.isEmpty;
});
```

## Complete Debug Setup Example

```dart
void main() {
  final store = Store<AppState>(
    initialState: AppState.initialState(),
    // Action logging (debug only)
    actionObservers: kDebugMode
        ? [ConsoleActionObserver(), DetailedActionObserver()]
        : null,
    // State change logging (debug only)
    stateObservers: kDebugMode
        ? [DebugStateObserver()]
        : null,
    // Widget rebuild tracking (debug only)
    modelObserver: kDebugMode ? DefaultModelObserver() : null,
    // Error observer (always enabled)
    errorObserver: MyErrorObserver(),
  );

  // Debug print initial state
  if (kDebugMode) {
    print('Initial state: ${store.state}');
    print('Dispatch count: ${store.dispatchCount}');
  }

  runApp(StoreProvider<AppState>(
    store: store,
    child: MyApp(),
  ));
}
```

## Debugging Tips

1. **Print state in actions**: Use `print(state)` in your reducer to see state at that moment
2. **Check initialState**: Access `action.initialState` to see state when action was dispatched (vs current `state`)
3. **Use action status**: Check `action.status.isCompletedOk` or `action.status.originalError` after dispatch
4. **Conditional logging**: Use `kDebugMode` from `package:flutter/foundation.dart` to disable in production
5. **Override toString**: Implement `toString()` on actions and state classes for better debug output

## References

URLs from the documentation:
- https://asyncredux.com/flutter/miscellaneous/logging
- https://asyncredux.com/flutter/miscellaneous/metrics
- https://asyncredux.com/flutter/miscellaneous/observing-rebuilds
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/wait-fail-succeed
- https://asyncredux.com/flutter/advanced-actions/action-status
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
