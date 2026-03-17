# 🎨 Skill: Arquitectura Modular

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-modular-architecture` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `modular`, `modular-architecture`, `module`, `multi-module` |
| **Referencia** | [Flutter Modular Package](https://pub.dev/packages/flutter_modular) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `modular`
- `modular-architecture`
- `module`
- `multi-module`
- `@skill:modular`

### Ejemplos de Prompts

```
Crea una app con arquitectura modular
```

```
Implementa módulos independientes para auth y productos
```

```
@skill:modular - Estructura la app en módulos reutilizables
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

La Arquitectura Modular divide la aplicación en módulos independientes y reutilizables, cada uno con su propia lógica, UI, rutas y dependencias. Cada módulo puede funcionar de manera autónoma y ser desarrollado, testeado y desplegado independientemente.

### ✅ Cuándo Usar Este Skill

- Aplicaciones grandes con múltiples features
- Equipos grandes trabajando en paralelo
- Necesitas reutilizar módulos entre proyectos
- Quieres reducir tiempos de compilación
- Necesitas deployment independiente de módulos
- Quieres aislar features y reducir acoplamiento
- Planeas crear un ecosistema de apps relacionadas

### ❌ Cuándo NO Usar Este Skill

- Aplicaciones pequeñas o prototipos
- Equipos muy pequeños (1-2 desarrolladores)
- No hay necesidad de reutilización
- Prefieres simplicidad sobre escalabilidad

## 🏗️ Estructura del Proyecto

```
my_app/
├── packages/
│   ├── core/
│   │   ├── lib/
│   │   │   ├── design_system/
│   │   │   │   ├── atoms/
│   │   │   │   │   ├── buttons.dart
│   │   │   │   │   ├── inputs.dart
│   │   │   │   │   └── typography.dart
│   │   │   │   ├── molecules/
│   │   │   │   │   ├── cards.dart
│   │   │   │   │   └── dialogs.dart
│   │   │   │   └── tokens/
│   │   │   │       ├── colors.dart
│   │   │   │       ├── spacing.dart
│   │   │   │       └── typography.dart
│   │   │   ├── networking/
│   │   │   │   ├── dio_client.dart
│   │   │   │   ├── interceptors/
│   │   │   │   └── api_endpoints.dart
│   │   │   ├── storage/
│   │   │   │   ├── secure_storage.dart
│   │   │   │   └── shared_preferences.dart
│   │   │   ├── utils/
│   │   │   │   ├── validators.dart
│   │   │   │   ├── formatters.dart
│   │   │   │   └── extensions/
│   │   │   ├── error/
│   │   │   │   ├── failures.dart
│   │   │   │   └── exceptions.dart
│   │   │   └── core.dart
│   │   └── pubspec.yaml
│   │
│   ├── auth_module/
│   │   ├── lib/
│   │   │   ├── src/
│   │   │   │   ├── data/
│   │   │   │   │   ├── datasources/
│   │   │   │   │   ├── models/
│   │   │   │   │   └── repositories/
│   │   │   │   ├── domain/
│   │   │   │   │   ├── entities/
│   │   │   │   │   ├── repositories/
│   │   │   │   │   └── usecases/
│   │   │   │   ├── presentation/
│   │   │   │   │   ├── bloc/
│   │   │   │   │   ├── screens/
│   │   │   │   │   └── widgets/
│   │   │   │   └── auth_module.dart
│   │   │   └── auth_module.dart (barrel file)
│   │   ├── test/
│   │   └── pubspec.yaml
│   │
│   ├── products_module/
│   │   ├── lib/
│   │   │   ├── src/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   ├── presentation/
│   │   │   │   └── products_module.dart
│   │   │   └── products_module.dart
│   │   ├── test/
│   │   └── pubspec.yaml
│   │
│   ├── cart_module/
│   │   ├── lib/
│   │   │   ├── src/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   ├── presentation/
│   │   │   │   └── cart_module.dart
│   │   │   └── cart_module.dart
│   │   ├── test/
│   │   └── pubspec.yaml
│   │
│   └── payment_module/
│       ├── lib/
│       │   ├── src/
│       │   │   ├── data/
│       │   │   ├── domain/
│       │   │   ├── presentation/
│       │   │   └── payment_module.dart
│       │   └── payment_module.dart
│       ├── test/
│       └── pubspec.yaml
│
├── lib/
│   ├── app/
│   │   ├── app_module.dart
│   │   ├── app_widget.dart
│   │   └── routes.dart
│   └── main.dart
├── test/
├── pubspec.yaml
└── melos.yaml
```

## 📦 Dependencias Requeridas

### App Principal (pubspec.yaml)

```yaml
name: my_modular_app
description: A modular Flutter application
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # Modular routing and DI
  flutter_modular: ^6.3.2

  # State management (opcional, según preferencia)
  flutter_bloc: ^8.1.3

  # Módulos locales
  core:
    path: packages/core
  auth_module:
    path: packages/auth_module
  products_module:
    path: packages/products_module
  cart_module:
    path: packages/cart_module
  payment_module:
    path: packages/payment_module

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

### Core Package (packages/core/pubspec.yaml)

```yaml
name: core
description: Core utilities and design system
version: 1.0.0
publish_to: none

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # Networking
  dio: ^5.4.0

  # Storage
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0

  # Utils
  equatable: ^2.0.5
  dartz: ^0.10.1
  intl: ^0.19.0

dev_dependencies:
  flutter_test:
    sdk: flutter
```

### Feature Module (packages/auth_module/pubspec.yaml)

```yaml
name: auth_module
description: Authentication module
version: 1.0.0
publish_to: none

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # Core dependency
  core:
    path: ../core

  # Modular
  flutter_modular: ^6.3.2

  # State management
  flutter_bloc: ^8.1.3

  # Utils
  equatable: ^2.0.5
  dartz: ^0.10.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.4
  mocktail: ^1.0.1
```

### Melos para Gestión de Monorepo (melos.yaml)

```yaml
name: my_modular_app
repository: https://github.com/your-org/my_modular_app

packages:
  - packages/**
  - .

command:
  bootstrap:
    usePubspecOverrides: true

scripts:
  analyze:
    run: melos exec -- flutter analyze
    description: Run flutter analyze in all packages (ejecutar desde raíz del proyecto)

  test:
    run: melos exec -- flutter test
    description: Run tests in all packages (ejecutar desde raíz del proyecto)

  format:
    run: melos exec -- dart format . --set-exit-if-changed
    description: Format all packages (ejecutar desde raíz del proyecto)

  clean:
    run: melos exec -- flutter clean
    description: Clean all packages (ejecutar desde raíz del proyecto)

  get:
    run: melos exec -- flutter pub get
    description: Get dependencies for all packages (ejecutar desde raíz del proyecto)
```

## 💻 Implementación

### 1. Core Module - Design System

```dart
// packages/core/lib/design_system/tokens/colors.dart
import 'package:flutter/material.dart';

class AppColors {
  // Brand colors
  static const Color primary = Color(0xFF6200EE);
  static const Color primaryVariant = Color(0xFF3700B3);
  static const Color secondary = Color(0xFF03DAC6);
  static const Color secondaryVariant = Color(0xFF018786);

  // Neutral colors
  static const Color background = Color(0xFFFFFFFF);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color error = Color(0xFFB00020);

  // Text colors
  static const Color onPrimary = Color(0xFFFFFFFF);
  static const Color onSecondary = Color(0xFF000000);
  static const Color onBackground = Color(0xFF000000);
  static const Color onSurface = Color(0xFF000000);
  static const Color onError = Color(0xFFFFFFFF);

  // Grays
  static const Color gray50 = Color(0xFFFAFAFA);
  static const Color gray100 = Color(0xFFF5F5F5);
  static const Color gray200 = Color(0xFFEEEEEE);
  static const Color gray300 = Color(0xFFE0E0E0);
  static const Color gray400 = Color(0xFFBDBDBD);
  static const Color gray500 = Color(0xFF9E9E9E);
  static const Color gray600 = Color(0xFF757575);
  static const Color gray700 = Color(0xFF616161);
  static const Color gray800 = Color(0xFF424242);
  static const Color gray900 = Color(0xFF212121);
}
```

```dart
// packages/core/lib/design_system/atoms/buttons.dart
import 'package:flutter/material.dart';
import '../tokens/colors.dart';
import '../tokens/spacing.dart';

class PrimaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;
  final IconData? icon;

  const PrimaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.onPrimary,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.lg,
          vertical: AppSpacing.md,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: isLoading
          ? const SizedBox(
              height: 20,
              width: 20,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(AppColors.onPrimary),
              ),
            )
          : Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (icon != null) ...[
                  Icon(icon, size: 20),
                  const SizedBox(width: AppSpacing.sm),
                ],
                Text(text),
              ],
            ),
    );
  }
}

class SecondaryButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final IconData? icon;

  const SecondaryButton({
    super.key,
    required this.text,
    this.onPressed,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      onPressed: onPressed,
      style: OutlinedButton.styleFrom(
        foregroundColor: AppColors.primary,
        side: const BorderSide(color: AppColors.primary),
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.lg,
          vertical: AppSpacing.md,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (icon != null) ...[
            Icon(icon, size: 20),
            const SizedBox(width: AppSpacing.sm),
          ],
          Text(text),
        ],
      ),
    );
  }
}
```

### 2. Core Module - Networking

```dart
// packages/core/lib/networking/dio_client.dart
import 'package:dio/dio.dart';
import 'interceptors/auth_interceptor.dart';
import 'interceptors/logging_interceptor.dart';

class DioClient {
  final Dio _dio;

  DioClient({
    required String baseUrl,
    Duration? connectTimeout,
    Duration? receiveTimeout,
  }) : _dio = Dio(
          BaseOptions(
            baseUrl: baseUrl,
            connectTimeout: connectTimeout ?? const Duration(seconds: 30),
            receiveTimeout: receiveTimeout ?? const Duration(seconds: 30),
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
          ),
        ) {
    _dio.interceptors.addAll([
      AuthInterceptor(),
      LoggingInterceptor(),
    ]);
  }

  Dio get dio => _dio;

  // GET request
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.get<T>(
      path,
      queryParameters: queryParameters,
      options: options,
    );
  }

  // POST request
  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.post<T>(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }

  // PUT request
  Future<Response<T>> put<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.put<T>(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }

  // DELETE request
  Future<Response<T>> delete<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    return await _dio.delete<T>(
      path,
      data: data,
      queryParameters: queryParameters,
      options: options,
    );
  }
}
```

### 3. Feature Module - Auth Module

```dart
// packages/auth_module/lib/src/auth_module.dart
import 'package:flutter_modular/flutter_modular.dart';
import 'package:core/core.dart';
import 'data/datasources/auth_remote_datasource.dart';
import 'data/repositories/auth_repository_impl.dart';
import 'domain/repositories/auth_repository.dart';
import 'domain/usecases/login_usecase.dart';
import 'domain/usecases/logout_usecase.dart';
import 'domain/usecases/register_usecase.dart';
import 'domain/usecases/get_current_user_usecase.dart';
import 'presentation/bloc/auth_bloc.dart';
import 'presentation/bloc/login/login_cubit.dart';
import 'presentation/screens/login_screen.dart';
import 'presentation/screens/register_screen.dart';

class AuthModule extends Module {
  @override
  List<Bind> get binds => [
    // Data sources
    Bind.singleton<AuthRemoteDataSource>(
      (i) => AuthRemoteDataSourceImpl(dioClient: i()),
    ),

    // Repositories
    Bind.singleton<AuthRepository>(
      (i) => AuthRepositoryImpl(remoteDataSource: i()),
    ),

    // Use cases
    Bind.factory<LoginUseCase>(
      (i) => LoginUseCase(repository: i()),
    ),
    Bind.factory<LogoutUseCase>(
      (i) => LogoutUseCase(repository: i()),
    ),
    Bind.factory<RegisterUseCase>(
      (i) => RegisterUseCase(repository: i()),
    ),
    Bind.factory<GetCurrentUserUseCase>(
      (i) => GetCurrentUserUseCase(repository: i()),
    ),

    // BLoCs
    Bind.singleton<AuthBloc>(
      (i) => AuthBloc(
        loginUseCase: i(),
        logoutUseCase: i(),
        getCurrentUserUseCase: i(),
      ),
    ),
    Bind.factory<LoginCubit>(
      (i) => LoginCubit(loginUseCase: i()),
    ),
  ];

  @override
  List<ModularRoute> get routes => [
    ChildRoute(
      '/',
      child: (context, args) => const LoginScreen(),
    ),
    ChildRoute(
      '/register',
      child: (context, args) => const RegisterScreen(),
    ),
  ];
}
```

```dart
// packages/auth_module/lib/src/presentation/screens/login_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_modular/flutter_modular.dart';
import 'package:core/core.dart';
import '../bloc/login/login_cubit.dart';
import '../widgets/login_form.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => Modular.get<LoginCubit>(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Login'),
        ),
        body: BlocListener<LoginCubit, LoginState>(
          listener: (context, state) {
            state.maybeWhen(
              success: () {
                // Navegar al home
                Modular.to.navigate('/home/');
              },
              error: (message) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(message),
                    backgroundColor: AppColors.error,
                  ),
                );
              },
              orElse: () {},
            );
          },
          child: const Padding(
            padding: EdgeInsets.all(AppSpacing.lg),
            child: LoginForm(),
          ),
        ),
      ),
    );
  }
}
```

### 4. App Module - Configuración Principal

```dart
// lib/app/app_module.dart
import 'package:flutter_modular/flutter_modular.dart';
import 'package:core/core.dart';
import 'package:auth_module/auth_module.dart';
import 'package:products_module/products_module.dart';
import 'package:cart_module/cart_module.dart';
import 'package:payment_module/payment_module.dart';
import 'app_widget.dart';

class AppModule extends Module {
  @override
  List<Bind> get binds => [
    // Core services
    Bind.singleton<DioClient>(
      (i) => DioClient(
        baseUrl: 'https://api.example.com',
      ),
    ),
  ];

  @override
  List<ModularRoute> get routes => [
    ModuleRoute(
      '/auth',
      module: AuthModule(),
    ),
    ModuleRoute(
      '/home',
      module: ProductsModule(),
      guards: [AuthGuard()],  // Requiere autenticación
    ),
    ModuleRoute(
      '/cart',
      module: CartModule(),
      guards: [AuthGuard()],
    ),
    ModuleRoute(
      '/payment',
      module: PaymentModule(),
      guards: [AuthGuard()],
    ),
    ChildRoute(
      '/',
      child: (context, args) => const AppWidget(),
    ),
  ];
}

// Guard para proteger rutas
class AuthGuard extends RouteGuard {
  @override
  Future<bool> canActivate(String path, ModularRoute route) async {
    final authBloc = Modular.get<AuthBloc>();
    final state = authBloc.state;

    return state.maybeWhen(
      authenticated: (_) => true,
      orElse: () {
        Modular.to.navigate('/auth/');
        return false;
      },
    );
  }
}
```

```dart
// lib/app/app_widget.dart
import 'package:flutter/material.dart';
import 'package:flutter_modular/flutter_modular.dart';
import 'package:core/core.dart';

class AppWidget extends StatelessWidget {
  const AppWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Modular App',
      theme: ThemeData(
        primaryColor: AppColors.primary,
        colorScheme: ColorScheme.fromSeed(seedColor: AppColors.primary),
        useMaterial3: true,
      ),
      routerConfig: Modular.routerConfig,
    );
  }
}
```

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_modular/flutter_modular.dart';
import 'app/app_module.dart';
import 'app/app_widget.dart';

void main() {
  runApp(
    ModularApp(
      module: AppModule(),
      child: const AppWidget(),
    ),
  );
}
```

### 5. Comunicación Entre Módulos

#### Event Bus para Comunicación Desacoplada

```dart
// packages/core/lib/events/app_events.dart
import 'dart:async';

class AppEventBus {
  static final AppEventBus _instance = AppEventBus._internal();
  factory AppEventBus() => _instance;
  AppEventBus._internal();

  final _streamController = StreamController<AppEvent>.broadcast();

  Stream<T> on<T extends AppEvent>() {
    return _streamController.stream.where((event) => event is T).cast<T>();
  }

  void fire(AppEvent event) {
    _streamController.add(event);
  }

  void dispose() {
    _streamController.close();
  }
}

// Base class para eventos
abstract class AppEvent {}

// Eventos específicos
class UserLoggedInEvent extends AppEvent {
  final String userId;
  final String email;

  UserLoggedInEvent({required this.userId, required this.email});
}

class UserLoggedOutEvent extends AppEvent {}

class ProductAddedToCartEvent extends AppEvent {
  final String productId;
  final int quantity;

  ProductAddedToCartEvent({
    required this.productId,
    required this.quantity,
  });
}

class OrderCompletedEvent extends AppEvent {
  final String orderId;
  final double total;

  OrderCompletedEvent({required this.orderId, required this.total});
}
```

#### Uso del Event Bus

```dart
// En Auth Module - Emitir evento
class LoginCubit extends Cubit<LoginState> {
  final LoginUseCase loginUseCase;
  final AppEventBus eventBus;

  LoginCubit({
    required this.loginUseCase,
    required this.eventBus,
  }) : super(const LoginState.initial());

  Future<void> login(String email, String password) async {
    emit(const LoginState.loading());

    final result = await loginUseCase(email: email, password: password);

    result.fold(
      (failure) => emit(LoginState.error(failure.message)),
      (user) {
        emit(const LoginState.success());

        // Emitir evento de login exitoso
        eventBus.fire(UserLoggedInEvent(
          userId: user.id,
          email: user.email,
        ));
      },
    );
  }
}

// En Cart Module - Escuchar evento
class CartBloc extends Bloc<CartEvent, CartState> {
  final AppEventBus eventBus;
  StreamSubscription? _userLoggedOutSubscription;

  CartBloc({required this.eventBus}) : super(const CartState.empty()) {
    // Escuchar evento de logout
    _userLoggedOutSubscription = eventBus.on<UserLoggedOutEvent>().listen(
      (_) => add(const CartEvent.clear()),
    );
  }

  @override
  Future<void> close() {
    _userLoggedOutSubscription?.cancel();
    return super.close();
  }
}
```

### 6. Testing de Módulos

```dart
// packages/auth_module/test/src/auth_module_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_modular/flutter_modular.dart';
import 'package:mocktail/mocktail.dart';
import 'package:auth_module/auth_module.dart';
import 'package:core/core.dart';

class MockDioClient extends Mock implements DioClient {}

void main() {
  setUpAll(() {
    Modular.bindModule(AuthModule());
    Modular.replaceInstance<DioClient>(MockDioClient());
  });

  tearDownAll(() {
    Modular.destroy();
  });

  group('AuthModule', () {
    test('should have all required binds', () {
      // Verificar que todos los binds estén registrados
      expect(Modular.get<AuthRepository>(), isA<AuthRepository>());
      expect(Modular.get<LoginUseCase>(), isA<LoginUseCase>());
      expect(Modular.get<AuthBloc>(), isA<AuthBloc>());
    });

    test('should navigate to login screen', () {
      final route = Modular.to.path;
      expect(route, equals('/auth/'));
    });
  });
}
```

### 7. Scripts de Melos para Monorepo

```bash
# Instalar melos globalmente
dart pub global activate melos

# Bootstrap: instalar dependencias de todos los paquetes
melos bootstrap

# Ejecutar tests en todos los módulos
melos run test

# Analizar código en todos los módulos
melos run analyze

# Formatear código en todos los módulos
melos run format

# Limpiar todos los módulos
melos run clean

# Ejecutar comando personalizado en un módulo específico
melos exec --scope=auth_module -- flutter test

# Ejecutar comando en todos los módulos excepto uno
melos exec --ignore=core -- flutter test

# Ver dependencias entre módulos
melos list --graph
```

## 🎯 Mejores Prácticas

### 1. Principio de Responsabilidad Única

✅ **DO:**
```
Cada módulo tiene una responsabilidad clara:
- auth_module: Solo autenticación
- products_module: Solo productos
- cart_module: Solo carrito
```

❌ **DON'T:**
```
- auth_module: Autenticación + Productos + Carrito
```

### 2. Dependencias Unidireccionales

✅ **DO:**
```
Feature Module → Core Module
(auth_module depende de core)
```

❌ **DON'T:**
```
Feature Module ← → Feature Module
(auth_module y products_module se dependen mutuamente)
```

### 3. Comunicación a través de Event Bus

✅ **DO:**
```dart
// AuthModule emite evento
eventBus.fire(UserLoggedInEvent(...));

// CartModule escucha evento
eventBus.on<UserLoggedInEvent>().listen(...);
```

❌ **DON'T:**
```dart
// No accedas directamente a otros módulos
final cartBloc = Modular.get<CartBloc>();  // ❌ Acoplamiento
cartBloc.clearCart();
```

### 4. Versionado de Módulos

✅ **DO:**
```yaml
# pubspec.yaml del módulo
version: 1.2.0  # Semantic versioning

# CHANGELOG.md del módulo
## [1.2.0] - 2025-12-17
### Added
- Nueva feature de recuperación de contraseña
```

### 5. Exportar Solo lo Necesario

✅ **DO:**
```dart
// packages/auth_module/lib/auth_module.dart
export 'src/auth_module.dart';
export 'src/domain/entities/user.dart';  // Solo entidades públicas

// No exportar implementaciones internas
```

❌ **DON'T:**
```dart
// No exportar todo
export 'src/data/datasources/auth_remote_datasource.dart';  // ❌ Implementación interna
export 'src/data/repositories/auth_repository_impl.dart';  // ❌ Implementación interna
```

### 6. Testing Independiente

✅ **DO:**
```dart
// Cada módulo tiene sus propios tests
packages/
  auth_module/
    test/
      unit/
      widget/
      integration/
```

## 📚 Recursos Adicionales

- [Flutter Modular Documentation](https://pub.dev/packages/flutter_modular)
- [Melos - Monorepo Management](https://melos.invertase.dev/)
- [Modular Architecture Best Practices](https://blog.flutterando.com.br/flutter-modular/)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md) - Arquitectura de cada módulo
- [Feature-First Architecture](../feature-first/SKILL.md) - Organización alternativa
- [Testing Strategy](../testing/SKILL.md) - Testing de módulos

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
