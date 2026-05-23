---
name: asyncredux-async-actions
description: Creates AsyncRedux (Flutter) asynchronous actions for API calls, database operations, and other async work. 
---

# AsyncRedux Async Actions

## Basic Async Action Structure

An action becomes asynchronous when its `reduce()` method returns `Future<AppState?>`
instead of `AppState?`. Use this for database access, API calls, file operations, or any
work requiring `await`.

```dart
class FetchUser extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    final user = await api.fetchUser();
    return state.copy(user: user);
  }
}
```

Unlike traditional Redux requiring middleware, AsyncRedux makes it simple: return a
`Future` and it works.

## Critical Rule: Every Path Must Have await

If the action is async (returns a Future) and changes the state (returns a non-null
state), the framework requires that,  **all execution paths contain at least
one `await`**. Never declare `Future<AppState?>` if you don't actually await something.

### Valid Patterns

```dart
// Simple async with await
Future<AppState?> reduce() async {
  final data = await fetchData();
  return state.copy(data: data);
}

// Using microtask (minimum valid await)
Future<AppState?> reduce() async {
  await microtask;
  return state.copy(timestamp: DateTime.now());
}

// Conditional - both paths have await
Future<AppState?> reduce() async {
  if (state.needsRefresh) {
    return await fetchAndUpdate();
  }
  else return await validateCurrent();
}

// Always returns null
Future<AppState?> reduce() async {
  if (state.needsRefresh) {
    await fetchAndUpdate();
  }  
  
  return null;
}
```

### Invalid Patterns (Will Cause Issues)

```dart
// WRONG: No await at all
Future<AppState?> reduce() async {
  return state.copy(counter: state.counter + 1);
}

// WRONG: await only on some paths
Future<AppState?> reduce() async {
  if (condition) {
    return await fetchData();
  }
  return state; // No await on this path!
}

// WRONG: Calling async function without await
Future<AppState?> reduce() async {
  someAsyncFunction(); // Not awaited
  return state;
}
```

## Using assertUncompletedFuture()

For complex reducers with multiple code paths, add `assertUncompletedFuture()` before the
final return. This catches violations at runtime during development:

```dart
class ComplexAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    if (state.cacheValid) {
      // Complex logic that might accidentally skip await
      return processCache();
    }

    final data = await fetchFromServer();
    final processed = transform(data);

    assertUncompletedFuture(); // Validates at least one await occurred
    return state.copy(data: processed);
  }
}
```

## State Changes During Async Operations

The `state` getter can change after every `await` because other actions may modify state
while yours is waiting:

```dart
class AsyncAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    print(state.counter); // e.g., 5

    await someSlowOperation();

    // state.counter might now be different (e.g., 10)
    // if another action modified it during the await
    print(state.counter);

    return state.copy(counter: state.counter + 1);
  }
}
```

### Using initialState for Comparison

Use `initialState` to access the state as it was when the action was dispatched (never
changes):

```dart
class SafeIncrement extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    final originalCounter = initialState.counter;

    await validateWithServer();

    // Check if state changed while we were waiting
    if (state.counter != originalCounter) {
      // State was modified by another action
      return null; // Abort our change
    }

    return state.copy(counter: state.counter + 1);
  }
}
```

## Dispatching Async Actions

### Fire and Forget

Use `dispatch()` when you don't need to wait for completion:

```dart
context.dispatch(FetchUser());
// Returns immediately, action runs in background
```

### Wait for Completion

Use `dispatchAndWait()` to await the action's completion:

```dart
await context.dispatchAndWait(FetchUser());
// Continues only after action finishes AND state changes
print('User loaded: ${context.state.user.name}');
```

### Dispatch Multiple in Parallel

```dart
// Fire all, don't wait
context.dispatchAll([FetchUser(), FetchSettings(), FetchNotifications()]);

// Fire all and wait for all to complete
await context.dispatchAndWaitAll([FetchUser(), FetchSettings()]);
```

## Showing Loading States

Use `isWaiting()` to show spinners while async actions run:

```dart
Widget build(BuildContext context) {
  if (context.isWaiting(FetchUser)) return CircularProgressIndicator();  
  else return Text('Hello, ${context.state.user.name}');
}
```

## Error Handling

Throw `UserException` for user-facing errors:

```dart
class FetchUser extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    final response = await api.fetchUser();

    if (response.statusCode == 404) 
      throw UserException('User not found.');    

    if (response.statusCode != 200) 
      throw UserException('Failed to load user. Please try again.');    

    return state.copy(user: response.data);
  }
}
```

Check for failures in widgets:

```dart
Widget build(BuildContext context) {
  if (context.isFailed(FetchUser)) {
    return Text('Error: ${context.exceptionFor(FetchUser)?.message}');
  }
  // ...
}
```

## Complete Example

```dart
// Async action with proper error handling
class LoadProducts extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    try {
      final products = await api.fetchProducts();
      return state.copy(products: products, productsLoaded: true);
    } catch (e) {
      throw UserException('Could not load products. Check your connection.');
    }
  }
}

// Widget showing all three states
Widget build(BuildContext context) {
  // Loading state
  if (context.isWaiting(LoadProducts)) {
    return Center(child: CircularProgressIndicator());
  }

  // Error state
  if (context.isFailed(LoadProducts)) {
    return Center(
      child: Column(
        children: [
          Text(context.exceptionFor(LoadProducts)?.message ?? 'Error'),
          ElevatedButton(
            onPressed: () => context.dispatch(LoadProducts()),
            child: Text('Retry'),
          ),
        ],
      ),
    );
  }

  // Success state
  return ListView.builder(
    itemCount: context.state.products.length,
    itemBuilder: (_, i) => ProductTile(context.state.products[i]),
  );
}
```

## Return Type Warning

Never return `FutureOr<AppState?>` directly. AsyncRedux must know if the action is sync or
async:

```dart
// CORRECT
Future<AppState?> reduce() async { ... }

// CORRECT
AppState? reduce() { ... }

// WRONG - throws StoreException
FutureOr<AppState?> reduce() { ... }
```

## References

URLs from the documentation:

- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/basics/actions-and-reducers
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/wait-fail-succeed
