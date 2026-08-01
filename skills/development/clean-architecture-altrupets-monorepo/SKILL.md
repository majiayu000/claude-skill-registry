---
name: clean-architecture
description: '| ID | flutter-clean-architecture |'
---

# 🏛️ Skill: Clean Architecture

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-clean-architecture` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `clean`, `clean-arch`, `clean-architecture`, `bloc`, `usecase`, `repository`, `ddd` |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `clean`
- `clean-arch`
- `clean-architecture`
- `bloc`
- `usecase`
- `repository-pattern`
- `ddd` (Domain-Driven Design)
- `@skill:clean-architecture`

### Ejemplos de Prompts

```
Crea un módulo de autenticación usando clean-architecture
```

```
Implementa clean-arch para un sistema de e-commerce con bloc
```

```
@skill:clean-architecture - Genera feature de productos con repository-pattern
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Clean Architecture organiza el código en capas con dependencias unidireccionales, facilitando la independencia del framework, testabilidad y mantenibilidad a largo plazo. Ideal para aplicaciones enterprise y proyectos escalables.

### ✅ Cuándo Usar Este Skill

- Aplicaciones enterprise grandes y complejas
- Proyectos que requieren máxima testabilidad
- Equipos grandes con múltiples desarrolladores
- Necesitas independencia del framework
- Planeas mantener el proyecto por años
- Requieres múltiples fuentes de datos (API, caché, etc.)

### ❌ Cuándo NO Usar Este Skill

- Prototipos rápidos o MVPs
- Proyectos pequeños con lógica simple
- Equipos sin experiencia en arquitecturas complejas
- Deadlines muy ajustados

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── error/
│   │   ├── exceptions.dart          # Excepciones personalizadas
│   │   └── failures.dart            # Failures para manejo de errores
│   ├── usecases/
│   │   └── usecase.dart             # Clase base para UseCases
│   ├── network/
│   │   └── network_info.dart        # Verificación de conectividad
│   ├── utils/
│   │   ├── constants.dart
│   │   ├── validators.dart
│   │   └── input_converter.dart
│   └── theme/
│       └── app_theme.dart
│
├── features/
│   └── [feature_name]/              # ej: authentication, products
│       │
│       ├── data/                    # 💾 CAPA DE DATOS
│       │   ├── datasources/
│       │   │   ├── feature_remote_datasource.dart
│       │   │   └── feature_local_datasource.dart
│       │   ├── models/
│       │   │   └── feature_model.dart
│       │   └── repositories/
│       │       └── feature_repository_impl.dart
│       │
│       ├── domain/                  # 🎯 CAPA DE DOMINIO
│       │   ├── entities/
│       │   │   └── feature_entity.dart
│       │   ├── repositories/
│       │   │   └── feature_repository.dart
│       │   └── usecases/
│       │       ├── get_feature.dart
│       │       ├── create_feature.dart
│       │       ├── update_feature.dart
│       │       └── delete_feature.dart
│       │
│       └── presentation/            # 🎨 CAPA DE PRESENTACIÓN
│           ├── bloc/
│           │   ├── feature_bloc.dart
│           │   ├── feature_event.dart
│           │   └── feature_state.dart
│           ├── pages/
│           │   ├── feature_list_page.dart
│           │   └── feature_detail_page.dart
│           └── widgets/
│               ├── feature_card.dart
│               └── feature_form.dart
│
└── injection_container.dart         # 💉 Dependency Injection
```

## 🧩 Capas de la Arquitectura

### 1. Domain Layer (Capa de Dominio) 🎯

La capa más interna, contiene la lógica de negocio pura e independiente del framework.

#### Entities (Entidades)

```dart
// domain/entities/user_entity.dart
import 'package:equatable/equatable.dart';

class UserEntity extends Equatable {
  final String id;
  final String name;
  final String email;
  final String? avatar;
  final DateTime createdAt;

  const UserEntity({
    required this.id,
    required this.name,
    required this.email,
    this.avatar,
    required this.createdAt,
  });

  @override
  List<Object?> get props => [id, name, email, avatar, createdAt];
}
```

#### Repositories (Interfaces)

```dart
// domain/repositories/user_repository.dart
import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../entities/user_entity.dart';

abstract class UserRepository {
  Future<Either<Failure, UserEntity>> getUser(String id);
  Future<Either<Failure, List<UserEntity>>> getUsers();
  Future<Either<Failure, UserEntity>> createUser(UserEntity user);
  Future<Either<Failure, UserEntity>> updateUser(UserEntity user);
  Future<Either<Failure, void>> deleteUser(String id);
}
```

#### Use Cases (Casos de Uso)

```dart
// domain/usecases/get_user.dart
import 'package:dartz/dartz.dart';
import '../../core/error/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/user_entity.dart';
import '../repositories/user_repository.dart';

class GetUser implements UseCase<UserEntity, String> {
  final UserRepository repository;

  GetUser(this.repository);

  @override
  Future<Either<Failure, UserEntity>> call(String userId) async {
    return await repository.getUser(userId);
  }
}

// core/usecases/usecase.dart
import 'package:dartz/dartz.dart';
import '../error/failures.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams {}
```

### 2. Data Layer (Capa de Datos) 💾

Implementa las interfaces definidas en la capa de dominio.

#### Models

```dart
// data/models/user_model.dart
import '../../domain/entities/user_entity.dart';

class UserModel extends UserEntity {
  const UserModel({
    required String id,
    required String name,
    required String email,
    String? avatar,
    required DateTime createdAt,
  }) : super(
          id: id,
          name: name,
          email: email,
          avatar: avatar,
          createdAt: createdAt,
        );

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      avatar: json['avatar'],
      createdAt: DateTime.parse(json['createdAt']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'avatar': avatar,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  factory UserModel.fromEntity(UserEntity entity) {
    return UserModel(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      avatar: entity.avatar,
      createdAt: entity.createdAt,
    );
  }
}
```

#### Data Sources

```dart
// data/datasources/user_remote_datasource.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/error/exceptions.dart';
import '../models/user_model.dart';

abstract class UserRemoteDataSource {
  /// Calls the https://api.example.com/users/{id} endpoint.
  ///
  /// Throws a [ServerException] for all error codes.
  Future<UserModel> getUser(String id);
  Future<List<UserModel>> getUsers();
  Future<UserModel> createUser(UserModel user);
  Future<UserModel> updateUser(UserModel user);
  Future<void> deleteUser(String id);
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final http.Client client;
  final String baseUrl;

  UserRemoteDataSourceImpl({
    required this.client,
    required this.baseUrl,
  });

  @override
  Future<UserModel> getUser(String id) async {
    final response = await client.get(
      Uri.parse('$baseUrl/users/$id'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return UserModel.fromJson(json.decode(response.body));
    } else {
      throw ServerException();
    }
  }

  @override
  Future<List<UserModel>> getUsers() async {
    final response = await client.get(
      Uri.parse('$baseUrl/users'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = json.decode(response.body);
      return jsonList.map((json) => UserModel.fromJson(json)).toList();
    } else {
      throw ServerException();
    }
  }

  @override
  Future<UserModel> createUser(UserModel user) async {
    final response = await client.post(
      Uri.parse('$baseUrl/users'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(user.toJson()),
    );

    if (response.statusCode == 201) {
      return UserModel.fromJson(json.decode(response.body));
    } else {
      throw ServerException();
    }
  }

  @override
  Future<UserModel> updateUser(UserModel user) async {
    final response = await client.put(
      Uri.parse('$baseUrl/users/${user.id}'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(user.toJson()),
    );

    if (response.statusCode == 200) {
      return UserModel.fromJson(json.decode(response.body));
    } else {
      throw ServerException();
    }
  }

  @override
  Future<void> deleteUser(String id) async {
    final response = await client.delete(
      Uri.parse('$baseUrl/users/$id'),
    );

    if (response.statusCode != 204) {
      throw ServerException();
    }
  }
}

// data/datasources/user_local_datasource.dart
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../../core/error/exceptions.dart';
import '../models/user_model.dart';

abstract class UserLocalDataSource {
  Future<UserModel> getCachedUser(String id);
  Future<List<UserModel>> getCachedUsers();
  Future<void> cacheUser(UserModel user);
  Future<void> cacheUsers(List<UserModel> users);
}

class UserLocalDataSourceImpl implements UserLocalDataSource {
  final SharedPreferences sharedPreferences;

  static const CACHED_USER = 'CACHED_USER_';
  static const CACHED_USERS = 'CACHED_USERS';

  UserLocalDataSourceImpl({required this.sharedPreferences});

  @override
  Future<UserModel> getCachedUser(String id) {
    final jsonString = sharedPreferences.getString('$CACHED_USER$id');
    if (jsonString != null) {
      return Future.value(UserModel.fromJson(json.decode(jsonString)));
    } else {
      throw CacheException();
    }
  }

  @override
  Future<List<UserModel>> getCachedUsers() {
    final jsonString = sharedPreferences.getString(CACHED_USERS);
    if (jsonString != null) {
      final List<dynamic> jsonList = json.decode(jsonString);
      return Future.value(
        jsonList.map((json) => UserModel.fromJson(json)).toList(),
      );
    } else {
      throw CacheException();
    }
  }

  @override
  Future<void> cacheUser(UserModel user) {
    return sharedPreferences.setString(
      '$CACHED_USER${user.id}',
      json.encode(user.toJson()),
    );
  }

  @override
  Future<void> cacheUsers(List<UserModel> users) {
    return sharedPreferences.setString(
      CACHED_USERS,
      json.encode(users.map((user) => user.toJson()).toList()),
    );
  }
}
```

#### Repository Implementation

```dart
// data/repositories/user_repository_impl.dart
import 'package:dartz/dartz.dart';
import '../../core/error/exceptions.dart';
import '../../core/error/failures.dart';
import '../../core/network/network_info.dart';
import '../../domain/entities/user_entity.dart';
import '../../domain/repositories/user_repository.dart';
import '../datasources/user_local_datasource.dart';
import '../datasources/user_remote_datasource.dart';
import '../models/user_model.dart';

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  UserRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, UserEntity>> getUser(String id) async {
    if (await networkInfo.isConnected) {
      try {
        final user = await remoteDataSource.getUser(id);
        await localDataSource.cacheUser(user);
        return Right(user);
      } on ServerException {
        return Left(ServerFailure());
      }
    } else {
      try {
        final user = await localDataSource.getCachedUser(id);
        return Right(user);
      } on CacheException {
        return Left(CacheFailure());
      }
    }
  }

  @override
  Future<Either<Failure, List<UserEntity>>> getUsers() async {
    if (await networkInfo.isConnected) {
      try {
        final users = await remoteDataSource.getUsers();
        await localDataSource.cacheUsers(users);
        return Right(users);
      } on ServerException {
        return Left(ServerFailure());
      }
    } else {
      try {
        final users = await localDataSource.getCachedUsers();
        return Right(users);
      } on CacheException {
        return Left(CacheFailure());
      }
    }
  }

  @override
  Future<Either<Failure, UserEntity>> createUser(UserEntity user) async {
    if (await networkInfo.isConnected) {
      try {
        final userModel = UserModel.fromEntity(user);
        final createdUser = await remoteDataSource.createUser(userModel);
        return Right(createdUser);
      } on ServerException {
        return Left(ServerFailure());
      }
    } else {
      return Left(NetworkFailure());
    }
  }

  @override
  Future<Either<Failure, UserEntity>> updateUser(UserEntity user) async {
    if (await networkInfo.isConnected) {
      try {
        final userModel = UserModel.fromEntity(user);
        final updatedUser = await remoteDataSource.updateUser(userModel);
        await localDataSource.cacheUser(updatedUser);
        return Right(updatedUser);
      } on ServerException {
        return Left(ServerFailure());
      }
    } else {
      return Left(NetworkFailure());
    }
  }

  @override
  Future<Either<Failure, void>> deleteUser(String id) async {
    if (await networkInfo.isConnected) {
      try {
        await remoteDataSource.deleteUser(id);
        return const Right(null);
      } on ServerException {
        return Left(ServerFailure());
      }
    } else {
      return Left(NetworkFailure());
    }
  }
}
```

### 3. Presentation Layer (Capa de Presentación) 🎨

Maneja la UI y la gestión de estado usando BLoC.

#### BLoC Pattern

```dart
// presentation/bloc/user_event.dart
import 'package:equatable/equatable.dart';
import '../../domain/entities/user_entity.dart';

abstract class UserEvent extends Equatable {
  const UserEvent();

  @override
  List<Object?> get props => [];
}

class GetUsersEvent extends UserEvent {}

class GetUserEvent extends UserEvent {
  final String userId;

  const GetUserEvent(this.userId);

  @override
  List<Object> get props => [userId];
}

class CreateUserEvent extends UserEvent {
  final UserEntity user;

  const CreateUserEvent(this.user);

  @override
  List<Object> get props => [user];
}

class UpdateUserEvent extends UserEvent {
  final UserEntity user;

  const UpdateUserEvent(this.user);

  @override
  List<Object> get props => [user];
}

class DeleteUserEvent extends UserEvent {
  final String userId;

  const DeleteUserEvent(this.userId);

  @override
  List<Object> get props => [userId];
}

// presentation/bloc/user_state.dart
import 'package:equatable/equatable.dart';
import '../../domain/entities/user_entity.dart';

abstract class UserState extends Equatable {
  const UserState();

  @override
  List<Object?> get props => [];
}

class UserInitial extends UserState {}

class UserLoading extends UserState {}

class UsersLoaded extends UserState {
  final List<UserEntity> users;

  const UsersLoaded(this.users);

  @override
  List<Object> get props => [users];
}

class UserLoaded extends UserState {
  final UserEntity user;

  const UserLoaded(this.user);

  @override
  List<Object> get props => [user];
}

class UserOperationSuccess extends UserState {
  final String message;

  const UserOperationSuccess(this.message);

  @override
  List<Object> get props => [message];
}

class UserError extends UserState {
  final String message;

  const UserError(this.message);

  @override
  List<Object> get props => [message];
}

// presentation/bloc/user_bloc.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/usecases/get_user.dart';
import '../../domain/usecases/get_users.dart';
import '../../domain/usecases/create_user.dart';
import '../../domain/usecases/update_user.dart';
import '../../domain/usecases/delete_user.dart';
import 'user_event.dart';
import 'user_state.dart';

class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUser getUser;
  final GetUsers getUsers;
  final CreateUser createUser;
  final UpdateUser updateUser;
  final DeleteUser deleteUser;

  UserBloc({
    required this.getUser,
    required this.getUsers,
    required this.createUser,
    required this.updateUser,
    required this.deleteUser,
  }) : super(UserInitial()) {
    on<GetUsersEvent>(_onGetUsers);
    on<GetUserEvent>(_onGetUser);
    on<CreateUserEvent>(_onCreateUser);
    on<UpdateUserEvent>(_onUpdateUser);
    on<DeleteUserEvent>(_onDeleteUser);
  }

  Future<void> _onGetUsers(
    GetUsersEvent event,
    Emitter<UserState> emit,
  ) async {
    emit(UserLoading());

    final result = await getUsers(NoParams());

    result.fold(
      (failure) => emit(UserError(_mapFailureToMessage(failure))),
      (users) => emit(UsersLoaded(users)),
    );
  }

  Future<void> _onGetUser(
    GetUserEvent event,
    Emitter<UserState> emit,
  ) async {
    emit(UserLoading());

    final result = await getUser(event.userId);

    result.fold(
      (failure) => emit(UserError(_mapFailureToMessage(failure))),
      (user) => emit(UserLoaded(user)),
    );
  }

  Future<void> _onCreateUser(
    CreateUserEvent event,
    Emitter<UserState> emit,
  ) async {
    emit(UserLoading());

    final result = await createUser(event.user);

    result.fold(
      (failure) => emit(UserError(_mapFailureToMessage(failure))),
      (_) => emit(const UserOperationSuccess('Usuario creado exitosamente')),
    );
  }

  Future<void> _onUpdateUser(
    UpdateUserEvent event,
    Emitter<UserState> emit,
  ) async {
    emit(UserLoading());

    final result = await updateUser(event.user);

    result.fold(
      (failure) => emit(UserError(_mapFailureToMessage(failure))),
      (_) => emit(const UserOperationSuccess('Usuario actualizado exitosamente')),
    );
  }

  Future<void> _onDeleteUser(
    DeleteUserEvent event,
    Emitter<UserState> emit,
  ) async {
    emit(UserLoading());

    final result = await deleteUser(event.userId);

    result.fold(
      (failure) => emit(UserError(_mapFailureToMessage(failure))),
      (_) => emit(const UserOperationSuccess('Usuario eliminado exitosamente')),
    );
  }

  String _mapFailureToMessage(Failure failure) {
    switch (failure.runtimeType) {
      case ServerFailure:
        return 'Error del servidor. Por favor intenta de nuevo.';
      case CacheFailure:
        return 'Error al cargar datos locales.';
      case NetworkFailure:
        return 'Sin conexión a internet.';
      default:
        return 'Error inesperado. Por favor intenta de nuevo.';
    }
  }
}
```

#### Pages

```dart
// presentation/pages/user_list_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/user_bloc.dart';
import '../bloc/user_event.dart';
import '../bloc/user_state.dart';
import '../widgets/user_card.dart';

class UserListPage extends StatelessWidget {
  const UserListPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Usuarios'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              context.read<UserBloc>().add(GetUsersEvent());
            },
          ),
        ],
      ),
      body: BlocBuilder<UserBloc, UserState>(
        builder: (context, state) {
          if (state is UserInitial) {
            // Cargar usuarios al iniciar
            context.read<UserBloc>().add(GetUsersEvent());
            return const Center(child: CircularProgressIndicator());
          } else if (state is UserLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (state is UsersLoaded) {
            if (state.users.isEmpty) {
              return const Center(
                child: Text('No hay usuarios disponibles'),
              );
            }
            return ListView.builder(
              itemCount: state.users.length,
              itemBuilder: (context, index) {
                return UserCard(user: state.users[index]);
              },
            );
          } else if (state is UserError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(state.message),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      context.read<UserBloc>().add(GetUsersEvent());
                    },
                    child: const Text('Reintentar'),
                  ),
                ],
              ),
            );
          }
          return Container();
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Navegar a página de creación
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## 💉 Dependency Injection

```dart
// injection_container.dart
import 'package:get_it/get_it.dart';
import 'package:http/http.dart' as http;
import 'package:internet_connection_checker/internet_connection_checker.dart';
import 'package:shared_preferences/shared_preferences.dart';

final sl = GetIt.instance;

Future<void> init() async {
  //! Features - User
  // Bloc
  sl.registerFactory(
    () => UserBloc(
      getUser: sl(),
      getUsers: sl(),
      createUser: sl(),
      updateUser: sl(),
      deleteUser: sl(),
    ),
  );

  // Use cases
  sl.registerLazySingleton(() => GetUser(sl()));
  sl.registerLazySingleton(() => GetUsers(sl()));
  sl.registerLazySingleton(() => CreateUser(sl()));
  sl.registerLazySingleton(() => UpdateUser(sl()));
  sl.registerLazySingleton(() => DeleteUser(sl()));

  // Repository
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data sources
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(
      client: sl(),
      baseUrl: 'https://api.example.com',
    ),
  );

  sl.registerLazySingleton<UserLocalDataSource>(
    () => UserLocalDataSourceImpl(sharedPreferences: sl()),
  );

  //! Core
  sl.registerLazySingleton<NetworkInfo>(
    () => NetworkInfoImpl(sl()),
  );

  //! External
  final sharedPreferences = await SharedPreferences.getInstance();
  sl.registerLazySingleton(() => sharedPreferences);
  sl.registerLazySingleton(() => http.Client());
  sl.registerLazySingleton(() => InternetConnectionChecker());
}
```

## 📦 Dependencias Recomendadas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_bloc: ^8.1.3

  # Dependency Injection
  get_it: ^7.6.4

  # Functional Programming
  dartz: ^0.10.1

  # Remote
  http: ^1.1.0

  # Local Storage
  shared_preferences: ^2.2.2
  hive: ^2.2.3
  hive_flutter: ^1.1.0

  # Network
  internet_connection_checker: ^1.0.0+1

  # Utilities
  equatable: ^2.0.5

dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.4
  mocktail: ^1.0.1
  bloc_test: ^9.1.5
  hive_generator: ^2.0.1
  build_runner: ^2.4.6
```

## 📊 Flujo de Datos

```
┌──────────────┐
│     User     │
│  Interaction │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Presentation │
│    (BLoC)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Domain     │
│  (UseCase)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│     Data     │
│ (Repository) │
└──────┬───────┘
       │
       ├─────────────┬─────────────┐
       ▼             ▼             ▼
  ┌────────┐   ┌────────┐   ┌────────┐
  │ Remote │   │ Local  │   │Network │
  │  API   │   │ Cache  │   │  Info  │
  └────────┘   └────────┘   └────────┘
```

## 🧪 Testing

Ver documentación completa de testing en cada archivo del skill.

## ✅ Principios SOLID

1. **Single Responsibility:** Cada clase tiene una única responsabilidad
2. **Open/Closed:** Abierto para extensión, cerrado para modificación
3. **Liskov Substitution:** Las implementaciones pueden sustituir a las abstracciones
4. **Interface Segregation:** Interfaces específicas en lugar de generales
5. **Dependency Inversion:** Dependencia de abstracciones, no de implementaciones

## 📚 Recursos Adicionales

- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Flutter BLoC Documentation](https://bloclibrary.dev/)
- [GetIt Package](https://pub.dev/packages/get_it)
- [Dartz Package](https://pub.dev/packages/dartz)

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
