---
name: asyncredux-undo-redo
description: Implement undo/redo functionality using state observers. Covers recording state history with stateObserver, creating a RecoverStateAction, implementing undo for the full state or partial state, and managing history limits.
---

# Undo and Redo in AsyncRedux

AsyncRedux simplifies undo/redo through a straightforward pattern: create a state observer to save states to a history list, and create actions to navigate through that history.

## Understanding StateObserver

The `StateObserver` abstract class tracks state modifications. Implement its `observe` method to be notified of state changes:

```dart
abstract class StateObserver<St> {
  void observe(
    ReduxAction<St> action,
    St stateIni,
    St stateEnd,
    Object? error,
    int dispatchCount,
  );
}
```

**Parameters:**
- `action` - The dispatched action that triggered the state change
- `stateIni` - The state before the reducer applied changes
- `stateEnd` - The new state returned by the reducer
- `error` - Null if successful; contains the thrown error otherwise
- `dispatchCount` - Sequential dispatch number

**Timing:** The observer fires right after the reducer returns, before both the `after()` method and error-wrapping processes.

## Step 1: Create the UndoRedoObserver

```dart
class UndoRedoObserver implements StateObserver<AppState> {
  final List<AppState> _history = [];
  int _currentIndex = -1;
  final int maxHistorySize;

  UndoRedoObserver({this.maxHistorySize = 50});

  @override
  void observe(
    ReduxAction<AppState> action,
    AppState stateIni,
    AppState stateEnd,
    Object? error,
    int dispatchCount,
  ) {
    // Skip if action had an error
    if (error != null) return;

    // Skip if state didn't change
    if (stateIni == stateEnd) return;

    // Skip undo/redo actions to prevent recursive history entries
    if (action is UndoAction || action is RedoAction) return;

    // When navigating backwards then performing new actions,
    // clear the "future" history
    if (_currentIndex < _history.length - 1) {
      _history.removeRange(_currentIndex + 1, _history.length);
    }

    // Add the new state to history
    _history.add(stateEnd);
    _currentIndex = _history.length - 1;

    // Enforce maximum history size by removing oldest entries
    while (_history.length > maxHistorySize) {
      _history.removeAt(0);
      _currentIndex--;
    }
  }

  /// Returns the previous state, or null if at the beginning
  AppState? getPreviousState() {
    if (_currentIndex > 0) {
      _currentIndex--;
      return _history[_currentIndex];
    }
    return null;
  }

  /// Returns the next state, or null if at the end
  AppState? getNextState() {
    if (_currentIndex < _history.length - 1) {
      _currentIndex++;
      return _history[_currentIndex];
    }
    return null;
  }

  bool get canUndo => _currentIndex > 0;
  bool get canRedo => _currentIndex < _history.length - 1;
}
```

## Step 2: Register the Observer with the Store

Pass the observer to `stateObservers` during store creation:

```dart
// Create the observer instance so actions can access it
final undoRedoObserver = UndoRedoObserver(maxHistorySize: 100);

var store = Store<AppState>(
  initialState: AppState.initialState(),
  stateObservers: [undoRedoObserver],
);
```

## Step 3: Create Navigation Actions

Create `UndoAction` and `RedoAction` that retrieve states from history:

```dart
class UndoAction extends ReduxAction<AppState> {
  final UndoRedoObserver observer;

  UndoAction(this.observer);

  @override
  AppState? reduce() {
    return observer.getPreviousState();
  }
}

class RedoAction extends ReduxAction<AppState> {
  final UndoRedoObserver observer;

  RedoAction(this.observer);

  @override
  AppState? reduce() {
    return observer.getNextState();
  }
}
```

**Alternative:** Access the observer through dependency injection using the environment pattern:

```dart
class UndoAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() {
    final observer = env.undoRedoObserver;
    return observer.getPreviousState();
  }
}
```

## Step 4: Integrate with the UI

Dispatch undo/redo actions from widgets:

```dart
class UndoRedoButtons extends StatelessWidget {
  final UndoRedoObserver observer;

  const UndoRedoButtons({required this.observer});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        IconButton(
          icon: Icon(Icons.undo),
          onPressed: observer.canUndo
              ? () => context.dispatch(UndoAction(observer))
              : null,
        ),
        IconButton(
          icon: Icon(Icons.redo),
          onPressed: observer.canRedo
              ? () => context.dispatch(RedoAction(observer))
              : null,
        ),
      ],
    );
  }
}
```

## Partial State Undo/Redo

The same approach works to undo/redo only **part** of the state. This is useful when you want to track changes to a specific slice of state independently.

```dart
class PartialUndoRedoObserver implements StateObserver<AppState> {
  final List<DocumentState> _history = [];
  int _currentIndex = -1;
  final int maxHistorySize;

  PartialUndoRedoObserver({this.maxHistorySize = 50});

  @override
  void observe(
    ReduxAction<AppState> action,
    AppState stateIni,
    AppState stateEnd,
    Object? error,
    int dispatchCount,
  ) {
    if (error != null) return;
    if (action is UndoDocumentAction || action is RedoDocumentAction) return;

    // Only track changes to the document portion of state
    if (stateIni.document == stateEnd.document) return;

    if (_currentIndex < _history.length - 1) {
      _history.removeRange(_currentIndex + 1, _history.length);
    }

    _history.add(stateEnd.document);
    _currentIndex = _history.length - 1;

    while (_history.length > maxHistorySize) {
      _history.removeAt(0);
      _currentIndex--;
    }
  }

  DocumentState? getPreviousDocument() {
    if (_currentIndex > 0) {
      _currentIndex--;
      return _history[_currentIndex];
    }
    return null;
  }

  DocumentState? getNextDocument() {
    if (_currentIndex < _history.length - 1) {
      _currentIndex++;
      return _history[_currentIndex];
    }
    return null;
  }
}

class UndoDocumentAction extends ReduxAction<AppState> {
  final PartialUndoRedoObserver observer;

  UndoDocumentAction(this.observer);

  @override
  AppState? reduce() {
    final previousDoc = observer.getPreviousDocument();
    if (previousDoc == null) return null;
    return state.copy(document: previousDoc);
  }
}
```

## Managing History Limits

Key considerations for history management:

1. **Set appropriate limits** - Balance memory usage with undo depth needs
2. **Remove oldest entries** - When exceeding the limit, remove from the beginning
3. **Clear future history** - When new actions occur after undoing, discard the redo stack
4. **Filter irrelevant actions** - Skip actions that don't change state or are navigation actions

```dart
// Example: Different limits for different use cases
final documentObserver = UndoRedoObserver(maxHistorySize: 100); // Heavy undo
final preferencesObserver = UndoRedoObserver(maxHistorySize: 10); // Light undo
```

## Complete Example

```dart
// observer.dart
class UndoRedoObserver implements StateObserver<AppState> {
  final List<AppState> _history = [];
  int _currentIndex = -1;
  final int maxHistorySize;

  UndoRedoObserver({this.maxHistorySize = 50});

  @override
  void observe(
    ReduxAction<AppState> action,
    AppState stateIni,
    AppState stateEnd,
    Object? error,
    int dispatchCount,
  ) {
    if (error != null) return;
    if (stateIni == stateEnd) return;
    if (action is UndoAction || action is RedoAction) return;

    if (_currentIndex < _history.length - 1) {
      _history.removeRange(_currentIndex + 1, _history.length);
    }

    _history.add(stateEnd);
    _currentIndex = _history.length - 1;

    while (_history.length > maxHistorySize) {
      _history.removeAt(0);
      _currentIndex--;
    }
  }

  AppState? getPreviousState() {
    if (_currentIndex > 0) {
      _currentIndex--;
      return _history[_currentIndex];
    }
    return null;
  }

  AppState? getNextState() {
    if (_currentIndex < _history.length - 1) {
      _currentIndex++;
      return _history[_currentIndex];
    }
    return null;
  }

  bool get canUndo => _currentIndex > 0;
  bool get canRedo => _currentIndex < _history.length - 1;

  void clear() {
    _history.clear();
    _currentIndex = -1;
  }
}

// actions.dart
class UndoAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() => env.undoRedoObserver.getPreviousState();
}

class RedoAction extends ReduxAction<AppState> {
  @override
  AppState? reduce() => env.undoRedoObserver.getNextState();
}

// main.dart
void main() {
  final undoRedoObserver = UndoRedoObserver(maxHistorySize: 100);

  final store = Store<AppState>(
    initialState: AppState.initialState(),
    stateObservers: [undoRedoObserver],
    environment: Environment(undoRedoObserver: undoRedoObserver),
  );

  runApp(
    StoreProvider<AppState>(
      store: store,
      child: MyApp(),
    ),
  );
}
```

## References

URLs from the documentation:
- https://asyncredux.com/flutter/miscellaneous/undo-and-redo
- https://asyncredux.com/flutter/basics/store
- https://asyncredux.com/flutter/miscellaneous/logging
- https://asyncredux.com/flutter/miscellaneous/metrics
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/testing/store-tester
- https://asyncredux.com/flutter/basics/sync-actions
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/basics/async-actions
