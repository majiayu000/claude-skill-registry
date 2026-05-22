---
name: "Clean Architecture Patterns"
description: "Domain, Data, and Presentation layer separation with dependency inversion and use case patterns"
version: "1.0.0"
---

# Clean Architecture Patterns

## Layer Structure

```
┌─────────────────────────────────────┐
│      PRESENTATION LAYER             │
│  (Controllers, Widgets, Bindings)   │
├─────────────────────────────────────┤
│         DOMAIN LAYER                │
│  (Entities, Use Cases, Interfaces)  │
├─────────────────────────────────────┤
│          DATA LAYER                 │
│  (Models, Repositories, Sources)    │
└─────────────────────────────────────┘
```

**Dependency Rule**: Outer layers depend on inner layers, NEVER reverse.

## Domain Layer (Pure Business Logic)

### Entities
```dart
// lib/domain/entities/user.dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String name;
  final String email;
  
  const User({
    required this.id,
    required this.name,
    required this.email,
  });
  
  @override
  List<Object?> get props => [id, name, email];
}
```

### Repository Interfaces
```dart
// lib/domain/repositories/user_repository.dart
import 'package:dartz/dartz.dart';
import '../../core/errors/failures.dart';
import '../entities/user.dart';

abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
  Future<Either<Failure, List<User>>> getAllUsers();
  Future<Either<Failure, User>> createUser(User user);
}
```

### Use Cases
```dart
// lib/domain/usecases/get_user.dart
import 'package:dartz/dartz.dart';
import '../../core/errors/failures.dart';
import '../entities/user.dart';
import '../repositories/user_repository.dart';

class GetUser {
  final UserRepository repository;
  
  GetUser(this.repository);
  
  Future<Either<Failure, User>> call(String id) {
    return repository.getUser(id);
  }
}
```

## Data Layer (Implementation Details)

### Models
```dart
// lib/data/models/user_model.dart
import '../../domain/entities/user.dart';

class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
  });
  
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }
  
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
  
  User toEntity() {
    return User(id: id, name: name, email: email);
  }
}
```

### Repository Implementation
```dart
// lib/data/repositories/user_repository_impl.dart
import 'package:dartz/dartz.dart';
import '../../core/errors/failures.dart';
import '../../core/errors/exceptions.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';
import '../providers/user_provider.dart';

class UserRepositoryImpl implements UserRepository {
  final UserProvider provider;
  
  UserRepositoryImpl(this.provider);
  
  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final model = await provider.fetchUser(id);
      return Right(model.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    }
  }
}
```

## Presentation Layer (UI & State Management)

### Controllers
```dart
// lib/presentation/controllers/user_controller.dart
import 'package:get/get.dart';
import '../../domain/usecases/get_user.dart';

class UserController extends GetxController {
  final GetUser getUserUseCase;
  
  UserController({required this.getUserUseCase});
  
  final _user = Rx<User?>(null);
  User? get user => _user.value;
  
  Future<void> loadUser(String id) async {
    final result = await getUserUseCase(id);
    result.fold(
      (failure) => Get.snackbar('Error', failure.message),
      (user) => _user.value = user,
    );
  }
}
```

## Dependency Inversion

```dart
// ❌ BAD: High-level module depends on low-level module
class UserController {
  final UserApiClient apiClient; // Concrete implementation
  
  void loadUser() {
    apiClient.fetchUser(); // Direct dependency on implementation
  }
}

// ✅ GOOD: Both depend on abstraction
class UserController {
  final UserRepository repository; // Abstract interface
  
  void loadUser() {
    repository.getUser(); // Depends on abstraction
  }
}
```
