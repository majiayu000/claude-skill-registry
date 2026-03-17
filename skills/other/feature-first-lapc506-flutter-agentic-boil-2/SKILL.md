# 🎨 Skill: Feature-First Architecture

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-feature-first` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `feature-first`, `feature-architecture`, `feature-driven` |
| **Referencia** | [Feature-First Architecture Guide](https://codewithandrea.com/articles/flutter-project-structure/) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `feature-first`
- `feature-architecture`
- `feature-driven`
- `@skill:feature-first`

### Ejemplos de Prompts

```
Crea una app con feature-first architecture
```

```
Organiza el proyecto con estructura feature-first
```

```
@skill:feature-first - Estructura la app por features
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Feature-First Architecture organiza el código por features en lugar de por capas técnicas. Cada feature contiene todo lo necesario (UI, lógica, datos) en una carpeta auto-contenida, facilitando la navegación y el mantenimiento del código.

### ✅ Cuándo Usar Este Skill

- Proyectos medianos a grandes con múltiples features
- Equipos que trabajan en features específicas
- Necesitas navegación rápida en el código
- Quieres features auto-contenidas y cohesivas
- Prefieres organización por dominio de negocio
- Necesitas escalar la app agregando features
- Quieres reducir conflictos de merge en el equipo

### ❌ Cuándo NO Usar Este Skill

- Proyectos muy pequeños (1-2 pantallas)
- Aplicaciones con pocas features
- Prefieres organización por capas técnicas (Data/Domain/Presentation)

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── constants/
│   │   ├── app_constants.dart
│   │   └── api_endpoints.dart
│   ├── theme/
│   │   ├── app_theme.dart
│   │   ├── app_colors.dart
│   │   └── app_text_styles.dart
│   ├── widgets/
│   │   ├── buttons/
│   │   │   ├── primary_button.dart
│   │   │   └── secondary_button.dart
│   │   ├── inputs/
│   │   │   ├── text_field.dart
│   │   │   └── search_field.dart
│   │   └── loading/
│   │       └── loading_indicator.dart
│   ├── router/
│   │   ├── app_router.dart
│   │   └── routes.dart
│   ├── services/
│   │   ├── api_service.dart
│   │   ├── storage_service.dart
│   │   └── analytics_service.dart
│   ├── utils/
│   │   ├── validators.dart
│   │   ├── formatters.dart
│   │   └── extensions/
│   │       ├── string_extensions.dart
│   │       ├── date_extensions.dart
│   │       └── context_extensions.dart
│   └── error/
│       ├── failures.dart
│       └── exceptions.dart
│
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   ├── auth_local_datasource.dart
│   │   │   │   └── auth_remote_datasource.dart
│   │   │   ├── models/
│   │   │   │   ├── user_model.dart
│   │   │   │   └── token_model.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   │       ├── login_usecase.dart
│   │   │       ├── register_usecase.dart
│   │   │       ├── logout_usecase.dart
│   │   │       └── get_user_usecase.dart
│   │   ├── presentation/
│   │   │   ├── bloc/
│   │   │   │   ├── auth_bloc.dart
│   │   │   │   ├── auth_event.dart
│   │   │   │   ├── auth_state.dart
│   │   │   │   └── login/
│   │   │   │       ├── login_cubit.dart
│   │   │   │       └── login_state.dart
│   │   │   ├── screens/
│   │   │   │   ├── login_screen.dart
│   │   │   │   ├── register_screen.dart
│   │   │   │   └── forgot_password_screen.dart
│   │   │   └── widgets/
│   │   │       ├── login_form.dart
│   │   │       ├── register_form.dart
│   │   │       └── social_login_buttons.dart
│   │   └── authentication.dart  // Barrel file
│   │
│   ├── products/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   ├── products_local_datasource.dart
│   │   │   │   └── products_remote_datasource.dart
│   │   │   ├── models/
│   │   │   │   ├── product_model.dart
│   │   │   │   └── category_model.dart
│   │   │   └── repositories/
│   │   │       └── products_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── product.dart
│   │   │   │   └── category.dart
│   │   │   ├── repositories/
│   │   │   │   └── products_repository.dart
│   │   │   └── usecases/
│   │   │       ├── get_products_usecase.dart
│   │   │       ├── get_product_detail_usecase.dart
│   │   │       ├── search_products_usecase.dart
│   │   │       └── filter_products_usecase.dart
│   │   ├── presentation/
│   │   │   ├── bloc/
│   │   │   │   ├── products_bloc.dart
│   │   │   │   ├── products_event.dart
│   │   │   │   ├── products_state.dart
│   │   │   │   └── product_detail/
│   │   │   │       ├── product_detail_cubit.dart
│   │   │   │       └── product_detail_state.dart
│   │   │   ├── screens/
│   │   │   │   ├── products_screen.dart
│   │   │   │   ├── product_detail_screen.dart
│   │   │   │   └── search_screen.dart
│   │   │   └── widgets/
│   │   │       ├── product_card.dart
│   │   │       ├── product_grid.dart
│   │   │       ├── category_filter.dart
│   │   │       └── price_filter.dart
│   │   └── products.dart  // Barrel file
│   │
│   ├── cart/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   └── cart_local_datasource.dart
│   │   │   ├── models/
│   │   │   │   └── cart_item_model.dart
│   │   │   └── repositories/
│   │   │       └── cart_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── cart_item.dart
│   │   │   ├── repositories/
│   │   │   │   └── cart_repository.dart
│   │   │   └── usecases/
│   │   │       ├── add_to_cart_usecase.dart
│   │   │       ├── remove_from_cart_usecase.dart
│   │   │       ├── update_quantity_usecase.dart
│   │   │       └── get_cart_items_usecase.dart
│   │   ├── presentation/
│   │   │   ├── bloc/
│   │   │   │   ├── cart_bloc.dart
│   │   │   │   ├── cart_event.dart
│   │   │   │   └── cart_state.dart
│   │   │   ├── screens/
│   │   │   │   └── cart_screen.dart
│   │   │   └── widgets/
│   │   │       ├── cart_item_card.dart
│   │   │       ├── cart_summary.dart
│   │   │       └── empty_cart.dart
│   │   └── cart.dart  // Barrel file
│   │
│   ├── orders/
│   │   ├── data/
│   │   ├── domain/
│   │   ├── presentation/
│   │   └── orders.dart
│   │
│   ├── profile/
│   │   ├── data/
│   │   ├── domain/
│   │   ├── presentation/
│   │   └── profile.dart
│   │
│   └── settings/
│       ├── data/
│       ├── domain/
│       ├── presentation/
│       └── settings.dart
│
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  flutter_bloc: ^8.1.3
  equatable: ^2.0.5
  
  # Navigation
  go_router: ^12.1.3
  
  # Dependency Injection
  get_it: ^7.6.4
  injectable: ^2.3.2
  
  # Networking
  dio: ^5.4.0
  retrofit: ^4.0.3
  
  # Local Storage
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # Utils
  dartz: ^0.10.1
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1

dev_dependencies:
  # Code Generation
  build_runner: ^2.4.6
  freezed: ^2.4.5
  json_serializable: ^6.7.1
  injectable_generator: ^2.4.1
  retrofit_generator: ^8.0.6
  hive_generator: ^2.0.1
  
  # Testing
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.4
  mocktail: ^1.0.1
```

## 💻 Implementación

### 1. Core - Configuración de Router

```dart
// lib/core/router/app_router.dart
import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';
import '../../features/authentication/authentication.dart';
import '../../features/products/products.dart';
import '../../features/cart/cart.dart';
import '../../features/orders/orders.dart';
import '../../features/profile/profile.dart';

final appRouter = GoRouter(
  initialLocation: '/login',
  routes: [
    // Authentication Routes
    GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/register',
      name: 'register',
      builder: (context, state) => const RegisterScreen(),
    ),
    
    // Main App with Bottom Navigation
    ShellRoute(
      builder: (context, state, child) {
        return MainScaffold(child: child);
      },
      routes: [
        // Products Routes
        GoRoute(
          path: '/products',
          name: 'products',
          builder: (context, state) => const ProductsScreen(),
          routes: [
            GoRoute(
              path: ':id',
              name: 'product-detail',
              builder: (context, state) {
                final productId = state.pathParameters['id']!;
                return ProductDetailScreen(productId: productId);
              },
            ),
          ],
        ),
        
        // Cart Routes
        GoRoute(
          path: '/cart',
          name: 'cart',
          builder: (context, state) => const CartScreen(),
        ),
        
        // Orders Routes
        GoRoute(
          path: '/orders',
          name: 'orders',
          builder: (context, state) => const OrdersScreen(),
          routes: [
            GoRoute(
              path: ':id',
              name: 'order-detail',
              builder: (context, state) {
                final orderId = state.pathParameters['id']!;
                return OrderDetailScreen(orderId: orderId);
              },
            ),
          ],
        ),
        
        // Profile Routes
        GoRoute(
          path: '/profile',
          name: 'profile',
          builder: (context, state) => const ProfileScreen(),
        ),
      ],
    ),
  ],
  redirect: (context, state) {
    // Implementar lógica de autenticación aquí
    // final isAuthenticated = ...
    // if (!isAuthenticated && state.location != '/login') {
    //   return '/login';
    // }
    return null;
  },
);
```

### 2. Dependency Injection

```dart
// lib/core/di/injection.dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';
import 'injection.config.dart';

final getIt = GetIt.instance;

@InjectableInit()
Future<void> configureDependencies() async {
  await getIt.init();
}
```

```dart
// lib/core/di/injection.config.dart (generado)
// Ejecutar desde la raíz del proyecto:
// cd mobile && dart run build_runner build --delete-conflicting-outputs && cd ..
```

### 3. Feature: Authentication

#### Domain Layer

```dart
// lib/features/authentication/domain/entities/user.dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final String? avatar;

  const User({
    required this.id,
    required this.email,
    required this.name,
    this.avatar,
  });

  @override
  List<Object?> get props => [id, email, name, avatar];
}
```

```dart
// lib/features/authentication/domain/repositories/auth_repository.dart
import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user.dart';

abstract class AuthRepository {
  Future<Either<Failure, User>> login({
    required String email,
    required String password,
  });
  
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    required String name,
  });
  
  Future<Either<Failure, void>> logout();
  
  Future<Either<Failure, User>> getCurrentUser();
}
```

```dart
// lib/features/authentication/domain/usecases/login_usecase.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../../../../core/error/failures.dart';
import '../entities/user.dart';
import '../repositories/auth_repository.dart';

@injectable
class LoginUseCase {
  final AuthRepository repository;

  LoginUseCase(this.repository);

  Future<Either<Failure, User>> call({
    required String email,
    required String password,
  }) async {
    return await repository.login(email: email, password: password);
  }
}
```

#### Data Layer

```dart
// lib/features/authentication/data/models/user_model.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/user.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
class UserModel with _$UserModel {
  const UserModel._();
  
  const factory UserModel({
    required String id,
    required String email,
    required String name,
    String? avatar,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);

  // Convert to domain entity
  User toEntity() {
    return User(
      id: id,
      email: email,
      name: name,
      avatar: avatar,
    );
  }

  // Convert from domain entity
  factory UserModel.fromEntity(User user) {
    return UserModel(
      id: user.id,
      email: user.email,
      name: user.name,
      avatar: user.avatar,
    );
  }
}
```

```dart
// lib/features/authentication/data/datasources/auth_remote_datasource.dart
import 'package:dio/dio.dart';
import 'package:injectable/injectable.dart';
import '../models/user_model.dart';

abstract class AuthRemoteDataSource {
  Future<UserModel> login({required String email, required String password});
  Future<UserModel> register({required String email, required String password, required String name});
  Future<void> logout();
  Future<UserModel> getCurrentUser();
}

@LazySingleton(as: AuthRemoteDataSource)
class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio dio;

  AuthRemoteDataSourceImpl(this.dio);

  @override
  Future<UserModel> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      return UserModel.fromJson(response.data['user']);
    } catch (e) {
      throw Exception('Login failed: $e');
    }
  }

  @override
  Future<UserModel> register({
    required String email,
    required String password,
    required String name,
  }) async {
    try {
      final response = await dio.post(
        '/auth/register',
        data: {
          'email': email,
          'password': password,
          'name': name,
        },
      );

      return UserModel.fromJson(response.data['user']);
    } catch (e) {
      throw Exception('Registration failed: $e');
    }
  }

  @override
  Future<void> logout() async {
    try {
      await dio.post('/auth/logout');
    } catch (e) {
      throw Exception('Logout failed: $e');
    }
  }

  @override
  Future<UserModel> getCurrentUser() async {
    try {
      final response = await dio.get('/auth/user');
      return UserModel.fromJson(response.data['user']);
    } catch (e) {
      throw Exception('Get current user failed: $e');
    }
  }
}
```

```dart
// lib/features/authentication/data/repositories/auth_repository_impl.dart
import 'package:dartz/dartz.dart';
import 'package:injectable/injectable.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_datasource.dart';

@LazySingleton(as: AuthRepository)
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;

  AuthRepositoryImpl(this.remoteDataSource);

  @override
  Future<Either<Failure, User>> login({
    required String email,
    required String password,
  }) async {
    try {
      final userModel = await remoteDataSource.login(
        email: email,
        password: password,
      );
      return Right(userModel.toEntity());
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    required String name,
  }) async {
    try {
      final userModel = await remoteDataSource.register(
        email: email,
        password: password,
        name: name,
      );
      return Right(userModel.toEntity());
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      await remoteDataSource.logout();
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> getCurrentUser() async {
    try {
      final userModel = await remoteDataSource.getCurrentUser();
      return Right(userModel.toEntity());
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
```

#### Presentation Layer

```dart
// lib/features/authentication/presentation/bloc/login/login_cubit.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:injectable/injectable.dart';
import '../../../domain/usecases/login_usecase.dart';

part 'login_state.dart';
part 'login_cubit.freezed.dart';

@injectable
class LoginCubit extends Cubit<LoginState> {
  final LoginUseCase loginUseCase;

  LoginCubit(this.loginUseCase) : super(const LoginState.initial());

  Future<void> login({
    required String email,
    required String password,
  }) async {
    emit(const LoginState.loading());

    final result = await loginUseCase(email: email, password: password);

    result.fold(
      (failure) => emit(LoginState.error(failure.message)),
      (user) => emit(LoginState.success(user)),
    );
  }
}
```

```dart
// lib/features/authentication/presentation/bloc/login/login_state.dart
part of 'login_cubit.dart';

@freezed
class LoginState with _$LoginState {
  const factory LoginState.initial() = LoginInitial;
  const factory LoginState.loading() = LoginLoading;
  const factory LoginState.success(User user) = LoginSuccess;
  const factory LoginState.error(String message) = LoginError;
}
```

```dart
// lib/features/authentication/presentation/screens/login_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/di/injection.dart';
import '../../../../core/widgets/buttons/primary_button.dart';
import '../../../../core/theme/app_colors.dart';
import '../bloc/login/login_cubit.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => getIt<LoginCubit>(),
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Login'),
        ),
        body: BlocConsumer<LoginCubit, LoginState>(
          listener: (context, state) {
            state.maybeWhen(
              success: (user) {
                context.go('/products');
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
          builder: (context, state) {
            final isLoading = state is LoginLoading;

            return Padding(
              padding: const EdgeInsets.all(24.0),
              child: Form(
                key: _formKey,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    TextFormField(
                      controller: _emailController,
                      decoration: const InputDecoration(
                        labelText: 'Email',
                        prefixIcon: Icon(Icons.email),
                      ),
                      keyboardType: TextInputType.emailAddress,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your email';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _passwordController,
                      decoration: const InputDecoration(
                        labelText: 'Password',
                        prefixIcon: Icon(Icons.lock),
                      ),
                      obscureText: true,
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter your password';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: PrimaryButton(
                        text: 'Login',
                        isLoading: isLoading,
                        onPressed: () {
                          if (_formKey.currentState!.validate()) {
                            context.read<LoginCubit>().login(
                                  email: _emailController.text,
                                  password: _passwordController.text,
                                );
                          }
                        },
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextButton(
                      onPressed: () => context.push('/register'),
                      child: const Text('Don\'t have an account? Register'),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
```

#### Barrel File

```dart
// lib/features/authentication/authentication.dart
// Domain
export 'domain/entities/user.dart';
export 'domain/repositories/auth_repository.dart';
export 'domain/usecases/login_usecase.dart';
export 'domain/usecases/register_usecase.dart';
export 'domain/usecases/logout_usecase.dart';
export 'domain/usecases/get_user_usecase.dart';

// Presentation
export 'presentation/screens/login_screen.dart';
export 'presentation/screens/register_screen.dart';
export 'presentation/bloc/auth_bloc.dart';
export 'presentation/bloc/login/login_cubit.dart';
```

### 4. Main Setup

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'core/di/injection.dart';
import 'core/router/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Configure dependency injection
  await configureDependencies();
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Feature-First App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      routerConfig: appRouter,
    );
  }
}
```

## 🎯 Mejores Prácticas

### 1. Organización por Feature

✅ **DO:**
```
features/
  authentication/
    data/
    domain/
    presentation/
    authentication.dart
```

❌ **DON'T:**
```
data/
  authentication/
domain/
  authentication/
presentation/
  authentication/
```

### 2. Barrel Files

✅ **DO:**
```dart
// lib/features/products/products.dart
export 'domain/entities/product.dart';
export 'presentation/screens/products_screen.dart';
// Solo exporta APIs públicas
```

❌ **DON'T:**
```dart
// No expongas implementaciones internas
export 'data/datasources/products_remote_datasource.dart';  // ❌
export 'data/models/product_model.dart';  // ❌
```

### 3. Dependencias entre Features

✅ **DO:**
```dart
// Usa core para comunicación entre features
import 'package:app/core/services/event_bus.dart';

// O pasa datos a través de navigation
context.push('/cart', extra: product);
```

❌ **DON'T:**
```dart
// No importes directamente desde otras features
import '../../products/domain/entities/product.dart';  // ❌
```

### 4. Testing por Feature

✅ **DO:**
```
features/
  authentication/
    test/
      unit/
      widget/
      integration/
```

## 📚 Recursos Adicionales

- [Flutter Project Structure by Andrea](https://codewithandrea.com/articles/flutter-project-structure/)
- [Feature-First Architecture](https://www.youtube.com/watch?v=z8NO_DpcfBM)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md) - Arquitectura de cada feature
- [Modular Architecture](../modular-architecture/SKILL.md) - Alternativa modular
- [Testing Strategy](../testing/SKILL.md) - Testing de features

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025

