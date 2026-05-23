---
name: asyncredux-user-exceptions
description: Handle user-facing errors with UserException. Covers throwing UserException from actions, setting up UserExceptionDialog, customizing error dialogs with `onShowUserExceptionDialog`, and using UserExceptionAction for non-interrupting error display.
---

# UserException in AsyncRedux

`UserException` is a special error type for user-facing errors that should be displayed to the user rather than logged as bugs. These represent issues the user can address or should be informed about.

## Throwing UserException from Actions

Throw `UserException` when an action encounters a user-facing error:

```dart
class TransferMoney extends AppAction {
  final double amount;
  TransferMoney(this.amount);

  AppState? reduce() {
    if (amount == 0) {
      throw UserException('You cannot transfer zero money.');
    }
    return state.copy(cash: state.cash - amount);
  }
}
```

For async actions with validation:

```dart
class SaveUser extends AppAction {
  final String name;
  SaveUser(this.name);

  Future<AppState?> reduce() async {
    if (name.length < 4)
      throw UserException('Name must have at least 4 letters.');

    await saveUser(name);
    return null;
  }
}
```

## Converting Errors to UserException

Use `addCause()` to preserve the original error while showing a user-friendly message:

```dart
class ConvertAction extends AppAction {
  final String text;
  ConvertAction(this.text);

  Future<AppState?> reduce() async {
    try {
      var value = int.parse(text);
      return state.copy(counter: value);
    } catch (error) {
      throw UserException('Please enter a valid number')
        .addCause(error);
    }
  }
}
```

## Setting Up UserExceptionDialog

Wrap your home page with `UserExceptionDialog` below both `StoreProvider` and `MaterialApp`:

```dart
Widget build(context) {
  return StoreProvider<AppState>(
    store: store,
    child: MaterialApp(
      home: UserExceptionDialog<AppState>(
        child: MyHomePage(),
      ),
    ),
  );
}
```

If you omit the `onShowUserExceptionDialog` parameter, a default dialog appears with the error message and an OK button.

## Customizing Error Dialogs

Use `onShowUserExceptionDialog` to create custom error dialogs:

```dart
UserExceptionDialog<AppState>(
  onShowUserExceptionDialog: (BuildContext context, UserException exception) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Error'),
        content: Text(exception.message ?? 'An error occurred'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('OK'),
          ),
        ],
      ),
    );
  },
  child: MyHomePage(),
)
```

For non-standard error presentation (like snackbars or banners), you can modify the behavior by accessing the `didUpdateWidget` method in a custom implementation.

## UserExceptionAction for Non-Interrupting Errors

Use `UserExceptionAction` to show an error dialog without throwing an exception or stopping action execution:

```dart
// Show error dialog without failing the action
dispatch(UserExceptionAction('Please enter a valid number'));
```

This is useful when you want to notify the user of an issue mid-action while continuing execution:

```dart
class ConvertAction extends AppAction {
  final String text;
  ConvertAction(this.text);

  Future<AppState?> reduce() async {
    var value = int.tryParse(text);
    if (value == null) {
      // Shows dialog but action continues
      dispatch(UserExceptionAction('Invalid number, using default'));
      value = 0;
    }
    return state.copy(counter: value);
  }
}
```

## Reusable Error Handling with Mixins

Create mixins to standardize UserException conversion across actions:

```dart
mixin ShowUserException on AppAction {
  String getErrorMessage();

  Object? wrapError(Object error, StackTrace stackTrace) {
    return UserException(getErrorMessage()).addCause(error);
  }
}

class ConvertAction extends AppAction with ShowUserException {
  final String text;
  ConvertAction(this.text);

  @override
  String getErrorMessage() => 'Please enter a valid number.';

  Future<AppState?> reduce() async {
    var value = int.parse(text); // Any error becomes UserException
    return state.copy(counter: value);
  }
}
```

## Global Error Handling with GlobalWrapError

Handle third-party or framework errors uniformly across all actions:

```dart
var store = Store<AppState>(
  initialState: AppState.initialState(),
  globalWrapError: MyGlobalWrapError(),
);

class MyGlobalWrapError extends GlobalWrapError {
  @override
  Object? wrap(Object error, StackTrace stackTrace, ReduxAction<dynamic> action) {
    if (error is PlatformException &&
        error.code == 'Error performing get') {
      return UserException('Check your internet connection')
        .addCause(error);
    }
    // Return the error unchanged for other cases
    return error;
  }
}
```

**Processing order**: Action's `wrapError()` -> `GlobalWrapError` -> `ErrorObserver`

## Error Queue

Thrown `UserException` instances are stored in a dedicated error queue within the store. The queue is consumed by `UserExceptionDialog` to display error messages. You can configure the maximum queue capacity in the Store constructor.

## Checking Failed Actions in Widgets

Use these methods to check action failure status and display errors inline:

```dart
Widget build(BuildContext context) {
  if (context.isFailed(SaveUserAction)) {
    var exception = context.exceptionFor(SaveUserAction);
    return Column(
      children: [
        Text('Failed: ${exception?.message}'),
        ElevatedButton(
          onPressed: () {
            context.clearExceptionFor(SaveUserAction);
            context.dispatch(SaveUserAction(name));
          },
          child: Text('Retry'),
        ),
      ],
    );
  }
  return Text('User saved successfully');
}
```

Note: Error states automatically clear when an action is redispatched, so manual cleanup before retry is usually unnecessary.

## Testing UserExceptions

Test that actions throw `UserException` correctly:

```dart
test('should throw UserException for invalid input', () async {
  var store = Store<AppState>(initialState: AppState.initialState());

  var status = await store.dispatchAndWait(TransferMoney(0));

  expect(status.isCompletedFailed, isTrue);
  var error = status.wrappedError;
  expect(error, isA<UserException>());
  expect((error as UserException).message, 'You cannot transfer zero money.');
});
```

Test multiple exceptions using the error queue:

```dart
test('should collect multiple UserExceptions', () async {
  var store = Store<AppState>(initialState: AppState.initialState());

  await store.dispatchAndWaitAll([
    InvalidAction1(),
    InvalidAction2(),
    InvalidAction3(),
  ]);

  var errors = store.errors;
  expect(errors.length, 3);
  expect(errors[0].message, 'First error message');
});
```

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/testing/testing-user-exceptions
- https://asyncredux.com/flutter/basics/wait-fail-succeed
- https://asyncredux.com/flutter/advanced-actions/wrapping-the-reducer
- https://asyncredux.com/flutter/basics/store
