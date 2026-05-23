---
name: asyncredux-abort-dispatch
description: Stops an AsyncRedux (Flutter) action from dispatching. Use only when the user mentions abortDispatch(), or explicitly asks to abort or prevent dispatch under certain conditions.
---

# AsyncRedux Aborting the Dispatch

## What is abortDispatch()?

The `abortDispatch()` method is an optional method on `ReduxAction` that lets you
conditionally prevent an action from executing. When this method returns `true`, the
entire action is skipped—`before()`, `reduce()`, and `after()` will NOT run, and state
remains unchanged.

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  bool abortDispatch() {
    // Return true to abort, false to proceed
    return someCondition;
  }

  @override
  AppState? reduce() {
    // Only runs if abortDispatch() returned false
    return state.copy(/* ... */);
  }
}
```

## Basic Usage

The simplest use case is checking a condition before allowing the action to proceed:

```dart
class LoadUserProfile extends ReduxAction<AppState> {
  @override
  bool abortDispatch() => state.user == null;

  @override
  Future<AppState?> reduce() async {
    // Only runs if user is logged in
    final profile = await api.fetchProfile(state.user!.id);
    return state.copy(profile: profile);
  }
}
```

## Action Lifecycle with abortDispatch()

When `abortDispatch()` returns `true`, the complete action lifecycle is skipped:

```dart
class MyAction extends ReduxAction<AppState> {
  @override
  bool abortDispatch() => state.shouldSkip;  // If true:

  @override
  void before() {
    // NOT called when aborted
  }

  @override
  AppState? reduce() {
    // NOT called when aborted
  }

  @override
  void after() {
    // NOT called when aborted
  }
}
```

This differs from throwing an error in `before()`, which would still cause `after()` to
run.

## Authentication Guard Pattern

A common pattern is creating a base action that requires authentication:

```dart
/// Base action that requires an authenticated user
abstract class AuthenticatedAction extends ReduxAction<AppState> {
  @override
  bool abortDispatch() => state.user == null;
}

/// Actions extending this will only run when user is logged in
class FetchUserOrders extends AuthenticatedAction {
  @override
  Future<AppState?> reduce() async {
    // Safe to use state.user! here - abortDispatch ensures it's not null
    final orders = await api.getOrders(state.user!.id);
    return state.copy(orders: orders);
  }
}

class UpdateUserSettings extends AuthenticatedAction {
  final Settings newSettings;
  UpdateUserSettings(this.newSettings);

  @override
  Future<AppState?> reduce() async {
    await api.updateSettings(state.user!.id, newSettings);
    return state.copy(settings: newSettings);
  }
}
```

## Creating Base Actions with Abort Logic

You can combine multiple abort conditions in a base action:

```dart
abstract class AppAction extends ReduxAction<AppState> {
  // Override in subclasses to add action-specific abort logic
  bool shouldAbort() => false;

  @override
  bool abortDispatch() {
    // Global abort conditions
    if (state.isMaintenanceMode) return true;
    if (state.isAppLocked) return true;

    // Action-specific abort conditions
    return shouldAbort();
  }
}

class RefreshData extends AppAction {
  @override
  bool shouldAbort() {
    // Don't refresh if data is still fresh
    return state.lastRefresh != null &&
        DateTime.now().difference(state.lastRefresh!) < Duration(minutes: 5);
  }

  @override
  Future<AppState?> reduce() async {
    final data = await api.fetchData();
    return state.copy(data: data, lastRefresh: DateTime.now());
  }
}
```

## Role-Based Authorization

Use `abortDispatch()` to implement role-based access control:

```dart
abstract class AdminAction extends ReduxAction<AppState> {
  @override
  bool abortDispatch() => state.user?.role != UserRole.admin;
}

class DeleteAllUsers extends AdminAction {
  @override
  Future<AppState?> reduce() async {
    // Only admins can reach this code
    await api.deleteAllUsers();
    return state.copy(users: []);
  }
}
```

## Conditional Feature Actions

Prevent actions when features are disabled:

```dart
class UsePremiumFeature extends ReduxAction<AppState> {
  @override
  bool abortDispatch() => !state.user!.isPremium;

  @override
  AppState? reduce() {
    // Premium-only functionality
    return state.copy(/* ... */);
  }
}
```

## Built-in Mixin: AbortWhenNoInternet

AsyncRedux provides `AbortWhenNoInternet`, a mixin that silently aborts actions when
there's no internet connection:

```dart
class FetchLatestNews extends AppAction with AbortWhenNoInternet {
  @override
  Future<AppState?> reduce() async {
    // Only runs if internet is available
    final news = await api.fetchNews();
    return state.copy(news: news);
  }
}
```

Key characteristics of `AbortWhenNoInternet`:

- No error dialogs are shown
- No exceptions are thrown
- The action is silently cancelled
- Only checks if device internet is on/off (not server availability)

Compare with `CheckInternet` which shows an error dialog instead of silently aborting.

## abortDispatch() vs Throwing in before()

Choose the right approach for your use case:

| Approach                       | `after()` runs? | Shows error?           | Use when             |
|--------------------------------|-----------------|------------------------|----------------------|
| `abortDispatch()` returns true | No              | No                     | Silently skip action |
| Throw in `before()`            | Yes             | Yes (if UserException) | Show error to user   |

```dart
// Silent abort - user doesn't know action was skipped
class SilentRefresh extends ReduxAction<AppState> {
  @override
  bool abortDispatch() => state.isOffline;
  // ...
}

// Visible error - user sees message
class ExplicitRefresh extends ReduxAction<AppState> {
  @override
  void before() {
    if (state.isOffline) {
      throw UserException('Cannot refresh while offline');
    }
  }
  // ...
}
```

## When to Use abortDispatch()

**Good use cases:**

- Authentication guards (action requires logged-in user)
- Authorization checks (action requires specific role/permission)
- Feature flags (action only for premium users)
- Freshness checks (don't refetch if data is recent)
- Maintenance mode (disable certain actions globally)
- Idempotency (skip if action's effect already applied)

**Consider alternatives when:**

- You want the user to see an error message (throw `UserException` in `before()`)
- You need cleanup code to run (use `before()` + `after()` pattern)
- You're implementing rate limiting (use `Throttle` or `Debounce` mixins)
- You're preventing duplicate dispatches (use `NonReentrant` mixin)

## Complete Example

```dart
// Base action with common abort logic
abstract class AppAction extends ReduxAction<AppState> {
  @override
  bool abortDispatch() {
    // Global maintenance mode check
    if (state.maintenanceMode) return true;
    return false;
  }
}

// Authenticated action that also checks maintenance mode
abstract class AuthenticatedAction extends AppAction {
  @override
  bool abortDispatch() {
    // Check parent conditions first
    if (super.abortDispatch()) return true;
    // Then check authentication
    return state.currentUser == null;
  }
}

// Admin action with full authorization chain
abstract class AdminAction extends AuthenticatedAction {
  @override
  bool abortDispatch() {
    if (super.abortDispatch()) return true;
    return state.currentUser?.role != UserRole.admin;
  }
}

// Concrete action using the hierarchy
class BanUser extends AdminAction {
  final String userId;
  BanUser(this.userId);

  @override
  Future<AppState?> reduce() async {
    // Only reaches here if:
    // 1. Not in maintenance mode
    // 2. User is logged in
    // 3. User is an admin
    await api.banUser(userId);
    return state.copy(
      users: state.users.where((u) => u.id != userId).toList(),
    );
  }
}
```

## Important Notes

- `abortDispatch()` is checked before `before()`, `reduce()`, and `after()`
- When aborted, no state changes occur
- The action is silently skipped—no errors are thrown or logged by default
- Use this feature judiciously; the documentation warns it's "a powerful feature" that
  should only be used "if you are sure it is the right solution"

## References

URLs from the documentation:

- https://asyncredux.com/flutter/advanced-actions/aborting-the-dispatch
- https://asyncredux.com/flutter/advanced-actions/redux-action
- https://asyncredux.com/flutter/advanced-actions/before-and-after-the-reducer
- https://asyncredux.com/flutter/advanced-actions/action-status
- https://asyncredux.com/flutter/advanced-actions/control-mixins
- https://asyncredux.com/flutter/advanced-actions/internet-mixins
- https://asyncredux.com/flutter/advanced-actions/action-mixins
- https://asyncredux.com/flutter/basics/actions-and-reducers
- https://asyncredux.com/flutter/basics/action-simplification
