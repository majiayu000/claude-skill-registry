---
name: asyncredux-selectors
description: Create and cache selectors for efficient state access. Covers writing selector functions, caching with `cache1` and `cache2`, the reselect pattern, and avoiding repeated computations in widgets.
---

## What Are Selectors?

Selectors are functions that extract specific data from the Redux store state. They provide three key benefits:

1. **Compute derived data** - Transform or filter state into the format your widget needs
2. **Abstract state structure** - Components don't depend on how the state is organized
3. **Enable caching (memoization)** - Avoid unnecessary recalculations

## The Problem: Repeated Computations

When displaying filtered or computed data, without selectors you might write:

```dart
// INEFFICIENT - filters the entire list on every access
state.users.where((user) => user.name.startsWith("A")).toList()[index].name;
```

This filtering operation runs every time the widget rebuilds, even when the data hasn't changed.

## Basic Selector Functions

Create a selector function that performs the computation once:

```dart
List<User> selectUsersStartingWith(AppState state, String text) {
  return state.users.where((user) => user.name.startsWith(text)).toList();
}
```

## Cached Selectors (Reselectors)

For expensive computations, wrap your selector with a cache function. AsyncRedux provides built-in caching utilities.

### Basic Caching Example

```dart
List<User> selectUsersStartingWith(AppState state, {required String text}) =>
    _selectUsersStartingWith(state)(text);

static final _selectUsersStartingWith = cache1state_1param(
  (AppState state) => (String text) =>
      state.users.where((user) => user.name.startsWith(text)).toList()
);
```

### Optimized Caching (State Subset)

For better performance, only depend on the specific state subset that matters:

```dart
List<User> selectUsersStartingWith(AppState state, {required String text}) =>
    _selectUsersStartingWith(state.users)(text);

static final _selectUsersStartingWith = cache1state_1param(
  (List<User> users) => (String text) =>
      users.where((user) => user.name.startsWith(text)).toList()
);
```

This version only recalculates when `state.users` changes, not when any part of `state` changes.

## Available Cache Functions

AsyncRedux provides these caching functions:

| Function | States | Parameters | Use Case |
|----------|--------|------------|----------|
| `cache1state` | 1 | 0 | Simple computed value from one state |
| `cache1state_1param` | 1 | 1 | Filtered/computed value with one param |
| `cache1state_2params` | 1 | 2 | Computation with two parameters |
| `cache1state_0params_x` | 1 | Many | Variable number of parameters |
| `cache2states` | 2 | 0 | Combines two state portions |
| `cache2states_1param` | 2 | 1 | Combines two states with one param |
| `cache2states_2params` | 2 | 2 | Combines two states with two params |
| `cache2states_0params_x` | 2 | Many | Two states, variable params |
| `cache3states` | 3 | 0 | Combines three state portions |
| `cache3states_0params_x` | 3 | Many | Three states, variable params |

The naming convention: `cache[N]state[s]_[M]param[s]` where N = number of states, M = number of parameters.

## Cache Characteristics

- **Multiple cached results** - Maintains separate caches for different parameter combinations
- **Weak-map storage** - Automatically discards cached data when states change or fall out of use
- **Memory efficient** - Won't hold obsolete information

## Action Selectors

Create selectors that actions can use via a dedicated class:

```dart
class ActionSelect {
  final AppState state;
  ActionSelect(this.state);

  List<Item> get items => state.items;
  Item get selectedItem => state.selectedItem;

  Item? findById(int id) =>
      state.items.firstWhereOrNull((item) => item.id == id);

  Item? searchByText(String text) =>
      state.items.firstWhereOrNull((item) => item.text.contains(text));

  int get selectedIndex => state.items.indexOf(state.selectedItem);
}
```

Add a getter in your base action:

```dart
abstract class AppAction extends ReduxAction<AppState> {
  ActionSelect get select => ActionSelect(state);
}
```

Usage in actions:

```dart
class LoadItemAction extends AppAction {
  final int itemId;
  LoadItemAction(this.itemId);

  @override
  AppState? reduce() {
    var item = select.findById(itemId);
    if (item == null) return null;
    return state.copy(selectedItem: item);
  }
}
```

## Widget Selectors

Create a `WidgetSelect` class for organized widget-level selectors:

```dart
class WidgetSelect {
  final BuildContext context;
  WidgetSelect(this.context);

  List<Item> get items => context.select((st) => st.items);
  Item get selectedItem => context.select((st) => st.selectedItem);

  Item? findById(int id) =>
      context.select((st) => st.items.firstWhereOrNull((item) => item.id == id));

  Item? searchByText(String text) =>
      context.select((st) => st.items.firstWhereOrNull((item) => item.text.contains(text)));

  int get selectedIndex =>
      context.select((st) => st.items.indexOf(st.selectedItem));
}
```

Add to your BuildContext extension:

```dart
extension BuildContextExtension on BuildContext {
  AppState get state => getState<AppState>();
  R select<R>(R Function(AppState state) selector) => getSelect<AppState, R>(selector);
  WidgetSelect get selector => WidgetSelect(this);
}
```

Usage in widgets:

```dart
Widget build(BuildContext context) {
  final item = context.selector.findById(42);
  return Text(item?.name ?? 'Not found');
}
```

## Reusing Action Selectors in Widgets

Widget selectors can leverage action selectors to avoid duplication:

```dart
class WidgetSelect {
  final BuildContext context;
  WidgetSelect(this.context);

  Item? findById(int id) =>
      context.select((st) => ActionSelect(st).findById(id));

  Item? searchByText(String text) =>
      context.select((st) => ActionSelect(st).searchByText(text));
}
```

## Important Guidelines

### Avoid context.state Inside Selectors

Never use `context.state` inside selector functions - this defeats selective rebuilding:

```dart
// WRONG - rebuilds on any state change
var items = context.select((state) => context.state.items.where(...));

// CORRECT - only rebuilds when items change
var items = context.select((state) => state.items.where(...));
```

### Never Nest context.select Calls

Nesting `context.select` causes errors:

```dart
// WRONG - will cause errors
var result = context.select((state) =>
  context.select((s) => s.items).where(...)  // Nested select!
);

// CORRECT
var items = context.select((state) => state.items);
var result = items.where(...).toList();
```

## Comparison with External Reselect Package

AsyncRedux's built-in caching differs from the external `reselect` package:

| Feature | AsyncRedux | reselect |
|---------|------------|----------|
| Results per selector | Multiple (different params) | One only |
| Memory on state change | Discards old cache | Retains indefinitely |

## Complete Example: Cached Filtered List

```dart
// Selector with caching
class UserSelectors {
  static List<User> usersStartingWith(AppState state, String prefix) =>
      _usersStartingWith(state.users)(prefix);

  static final _usersStartingWith = cache1state_1param(
    (List<User> users) => (String prefix) =>
        users.where((u) => u.name.startsWith(prefix)).toList()
  );

  static List<User> activeUsers(AppState state) =>
      _activeUsers(state.users);

  static final _activeUsers = cache1state(
    (List<User> users) => users.where((u) => u.isActive).toList()
  );
}

// Usage in widget
Widget build(BuildContext context) {
  var filtered = context.select(
    (state) => UserSelectors.usersStartingWith(state, 'A')
  );
  return ListView.builder(
    itemCount: filtered.length,
    itemBuilder: (_, i) => Text(filtered[i].name),
  );
}
```

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/miscellaneous/cached-selectors
- https://asyncredux.com/flutter/miscellaneous/widget-selectors
- https://asyncredux.com/flutter/advanced-actions/action-selectors
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/connector/store-connector
- https://asyncredux.com/flutter/connector/advanced-view-model
