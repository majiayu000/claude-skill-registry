---
name: asyncredux-wait-fail-succeed
description: Show loading states and handle action failures in widgets. Covers `isWaiting(ActionType)` for spinners, `isFailed(ActionType)` for error states, `exceptionFor(ActionType)` for error messages, and `clearExceptionFor()` to reset failure states.
---

# AsyncRedux Wait, Fail, Succeed

AsyncRedux provides context extension methods to track async action states: waiting (in progress), failed (error), and succeeded (complete). These are essential for showing spinners, error messages, and success states in the UI.

## Four Core Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `isWaiting(ActionType)` | `bool` | True if the action is currently running |
| `isFailed(ActionType)` | `bool` | True if the action recently failed |
| `exceptionFor(ActionType)` | `UserException?` | The exception from a failed action |
| `clearExceptionFor(ActionType)` | `void` | Manually clears stored exception |

## Showing a Loading Spinner

Use `isWaiting()` to display a spinner while an action runs:

```dart
Widget build(BuildContext context) {
  if (context.isWaiting(FetchDataAction)) {
    return CircularProgressIndicator();
  }
  return Text('Data: ${context.state.data}');
}
```

The widget automatically rebuilds when the action starts and completes.

## Showing Error States

Use `isFailed()` and `exceptionFor()` to display error messages:

```dart
Widget build(BuildContext context) {
  if (context.isFailed(FetchDataAction)) {
    var exception = context.exceptionFor(FetchDataAction);
    return Text('Error: ${exception?.message}');
  }
  return Text('Data: ${context.state.data}');
}
```

## Combined Pattern: Loading, Error, and Success

The typical pattern handles all three states:

```dart
Widget build(BuildContext context) {
  // Loading state
  if (context.isWaiting(GetItemsAction)) {
    return Center(child: CircularProgressIndicator());
  }

  // Error state with retry
  if (context.isFailed(GetItemsAction)) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text('Failed to load items'),
        Text(context.exceptionFor(GetItemsAction)?.message ?? ''),
        ElevatedButton(
          onPressed: () => context.dispatch(GetItemsAction()),
          child: Text('Retry'),
        ),
      ],
    );
  }

  // Success state
  return ListView.builder(
    itemCount: context.state.items.length,
    itemBuilder: (context, index) => ListTile(
      title: Text(context.state.items[index].name),
    ),
  );
}
```

## Automatic Error Clearing

When an action is dispatched again, any previous error for that action type is automatically cleared. This means:

- User sees error
- User taps "Retry" which dispatches the action again
- `isFailed()` becomes false immediately
- `isWaiting()` becomes true
- If action succeeds, widget shows success state
- If action fails again, `isFailed()` becomes true with the new exception

## Manual Error Clearing

Use `clearExceptionFor()` when you need to dismiss an error without retrying:

```dart
Widget build(BuildContext context) {
  if (context.isFailed(SubmitFormAction)) {
    return AlertDialog(
      title: Text('Error'),
      content: Text(context.exceptionFor(SubmitFormAction)?.message ?? ''),
      actions: [
        TextButton(
          onPressed: () {
            context.clearExceptionFor(SubmitFormAction);
          },
          child: Text('Dismiss'),
        ),
        TextButton(
          onPressed: () => context.dispatch(SubmitFormAction()),
          child: Text('Retry'),
        ),
      ],
    );
  }
  // ...
}
```

## How Actions Fail

Actions fail when they throw an error in `before()` or `reduce()`. Use `UserException` for user-facing errors:

```dart
class FetchDataAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    final response = await api.fetchData();

    if (response.statusCode == 404) {
      throw UserException('Data not found.');
    }

    if (response.statusCode != 200) {
      throw UserException('Failed to load data. Please try again.');
    }

    return state.copy(data: response.data);
  }
}
```

## Checking Multiple Actions

You can check multiple action types for waiting or failure:

```dart
Widget build(BuildContext context) {
  // Check if any of several actions are running
  bool isLoading = context.isWaiting(FetchUserAction) ||
                   context.isWaiting(FetchSettingsAction);

  if (isLoading) {
    return CircularProgressIndicator();
  }

  // Check for any failures
  if (context.isFailed(FetchUserAction)) {
    return Text('Failed to load user');
  }
  if (context.isFailed(FetchSettingsAction)) {
    return Text('Failed to load settings');
  }

  return MyContent();
}
```

## Pull-to-Refresh Integration

Combine with `dispatchAndWait()` for refresh indicators:

```dart
class MyListWidget extends StatelessWidget {
  Future<void> _onRefresh(BuildContext context) {
    return context.dispatchAndWait(RefreshItemsAction());
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: () => _onRefresh(context),
      child: ListView.builder(
        itemCount: context.state.items.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(context.state.items[index].name),
        ),
      ),
    );
  }
}
```

## Complete Example

```dart
class LoadProductsAction extends ReduxAction<AppState> {
  @override
  Future<AppState?> reduce() async {
    final products = await api.fetchProducts();
    if (products.isEmpty) {
      throw UserException('No products available.');
    }
    return state.copy(products: products);
  }
}

class ProductsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Products')),
      body: _buildBody(context),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.dispatch(LoadProductsAction()),
        child: Icon(Icons.refresh),
      ),
    );
  }

  Widget _buildBody(BuildContext context) {
    if (context.isWaiting(LoadProductsAction)) {
      return Center(child: CircularProgressIndicator());
    }

    if (context.isFailed(LoadProductsAction)) {
      final error = context.exceptionFor(LoadProductsAction);
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.error, size: 64, color: Colors.red),
            SizedBox(height: 16),
            Text(error?.message ?? 'An error occurred'),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => context.dispatch(LoadProductsAction()),
              child: Text('Try Again'),
            ),
          ],
        ),
      );
    }

    final products = context.state.products;
    if (products.isEmpty) {
      return Center(child: Text('No products yet. Tap refresh to load.'));
    }

    return ListView.builder(
      itemCount: products.length,
      itemBuilder: (context, index) => ListTile(
        title: Text(products[index].name),
        subtitle: Text('\$${products[index].price}'),
      ),
    );
  }
}
```

## References

URLs from the documentation:
- https://asyncredux.com/flutter/basics/wait-fail-succeed
- https://asyncredux.com/flutter/miscellaneous/advanced-waiting
- https://asyncredux.com/flutter/advanced-actions/action-status
- https://asyncredux.com/flutter/basics/failed-actions
- https://asyncredux.com/flutter/advanced-actions/errors-thrown-by-actions
- https://asyncredux.com/flutter/basics/using-the-store-state
- https://asyncredux.com/flutter/basics/dispatching-actions
- https://asyncredux.com/flutter/basics/async-actions
- https://asyncredux.com/flutter/miscellaneous/refresh-indicators
