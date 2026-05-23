---
name: "Repository Patterns"
description: "Repository interface and implementation patterns with offline-first strategies"
version: "1.0.0"
---

# Repository Patterns

## Repository Interface (Domain Layer)

```dart
// lib/domain/repositories/user_repository.dart
import 'package:dartz/dartz.dart';
import '../../core/errors/failures.dart';
import '../entities/user.dart';

abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
  Future<Either<Failure, List<User>>> getAllUsers();
  Future<Either<Failure, User>> createUser(User user);
  Future<Either<Failure, User>> updateUser(User user);
  Future<Either<Failure, void>> deleteUser(String id);
}
```

## Repository Implementation (Data Layer)

### Basic Implementation

```dart
// lib/data/repositories/user_repository_impl.dart
import 'package:dartz/dartz.dart';
import '../../core/errors/failures.dart';
import '../../core/errors/exceptions.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';
import '../providers/user_provider.dart';

class UserRepositoryImpl implements UserRepository {
  final UserProvider _provider;
  
  UserRepositoryImpl(this._provider);
  
  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final model = await _provider.fetchUser(id);
      return Right(model.toEntity());
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    } on NetworkException {
      return Left(NetworkFailure());
    } catch (e) {
      return Left(ServerFailure('Unexpected error: $e'));
    }
  }
}
```

### Offline-First Implementation

```dart
class UserRepositoryImpl implements UserRepository {
  final UserProvider _remoteSource;
  final UserLocalSource _localSource;
  final NetworkInfo _networkInfo;
  
  UserRepositoryImpl(
    this._remoteSource,
    this._localSource,
    this._networkInfo,
  );
  
  @override
  Future<Either<Failure, User>> getUser(String id) async {
    if (await _networkInfo.isConnected) {
      // Try remote first
      try {
        final model = await _remoteSource.fetchUser(id);
        // Cache for offline use
        await _localSource.cacheUser(model);
        return Right(model.toEntity());
      } on ServerException catch (e) {
        // Fallback to cache on server error
        return _getCachedUser(id);
      }
    } else {
      // Use cache when offline
      return _getCachedUser(id);
    }
  }
  
  Future<Either<Failure, User>> _getCachedUser(String id) async {
    try {
      final cached = await _localSource.getCachedUser(id);
      if (cached != null) {
        return Right(cached.toEntity());
      } else {
        return Left(CacheFailure('No cached data available'));
      }
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    }
  }
  
  @override
  Future<Either<Failure, List<User>>> getAllUsers() async {
    if (await _networkInfo.isConnected) {
      try {
        final models = await _remoteSource.fetchAllUsers();
        await _localSource.cacheUsers(models);
        return Right(models.map((m) => m.toEntity()).toList());
      } on ServerException {
        return _getCachedUsers();
      }
    } else {
      return _getCachedUsers();
    }
  }
  
  Future<Either<Failure, List<User>>> _getCachedUsers() async {
    try {
      final cached = await _localSource.getCachedUsers();
      if (cached != null && cached.isNotEmpty) {
        return Right(cached.map((m) => m.toEntity()).toList());
      } else {
        return Left(CacheFailure('No cached users'));
      }
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    }
  }
}
```

## Caching Strategies

### 1. Cache-First (Offline-First)
```dart
// Try cache first, then network
Future<Either<Failure, User>> getUser(String id) async {
  // Check cache first
  final cached = await _localSource.getCachedUser(id);
  if (cached != null) {
    // Return cached data immediately
    _refreshInBackground(id); // Update in background
    return Right(cached.toEntity());
  }
  
  // Cache miss - fetch from network
  return _fetchFromNetwork(id);
}
```

### 2. Network-First (Fresh Data Priority)
```dart
// Try network first, fallback to cache
Future<Either<Failure, User>> getUser(String id) async {
  if (await _networkInfo.isConnected) {
    try {
      final model = await _remoteSource.fetchUser(id);
      await _localSource.cacheUser(model);
      return Right(model.toEntity());
    } catch (e) {
      return _getCachedUser(id); // Fallback
    }
  } else {
    return _getCachedUser(id);
  }
}
```

### 3. Cache-Then-Network
```dart
// Return cache immediately, then update with network data
Stream<Either<Failure, User>> getUserStream(String id) async* {
  // Emit cached data first
  final cached = await _localSource.getCachedUser(id);
  if (cached != null) {
    yield Right(cached.toEntity());
  }
  
  // Then fetch from network
  if (await _networkInfo.isConnected) {
    try {
      final model = await _remoteSource.fetchUser(id);
      await _localSource.cacheUser(model);
      yield Right(model.toEntity());
    } on ServerException catch (e) {
      yield Left(ServerFailure(e.message));
    }
  }
}
```
