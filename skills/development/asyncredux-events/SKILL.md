---
name: asyncredux-events
description: Use the Event class to interact with Flutter's stateful widgets (TextField, ListView, etc.). Covers creating Event objects in state, consuming events with `context.event()`, scrolling lists, changing text fields, and the event lifecycle.
---

# Events in AsyncRedux

Events are **single-use notifications** used to trigger side effects in widgets. They're designed for controlling native Flutter widgets like `TextField` and `ListView` that manage their own state through controllers.

## When to Use Events

Use events for:
- **Controller actions**: Clearing text, changing text, scrolling lists, focusing inputs
- **One-off UI actions**: Showing dialogs, snackbars, triggering animations
- **Implicit state changes**: Navigation, any action that should happen exactly once

Do NOT use events for:
- Values that need to be read multiple times (use regular state instead)
- Data that should be persisted (events should never be saved to local storage)

## Setup: Add context.event() Extension

Add the `event` method to your BuildContext extension:

```dart
extension BuildContextExtension on BuildContext {
  AppState get state => getState<AppState>();

  R select<R>(R Function(AppState state) selector) =>
    getSelect<AppState, R>(selector);

  // Add this for events:
  R? event<R>(Evt<R> Function(AppState state) selector) =>
    getEvent<AppState, R>(selector);
}
```

## Creating Events

### Boolean Events

For simple triggers that don't carry data:

```dart
// Create an unspent event (will return true once)
var clearTextEvt = Evt();

// Create a spent event (will return false)
var clearTextEvt = Evt.spent();
```

### Typed Events

For events that carry a value:

```dart
// Create an unspent event with a value (will return value once, then null)
var changeTextEvt = Evt<String>("New text");
var scrollToIndexEvt = Evt<int>(42);

// Create a spent event (will return null)
var changeTextEvt = Evt<String>.spent();
```

## Declaring Events in State

Initialize all events as **spent** in your initial state:

```dart
class AppState {
  final Evt clearTextEvt;
  final Evt<String> changeTextEvt;
  final Evt<int> scrollToIndexEvt;

  AppState({
    required this.clearTextEvt,
    required this.changeTextEvt,
    required this.scrollToIndexEvt,
  });

  static AppState initialState() => AppState(
    clearTextEvt: Evt.spent(),
    changeTextEvt: Evt<String>.spent(),
    scrollToIndexEvt: Evt<int>.spent(),
  );

  AppState copy({
    Evt? clearTextEvt,
    Evt<String>? changeTextEvt,
    Evt<int>? scrollToIndexEvt,
  }) => AppState(
    clearTextEvt: clearTextEvt ?? this.clearTextEvt,
    changeTextEvt: changeTextEvt ?? this.changeTextEvt,
    scrollToIndexEvt: scrollToIndexEvt ?? this.scrollToIndexEvt,
  );
}
```

## Dispatching Events from Actions

Actions create **unspent** events and place them in state:

```dart
// Boolean event - triggers clearing the text field
class ClearTextAction extends AppAction {
  AppState reduce() => state.copy(clearTextEvt: Evt());
}

// Typed event - changes the text field to a new value
class ChangeTextAction extends AppAction {
  final String newText;
  ChangeTextAction(this.newText);

  AppState reduce() => state.copy(changeTextEvt: Evt<String>(newText));
}

// Typed event from async operation
class FetchAndSetTextAction extends AppAction {
  Future<AppState> reduce() async {
    String text = await api.fetchText();
    return state.copy(changeTextEvt: Evt<String>(text));
  }
}

// Scroll to a specific index in a ListView
class ScrollToItemAction extends AppAction {
  final int index;
  ScrollToItemAction(this.index);

  AppState reduce() => state.copy(scrollToIndexEvt: Evt<int>(index));
}
```

## Consuming Events in Widgets

Use `context.event()` in the widget's build method. **The event is consumed (marked as spent) immediately when read.**

### TextField Example

```dart
class MyTextField extends StatefulWidget {
  @override
  State<MyTextField> createState() => _MyTextFieldState();
}

class _MyTextFieldState extends State<MyTextField> {
  final controller = TextEditingController();

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Consume the clear event - returns true once, then false
    bool shouldClear = context.event((s) => s.clearTextEvt);
    if (shouldClear) {
      controller.clear();
    }

    // Consume the change event - returns the value once, then null
    String? newText = context.event((s) => s.changeTextEvt);
    if (newText != null) {
      controller.text = newText;
    }

    return TextField(controller: controller);
  }
}
```

### ListView Scrolling Example

```dart
class MyListView extends StatefulWidget {
  @override
  State<MyListView> createState() => _MyListViewState();
}

class _MyListViewState extends State<MyListView> {
  final scrollController = ScrollController();
  final itemHeight = 50.0;

  @override
  void dispose() {
    scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final items = context.select((s) => s.items);

    // Consume the scroll event
    int? scrollToIndex = context.event((s) => s.scrollToIndexEvt);
    if (scrollToIndex != null) {
      // Schedule the scroll after the frame is built
      WidgetsBinding.instance.addPostFrameCallback((_) {
        scrollController.animateTo(
          scrollToIndex * itemHeight,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      });
    }

    return ListView.builder(
      controller: scrollController,
      itemCount: items.length,
      itemBuilder: (context, index) => SizedBox(
        height: itemHeight,
        child: Text(items[index]),
      ),
    );
  }
}
```

## Event Lifecycle

1. **Created as spent**: Events start as `Evt.spent()` in initial state
2. **Dispatched as unspent**: Action creates `Evt()` or `Evt<T>(value)` and puts it in state
3. **Widget rebuilds**: State change triggers widget rebuild
4. **Consumed once**: `context.event()` returns the value and marks the event as spent
5. **Returns null/false**: Subsequent reads return `null` (typed) or `false` (boolean)

## Important Rules

### Each Event Can Only Be Consumed by One Widget

If multiple widgets need the same trigger, create separate events:

```dart
class AppState {
  final Evt clearSearchEvt;      // For search field
  final Evt clearCommentsEvt;    // For comments field
  // ...
}
```

### Don't Use Events for Persistent Data

Events are mutable and designed for one-time use. Never persist them to local storage.

### Event Equality Prevents Unnecessary Rebuilds

Events have special equality methods that prevent unnecessary widget rebuilds when used correctly with the selector pattern.

## Advanced: Checking Event Status Without Consuming

Use these methods to check an event's status without consuming it:

```dart
// Check if an event has been consumed
bool consumed = myEvent.isSpent;

// Check if an event is ready to be consumed
bool ready = myEvent.isNotSpent;

// Get the underlying state without consuming
var eventState = myEvent.state;
```

## Advanced: Event.map() for Transformations

Transform an event's value:

```dart
// Map an event to a different type
Evt<String> nameEvt = Evt<int>(42).map((value) => 'Item $value');
```

## Advanced: Consuming from Multiple Event Sources

When you need to consume from multiple possible event sources:

```dart
// Create an event that consumes from first non-spent source
var combined = Event.from([event1, event2, event3]);

// Or use the static method
var value = Event.consumeFrom([event1, event2, event3]);
```

## References

URLs from the documentation:
- https://asyncredux.com/flutter/basics/events
- https://asyncredux.com/flutter/miscellaneous/advanced-events
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/connector/store-connector
