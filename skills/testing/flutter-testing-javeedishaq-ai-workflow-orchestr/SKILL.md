---
description: Flutter testing patterns for Ballee mobile app. Covers unit tests, widget tests, golden tests, integration tests, and mocking with Riverpod.
version: "1.0.0"
updated: "2025-12-22"
---

# Flutter Testing Patterns

Comprehensive guide for testing the Ballee mobile app.

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Unit Tests](#unit-tests)
3. [Widget Tests](#widget-tests)
4. [Golden Tests](#golden-tests)
5. [Integration Tests](#integration-tests)
6. [Mocking with Mocktail](#mocking-with-mocktail)
7. [Testing Riverpod Providers](#testing-riverpod-providers)
8. [Test Organization](#test-organization)

---

## Testing Overview

### Test Pyramid

```
        ╱╲
       ╱  ╲
      ╱ E2E╲         Few integration tests (slow, comprehensive)
     ╱──────╲
    ╱ Widget ╲       Many widget tests (medium speed)
   ╱──────────╲
  ╱   Unit     ╲     Most unit tests (fast, focused)
 ╱──────────────╲
```

### Dependencies

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.0
  riverpod: ^2.6.0  # For ProviderContainer in tests
```

### Running Tests

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/modules/events/domain/event_test.dart

# Run with coverage
flutter test --coverage

# Run in watch mode
flutter test --watch
```

---

## Unit Tests

Test pure Dart logic: domain models, repositories, utilities.

### Domain Model Tests

```dart
// test/modules/events/domain/event_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:apparence_kit/modules/events/domain/event.dart';

void main() {
  group('Event', () {
    test('isUpcoming returns true for future events', () {
      final event = Event(
        id: '1',
        title: 'Swan Lake',
        startDateTime: DateTime.now().add(const Duration(days: 7)),
        status: EventStatus.active,
      );

      expect(event.isUpcoming, isTrue);
    });

    test('isUpcoming returns false for past events', () {
      final event = Event(
        id: '1',
        title: 'Swan Lake',
        startDateTime: DateTime.now().subtract(const Duration(days: 7)),
        status: EventStatus.active,
      );

      expect(event.isUpcoming, isFalse);
    });

    test('fromEntity correctly maps all fields', () {
      final entity = EventEntity(
        id: '123',
        title: 'Test Event',
        startDateTime: DateTime(2025, 6, 15, 19, 0),
        endDateTime: DateTime(2025, 6, 15, 22, 0),
        status: 'active',
        productions: ProductionEntity(id: 'p1', name: 'The Nutcracker'),
        venues: VenueEntity(id: 'v1', name: 'Opera House', city: 'Paris'),
      );

      final event = Event.fromEntity(entity);

      expect(event.id, '123');
      expect(event.title, 'Test Event');
      expect(event.productionName, 'The Nutcracker');
      expect(event.venueName, 'Opera House');
      expect(event.city, 'Paris');
      expect(event.status, EventStatus.active);
    });
  });

  group('EventStatus', () {
    test('fromString parses valid status', () {
      expect(EventStatus.fromString('active'), EventStatus.active);
      expect(EventStatus.fromString('completed'), EventStatus.completed);
    });

    test('fromString returns draft for invalid status', () {
      expect(EventStatus.fromString('invalid'), EventStatus.draft);
      expect(EventStatus.fromString(null), EventStatus.draft);
    });
  });
}
```

### Repository Tests

```dart
// test/modules/events/repositories/events_repository_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockEventsApi extends Mock implements EventsApi {}

void main() {
  late MockEventsApi mockApi;
  late EventsRepository repository;

  setUp(() {
    mockApi = MockEventsApi();
    repository = EventsRepository(api: mockApi);
  });

  group('EventsRepository', () {
    test('getOpenEvents returns mapped domain models', () async {
      // Arrange
      final entities = [
        EventEntity(
          id: '1',
          title: 'Event 1',
          startDateTime: DateTime(2025, 6, 1),
          status: 'active',
        ),
        EventEntity(
          id: '2',
          title: 'Event 2',
          startDateTime: DateTime(2025, 6, 2),
          status: 'active',
        ),
      ];
      when(() => mockApi.getOpenEvents()).thenAnswer((_) async => entities);

      // Act
      final result = await repository.getOpenEvents();

      // Assert
      expect(result, hasLength(2));
      expect(result[0].id, '1');
      expect(result[0].title, 'Event 1');
      expect(result[1].id, '2');
      verify(() => mockApi.getOpenEvents()).called(1);
    });

    test('getById returns null when event not found', () async {
      when(() => mockApi.getById(any())).thenAnswer((_) async => null);

      final result = await repository.getById('nonexistent');

      expect(result, isNull);
    });
  });
}
```

### Result Pattern Tests

```dart
// test/core/data/result_test.dart
void main() {
  group('Result', () {
    test('Ok contains success value', () {
      const result = Ok<int>(42);

      expect(result.isSuccess, isTrue);
      expect(result.isError, isFalse);
      expect(result.valueOrNull, 42);
    });

    test('Err contains error', () {
      final result = Err<int>(NetworkException());

      expect(result.isSuccess, isFalse);
      expect(result.isError, isTrue);
      expect(result.valueOrNull, isNull);
    });

    test('when handles both cases', () {
      const ok = Ok<int>(42);
      final err = Err<int>(NetworkException());

      expect(
        ok.when(ok: (v) => 'value: $v', err: (e) => 'error'),
        'value: 42',
      );
      expect(
        err.when(ok: (v) => 'value: $v', err: (e) => 'error'),
        'error',
      );
    });
  });
}
```

---

## Widget Tests

Test UI components in isolation with `flutter_test`.

### Basic Widget Test

```dart
// test/modules/events/ui/widgets/event_card_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:apparence_kit/modules/events/ui/widgets/event_card.dart';

void main() {
  group('EventCard', () {
    final testEvent = Event(
      id: '1',
      title: 'Swan Lake',
      startDateTime: DateTime(2025, 6, 15, 19, 0),
      venueName: 'Opera House',
      city: 'Paris',
      status: EventStatus.active,
    );

    testWidgets('displays event title', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: EventCard(event: testEvent),
          ),
        ),
      );

      expect(find.text('Swan Lake'), findsOneWidget);
    });

    testWidgets('displays venue and city', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: EventCard(event: testEvent),
          ),
        ),
      );

      expect(find.text('Opera House'), findsOneWidget);
      expect(find.text('Paris'), findsOneWidget);
    });

    testWidgets('calls onTap when pressed', (tester) async {
      var tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: EventCard(
              event: testEvent,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType(EventCard));
      await tester.pumpAndSettle();

      expect(tapped, isTrue);
    });
  });
}
```

### Widget Test with Riverpod

```dart
// test/modules/events/ui/events_list_page_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockEventsRepository extends Mock implements EventsRepository {}

void main() {
  late MockEventsRepository mockRepository;

  setUp(() {
    mockRepository = MockEventsRepository();
  });

  Widget buildTestWidget() {
    return ProviderScope(
      overrides: [
        eventsRepositoryProvider.overrideWithValue(mockRepository),
      ],
      child: const MaterialApp(
        home: EventsListPage(),
      ),
    );
  }

  group('EventsListPage', () {
    testWidgets('shows loading indicator while fetching', (tester) async {
      when(() => mockRepository.getOpenEvents()).thenAnswer(
        (_) => Future.delayed(const Duration(seconds: 1), () => []),
      );

      await tester.pumpWidget(buildTestWidget());

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows events when loaded', (tester) async {
      final events = [
        Event(
          id: '1',
          title: 'Swan Lake',
          startDateTime: DateTime(2025, 6, 15),
          status: EventStatus.active,
        ),
      ];
      when(() => mockRepository.getOpenEvents()).thenAnswer((_) async => events);

      await tester.pumpWidget(buildTestWidget());
      await tester.pumpAndSettle();

      expect(find.text('Swan Lake'), findsOneWidget);
    });

    testWidgets('shows error message on failure', (tester) async {
      when(() => mockRepository.getOpenEvents())
          .thenThrow(Exception('Network error'));

      await tester.pumpWidget(buildTestWidget());
      await tester.pumpAndSettle();

      expect(find.text('Error: Exception: Network error'), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);
    });

    testWidgets('retries on button press', (tester) async {
      var callCount = 0;
      when(() => mockRepository.getOpenEvents()).thenAnswer((_) async {
        callCount++;
        if (callCount == 1) throw Exception('First failure');
        return [];
      });

      await tester.pumpWidget(buildTestWidget());
      await tester.pumpAndSettle();

      await tester.tap(find.text('Retry'));
      await tester.pumpAndSettle();

      expect(callCount, 2);
    });
  });
}
```

### Testing Form Widgets

```dart
testWidgets('validates required fields', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(home: ProfileForm()),
  );

  // Leave fields empty and submit
  await tester.tap(find.text('Save'));
  await tester.pumpAndSettle();

  expect(find.text('First name is required'), findsOneWidget);
  expect(find.text('Last name is required'), findsOneWidget);
});

testWidgets('submits valid form', (tester) async {
  await tester.pumpWidget(
    const MaterialApp(home: ProfileForm()),
  );

  await tester.enterText(find.byKey(const Key('firstName')), 'John');
  await tester.enterText(find.byKey(const Key('lastName')), 'Doe');
  await tester.tap(find.text('Save'));
  await tester.pumpAndSettle();

  // Verify submission
  expect(find.text('Profile saved'), findsOneWidget);
});
```

---

## Golden Tests

Visual regression tests that compare widget renders against reference images.

### Setup

```dart
// test/golden_test_helper.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

Widget buildGoldenTestWidget(Widget child) {
  return ProviderScope(
    child: MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.light(),
      home: Material(child: child),
    ),
  );
}
```

### Golden Test

```dart
// test/modules/events/ui/widgets/event_card_golden_test.dart
import 'package:flutter_test/flutter_test.dart';

import '../../../golden_test_helper.dart';

void main() {
  group('EventCard Golden Tests', () {
    final testEvent = Event(
      id: '1',
      title: 'Swan Lake',
      startDateTime: DateTime(2025, 6, 15, 19, 0),
      productionName: 'The Royal Ballet',
      venueName: 'Opera House',
      city: 'Paris',
      status: EventStatus.active,
    );

    testWidgets('renders correctly', (tester) async {
      await tester.pumpWidget(
        buildGoldenTestWidget(
          SizedBox(
            width: 400,
            child: EventCard(event: testEvent),
          ),
        ),
      );

      await expectLater(
        find.byType(EventCard),
        matchesGoldenFile('goldens/event_card.png'),
      );
    });

    testWidgets('renders interested state', (tester) async {
      await tester.pumpWidget(
        buildGoldenTestWidget(
          SizedBox(
            width: 400,
            child: EventCard(
              event: testEvent,
              isInterested: true,
            ),
          ),
        ),
      );

      await expectLater(
        find.byType(EventCard),
        matchesGoldenFile('goldens/event_card_interested.png'),
      );
    });
  });
}
```

### Update Golden Files

```bash
# Generate/update golden files
flutter test --update-goldens

# Specific test
flutter test test/modules/events/ui/widgets/event_card_golden_test.dart --update-goldens
```

### CI Configuration

```yaml
# .github/workflows/test.yml
- name: Run golden tests
  run: flutter test --tags=golden
  env:
    FLUTTER_TEST_HEADLESS: true
```

---

## Integration Tests

End-to-end tests running on device/emulator.

### Setup

```yaml
# pubspec.yaml
dev_dependencies:
  integration_test:
    sdk: flutter
```

### Test Structure

```
integration_test/
├── app_test.dart
├── robots/
│   ├── login_robot.dart
│   └── events_robot.dart
└── test_data/
    └── fixtures.dart
```

### Integration Test

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:apparence_kit/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('End-to-end test', () {
    testWidgets('login flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Navigate to login
      await tester.tap(find.text('Sign In'));
      await tester.pumpAndSettle();

      // Enter credentials
      await tester.enterText(
        find.byKey(const Key('email')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(const Key('password')),
        'password123',
      );

      // Submit
      await tester.tap(find.text('Sign In'));
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Verify home screen
      expect(find.text('Welcome'), findsOneWidget);
    });
  });
}
```

### Robot Pattern

```dart
// integration_test/robots/events_robot.dart
class EventsRobot {
  final WidgetTester tester;

  EventsRobot(this.tester);

  Future<void> navigateToEvents() async {
    await tester.tap(find.byIcon(Icons.event));
    await tester.pumpAndSettle();
  }

  Future<void> tapEvent(String title) async {
    await tester.tap(find.text(title));
    await tester.pumpAndSettle();
  }

  Future<void> expressInterest() async {
    await tester.tap(find.text('Interested'));
    await tester.pumpAndSettle();
  }

  void expectEventVisible(String title) {
    expect(find.text(title), findsOneWidget);
  }
}

// Usage
testWidgets('can express interest in event', (tester) async {
  app.main();
  await tester.pumpAndSettle();

  final robot = EventsRobot(tester);
  await robot.navigateToEvents();
  await robot.tapEvent('Swan Lake');
  await robot.expressInterest();

  robot.expectEventVisible('You are interested!');
});
```

### Run Integration Tests

```bash
# On connected device
flutter test integration_test

# On specific device
flutter test integration_test --device-id=<device-id>

# With Firebase Test Lab
flutter build apk --debug
gcloud firebase test android run \
  --type instrumentation \
  --app build/app/outputs/apk/debug/app-debug.apk \
  --test build/app/outputs/apk/androidTest/debug/app-debug-androidTest.apk
```

---

## Mocking with Mocktail

### Setup

```dart
// Create mock
class MockEventsApi extends Mock implements EventsApi {}

// Register fallback values for complex types
setUpAll(() {
  registerFallbackValue(Event.empty());
  registerFallbackValue(InterestLevel.interested);
});
```

### Stubbing

```dart
// Return value
when(() => mockApi.getEvents()).thenAnswer((_) async => [testEvent]);

// Throw exception
when(() => mockApi.getEvents()).thenThrow(Exception('Network error'));

// Return based on arguments
when(() => mockApi.getById(any())).thenAnswer((invocation) async {
  final id = invocation.positionalArguments[0] as String;
  return events.firstWhereOrNull((e) => e.id == id);
});

// Multiple calls return different values
var callCount = 0;
when(() => mockApi.getEvents()).thenAnswer((_) async {
  callCount++;
  return callCount == 1 ? [] : [testEvent];
});
```

### Verification

```dart
// Verify called
verify(() => mockApi.getEvents()).called(1);

// Verify called with arguments
verify(() => mockApi.getById('123')).called(1);

// Verify never called
verifyNever(() => mockApi.deleteEvent(any()));

// Capture arguments
final captured = verify(() => mockApi.updateEvent(captureAny())).captured;
expect(captured.first.title, 'Updated Title');
```

---

## Testing Riverpod Providers

### Using ProviderContainer

```dart
// test/modules/events/providers/events_list_notifier_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:riverpod/riverpod.dart';
import 'package:mocktail/mocktail.dart';

class MockEventsRepository extends Mock implements EventsRepository {}

void main() {
  late ProviderContainer container;
  late MockEventsRepository mockRepository;

  setUp(() {
    mockRepository = MockEventsRepository();
    container = ProviderContainer(
      overrides: [
        eventsRepositoryProvider.overrideWithValue(mockRepository),
      ],
    );
  });

  tearDown(() {
    container.dispose();
  });

  group('EventsListNotifier', () {
    test('loads events on build', () async {
      final events = [
        Event(id: '1', title: 'Event 1', startDateTime: DateTime.now(), status: EventStatus.active),
      ];
      when(() => mockRepository.getOpenEvents()).thenAnswer((_) async => events);

      // Wait for async build
      await container.read(eventsListNotifierProvider.future);

      final state = container.read(eventsListNotifierProvider).value!;
      expect(state.events, hasLength(1));
      expect(state.events.first.title, 'Event 1');
    });

    test('setFilter updates state', () async {
      when(() => mockRepository.getOpenEvents()).thenAnswer((_) async => []);
      await container.read(eventsListNotifierProvider.future);

      container.read(eventsListNotifierProvider.notifier)
          .setFilter(EventFilter.interested);

      expect(
        container.read(eventsListNotifierProvider).value!.filter,
        EventFilter.interested,
      );
    });

    test('refresh invalidates and refetches', () async {
      when(() => mockRepository.getOpenEvents()).thenAnswer((_) async => []);
      await container.read(eventsListNotifierProvider.future);

      await container.read(eventsListNotifierProvider.notifier).refresh();

      verify(() => mockRepository.getOpenEvents()).called(2); // Initial + refresh
    });
  });
}
```

### Testing Family Providers

```dart
test('EventDetailNotifier loads specific event', () async {
  final event = Event(id: '123', title: 'Test', startDateTime: DateTime.now(), status: EventStatus.active);
  when(() => mockRepository.getById('123')).thenAnswer((_) async => event);

  final result = await container.read(
    eventDetailNotifierProvider('123').future,
  );

  expect(result.id, '123');
  expect(result.title, 'Test');
});
```

### Testing Async Mutations

```dart
test('expressInterest updates optimistically then confirms', () async {
  when(() => mockRepository.getOpenEvents()).thenAnswer((_) async => [testEvent]);
  when(() => mockRepository.updateParticipation(any(), any()))
      .thenAnswer((_) async {});

  await container.read(eventsListNotifierProvider.future);

  // Start mutation
  final future = container
      .read(eventsListNotifierProvider.notifier)
      .expressInterest('1', InterestLevel.interested);

  // Check optimistic update immediately
  expect(
    container.read(eventsListNotifierProvider).value!.events.first.interestLevel,
    InterestLevel.interested,
  );

  // Wait for completion
  await future;

  verify(() => mockRepository.updateParticipation('1', InterestLevel.interested)).called(1);
});
```

---

## Test Organization

### Folder Structure

```
test/
├── core/
│   ├── data/
│   │   └── result_test.dart
│   └── widgets/
│       └── loading_indicator_test.dart
├── modules/
│   └── events/
│       ├── domain/
│       │   └── event_test.dart
│       ├── repositories/
│       │   └── events_repository_test.dart
│       ├── providers/
│       │   └── events_list_notifier_test.dart
│       └── ui/
│           ├── widgets/
│           │   ├── event_card_test.dart
│           │   └── event_card_golden_test.dart
│           └── events_list_page_test.dart
├── fixtures/
│   └── test_events.dart
└── helpers/
    ├── pump_app.dart
    └── mock_providers.dart
```

### Shared Test Fixtures

```dart
// test/fixtures/test_events.dart
final testEvent = Event(
  id: '1',
  title: 'Swan Lake',
  startDateTime: DateTime(2025, 6, 15, 19, 0),
  endDateTime: DateTime(2025, 6, 15, 22, 0),
  productionName: 'The Royal Ballet',
  venueName: 'Opera House',
  city: 'Paris',
  status: EventStatus.active,
);

final testEvents = [
  testEvent,
  Event(
    id: '2',
    title: 'The Nutcracker',
    startDateTime: DateTime(2025, 12, 20, 14, 0),
    status: EventStatus.active,
  ),
];
```

### Test Helpers

```dart
// test/helpers/pump_app.dart
extension PumpApp on WidgetTester {
  Future<void> pumpApp(
    Widget widget, {
    List<Override> overrides = const [],
  }) async {
    await pumpWidget(
      ProviderScope(
        overrides: overrides,
        child: MaterialApp(home: widget),
      ),
    );
  }
}

// Usage
await tester.pumpApp(
  const EventCard(event: testEvent),
  overrides: [
    eventsRepositoryProvider.overrideWithValue(mockRepository),
  ],
);
```

### Test Tags

```dart
// Run specific categories
@Tags(['golden'])
void main() {
  // Golden tests only
}

// dart_test.yaml
tags:
  golden:
    skip: "Golden tests require specific environment"
```

```bash
# Run only golden tests
flutter test --tags=golden

# Exclude golden tests
flutter test --exclude-tags=golden
```

---

## Quick Reference

### Common Assertions

```dart
expect(value, equals(expected));
expect(value, isNull);
expect(value, isNotNull);
expect(list, hasLength(3));
expect(list, contains(item));
expect(list, isEmpty);
expect(future, completes);
expect(future, throwsA(isA<Exception>()));
expect(find.text('Hello'), findsOneWidget);
expect(find.byType(Button), findsNothing);
```

### Common Finders

```dart
find.text('Hello')
find.byType(EventCard)
find.byKey(const Key('myKey'))
find.byIcon(Icons.add)
find.byWidgetPredicate((w) => w is Text && w.data!.contains('Hello'))
find.descendant(of: find.byType(Card), matching: find.text('Title'))
```

### Common Actions

```dart
await tester.tap(finder);
await tester.longPress(finder);
await tester.enterText(finder, 'text');
await tester.drag(finder, const Offset(0, -300));
await tester.pump();              // Single frame
await tester.pumpAndSettle();     // Until animations complete
await tester.pump(Duration(seconds: 1)); // Specific duration
```
