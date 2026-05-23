---
name: asyncredux-before-after
description: Implement action lifecycle methods `before()` and `after()`. Covers running precondition checks, showing/hiding modal barriers, cleanup logic in `after()`, and understanding that `after()` always runs (like a finally block).
---

# AsyncRedux Before and After Methods

## Action Lifecycle Overview

Every `ReduxAction` has three lifecycle methods that execute in order:

1. `before()` - Runs first, before the reducer
2. `reduce()` - The main reducer (required)
3. `after()` - Runs last, always executes

Only `reduce()` is required. The `before()` and `after()` methods are optional hooks for managing side effects.

## The before() Method

The `before()` method executes before the reducer runs. It can be synchronous or asynchronous.

### Synchronous before()

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  void before() {
    // Runs synchronously before reduce()
    print('Action starting');
  }

  @override
  AppState? reduce() {
    return state.copy(counter: state.counter + 1);
  }
}
```

### Asynchronous before()

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  Future<void> before() async {
    // Runs asynchronously before reduce()
    await validatePermissions();
  }

  @override
  Future<AppState?> reduce() async {
    final data = await fetchData();
    return state.copy(data: data);
  }
}
```

### Precondition Checks in before()

If `before()` throws an error, `reduce()` will NOT run. This makes it ideal for validation:

```dart
class FetchUserData extends ReduxAction<AppState> {
  @override
  Future<void> before() async {
    if (!await hasInternetConnection()) {
      throw UserException('No internet connection');
    }
  }

  @override
  Future<AppState?> reduce() async {
    // Only runs if before() completed without error
    final user = await api.fetchUser();
    return state.copy(user: user);
  }
}
```

### Common before() Use Cases

- Validate preconditions (authentication, permissions)
- Check network connectivity
- Show loading indicators or modal barriers
- Log action start for analytics
- Dispatch prerequisite actions

## The after() Method

The `after()` method executes after the reducer completes. Its key property: **it always runs, even if `before()` or `reduce()` throws an error**. This makes it similar to a `finally` block.

### Basic after()

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    return state.copy(counter: state.counter + 1);
  }

  @override
  void after() {
    // Always runs, regardless of success or failure
    print('Action completed');
  }
}
```

### Guaranteed Cleanup

Because `after()` always runs, it's perfect for cleanup operations:

```dart
class SaveDocument extends ReduxAction<AppState> {
  @override
  Future<void> before() async {
    dispatch(ShowSavingIndicatorAction(true));
  }

  @override
  Future<AppState?> reduce() async {
    await api.saveDocument(state.document);
    return state.copy(lastSaved: DateTime.now());
  }

  @override
  void after() {
    // Hides indicator even if save fails
    dispatch(ShowSavingIndicatorAction(false));
  }
}
```

### Important: Never Throw from after()

The `after()` method should never throw errors. Any exception thrown from `after()` will appear asynchronously in the console and cannot be caught normally:

```dart
// WRONG - Don't throw in after()
@override
void after() {
  if (someCondition) {
    throw Exception('This will cause problems');
  }
}

// CORRECT - Handle errors gracefully
@override
void after() {
  try {
    cleanup();
  } catch (e) {
    // Log but don't throw
    logger.error('Cleanup failed: $e');
  }
}
```

### Common after() Use Cases

- Hide loading indicators or modal barriers
- Close database connections or file handles
- Release temporary resources
- Log action completion for analytics
- Dispatch follow-up actions

## Modal Barrier Pattern

A common pattern is showing a modal barrier (blocking overlay) during async operations:

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    String description = await read(Uri.http("numbersapi.com", "${state.counter}"));
    return state.copy(description: description);
  }

  @override
  void before() => dispatch(BarrierAction(true));

  @override
  void after() => dispatch(BarrierAction(false));
}
```

The `BarrierAction` would update state to show/hide a loading overlay:

```dart
class BarrierAction extends ReduxAction<AppState> {
  final bool show;
  BarrierAction(this.show);

  @override
  AppState reduce() => state.copy(showBarrier: show);
}
```

## Creating Reusable Mixins

For patterns you use repeatedly, create a mixin:

```dart
mixin Barrier on ReduxAction<AppState> {
  @override
  void before() {
    super.before();
    dispatch(BarrierAction(true));
  }

  @override
  void after() {
    dispatch(BarrierAction(false));
    super.after();
  }
}
```

Then apply it to any action:

```dart
class FetchData extends ReduxAction<AppState> with Barrier {
  @override
  Future<AppState?> reduce() async {
    // Barrier shown automatically before this runs
    final data = await api.fetchData();
    return state.copy(data: data);
    // Barrier hidden automatically after (even on error)
  }
}
```

### Multiple Mixins

You can combine multiple mixins:

```dart
class ImportantAction extends ReduxAction<AppState> with Barrier, NonReentrant {
  @override
  Future<AppState?> reduce() async {
    // Has both modal barrier AND prevents duplicate dispatches
    return state;
  }
}
```

## Error Handling Flow

Understanding how errors interact with the lifecycle:

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  Future<void> before() async {
    // If this throws, reduce() is skipped, after() still runs
  }

  @override
  Future<AppState?> reduce() async {
    // If this throws, state is not changed, after() still runs
  }

  @override
  void after() {
    // ALWAYS runs regardless of errors above
  }
}
```

### Checking What Completed

Use `ActionStatus` to determine which methods finished:

```dart
var status = await dispatchAndWait(MyAction());

if (status.hasFinishedMethodBefore) {
  print('before() completed');
}

if (status.hasFinishedMethodReduce) {
  print('reduce() completed');
}

if (status.hasFinishedMethodAfter) {
  print('after() completed');
}

if (status.isCompletedOk) {
  print('Both before() and reduce() completed without errors');
}

if (status.isCompletedFailed) {
  print('Error: ${status.originalError}');
}
```

## Relationship with abortDispatch()

If `abortDispatch()` returns `true`, none of the lifecycle methods run:

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  bool abortDispatch() => state.user == null;

  @override
  void before() {
    // Skipped if abortDispatch() returns true
  }

  @override
  AppState? reduce() {
    // Skipped if abortDispatch() returns true
  }

  @override
  void after() {
    // Skipped if abortDispatch() returns true
  }
}
```

## Complete Example

```dart
class SubmitForm extends ReduxAction<AppState> {
  final String formData;
  SubmitForm(this.formData);

  @override
  Future<void> before() async {
    // Validate preconditions
    if (state.user == null) {
      throw UserException('Please log in first');
    }

    if (!await checkInternetConnection()) {
      throw UserException('No internet connection');
    }

    // Show loading state
    dispatch(SetSubmittingAction(true));
  }

  @override
  Future<AppState?> reduce() async {
    final result = await api.submitForm(formData);
    return state.copy(
      lastSubmission: result,
      submissionCount: state.submissionCount + 1,
    );
  }

  @override
  void after() {
    // Always hide loading state, even on error
    dispatch(SetSubmittingAction(false));

    // Log completion
    analytics.log('form_submitted');
  }
}
```

## Built-in Mixins Using before() and after()

Several AsyncRedux mixins use these methods internally:

| Mixin | Uses before() | Uses after() | Purpose |
|-------|--------------|--------------|---------|
| `CheckInternet` | Yes | No | Verifies connectivity, shows dialog if offline |
| `AbortWhenNoInternet` | Yes | No | Silently aborts if offline |
| `Throttle` | No | Yes | Limits execution frequency |
| `NonReentrant` | Yes | Yes | Prevents duplicate dispatches |
| `Retry` | No | Yes | Retries on failure |
| `Debounce` | No | No | Waits for input pause (uses `wrapReduce`) |

When using these mixins, be aware that they may already override `before()` or `after()`. Call `super.before()` and `super.after()` if you need to combine behaviors.

## References

URLs from the documentation:
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/advanced-actions/action-status
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/aborting-the-dispatch
- https://asyncredux.com/flutter/advanced-actions/wrapping-the-reducer
