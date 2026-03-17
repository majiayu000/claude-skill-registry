---
name: flutter-test
description: Generate high-quality Flutter tests for BLoC-based applications.
metadata:
  short-description: Generate unit and widget tests using bloc_test and mocktail.
---

Generate Flutter tests following best practices for BLoC-based state management.

## Required Test Dependencies
Ensure the project has these `dev_dependencies` before generating tests:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^10.0.0
  mocktail: ^1.0.4
```

Default mocking stack for this skill remains:
- `bloc_test` for BLoC/Cubit behavior tests.
- `mocktail` for repositories/services and interaction verification.

## Requirements

### General
- Use **Flutter test conventions** and idioms.
- Always separate:
  - **Unit tests** (BLoC, Cubit, business logic)
  - **Widget tests** (UI behavior, rendering, interaction)
- Tests must be **deterministic** and **isolated**.
- Always use **English** for test names and comments.
- Prefer readability and clarity over brevity.

### Unit Test Requirements (State Management)
- Use `bloc_test` for all `Bloc` or `Cubit` testing.
- Tests must:
  - Clearly describe **initial state**, **action**, and **expected states**
  - Use `blocTest<TBloc, TState>`
- Each public event or method must have:
  - At least one **success case**
  - At least one **failure or edge case** (if applicable)
- Avoid testing UI-related logic in unit tests.

- Use `mocktail` for mocking dependencies:
  - Repositories
  - Data sources
  - External services
- **Do NOT** use real implementations in unit tests.

### Widget Test Requirements
- Use `flutter_test` with `WidgetTester`.
- Widget tests must:
  - Verify **rendered UI states** (loading, success, error)
  - Test **user interactions** (tap, input, scroll)
  - Assert **visible behavior**, not implementation details
- Inject mocked BLoCs using:
  - `BlocProvider.value`
  - or `MultiBlocProvider`
- Avoid golden tests unless explicitly requested.

### Assertions & Style
- Prefer:
  - `expect` for standard assertions
  - `verify` / `verifyNever` from `mocktail` for interaction checks
- Avoid excessive `pumpAndSettle`; prefer explicit `pump` durations.
- Use descriptive test names:
  - `"emits [Loading, Success] when fetch is successful"`

## Coverage Guidelines
- Aim for **minimum ≥80% coverage** at the package or feature level.
- Coverage must include:
  - All major BLoC state transitions
  - At least one widget test per critical UI state
- Do not introduce meaningless assertions just to increase coverage.
- If ≥80% coverage cannot be achieved without testing private details:
  - Explain briefly why
  - Suggest a refactor (e.g. extract logic into BLoC or service)

## Output Expectations
- Generate **complete and runnable** test files.
- Follow Flutter naming conventions:
  - `*_bloc_test.dart`
  - `*_widget_test.dart`
- Include all required imports.
- Separate Arrange / Act / Assert clearly.
- Output test code only unless explanation is explicitly requested.

## When to Load References
- Detailed technical reference: [REFERENCE.md](./references/REFERENCE.md).

### Unit Tests (BLoC / Cubit)
- BLoC testing patterns: [unit_bloc_testing.md](./references/unit_bloc_testing.md)
- Mocking with mocktail: [mocktail.md](./references/mocktail.md)

### Widget Tests
- Widget testing fundamentals: [widget_testing.md](./references/widget_testing.md)
- Testing BLoC-powered widgets: [bloc_widget_testing.md](./references/bloc_widget_testing.md)

## Additional Guidelines
- Prefer testing **behavior over structure**.
- Avoid testing Flutter framework internals.
- Do not mock Flutter SDK classes unless unavoidable.
- If a widget is hard to test:
  - Explain why briefly
  - Suggest architectural improvement (e.g. push logic into BLoC).

For auth output contract and concrete auth examples, see [REFERENCE.md](./references/REFERENCE.md).
