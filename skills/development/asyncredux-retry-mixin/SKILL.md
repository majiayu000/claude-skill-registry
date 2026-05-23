---
name: asyncredux-retry-mixin
description: Add the Retry mixin for automatic retry with exponential backoff on action failure. Covers using Retry alone for limited retries, combining with UnlimitedRetries for infinite retries, and configuring retry behavior.
---

# Retry Mixin

The `Retry` mixin automatically retries failed actions using exponential backoff. When an error occurs in the `reduce()` method, the action is re-executed with progressively increasing delays between attempts.

## Basic Usage

Add the `Retry` mixin to any action that should automatically retry on failure:

```dart
class LoadDataAction extends AppAction with Retry {
  Future<AppState?> reduce() async {
    var data = await fetchDataFromServer();
    return state.copy(data: data);
  }
}
```

With this mixin:
- If the action fails, it automatically retries up to 3 times (default)
- Each retry waits longer than the previous (exponential backoff)
- If all retries fail, the original error is thrown

## Configuration Parameters

Override these getters to customize retry behavior:

```dart
class LoadDataAction extends AppAction with Retry {

  // Delay before first retry (default: 350ms)
  int get initialDelay => 500;

  // Multiplier for delay growth (default: 2)
  int get multiplier => 2;

  // Maximum retry attempts (default: 3)
  int get maxRetries => 5;

  // Upper limit on delay to prevent excessive waits (default: 5000ms)
  int get maxDelay => 10000;

  Future<AppState?> reduce() async {
    var data = await fetchDataFromServer();
    return state.copy(data: data);
  }
}
```

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `initialDelay` | 350 ms | Waiting period before first retry |
| `multiplier` | 2 | Growth factor for delays between attempts |
| `maxRetries` | 3 | Maximum retry count (total executions = maxRetries + 1) |
| `maxDelay` | 5 sec | Upper limit on delay to prevent excessive waits |

### Retry Sequence Example

With default settings (initialDelay=350ms, multiplier=2, maxRetries=3):

1. **Initial attempt** - Action runs, fails
2. **Wait 350ms** - First retry, fails
3. **Wait 700ms** - Second retry, fails
4. **Wait 1400ms** - Third retry, fails
5. **Error thrown** - All retries exhausted

## Timing Considerations

Retry delays start **after** the reducer finishes, not from when the action was dispatched. If `reduce()` takes 1 second to fail and `initialDelay` is 350ms, the first retry starts 1.35 seconds after the action began.

## Tracking Retry Attempts

Access the `attempts` getter within your action to know which attempt is currently running:

```dart
class LoadDataAction extends AppAction with Retry {
  Future<AppState?> reduce() async {
    print('Attempt ${attempts + 1}'); // 0-indexed, so first attempt is 0

    if (attempts > 0) {
      // Maybe try a different server on retries
      return state.copy(data: await fetchFromBackupServer());
    }

    return state.copy(data: await fetchFromPrimaryServer());
  }
}
```

## Unlimited Retries

Combine `UnlimitedRetries` with `Retry` to retry indefinitely until the action succeeds:

```dart
class CriticalSyncAction extends AppAction with Retry, UnlimitedRetries {
  Future<AppState?> reduce() async {
    await syncCriticalData();
    return state.copy(syncComplete: true);
  }
}
```

This is equivalent to setting `maxRetries` to `-1`.

**Warning:** Using `await dispatchAndWait(action)` with `UnlimitedRetries` may hang indefinitely if the action continues failing. Use with caution and consider whether the action has a realistic chance of eventually succeeding.

## Important Behavior Notes

### Only reduce() Failures Trigger Retry

The `Retry` mixin only retries when errors occur in the `reduce()` method. Failures in the `before()` method do **not** trigger retries - they fail immediately.

```dart
class LoadDataAction extends AppAction with Retry {

  @override
  Future<void> before() async {
    // Errors here will NOT trigger retry - action fails immediately
    await validatePermissions();
  }

  Future<AppState?> reduce() async {
    // Only errors here trigger the retry mechanism
    return state.copy(data: await fetchData());
  }
}
```

### Actions Become Asynchronous

All actions using the `Retry` mixin become asynchronous, regardless of their original synchronous nature. This is because the retry mechanism needs to wait between attempts.

## Combining with NonReentrant (Best Practice)

Most actions using `Retry` should also include the `NonReentrant` mixin to prevent multiple instances from running simultaneously:

```dart
class SaveDataAction extends AppAction with NonReentrant, Retry {
  Future<AppState?> reduce() async {
    await saveToServer();
    return state.copy(saved: true);
  }
}
```

This prevents scenarios where:
- User clicks "Save" multiple times
- Multiple retry sequences run in parallel
- Server receives duplicate or conflicting requests

## Combining with CheckInternet

For network operations, combine `Retry` with `CheckInternet` to ensure connectivity before attempting the action:

```dart
class FetchUserProfile extends AppAction with CheckInternet, Retry {
  Future<AppState?> reduce() async {
    var profile = await api.getUserProfile();
    return state.copy(profile: profile);
  }
}
```

The `CheckInternet` mixin runs first. If there's no connection, the action fails immediately without attempting retries.

## Common Use Cases

### API Calls with Transient Failures

```dart
class FetchProductsAction extends AppAction with Retry {
  int get maxRetries => 3;
  int get initialDelay => 500;

  Future<AppState?> reduce() async {
    var products = await api.getProducts();
    return state.copy(products: products);
  }
}
```

### Critical Sync Operations

```dart
class SyncPendingChanges extends AppAction with Retry, UnlimitedRetries {
  int get initialDelay => 1000;
  int get maxDelay => 30000; // Cap at 30 seconds between retries

  Future<AppState?> reduce() async {
    await syncService.pushPendingChanges();
    return state.copy(hasPendingChanges: false);
  }
}
```

### Payment Processing with Extended Retries

```dart
class ProcessPaymentAction extends AppAction with NonReentrant, Retry {
  final double amount;

  ProcessPaymentAction(this.amount);

  int get maxRetries => 5;
  int get initialDelay => 1000;
  int get multiplier => 2;
  int get maxDelay => 10000;

  Future<AppState?> reduce() async {
    var result = await paymentGateway.process(amount);
    return state.copy(paymentStatus: result.status);
  }
}
```

## Mixin Compatibility

**Compatible with:**
- `CheckInternet`
- `NoDialog`
- `AbortWhenNoInternet`
- `NonReentrant`
- `Throttle`
- `Debounce`

**Can be combined with:**
- `UnlimitedRetries` (enables infinite retries)

## Full Example with All Options

```dart
class RobustApiAction extends AppAction
    with CheckInternet, NonReentrant, Retry {

  // Retry configuration
  int get initialDelay => 500;     // 500ms before first retry
  int get multiplier => 2;          // Double delay each time
  int get maxRetries => 4;          // Try up to 5 times total
  int get maxDelay => 8000;         // Never wait more than 8 seconds

  Future<AppState?> reduce() async {
    if (attempts > 0) {
      print('Retry attempt $attempts');
    }

    var data = await api.fetchCriticalData();
    return state.copy(data: data);
  }
}
```

## References

URLs from the documentation:
- https://asyncredux.com/sitemap.xml
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/advanced-actions/control-mixins
- https://asyncredux.com/flutter/advanced-actions/wrapping-the-reducer
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/basics/wait-fail-succeed
