---
name: asyncredux-streams-timers
description: Manage Streams and Timers with AsyncRedux. Covers creating actions to start/stop streams, storing stream subscriptions in store props, dispatching actions from stream callbacks, and proper cleanup with disposeProps().
---

# AsyncRedux Streams and Timers

## Core Principles

Two fundamental rules for working with streams and timers in AsyncRedux:

1. **Don't send streams or timers down to widgets.** Don't declare, subscribe, or unsubscribe to them inside widgets.

2. **Don't put streams or timers in the Redux store state.** They produce state changes, but they are not state themselves.

Instead, store streams and timers in the store's **props** - a key-value container that can hold any object type.

## Store Props API

AsyncRedux provides methods for managing props in both `Store` and `ReduxAction`:

### `setProp(key, value)`

Stores an object (timer, stream subscription, etc.) in the store's props:

```dart
setProp('myTimer', Timer.periodic(Duration(seconds: 1), callback));
setProp('priceStream', priceStream.listen(onData));
```

### `prop<T>(key)`

Retrieves a property from the store:

```dart
var timer = prop<Timer>('myTimer');
var subscription = prop<StreamSubscription>('priceStream');
```

### `disposeProp(key)`

Disposes a single property by its key. Automatically cancels/closes timers, futures, and stream subscriptions:

```dart
disposeProp('myTimer'); // Cancels the timer and removes from props
```

### `disposeProps([predicate])`

Disposes multiple properties. Without a predicate, disposes all Timer, Future, and Stream-related props:

```dart
// Dispose all timers, futures, stream subscriptions
disposeProps();

// Dispose only timers
disposeProps(({Object? key, Object? value}) => value is Timer);

// Dispose props with specific keys
disposeProps(({Object? key, Object? value}) => key.toString().startsWith('temp_'));
```

## Timer Pattern

### Starting a Timer

Create an action that sets up a `Timer.periodic` and stores it in props:

```dart
class StartPollingAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    // Store the timer in props
    setProp('pollingTimer', Timer.periodic(
      Duration(seconds: 5),
      (timer) => dispatch(FetchDataAction()),
    ));
    return null; // No state change from this action
  }
}
```

### Stopping a Timer

Create an action to dispose the timer:

```dart
class StopPollingAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    disposeProp('pollingTimer');
    return null;
  }
}
```

### Timer with Tick Count

Access the timer's tick count in callbacks:

```dart
class StartTimerAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    setProp('myTimer', Timer.periodic(
      Duration(seconds: 1),
      (timer) => dispatch(UpdateTickAction(timer.tick)),
    ));
    return null;
  }
}

class UpdateTickAction extends ReduxAction<AppState> {
  final int tick;
  UpdateTickAction(this.tick);

  @override
  AppState? reduce() => state.copy(tickCount: tick);
}
```

## Stream Pattern

### Subscribing to a Stream

Create an action that subscribes to a stream and stores the subscription:

```dart
class StartListeningAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    final subscription = myDataStream.listen(
      (data) => dispatch(DataReceivedAction(data)),
      onError: (error) => dispatch(StreamErrorAction(error)),
    );
    setProp('dataSubscription', subscription);
    return null;
  }
}
```

### Unsubscribing from a Stream

```dart
class StopListeningAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    disposeProp('dataSubscription');
    return null;
  }
}
```

### Handling Stream Data

The stream callback dispatches an action with the data, which updates the state:

```dart
class DataReceivedAction extends ReduxAction<AppState> {
  final MyData data;
  DataReceivedAction(this.data);

  @override
  AppState? reduce() => state.copy(latestData: data);
}
```

## Lifecycle Management

### Screen-Specific Streams/Timers

Use `StoreConnector`'s `onInit` and `onDispose` callbacks:

```dart
class PriceScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return StoreConnector<AppState, _Vm>(
      vm: () => _Factory(),
      onInit: _onInit,
      onDispose: _onDispose,
      builder: (context, vm) => PriceWidget(price: vm.price),
    );
  }

  void _onInit(Store<AppState> store) {
    store.dispatch(StartPriceStreamAction());
  }

  void _onDispose(Store<AppState> store) {
    store.dispatch(StopPriceStreamAction());
  }
}
```

### App-Wide Streams/Timers

Start after store creation, stop when app closes:

```dart
void main() {
  final store = Store<AppState>(initialState: AppState.initialState());

  // Start app-wide streams/timers
  store.dispatch(StartGlobalPollingAction());

  runApp(StoreProvider<AppState>(
    store: store,
    child: MyApp(),
  ));
}

// In your app's dispose logic
store.dispatch(StopGlobalPollingAction());
store.disposeProps(); // Clean up all remaining props
store.shutdown();
```

### Single Action That Toggles

Combine start/stop in one action:

```dart
class TogglePollingAction extends ReduxAction<AppState> {
  final bool start;
  TogglePollingAction(this.start);

  @override
  AppState? reduce() {
    if (start) {
      setProp('polling', Timer.periodic(
        Duration(seconds: 5),
        (_) => dispatch(RefreshDataAction()),
      ));
    } else {
      disposeProp('polling');
    }
    return null;
  }
}
```

## Complete Example: Real-Time Price Updates

```dart
// State
class AppState {
  final double price;
  final bool isStreaming;

  AppState({required this.price, required this.isStreaming});

  static AppState initialState() => AppState(price: 0.0, isStreaming: false);

  AppState copy({double? price, bool? isStreaming}) => AppState(
    price: price ?? this.price,
    isStreaming: isStreaming ?? this.isStreaming,
  );
}

// Start streaming prices
class StartPriceStreamAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    // Don't start if already streaming
    if (state.isStreaming) return null;

    final subscription = priceService.priceStream.listen(
      (price) => dispatch(UpdatePriceAction(price)),
      onError: (e) => dispatch(PriceStreamErrorAction(e)),
    );

    setProp('priceSubscription', subscription);
    return state.copy(isStreaming: true);
  }
}

// Stop streaming prices
class StopPriceStreamAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    if (!state.isStreaming) return null;

    disposeProp('priceSubscription');
    return state.copy(isStreaming: false);
  }
}

// Handle price updates
class UpdatePriceAction extends ReduxAction<AppState> {
  final double price;
  UpdatePriceAction(this.price);

  @override
  AppState? reduce() => state.copy(price: price);
}

// Handle stream errors
class PriceStreamErrorAction extends ReduxAction<AppState> {
  final Object error;
  PriceStreamErrorAction(this.error);

  @override
  AppState? reduce() {
    // Stop streaming on error
    disposeProp('priceSubscription');
    return state.copy(isStreaming: false);
  }
}
```

## Testing onInit/onDispose

Use `ConnectorTester` to test lifecycle callbacks without full widget tests:

```dart
test('starts and stops polling on screen lifecycle', () async {
  var store = Store<AppState>(initialState: AppState.initialState());
  var connectorTester = store.getConnectorTester(PriceScreen());

  // Simulate screen entering view
  connectorTester.runOnInit();
  var startAction = await store.waitAnyActionTypeFinishes([StartPriceStreamAction]);
  expect(store.state.isStreaming, true);

  // Simulate screen leaving view
  connectorTester.runOnDispose();
  var stopAction = await store.waitAnyActionTypeFinishes([StopPriceStreamAction]);
  expect(store.state.isStreaming, false);
});
```

## Cleanup on Store Shutdown

Call `disposeProps()` before shutting down the store to clean up all remaining timers and stream subscriptions:

```dart
// Clean up all Timer, Future, and Stream-related props
store.disposeProps();

// Shut down the store
store.shutdown();
```

The `disposeProps()` method automatically:
- Cancels `Timer` objects
- Cancels `StreamSubscription` objects
- Closes `StreamController` and `StreamSink` objects
- Ignores `Future` objects (to prevent unhandled errors)

Regular (non-disposable) props are kept unless you provide a predicate that matches them.

## References

URLs from the documentation:
- https://asyncredux.com/flutter/miscellaneous/streams-and-timers
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/testing/testing-oninit-ondispose
- https://asyncredux.com/flutter/miscellaneous/dependency-injection
