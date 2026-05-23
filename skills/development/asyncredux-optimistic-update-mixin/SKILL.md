---
name: asyncredux-optimistic-update-mixin
description: Add the OptimisticUpdate mixin for instant UI feedback before server confirmation. Covers immediate state changes, automatic rollback on failure, and optionally notifying users of rollback.
---

# Optimistic Update Mixins

AsyncRedux provides three optimistic update mixins for different scenarios:

| Mixin | Use Case |
|-------|----------|
| `OptimisticCommand` | One-time operations (create, delete, submit) with rollback |
| `OptimisticSync` | Rapid toggling/interactions with coalescing |
| `OptimisticSyncWithPush` | Real-time server push scenarios with revision tracking |

## OptimisticCommand

Use for one-time server operations where immediate UI feedback matters: creating todos, deleting items, submitting forms, or processing payments.

### Basic Example

Without optimistic updates (user waits for server):

```dart
class SaveTodo extends AppAction {
  final Todo newTodo;
  SaveTodo(this.newTodo);

  Future<AppState?> reduce() async {
    await saveTodo(newTodo);
    var reloadedList = await loadTodoList();
    return state.copy(todoList: reloadedList);
  }
}
```

With OptimisticCommand (instant UI feedback):

```dart
class SaveTodo extends AppAction with OptimisticCommand {
  final Todo newTodo;
  SaveTodo(this.newTodo);

  // Value to apply immediately to UI
  Object? optimisticValue() => newTodo;

  // Extract current value from state (for rollback comparison)
  Object? getValueFromState(AppState state)
    => state.todoList.getById(newTodo.id);

  // Apply value to state and return new state
  AppState applyValueToState(AppState state, Object? value)
    => state.copy(todoList: state.todoList.add(value as Todo));

  // Send to server (retries if using Retry mixin)
  Future<Object?> sendCommandToServer(Object? value) async
    => await saveTodo(newTodo);

  // Optional: reload from server on error
  Future<Object?> reloadFromServer() async
    => await loadTodoList();
}
```

### How Rollback Works

If `sendCommandToServer` fails, the mixin automatically rolls back only if the current state still matches the optimistic value. This avoids undoing newer changes made while the request was in flight.

Override these methods to customize rollback:

```dart
// Determine whether to restore previous state
bool shouldRollback() => true;

// Specify exact state to restore
AppState? rollbackState() => previousState;
```

### Non-Reentrant by Default

OptimisticCommand prevents concurrent execution of the same action. Use `nonReentrantKeyParams()` to allow parallel operations on different items:

```dart
class SaveTodo extends AppAction with OptimisticCommand {
  final String itemId;
  SaveTodo(this.itemId);

  // Allow SaveTodo('A') and SaveTodo('B') to run simultaneously
  // but prevent two SaveTodo('A') from running together
  Object? nonReentrantKeyParams() => itemId;

  // ... rest of implementation
}
```

Check if action is in progress in UI:

```dart
if (context.isWaiting(SaveTodo)) {
  return CircularProgressIndicator();
}
```

### Combining with Other Mixins

- **With Retry**: Only `sendCommandToServer` retries; optimistic UI remains stable
- **With CheckInternet**: No optimistic state applied when offline

## OptimisticSync

Use for rapid user interactions (toggling likes, switches, sliders) where only the final value matters and intermediate states can be discarded.

### Toggle Example

```dart
class ToggleLike extends AppAction with OptimisticSync<AppState, bool> {
  final String itemId;
  ToggleLike(this.itemId);

  // Allow concurrent operations on different items
  Object? optimisticSyncKeyParams() => itemId;

  // Value to apply optimistically (toggle current value)
  bool valueToApply() => !state.items[itemId].liked;

  // Apply optimistic change to state
  AppState applyOptimisticValueToState(AppState state, bool isLiked)
    => state.copy(items: state.items.setLiked(itemId, isLiked));

  // Extract current value from state
  bool getValueFromState(AppState state) => state.items[itemId].liked;

  // Send to server
  Future<Object?> sendValueToServer(Object? value) async
    => await api.setLiked(itemId, value);

  // Optional: Apply server response to state
  AppState? applyServerResponseToState(AppState state, Object serverResponse)
    => state.copy(items: state.items.setLiked(itemId, serverResponse as bool));

  // Optional: Handle completion/errors
  Future<AppState?> onFinish(Object? error) async {
    if (error != null) {
      // Reload from server on failure
      var reloaded = await api.getItem(itemId);
      return state.copy(items: state.items.update(itemId, reloaded));
    }
    return null;
  }
}
```

### How Coalescing Works

Multiple rapid changes are merged into minimal server requests:

1. User taps like button 5 times quickly
2. UI updates instantly each time (toggle, toggle, toggle...)
3. Only **one** server request sends the final state
4. If state changes during in-flight request, a follow-up request sends the new final value

## OptimisticSyncWithPush

Use when your app receives real-time server updates (WebSockets, Firebase) across multiple devices modifying shared data.

### Key Differences from OptimisticSync

- Each local dispatch increments a `localRevision` counter
- Server pushes do NOT increment `localRevision`
- Follow-up logic compares revisions instead of just values
- Stale pushes are automatically ignored

### Implementation

```dart
class ToggleLike extends AppAction with OptimisticSyncWithPush<AppState, bool> {
  final String itemId;
  ToggleLike(this.itemId);

  Object? optimisticSyncKeyParams() => itemId;

  bool valueToApply() => !state.items[itemId].liked;

  AppState applyOptimisticValueToState(AppState state, bool isLiked)
    => state.copy(items: state.items.setLiked(itemId, isLiked));

  bool getValueFromState(AppState state) => state.items[itemId].liked;

  // Read server revision from state
  int? getServerRevisionFromState(Object? key)
    => state.items[key as String].serverRevision;

  AppState? applyServerResponseToState(AppState state, Object serverResponse)
    => state.copy(items: state.items.setLiked(itemId, serverResponse as bool));

  Future<Object?> sendValueToServer(Object? value) async {
    // Get local revision BEFORE await
    int localRev = localRevision();

    var response = await api.setLiked(itemId, value, localRev: localRev);

    // Record server's revision after response
    informServerRevision(response.serverRev);

    return response.liked;
  }
}
```

### ServerPush Mixin

Handle incoming server pushes with automatic stale detection:

```dart
class PushLikeUpdate extends AppAction with ServerPush<AppState> {
  final String itemId;
  final bool liked;
  final int serverRev;

  PushLikeUpdate({
    required this.itemId,
    required this.liked,
    required this.serverRev,
  });

  // Link to corresponding OptimisticSyncWithPush action
  Type associatedAction() => ToggleLike;

  Object? optimisticSyncKeyParams() => itemId;

  int serverRevision() => serverRev;

  int? getServerRevisionFromState(Object? key)
    => state.items[key as String].serverRevision;

  AppState? applyServerPushToState(AppState state, Object? key, int serverRevision)
    => state.copy(
         items: state.items.update(
           key as String,
           (item) => item.copy(liked: liked, serverRevision: serverRevision),
         ),
       );
}
```

If incoming `serverRevision` ≤ current known revision, the push is automatically ignored. This prevents older server states from overwriting newer ones.

### Data Model for Revision Tracking

Store server revisions in your data model:

```dart
class Item {
  final bool liked;
  final int? serverRevision;

  Item({required this.liked, this.serverRevision});

  Item copy({bool? liked, int? serverRevision}) => Item(
    liked: liked ?? this.liked,
    serverRevision: serverRevision ?? this.serverRevision,
  );
}
```

## Notifying Users of Rollback

To notify users when a rollback occurs, use `UserException` in your error handling:

```dart
class SaveTodo extends AppAction with OptimisticCommand {
  // ... required methods ...

  Future<Object?> sendCommandToServer(Object? value) async {
    try {
      return await saveTodo(newTodo);
    } catch (e) {
      // Throw UserException to show dialog after rollback
      throw UserException('Failed to save. Your change was reverted.').addCause(e);
    }
  }
}
```

Or use `onFinish` with OptimisticSync:

```dart
Future<AppState?> onFinish(Object? error) async {
  if (error != null) {
    // Dispatch a notification action
    dispatch(UserExceptionAction('Failed to update. Reverting...'));

    // Reload correct state from server
    var reloaded = await api.getItem(itemId);
    return state.copy(items: state.items.update(itemId, reloaded));
  }
  return null;
}
```

## Choosing the Right Mixin

| Scenario | Mixin |
|----------|-------|
| Create/delete/submit operations | `OptimisticCommand` |
| Toggle switches, like buttons | `OptimisticSync` |
| Sliders, rapid input changes | `OptimisticSync` |
| Multi-device with real-time sync | `OptimisticSyncWithPush` + `ServerPush` |

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/advanced-actions/optimistic-mixins
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/advanced-actions/control-mixins
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/failed-actions
