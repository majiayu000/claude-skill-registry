---
name: flutter
description: |
  Flutter framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Flutter projects, or when the user mentions Flutter.
  Provides widget patterns, state management (Riverpod), navigation, and cross-platform guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: dart
  extensions: ".dart"
---

# Flutter Guide

> Applies to: Flutter 3.x, Dart 3.x, Mobile (iOS/Android), Web, Desktop

## Core Principles

1. **Widget Composition**: Build complex UIs by composing small, focused widgets
2. **Declarative UI**: Describe what the UI should look like; Flutter handles rendering
3. **Immutable Widgets**: Widgets are configuration objects; state lives in State classes or providers
4. **Single Codebase**: One Dart codebase targets iOS, Android, Web, macOS, Windows, Linux
5. **Riverpod for State**: Use Riverpod as the primary state management solution
6. **Material 3 First**: Default to Material 3 design system with `useMaterial3: true`

## Guardrails

### Widget Rules

- Keep widget `build` methods under 50 lines (extract sub-widgets)
- Prefer `const` constructors for all stateless widgets
- Always use `super.key` in widget constructors
- Use `ConsumerWidget` / `ConsumerStatefulWidget` when accessing providers
- Dispose controllers, subscriptions, and animation controllers in `dispose()`
- Never perform async work directly in `build()` -- use providers or `FutureBuilder`
- Prefer composition over deep widget nesting (max 5-6 levels in one build method)

### State Management (Riverpod)

- Wrap app root in `ProviderScope`
- Use `Provider` for synchronous values and dependency injection
- Use `StateProvider` for simple mutable state (toggles, filters, counters)
- Use `AsyncNotifierProvider` for async business logic with CRUD operations
- Use `StreamProvider` for real-time data (auth state, WebSocket, Firestore)
- Use `ref.watch()` in build methods; use `ref.read()` in callbacks and event handlers
- Use `ref.listen()` for side effects (showing snackbars, navigation)
- Never call `ref.watch()` outside of build methods or provider bodies

### Navigation (go_router)

- Define all routes in a single `GoRouter` configuration
- Use named routes with `context.goNamed()` / `context.pushNamed()`
- Implement redirect guards for authentication
- Use `ShellRoute` for persistent navigation scaffolds (bottom nav, drawer)
- Use `pathParameters` for required values, `queryParameters` for optional filters
- Define an `errorBuilder` for unknown routes

### File Naming

- Widgets/screens: `snake_case.dart` (e.g., `user_profile_screen.dart`)
- Providers: `snake_case_provider.dart` (e.g., `auth_provider.dart`)
- Models: `snake_case_model.dart` (e.g., `user_model.dart`)
- Repositories: `snake_case_repository.dart`
- Tests: `*_test.dart` (co-located or in `test/` mirroring `lib/`)

## Project Structure

```
myapp/
├── lib/
│   ├── main.dart                 # Entry point, ProviderScope
│   ├── app.dart                  # MaterialApp.router configuration
│   ├── features/                 # Feature-first organization
│   │   └── auth/
│   │       ├── data/             # Models, repos impl, datasources
│   │       ├── domain/           # Entities, abstract repos, use cases
│   │       └── presentation/     # Screens, widgets, providers
│   ├── core/
│   │   ├── constants/            # App-wide constants
│   │   ├── errors/               # Failure/exception classes
│   │   ├── network/              # API client, interceptors
│   │   ├── router/               # GoRouter configuration
│   │   ├── theme/                # Material 3 theme
│   │   ├── utils/                # Validators, formatters
│   │   └── widgets/              # Shared reusable widgets
│   └── l10n/                     # Localization ARB files
├── test/
│   ├── unit/                     # Provider and logic tests
│   ├── widget/                   # Widget tests
│   └── integration/              # End-to-end tests
├── integration_test/             # Integration test driver
├── pubspec.yaml
└── analysis_options.yaml
```

- `features/` follows clean architecture: data, domain, presentation layers
- `core/` for cross-cutting concerns shared across features
- `domain/` contains pure Dart (no Flutter imports)
- `data/` handles serialization, networking, and storage

## Application Setup

### Entry Point

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Initialize services (Firebase, Hive, etc.) here
  runApp(const ProviderScope(child: MyApp()));
}
```

### App Widget

```dart
// lib/app.dart
class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    return MaterialApp.router(
      title: 'My App',
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      themeMode: ThemeMode.system,
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
```

## Widget Composition

### Screen Widget (ConsumerWidget)

```dart
class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(filteredUsersProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Users')),
      body: usersAsync.when(
        data: (users) => UserListView(users: users),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => ErrorRetryWidget(
          message: error.toString(),
          onRetry: () => ref.invalidate(usersProvider),
        ),
      ),
    );
  }
}
```

### Stateful Widget Pattern

Use `ConsumerStatefulWidget` when you need `TextEditingController`, `AnimationController`,
or other objects that require `dispose()`. Key patterns:

- Create controllers in the state class, dispose them in `dispose()`
- Use `ref.watch()` in `build()` for reactive state
- Use `ref.read()` in callbacks like `_submit()`
- Use `ref.listen()` for side effects (snackbars, navigation on error/success)

See [references/patterns.md](references/patterns.md) for the full LoginForm example.

## State Management (Riverpod)

### AsyncNotifier for CRUD

```dart
final usersProvider = AsyncNotifierProvider<UsersNotifier, List<User>>(
  UsersNotifier.new,
);

class UsersNotifier extends AsyncNotifier<List<User>> {
  @override
  Future<List<User>> build() async {
    final repo = ref.read(userRepositoryProvider);
    return repo.getUsers();
  }

  Future<void> addUser(User user) async {
    final repo = ref.read(userRepositoryProvider);
    await repo.createUser(user);
    state = AsyncData([...state.value ?? [], user]);
  }

  Future<void> deleteUser(String id) async {
    final repo = ref.read(userRepositoryProvider);
    await repo.deleteUser(id);
    state = AsyncData(
      state.value?.where((u) => u.id != id).toList() ?? [],
    );
  }
}
```

### Derived / Filtered Providers

```dart
final searchQueryProvider = StateProvider<String>((ref) => '');

final filteredUsersProvider = Provider<AsyncValue<List<User>>>((ref) {
  final users = ref.watch(usersProvider);
  final query = ref.watch(searchQueryProvider).toLowerCase();
  return users.whenData((list) {
    if (query.isEmpty) return list;
    return list.where((u) => u.name.toLowerCase().contains(query)).toList();
  });
});
```

### Stream Provider (Auth State)

```dart
final authStateProvider = StreamProvider<User?>((ref) {
  final repo = ref.watch(authRepositoryProvider);
  return repo.authStateChanges;
});

final currentUserProvider = Provider<User?>((ref) {
  return ref.watch(authStateProvider).valueOrNull;
});
```

## Navigation (go_router)

```dart
final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authStateProvider);

  return GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      final isLoggedIn = authState.valueOrNull != null;
      final isOnLogin = state.matchedLocation == '/login';
      if (!isLoggedIn && !isOnLogin) return '/login';
      if (isLoggedIn && isOnLogin) return '/';
      return null;
    },
    routes: [
      GoRoute(
        path: '/login', name: 'login',
        builder: (_, __) => const LoginScreen(),
      ),
      ShellRoute(
        builder: (_, __, child) => ScaffoldWithNavBar(child: child),
        routes: [
          GoRoute(path: '/', name: 'home', builder: (_, __) => const HomeScreen()),
          GoRoute(path: '/profile', name: 'profile', builder: (_, __) => const ProfileScreen()),
          GoRoute(
            path: '/users/:id', name: 'user-detail',
            builder: (_, state) => UserDetailScreen(userId: state.pathParameters['id']!),
          ),
        ],
      ),
    ],
    errorBuilder: (_, state) => ErrorScreen(error: state.error),
  );
});
```

## Theming (Material 3)

```dart
class AppTheme {
  AppTheme._();

  static ThemeData get light => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF6750A4),
      brightness: Brightness.light,
    ),
    appBarTheme: const AppBarTheme(centerTitle: true, elevation: 0),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      filled: true,
    ),
  );

  static ThemeData get dark => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF6750A4),
      brightness: Brightness.dark,
    ),
  );
}
```

## Data Layer

### Freezed Models

```dart
@freezed
class UserModel with _$UserModel {
  const UserModel._();
  const factory UserModel({
    required String id,
    required String email,
    required String name,
    @JsonKey(name: 'avatar_url') String? avatarUrl,
    @JsonKey(name: 'created_at') required DateTime createdAt,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);

  User toEntity() => User(
    id: id, email: email, name: name,
    avatarUrl: avatarUrl, createdAt: createdAt,
  );
}
```

### Repository Pattern

Use abstract interfaces in `domain/` and implementations in `data/`. Repositories return
`Either<Failure, T>` for error handling. Inject via Riverpod `Provider`:

```dart
// domain layer: abstract contract
abstract class AuthRepository {
  Stream<User?> get authStateChanges;
  Future<Either<Failure, User>> signInWithEmailAndPassword(String email, String password);
  Future<Either<Failure, void>> signOut();
}

// provider: inject implementation
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepositoryImpl(
    remoteDataSource: ref.watch(authRemoteDataSourceProvider),
    localDataSource: ref.watch(authLocalDataSourceProvider),
  );
});
```

See [references/patterns.md](references/patterns.md) for full repository implementation and API client patterns.

### API Client (Dio)

```dart
final dioProvider = Provider<Dio>((ref) {
  return Dio(BaseOptions(
    baseUrl: AppConstants.apiBaseUrl,
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
    headers: {'Content-Type': 'application/json'},
  ))..interceptors.addAll([AuthInterceptor(ref), LogInterceptor()]);
});
```

## Platform Channels

When native platform functionality is needed beyond existing packages:

```dart
// MethodChannel for one-off calls
static const _channel = MethodChannel('com.example.app/battery');
Future<int> getBatteryLevel() async {
  final level = await _channel.invokeMethod<int>('getBatteryLevel');
  return level ?? -1;
}

// EventChannel for continuous streams
static const _eventChannel = EventChannel('com.example.app/sensors');
Stream<SensorData> get sensorStream =>
    _eventChannel.receiveBroadcastStream().map((e) => SensorData.fromMap(e));
```

## Testing Overview

### Widget Test

```dart
Widget createWidget() {
  return ProviderScope(
    overrides: [authRepositoryProvider.overrideWithValue(mockRepo)],
    child: const MaterialApp(home: Scaffold(body: LoginForm())),
  );
}

testWidgets('shows validation errors for empty fields', (tester) async {
  await tester.pumpWidget(createWidget());
  await tester.tap(find.text('Sign In'));
  await tester.pump();
  expect(find.text('Email is required'), findsOneWidget);
});
```

### Provider Test

```dart
final container = ProviderContainer(
  overrides: [authRepositoryProvider.overrideWithValue(mockRepo)],
);
addTearDown(container.dispose);

test('login success clears error state', () async {
  when(() => mockRepo.signInWithEmailAndPassword(any(), any()))
      .thenAnswer((_) async => Right(testUser));
  await container.read(loginProvider.notifier).login('a@b.com', 'pass');
  expect(container.read(loginProvider).hasError, false);
});
```

## Commands

```bash
# Create project
flutter create myapp

# Run
flutter run                           # Default device
flutter run -d chrome                 # Web
flutter run -d macos                  # macOS desktop

# Build
flutter build apk                    # Android APK
flutter build ios                    # iOS archive
flutter build web                    # Web build

# Code generation (Freezed, json_serializable, Riverpod codegen)
dart run build_runner build --delete-conflicting-outputs
dart run build_runner watch           # Continuous generation

# Testing
flutter test                          # All unit + widget tests
flutter test --coverage               # With coverage report
flutter test integration_test/        # Integration tests

# Quality
flutter analyze                       # Static analysis
dart format .                         # Format all files
dart fix --apply                      # Auto-apply lint fixes
```

## Recommended Dependencies

| Package | Purpose |
|---------|---------|
| `flutter_riverpod` | State management |
| `go_router` | Declarative routing |
| `dio` | HTTP client with interceptors |
| `freezed_annotation` + `freezed` | Immutable data classes (codegen) |
| `json_annotation` + `json_serializable` | JSON serialization (codegen) |
| `dartz` | Either type for error handling |
| `shared_preferences` | Key-value local storage |
| `flutter_secure_storage` | Encrypted credential storage |
| `mocktail` | Mocking for tests (no codegen) |
| `flutter_lints` | Recommended lint rules |

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Widget patterns, animations, networking, local storage, testing, platform-specific code, performance

## External References

- [Flutter Documentation](https://docs.flutter.dev/)
- [Riverpod Documentation](https://riverpod.dev/)
- [go_router Documentation](https://pub.dev/packages/go_router)
- [Freezed Package](https://pub.dev/packages/freezed)
- [Flutter Testing](https://docs.flutter.dev/testing)
- [Material 3 Design](https://m3.material.io/)
