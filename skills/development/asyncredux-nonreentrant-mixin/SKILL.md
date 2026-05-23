---
name: asyncredux-nonreentrant-mixin
description: Add the NonReentrant mixin to prevent an action from dispatching while already in progress. Covers preventing duplicate form submissions, avoiding race conditions, and protecting long-running operations.
---

# NonReentrant Mixin

The `NonReentrant` mixin prevents concurrent execution of the same action type. When an action instance is already running, new dispatches of that same action are silently aborted.

## Basic Usage

Add the `NonReentrant` mixin to any action that should not run concurrently:

```dart
class SaveAction extends AppAction with NonReentrant {
  Future<AppState?> reduce() async {
    await http.put('http://myapi.com/save', body: 'data');
    return null;
  }
}
```

With this mixin:
- If the user clicks "Save" multiple times rapidly, only the first dispatch executes
- Subsequent dispatches while the first is running are silently aborted
- No duplicate API calls or race conditions occur

## How It Works

The `NonReentrant` mixin overrides the `abortDispatch` method. When `abortDispatch()` returns `true`, the action's `before()`, `reduce()`, and `after()` methods will not run, and the state stays unchanged.

By default, checks are based on the action's runtime type - multiple instances of the same action class cannot run simultaneously.

## Common Use Cases

1. **Preventing duplicate form submissions** - Stop users from accidentally submitting forms multiple times
2. **Protecting API calls** - Ensure save/update/delete operations don't fire concurrently
3. **Resource-intensive tasks** - Prevent expensive computations from running in parallel
4. **Avoiding race conditions** - Ensure sequential execution of operations that must not overlap

## Customization

### Allow Different Parameters to Run Concurrently

Override `nonReentrantKeyParams()` to allow actions with different parameters to run in parallel:

```dart
class SaveItemAction extends AppAction with NonReentrant {
  final String itemId;
  SaveItemAction(this.itemId);

  @override
  Object? nonReentrantKeyParams() => itemId;

  Future<AppState?> reduce() async {
    await saveItem(itemId);
    return null;
  }
}
```

With this customization:
- `SaveItemAction('A')` and `SaveItemAction('B')` can run concurrently
- Two `SaveItemAction('A')` dispatches will still block each other

### Share Keys Across Different Action Types

Override `computeNonReentrantKey()` to make different action classes block each other:

```dart
class SaveUserAction extends AppAction with NonReentrant {
  final String orderId;
  SaveUserAction(this.orderId);

  @override
  Object? computeNonReentrantKey() => orderId;

  Future<AppState?> reduce() async { ... }
}

class DeleteUserAction extends AppAction with NonReentrant {
  final String orderId;
  DeleteUserAction(this.orderId);

  @override
  Object? computeNonReentrantKey() => orderId;

  Future<AppState?> reduce() async { ... }
}
```

This prevents `SaveUserAction('123')` and `DeleteUserAction('123')` from running simultaneously - useful when different operations on the same resource must not overlap.

## Combining with Other Mixins

You can combine `NonReentrant` with other compatible mixins:

```dart
class LoadDataAction extends AppAction with CheckInternet, NonReentrant {
  Future<AppState?> reduce() async {
    final data = await fetchData();
    return state.copy(data: data);
  }
}
```

**Incompatible mixins:** `NonReentrant` cannot be combined with:
- `Throttle`
- `UnlimitedRetryCheckInternet`
- Most optimistic update mixins (check the compatibility matrix)

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/advanced-actions/control-mixins
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/aborting-the-dispatch
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/async-actions
