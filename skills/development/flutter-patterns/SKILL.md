---
name: Flutter Development Patterns
description: Project structure, widgets, state management, navigation, theming, platform channels, and best practices for building cross-platform mobile applications with Flutter.
---

# Flutter Development Patterns

> **Current Level:** Intermediate  
> **Domain:** Mobile Development / Flutter

---

## Overview

Flutter development patterns cover project structure, widgets, state management, navigation, and best practices for building cross-platform mobile applications. Effective Flutter development uses proper architecture, state management, and platform-specific optimizations.

---

## Core Concepts

### Table of Contents

1. [Flutter Setup](#flutter-setup)
2. [Project Structure](#projectstructure)
3. [Widget Patterns](#widget-patterns)
4. [State Management](#state-management)
5. [Navigation](#navigation)
6. [Theming](#theming)
7. [Platform Channels](#platform-channels)
8. [Async Patterns](#async-patterns)
9. [Performance Optimization](#performance-optimization)
10. [Testing](#testing)
11. [Common Packages](#common-packages)
12. [Best Practices](#best-practices)

---

## Flutter Setup

### Project Initialization

```bash
# Using Flutter CLI
flutter create my_app --org com.example.myapp --platforms android,ios,web

# Using very_good_cli
very_good_cli create my_app

# Navigate to project
cd my_app

# Install dependencies
flutter pub get

# Run the app
flutter run
```

### Configuration

```yaml
# pubspec.yaml
name: my_app
description: A Flutter application.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: ">=3.0.0"

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.2
  go_router: ^12.0.0
  flutter_riverpod: ^2.3.0
  dio: ^5.3.0
  shared_preferences: ^2.2.0
  flutter_secure_storage: ^8.0.0
  connectivity_plus: ^5.0.0
  cached_network_image: ^3.2.0
  flutter_svg: ^2.0.0
  image_picker: ^1.0.4
  permission_handler: ^11.0.0
  intl: ^0.18.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  build_runner: ^2.4.0
  json_serializable: ^6.7.0

flutter:
  uses-material-design: true
  assets:
    - assets/images/
    - assets/icons/
  fonts:
    - family: Roboto
      fonts:
        - asset: fonts/Roboto-Regular.ttf
        - asset: fonts/Roboto-Bold.ttf
          weight: 700
```

---

## Project Structure

### Recommended Structure

```
lib/
├── main.dart                 # App entry point
├── app.dart                  # Root widget
├── core/                    # Core functionality
│   ├── constants/            # App constants
│   ├── error/                # Error handling
│   ├── network/              # Network utilities
│   ├── router/               # Routing configuration
│   └── theme/                # App theming
├── data/                    # Data layer
│   ├── models/               # Data models
│   ├── repositories/          # Data repositories
│   └── datasources/          # API and local storage
│       ├── api/              # API clients
│       └── local/            # Local storage
├── domain/                  # Domain layer
│   ├── entities/             # Domain entities
│   ├── usecases/             # Business logic
│   └── repositories/         # Repository interfaces
├── presentation/             # Presentation layer
│   ├── pages/                # Screen widgets
│   ├── widgets/              # Reusable widgets
│   │   ├── common/          # Generic widgets
│   │   ├── buttons/         # Button widgets
│   │   ├── inputs/          # Input widgets
│   │   └── cards/           # Card widgets
│   └── providers/            # State providers
└── services/                # Services
    ├── api/                  # API service
    ├── auth/                 # Authentication service
    ├── storage/              # Storage service
    └── notifications/         # Notification service
```

### Example Files

```dart
// lib/core/constants/app_constants.dart
class AppConstants {
  static const String appName = 'MyApp';
  static const String defaultCurrency = 'USD';
  static const int apiTimeout = 30000;
  static const int cacheDuration = 86400; // 24 hours
}

// lib/core/theme/app_theme.dart
import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF007AFF),
      brightness: Brightness.light,
    ),
    scaffoldBackgroundColor: Colors.white,
    appBarTheme: const AppBarTheme(
      centerTitle: true,
      elevation: 0,
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: const Color(0xFF007AFF),
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(
          horizontal: 24,
          vertical: 12,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
    ),
  );

  static ThemeData get darkTheme => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF007AFF),
      brightness: Brightness.dark,
    ),
    scaffoldBackgroundColor: const Color(0xFF121212),
  );
}

// lib/data/models/user.dart
class User {
  final String id;
  final String email;
  final String name;
  final String? avatar;

  User({
    required this.id,
    required this.email,
    required this.name,
    this.avatar,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      name: json['name'],
      avatar: json['avatar'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'avatar': avatar,
    };
  }
}
```

---

## Widget Patterns

### Common Widgets

```dart
// lib/presentation/widgets/common/loading_widget.dart
import 'package:flutter/material.dart';

class LoadingWidget extends StatelessWidget {
  const LoadingWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: CircularProgressIndicator(),
    );
  }
}

// lib/presentation/widgets/common/error_widget.dart
class ErrorWidget extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const ErrorWidget({
    super.key,
    required this.message,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(
            Icons.error_outline,
            size: 48,
            color: Colors.red,
          ),
          const SizedBox(height: 16),
          Text(
            message,
            style: Theme.of(context).textTheme.bodyLarge,
            textAlign: TextAlign.center,
          ),
          if (onRetry != null) ...[
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: onRetry,
              child: const Text('Retry'),
            ),
          ],
        ],
      ),
    );
  }
}

// lib/presentation/widgets/common/empty_widget.dart
class EmptyWidget extends StatelessWidget {
  final String message;
  final IconData? icon;

  const EmptyWidget({
    super.key,
    required this.message,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            icon ?? Icons.inbox_outlined,
            size: 64,
            color: Colors.grey[400],
          ),
          const SizedBox(height: 16),
          Text(
            message,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: Colors.grey[600],
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
```

### Custom Widgets

```dart
// lib/presentation/widgets/buttons/primary_button.dart
import 'package:flutter/material.dart';

class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final bool isDisabled;

  const PrimaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.isDisabled = false,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: (isDisabled || isLoading) ? null : onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: Theme.of(context).colorScheme.primary,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
        child: isLoading
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  color: Colors.white,
                ),
              )
            : Text(
                text,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                ),
              ),
      ),
    );
  }
}

// lib/presentation/widgets/inputs/text_input.dart
class TextInputWidget extends StatelessWidget {
  final String label;
  final String? initialValue;
  final bool obscureText;
  final bool enabled;
  final TextInputType? keyboardType;
  final Function(String)? onChanged;
  final String? Function(String)? validator;
  final Widget? suffixIcon;

  const TextInputWidget({
    super.key,
    required this.label,
    this.initialValue,
    this.obscureText = false,
    this.enabled = true,
    this.keyboardType,
    this.onChanged,
    this.validator,
    this.suffixIcon,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(height: 8),
        TextFormField(
          initialValue: initialValue,
          obscureText: obscureText,
          enabled: enabled,
          keyboardType: keyboardType,
          onChanged: onChanged,
          validator: validator,
          decoration: InputDecoration(
            filled: true,
            fillColor: Colors.grey[100],
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8),
              borderSide: BorderSide.none,
            ),
            suffixIcon: suffixIcon,
          ),
        ),
      ],
    );
  }
}
```

---

## State Management

### Riverpod Setup

```dart
// lib/presentation/providers/auth_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:my_app/data/models/user.dart';

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier() : super(AuthState.initial());

  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true);

    try {
      final user = await _authService.login(email, password);
      state = state.copyWith(
        user: user,
        isAuthenticated: true,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        error: e.toString(),
        isLoading: false,
      );
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    state = AuthState.initial();
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}

class AuthState {
  final User? user;
  final bool isAuthenticated;
  final bool isLoading;
  final String? error;

  AuthState({
    this.user,
    required this.isAuthenticated,
    required this.isLoading,
    this.error,
  });

  factory AuthState.initial() {
    return AuthState(
      isAuthenticated: false,
      isLoading: false,
      error: null,
    );
  }

  AuthState copyWith({
    User? user,
    bool? isAuthenticated,
    bool? isLoading,
    String? error,
  }) {
    return AuthState(
      user: user ?? this.user,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>(
  (ref) => AuthNotifier(),
);
```

### Provider Usage

```dart
// lib/presentation/pages/home_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await ref.read(authProvider.notifier).logout();
            },
          ),
        ],
      ),
      body: authState.isLoading
          ? const LoadingWidget()
          : authState.error != null
              ? ErrorWidget(
                  message: authState.error!,
                  onRetry: () => ref.read(authProvider.notifier).clearError(),
                )
              : Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text('Welcome, ${authState.user?.name ?? 'Guest'}'),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: () {
                          // Navigate to profile
                        },
                        child: const Text('View Profile'),
                      ),
                    ],
                  ),
                ),
    );
  }
}
```

---

## Navigation

### Go Router Setup

```dart
// lib/core/router/app_router.dart
import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';

enum AppRoute {
  home,
  login,
  register,
  profile,
  productDetails,
}

final goRouter = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      name: AppRoute.home,
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/login',
      name: AppRoute.login,
      builder: (context, state) => const LoginPage(),
    ),
    GoRoute(
      path: '/register',
      name: AppRoute.register,
      builder: (context, state) => const RegisterPage(),
    ),
    GoRoute(
      path: '/profile/:userId',
      name: AppRoute.profile,
      builder: (context, state) {
        final userId = state.pathParameters['userId']!;
        return ProfilePage(userId: userId);
      },
    ),
    GoRoute(
      path: '/product/:productId',
      name: AppRoute.productDetails,
      builder: (context, state) {
        final productId = state.pathParameters['productId']!;
        return ProductDetailsPage(productId: productId);
      },
    ),
  ],
  errorBuilder: (context, state) => ErrorPage(error: state.error),
);
```

### Navigation Helpers

```dart
// lib/core/router/navigation_helpers.dart
import 'package:go_router/go_router.dart';

extension GoRouterHelper on GoRouter {
  void navigateToHome() {
    go(AppRoute.home);
  }

  void navigateToLogin() {
    go(AppRoute.login);
  }

  void navigateToProfile(String userId) {
    push(AppRoute.profile, pathParameters: {'userId': userId});
  }

  void navigateToProductDetails(String productId) {
    push(AppRoute.productDetails, pathParameters: {'productId': productId});
  }

  void goBack() {
    pop();
  }
}

// Usage
class ProductCard extends StatelessWidget {
  final String productId;
  final String productName;

  const ProductCard({
    super.key,
    required this.productId,
    required this.productName,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        context.goRouter.navigateProductDetails(productId);
      },
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Text(productName),
        ),
      ),
    );
  }
}
```

---

## Theming

### Theme Provider

```dart
// lib/presentation/providers/theme_provider.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

enum ThemeMode {
  light,
  dark,
  system,
}

class ThemeNotifier extends StateNotifier<ThemeMode> {
  ThemeNotifier() : super(ThemeMode.system);

  void setTheme(ThemeMode mode) {
    state = mode;
  }

  void toggleTheme() {
    switch (state) {
      case ThemeMode.light:
        state = ThemeMode.dark;
        break;
      case ThemeMode.dark:
        state = ThemeMode.light;
        break;
      case ThemeMode.system:
        final isDark = WidgetsBinding.instance.platformDispatcher.platformBrightness ==
            Brightness.dark;
        state = isDark ? ThemeMode.light : ThemeMode.dark;
        break;
    }
  }
}

final themeProvider = StateNotifierProvider<ThemeNotifier, ThemeMode>(
  (ref) => ThemeNotifier(),
);

final themeModeProvider = Provider<ThemeData>((ref) {
  final mode = ref.watch(themeProvider);
  final brightness = MediaQuery.of(ref.context).platformBrightness;

  switch (mode) {
    case ThemeMode.light:
      return AppTheme.lightTheme;
    case ThemeMode.dark:
      return AppTheme.darkTheme;
    case ThemeMode.system:
      return brightness == Brightness.dark
          ? AppTheme.darkTheme
          : AppTheme.lightTheme;
  }
});
```

---

## Platform Channels

### Native Communication

```dart
// lib/services/platform/platform_service.dart
import 'package:flutter/services.dart';

class PlatformService {
  static const MethodChannel _channel =
      MethodChannel('com.example.myapp/platform');

  static Future<String> getDeviceName() async {
    try {
      final result = await _channel.invokeMethod('getDeviceName');
      return result as String;
    } on PlatformException catch (e) {
      throw Exception('Failed to get device name: ${e.message}');
    }
  }

  static Future<void> openSettings() async {
    try {
      await _channel.invokeMethod('openSettings');
    } on PlatformException catch (e) {
      throw Exception('Failed to open settings: ${e.message}');
    }
  }
}

// Android: android/app/src/main/kotlin/com/example/myapp/MainActivity.kt
package com.example.myapp

import android.os.Bundle
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterActivity() {
  private val CHANNEL = "com.example.myapp/platform"

  override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
    super.configureFlutterEngine(flutterEngine)

    MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
        .setMethodCallHandler { call, result ->
          when (call.method) {
            "getDeviceName" -> {
              result.invokeMethod("getDeviceName", null, object : Bundle())
            }
            "openSettings" -> {
              val intent = android.content.Intent(
                android.provider.Settings.ACTION_APPLICATION_DETAILS_SETTINGS
              )
              intent.addCategory(android.content.Intent.CATEGORY_DEFAULT)
              intent.data = context.packageName
              startActivity(intent)
              result.success(null)
            }
            else -> result.notImplemented()
          }
        }
  }
}

// iOS: ios/Runner/AppDelegate.swift
import Flutter
import UIKit

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    let controller = window?.rootViewController as? FlutterViewController

    let channel = FlutterMethodChannel(
      name: "com.example.myapp/platform",
      binaryMessenger: controller!.binaryMessenger
    )

    channel.setMethodCallHandler { [weak self] (call, result) in
      switch call.method {
      case "getDeviceName":
        let name = UIDevice.current.name
        result(name)
      case "openSettings":
        if let url = URL(string: UIApplication.openSettingsURLString) {
          UIApplication.shared.open(url)
          result(Bool(true))
        } else {
          result(FlutterError(code: "UNAVAILABLE", message: "Settings not available", details: nil))
        }
      default:
        result(FlutterMethodNotImplemented)
      }
    }

    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }
}
```

---

## Async Patterns

### Async/Await

```dart
// lib/services/api/api_service.dart
import 'package:dio/dio.dart';
import 'package:my_app/core/error/exceptions.dart';

class ApiService {
  final Dio _dio;

  ApiService(this._dio);

  Future<T> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      final response = await _dio.get(
        path,
        queryParameters: queryParameters,
        options: options,
      );

      return response.data as T;
    } on DioException catch (e) {
      throw ApiException.fromDioException(e);
    }
  }

  Future<T> post<T>(
    String path, {
    dynamic data,
    Options? options,
  }) async {
    try {
      final response = await _dio.post(
        path,
        data: data,
        options: options,
      );

      return response.data as T;
    } on DioException catch (e) {
      throw ApiException.fromDioException(e);
    }
  }
}

// lib/core/error/exceptions.dart
class ApiException implements Exception {
  final String message;
  final int? statusCode;

  ApiException(this.message, {this.statusCode});

  factory ApiException.fromDioException(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return ApiException('Connection timeout');
      case DioExceptionType.badResponse:
        return ApiException(
          e.response?.statusMessage ?? 'Server error',
          statusCode: e.response?.statusCode,
        );
      case DioExceptionType.cancel:
        return ApiException('Request cancelled');
      default:
        return ApiException('Network error');
    }
  }
}
```

---

## Performance Optimization

### List Optimization

```dart
// lib/presentation/widgets/common/optimized_list.dart
import 'package:flutter/material.dart';

class OptimizedList extends StatelessWidget {
  final List<dynamic> items;
  final Widget Function(dynamic item) itemBuilder;
  final String Function(dynamic item) keyExtractor;

  const OptimizedList({
    super.key,
    required this.items,
    required this.itemBuilder,
    required this.keyExtractor,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        final item = items[index];
        return itemBuilder(item);
      },
      cacheExtent: 200,
      addAutomaticKeepAlives: true,
    );
  }
}

// Usage
class ProductListPage extends StatelessWidget {
  const ProductListPage({super.key});

  @override
  Widget build(BuildContext context) {
    final products = Provider.of<ProductProvider>(context).products;

    return OptimizedList(
      items: products,
      keyExtractor: (product) => product.id,
      itemBuilder: (product) => ProductCard(product: product),
    );
  }
}
```

---

## Testing

### Widget Testing

```dart
// test/presentation/widgets/buttons/primary_button_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/presentation/widgets/buttons/primary_button.dart';

void main() {
  group('PrimaryButton', () {
    testWidgets('renders correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PrimaryButton(
              text: 'Click me',
              onPressed: () {},
            ),
          ),
        ),
      );

      expect(find.text('Click me'), findsOneWidget);
    });

    testWidgets('shows loading indicator when isLoading is true', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PrimaryButton(
              text: 'Click me',
              isLoading: true,
              onPressed: () {},
            ),
          ),
        ),
      );

      expect(find.byType(CircularProgressIndicatorIndicator), findsOneWidget);
      expect(find.text('Click me'), findsNothing);
    });

    testWidgets('is disabled when isDisabled is true', (tester) async {
      bool onPressedCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PrimaryButton(
              text: 'Click me',
              isDisabled: true,
              onPressed: () {
                onPressedCalled = true;
              },
            ),
          ),
        ),
      );

      await tester.tap(find.byType(ElevatedButton));
      expect(onPressedCalled, false);
    });
  });
}
```

---

## Common Packages

### Essential Packages

```yaml
# pubspec.yaml
dependencies:
  # Navigation
  go_router: ^12.0.0
  
  # State Management
  flutter_riverpod: ^2.3.0
  
  # Networking
  dio: ^5.3.0
  connectivity_plus: ^5.0.0
  
  # Storage
  shared_preferences: ^2.2.0
  flutter_secure_storage: ^8.0.0
  hive: ^2.2.3
  sqflite: ^2.3.0
  
  # UI Components
  cached_network_image: ^3.2.0
  flutter_svg: ^2.0.0
  image_picker: ^1.0.4
  permission_handler: ^11.0.0
  flutter_local_notifications: ^16.0.0
  url_launcher: ^6.1.11
  share_plus: ^7.2.1
  
  # Utilities
  intl: ^0.18.0
  path_provider: ^2.1.1
  device_info_plus: ^9.1.0
  
  # Firebase
  firebase_core: ^2.15.0
  firebase_auth: ^4.7.3
  cloud_firestore: ^4.8.5
  firebase_messaging: ^14.6.4
  firebase_analytics: ^10.4.5
  
  # Maps & Location
  google_maps_flutter: ^2.5.0
  geolocator: ^10.0.0
  permission_handler: ^11.0.0
  
  # Testing
  flutter_test: ^0.7.0
  mockito: ^5.4.1
  build_runner: ^2.4.0
  json_serializable: ^6.7.0
```

---

## Best Practices

### Performance Best Practices

```dart
// 1. Use const widgets where possible
class GoodExample extends StatelessWidget {
  const GoodExample({super.key});

  @override
  Widget build(BuildContext context) {
    return const Text('Hello'); // Good
  }
}

class BadExample extends StatelessWidget {
  const BadExample({super.key});

  @override
  Widget build(BuildContext context) {
    return Text('Hello'); // Bad: Creates new widget every build
  }
}

// 2. Use ListView.builder for long lists
class GoodListExample extends StatelessWidget {
  final List<String> items;

  const GoodListExample({super.key, required this.items});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) {
        return ListTile(title: Text(items[index]));
      },
    );
  }
}

class BadListExample extends StatelessWidget {
  final List<String> items;

  const BadListExample({super.key, required this.items});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: items.map((item) => ListTile(title: Text(item))).toList(), // Bad: All widgets built at once
    );
  }
}

// 3. Use memo for expensive widgets
class ExpensiveWidget extends StatelessWidget {
  final String data;

  const ExpensiveWidget({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return _ExpensiveWidgetContent(data: data);
  }
}

class _ExpensiveWidgetContent extends StatelessWidget {
  final String data;

  const _ExpensiveWidgetContent({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    // Expensive computation
    final processedData = data.toUpperCase();
    return Text(processedData);
  }
}

// 4. Avoid rebuilds with const constructors
class RebuildExample extends StatelessWidget {
  const RebuildExample({super.key});

  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        Text('Static text 1'),
        Text('Static text 2'),
      ],
    );
  }
}

// 5. Use Provider/Riverpod for state management
class ProviderExample extends StatelessWidget {
  const ProviderExample({super.key});

  @override
  Widget build(BuildContext context) {
    final counter = Provider.of<CounterProvider>(context);
    return Text('Count: ${counter.count}');
  }
}
```

---

---

## Quick Start

### Flutter Project Structure

```
lib/
  main.dart
  models/
    user.dart
  services/
    api_service.dart
  screens/
    home_screen.dart
  widgets/
    custom_button.dart
  utils/
    constants.dart
```

### State Management (Provider)

```dart
class CounterProvider extends ChangeNotifier {
  int _count = 0;
  
  int get count => _count;
  
  void increment() {
    _count++;
    notifyListeners();
  }
}

// Usage
Consumer<CounterProvider>(
  builder: (context, counter, child) {
    return Text('Count: ${counter.count}');
  },
)
```

---

## Production Checklist

- [ ] **Project Structure**: Organized project structure
- [ ] **State Management**: Choose state management solution
- [ ] **Navigation**: Navigation setup
- [ ] **Theming**: Theme configuration
- [ ] **Platform Channels**: Native integration if needed
- [ ] **Async Patterns**: Proper async/await usage
- [ ] **Performance**: Performance optimization
- [ ] **Testing**: Unit and widget tests
- [ ] **Packages**: Use appropriate packages
- [ ] **Documentation**: Document code
- [ ] **CI/CD**: Automated builds
- [ ] **Error Handling**: Comprehensive error handling

---

## Anti-patterns

### ❌ Don't: No State Management

```dart
// ❌ Bad - No state management
int count = 0;
// State scattered everywhere!
```

```dart
// ✅ Good - State management
class CounterProvider extends ChangeNotifier {
  int count = 0;
  // Centralized state
}
```

### ❌ Don't: Build in Build

```dart
// ❌ Bad - Build in build
Widget build(BuildContext context) {
  return FutureBuilder(
    future: fetchData(),  // Called on every build!
    builder: (context, snapshot) => ...
  )
}
```

```dart
// ✅ Good - Initialize once
class _MyWidgetState extends State<MyWidget> {
  late Future<Data> _data;
  
  @override
  void initState() {
    super.initState();
    _data = fetchData();  // Called once
  }
  
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _data,
      builder: (context, snapshot) => ...
    )
  }
}
```

---

## Integration Points

- **React Native Patterns** (`31-mobile-development/react-native-patterns/`) - Cross-platform patterns
- **Mobile CI/CD** (`31-mobile-development/mobile-ci-cd/`) - CI/CD for Flutter
- **App Distribution** (`31-mobile-development/app-distribution/`) - Distribution

---

## Further Reading

- [Flutter Documentation](https://docs.flutter.dev/)
- [Flutter State Management](https://docs.flutter.dev/development/data-and-backend/state-mgmt)
- [Flutter Best Practices](https://docs.flutter.dev/development/best-practices)

## Resources

- [Flutter Documentation](https://docs.flutter.dev/)
- [Flutter Packages](https://pub.dev/)
- [Go Router](https://gorouter.dev/)
- [Riverpod](https://riverpod.dev/)
- [Flutter Samples](https://github.com/flutter/samples)
