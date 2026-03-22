---
name: riverpod-overrides
description: Override Riverpod providers for tests, debugging, or environment-specific behavior; ProviderScope and ProviderContainer overrides, overrideWith, overrideWithValue. Use when mocking providers in tests, injecting different implementations, or scoping provider behavior. Use this skill when the user asks about overrides, testing Riverpod, or mocking providers.
---

# Riverpod — Provider overrides

## Instructions

All providers can be **overridden** to change their behavior. Overrides are set on the **container** (ProviderScope in Flutter, ProviderContainer in Dart) via the `overrides` parameter. Use overrides for testing, debugging, different environments, or scoping (see riverpod-scoping).

### Where to set overrides

- **Flutter:** Pass `overrides` to `ProviderScope` (usually at the root or around a subtree).
- **Dart:** Pass `overrides` to `ProviderContainer`.

### Override methods

Each provider type exposes methods whose names start with `overrideWith`, for example:

- **overrideWith** — Provide a new implementation (e.g. a function that returns a value or builds state).
- **overrideWithValue** — Replace with a fixed value (e.g. for FutureProvider/StreamProvider).
- **overrideWithBuild** — Custom build logic (e.g. for StreamProvider).

Check the provider's API for the exact method (e.g. `Provider.overrideWith`, `FutureProvider.overrideWithValue`).

### Example: override a counter

```dart
// Flutter
void main() {
  runApp(
    ProviderScope(
      overrides: [
        counterProvider.overrideWith((ref) => 42),
      ],
      child: MyApp(),
    ),
  );
}

// Dart
final container = ProviderContainer(
  overrides: [
    counterProvider.overrideWith((ref) => 42),
  ],
);
```

### Family overrides

- **Single parameter:** Override one specific argument: `userProvider('123').overrideWith((ref) => User(name: 'User 123'))`.
- **All parameters:** Override the whole family: `userProvider.overrideWith((ref, arg) => User(name: 'User $arg'))`.

See riverpod-family and riverpod-testing for more test patterns.
