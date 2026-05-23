---
name: asyncredux-sync-actions
description: Creates AsyncRedux (Flutter) synchronous actions that update state immediately by implementing reduce() to return a new state. 
---

# AsyncRedux Sync Actions

## Basic Sync Action Structure

A synchronous action returns `AppState?` from its `reduce()` method. The action completes
immediately and state updates right away.

```dart
class Increment extends ReduxAction<AppState> {
  @override
  AppState? reduce() => state.copy(counter: state.counter + 1);
}
```

## Key Components

### Extending ReduxAction

Every action extends `ReduxAction<AppState>`:

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    // Return new state
  }
}
```

### The `state` Getter

Inside `reduce()`, access current state via the `state` getter:

```dart
class ToggleFlag extends ReduxAction<AppState> {
  @override
  AppState? reduce() => state.copy(flag: !state.flag);
}
```

### Passing Parameters via Constructor

Pass data to actions through constructor fields:

```dart
class SetName extends ReduxAction<AppState> {
  final String name;
  SetName(this.name);

  @override
  AppState? reduce() => state.copy(name: name);
}

class IncrementBy extends ReduxAction<AppState> {
  final int amount;
  IncrementBy({required this.amount});

  @override
  AppState? reduce() => state.copy(counter: state.counter + amount);
}
```

### Modifying Nested State

For nested state objects, create the new nested object first:

```dart
class UpdateUserName extends ReduxAction<AppState> {
  final String name;
  UpdateUserName(this.name);

  @override
  AppState? reduce() {
    var newUser = state.user.copy(name: name);
    return state.copy(user: newUser);
  }
}
```

## Dispatching Sync Actions

### From Widgets

Use context extensions:

```dart
// Fire and forget
context.dispatch(Increment());

// With parameters
context.dispatch(SetName('Alice'));
context.dispatch(IncrementBy(amount: 5));
```

### Immediate State Update

Sync actions update state immediately:

```dart
print(store.state.counter); // 2
store.dispatch(IncrementBy(amount: 3));
print(store.state.counter); // 5
```

### Guaranteed Sync with dispatchSync()

The `dispatchSync()` throws `StoreException` if the action is async. Otherwise, it
behaves exactly like `dispatch()`.

Use `dispatchSync()` only in the rare cases when you must ensure the action is synchronous
because you need the state to be applied right after the dispatch returns. 

```dart
context.dispatchSync(Increment());
```

### From Other Actions

Actions can dispatch other actions:

```dart
class ResetAndIncrement extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    dispatch(Reset());
    dispatch(Increment());
    return null; // This action itself doesn't change state
  }
}
```

## Returning Null (No State Change)

Return `null` when you don't need to change state:

```dart
class LogCurrentState extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    print('Current counter: ${state.counter}');
    return null; // No state change
  }
}
```

Conditional state changes:

```dart
class IncrementIfPositive extends ReduxAction<AppState> {
  final int amount;
  IncrementIfPositive(this.amount);

  @override
  AppState? reduce() {
    if (amount <= 0) return null;
    return state.copy(counter: state.counter + amount);
  }
}
```

## Action Simplification with Base Class

Create a base action class to reduce boilerplate:

```dart
// Define once
abstract class AppAction extends ReduxAction<AppState> {}

// Use everywhere
class Increment extends AppAction {
  @override
  AppState? reduce() => state.copy(counter: state.counter + 1);
}

class SetName extends AppAction {
  final String name;
  SetName(this.name);

  @override
  AppState? reduce() => state.copy(name: name);
}
```

You can add shared functionality to your base class:

```dart
abstract class AppAction extends ReduxAction<AppState> {
  // Shortcuts to state parts
  User get user => state.user;
  Settings get settings => state.settings;
}

class UpdateEmail extends AppAction {
  final String email;
  UpdateEmail(this.email);

  @override
  AppState? reduce() => state.copy(
    user: user.copy(email: email), // Uses shortcut
  );
}
```

## Return Type Warning

The `reduce()` method signature is `FutureOr<AppState?>`. For sync actions, always return
`AppState?` directly:

```dart
// CORRECT - Sync action
AppState? reduce() => state.copy(counter: state.counter + 1);

// WRONG - Don't return FutureOr directly
FutureOr<AppState?> reduce() => state.copy(counter: state.counter + 1);
```

If you return `FutureOr<AppState?>` directly, AsyncRedux cannot determine if the action is
sync or async and will throw a `StoreException`.

## Complete Example

```dart
// State
class AppState {
  final int counter;
  final String name;

  AppState({required this.counter, required this.name});

  static AppState initialState() => AppState(counter: 0, name: '');

  AppState copy({int? counter, String? name}) => AppState(
    counter: counter ?? this.counter,
    name: name ?? this.name,
  );
}

// Base action
abstract class AppAction extends ReduxAction<AppState> {}

// Sync actions
class Increment extends AppAction {
  @override
  AppState? reduce() => state.copy(counter: state.counter + 1);
}

class Decrement extends AppAction {
  @override
  AppState? reduce() => state.copy(counter: state.counter - 1);
}

class IncrementBy extends AppAction {
  final int amount;
  IncrementBy(this.amount);

  @override
  AppState? reduce() => state.copy(counter: state.counter + amount);
}

class SetName extends AppAction {
  final String name;
  SetName(this.name);

  @override
  AppState? reduce() => state.copy(name: name);
}

class Reset extends AppAction {
  @override
  AppState? reduce() => AppState.initialState();
}

// Usage in widget
ElevatedButton(
  onPressed: () => context.dispatch(IncrementBy(5)),
  child: Text('Add 5'),
)
```

## References

URLs from the documentation:

- https://asyncredux.com/flutter/basics/sync-actions
- https://asyncredux.com/flutter/basics/actions-and-reducers
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/action-simplification
- https://asyncredux.com/flutter/basics/changing-state-is-optional
