---
name: asyncredux-check-internet-mixin
description: Add the CheckInternet mixin to ensure network connectivity before action execution. Covers automatic error dialogs, combining with NoDialog for custom UI handling, and AbortWhenNoInternet for silent abort.
---

# CheckInternet Mixin

The `CheckInternet` mixin verifies device connectivity before an action executes. If there's no internet connection, the action aborts and displays a dialog with the message: "There is no Internet. Please, verify your connection."

## Basic Usage

```dart
class LoadText extends AppAction with CheckInternet {

  Future<AppState?> reduce() async {
    var response = await http.get('https://api.example.com/text');
    return state.copy(text: response.body);
  }
}
```

The mixin works by overriding the `before()` method. If the device lacks connectivity, it throws a `UserException` which triggers the standard error dialog.

## Customizing the Error Message

Override `connectionException()` to return a custom `UserException`:

```dart
class LoadText extends AppAction with CheckInternet {

  @override
  UserException connectionException(UserException error) {
    return UserException('Unable to load data. Check your connection.');
  }

  Future<AppState?> reduce() async {
    var response = await http.get('https://api.example.com/text');
    return state.copy(text: response.body);
  }
}
```

## NoDialog Modifier

Use `NoDialog` alongside `CheckInternet` to suppress the automatic error dialog. This allows you to handle connectivity failures in your widgets using `isFailed()` and `exceptionFor()`:

```dart
class LoadText extends AppAction with CheckInternet, NoDialog {

  Future<AppState?> reduce() async {
    var response = await http.get('https://api.example.com/text');
    return state.copy(text: response.body);
  }
}
```

Then handle the error in your widget:

```dart
Widget build(BuildContext context) {
  if (context.isWaiting(LoadText)) {
    return CircularProgressIndicator();
  }

  if (context.isFailed(LoadText)) {
    var exception = context.exceptionFor(LoadText);
    return Text('Error: ${exception?.message}');
  }

  return Text(context.state.text);
}
```

## AbortWhenNoInternet

Use `AbortWhenNoInternet` for silent failure when offline. The action aborts without throwing errors or displaying dialogs—as if it had never been dispatched:

```dart
class RefreshData extends AppAction with AbortWhenNoInternet {

  Future<AppState?> reduce() async {
    var response = await http.get('https://api.example.com/data');
    return state.copy(data: response.body);
  }
}
```

This is useful for background refreshes or non-critical operations where user notification isn't needed.

## UnlimitedRetryCheckInternet

This mixin combines three capabilities: internet verification, unlimited retry with exponential backoff, and non-reentrant behavior. It's ideal for essential operations like loading startup data:

```dart
class LoadAppStartupData extends AppAction with UnlimitedRetryCheckInternet {

  Future<AppState?> reduce() async {
    var response = await http.get('https://api.example.com/startup');
    return state.copy(startupData: response.body);
  }
}
```

Default retry parameters:
- Initial delay: 350ms
- Multiplier: 2
- Maximum delay with internet: 5 seconds
- Maximum delay without internet: 1 second

Track retry attempts via the `attempts` getter and customize logging through `printRetries()`.

## Mixin Compatibility

Important compatibility rules:
- `CheckInternet` and `AbortWhenNoInternet` are **incompatible** with each other
- Neither `CheckInternet` nor `AbortWhenNoInternet` can be combined with `UnlimitedRetryCheckInternet`
- `CheckInternet` works well with `Retry`, `NonReentrant`, `Throttle`, `Debounce`, and optimistic mixins

## Testing Internet Connectivity

Two methods for simulating connectivity in tests:

**Per-action simulation** - Override `internetOnOffSimulation` within specific actions:

```dart
class LoadText extends AppAction with CheckInternet {
  @override
  bool? get internetOnOffSimulation => false; // Simulate offline

  Future<AppState?> reduce() async {
    // ...
  }
}
```

**Global simulation** - Set `forceInternetOnOffSimulation` on the store:

```dart
var store = Store<AppState>(
  initialState: AppState.initialState(),
);
store.forceInternetOnOffSimulation = false; // All actions see no internet
```

## Limitations

These mixins only detect device connectivity status. They cannot verify:
- Internet provider functionality
- Server availability
- API endpoint reachability

For server-specific connectivity checks, implement additional validation in your action's `reduce()` method or `before()` method.

## References

URLs from the documentation:
- https://asyncredux.com/flutter/advanced-actions/internet-mixins
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/aborting-the-dispatch
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/advanced-actions/control-mixins
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/basics/wait-fail-succeed
- https://asyncredux.com/flutter/testing/mocking
