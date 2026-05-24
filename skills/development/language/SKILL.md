---
name: Dart Language Patterns
description: Modern Dart standards (3.x+) including null safety and patterns.
metadata:
  labels: [dart, language, idioms]
  triggers:
    files: ['**/*.dart']
    keywords: [sealed, record, switch, pattern, extension, final, late, async, await]
---

# Dart Language Patterns

## **Priority: P0 (CRITICAL)**

Modern Dart standards for safety, performance, and readability.

## Implementation Guidelines

- **Null Safety**: Avoid `!`. Use `?.`, `??`, or short-circuiting. Use `late` only if necessary.
- **Immutability**: Use `final` for all variables. Use `@freezed` for data classes.
- **Pattern Matching (3.x)**: Use `switch (value)` with patterns and destructuring.
- **Records**: Use Records (e.g., `(String, int)`) for returning multiple values.
- **Sealed Classes**: Use `sealed class` for exhaustive state handling in domain logic.
- **Extensions**: Use `extension` to add utility methods to third-party types.
- **Wildcards (3.7+)**: Use `_` for unused variables in declarations and patterns.
- **Tear-offs**: Prefer using tear-offs (e.g., `list.forEach(print)`) over anonymous lambdas (e.g., `list.forEach((e) => print(e))`).
- **Asynchrony**: Prefer `async/await` over raw `Future.then`. Use `unawaited` for fire-and-forget logic if necessary.
- **Collections**: Use `collection-if`, `collection-for`, and spread operators `...`.

## Anti-Patterns

- **No ! Operator**: Do not use the bang operator `!` unless you can prove the value is non-null via `if` or `assert`.
- **No var for members**: Do not use `var` for class members; use `final` or explicit types.
- **No logic in constructors**: Do not perform complex calculations or async work inside constructors.

## Code

```dart
// Sealed class and Switch expression
sealed class Result {}
class Success extends Result { final String data; Success(this.data); }
class Failure extends Result {}

String message(Result r) => switch (r) {
  Success(data: var d) => "Got $d",
  Failure() => "Error",
};
```

## Related Topics

feature-based-clean-architecture | tooling
