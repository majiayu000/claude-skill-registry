---
name: asyncredux-action-status
description: Checks an AsyncRedux (Flutter) action's completion status using ActionStatus right after the dispatch returns. Use only when you need to know whether an action completed, whether it failed with an error, what error it produced, or how to navigate based on success or failure.
---

# ActionStatus in AsyncRedux

The `ActionStatus` object provides information about whether an action completed successfully or encountered errors. It is returned by `dispatchAndWait()` and related methods.

## Getting ActionStatus

Use `dispatchAndWait()` to get the status after an action completes:

```dart
var status = await dispatchAndWait(MyAction());
```

From within an action, you can also use:

```dart
var status = await dispatchAndWait(SomeOtherAction());
```

## ActionStatus Properties

### Completion Status

- **`isCompleted`**: Returns `true` if the action has finished executing (whether successful or failed)
- **`isCompletedOk`**: Returns `true` if the action finished without errors in both `before()` and `reduce()` methods
- **`isCompletedFailed`**: Returns `true` if the action encountered errors (opposite of `isCompletedOk`)

### Error Information

- **`originalError`**: The error originally thrown by `before()` or `reduce()`, before any modification
- **`wrappedError`**: The error after processing by the action's `wrapError()` method

### Execution Tracking

These properties track which lifecycle methods have completed:

- **`hasFinishedMethodBefore`**: Returns `true` if the `before()` method completed
- **`hasFinishedMethodReduce`**: Returns `true` if the `reduce()` method completed
- **`hasFinishedMethodAfter`**: Returns `true` if the `after()` method completed

Note: The execution tracking properties are primarily meant for testing and debugging. In production code, focus on `isCompletedOk` and `isCompletedFailed`.

## Common Use Cases

### Conditional Navigation After Success

The most common production use is checking if an action succeeded before navigating:

```dart
// In a widget callback
Future<void> _onSavePressed() async {
  var status = await context.dispatchAndWait(SaveFormAction());
  if (status.isCompletedOk) {
    Navigator.pop(context);
  }
}
```

Another example with push navigation:

```dart
Future<void> _onLoginPressed() async {
  var status = await context.dispatchAndWait(LoginAction(
    email: emailController.text,
    password: passwordController.text,
  ));

  if (status.isCompletedOk) {
    Navigator.pushReplacementNamed(context, '/home');
  }
  // If failed, the error will be shown via UserExceptionDialog
}
```

### Testing Action Errors

Use ActionStatus to verify that actions throw expected errors:

```dart
test('MyAction fails with invalid input', () async {
  var store = Store<AppState>(initialState: AppState.initial());

  var status = await store.dispatchAndWait(MyAction(value: -1));

  expect(status.isCompletedFailed, isTrue);
  expect(status.wrappedError, isA<UserException>());
  expect((status.wrappedError as UserException).msg, "Value must be positive");
});
```

### Testing Action Success

```dart
test('SaveAction completes successfully', () async {
  var store = Store<AppState>(initialState: AppState.initial());

  var status = await store.dispatchAndWait(SaveAction(data: validData));

  expect(status.isCompletedOk, isTrue);
  expect(store.state.saved, isTrue);
});
```

### Checking Original vs Wrapped Error

When your action uses `wrapError()` to transform errors, you can inspect both:

```dart
class MyAction extends AppAction {
  @override
  Future<AppState?> reduce() async {
    throw Exception('Network error');
  }

  @override
  Object? wrapError(Object error, StackTrace stackTrace) {
    return UserException('Could not save. Please try again.');
  }
}

// In test:
var status = await store.dispatchAndWait(MyAction());
expect(status.originalError, isA<Exception>()); // The original Exception
expect(status.wrappedError, isA<UserException>()); // The wrapped UserException
```

## Action Lifecycle and Status

The action lifecycle runs in this order:

1. `before()` - Runs first, can be used for preconditions
2. `reduce()` - Runs second (only if `before()` succeeded)
3. `after()` - Runs last, always executes (like a finally block)

The `isCompletedOk` property is `true` only if both `before()` and `reduce()` completed without errors. Note that errors in `after()` do not affect `isCompletedOk`.

If `before()` throws an error, `reduce()` will not run, but `after()` will still execute.

## Best Practices

1. **Use state changes for UI updates**: In production, prefer checking state changes rather than action status. Reserve ActionStatus for cases where you need to perform side effects (like navigation) based on success/failure.

2. **Use `isCompletedOk` for navigation**: The common pattern is to navigate only after an action succeeds:
   ```dart
   if (status.isCompletedOk) Navigator.pop(context);
   ```

3. **Use `wrappedError` in tests**: When testing error handling, check `wrappedError` to see what the user will actually see (after `wrapError()` processing).

4. **Use `originalError` for debugging**: When you need to see the underlying error before any transformation, use `originalError`.

## References

URLs from the documentation:
- https://asyncredux.com/flutter/advanced-actions/action-status
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/miscellaneous/navigation
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
- https://asyncredux.com/flutter/testing/testing-user-exceptions
