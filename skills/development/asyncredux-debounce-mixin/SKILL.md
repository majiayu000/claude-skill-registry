---
name: asyncredux-debounce-mixin
description: Add the Debounce mixin to wait for user input pauses before acting. Covers setting the `debounce` duration, implementing search-as-you-type, and avoiding excessive API calls during rapid input.
---

# Debounce Mixin

The `Debounce` mixin delays action execution until after a period of inactivity. Each new dispatch resets the timer, so the action only runs once dispatching stops for the specified duration. This is ideal for search-as-you-type functionality and avoiding excessive API calls during rapid user input.

## Basic Usage

Add the `Debounce` mixin to your action class:

```dart
class SearchText extends AppAction with Debounce {
  final String searchTerm;
  SearchText(this.searchTerm);

  Future<AppState?> reduce() async {
    var response = await http.get(
      Uri.parse('https://example.com/?q=${Uri.encodeComponent(searchTerm)}')
    );
    return state.copy(searchResult: response.body);
  }
}
```

When the user types quickly, each keystroke dispatches `SearchText`. The mixin delays execution, and each new dispatch resets the timer. The API call only happens once the user stops typing for the debounce period.

## Setting the Debounce Duration

The default debounce period is **333 milliseconds**. Override the `debounce` getter to customize:

```dart
class SearchText extends AppAction with Debounce {
  final String searchTerm;
  SearchText(this.searchTerm);

  // Wait 1 second of inactivity before executing
  int get debounce => 1000;

  Future<AppState?> reduce() async {
    var response = await http.get(
      Uri.parse('https://example.com/?q=${Uri.encodeComponent(searchTerm)}')
    );
    return state.copy(searchResult: response.body);
  }
}
```

## Custom Lock Builder

By default, all instances of a debounced action share the same lock. Override `lockBuilder()` to create independent debounce periods for different action instances:

```dart
class SearchField extends AppAction with Debounce {
  final String fieldId;
  final String searchTerm;
  SearchField(this.fieldId, this.searchTerm);

  // Each fieldId gets its own independent debounce timer
  Object? lockBuilder() => fieldId;

  Future<AppState?> reduce() async {
    // Search logic here
  }
}
```

This enables multiple search fields to operate independently, each with their own debounce timer.

## Debounce vs Throttle

These two mixins serve different purposes:

| Mixin | Behavior | Best For |
|-------|----------|----------|
| **Throttle** | Runs immediately on first dispatch, then blocks subsequent dispatches for the period | Rate-limiting actions that should execute right away (e.g., refresh button) |
| **Debounce** | Waits for quiet time, only runs after dispatches stop | Waiting for user to finish input (e.g., search-as-you-type) |

**Throttle**: "Execute now, then wait before allowing again"
**Debounce**: "Wait until activity stops, then execute"

## Mixin Compatibility

Debounce **can** be combined with:
- `CheckInternet`
- `NoDialog`
- `AbortWhenNoInternet`
- `NonReentrant`
- `Fresh`
- `Throttle`

Debounce **cannot** be combined with:
- `Retry`
- `UnlimitedRetries`
- `UnlimitedRetryCheckInternet`
- `OptimisticCommand`
- `OptimisticSync`
- `OptimisticSyncWithPush`
- `ServerPush`

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/control-mixins
- https://asyncredux.com/flutter/advanced-actions/control-mixins#debounce
- https://asyncredux.com/flutter/advanced-actions/control-mixins#throttle
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/actions-and-reducers
- https://asyncredux.com/flutter/basics/events
- https://asyncredux.com/flutter/advanced-actions/action-mixins#compatibility
