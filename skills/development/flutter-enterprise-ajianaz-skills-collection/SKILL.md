---
name: flutter-enterprise
description: "Lightweight Flutter enterprise development skill focused on feature-based clean architecture. Use when user asks to: (1) Build enterprise Flutter apps with clean architecture, (2) Implement feature-based modular structure, (3) Set up scalable Flutter project organization, (4) Create maintainable enterprise codebase. Triggers: Flutter enterprise app, clean architecture Flutter, feature-based Flutter, enterprise Flutter structure, modular Flutter architecture"
---

# Flutter Enterprise - Feature-Based Clean Architecture

Lightweight Flutter development skill for building enterprise applications using feature-based clean architecture patterns.

## Core Philosophy

**"Feature-first, testable, maintainable enterprise code"** - Focus on:

| Priority | Area | Purpose |
|----------|------|---------|
| 1 | Feature-Based Structure | Modular, scalable code organization |
| 2 | Clean Architecture | Separation of concerns and testability |
| 3 | Dependency Injection | Loose coupling and maintainability |
| 4 | Enterprise Patterns | Proven enterprise development practices |
| 5 | Code Generation | Boilerplate reduction and consistency |

## Development Workflow

Execute phases sequentially. Complete each before proceeding.

### Phase 1: Analyze Requirements

1. **Feature identification** - Identify distinct business features
2. **Data flow analysis** - Map data dependencies between features
3. **Integration points** - Define external service integrations
4. **Scalability requirements** - Plan for future feature additions

Output: Feature breakdown with dependency mapping.

### Phase 2: Design Feature Architecture

1. **Feature boundary definition** - Define clear feature boundaries
2. **Data layer planning** - Design repositories and data sources
3. **Domain modeling** - Create entities and use cases
4. **Presentation layer design** - Plan UI components and state management

Output: Feature architecture diagram and data contracts.

### Phase 3: Implement Core Structure

1. **Project setup** - Create feature-based directory structure
2. **Dependency injection** - Set up service locator or DI container
3. **Core utilities** - Create shared utilities and constants
4. **Navigation setup** - Implement routing structure

**Feature Structure Pattern:**
```
lib/
├── core/
│   ├── constants/
│   ├── errors/
│   ├── network/
│   ├── utils/
│   └── widgets/
├── features/
│   ├── feature_name/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── pages/
│   │       ├── widgets/
│   │       └── providers/
│   └── ...
└── main.dart
```

### Phase 4: Implement Feature Modules

1. **Data layer** - Implement repositories and data sources
2. **Domain layer** - Create business logic and use cases
3. **Presentation layer** - Build UI components and state management
4. **Feature integration** - Connect feature to main app

**Clean Architecture Implementation:**
```dart
// Domain Layer - Entity
class User {
  final String id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});
}

// Domain Layer - Repository (Abstract)
abstract class UserRepository {
  Future<List<User>> getUsers();
  Future<User> getUserById(String id);
}

// Domain Layer - Use Case
class GetUsersUseCase {
  final UserRepository repository;

  GetUsersUseCase(this.repository);

  Future<List<User>> call() async {
    return await repository.getUsers();
  }
}

// Data Layer - Repository Implementation
class UserRepositoryImpl implements UserRepository {
  final RemoteDataSource remoteDataSource;

  UserRepositoryImpl(this.remoteDataSource);

  @override
  Future<List<User>> getUsers() async {
    final userModels = await remoteDataSource.getUsers();
    return userModels.map((model) => model.toEntity()).toList();
  }
}
```

### Phase 5: Setup Testing Structure

1. **Unit tests** - Test domain layer and use cases
2. **Integration tests** - Test data layer and repositories
3. **Widget tests** - Test presentation layer components
4. **Test utilities** - Create mock objects and test helpers

## Quick Reference

### Feature-Based Architecture Patterns

| Layer | Responsibility | Key Components |
|-------|----------------|----------------|
| **Presentation** | UI and State Management | Pages, Widgets, Providers/Bloc |
| **Domain** | Business Logic | Entities, Use Cases, Repository Interfaces |
| **Data** | Data Implementation | Models, Data Sources, Repository Implementations |

### Dependency Injection Setup

```dart
// main.dart
void main() {
  // Initialize dependencies
  final serviceLocator = GetIt.instance;

  // Data sources
  serviceLocator.registerLazySingleton<RemoteDataSource>(
    () => RemoteDataSourceImpl(httpClient: serviceLocator()));

  // Repositories
  serviceLocator.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(serviceLocator()));

  // Use cases
  serviceLocator.registerFactory<GetUsersUseCase>(
    () => GetUsersUseCase(serviceLocator()));

  runApp(MyApp());
}
```

### State Management Patterns

This skill now supports **state management neutrality** with equivalent implementations for all four major approaches:

#### Provider Pattern
```dart
// Presentation Layer - Provider
class UserProvider extends ChangeNotifier {
  final GetUsersUseCase getUsersUseCase;

  List<User> _users = [];
  bool _isLoading = false;

  UserProvider({required this.getUsersUseCase});

  List<User> get users => _users;
  bool get isLoading => _isLoading;

  Future<void> loadUsers() async {
    _isLoading = true;
    notifyListeners();

    try {
      _users = await getUsersUseCase();
    } catch (e) {
      // Handle error
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
```

#### Bloc Pattern
```dart
// Presentation Layer - Bloc
abstract class UserEvent extends Equatable {}
class LoadUsers extends UserEvent {}

abstract class UserState extends Equatable {}
class UserLoading extends UserState {}
class UserLoaded extends UserState {
  final List<User> users;
  UserLoaded(this.users);
  @override
  List<Object> get props => [users];
}

class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUsersUseCase getUsersUseCase;

  UserBloc({required this.getUsersUseCase}) : super(UserInitial()) {
    on<LoadUsers>(_onLoadUsers);
  }

  Future<void> _onLoadUsers(LoadUsers event, Emitter<UserState> emit) async {
    emit(UserLoading());
    try {
      final users = await getUsersUseCase();
      emit(UserLoaded(users));
    } catch (e) {
      // Handle error
    }
  }
}
```

#### Riverpod Pattern
```dart
// Presentation Layer - Riverpod
class UserNotifier extends StateNotifier<AsyncValue<List<User>>> {
  final GetUsersUseCase getUsersUseCase;

  UserNotifier({required this.getUsersUseCase}) : super(const AsyncValue.loading());

  Future<void> loadUsers() async {
    state = const AsyncValue.loading();
    try {
      final users = await getUsersUseCase();
      state = AsyncValue.data(users);
    } catch (e, stackTrace) {
      state = AsyncValue.error(e, stackTrace);
    }
  }
}

final userProvider = StateNotifierProvider<UserNotifier, AsyncValue<List<User>>>((ref) {
  return UserNotifier(getUsersUseCase: ref.watch(getUsersUseCaseProvider));
});
```

#### GetX Pattern
```dart
// Presentation Layer - GetX
class UserController extends GetxController {
  final GetUsersUseCase getUsersUseCase;

  UserController({required this.getUsersUseCase});

  final RxList<User> _users = <User>[].obs;
  final RxBool _isLoading = false.obs;

  List<User> get users => _users;
  bool get isLoading => _isLoading.value;

  Future<void> loadUsers() async {
    _isLoading.value = true;
    try {
      final userList = await getUsersUseCase();
      _users.assignAll(userList);
    } catch (e) {
      // Handle error
    } finally {
      _isLoading.value = false;
    }
  }
}

// Page Example with GetX
class UserListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetBuilder<UserController>(
      init: UserController(getUsersUseCase: Get.find()),
      builder: (controller) {
        return Scaffold(
          appBar: AppBar(title: Text('Users')),
          body: Obx(() {
            if (controller.isLoading.value) {
              return Center(child: CircularProgressIndicator());
            }

            return ListView.builder(
              itemCount: controller.users.length,
              itemBuilder: (context, index) {
                final user = controller.users[index];
                return UserTile(user: user);
              },
            );
          }),
        );
      },
    );
  }
}
```

## Resources

- **Architecture patterns**: See `references/clean-architecture.md`
- **Feature templates**: See `references/feature-templates.md`
- **Testing patterns**: See `references/testing-patterns.md`
- **Code generation**: See `references/code-generation.md`

## Technical Stack

- **Architecture**: Clean Architecture with feature-based structure
- **State Management**: Provider/Bloc/Riverpod/GetX (state management neutral - all four approaches fully supported with equivalent examples)
- **Dependency Injection**: GetIt/Injectable
- **Code Generation**: build_runner, json_annotation, freezed
- **Testing**: mockito, bloc_test, widget testing

## Best Practices

- **Feature Independence**: Each feature should be self-contained
- **Dependency Rule**: Dependencies point inward (Presentation → Domain ← Data)
- **Interface Segregation**: Keep interfaces small and focused
- **Single Responsibility**: Each class has one reason to change
- **Test Coverage**: Aim for 80%+ coverage on domain and data layers

---

This Flutter enterprise skill transforms complex enterprise app development into a systematic process that ensures maintainable, scalable, and testable applications using feature-based clean architecture.