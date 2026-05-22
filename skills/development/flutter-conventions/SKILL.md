---
name: "Flutter Conventions & Best Practices"
description: "Dart 3.x and Flutter 3.x conventions, naming patterns, code organization, null safety, and async/await best practices"
version: "1.0.0"
---

# Flutter Conventions & Best Practices

## Dart 3.x Features

### Pattern Matching
```dart
String describeUser(User user) {
  return switch (user) {
    User(role: 'admin', isActive: true) => 'Active administrator',
    User(role: 'user', isActive: true) => 'Active user',
    User(isActive: false) => 'Inactive account',
    _ => 'Unknown status',
  };
}
```

### Records
```dart
(int, String) getUserInfo() => (123, 'John Doe');

final (id, name) = getUserInfo();
```

### Sealed Classes
```dart
sealed class Result<T> {}
class Success<T> extends Result<T> {
  final T data;
  Success(this.data);
}
class Error<T> extends Result<T> {
  final String message;
  Error(this.message);
}
```

## File Naming Conventions

- **Files**: `snake_case.dart`
- **Classes**: `PascalCase`
- **Variables/Functions**: `camelCase`
- **Constants**: `lowerCamelCase` or `SCREAMING_SNAKE_CASE` for compile-time constants

```dart
// user_controller.dart
class UserController extends GetxController {
  static const int maxRetries = 3;
  static const String BASE_URL = 'https://api.example.com';
  
  final userName = 'John'.obs;
  
  void fetchUserData() {
    // ...
  }
}
```

## Directory Organization

**Layer-first** (recommended for Clean Architecture):
```
lib/
├── domain/
├── data/
└── presentation/
```

**Feature-first** (alternative):
```
lib/
└── features/
    ├── auth/
    │   ├── domain/
    │   ├── data/
    │   └── presentation/
    └── profile/
```

## Null Safety

```dart
// Use late for non-nullable fields initialized later
class MyController extends GetxController {
  late final UserRepository repository;
  
  @override
  void onInit() {
    super.onInit();
    repository = Get.find();
  }
}

// Use ? for nullable types
String? userName;

// Use ! only when absolutely certain
final name = userName!; // Use sparingly

// Prefer ?? for defaults
final displayName = userName ?? 'Guest';
```

## Async/Await Best Practices

```dart
// Use async/await for asynchronous operations
Future<User> fetchUser(String id) async {
  try {
    final response = await client.get(Uri.parse('/users/$id'));
    return User.fromJson(jsonDecode(response.body));
  } on SocketException {
    throw NetworkException();
  } catch (e) {
    throw UnknownException(e.toString());
  }
}

// Use Future.wait for parallel operations
Future<void> loadAllData() async {
  final results = await Future.wait([
    fetchUsers(),
    fetchSettings(),
    fetchPreferences(),
  ]);
}

// Use unawaited for fire-and-forget
unawaited(analytics.logEvent('page_view'));
```

## Code Organization Within Files

```dart
class MyClass {
  // 1. Constants
  static const int maxRetries = 3;
  
  // 2. Static fields
  static final instance = MyClass._();
  
  // 3. Instance fields
  final String id;
  final _isLoading = false.obs;
  
  // 4. Constructors
  MyClass(this.id);
  MyClass._();
  
  // 5. Getters/Setters
  bool get isLoading => _isLoading.value;
  
  // 6. Lifecycle methods
  @override
  void onInit() {}
  
  // 7. Public methods
  void publicMethod() {}
  
  // 8. Private methods
  void _privateMethod() {}
}
```

## Widget Best Practices

```dart
// Prefer const constructors
class MyWidget extends StatelessWidget {
  const MyWidget({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return const Text('Hello');
  }
}

// Extract widgets for reusability
class UserCard extends StatelessWidget {
  final User user;
  
  const UserCard({Key? key, required this.user}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: _buildContent(),
    );
  }
  
  Widget _buildContent() {
    return Column(
      children: [
        Text(user.name),
        Text(user.email),
      ],
    );
  }
}
```
