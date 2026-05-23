---
name: Core Layer Patterns
description: Base classes, error handling, utilities, configuration, and dependency injection patterns for Flutter Clean Architecture
version: 1.0.0
---

# Core Layer Patterns

The **core layer** provides fundamental building blocks used across all other layers in Clean Architecture. It contains no Flutter-specific code and focuses on pure Dart patterns.

## Directory Structure

```
lib/core/
├── errors/
│   ├── failures.dart         # Base Failure classes
│   └── exceptions.dart       # Base Exception classes
├── utils/
│   ├── extensions.dart       # Dart extensions
│   └── validators.dart       # Input validators
├── config/
│   ├── app_config.dart       # Environment configuration
│   └── theme_config.dart     # Theme configuration
└── di/
    └── injection_container.dart  # Dependency injection setup
```

## Error Handling Patterns

### Failures (Domain Layer)

Failures represent expected error states in the domain layer. They are **returned** from use cases using the `Either<Failure, T>` pattern.

```dart
// lib/core/errors/failures.dart
abstract class Failure {
  final String message;
  const Failure(this.message);

  @override
  String toString() => message;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Failure &&
          runtimeType == other.runtimeType &&
          message == other.message;

  @override
  int get hashCode => message.hashCode;
}

// Network-related failures
class ServerFailure extends Failure {
  const ServerFailure([String message = 'Server error occurred']) : super(message);
}

class NetworkFailure extends Failure {
  const NetworkFailure([String message = 'Network error occurred']) : super(message);
}

class TimeoutFailure extends Failure {
  const TimeoutFailure([String message = 'Request timed out']) : super(message);
}

// Data-related failures
class CacheFailure extends Failure {
  const CacheFailure([String message = 'Cache error occurred']) : super(message);
}

class ParseFailure extends Failure {
  const ParseFailure([String message = 'Failed to parse data']) : super(message);
}

// Validation failures
class ValidationFailure extends Failure {
  const ValidationFailure([String message = 'Validation error occurred']) : super(message);
}

class InvalidInputFailure extends Failure {
  const InvalidInputFailure([String message = 'Invalid input provided']) : super(message);
}

// Authentication failures
class UnauthorizedFailure extends Failure {
  const UnauthorizedFailure([String message = 'Unauthorized access']) : super(message);
}

class ForbiddenFailure extends Failure {
  const ForbiddenFailure([String message = 'Access forbidden']) : super(message);
}

// Not found failures
class NotFoundFailure extends Failure {
  const NotFoundFailure([String message = 'Resource not found']) : super(message);
}
```

**Usage in Use Cases**:
```dart
class LoginUser {
  final UserRepository repository;
  const LoginUser({required this.repository});

  Future<Either<Failure, User>> call(String email, String password) async {
    return await repository.login(email, password);
  }
}
```

### Exceptions (Data Layer)

Exceptions represent unexpected error states in the data layer. They are **thrown** by data sources and **caught** by repositories.

```dart
// lib/core/errors/exceptions.dart
class ServerException implements Exception {
  final String message;
  final int? statusCode;

  const ServerException(this.message, [this.statusCode]);

  @override
  String toString() => 'ServerException: $message (status: $statusCode)';
}

class NetworkException implements Exception {
  final String message;

  const NetworkException(this.message);

  @override
  String toString() => 'NetworkException: $message';
}

class CacheException implements Exception {
  final String message;

  const CacheException(this.message);

  @override
  String toString() => 'CacheException: $message';
}

class ParseException implements Exception {
  final String message;
  final dynamic originalError;

  const ParseException(this.message, [this.originalError]);

  @override
  String toString() => 'ParseException: $message';
}

class UnauthorizedException implements Exception {
  final String message;

  const UnauthorizedException([this.message = 'Unauthorized']);

  @override
  String toString() => 'UnauthorizedException: $message';
}
```

**Usage in Repositories**:
```dart
class UserRepositoryImpl implements UserRepository {
  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    try {
      final userModel = await remoteDataSource.login(email, password);
      return Right(userModel.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(e.message));
    } on UnauthorizedException catch (e) {
      return Left(UnauthorizedFailure(e.message));
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e'));
    }
  }
}
```

## Extension Methods

```dart
// lib/core/utils/extensions.dart
import 'package:flutter/material.dart';

/// String extensions
extension StringExtensions on String {
  /// Capitalize first letter
  String capitalize() {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1)}';
  }

  /// Check if string is valid email
  bool get isValidEmail {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return emailRegex.hasMatch(this);
  }

  /// Check if string is valid phone
  bool get isValidPhone {
    final phoneRegex = RegExp(r'^\+?[\d\s-]{10,}$');
    return phoneRegex.hasMatch(this);
  }

  /// Remove all whitespace
  String removeWhitespace() => replaceAll(RegExp(r'\s+'), '');
}

/// DateTime extensions
extension DateTimeExtensions on DateTime {
  /// Check if date is today
  bool get isToday {
    final now = DateTime.now();
    return year == now.year && month == now.month && day == now.day;
  }

  /// Check if date is yesterday
  bool get isYesterday {
    final yesterday = DateTime.now().subtract(const Duration(days: 1));
    return year == yesterday.year &&
        month == yesterday.month &&
        day == yesterday.day;
  }

  /// Format as relative time (2 hours ago, 3 days ago)
  String get relativeTime {
    final now = DateTime.now();
    final difference = now.difference(this);

    if (difference.inDays > 365) {
      return '${(difference.inDays / 365).floor()} year${difference.inDays > 730 ? 's' : ''} ago';
    } else if (difference.inDays > 30) {
      return '${(difference.inDays / 30).floor()} month${difference.inDays > 60 ? 's' : ''} ago';
    } else if (difference.inDays > 0) {
      return '${difference.inDays} day${difference.inDays > 1 ? 's' : ''} ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours} hour${difference.inHours > 1 ? 's' : ''} ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes} minute${difference.inMinutes > 1 ? 's' : ''} ago';
    } else {
      return 'Just now';
    }
  }
}

/// List extensions
extension ListExtensions<T> on List<T> {
  /// Get element at index or null
  T? elementAtOrNull(int index) {
    if (index < 0 || index >= length) return null;
    return this[index];
  }

  /// Remove duplicates
  List<T> unique() => toSet().toList();
}

/// BuildContext extensions
extension ContextExtensions on BuildContext {
  /// Get screen width
  double get screenWidth => MediaQuery.of(this).size.width;

  /// Get screen height
  double get screenHeight => MediaQuery.of(this).size.height;

  /// Get theme
  ThemeData get theme => Theme.of(this);

  /// Get text theme
  TextTheme get textTheme => Theme.of(this).textTheme;

  /// Show snackbar
  void showSnackBar(String message, {bool isError = false}) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError ? Colors.red : null,
      ),
    );
  }
}
```

## Validators

```dart
// lib/core/utils/validators.dart
class Validators {
  /// Email validator
  static String? email(String? value) {
    if (value == null || value.isEmpty) {
      return 'Email is required';
    }
    if (!value.isValidEmail) {
      return 'Please enter a valid email';
    }
    return null;
  }

  /// Password validator
  static String? password(String? value, {int minLength = 8}) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    }
    if (value.length < minLength) {
      return 'Password must be at least $minLength characters';
    }
    return null;
  }

  /// Phone validator
  static String? phone(String? value) {
    if (value == null || value.isEmpty) {
      return 'Phone number is required';
    }
    if (!value.isValidPhone) {
      return 'Please enter a valid phone number';
    }
    return null;
  }

  /// Required field validator
  static String? required(String? value, {String? fieldName}) {
    if (value == null || value.trim().isEmpty) {
      return '${fieldName ?? 'This field'} is required';
    }
    return null;
  }

  /// Min length validator
  static String? minLength(String? value, int min, {String? fieldName}) {
    if (value == null || value.length < min) {
      return '${fieldName ?? 'This field'} must be at least $min characters';
    }
    return null;
  }

  /// Max length validator
  static String? maxLength(String? value, int max, {String? fieldName}) {
    if (value != null && value.length > max) {
      return '${fieldName ?? 'This field'} must not exceed $max characters';
    }
    return null;
  }

  /// Compose multiple validators
  static String? Function(String?) compose(List<String? Function(String?)> validators) {
    return (value) {
      for (final validator in validators) {
        final error = validator(value);
        if (error != null) return error;
      }
      return null;
    };
  }
}
```

**Usage in Forms**:
```dart
TextFormField(
  validator: Validators.compose([
    Validators.required,
    Validators.email,
  ]),
  decoration: const InputDecoration(labelText: 'Email'),
)
```

## Application Configuration

```dart
// lib/core/config/app_config.dart
class AppConfig {
  final String appName;
  final String apiBaseUrl;
  final String apiKey;
  final int connectTimeout;
  final int receiveTimeout;
  final bool enableLogging;

  const AppConfig({
    required this.appName,
    required this.apiBaseUrl,
    required this.apiKey,
    this.connectTimeout = 30000,
    this.receiveTimeout = 30000,
    this.enableLogging = false,
  });

  /// Development configuration
  factory AppConfig.development() {
    return const AppConfig(
      appName: 'MyApp (Dev)',
      apiBaseUrl: 'https://dev-api.example.com',
      apiKey: 'dev_api_key',
      enableLogging: true,
    );
  }

  /// Staging configuration
  factory AppConfig.staging() {
    return const AppConfig(
      appName: 'MyApp (Staging)',
      apiBaseUrl: 'https://staging-api.example.com',
      apiKey: 'staging_api_key',
      enableLogging: true,
    );
  }

  /// Production configuration
  factory AppConfig.production() {
    return const AppConfig(
      appName: 'MyApp',
      apiBaseUrl: 'https://api.example.com',
      apiKey: 'prod_api_key',
      enableLogging: false,
    );
  }
}
```

## Theme Configuration

```dart
// lib/core/config/theme_config.dart
import 'package:flutter/material.dart';

class ThemeConfig {
  /// Light theme
  static ThemeData lightTheme() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue,
        brightness: Brightness.light,
      ),
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        filled: true,
      ),
    );
  }

  /// Dark theme
  static ThemeData darkTheme() {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue,
        brightness: Brightness.dark,
      ),
      appBarTheme: const AppBarTheme(
        elevation: 0,
        centerTitle: true,
      ),
      cardTheme: CardTheme(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        filled: true,
      ),
    );
  }
}
```

## Dependency Injection

```dart
// lib/core/di/injection_container.dart
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';
import 'package:http/http.dart' as http;

class DependencyInjection {
  /// Initialize all dependencies
  static Future<void> init() async {
    // Core dependencies
    _initCore();

    // Data sources
    _initDataSources();

    // Repositories
    _initRepositories();

    // Use cases
    _initUseCases();
  }

  static void _initCore() {
    // HTTP client
    Get.put<http.Client>(http.Client(), permanent: true);

    // GetStorage
    Get.put<GetStorage>(GetStorage(), permanent: true);

    // App configuration
    Get.put<AppConfig>(AppConfig.production(), permanent: true);
  }

  static void _initDataSources() {
    // Register data sources
    // Example:
    // Get.lazyPut<UserRemoteDataSource>(
    //   () => UserRemoteDataSourceImpl(http: Get.find()),
    // );
  }

  static void _initRepositories() {
    // Register repositories
    // Example:
    // Get.lazyPut<UserRepository>(
    //   () => UserRepositoryImpl(
    //     remoteDataSource: Get.find(),
    //     localDataSource: Get.find(),
    //   ),
    // );
  }

  static void _initUseCases() {
    // Register use cases
    // Example:
    // Get.lazyPut(() => LoginUser(repository: Get.find()));
  }
}
```

**Usage in main.dart**:
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await GetStorage.init();
  await DependencyInjection.init();
  runApp(const MyApp());
}
```

## Best Practices

1. **Failures vs Exceptions**:
   - Use `Failure` in domain layer (returned via `Either`)
   - Use `Exception` in data layer (thrown and caught)
   - Never throw exceptions from use cases

2. **Extension Methods**:
   - Keep extensions focused and single-purpose
   - Avoid overly generic extension names
   - Document complex extensions

3. **Configuration**:
   - Use factory constructors for different environments
   - Never hardcode sensitive data (API keys, secrets)
   - Use environment variables for sensitive config

4. **Dependency Injection**:
   - Register dependencies in correct order (data sources → repositories → use cases → controllers)
   - Use `lazyPut` for most dependencies
   - Use `put` with `permanent: true` for singletons needed throughout app lifecycle
