---
name: asyncredux-state-design
description: Design immutable state classes following AsyncRedux best practices. Includes creating the AppState class with a `copy()` method, defining `initialState()`, composing nested state objects, and optionally using the fast_immutable_collections package for IList, ISet, and IMap.
---

# AsyncRedux State Design

## Core Principle: Immutability

State classes must be immutable—fields cannot be modified after creation. Instead of changing state directly, you create new instances. All fields should be marked `final`.

## Basic State Class Structure

```dart
class AppState {
  final String name;
  final int age;

  AppState({required this.name, required this.age});

  static AppState initialState() => AppState(name: "", age: 0);

  AppState copy({String? name, int? age}) =>
      AppState(
        name: name ?? this.name,
        age: age ?? this.age,
      );
}
```

### Key Components

1. **Final fields** - All state fields must be `final`
2. **`initialState()`** - Static factory method providing default values
3. **`copy()` method** - Creates modified instances without mutating original

## The copy() Method Pattern

The `copy()` method accepts optional parameters for each field. If a parameter is null, it keeps the existing value:

```dart
AppState copy({String? name, int? age}) =>
    AppState(
      name: name ?? this.name,
      age: age ?? this.age,
    );
```

You can also add convenience methods:

```dart
AppState withName(String name) => copy(name: name);
AppState withAge(int age) => copy(age: age);
```

## Nested/Composite State

For complex applications, compose multiple state classes within a single `AppState`:

```dart
class AppState {
  final TodoList todoList;
  final User user;
  final Settings settings;

  AppState({
    required this.todoList,
    required this.user,
    required this.settings,
  });

  static AppState initialState() => AppState(
    todoList: TodoList.initialState(),
    user: User.initialState(),
    settings: Settings.initialState(),
  );

  AppState copy({
    TodoList? todoList,
    User? user,
    Settings? settings,
  }) =>
      AppState(
        todoList: todoList ?? this.todoList,
        user: user ?? this.user,
        settings: settings ?? this.settings,
      );
}
```

Each nested class follows the same pattern:

```dart
class User {
  final String name;
  final String email;

  User({required this.name, required this.email});

  static User initialState() => User(name: "", email: "");

  User copy({String? name, String? email}) =>
      User(
        name: name ?? this.name,
        email: email ?? this.email,
      );
}
```

## Updating Nested State in Actions

```dart
class UpdateUserName extends ReduxAction<AppState> {
  final String name;
  UpdateUserName(this.name);

  @override
  AppState reduce() {
    var newUser = state.user.copy(name: name);
    return state.copy(user: newUser);
  }
}
```

## Using fast_immutable_collections

For lists, sets, and maps, use the `fast_immutable_collections` package (by the same author as AsyncRedux):

```yaml
dependencies:
  fast_immutable_collections: ^10.0.0
```

### IList Example

Use `Iterable` in constructors and copy methods, with `IList.orNull()` for conversion. This lets callers pass any iterable (List, Set, IList) without manual conversion:

```dart
import 'package:fast_immutable_collections/fast_immutable_collections.dart';

class AppState {
  final IList<Todo> todos;

  AppState({
    Iterable<Todo>? todos,
  }) : todos = IList.orNull(todos) ?? const IList.empty();

  static AppState initialState() => AppState();

  AppState copy({Iterable<Todo>? todos}) =>
      AppState(todos: IList.orNull(todos) ?? this.todos);

  // Convenience methods with business logic
  AppState addTodo(Todo todo) => copy(todos: todos.add(todo));
  AppState removeTodo(Todo todo) => copy(todos: todos.remove(todo));
  AppState toggleTodo(int index) => copy(
    todos: todos.replace(index, todos[index].copy(done: !todos[index].done)),
  );
}

// Flexible usage:
var state = AppState();                           // Empty list
var state = AppState(todos: [todo1, todo2]);      // List works
var state = AppState(todos: {todo1, todo2});      // Set works
var state = AppState(todos: existingIList);       // IList reused (no copy)
```

### IMap Example

Use `Map` in constructors and copy methods, with `IMap.orNull()` for conversion:

```dart
class AppState {
  final IMap<String, User> usersById;

  AppState({
    Map<String, User>? usersById,
  }) : usersById = IMap.orNull(usersById) ?? const IMap.empty();

  static AppState initialState() => AppState();

  AppState copy({Map<String, User>? usersById}) =>
      AppState(usersById: IMap.orNull(usersById) ?? this.usersById);

  AppState addUser(User user) => copy(usersById: usersById.add(user.id, user));
  AppState removeUser(String id) => copy(usersById: usersById.remove(id));
}
```

### ISet Example

Use `Iterable` in constructors and copy methods, with `ISet.orNull()` for conversion:

```dart
class AppState {
  final ISet<String> selectedIds;

  AppState({
    Iterable<String>? selectedIds,
  }) : selectedIds = ISet.orNull(selectedIds) ?? const ISet.empty();

  static AppState initialState() => AppState();

  AppState copy({Iterable<String>? selectedIds}) =>
      AppState(selectedIds: ISet.orNull(selectedIds) ?? this.selectedIds);

  AppState toggleSelection(String id) => copy(
    selectedIds: selectedIds.contains(id)
        ? selectedIds.remove(id)
        : selectedIds.add(id),
  );
}
```

## Events in State

For one-time UI interactions (scrolling, text field changes), use `Evt`:

```dart
class AppState {
  final Evt clearTextEvt;
  final Evt<String> changeTextEvt;

  AppState({
    required this.clearTextEvt,
    required this.changeTextEvt,
  });

  static AppState initialState() => AppState(
    clearTextEvt: Evt.spent(),
    changeTextEvt: Evt<String>.spent(),
  );

  AppState copy({
    Evt? clearTextEvt,
    Evt<String>? changeTextEvt,
  }) =>
      AppState(
        clearTextEvt: clearTextEvt ?? this.clearTextEvt,
        changeTextEvt: changeTextEvt ?? this.changeTextEvt,
      );
}
```

Events are initialized as "spent" and become active when replaced with new instances in actions.

## Business Logic in State Classes

AsyncRedux recommends placing business logic in state classes, not in actions or widgets:

```dart
class TodoList {
  final IList<Todo> items;

  TodoList({required this.items});

  // Business logic methods
  int get completedCount => items.where((t) => t.done).length;
  int get pendingCount => items.length - completedCount;
  double get completionRate => items.isEmpty ? 0 : completedCount / items.length;

  IList<Todo> get completed => items.where((t) => t.done).toIList();
  IList<Todo> get pending => items.where((t) => !t.done).toIList();

  TodoList addTodo(Todo todo) => TodoList(items: items.add(todo));
  TodoList removeTodo(Todo todo) => TodoList(items: items.remove(todo));
}
```

Actions become simple orchestrators:

```dart
class AddTodo extends ReduxAction<AppState> {
  final Todo todo;
  AddTodo(this.todo);

  @override
  AppState reduce() => state.copy(
    todoList: state.todoList.addTodo(todo),
  );
}
```

## State Access in Actions

Actions access state through getters:

- **`state`** - Current state (updates after each `await` in async actions)
- **`initialState`** - State when the action was first dispatched (never changes)

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    var originalValue = initialState.counter; // Preserved
    await someAsyncWork();
    var currentValue = state.counter; // May have changed
    return state.copy(counter: currentValue + 1);
  }
}
```

## Testing Benefits

Immutable state with pure methods makes unit testing straightforward:

```dart
void main() {
  test('addTodo adds item to list', () {
    var state = AppState.initialState();
    var todo = Todo(text: 'Test', done: false);

    var newState = state.addTodo(todo);

    expect(newState.todos.length, 1);
    expect(newState.todos.first.text, 'Test');
    expect(state.todos.length, 0); // Original unchanged
  });
}
```

## References

URLs from the documentation:
- https://asyncredux.com/flutter/basics/state
- https://asyncredux.com/flutter/basics/sync-actions
- https://asyncredux.com/flutter/basics/changing-state-is-optional
- https://asyncredux.com/flutter/basics/actions-and-reducers
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/events
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/miscellaneous/business-logic
- https://asyncredux.com/flutter/miscellaneous/persistence
- https://asyncredux.com/flutter/connector/store-connector
- https://asyncredux.com/flutter/testing/mocking
- https://asyncredux.com/flutter/intro
- https://asyncredux.com/flutter/about
