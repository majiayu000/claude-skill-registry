# 🔧 Skill: Code Generation Workflows

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-code-generation` |
| **Nivel** | 🟢 Básico |
| **Versión** | 1.0.0 |
| **Keywords** | `code-gen`, `build-runner`, `freezed`, `json-serializable`, `injectable`, `auto-route` |
| **Referencia** | [build_runner Package](https://pub.dev/packages/build_runner), [Context7 MCP](https://github.com/upstash/context7) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `code-gen`
- `build-runner`
- `freezed`
- `json-serializable`
- `injectable`
- `auto-route`
- `code-generation`
- `@skill:code-generation`

### Ejemplos de Prompts

```
Configura code generation con freezed y json_serializable
```

```
Implementa dependency injection con injectable y code generation
```

```
@skill:code-generation - Setup completo de build_runner para el proyecto
```

```
Necesito generar modelos inmutables con freezed y serialización JSON
```

```
Configura auto_route para navigation con code generation
```

## 📖 Descripción

Code Generation en Flutter automatiza la creación de código boilerplate, reduciendo errores, mejorando type safety y aumentando dramáticamente la productividad del desarrollador. Este skill cubre las herramientas principales del ecosistema Flutter para generación de código.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Proyectos con muchos modelos de datos (DTOs, entities)
- Necesitas immutability con copyWith, equals, hashCode
- Serialización/deserialización JSON frecuente
- Dependency Injection en proyectos medianos a grandes
- Navigation compleja con deep linking
- Quieres reducir código boilerplate manual
- Type safety es crítico
- Equipos grandes (consistencia de código)

### ❌ Cuándo NO Usar Este Skill

- Prototipos muy rápidos (overhead inicial)
- Proyectos extremadamente simples (1-2 pantallas)
- Team no familiarizado con code generation
- Build times son críticos (aunque se puede optimizar)

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── models/
│   │   ├── user.dart              # Freezed + JSON
│   │   ├── user.freezed.dart      # Generated
│   │   ├── user.g.dart            # Generated
│   │   ├── product.dart
│   │   ├── product.freezed.dart
│   │   └── product.g.dart
│   │
│   ├── api/
│   │   ├── api_response.dart      # Generic response
│   │   ├── api_response.freezed.dart
│   │   └── api_response.g.dart
│   │
│   ├── routes/
│   │   ├── app_router.dart        # auto_route config
│   │   └── app_router.gr.dart     # Generated routes
│   │
│   ├── di/
│   │   ├── injection.dart         # Injectable config
│   │   └── injection.config.dart  # Generated DI
│   │
│   ├── core/
│   │   ├── converters/
│   │   │   ├── date_time_converter.dart
│   │   │   └── enum_converter.dart
│   │   └── modules/
│   │       └── third_party_module.dart
│   │
│   └── main.dart
│
├── test/
│   └── models/
│       └── user_test.dart
│
├── build.yaml                      # Build runner config
├── pubspec.yaml
└── analysis_options.yaml
```

## 📦 Dependencias Requeridas

```yaml
name: my_app
description: A Flutter app with code generation

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # Code Generation - Runtime dependencies
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  injectable: ^2.3.2
  get_it: ^7.6.4
  auto_route: ^7.8.4

  # Utilities
  equatable: ^2.0.5  # Optional: for non-freezed classes

dev_dependencies:
  flutter_test:
    sdk: flutter

  # Code Generation - Dev dependencies
  build_runner: ^2.4.6
  freezed: ^2.4.5
  json_serializable: ^6.7.1
  injectable_generator: ^2.4.1
  auto_route_generator: ^7.3.2

  # Linting
  flutter_lints: ^3.0.0
```

## 💻 Implementación

### 1. build_runner - Foundation

#### 1.1 Setup y Comandos Básicos

```bash
# Agregar dependencias
flutter pub add freezed_annotation json_annotation injectable get_it auto_route
flutter pub add dev:build_runner dev:freezed dev:json_serializable dev:injectable_generator dev:auto_route_generator

# ⚠️ IMPORTANTE: Ejecutar desde la raíz del proyecto (donde está mobile/)
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Generar código (one-time)
cd mobile
flutter pub run build_runner build
cd ..

# Generar con limpieza de conflictos
cd mobile
flutter pub run build_runner build --delete-conflicting-outputs
cd ..

# Watch mode (regenera automáticamente)
cd mobile
flutter pub run build_runner watch --delete-conflicting-outputs
cd ..

# Limpiar archivos generados
cd mobile
flutter pub run build_runner clean
cd ..
```

#### 1.2 Configuración build.yaml

```yaml
# build.yaml (raíz del proyecto)
targets:
  $default:
    builders:
      # Freezed
      freezed:
        enabled: true
        options:
          # Genera métodos copyWith, toString, ==, hashCode
          copy_with: true
          equal: true
          to_string: true

      # JSON Serializable
      json_serializable:
        enabled: true
        options:
          # Configuración global
          any_map: false
          checked: true
          create_factory: true
          create_to_json: true
          disallow_unrecognized_keys: false
          explicit_to_json: true
          field_rename: none
          generic_argument_factories: false
          ignore_unannotated: false

      # Injectable
      injectable_generator:injectable_builder:
        enabled: true
        options:
          auto_register: true

      # Auto Route
      auto_route_generator:
        enabled: true
        options:
          # Configuración de rutas
          routes_class_name: AppRouter

# Optimización de performance
global_options:
  # Cache builds
  build_cache:
    enabled: true

  # Builders a ejecutar
  runs_before:
    - freezed
    - json_serializable
    - injectable_generator
    - auto_route_generator
```

#### 1.3 .gitignore Configuration

```gitignore
# build_runner
*.g.dart
*.freezed.dart
*.gr.dart
*.config.dart

# Build cache
.dart_tool/
build/

# Generated files (opcional: commitear para CI/CD más rápido)
# Descomentar si NO quieres commitear archivos generados
# **/*.g.dart
# **/*.freezed.dart
# **/*.gr.dart
```

### 2. Freezed - Immutable Data Classes

#### 2.1 Modelo Básico

```dart
// lib/models/user.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatarUrl,
    @Default(false) bool isVerified,
    @Default([]) List<String> roles,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Uso:
void main() {
  // Crear instancia
  final user = User(
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
  );

  // copyWith (inmutable)
  final updatedUser = user.copyWith(name: 'Jane Doe');

  // Equality (automático)
  print(user == updatedUser); // false
  print(user == user.copyWith()); // true

  // toString (automático)
  print(user); // User(id: 1, name: John Doe, ...)

  // JSON serialization
  final json = user.toJson();
  final fromJson = User.fromJson(json);
}
```

#### 2.2 Unions y Pattern Matching

```dart
// lib/models/api_result.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'api_result.freezed.dart';

@freezed
class ApiResult<T> with _$ApiResult<T> {
  const factory ApiResult.success(T data) = Success<T>;
  const factory ApiResult.error(String message, {int? code}) = Error<T>;
  const factory ApiResult.loading() = Loading<T>;
}

// Uso con pattern matching:
void handleResult(ApiResult<User> result) {
  result.when(
    success: (user) => print('User: ${user.name}'),
    error: (message, code) => print('Error $code: $message'),
    loading: () => print('Loading...'),
  );

  // O con map
  final message = result.map(
    success: (value) => 'Success: ${value.data}',
    error: (err) => 'Error: ${err.message}',
    loading: (_) => 'Loading...',
  );

  // O con maybeWhen (con default)
  result.maybeWhen(
    success: (user) => print('Got user: ${user.name}'),
    orElse: () => print('Not success'),
  );
}
```

#### 2.3 Freezed con Custom Methods

```dart
// lib/models/product.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'product.freezed.dart';
part 'product.g.dart';

@freezed
class Product with _$Product {
  const Product._(); // Private constructor para custom methods

  const factory Product({
    required String id,
    required String name,
    required double price,
    @Default(0) int stock,
    @Default([]) List<String> images,
    DateTime? createdAt,
  }) = _Product;

  factory Product.fromJson(Map<String, dynamic> json) =>
      _$ProductFromJson(json);

  // Custom getters
  bool get isAvailable => stock > 0;

  bool get isNew {
    if (createdAt == null) return false;
    final daysSinceCreation = DateTime.now().difference(createdAt!).inDays;
    return daysSinceCreation <= 30;
  }

  String get displayPrice => '\$${price.toStringAsFixed(2)}';

  String get mainImage => images.isNotEmpty ? images.first : '';

  // Custom methods
  Product decrementStock([int amount = 1]) {
    return copyWith(stock: (stock - amount).clamp(0, stock));
  }

  Product addImage(String imageUrl) {
    return copyWith(images: [...images, imageUrl]);
  }
}
```

#### 2.4 Freezed con JSON Custom Converters

```dart
// lib/core/converters/date_time_converter.dart
import 'package:json_annotation/json_annotation.dart';

class DateTimeConverter implements JsonConverter<DateTime, String> {
  const DateTimeConverter();

  @override
  DateTime fromJson(String json) => DateTime.parse(json);

  @override
  String toJson(DateTime object) => object.toIso8601String();
}

class TimestampConverter implements JsonConverter<DateTime, int> {
  const TimestampConverter();

  @override
  DateTime fromJson(int json) => DateTime.fromMillisecondsSinceEpoch(json);

  @override
  int toJson(DateTime object) => object.millisecondsSinceEpoch;
}

// lib/models/order.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import '../core/converters/date_time_converter.dart';

part 'order.freezed.dart';
part 'order.g.dart';

@freezed
class Order with _$Order {
  const factory Order({
    required String id,
    required double total,
    @DateTimeConverter() required DateTime createdAt,
    @TimestampConverter() DateTime? completedAt,
  }) = _Order;

  factory Order.fromJson(Map<String, dynamic> json) => _$OrderFromJson(json);
}
```

#### 2.5 Freezed con Nested Objects

```dart
// lib/models/address.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'address.freezed.dart';
part 'address.g.dart';

@freezed
class Address with _$Address {
  const factory Address({
    required String street,
    required String city,
    required String country,
    String? zipCode,
  }) = _Address;

  factory Address.fromJson(Map<String, dynamic> json) =>
      _$AddressFromJson(json);
}

// lib/models/user_profile.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'address.dart';

part 'user_profile.freezed.dart';
part 'user_profile.g.dart';

@freezed
class UserProfile with _$UserProfile {
  const factory UserProfile({
    required String userId,
    required String name,
    Address? address,  // Nested object
    @Default([]) List<Address> addresses,  // List of objects
  }) = _UserProfile;

  factory UserProfile.fromJson(Map<String, dynamic> json) =>
      _$UserProfileFromJson(json);
}

// JSON example:
// {
//   "userId": "123",
//   "name": "John",
//   "address": {
//     "street": "Main St",
//     "city": "NYC",
//     "country": "USA"
//   },
//   "addresses": [...]
// }
```

### 3. json_serializable - JSON Serialization

#### 3.1 Configuración Básica

```dart
// lib/models/simple_model.dart
import 'package:json_annotation/json_annotation.dart';

part 'simple_model.g.dart';

@JsonSerializable()
class SimpleModel {
  final String id;
  final String name;

  @JsonKey(name: 'email_address')  // Map to different JSON key
  final String email;

  @JsonKey(includeIfNull: false)  // Omit if null
  final String? phone;

  @JsonKey(defaultValue: false)  // Default value
  final bool isActive;

  SimpleModel({
    required this.id,
    required this.name,
    required this.email,
    this.phone,
    this.isActive = false,
  });

  factory SimpleModel.fromJson(Map<String, dynamic> json) =>
      _$SimpleModelFromJson(json);

  Map<String, dynamic> toJson() => _$SimpleModelToJson(this);
}
```

#### 3.2 Custom Converters

```dart
// lib/core/converters/enum_converter.dart
import 'package:json_annotation/json_annotation.dart';

enum UserRole {
  admin,
  user,
  guest,
}

class UserRoleConverter implements JsonConverter<UserRole, String> {
  const UserRoleConverter();

  @override
  UserRole fromJson(String json) {
    return UserRole.values.firstWhere(
      (role) => role.name.toLowerCase() == json.toLowerCase(),
      orElse: () => UserRole.guest,
    );
  }

  @override
  String toJson(UserRole object) => object.name;
}

// Uso:
@JsonSerializable()
class User {
  final String id;

  @UserRoleConverter()
  final UserRole role;

  User({required this.id, required this.role});

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

#### 3.3 Generic Classes

```dart
// lib/models/paginated_response.dart
import 'package:json_annotation/json_annotation.dart';

part 'paginated_response.g.dart';

@JsonSerializable(genericArgumentFactories: true)
class PaginatedResponse<T> {
  final List<T> data;
  final int page;
  final int totalPages;
  final int totalItems;

  PaginatedResponse({
    required this.data,
    required this.page,
    required this.totalPages,
    required this.totalItems,
  });

  factory PaginatedResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object? json) fromJsonT,
  ) =>
      _$PaginatedResponseFromJson(json, fromJsonT);

  Map<String, dynamic> toJson(Object Function(T value) toJsonT) =>
      _$PaginatedResponseToJson(this, toJsonT);
}

// Uso:
final response = PaginatedResponse<Product>.fromJson(
  jsonData,
  (json) => Product.fromJson(json as Map<String, dynamic>),
);
```

### 4. injectable - Dependency Injection

#### 4.1 Setup Inicial

```dart
// lib/di/injection.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

import 'injection.config.dart';

final getIt = GetIt.instance;

@InjectableInit(
  initializerName: 'init',
  preferRelativeImports: true,
  asExtension: true,
)
void configureDependencies() => getIt.init();

// lib/main.dart
void main() {
  configureDependencies();
  runApp(MyApp());
}
```

#### 4.2 Injectable Annotations

```dart
// lib/services/api_service.dart
import 'package:injectable/injectable.dart';
import 'package:dio/dio.dart';

@injectable
class ApiService {
  final Dio dio;

  ApiService(this.dio);

  Future<List<User>> getUsers() async {
    final response = await dio.get('/users');
    return (response.data as List)
        .map((json) => User.fromJson(json))
        .toList();
  }
}

// lib/repositories/user_repository.dart
@injectable
class UserRepository {
  final ApiService apiService;

  UserRepository(this.apiService);

  Future<User> getUserById(String id) async {
    // Implementation
  }
}

// lib/blocs/user_bloc.dart
@injectable
class UserBloc {
  final UserRepository repository;

  UserBloc(this.repository);
}
```

#### 4.3 Singletons y Lazy Singletons

```dart
// lib/services/analytics_service.dart
@singleton  // Single instance throughout app lifecycle
class AnalyticsService {
  AnalyticsService() {
    print('AnalyticsService created');
  }

  void logEvent(String event) {
    print('Event: $event');
  }
}

// lib/services/cache_service.dart
@lazySingleton  // Created only when first accessed
class CacheService {
  CacheService() {
    print('CacheService created lazily');
  }

  Future<void> cache(String key, dynamic value) async {
    // Implementation
  }
}
```

#### 4.4 Named Dependencies

```dart
// lib/services/http_service.dart
@Named('authenticated')
@injectable
class AuthenticatedHttpService {
  // Implementation with auth
}

@Named('public')
@injectable
class PublicHttpService {
  // Implementation without auth
}

// Uso:
@injectable
class MyService {
  final AuthenticatedHttpService authHttp;
  final PublicHttpService publicHttp;

  MyService(
    @Named('authenticated') this.authHttp,
    @Named('public') this.publicHttp,
  );
}
```

#### 4.5 Modules para Third-Party

```dart
// lib/di/modules/third_party_module.dart
import 'package:injectable/injectable.dart';
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

@module
abstract class ThirdPartyModule {
  @lazySingleton
  Dio get dio => Dio(
        BaseOptions(
          baseUrl: 'https://api.example.com',
          connectTimeout: const Duration(seconds: 30),
        ),
      );

  @preResolve  // Async initialization
  Future<SharedPreferences> get prefs => SharedPreferences.getInstance();
}

// lib/main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await configureDependencies();  // Await para preResolve
  runApp(MyApp());
}
```

#### 4.6 Environments

```dart
// lib/services/logger_service.dart
@dev
@injectable
class DebugLoggerService implements LoggerService {
  @override
  void log(String message) => print('[DEBUG] $message');
}

@prod
@injectable
class ProductionLoggerService implements LoggerService {
  @override
  void log(String message) {
    // Send to remote logging service
  }
}

// lib/di/injection.dart
@InjectableInit(
  initializerName: 'init',
  preferRelativeImports: true,
  asExtension: true,
)
void configureDependencies(String environment) =>
    getIt.init(environment: environment);

// lib/main.dart
void main() {
  const environment = String.fromEnvironment('ENV', defaultValue: 'dev');
  configureDependencies(environment);
  runApp(MyApp());
}

// Run with environment:
// flutter run --dart-define=ENV=prod
```

### 5. auto_route - Navigation Code Generation

#### 5.1 Setup Básico

```dart
// lib/routes/app_router.dart
import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';

import '../screens/home_screen.dart';
import '../screens/profile_screen.dart';
import '../screens/product_detail_screen.dart';

part 'app_router.gr.dart';

@AutoRouterConfig()
class AppRouter extends _$AppRouter {
  @override
  List<AutoRoute> get routes => [
        AutoRoute(page: HomeRoute.page, initial: true),
        AutoRoute(page: ProfileRoute.page),
        AutoRoute(page: ProductDetailRoute.page),
      ];
}

// lib/main.dart
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final _appRouter = AppRouter();

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _appRouter.config(),
    );
  }
}
```

#### 5.2 Screen Setup

```dart
// lib/screens/home_screen.dart
import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';

@RoutePage()
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            context.router.push(const ProfileRoute());
          },
          child: const Text('Go to Profile'),
        ),
      ),
    );
  }
}

// lib/screens/product_detail_screen.dart
@RoutePage()
class ProductDetailScreen extends StatelessWidget {
  final String productId;

  const ProductDetailScreen({
    super.key,
    @PathParam('id') required this.productId,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Product $productId')),
      body: Center(child: Text('Details for $productId')),
    );
  }
}
```

#### 5.3 Nested Navigation

```dart
// lib/routes/app_router.dart
@AutoRouterConfig()
class AppRouter extends _$AppRouter {
  @override
  List<AutoRoute> get routes => [
        AutoRoute(
          page: MainRoute.page,
          initial: true,
          children: [
            AutoRoute(page: HomeRoute.page, initial: true),
            AutoRoute(page: SearchRoute.page),
            AutoRoute(page: ProfileRoute.page),
          ],
        ),
        AutoRoute(page: ProductDetailRoute.page),
        AutoRoute(page: SettingsRoute.page),
      ];
}

// lib/screens/main_screen.dart
@RoutePage()
class MainScreen extends StatelessWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AutoTabsScaffold(
      routes: const [
        HomeRoute(),
        SearchRoute(),
        ProfileRoute(),
      ],
      bottomNavigationBuilder: (_, tabsRouter) {
        return BottomNavigationBar(
          currentIndex: tabsRouter.activeIndex,
          onTap: tabsRouter.setActiveIndex,
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
            BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
            BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
          ],
        );
      },
    );
  }
}
```

#### 5.4 Route Guards

```dart
// lib/routes/guards/auth_guard.dart
import 'package:auto_route/auto_route.dart';

class AuthGuard extends AutoRouteGuard {
  @override
  void onNavigation(NavigationResolver resolver, StackRouter router) {
    final isAuthenticated = checkAuth(); // Your auth logic

    if (isAuthenticated) {
      resolver.next(true);
    } else {
      resolver.redirect(const LoginRoute());
    }
  }

  bool checkAuth() {
    // Check if user is authenticated
    return false;
  }
}

// lib/routes/app_router.dart
@AutoRouterConfig()
class AppRouter extends _$AppRouter {
  @override
  List<AutoRoute> get routes => [
        AutoRoute(page: LoginRoute.page),
        AutoRoute(
          page: ProfileRoute.page,
          guards: [AuthGuard()],  // Protected route
        ),
      ];
}
```

## 🔄 Workflows Completos

### Workflow 1: Complete User Model

```dart
// lib/models/user.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const User._();

  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatarUrl,
    @Default(UserRole.user) UserRole role,
    @Default([]) List<String> permissions,
    DateTime? lastLoginAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  // Custom getters
  bool get isAdmin => role == UserRole.admin;
  bool get hasRecentActivity {
    if (lastLoginAt == null) return false;
    return DateTime.now().difference(lastLoginAt!).inDays < 7;
  }

  // Custom methods
  bool hasPermission(String permission) {
    return permissions.contains(permission) || isAdmin;
  }
}

enum UserRole {
  admin,
  user,
  guest,
}
```

### Workflow 2: API Service with DI

```dart
// lib/services/user_service.dart
import 'package:injectable/injectable.dart';
import '../models/user.dart';
import 'api_service.dart';

@injectable
class UserService {
  final ApiService _apiService;

  UserService(this._apiService);

  Future<List<User>> getUsers() async {
    final response = await _apiService.get('/users');
    return (response.data as List)
        .map((json) => User.fromJson(json))
        .toList();
  }

  Future<User> getUserById(String id) async {
    final response = await _apiService.get('/users/$id');
    return User.fromJson(response.data);
  }

  Future<User> updateUser(User user) async {
    final response = await _apiService.put(
      '/users/${user.id}',
      data: user.toJson(),
    );
    return User.fromJson(response.data);
  }
}

// Uso en BLoC/Cubit:
@injectable
class UserBloc extends Bloc<UserEvent, UserState> {
  final UserService _userService;

  UserBloc(this._userService) : super(UserInitial());
}
```

### Workflow 3: Complete App Setup

```bash
# 1. Crear proyecto
flutter create my_app
cd my_app

# 2. Agregar dependencias
flutter pub add freezed_annotation json_annotation injectable get_it auto_route
flutter pub add dev:build_runner dev:freezed dev:json_serializable dev:injectable_generator dev:auto_route_generator

# 3. Crear estructura
mkdir -p lib/{models,services,routes,di,screens}

# 4. Crear archivos base
# - lib/di/injection.dart
# - lib/routes/app_router.dart
# - lib/models/user.dart

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# 5. Generar código
cd mobile
flutter pub run build_runner build --delete-conflicting-outputs
cd ..

# 6. Ejecutar en watch mode durante desarrollo
cd mobile
flutter pub run build_runner watch --delete-conflicting-outputs
cd ..
```

## 🎯 Mejores Prácticas

### 1. Organización de Archivos

✅ **DO:**
```
lib/
├── models/          # Todos los modelos juntos
│   ├── user.dart
│   └── product.dart
├── di/              # DI configuration
│   └── injection.dart
└── routes/          # Navigation
    └── app_router.dart
```

❌ **DON'T:**
```
lib/
└── features/
    ├── auth/
    │   └── user.dart         # ❌ Fragmentado
    └── products/
        └── product.dart      # ❌ Dificulta generación
```

### 2. Commits de Archivos Generados

**Opción A: Commitear archivos generados**
✅ Ventajas:
- CI/CD más rápido (no regenera)
- Developers no necesitan regenerar
- Code review completo

❌ Desventajas:
- Merge conflicts frecuentes
- Ruido en diffs

**Opción B: NO commitear (usar .gitignore)**
✅ Ventajas:
- Diffs limpios
- Menos conflicts

❌ Desventajas:
- CI/CD debe regenerar
- Setup inicial más complejo

**Recomendación:** Commitear en proyectos pequeños/medianos, NO commitear en grandes con muchos developers.

### 3. Watch Mode Durante Desarrollo

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Terminal 1: Watch mode
cd mobile
flutter pub run build_runner watch --delete-conflicting-outputs
cd ..

# Terminal 2: Hot reload app
cd mobile
flutter run
cd ..
```

### 4. CI/CD Integration

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.35.0'
          cache: true

      - name: Get dependencies
        working-directory: mobile
        run: flutter pub get

      - name: Generate code
        working-directory: mobile
        run: flutter pub run build_runner build --delete-conflicting-outputs

      - name: Analyze
        working-directory: mobile
        run: flutter analyze

      - name: Test
        run: flutter test
```

### 5. Performance Optimization

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Use cache entre builds
cd mobile
flutter pub run build_runner build --delete-conflicting-outputs
cd ..

# Para builds muy lentos, usa:
cd mobile
flutter pub run build_runner build --delete-conflicting-outputs --low-resources-mode
cd ..

# Limpia cache si hay problemas
cd mobile
flutter clean
flutter pub get
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
cd ..
```

### 6. Freezed vs Manual Implementation

**Usa Freezed cuando:**
- Necesitas immutability
- copyWith frequent
- Union types
- Pattern matching
- Serialización JSON

**Usa manual cuando:**
- Clases muy simples (2-3 fields)
- No necesitas copyWith
- Mutable state requerido

## 🚨 Troubleshooting

### Error: "Conflicting outputs"

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Solución: Usar --delete-conflicting-outputs
cd mobile
flutter pub run build_runner build --delete-conflicting-outputs
cd ..
```

### Error: "Part file doesn't exist"

```dart
// Verifica que la declaración part esté correcta:
part 'user.freezed.dart';  // ✅ Correcto
part 'user_freezed.dart';  // ❌ Incorrecto (sin punto)
```

### Error: Build muy lento

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# 1. Limpiar cache
cd mobile
flutter clean
flutter pub get
cd ..

# 2. Usar low-resources-mode
cd mobile
flutter pub run build_runner build --low-resources-mode
cd ..

# 3. Reducir builders activos en build.yaml
```

### Error: "Ambiguous imports"

```dart
// Si tienes conflictos de imports:
import 'package:freezed_annotation/freezed_annotation.dart' as freezed;

@freezed.freezed
class User with _$User {
  // ...
}
```

### Error: Generated file no actualiza

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Forzar regeneración
cd mobile
flutter pub run build_runner clean
flutter pub run build_runner build --delete-conflicting-outputs
cd ..
```

### Error: JSON serialization falla

```dart
// Verifica que toJson use explicitToJson
@JsonSerializable(explicitToJson: true)
class User {
  final Address address;  // Nested object
  // ...
}
```

## 🔧 Scripts de Automatización

### Makefile

```makefile
# Makefile
.PHONY: generate watch clean get help

help:
	@echo "Comandos disponibles:"
	@echo "  make generate - Generar código"
	@echo "  make watch    - Watch mode"
	@echo "  make clean    - Limpiar"
	@echo "  make get      - Obtener dependencias"

get:
	cd mobile && flutter pub get

generate: get
	cd mobile && flutter pub run build_runner build --delete-conflicting-outputs

watch: get
	cd mobile && flutter pub run build_runner watch --delete-conflicting-outputs

clean:
	cd mobile && flutter clean
	cd mobile && flutter pub get
	cd mobile && flutter pub run build_runner clean

rebuild: clean generate

# Uso:
# make generate
# make watch
```

### Bash Script

```bash
#!/bin/bash
# scripts/generate.sh

echo "🔧 Starting code generation..."

# Clean if flag passed
if [ "$1" == "--clean" ]; then
    echo "🧹 Cleaning..."
    flutter clean
    flutter pub get
    flutter pub run build_runner clean
fi

# Generate
echo "⚡ Generating code..."
flutter pub run build_runner build --delete-conflicting-outputs

echo "✅ Code generation complete!"

# Uso:
# ./scripts/generate.sh
# ./scripts/generate.sh --clean
```

## 🧪 Testing Generated Code

```dart
// test/models/user_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/models/user.dart';

void main() {
  group('User Model', () {
    test('should create user from JSON', () {
      final json = {
        'id': '1',
        'name': 'John Doe',
        'email': 'john@example.com',
      };

      final user = User.fromJson(json);

      expect(user.id, '1');
      expect(user.name, 'John Doe');
      expect(user.email, 'john@example.com');
    });

    test('should convert user to JSON', () {
      const user = User(
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
      );

      final json = user.toJson();

      expect(json['id'], '1');
      expect(json['name'], 'John Doe');
      expect(json['email'], 'john@example.com');
    });

    test('copyWith should create new instance', () {
      const user = User(
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
      );

      final updated = user.copyWith(name: 'Jane Doe');

      expect(updated.id, user.id);
      expect(updated.name, 'Jane Doe');
      expect(updated.email, user.email);
      expect(updated != user, true);
    });

    test('equality should work correctly', () {
      const user1 = User(
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
      );

      const user2 = User(
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
      );

      expect(user1, user2);
    });
  });
}
```

## 🤖 Context7 MCP Integration

Context7 es un MCP server que proporciona documentación actualizada de código para LLMs y editores de código AI. Está configurado en `mcp.json` y permite obtener documentación en tiempo real de las librerías de code generation.

### Configuración

Context7 ya está configurado en `mcp.json`:

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
    "env": {
      "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
    }
  }
}
```

**Nota:** Puedes usar Context7 sin API key (con rate limits) o obtener una API key gratuita en [context7.com/dashboard](https://context7.com/dashboard).

### Uso con IA

Cuando trabajes con code generation, puedes pedirle a tu asistente de IA:

```
Usa context7 para obtener la documentación más reciente de freezed
```

```
Implementa json_serializable usando la documentación de context7
```

```
Consulta context7 para la mejor práctica de injectable en Flutter
```

### Herramientas Disponibles

Context7 MCP proporciona las siguientes herramientas:

1. **`resolve-library-id`**: Resuelve un nombre de librería en un ID compatible con Context7
   - Ejemplo: `freezed` → `/freezed/freezed`

2. **`get-library-docs`**: Obtiene documentación de una librería usando su ID de Context7
   - Ejemplo: `/freezed/freezed` para documentación de Freezed
   - Soporta `topic` para enfocar la documentación (ej: "immutability", "unions")
   - Soporta `page` para paginación (1-10)

### Ejemplos de Uso

#### Obtener Documentación de Freezed

```
use context7 get-library-docs /freezed/freezed topic="immutability unions"
```

#### Obtener Documentación de build_runner

```
use context7 get-library-docs /dart-lang/build_runner topic="code generation"
```

#### Obtener Documentación de json_serializable

```
use context7 get-library-docs /dart-lang/json_serializable topic="custom converters"
```

### Librerías de Code Generation en Context7

Las siguientes librerías están disponibles en Context7:

- `/freezed/freezed` - Freezed para clases inmutables
- `/dart-lang/build_runner` - build_runner para generación de código
- `/dart-lang/json_serializable` - Serialización JSON
- `/dart-lang/injectable` - Dependency Injection
- `/dart-lang/auto_route` - Navigation con code generation

### Tips

1. **Usa Library ID directamente**: Si conoces el ID exacto, úsalo en tu prompt:
   ```
   Implementa freezed usando /freezed/freezed
   ```

2. **Especifica topics**: Enfoca la documentación en temas específicos:
   ```
   use context7 get-library-docs /freezed/freezed topic="copyWith unions"
   ```

3. **Paginación**: Si la documentación es extensa, usa `page=2`, `page=3`, etc.

### Recursos

- [Context7 GitHub](https://github.com/upstash/context7)
- [Context7 Website](https://context7.com/)
- [Context7 Dashboard](https://context7.com/dashboard) - Obtén tu API key gratuita

## 📚 Recursos Adicionales

### Documentación Oficial
- [build_runner](https://pub.dev/packages/build_runner)
- [freezed](https://pub.dev/packages/freezed)
- [json_serializable](https://pub.dev/packages/json_serializable)
- [injectable](https://pub.dev/packages/injectable)
- [auto_route](https://pub.dev/packages/auto_route)

### Tutoriales
- [Freezed Complete Guide](https://codewithandrea.com/articles/flutter-freezed-data-classes/)
- [Injectable DI Tutorial](https://resocoder.com/flutter-clean-architecture-tdd/)
- [auto_route Navigation](https://autoroute.vercel.app/)

### Videos
- [Code Generation in Flutter - Reso Coder](https://www.youtube.com/watch?v=w7pxubJBaE0)
- [Freezed Deep Dive - Flutter Explained](https://www.youtube.com/watch?v=ApvMmTrBaFI)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md) - Arquitectura con DI
- [MVVM](../mvvm/SKILL.md) - MVVM con code generation
- [Feature-First](../feature-first/SKILL.md) - Organización de código generado
- [Testing](../testing/SKILL.md) - Testing de código generado

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,250+
