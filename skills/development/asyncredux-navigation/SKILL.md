---
name: asyncredux-navigation
description: Handle navigation through actions using NavigateAction. Covers setting up the navigator key, dispatching NavigateAction for push/pop/replace, and testing navigation in isolation.
---

# Navigation with NavigateAction

AsyncRedux enables app navigation through action dispatching, making it easier to unit test navigation logic. This approach is optional and currently supports Navigator 1 only.

## Setup

### 1. Create and Register the Navigator Key

Create a global navigator key and register it with NavigateAction during app initialization:

```dart
import 'package:async_redux/async_redux.dart';
import 'package:flutter/material.dart';

final navigatorKey = GlobalKey<NavigatorState>();

void main() async {
  NavigateAction.setNavigatorKey(navigatorKey);
  // ... rest of initialization
  runApp(MyApp());
}
```

### 2. Configure MaterialApp

Pass the same navigator key to your MaterialApp:

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreProvider<AppState>(
      store: store,
      child: MaterialApp(
        routes: {
          '/': (context) => HomePage(),
          '/details': (context) => DetailsPage(),
          '/settings': (context) => SettingsPage(),
        },
        navigatorKey: navigatorKey,
      ),
    );
  }
}
```

## Dispatching Navigation Actions

### Push Operations

```dart
// Push a named route
dispatch(NavigateAction.pushNamed('/details'));

// Push a route with a Route object
dispatch(NavigateAction.push(
  MaterialPageRoute(builder: (context) => DetailsPage()),
));

// Push and replace current route (named)
dispatch(NavigateAction.pushReplacementNamed('/newRoute'));

// Push and replace current route (with Route object)
dispatch(NavigateAction.pushReplacement(
  MaterialPageRoute(builder: (context) => NewPage()),
));

// Pop current route and push a new named route
dispatch(NavigateAction.popAndPushNamed('/otherRoute'));

// Push named route and remove all routes until predicate is true
dispatch(NavigateAction.pushNamedAndRemoveUntil(
  '/home',
  (route) => false, // Removes all routes
));

// Push named route and remove all routes (convenience method)
dispatch(NavigateAction.pushNamedAndRemoveAll('/home'));

// Push route and remove until predicate
dispatch(NavigateAction.pushAndRemoveUntil(
  MaterialPageRoute(builder: (context) => HomePage()),
  (route) => false,
));
```

### Pop Operations

```dart
// Pop the current route
dispatch(NavigateAction.pop());

// Pop with a result value
dispatch(NavigateAction.pop(result: 'some_value'));

// Pop routes until predicate is true
dispatch(NavigateAction.popUntil((route) => route.isFirst));

// Pop until reaching a specific named route
dispatch(NavigateAction.popUntilRouteName('/home'));

// Pop until reaching a specific route
dispatch(NavigateAction.popUntilRoute(someRoute));
```

### Replace Operations

```dart
// Replace a specific route with a new one
dispatch(NavigateAction.replace(
  oldRoute: currentRoute,
  newRoute: MaterialPageRoute(builder: (context) => NewPage()),
));

// Replace the route below the current one
dispatch(NavigateAction.replaceRouteBelow(
  anchorRoute: currentRoute,
  newRoute: MaterialPageRoute(builder: (context) => NewPage()),
));
```

### Remove Operations

```dart
// Remove a specific route
dispatch(NavigateAction.removeRoute(routeToRemove));

// Remove the route below a specific route
dispatch(NavigateAction.removeRouteBelow(anchorRoute));
```

## Complete Example

```dart
import 'package:async_redux/async_redux.dart';
import 'package:flutter/material.dart';

late Store<AppState> store;
final navigatorKey = GlobalKey<NavigatorState>();

void main() async {
  NavigateAction.setNavigatorKey(navigatorKey);
  store = Store<AppState>(initialState: AppState());
  runApp(MyApp());
}

class AppState {}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreProvider<AppState>(
      store: store,
      child: MaterialApp(
        routes: {
          '/': (context) => HomePage(),
          '/details': (context) => DetailsPage(),
        },
        navigatorKey: navigatorKey,
      ),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Home')),
      body: Center(
        child: ElevatedButton(
          child: Text('Go to Details'),
          onPressed: () => context.dispatch(NavigateAction.pushNamed('/details')),
        ),
      ),
    );
  }
}

class DetailsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Details')),
      body: Center(
        child: ElevatedButton(
          child: Text('Go Back'),
          onPressed: () => context.dispatch(NavigateAction.pop()),
        ),
      ),
    );
  }
}
```

## Getting the Current Route Name

Rather than storing the current route in your app state (which can create complications), access it directly:

```dart
String routeName = NavigateAction.getCurrentNavigatorRouteName(context);
```

## Navigation from Actions

You can dispatch navigation actions from within other actions:

```dart
class LoginAction extends ReduxAction<AppState> {
  final String username;
  final String password;

  LoginAction({required this.username, required this.password});

  @override
  Future<AppState?> reduce() async {
    final user = await api.login(username, password);

    // Navigate to home after successful login
    dispatch(NavigateAction.pushReplacementNamed('/home'));

    return state.copy(user: user);
  }
}
```

## Testing Navigation

NavigateAction enables unit testing of navigation without widget or driver tests:

```dart
test('login navigates to home on success', () async {
  final store = Store<AppState>(initialState: AppState());

  // Capture dispatched actions
  NavigateAction? navigateAction;
  store.actionObservers.add((action, ini, prevState, newState) {
    if (action is NavigateAction) {
      navigateAction = action;
    }
  });

  await store.dispatchAndWait(LoginAction(
    username: 'test',
    password: 'password',
  ));

  // Assert navigation type
  expect(navigateAction!.type, NavigateType.pushReplacementNamed);

  // Assert route name
  expect(
    (navigateAction!.details as NavigatorDetails_PushReplacementNamed).routeName,
    '/home',
  );
});
```

### NavigateType Enum Values

The `NavigateType` enum includes values for all navigation operations:

- `push`, `pushNamed`
- `pop`
- `pushReplacement`, `pushReplacementNamed`
- `popAndPushNamed`
- `pushAndRemoveUntil`, `pushNamedAndRemoveUntil`, `pushNamedAndRemoveAll`
- `popUntil`, `popUntilRouteName`, `popUntilRoute`
- `replace`, `replaceRouteBelow`
- `removeRoute`, `removeRouteBelow`

## Important Notes

- Navigation via AsyncRedux is entirely optional
- Currently supports Navigator 1 only
- For modern navigation packages (like go_router), you'll need to create custom action implementations
- Don't store the current route in your app state; use `getCurrentNavigatorRouteName()` instead

## References

URLs from the documentation:
- https://asyncredux.com/flutter/miscellaneous/navigation
- https://asyncredux.com/flutter/testing/testing-navigation
- https://github.com/marcglasberg/async_redux/blob/master/example/lib/main_navigate.dart
- https://raw.githubusercontent.com/marcglasberg/async_redux/master/lib/src/navigate_action.dart
