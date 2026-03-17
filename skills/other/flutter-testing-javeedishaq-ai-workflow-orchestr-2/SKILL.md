# Flutter Testing Patterns

Comprehensive testing patterns for Flutter applications.

> **Template Usage:** Customize for your state management (Riverpod, Bloc, Provider) and testing preferences.

## Test Structure

```
test/
├── unit/                    # Pure Dart logic tests
│   ├── models/
│   ├── repositories/
│   └── utils/
├── widget/                  # Widget tests
│   ├── screens/
│   └── components/
├── golden/                  # Visual regression tests
│   └── screenshots/
├── integration/             # Full app tests
│   └── flows/
├── fixtures/                # Test data
│   ├── json/
│   └── mocks/
└── helpers/                 # Test utilities
    ├── pump_app.dart
    ├── mocks.dart
    └── finders.dart
```

## Unit Tests

### Model Tests

```dart
// test/unit/models/user_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/modules/user/domain/models/user.dart';

void main() {
  group('User', () {
    test('fromJson creates valid User', () {
      final json = {
        'id': '123',
        'email': 'test@example.com',
        'name': 'Test User',
        'is_verified': true,
      };

      final user = User.fromJson(json);

      expect(user.id, '123');
      expect(user.email, 'test@example.com');
      expect(user.name, 'Test User');
      expect(user.isVerified, true);
    });

    test('toJson produces valid JSON', () {
      const user = User(
        id: '123',
        email: 'test@example.com',
        name: 'Test User',
      );

      final json = user.toJson();

      expect(json['id'], '123');
      expect(json['email'], 'test@example.com');
    });

    test('copyWith creates modified copy', () {
      const user = User(id: '123', email: 'test@example.com');

      final updated = user.copyWith(name: 'New Name');

      expect(updated.name, 'New Name');
      expect(updated.id, user.id);
      expect(updated.email, user.email);
    });

    test('equality works correctly', () {
      const user1 = User(id: '123', email: 'test@example.com');
      const user2 = User(id: '123', email: 'test@example.com');
      const user3 = User(id: '456', email: 'other@example.com');

      expect(user1, equals(user2));
      expect(user1, isNot(equals(user3)));
    });
  });
}
```

### Repository Tests

```dart
// test/unit/repositories/user_repository_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

class MockSupabaseClient extends Mock implements SupabaseClient {}
class MockSupabaseQueryBuilder extends Mock implements SupabaseQueryBuilder {}
class MockPostgrestFilterBuilder extends Mock implements PostgrestFilterBuilder {}

void main() {
  late MockSupabaseClient mockClient;
  late UserRepository repository;

  setUp(() {
    mockClient = MockSupabaseClient();
    repository = SupabaseUserRepository(mockClient);
  });

  group('UserRepository', () {
    group('getUser', () {
      test('returns user when found', () async {
        final mockQueryBuilder = MockSupabaseQueryBuilder();
        final mockFilterBuilder = MockPostgrestFilterBuilder();

        when(() => mockClient.from('users')).thenReturn(mockQueryBuilder);
        when(() => mockQueryBuilder.select()).thenReturn(mockFilterBuilder);
        when(() => mockFilterBuilder.eq('id', '123')).thenReturn(mockFilterBuilder);
        when(() => mockFilterBuilder.maybeSingle()).thenAnswer(
          (_) async => {'id': '123', 'email': 'test@example.com'},
        );

        final user = await repository.getUser('123');

        expect(user, isNotNull);
        expect(user!.id, '123');
      });

      test('returns null when not found', () async {
        // Setup mocks to return null...

        final user = await repository.getUser('nonexistent');

        expect(user, isNull);
      });

      test('throws on network error', () async {
        when(() => mockClient.from('users')).thenThrow(
          PostgrestException(message: 'Network error'),
        );

        expect(
          () => repository.getUser('123'),
          throwsA(isA<NetworkException>()),
        );
      });
    });
  });
}
```

## Widget Tests

### Basic Widget Test

```dart
// test/widget/components/user_avatar_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/shared/widgets/user_avatar.dart';

void main() {
  group('UserAvatar', () {
    testWidgets('displays initials when no image', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: UserAvatar(name: 'John Doe'),
          ),
        ),
      );

      expect(find.text('JD'), findsOneWidget);
    });

    testWidgets('displays image when provided', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: UserAvatar(
              name: 'John Doe',
              imageUrl: 'https://example.com/avatar.jpg',
            ),
          ),
        ),
      );

      expect(find.byType(CircleAvatar), findsOneWidget);
    });

    testWidgets('respects size parameter', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: UserAvatar(name: 'John', size: 100),
          ),
        ),
      );

      final avatar = tester.widget<CircleAvatar>(find.byType(CircleAvatar));
      expect(avatar.radius, 50); // radius = size / 2
    });
  });
}
```

### Screen Tests with Riverpod

```dart
// test/widget/screens/login_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockAuthNotifier extends Mock implements AuthNotifier {}

void main() {
  late MockAuthNotifier mockAuthNotifier;

  setUp(() {
    mockAuthNotifier = MockAuthNotifier();
  });

  Widget buildTestWidget() {
    return ProviderScope(
      overrides: [
        authProvider.overrideWith(() => mockAuthNotifier),
      ],
      child: const MaterialApp(
        home: LoginScreen(),
      ),
    );
  }

  group('LoginScreen', () {
    testWidgets('displays email and password fields', (tester) async {
      when(() => mockAuthNotifier.build()).thenReturn(const AuthState.initial());

      await tester.pumpWidget(buildTestWidget());

      expect(find.byKey(const Key('email_field')), findsOneWidget);
      expect(find.byKey(const Key('password_field')), findsOneWidget);
    });

    testWidgets('shows validation error for invalid email', (tester) async {
      when(() => mockAuthNotifier.build()).thenReturn(const AuthState.initial());

      await tester.pumpWidget(buildTestWidget());

      await tester.enterText(find.byKey(const Key('email_field')), 'invalid');
      await tester.tap(find.byKey(const Key('submit_button')));
      await tester.pumpAndSettle();

      expect(find.text('Please enter a valid email'), findsOneWidget);
    });

    testWidgets('calls signIn on valid submission', (tester) async {
      when(() => mockAuthNotifier.build()).thenReturn(const AuthState.initial());
      when(() => mockAuthNotifier.signIn(any(), any())).thenAnswer((_) async {});

      await tester.pumpWidget(buildTestWidget());

      await tester.enterText(
        find.byKey(const Key('email_field')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(const Key('password_field')),
        'password123',
      );
      await tester.tap(find.byKey(const Key('submit_button')));
      await tester.pumpAndSettle();

      verify(() => mockAuthNotifier.signIn('test@example.com', 'password123')).called(1);
    });

    testWidgets('shows loading indicator during authentication', (tester) async {
      when(() => mockAuthNotifier.build()).thenReturn(const AuthState.loading());

      await tester.pumpWidget(buildTestWidget());

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows error message on auth failure', (tester) async {
      when(() => mockAuthNotifier.build()).thenReturn(
        const AuthState.error('Invalid credentials'),
      );

      await tester.pumpWidget(buildTestWidget());

      expect(find.text('Invalid credentials'), findsOneWidget);
    });
  });
}
```

## Golden Tests

```dart
// test/golden/user_profile_golden_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';

void main() {
  group('UserProfile Golden Tests', () {
    testGoldens('renders correctly on different devices', (tester) async {
      final builder = DeviceBuilder()
        ..overrideDevicesForAllScenarios(devices: [
          Device.phone,
          Device.iphone11,
          Device.tabletPortrait,
        ])
        ..addScenario(
          name: 'default',
          widget: const UserProfileScreen(userId: '123'),
        )
        ..addScenario(
          name: 'loading',
          widget: const UserProfileScreen(userId: '123', isLoading: true),
        );

      await tester.pumpDeviceBuilder(builder);

      await screenMatchesGolden(tester, 'user_profile_multi_device');
    });

    testGoldens('handles dark mode', (tester) async {
      await tester.pumpWidgetBuilder(
        const UserProfileScreen(userId: '123'),
        wrapper: materialAppWrapper(
          theme: ThemeData.dark(),
        ),
      );

      await screenMatchesGolden(tester, 'user_profile_dark');
    });
  });
}

// Update golden files:
// flutter test --update-goldens
```

## Integration Tests

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('End-to-end Tests', () {
    testWidgets('complete login flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Verify on login screen
      expect(find.text('Sign In'), findsOneWidget);

      // Enter credentials
      await tester.enterText(
        find.byKey(const Key('email_field')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(const Key('password_field')),
        'password123',
      );

      // Submit
      await tester.tap(find.byKey(const Key('submit_button')));
      await tester.pumpAndSettle();

      // Verify navigation to home
      expect(find.text('Welcome'), findsOneWidget);
    });

    testWidgets('navigation between screens', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Login first...

      // Navigate to profile
      await tester.tap(find.byIcon(Icons.person));
      await tester.pumpAndSettle();

      expect(find.text('Profile'), findsOneWidget);

      // Navigate back
      await tester.tap(find.byIcon(Icons.arrow_back));
      await tester.pumpAndSettle();

      expect(find.text('Home'), findsOneWidget);
    });
  });
}

// Run integration tests:
// flutter test integration_test
```

## Test Helpers

### Pump App Helper

```dart
// test/helpers/pump_app.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

extension PumpApp on WidgetTester {
  Future<void> pumpApp(
    Widget widget, {
    List<Override> overrides = const [],
    ThemeData? theme,
  }) async {
    await pumpWidget(
      ProviderScope(
        overrides: overrides,
        child: MaterialApp(
          theme: theme ?? ThemeData.light(),
          home: widget,
        ),
      ),
    );
  }

  Future<void> pumpAppWithRouter(
    GoRouter router, {
    List<Override> overrides = const [],
  }) async {
    await pumpWidget(
      ProviderScope(
        overrides: overrides,
        child: MaterialApp.router(
          routerConfig: router,
        ),
      ),
    );
  }
}
```

### Mock Providers

```dart
// test/helpers/mocks.dart
import 'package:mocktail/mocktail.dart';

class MockUserRepository extends Mock implements UserRepository {}
class MockAuthRepository extends Mock implements AuthRepository {}
class MockSupabaseClient extends Mock implements SupabaseClient {}

// Fake classes for registerFallbackValue
class FakeUser extends Fake implements User {}
class FakeCreateUserInput extends Fake implements CreateUserInput {}

void setupMocks() {
  registerFallbackValue(FakeUser());
  registerFallbackValue(FakeCreateUserInput());
}
```

### Custom Finders

```dart
// test/helpers/finders.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

Finder findByKeyString(String key) => find.byKey(Key(key));

Finder findTextButton(String text) => find.widgetWithText(TextButton, text);

Finder findElevatedButton(String text) => find.widgetWithText(ElevatedButton, text);

Finder findTextField(String label) => find.widgetWithText(TextField, label);

extension WidgetTesterX on WidgetTester {
  Future<void> enterTextByKey(String key, String text) async {
    await enterText(findByKeyString(key), text);
  }

  Future<void> tapByKey(String key) async {
    await tap(findByKeyString(key));
  }
}
```

## Test Fixtures

```dart
// test/fixtures/user_fixtures.dart

class UserFixtures {
  static const testUser = User(
    id: 'test-user-id',
    email: 'test@example.com',
    name: 'Test User',
    isVerified: true,
  );

  static const adminUser = User(
    id: 'admin-user-id',
    email: 'admin@example.com',
    name: 'Admin User',
    isVerified: true,
  );

  static List<User> userList([int count = 10]) {
    return List.generate(
      count,
      (i) => User(
        id: 'user-$i',
        email: 'user$i@example.com',
        name: 'User $i',
      ),
    );
  }

  static Map<String, dynamic> userJson = {
    'id': 'test-user-id',
    'email': 'test@example.com',
    'name': 'Test User',
    'is_verified': true,
  };
}
```

## Running Tests

```bash
# Run all tests
flutter test

# Run with coverage
flutter test --coverage

# Run specific test file
flutter test test/unit/models/user_test.dart

# Run tests matching pattern
flutter test --name "UserRepository"

# Run integration tests
flutter test integration_test

# Update golden files
flutter test --update-goldens

# Run with verbose output
flutter test --reporter expanded
```

## Checklist

### Unit Tests
- [ ] Models: fromJson, toJson, copyWith, equality
- [ ] Repositories: success, error, edge cases
- [ ] Utils: pure functions tested
- [ ] Business logic isolated and tested

### Widget Tests
- [ ] Renders correctly
- [ ] User interactions work
- [ ] State changes reflected
- [ ] Error states handled
- [ ] Loading states shown

### Golden Tests
- [ ] Multiple device sizes
- [ ] Light and dark themes
- [ ] Different states (loading, error, empty)
- [ ] Goldens updated when UI changes

### Integration Tests
- [ ] Critical user flows covered
- [ ] Navigation works correctly
- [ ] Data persists across screens
- [ ] Error recovery works

### Coverage
- [ ] Minimum 80% coverage
- [ ] Critical paths 100% covered
- [ ] Coverage report generated
