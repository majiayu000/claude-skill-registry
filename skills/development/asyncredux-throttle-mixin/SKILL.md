---
name: asyncredux-throttle-mixin
description: Add the Throttle mixin to prevent actions from running too frequently. Covers setting the throttle duration in milliseconds, use cases like price refresh, and how freshness/staleness works.
---

# Throttle Mixin

The `Throttle` mixin limits action execution to at most once per throttle period. When an action is dispatched multiple times within the defined window, only the first execution runs while subsequent calls abort silently. After the period expires, the next dispatch is permitted.

## Basic Usage

```dart
class LoadPrices extends AppAction with Throttle {

  // Throttle period in milliseconds (default is 1000ms)
  int get throttle => 5000; // 5 seconds

  Future<AppState?> reduce() async {
    var prices = await fetchCurrentPrices();
    return state.copy(prices: prices);
  }
}
```

The default throttle duration is **1000 milliseconds** (1 second). Override the `throttle` getter to set a custom duration.

## How Throttle Works (Freshness/Staleness)

Throttle uses a "freshness window" concept:

1. **First dispatch**: Action runs immediately, data becomes "fresh"
2. **During throttle period**: Data is considered fresh, subsequent dispatches are aborted
3. **After throttle period expires**: Data becomes "stale", next dispatch is allowed to run

This ensures that frequently triggered actions (like a "Refresh Prices" button) don't overwhelm your server while still allowing updates after a reasonable interval.

```dart
// User taps "Refresh" rapidly 5 times in 2 seconds
// With a 5-second throttle:
// - 1st tap: Action runs, prices update
// - 2nd-5th taps: Silently aborted (data still "fresh")
// - Tap after 5 seconds: Action runs again (data now "stale")
```

## Throttle vs Debounce

| Aspect | Throttle | Debounce |
|--------|----------|----------|
| **When it runs** | Immediately on first dispatch | After dispatches stop |
| **Blocking** | Blocks for the period after running | Resets timer on each dispatch |
| **Use case** | Price refresh, rate-limited APIs | Search-as-you-type |

## Bypassing Throttle

Override `ignoreThrottle` to conditionally skip rate limiting:

```dart
class LoadPrices extends AppAction with Throttle {
  final bool forceRefresh;

  LoadPrices({this.forceRefresh = false});

  int get throttle => 5000;

  // Bypass throttle when force refresh is requested
  bool get ignoreThrottle => forceRefresh;

  Future<AppState?> reduce() async {
    var prices = await fetchCurrentPrices();
    return state.copy(prices: prices);
  }
}

// Normal dispatch - respects throttle
dispatch(LoadPrices());

// Force refresh - ignores throttle
dispatch(LoadPrices(forceRefresh: true));
```

## Failure Handling

By default, the throttle lock persists even after errors, preventing immediate retry:

```dart
class LoadPrices extends AppAction with Throttle {
  int get throttle => 5000;

  // Allow immediate retry if the action fails
  bool get removeLockOnError => true;

  Future<AppState?> reduce() async {
    var prices = await fetchCurrentPrices();
    return state.copy(prices: prices);
  }
}
```

### Manual Lock Control

For more control, use these methods:

```dart
// Remove the lock for this specific action type
removeLock();

// Remove locks for all throttled actions
removeAllLocks();
```

## Custom Locking Strategies

Override `lockBuilder()` to implement different locking behaviors:

```dart
class LoadPricesForSymbol extends AppAction with Throttle {
  final String symbol;

  LoadPricesForSymbol(this.symbol);

  int get throttle => 5000;

  // Use the symbol as part of the lock key
  // This allows throttling per symbol instead of per action type
  Object lockBuilder() => 'LoadPrices_$symbol';

  Future<AppState?> reduce() async {
    var price = await fetchPrice(symbol);
    return state.copy(prices: state.prices.add(symbol, price));
  }
}

// These can run in parallel (different lock keys):
dispatch(LoadPricesForSymbol('AAPL'));
dispatch(LoadPricesForSymbol('GOOGL'));

// But this will be throttled (same lock key as first):
dispatch(LoadPricesForSymbol('AAPL')); // Aborted if within 5 seconds
```

## Common Use Cases

### Price/Data Refresh

```dart
class RefreshStockPrices extends AppAction with Throttle {
  int get throttle => 10000; // At most once every 10 seconds

  Future<AppState?> reduce() async {
    var prices = await stockApi.getAllPrices();
    return state.copy(stockPrices: prices);
  }
}
```

### Rate-Limited API Calls

```dart
class SyncWithServer extends AppAction with Throttle {
  int get throttle => 30000; // At most once every 30 seconds

  Future<AppState?> reduce() async {
    var data = await api.sync();
    return state.copy(lastSync: DateTime.now(), data: data);
  }
}
```

### Preventing Button Spam

```dart
class SubmitFeedback extends AppAction with Throttle {
  final String feedback;

  SubmitFeedback(this.feedback);

  int get throttle => 60000; // At most once per minute

  Future<AppState?> reduce() async {
    await api.submitFeedback(feedback);
    return state.copy(feedbackSubmitted: true);
  }
}
```

## Mixin Compatibility

**Compatible with:**
- `CheckInternet`
- `NoDialog`
- `AbortWhenNoInternet`
- `Retry`
- `UnlimitedRetries`
- `Debounce`

**Incompatible with:**
- `NonReentrant` (use one or the other, not both)
- `OptimisticUpdate`
- `OptimisticSync`
- `OptimisticSyncWithPush`

## Combining Multiple Mixins

```dart
class LoadPrices extends AppAction
    with CheckInternet, Throttle, Retry {

  int get throttle => 5000;

  Future<AppState?> reduce() async {
    // CheckInternet ensures connectivity
    // Throttle prevents excessive calls
    // Retry handles transient failures
    var prices = await fetchCurrentPrices();
    return state.copy(prices: prices);
  }
}
```

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/control-mixins
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/advanced-actions/aborting-the-dispatch
- https://asyncredux.com/flutter/advanced-actions/optimistic-mixins
- https://asyncredux.com/flutter/advanced-actions/internet-mixins
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/miscellaneous/refresh-indicators
- https://asyncredux.com/flutter/miscellaneous/database-and-cloud
- https://asyncredux.com/flutter/miscellaneous/wait-condition
- https://asyncredux.com/flutter/testing/mocking
- https://asyncredux.com/flutter/about
- https://asyncredux.com/flutter/intro
