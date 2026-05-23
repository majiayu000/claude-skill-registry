---
name: asyncredux-flutter-hooks
description: Integrate AsyncRedux with the flutter_hooks package. Covers adding flutter_hooks_async_redux, using the useSelector hook, and combining hooks with AsyncRedux state management.
---

## Overview

The `flutter_hooks_async_redux` package provides a hooks-based API for accessing AsyncRedux state. If you prefer functional components with hooks over the widget-based `StoreConnector` pattern, this package lets you use hooks like `useSelector` and `useDispatch` to interact with the Redux store.

## Installation

Add these dependencies to your `pubspec.yaml`:

```yaml
dependencies:
  flutter_hooks: ^0.21.2
  async_redux: ^24.2.2
  flutter_hooks_async_redux: ^3.1.0
```

Then run `flutter pub get`.

## Core Hooks

### useSelector

Selects a part of the state and subscribes to updates. The widget rebuilds when the selected value changes:

```dart
String username = useSelector<AppState, String>((state) => state.username);
```

The `distinct` parameter (default `true`) controls whether the widget rebuilds only when the selected value changes.

### Creating a Custom useAppState Hook

For convenience, define a custom hook that's pre-typed for your state:

```dart
T useAppState<T>(T Function(AppState state) converter, {bool distinct = true}) =>
    useSelector<AppState, T>(converter, distinct: distinct);
```

This simplifies state access throughout your app:

```dart
// Instead of:
String username = useSelector<AppState, String>((state) => state.username);

// Use:
String username = useAppState((state) => state.username);
```

### useDispatch

Dispatches actions that may change the store state. Works with both sync and async actions:

```dart
class MyWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    var dispatch = useDispatch();

    return ElevatedButton(
      onPressed: () => dispatch(IncrementAction()),
      child: Text('Increment'),
    );
  }
}
```

### useDispatchAndWait

Dispatches an action and returns a `Future<ActionStatus>` that resolves when the action completes:

```dart
class MyWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    var dispatchAndWait = useDispatchAndWait();
    var dispatch = useDispatch();

    Future<void> handleSubmit() async {
      // Wait for first action to complete
      await dispatchAndWait(DoThisFirstAction());
      // Then dispatch the second
      dispatch(DoThisSecondAction());
    }

    return ElevatedButton(
      onPressed: handleSubmit,
      child: Text('Submit'),
    );
  }
}
```

You can also check the action status:

```dart
var status = await dispatchAndWait(MyAction());
if (status.isCompletedOk) {
  // Action succeeded
}
```

### useDispatchSync

Enforces synchronous action dispatch. Throws `StoreException` if you attempt to dispatch an async action:

```dart
var dispatchSync = useDispatchSync();
dispatchSync(MySyncAction()); // OK
dispatchSync(MyAsyncAction()); // Throws StoreException
```

## Waiting and Error Hooks

### useIsWaiting

Checks if an async action is currently being processed:

```dart
class MyWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    var dispatch = useDispatch();
    var isLoading = useIsWaiting(LoadDataAction);

    return Column(
      children: [
        if (isLoading) CircularProgressIndicator(),
        ElevatedButton(
          onPressed: () => dispatch(LoadDataAction()),
          child: Text('Load'),
        ),
      ],
    );
  }
}
```

You can check by action type, action instance, or multiple types:

```dart
// By action type
var isWaiting = useIsWaiting(MyAction);

// By action instance
var action = MyAction();
dispatch(action);
var isWaiting = useIsWaiting(action);

// Multiple types - true if ANY are in progress
var isWaiting = useIsWaiting([BuyAction, SellAction]);
```

### useIsFailed

Checks if an action has failed:

```dart
var isFailed = useIsFailed(MyAction);

if (isFailed) {
  return Text('Something went wrong');
}
```

### useExceptionFor

Retrieves the `UserException` from a failed action:

```dart
var exception = useExceptionFor(MyAction);

if (exception != null) {
  return Text(exception.reason ?? 'Unknown error');
}
```

### useClearExceptionFor

Gets a function to clear the exception state for an action:

```dart
var clearExceptionFor = useClearExceptionFor();

// Clear exception when user dismisses error
ElevatedButton(
  onPressed: () => clearExceptionFor(MyAction),
  child: Text('Dismiss'),
)
```

## Complete Example

Here's a full example combining multiple hooks:

```dart
class UserProfileWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    // Select state
    var username = useAppState((state) => state.user.name);
    var email = useAppState((state) => state.user.email);

    // Dispatch hooks
    var dispatch = useDispatch();
    var dispatchAndWait = useDispatchAndWait();

    // Loading and error state
    var isLoading = useIsWaiting(UpdateProfileAction);
    var isFailed = useIsFailed(UpdateProfileAction);
    var exception = useExceptionFor(UpdateProfileAction);
    var clearException = useClearExceptionFor();

    Future<void> handleUpdate() async {
      var status = await dispatchAndWait(UpdateProfileAction());
      if (status.isCompletedOk) {
        // Show success message
      }
    }

    return Column(
      children: [
        Text('Username: $username'),
        Text('Email: $email'),

        if (isLoading)
          CircularProgressIndicator(),

        if (isFailed && exception != null)
          Row(
            children: [
              Text(exception.reason ?? 'Update failed'),
              IconButton(
                icon: Icon(Icons.close),
                onPressed: () => clearException(UpdateProfileAction),
              ),
            ],
          ),

        ElevatedButton(
          onPressed: isLoading ? null : handleUpdate,
          child: Text('Update Profile'),
        ),
      ],
    );
  }
}
```

## Hook Parameters Reference

| Hook | Accepts | Returns |
|------|---------|---------|
| `useSelector<St, T>` | Converter function | Selected value of type T |
| `useDispatch` | None | Dispatch function |
| `useDispatchAndWait` | None | Function returning `Future<ActionStatus>` |
| `useDispatchSync` | None | Sync dispatch function |
| `useIsWaiting` | Action type, instance, or list of types | `bool` |
| `useIsFailed` | Action type, instance, or list of types | `bool` |
| `useExceptionFor` | Action type, instance, or list of types | `UserException?` |
| `useClearExceptionFor` | None | Clear function |

## Hooks vs StoreConnector

Choose hooks when:
- You prefer functional widget patterns
- You're already using `flutter_hooks` in your project
- You want concise state access without view-model boilerplate

Choose `StoreConnector` when:
- You want explicit separation between UI and state logic
- You need the structured view-model pattern for testing
- You're not using hooks elsewhere in your project

Both approaches work well with AsyncRedux - pick the one that fits your team's preferences.

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/other-packages/using-flutter-hooks-package
- https://pub.dev/packages/flutter_hooks_async_redux
- https://github.com/marcglasberg/flutter_hooks_async_redux
