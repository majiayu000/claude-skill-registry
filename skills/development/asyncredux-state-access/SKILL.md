---
name: asyncredux-state-access
description: Access store state in widgets using `context.state`, `context.select()`, and `context.read()`. Covers when to use each method, setting up BuildContext extensions, and optimizing widget rebuilds with selective state access.
---

## BuildContext Extension Setup

To access your application state in widgets, first define a `BuildContext` extension. Add this to your project (typically in a shared file that all widgets can import):

```dart
extension BuildContextExtension on BuildContext {
  AppState get state => getState<AppState>();
  AppState read() => getRead<AppState>();
  R select<R>(R Function(AppState state) selector) => getSelect<AppState, R>(selector);
  R? event<R>(Evt<R> Function(AppState state) selector) => getEvent<AppState, R>(selector);
}
```

Replace `AppState` with your actual state class name.

## The Three State Access Methods

### context.state

Grants access to the entire state object. All widgets that use `context.state` will automatically rebuild whenever the store state changes (any part of it).

```dart
Widget build(BuildContext context) {
  return Text('Counter: ${context.state.counter}');
}
```

### context.select()

Retrieves only specific state portions. This is more efficient as it only rebuilds the widget when the selected part of the state changes.

```dart
Widget build(BuildContext context) {
  var counter = context.select((state) => state.counter);
  return Text('Counter: $counter');
}
```

### context.read()

Retrieves state without triggering rebuilds. Use this in event handlers, `initState`, or anywhere you need to read state once without subscribing to changes.

```dart
void _onButtonPressed() {
  var currentCount = context.read().counter;
  print('Current count is $currentCount');
}
```

## When to Use Each Method

| Method | Use In | Triggers Rebuilds? | Best For |
|--------|--------|-------------------|----------|
| `context.state` | `build` method | Yes, on any state change | Simple widgets or when you need many state properties |
| `context.select()` | `build` method | Only when selected part changes | Performance-sensitive widgets |
| `context.read()` | `initState`, event handlers, callbacks | No | One-time reads, button handlers |

## Accessing Multiple State Properties

When you need several pieces of state, you have two options:

**Option 1: Multiple select calls**

```dart
Widget build(BuildContext context) {
  var name = context.select((state) => state.user.name);
  var email = context.select((state) => state.user.email);
  var itemCount = context.select((state) => state.items.length);
  // Widget rebuilds only if name, email, or itemCount changes
  return Text('$name ($email) - $itemCount items');
}
```

**Option 2: Dart records for combined selection**

```dart
Widget build(BuildContext context) {
  var (name, email) = context.select((state) => (state.user.name, state.user.email));
  return Text('$name ($email)');
}
```

## Additional Context Methods for Action States

Beyond state access, the context extension provides methods for tracking async action progress:

```dart
Widget build(BuildContext context) {
  // Check if an action is currently running
  if (context.isWaiting(LoadDataAction)) {
    return CircularProgressIndicator();
  }

  // Check if an action failed
  if (context.isFailed(LoadDataAction)) {
    var exception = context.exceptionFor(LoadDataAction);
    return Text('Error: ${exception?.message}');
  }

  // Show the data
  return Text('Data: ${context.state.data}');
}
```

Available methods:
- `context.isWaiting(ActionType)` - Returns true if the action is in progress
- `context.isFailed(ActionType)` - Returns true if the action recently failed
- `context.exceptionFor(ActionType)` - Gets the exception from a failed action
- `context.clearExceptionFor(ActionType)` - Manually clears the stored exception

## Widget Selectors Pattern

For complex selection logic, create a `WidgetSelect` class to organize reusable selectors:

```dart
class WidgetSelect {
  final BuildContext context;
  WidgetSelect(this.context);

  // Getter shortcuts
  List<Item> get items => context.select((state) => state.items);
  User get currentUser => context.select((state) => state.user);

  // Custom finder methods
  Item? findById(int id) => context.select(
    (state) => state.items.firstWhereOrNull((item) => item.id == id)
  );

  List<Item> searchByText(String text) => context.select(
    (state) => state.items.where((item) => item.name.contains(text)).toList()
  );
}
```

Add it to your BuildContext extension:

```dart
extension BuildContextExtension on BuildContext {
  AppState get state => getState<AppState>();
  // ... other methods ...
  WidgetSelect get selector => WidgetSelect(this);
}
```

Usage in widgets:

```dart
Widget build(BuildContext context) {
  var user = context.selector.currentUser;
  var item = context.selector.findById(42);
  return Text('${user.name}: ${item?.name}');
}
```

## Important Guidelines

### Avoid context.state inside selectors

Never use `context.state` inside your selector functions. This defeats the purpose of selective rebuilding:

```dart
// WRONG - rebuilds on any state change
var items = context.select((state) => context.state.items.where(...));

// CORRECT - only rebuilds when items change
var items = context.select((state) => state.items.where(...));
```

### Never nest context.select calls

Nesting `context.select` causes errors. Always apply selection at the top level:

```dart
// WRONG - will cause errors
var result = context.select((state) =>
  context.select((s) => s.items).where(...) // Nested select!
);

// CORRECT
var items = context.select((state) => state.items);
var result = items.where(...);
```

## Debugging Rebuilds

To observe when widgets rebuild (useful for performance debugging), use a `ModelObserver`:

```dart
var store = Store<AppState>(
  initialState: AppState.initialState(),
  modelObserver: DefaultModelObserver(),
);
```

The `DefaultModelObserver` logs console output showing:
- Whether a rebuild occurred
- Which connector/widget triggered it
- The view model state

Example output:
```
Model D:1 R:1 = Rebuild:true, Connector:MyWidgetConnector, Model:MyViewModel{counter: 5}
```

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/miscellaneous/widget-selectors
- https://asyncredux.com/flutter/miscellaneous/observing-rebuilds
- https://asyncredux.com/flutter/miscellaneous/cached-selectors
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/advanced-actions/action-selectors
- https://asyncredux.com/flutter/connector/store-connector
- https://asyncredux.com/flutter/intro
- https://asyncredux.com/flutter/basics/wait-fail-succeed
