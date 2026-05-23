---
name: asyncredux-provider-integration
description: Integrate AsyncRedux with the Provider package. Covers using provider_for_redux, the ReduxSelector widget, and choosing between StoreConnector and ReduxSelector approaches.
---

# Provider Integration with AsyncRedux

The `provider_for_redux` package bridges Provider and AsyncRedux, enabling you to use Provider's dependency injection with Redux state management.

## Installation

Add the package to your `pubspec.yaml`:

```yaml
dependencies:
  provider_for_redux: ^8.0.0
```

## Setting Up AsyncReduxProvider

Replace `StoreProvider` with `AsyncReduxProvider` to expose three items to descendant widgets:

- The Redux store (`Store<AppState>`)
- The application state (`AppState`)
- The dispatch method (`Dispatch`)

```dart
import 'package:provider_for_redux/provider_for_redux.dart';

void main() {
  final store = Store<AppState>(initialState: AppState.initial());

  runApp(
    AsyncReduxProvider<AppState>.value(
      value: store,
      child: MaterialApp(home: MyHomePage()),
    ),
  );
}
```

## Accessing State with Provider.of

Access store components directly using standard Provider patterns:

```dart
// Access state (rebuilds on state changes)
final counter = Provider.of<AppState>(context).counter;

// Access dispatch (use listen: false for actions)
Provider.of<Dispatch>(context, listen: false)(IncrementAction());

// Access the store directly
final store = Provider.of<Store<AppState>>(context, listen: false);
```

## ReduxConsumer Widget

`ReduxConsumer` provides store, state, and dispatch in a single builder, simplifying access:

```dart
ReduxConsumer<AppState>(
  builder: (context, store, state, dispatch, child) {
    return Column(
      children: [
        Text('Counter: ${state.counter}'),
        Text('Description: ${state.description}'),
        ElevatedButton(
          onPressed: () => dispatch(IncrementAction()),
          child: Text('Increment'),
        ),
      ],
    );
  },
)
```

## ReduxSelector Widget

`ReduxSelector` prevents unnecessary rebuilds by selecting specific state portions. Only when selected values change does the widget rebuild.

### Using a List (Recommended)

The simplest approach - explicitly list the properties that should trigger rebuilds:

```dart
ReduxSelector<AppState, dynamic>(
  selector: (context, state) => [state.counter, state.description],
  builder: (context, store, state, dispatch, model, child) {
    return Column(
      children: [
        Text('Counter: ${state.counter}'),
        Text('Description: ${state.description}'),
        ElevatedButton(
          onPressed: () => dispatch(IncrementAction()),
          child: Text('Increment'),
        ),
      ],
    );
  },
)
```

### Using a Custom Model

For structured data, use a Tuple or custom class:

```dart
ReduxSelector<AppState, Tuple2<int, String>>(
  selector: (context, state) => Tuple2(state.counter, state.description),
  builder: (context, store, state, dispatch, model, child) {
    return Column(
      children: [
        Text('Counter: ${model.item1}'),
        Text('Description: ${model.item2}'),
        ElevatedButton(
          onPressed: () => dispatch(IncrementAction()),
          child: Text('Increment'),
        ),
      ],
    );
  },
)
```

## Choosing Between StoreConnector and ReduxSelector

Both approaches manage widget rebuilds during state changes, but serve different use cases:

### Use StoreConnector When:

- You want to separate smart (store-aware) and dumb (presentational) widgets
- You need view-models with explicit equality comparison
- You're building reusable UI components that shouldn't know about Redux
- You want to test UI widgets in isolation without a store

```dart
class MyCounterConnector extends StatelessWidget {
  Widget build(BuildContext context) {
    return StoreConnector<AppState, ViewModel>(
      vm: () => Factory(this),
      builder: (context, vm) => MyCounter(
        counter: vm.counter,
        description: vm.description,
        onIncrement: vm.onIncrement,
      ),
    );
  }
}

class ViewModel extends Vm {
  final int counter;
  final String description;
  final VoidCallback onIncrement;

  ViewModel({
    required this.counter,
    required this.description,
    required this.onIncrement,
  }) : super(equals: [counter, description]);
}
```

### Use ReduxSelector When:

- You prefer minimal boilerplate
- Direct store access within a single widget is acceptable
- You want Provider-style dependency injection
- You're integrating with existing Provider-based code

```dart
ReduxSelector<AppState, dynamic>(
  selector: (context, state) => [state.counter, state.description],
  builder: (context, store, state, dispatch, model, child) {
    return MyCounter(
      counter: state.counter,
      description: state.description,
      onIncrement: () => dispatch(IncrementAction()),
    );
  },
)
```

## Migration Strategy

Both Provider and AsyncRedux connectors work simultaneously, enabling gradual migration:

```dart
// Old code using StoreConnector continues to work
class OldFeatureConnector extends StatelessWidget {
  Widget build(BuildContext context) {
    return StoreConnector<AppState, OldViewModel>(
      vm: () => OldFactory(this),
      builder: (context, vm) => OldFeatureWidget(vm: vm),
    );
  }
}

// New code can use ReduxSelector
class NewFeatureWidget extends StatelessWidget {
  Widget build(BuildContext context) {
    return ReduxSelector<AppState, dynamic>(
      selector: (context, state) => [state.newFeature],
      builder: (context, store, state, dispatch, model, child) {
        return NewFeatureContent(feature: state.newFeature);
      },
    );
  }
}
```

This allows you to migrate incrementally without rewriting your entire application.

## Comparison Summary

| Aspect | StoreConnector | ReduxSelector |
|--------|---------------|---------------|
| Boilerplate | More (ViewModel + Factory) | Less (inline selector) |
| Separation | Smart/Dumb widget pattern | Single widget |
| Testing | Easy to test UI in isolation | Requires store setup |
| Provider compatibility | Native AsyncRedux | Full Provider integration |
| Rebuild control | Via ViewModel equality | Via selector list |

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/other-packages/using-the-provider-package
- https://asyncredux.com/flutter/connector/store-connector
- https://asyncredux.com/flutter/connector/connector-pattern
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/miscellaneous/widget-selectors
- https://pub.dev/packages/provider_for_redux
- https://github.com/marcglasberg/provider_for_redux
