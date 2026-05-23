---
name: asyncredux-base-action
description: Create a custom base action class for your app. Covers adding getter shortcuts to state parts, adding selector methods, implementing shared wrapError logic, and establishing project-wide action conventions.
---

# Creating a Custom Base Action Class

Every AsyncRedux application should define an abstract base action class that all actions
extend. This provides a central place for:

- Convenient getter shortcuts to state parts
- Selector methods for common queries
- Shared error handling logic
- Type-safe environment access
- Project-wide conventions

## Basic Base Action Setup

Create an abstract class extending `ReduxAction<AppState>`.
The recomended name is `AppAction`, in file `app_action.dart`:

```dart
abstract class AppAction extends ReduxAction<AppState> {
  // All your actions will extend this class
}
```

Then extend `AppAction` instead of `ReduxAction<AppState>` in all your actions:

```dart
class IncrementCounter extends AppAction {
  @override
  AppState reduce() => state.copy(counter: state.counter + 1);
}
```

## Adding Getter Shortcuts to State Parts

When your state has nested objects, add getters to simplify access:

```dart
abstract class AppAction extends ReduxAction<AppState> {
  // Shortcuts to nested state parts
  User get user => state.user;
  Settings get settings => state.settings;
  IList<Todo> get todos => state.todos;
  Cart get cart => state.cart;
}
```

Now actions can write cleaner code:

```dart
class UpdateUserName extends AppAction {
  final String name;
  UpdateUserName(this.name);

  @override
  AppState reduce() {
    // Instead of: state.user.name
    // You can write: user.name
    return state.copy(user: user.copy(name: name));
  }
}
```

## Adding Selector Methods

For common data lookups, add selector methods directly to your base action:

```dart
abstract class AppAction extends ReduxAction<AppState> {
  // Getters for state parts
  User get user => state.user;
  IList<Item> get items => state.items;

  // Selector methods
  Item? findItemById(String id) =>
      items.firstWhereOrNull((item) => item.id == id);

  List<Item> get completedItems =>
      items.where((item) => item.isCompleted).toList();

  bool get isLoggedIn => user.isAuthenticated;
}
```

Actions can then use these selectors:

```dart
class MarkItemComplete extends AppAction {
  final String itemId;
  MarkItemComplete(this.itemId);

  @override
  AppState reduce() {
    final item = findItemById(itemId);
    if (item == null) return null; // No change

    return state.copy(
      items: items.replaceFirstWhere(
        (i) => i.id == itemId,
        item.copy(isCompleted: true),
      ),
    );
  }
}
```

### Using a Separate Selector Class

For most applications, it's better to use instead a dedicated selector class to keep the
base action clean:

```dart
class ActionSelect {
  final AppState state;
  ActionSelect(this.state);

  Item? findById(String id) =>
      state.items.firstWhereOrNull((item) => item.id == id);

  List<Item> get completed =>
      state.items.where((item) => item.isCompleted).toList();

  List<Item> get pending =>
      state.items.where((item) => !item.isCompleted).toList();
}

abstract class AppAction extends ReduxAction<AppState> {
  ActionSelect get select => ActionSelect(state);
}
```

These namespaces selectors under `select`, enabling IDE autocompletion:

```dart
class ProcessItem extends AppAction {
  final String itemId;
  ProcessItem(this.itemId);

  @override
  AppState reduce() {
    // IDE autocomplete shows: select.findById, select.completed, etc.
    final item = select.findById(itemId);
    // ...
  }
}
```

## Type-Safe Environment Access

For dependency injection, override the `env` getter in your base action:

```dart
class Environment {
  final ApiClient api;
  final AuthService auth;
  final AnalyticsService analytics;

  Environment({
    required this.api,
    required this.auth,
    required this.analytics,
  });
}

abstract class AppAction extends ReduxAction<AppState> {
  // Type-safe access to environment
  @override
  Environment get env => super.env as Environment;

  // Convenience getters for common services
  ApiClient get api => env.api;
  AuthService get auth => env.auth;
}
```

Actions can then use services directly:

```dart
class FetchUserProfile extends AppAction {
  @override
  Future<AppState?> reduce() async {
    // Uses the api getter from base action
    final profile = await api.getUserProfile();
    return state.copy(user: profile);
  }
}
```

## References

URLs from the documentation:

- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/advanced-actions/action-selectors
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/advanced-actions/wrapping-the-reducer
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/aborting-the-dispatch
- https://asyncredux.com/flutter/basics/actions-and-reducers
- https://asyncredux.com/flutter/basics/state
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/miscellaneous/business-logic
- https://asyncredux.com/flutter/miscellaneous/dependency-injection
