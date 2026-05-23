# 🎨 Skill: MVVM Pattern

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-mvvm-pattern` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `mvvm`, `model-view-viewmodel`, `provider`, `changenotifier` |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `mvvm`
- `model-view-viewmodel`
- `provider`
- `changenotifier`
- `@skill:mvvm`

### Ejemplos de Prompts

```
Crea una app de lista de tareas usando mvvm
```

```
Implementa model-view-viewmodel para un módulo de productos
```

```
@skill:mvvm - Genera una app de gestión de usuarios con provider
```

## 📖 Descripción

El patrón MVVM (Model-View-ViewModel) proporciona una separación clara entre la lógica de negocio y la interfaz de usuario, facilitando el testing, mantenimiento y escalabilidad del código.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Proyectos medianos con lógica de negocio moderada
- Necesitas separación clara entre UI y lógica
- Quieres testear la lógica de presentación fácilmente
- El equipo está familiarizado con reactive programming
- Necesitas gestión de estado reactiva

### ❌ Cuándo NO Usar Este Skill

- Proyectos muy pequeños (usa setState)
- Aplicaciones enterprise muy complejas (considera Clean Architecture)
- Necesitas máxima separación de capas (usa Clean Architecture)

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── constants/
│   │   ├── app_constants.dart
│   │   ├── api_constants.dart
│   │   └── string_constants.dart
│   ├── utils/
│   │   ├── validators.dart
│   │   ├── formatters.dart
│   │   └── helpers.dart
│   └── extensions/
│       ├── string_extensions.dart
│       ├── date_extensions.dart
│       └── context_extensions.dart
│
├── models/
│   ├── entities/
│   │   ├── user.dart
│   │   ├── product.dart
│   │   └── order.dart
│   └── dto/
│       ├── user_dto.dart
│       └── api_response.dart
│
├── views/
│   ├── screens/
│   │   ├── home_screen.dart
│   │   ├── detail_screen.dart
│   │   └── settings_screen.dart
│   ├── widgets/
│   │   ├── custom_button.dart
│   │   ├── custom_card.dart
│   │   └── loading_indicator.dart
│   └── dialogs/
│       ├── confirmation_dialog.dart
│       └── error_dialog.dart
│
├── viewmodels/
│   ├── home_viewmodel.dart
│   ├── detail_viewmodel.dart
│   └── providers/
│       └── app_provider.dart
│
├── services/
│   ├── api/
│   │   ├── api_service.dart
│   │   └── http_client.dart
│   ├── storage/
│   │   ├── local_storage.dart
│   │   └── secure_storage.dart
│   └── navigation/
│       └── navigation_service.dart
│
└── main.dart
```

## 🧩 Componentes Principales

### 1. Model (Modelo)

Representa los datos y la lógica de negocio.

```dart
// models/entities/user.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatar,
    DateTime? createdAt,
  }) = _User;
  
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

**Características:**
- Inmutabilidad usando `freezed`
- Serialización JSON automática
- CopyWith para actualizaciones
- Equality por valor

### 2. View (Vista)

Widgets de Flutter que representan la UI.

```dart
// views/screens/user_list_screen.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class UserListScreen extends StatelessWidget {
  const UserListScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Usuarios'),
      ),
      body: Consumer<UserViewModel>(
        builder: (context, viewModel, child) {
          // Estado de carga
          if (viewModel.isLoading) {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }
          
          // Estado de error
          if (viewModel.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(viewModel.error!),
                  ElevatedButton(
                    onPressed: viewModel.fetchUsers,
                    child: const Text('Reintentar'),
                  ),
                ],
              ),
            );
          }
          
          // Estado exitoso
          return ListView.builder(
            itemCount: viewModel.users.length,
            itemBuilder: (context, index) {
              final user = viewModel.users[index];
              return ListTile(
                leading: CircleAvatar(
                  backgroundImage: user.avatar != null
                      ? NetworkImage(user.avatar!)
                      : null,
                  child: user.avatar == null
                      ? Text(user.name[0])
                      : null,
                ),
                title: Text(user.name),
                subtitle: Text(user.email),
                onTap: () => _navigateToDetail(context, user),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _navigateToCreate(context),
        child: const Icon(Icons.add),
      ),
    );
  }
  
  void _navigateToDetail(BuildContext context, User user) {
    // Navegación al detalle
  }
  
  void _navigateToCreate(BuildContext context) {
    // Navegación a creación
  }
}
```

**Características:**
- Libre de lógica de negocio
- Observa cambios con `Consumer`
- Maneja múltiples estados (loading, error, success)
- Usa `Selector` para optimizar rebuilds

### 3. ViewModel

Maneja la lógica de presentación y gestiona el estado.

```dart
// viewmodels/user_viewmodel.dart
import 'package:flutter/foundation.dart';

class UserViewModel extends ChangeNotifier {
  final UserService _userService;
  
  UserViewModel(this._userService);
  
  // Estado
  List<User> _users = [];
  List<User> get users => List.unmodifiable(_users);
  
  bool _isLoading = false;
  bool get isLoading => _isLoading;
  
  String? _error;
  String? get error => _error;
  
  User? _selectedUser;
  User? get selectedUser => _selectedUser;
  
  // Acciones
  Future<void> fetchUsers() async {
    _setLoading(true);
    _clearError();
    
    try {
      _users = await _userService.getUsers();
      notifyListeners();
    } catch (e) {
      _setError('Error al cargar usuarios: ${e.toString()}');
    } finally {
      _setLoading(false);
    }
  }
  
  Future<void> createUser(User user) async {
    _setLoading(true);
    _clearError();
    
    try {
      final createdUser = await _userService.createUser(user);
      _users.add(createdUser);
      notifyListeners();
    } catch (e) {
      _setError('Error al crear usuario: ${e.toString()}');
    } finally {
      _setLoading(false);
    }
  }
  
  Future<void> updateUser(User user) async {
    _setLoading(true);
    _clearError();
    
    try {
      final updatedUser = await _userService.updateUser(user);
      final index = _users.indexWhere((u) => u.id == user.id);
      if (index != -1) {
        _users[index] = updatedUser;
        notifyListeners();
      }
    } catch (e) {
      _setError('Error al actualizar usuario: ${e.toString()}');
    } finally {
      _setLoading(false);
    }
  }
  
  Future<void> deleteUser(String userId) async {
    _setLoading(true);
    _clearError();
    
    try {
      await _userService.deleteUser(userId);
      _users.removeWhere((u) => u.id == userId);
      notifyListeners();
    } catch (e) {
      _setError('Error al eliminar usuario: ${e.toString()}');
    } finally {
      _setLoading(false);
    }
  }
  
  void selectUser(User user) {
    _selectedUser = user;
    notifyListeners();
  }
  
  void clearSelection() {
    _selectedUser = null;
    notifyListeners();
  }
  
  // Helpers privados
  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }
  
  void _setError(String message) {
    _error = message;
    notifyListeners();
  }
  
  void _clearError() {
    _error = null;
  }
  
  @override
  void dispose() {
    // Limpiar recursos si es necesario
    super.dispose();
  }
}
```

**Características:**
- Extiende `ChangeNotifier`
- Expone estado inmutable
- Maneja errores y loading
- Interactúa con servicios
- Limpia recursos en dispose

### 4. Service (Servicio)

```dart
// services/api/user_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class UserService {
  final http.Client _client;
  final String _baseUrl;
  
  UserService({
    required http.Client client,
    required String baseUrl,
  })  : _client = client,
        _baseUrl = baseUrl;
  
  Future<List<User>> getUsers() async {
    final response = await _client.get(
      Uri.parse('$_baseUrl/users'),
    );
    
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => User.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load users');
    }
  }
  
  Future<User> createUser(User user) async {
    final response = await _client.post(
      Uri.parse('$_baseUrl/users'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(user.toJson()),
    );
    
    if (response.statusCode == 201) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create user');
    }
  }
  
  Future<User> updateUser(User user) async {
    final response = await _client.put(
      Uri.parse('$_baseUrl/users/${user.id}'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(user.toJson()),
    );
    
    if (response.statusCode == 200) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to update user');
    }
  }
  
  Future<void> deleteUser(String userId) async {
    final response = await _client.delete(
      Uri.parse('$_baseUrl/users/$userId'),
    );
    
    if (response.statusCode != 204) {
      throw Exception('Failed to delete user');
    }
  }
}
```

## 📦 Dependencias Recomendadas

```yaml
name: my_mvvm_app
description: Flutter app with MVVM pattern
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.1.1
  
  # Immutability & Serialization
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  
  # Utilities
  equatable: ^2.0.5
  
  # HTTP
  http: ^1.1.0
  
  # Local Storage
  shared_preferences: ^2.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  
  # Code Generation
  build_runner: ^2.4.6
  freezed: ^2.4.5
  json_serializable: ^6.7.1
  
  # Testing
  mockito: ^5.4.4
  
  # Linting
  flutter_lints: ^3.0.1
```

## 📊 Flujo de Datos

```
┌─────────────┐
│    User     │
│ Interaction │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    View     │
│  (Widget)   │
└──────┬──────┘
       │ Consumer/Selector
       ▼
┌─────────────┐
│  ViewModel  │  ◄─── notifyListeners()
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Service   │
│  (API/DB)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Model    │
│   (Data)    │
└─────────────┘
```

## 🧪 Testing

### Test del ViewModel

```dart
// test/viewmodels/user_viewmodel_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

@GenerateMocks([UserService])
void main() {
  late UserViewModel viewModel;
  late MockUserService mockService;
  
  setUp(() {
    mockService = MockUserService();
    viewModel = UserViewModel(mockService);
  });
  
  tearDown(() {
    viewModel.dispose();
  });
  
  group('UserViewModel', () {
    test('initial state should be empty', () {
      expect(viewModel.users, isEmpty);
      expect(viewModel.isLoading, false);
      expect(viewModel.error, null);
    });
    
    test('fetchUsers should update users list when successful', () async {
      // Arrange
      final users = [
        User(id: '1', name: 'John', email: 'john@test.com'),
        User(id: '2', name: 'Jane', email: 'jane@test.com'),
      ];
      when(mockService.getUsers()).thenAnswer((_) async => users);
      
      // Act
      await viewModel.fetchUsers();
      
      // Assert
      expect(viewModel.users, users);
      expect(viewModel.isLoading, false);
      expect(viewModel.error, null);
      verify(mockService.getUsers()).called(1);
    });
    
    test('fetchUsers should set error when service fails', () async {
      // Arrange
      when(mockService.getUsers()).thenThrow(Exception('Network error'));
      
      // Act
      await viewModel.fetchUsers();
      
      // Assert
      expect(viewModel.users, isEmpty);
      expect(viewModel.isLoading, false);
      expect(viewModel.error, isNotNull);
      expect(viewModel.error, contains('Network error'));
    });
    
    test('createUser should add user to list', () async {
      // Arrange
      final newUser = User(id: '1', name: 'John', email: 'john@test.com');
      when(mockService.createUser(any)).thenAnswer((_) async => newUser);
      
      // Act
      await viewModel.createUser(newUser);
      
      // Assert
      expect(viewModel.users, contains(newUser));
      expect(viewModel.isLoading, false);
    });
  });
}
```

### Test de Widget

```dart
// test/widgets/user_list_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:mockito/mockito.dart';

void main() {
  late MockUserViewModel mockViewModel;
  
  setUp(() {
    mockViewModel = MockUserViewModel();
  });
  
  Widget createWidgetUnderTest() {
    return MaterialApp(
      home: ChangeNotifierProvider<UserViewModel>.value(
        value: mockViewModel,
        child: const UserListScreen(),
      ),
    );
  }
  
  testWidgets('should show loading indicator when loading', (tester) async {
    // Arrange
    when(mockViewModel.isLoading).thenReturn(true);
    when(mockViewModel.users).thenReturn([]);
    when(mockViewModel.error).thenReturn(null);
    
    // Act
    await tester.pumpWidget(createWidgetUnderTest());
    
    // Assert
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });
  
  testWidgets('should show user list when loaded', (tester) async {
    // Arrange
    final users = [
      User(id: '1', name: 'John', email: 'john@test.com'),
      User(id: '2', name: 'Jane', email: 'jane@test.com'),
    ];
    when(mockViewModel.isLoading).thenReturn(false);
    when(mockViewModel.users).thenReturn(users);
    when(mockViewModel.error).thenReturn(null);
    
    // Act
    await tester.pumpWidget(createWidgetUnderTest());
    
    // Assert
    expect(find.text('John'), findsOneWidget);
    expect(find.text('Jane'), findsOneWidget);
  });
  
  testWidgets('should show error message when error occurs', (tester) async {
    // Arrange
    when(mockViewModel.isLoading).thenReturn(false);
    when(mockViewModel.users).thenReturn([]);
    when(mockViewModel.error).thenReturn('Network error');
    
    // Act
    await tester.pumpWidget(createWidgetUnderTest());
    
    // Assert
    expect(find.text('Network error'), findsOneWidget);
    expect(find.text('Reintentar'), findsOneWidget);
  });
}
```

## ✅ Mejores Prácticas

### 1. Single Responsibility
Cada ViewModel debe manejar una única funcionalidad o pantalla.

### 2. Dependency Injection
Inyecta servicios a través del constructor del ViewModel.

```dart
// ❌ Malo
class UserViewModel extends ChangeNotifier {
  final service = UserService(); // Acoplamiento fuerte
}

// ✅ Bueno
class UserViewModel extends ChangeNotifier {
  final UserService _service;
  UserViewModel(this._service); // Inyección de dependencia
}
```

### 3. Error Handling Consistente
Maneja errores de forma uniforme en todos los ViewModels.

### 4. Estado Loading
Siempre indica estados de carga para mejor UX.

### 5. Dispose Resources
Limpia recursos en el método `dispose()`.

```dart
@override
void dispose() {
  _streamSubscription?.cancel();
  _controller.dispose();
  super.dispose();
}
```

### 6. Immutability
Usa objetos inmutables para los modelos.

### 7. Optimización con Selector
Usa `Selector` en lugar de `Consumer` cuando solo necesites parte del estado.

```dart
Selector<UserViewModel, bool>(
  selector: (context, viewModel) => viewModel.isLoading,
  builder: (context, isLoading, child) {
    return isLoading 
        ? CircularProgressIndicator()
        : child!;
  },
  child: UserList(),
)
```

## 📚 Recursos Adicionales

- [Provider Documentation](https://pub.dev/packages/provider)
- [Freezed Package](https://pub.dev/packages/freezed)

## 🔄 Migración

### Desde setState

1. Extrae la lógica de negocio de tus Widgets a ViewModels
2. Reemplaza `setState()` con `notifyListeners()`
3. Envuelve tus Widgets con `Consumer` o `Selector`

### A Clean Architecture

Si tu proyecto crece, considera migrar a Clean Architecture para mayor escalabilidad.

---

**Última actualización:** Diciembre 2025  
**Versión:** 1.0.0

