---
name: riverpod-testing
description: Test Riverpod providers and widgets; ProviderContainer.test, unit tests, widget tests with ProviderScope, tester.container(), mocking with overrides, container.listen for auto-dispose, awaiting .future. Use when writing unit or widget tests for Riverpod code, mocking providers, or testing with overrides. Use this skill when the user asks about testing Riverpod, mocking providers, or ProviderContainer in tests.
---

# Riverpod — Testing

## Instructions

Riverpod is designed for testability: isolate state per test, mock via overrides, and keep the test environment close to production.

### Unit tests (no Flutter)

Use **ProviderContainer.test()** to create a container for the test. Do not share containers between tests.

```dart
void main() {
  test('Some description', () {
    final container = ProviderContainer.test();
    expect(container.read(provider), equals('some value'));
  });
}
```

- **container.read(provider)** — Read current value.
- **container.listen(provider, (prev, next) {})** — Listen and get a subscription; use **subscription.read()** to read. Prefer listen when the provider is auto-dispose so it is not disposed mid-test.

```dart
final subscription = container.listen<String>(provider, (_, _) {});
expect(subscription.read(), 'Some value');
```

### Widget tests

Wrap the widget under test in **ProviderScope**:

```dart
testWidgets('Some description', (tester) async {
  await tester.pumpWidget(
    const ProviderScope(child: YourWidgetYouWantToTest()),
  );
});
```

To interact with providers in the test, get the container with **tester.container()**:

```dart
final container = tester.container();
expect(container.read(provider), 'some value');
```

### Mocking providers

Use **overrides** on ProviderContainer or ProviderScope. All providers can be overridden without extra setup.

```dart
final container = ProviderContainer.test(
  overrides: [
    exampleProvider.overrideWith((ref) => 'Hello from tests'),
  ],
);

// Or in widget tests:
await tester.pumpWidget(
  ProviderScope(
    overrides: [exampleProvider.overrideWith((ref) => 'Hello from tests')],
    child: const YourWidgetYouWantToTest(),
  ),
);
```

See riverpod-overrides for family overrides and other override methods.

### Awaiting async providers

Read **provider.future** to get a Future that completes with the provider value; use with expectLater:

```dart
await expectLater(
  container.read(provider.future),
  completion('some value'),
);
```

### Listening / spying

Use **container.listen(provider, callback)** and assert on the callback arguments or collect values in a list for assertions. Works with mockito/mocktail verify patterns.

### Mocking Notifiers

Prefer mocking a dependency (e.g. repository) the Notifier uses rather than mocking the Notifier. If you must mock a Notifier, **subclass** it (do not implement), so the mock extends the original base class. With code generation, the mock usually needs to live in the same file as the Notifier to access the generated base class.

See riverpod-overrides and the official docs for more examples.
