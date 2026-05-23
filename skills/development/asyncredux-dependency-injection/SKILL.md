---
name: asyncredux-dependency-injection
description: Inject dependencies into actions using the environment pattern. Covers creating an Environment class, passing it to the Store, accessing `env` from actions, and using dependency injection for testability.
---

# Dependency Injection with Environment

AsyncRedux provides dependency injection through the Store's `environment` parameter. Dependencies stored in the environment are accessible throughout actions, widgets, and view-model factories, and are automatically disposed when the store is disposed.

## Step 1: Define an Environment Interface

Create an abstract class defining your injectable services:

```dart
abstract class Environment {
  // Define your injectable services as abstract methods/getters
  ApiClient get apiClient;
  AuthService get authService;
  Analytics get analytics;

  int incrementer(int value, int amount);
  int limit(int value);
}
```

## Step 2: Implement the Environment

Create concrete implementations for different contexts (production, staging, test):

```dart
class ProductionEnvironment implements Environment {
  @override
  ApiClient get apiClient => RealApiClient();

  @override
  AuthService get authService => FirebaseAuthService();

  @override
  Analytics get analytics => MixpanelAnalytics();

  @override
  int incrementer(int value, int amount) => value + amount;

  @override
  int limit(int value) => min(value, 100);
}

class TestEnvironment implements Environment {
  @override
  ApiClient get apiClient => MockApiClient();

  @override
  AuthService get authService => MockAuthService();

  @override
  Analytics get analytics => NoOpAnalytics();

  @override
  int incrementer(int value, int amount) => value + amount;

  @override
  int limit(int value) => value; // No limit in tests
}
```

## Step 3: Pass Environment to the Store

When creating the store, pass your environment instance:

```dart
void main() {
  var store = Store<AppState>(
    initialState: AppState.initialState(),
    environment: ProductionEnvironment(),
  );

  runApp(
    StoreProvider<AppState>(
      store: store,
      child: MyApp(),
    ),
  );
}
```

## Step 4: Access Environment from Actions

Extend `ReduxAction` to provide typed access to your environment:

```dart
/// Base action class with typed environment access
abstract class Action extends ReduxAction<AppState> {
  @override
  Environment get env => super.env as Environment;
}
```

Now use `env` in your actions:

```dart
class FetchUserAction extends Action {
  final String userId;
  FetchUserAction(this.userId);

  @override
  Future<AppState?> reduce() async {
    // Access injected dependencies via env
    final user = await env.apiClient.fetchUser(userId);
    env.analytics.logEvent('user_fetched');

    return state.copy(user: user);
  }
}

class IncrementAction extends Action {
  final int amount;
  IncrementAction({required this.amount});

  @override
  AppState reduce() {
    // Use environment methods in reducer
    final newCount = env.incrementer(state.counter, amount);
    return state.copy(counter: env.limit(newCount));
  }
}
```

## Step 5: Access Environment from Widgets

Create a `BuildContext` extension to access the environment in widgets:

```dart
extension BuildContextExtension on BuildContext {
  AppState get state => getState<AppState>();

  R select<R>(R Function(AppState state) selector) =>
      getSelect<AppState, R>(selector);

  Environment get env => getEnvironment<AppState>() as Environment;
}
```

Use in widgets:

```dart
class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Access environment
    final env = context.env;

    // Use environment logic in selectors
    final counter = context.select((state) => env.limit(state.counter));

    return Scaffold(
      body: Center(
        child: Text('Counter: $counter'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => dispatch(IncrementAction(amount: 1)),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## Testing with Different Environments

The environment pattern makes testing straightforward by allowing you to inject test doubles:

```dart
void main() {
  group('IncrementAction', () {
    test('increments counter using environment', () async {
      // Create store with test environment
      var store = Store<AppState>(
        initialState: AppState(counter: 0),
        environment: TestEnvironment(),
      );

      await store.dispatchAndWait(IncrementAction(amount: 5));

      // TestEnvironment has no limit, so value is 5
      expect(store.state.counter, 5);
    });

    test('production environment limits counter', () async {
      var store = Store<AppState>(
        initialState: AppState(counter: 95),
        environment: ProductionEnvironment(),
      );

      await store.dispatchAndWait(IncrementAction(amount: 10));

      // ProductionEnvironment limits to 100
      expect(store.state.counter, 100);
    });
  });
}
```

## Complete Working Example

```dart
import 'dart:math';
import 'package:async_redux/async_redux.dart';
import 'package:flutter/material.dart';

late Store<int> store;

void main() {
  store = Store<int>(
    initialState: 0,
    environment: EnvironmentImpl(),
  );
  runApp(MyApp());
}

/// Abstract environment interface
abstract class Environment {
  int incrementer(int value, int amount);
  int limit(int value);
}

/// Production implementation
class EnvironmentImpl implements Environment {
  @override
  int incrementer(int value, int amount) => value + amount;

  @override
  int limit(int value) => min(value, 5); // Limit counter at 5
}

/// Base action with typed env access
abstract class Action extends ReduxAction<int> {
  @override
  Environment get env => super.env as Environment;
}

/// Action using environment
class IncrementAction extends Action {
  final int amount;
  IncrementAction({required this.amount});

  @override
  int reduce() => env.incrementer(state, amount);
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreProvider<int>(
      store: store,
      child: MaterialApp(home: MyHomePage()),
    );
  }
}

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final env = context.env;
    final counter = context.select((state) => env.limit(state));

    return Scaffold(
      appBar: AppBar(title: const Text('Dependency Injection Example')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Counter (limited to 5):'),
            Text('$counter', style: const TextStyle(fontSize: 30)),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => dispatch(IncrementAction(amount: 1)),
        child: const Icon(Icons.add),
      ),
    );
  }
}

extension BuildContextExtension on BuildContext {
  int get state => getState<int>();
  R select<R>(R Function(int state) selector) => getSelect<int, R>(selector);
  Environment get env => getEnvironment<int>() as Environment;
}
```

## Key Benefits

- **Testability**: Swap implementations for testing without changing action code
- **Separation of concerns**: Business logic lives in environment, actions orchestrate
- **Automatic disposal**: Dependencies are disposed when the store is disposed
- **Type safety**: The typed `env` getter provides compile-time checking
- **Scoped dependencies**: Each store instance has its own environment, preventing test contamination

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/miscellaneous/dependency-injection
- https://asyncredux.com/flutter/testing/mocking
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/connector/store-connector
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/testing/dispatch-wait-and-expect
- https://github.com/marcglasberg/async_redux/blob/master/example/lib/main_environment.dart
