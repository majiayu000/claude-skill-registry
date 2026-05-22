---
name: flutter
description: Flutter development with Riverpod state management, Freezed, go_router, and mocktail testing
---

# Flutter Skill

*Load with: base.md*

---

## Project Structure

```
project/
├── lib/
│   ├── core/                           # Core utilities
│   │   ├── constants/                  # App constants
│   │   ├── extensions/                 # Dart extensions
│   │   ├── router/                     # go_router configuration
│   │   │   └── app_router.dart
│   │   └── theme/                      # App theme
│   │       └── app_theme.dart
│   ├── data/                           # Data layer
│   │   ├── models/                     # Freezed data models
│   │   ├── repositories/               # Repository implementations
│   │   └── services/                   # API services
│   ├── domain/                         # Domain layer
│   │   ├── entities/                   # Business entities
│   │   └── repositories/               # Repository interfaces
│   ├── presentation/                   # UI layer
│   │   ├── common/                     # Shared widgets
│   │   ├── features/                   # Feature modules
│   │   │   └── feature_name/
│   │   │       ├── providers/          # Riverpod providers
│   │   │       ├── widgets/            # Feature-specific widgets
│   │   │       └── feature_screen.dart
│   │   └── providers/                  # Global providers
│   ├── main.dart
│   └── app.dart
├── test/
│   ├── unit/                           # Unit tests
│   ├── widget/                         # Widget tests
│   └── integration/                    # Integration tests
├── pubspec.yaml
├── analysis_options.yaml
└── CLAUDE.md
```

---

## Riverpod State Management

### Provider Types
```dart
// Simple value provider
final appNameProvider = Provider<String>((ref) => 'My App');

// StateProvider for simple mutable state
final counterProvider = StateProvider<int>((ref) => 0);

// NotifierProvider for complex state logic
final userProvider = NotifierProvider<UserNotifier, User?>(() => UserNotifier());

// AsyncNotifierProvider for async operations
final usersProvider = AsyncNotifierProvider<UsersNotifier, List<User>>(
  () => UsersNotifier(),
);

// FutureProvider for simple async data
final configProvider = FutureProvider<Config>((ref) async {
  return await ref.watch(configServiceProvider).loadConfig();
});

// StreamProvider for real-time data
final messagesProvider = StreamProvider<List<Message>>((ref) {
  return ref.watch(messageServiceProvider).watchMessages();
});

// Family providers for parameterized data
final userByIdProvider = FutureProvider.family<User, String>((ref, userId) async {
  return await ref.watch(userRepositoryProvider).getUser(userId);
});
```

### Notifier Pattern
```dart
@riverpod
class Users extends _$Users {
  @override
  Future<List<User>> build() async {
    return await _fetchUsers();
  }

  Future<List<User>> _fetchUsers() async {
    final repository = ref.read(userRepositoryProvider);
    return await repository.getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(() => _fetchUsers());
  }

  Future<void> addUser(User user) async {
    final repository = ref.read(userRepositoryProvider);
    await repository.addUser(user);
    ref.invalidateSelf();
  }
}
```

### AsyncValue Handling
```dart
class UsersScreen extends ConsumerWidget {
  const UsersScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersProvider);

    return usersAsync.when(
      data: (users) => UsersList(users: users),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => ErrorDisplay(
        error: error,
        onRetry: () => ref.invalidate(usersProvider),
      ),
    );
  }
}

// Pattern matching alternative
Widget build(BuildContext context, WidgetRef ref) {
  final usersAsync = ref.watch(usersProvider);

  return switch (usersAsync) {
    AsyncData(:final value) => UsersList(users: value),
    AsyncLoading() => const LoadingIndicator(),
    AsyncError(:final error) => ErrorDisplay(error: error),
  };
}
```

### ref Methods
```dart
// watch - rebuilds when provider changes
final users = ref.watch(usersProvider);

// read - one-time read, no rebuild
void onButtonPressed() {
  ref.read(counterProvider.notifier).state++;
}

// listen - react to changes without rebuild
ref.listen(authProvider, (previous, next) {
  if (next == null) {
    context.go('/login');
  }
});

// invalidate - force refresh
ref.invalidate(usersProvider);

// keepAlive - prevent auto-dispose
final link = ref.keepAlive();
// Later: link.close() to allow disposal
```

---

## Freezed Data Models

### Model Definition
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    @Default(false) bool isActive,
    DateTime? createdAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Union types for states
@freezed
sealed class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.unauthenticated() = _Unauthenticated;
  const factory AuthState.error(String message) = _Error;
}
```

### Using Freezed Unions
```dart
Widget build(BuildContext context, WidgetRef ref) {
  final authState = ref.watch(authProvider);

  return authState.when(
    initial: () => const SplashScreen(),
    loading: () => const LoadingScreen(),
    authenticated: (user) => HomeScreen(user: user),
    unauthenticated: () => const LoginScreen(),
    error: (message) => ErrorScreen(message: message),
  );
}
```

---

## go_router Navigation

### Router Configuration
```dart
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    initialLocation: '/',
    refreshListenable: authState,
    redirect: (context, state) {
      final isLoggedIn = authState.valueOrNull != null;
      final isLoggingIn = state.matchedLocation == '/login';

      if (!isLoggedIn && !isLoggingIn) return '/login';
      if (isLoggedIn && isLoggingIn) return '/';
      return null;
    },
    routes: [
      GoRoute(
        path: '/',
        builder: (context, state) => const HomeScreen(),
        routes: [
          GoRoute(
            path: 'user/:id',
            builder: (context, state) => UserScreen(
              userId: state.pathParameters['id']!,
            ),
          ),
        ],
      ),
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
    ],
    errorBuilder: (context, state) => ErrorScreen(error: state.error),
  );
});
```

### Navigation
```dart
// Navigate to route
context.go('/user/123');

// Push onto stack
context.push('/user/123');

// Pop current route
context.pop();

// Replace current route
context.pushReplacement('/home');

// Named routes
context.goNamed('user', pathParameters: {'id': '123'});
```

---

## Widget Patterns

### ConsumerWidget vs ConsumerStatefulWidget
```dart
// Stateless with Riverpod
class UserCard extends ConsumerWidget {
  const UserCard({super.key, required this.userId});

  final String userId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(userByIdProvider(userId));
    return user.when(
      data: (user) => Card(child: Text(user.name)),
      loading: () => const CardSkeleton(),
      error: (e, _) => ErrorCard(error: e),
    );
  }
}

// Stateful with Riverpod
class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({super.key});

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final results = ref.watch(searchProvider(_controller.text));
    return Column(
      children: [
        TextField(
          controller: _controller,
          onChanged: (_) => setState(() {}),
        ),
        Expanded(child: SearchResults(results: results)),
      ],
    );
  }
}
```

### HookConsumerWidget (with flutter_hooks)
```dart
class AnimatedCounter extends HookConsumerWidget {
  const AnimatedCounter({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = useAnimationController(duration: const Duration(milliseconds: 300));
    final count = ref.watch(counterProvider);

    useEffect(() {
      controller.forward(from: 0);
      return null;
    }, [count]);

    return ScaleTransition(
      scale: controller,
      child: Text('$count'),
    );
  }
}
```

---

## Testing with Mocktail

### Unit Tests
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:riverpod/riverpod.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepository;
  late ProviderContainer container;

  setUp(() {
    mockRepository = MockUserRepository();
    container = ProviderContainer(
      overrides: [
        userRepositoryProvider.overrideWithValue(mockRepository),
      ],
    );
  });

  tearDown(() {
    container.dispose();
  });

  test('usersProvider returns list of users', () async {
    final users = [User(id: '1', name: 'John', email: 'john@example.com')];
    when(() => mockRepository.getUsers()).thenAnswer((_) async => users);

    final result = await container.read(usersProvider.future);

    expect(result, equals(users));
    verify(() => mockRepository.getUsers()).called(1);
  });
}
```

### Widget Tests
```dart
void main() {
  testWidgets('UserCard displays user name', (tester) async {
    final user = User(id: '1', name: 'John', email: 'john@example.com');

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          userByIdProvider('1').overrideWith((_) => AsyncData(user)),
        ],
        child: const MaterialApp(home: UserCard(userId: '1')),
      ),
    );

    expect(find.text('John'), findsOneWidget);
  });

  testWidgets('UserCard shows loading indicator', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          userByIdProvider('1').overrideWith((_) => const AsyncLoading()),
        ],
        child: const MaterialApp(home: UserCard(userId: '1')),
      ),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });
}
```

---

## pubspec.yaml

```yaml
name: my_app
description: A Flutter application
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.2.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # State management
  flutter_riverpod: ^2.4.9
  riverpod_annotation: ^2.3.3

  # Data models
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1

  # Navigation
  go_router: ^13.0.0

  # Networking
  dio: ^5.4.0

  # Storage
  shared_preferences: ^2.2.2

  # Utils
  intl: ^0.19.0

dev_dependencies:
  flutter_test:
    sdk: flutter

  # Code generation
  build_runner: ^2.4.8
  freezed: ^2.4.6
  json_serializable: ^6.7.1
  riverpod_generator: ^2.3.9

  # Testing
  mocktail: ^1.0.2

  # Linting
  flutter_lints: ^3.0.1
```

---

## GitHub Actions

```yaml
name: Flutter CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'
          cache: true

      - name: Install dependencies
        run: flutter pub get

      - name: Generate code
        run: dart run build_runner build --delete-conflicting-outputs

      - name: Analyze
        run: flutter analyze --fatal-infos

      - name: Run tests
        run: flutter test --coverage

      - name: Build APK
        run: flutter build apk --release
```

---

## analysis_options.yaml

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  errors:
    invalid_annotation_target: ignore
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true

linter:
  rules:
    - always_declare_return_types
    - avoid_dynamic_calls
    - avoid_print
    - avoid_type_to_string
    - cancel_subscriptions
    - close_sinks
    - prefer_const_constructors
    - prefer_const_declarations
    - prefer_final_locals
    - require_trailing_commas
    - unawaited_futures
    - use_super_parameters
```

---

## Flutter Anti-Patterns

- ❌ **Provider without autoDispose** - Use `.autoDispose` to prevent memory leaks
- ❌ **watch in callbacks** - Use `ref.read()` in onPressed/callbacks, not `ref.watch()`
- ❌ **Business logic in widgets** - Move to Notifiers/providers
- ❌ **Mutable state in providers** - Use Freezed for immutable models
- ❌ **Not using AsyncValue** - Handle loading/error states with `when()`
- ❌ **setState with Riverpod** - Use providers for shared state
- ❌ **Passing ref to functions** - Keep ref usage within widgets/providers
- ❌ **Deeply nested Consumer** - Use ConsumerWidget instead
- ❌ **Not using family for params** - Use `.family` for parameterized providers
- ❌ **Global GoRouter instance** - Use Provider for router with redirect logic
- ❌ **BuildContext across async** - Store values before await, not context
- ❌ **Ignoring dispose** - Clean up controllers in ConsumerStatefulWidget

