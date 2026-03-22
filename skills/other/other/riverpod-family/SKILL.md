---
name: riverpod-family
description: Use Riverpod family providers to pass parameters and cache per parameter; FutureProvider.family, NotifierProvider.family, autoDispose with family, overriding in tests. Use when fetching data by ID, pagination, or any provider that depends on a parameter. Use this skill when the user asks about family, provider parameters, or caching by ID.
---

# Riverpod — Family

## Instructions

**Family** lets a single provider have multiple independent states, one per parameter combination (like a Map from parameter to state). Use it for API calls that depend on an ID, query, or page number.

### Creating a family (functional)

Add `.family` and an extra type parameter for the argument. The provider function receives `(ref, param)`:

```dart
final userProvider = FutureProvider.autoDispose.family<User, String>((ref, id) async {
  final dio = Dio();
  final response = await dio.get('https://api.example.com/users/$id');
  return User.fromJson(response.data);
});
```

With code generation, add parameters to the function; the generated provider accepts arguments: `userProvider(id)`.

### Creating a family (Notifier)

Use `NotifierProvider.family` / `AsyncNotifierProvider.family` (and `.autoDispose.family`). The Notifier must have a constructor that stores the parameter:

```dart
final userProvider = AsyncNotifierProvider.autoDispose.family<UserNotifier, User, String>(
  UserNotifier.new,
);

class UserNotifier extends AsyncNotifier<User> {
  UserNotifier(this.id);
  final String id;

  @override
  Future<User> build() async {
    final dio = Dio();
    final response = await dio.get('https://api.example.com/users/$id');
    return User.fromJson(response.data);
  }
}
```

### Using a family

Pass the parameter when watching or reading:

```dart
final user = ref.watch(userProvider('123'));
final other = ref.watch(userProvider('456'));  // independent state
```

Parameters must have consistent **==** and **hashCode**. Do not use mutable or list/map literals as parameters (e.g. `ref.watch(myProvider([1,2,3]))` is wrong because `[1,2,3] != [1,2,3]`). Prefer primitives or custom classes with ==/hashCode. Enable riverpod_lint provider_parameters rule to catch mistakes.

### Auto-dispose with family

Enable auto-dispose when using family so that when the parameter goes out of use (e.g. user navigates away), that parameter's state can be disposed and you avoid unbounded cache growth.

### Overriding in tests

- Override a single parameter: pass the same parameter to the override.
- Override all parameters: override with a provider that ignores the parameter or returns a fixed value. See riverpod-overrides and the docs for exact syntax.
