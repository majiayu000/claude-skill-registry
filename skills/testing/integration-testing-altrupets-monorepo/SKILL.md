# 🧪 Skill: Testing Strategy

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-testing-strategy` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `testing`, `test`, `unit-test`, `widget-test`, `integration-test`, `tdd` |

## 🔑 Keywords para Invocación

- `testing`
- `test`
- `unit-test`
- `widget-test`
- `integration-test`
- `tdd` (Test-Driven Development)
- `@skill:integration-testing`

### Ejemplos de Prompts

```
Implementa testing comprehensivo para este módulo
```

```
Necesito unit-test y widget-test para la feature de usuarios
```

```
@skill:testing - Crea tests TDD para el módulo de autenticación
```

## 📖 Descripción

Estrategia completa de testing para Flutter, incluyendo unit tests, widget tests, integration tests y mejores prácticas.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

## 🎯 Tipos de Testing

### 1. Unit Tests ⚡

Prueban lógica de negocio aislada (ViewModels, UseCases, Repositories).

```dart
// test/domain/usecases/get_user_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dartz/dartz.dart';

void main() {
  late GetUser usecase;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    usecase = GetUser(mockRepository);
  });

  test('should get user from repository', () async {
    // Arrange
    const userId = '1';
    const tUser = UserEntity(
      id: '1',
      name: 'Test',
      email: 'test@test.com',
      createdAt: DateTime(2024),
    );
    when(mockRepository.getUser(any))
        .thenAnswer((_) async => const Right(tUser));

    // Act
    final result = await usecase(userId);

    // Assert
    expect(result, const Right(tUser));
    verify(mockRepository.getUser(userId));
    verifyNoMoreInteractions(mockRepository);
  });
}
```

### 2. Widget Tests 🎨

Prueban UI y comportamiento de widgets.

```dart
// test/presentation/widgets/user_card_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('UserCard displays user information', (tester) async {
    // Arrange
    const user = UserEntity(
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
      createdAt: DateTime(2024),
    );

    // Act
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: UserCard(user: user),
        ),
      ),
    );

    // Assert
    expect(find.text('John Doe'), findsOneWidget);
    expect(find.text('john@example.com'), findsOneWidget);
  });

  testWidgets('UserCard calls onTap when tapped', (tester) async {
    // Arrange
    var tapped = false;
    const user = UserEntity(
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
      createdAt: DateTime(2024),
    );

    // Act
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: UserCard(
            user: user,
            onTap: () => tapped = true,
          ),
        ),
      ),
    );

    await tester.tap(find.byType(UserCard));

    // Assert
    expect(tapped, true);
  });
}
```

### 3. Integration Tests 🔄

Prueban flujos completos end-to-end.

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('User Flow Integration Tests', () {
    testWidgets('complete user CRUD flow', (tester) async {
      // Arrange
      await tester.pumpWidget(const MyApp());
      await tester.pumpAndSettle();

      // Navigate to user list
      await tester.tap(find.text('Users'));
      await tester.pumpAndSettle();

      // Create new user
      await tester.tap(find.byIcon(Icons.add));
      await tester.pumpAndSettle();

      await tester.enterText(
        find.byKey(const Key('nameField')),
        'John Doe',
      );
      await tester.enterText(
        find.byKey(const Key('emailField')),
        'john@example.com',
      );

      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();

      // Verify user was created
      expect(find.text('John Doe'), findsOneWidget);

      // Update user
      await tester.tap(find.text('John Doe'));
      await tester.pumpAndSettle();

      await tester.tap(find.byIcon(Icons.edit));
      await tester.pumpAndSettle();

      await tester.enterText(
        find.byKey(const Key('nameField')),
        'Jane Doe',
      );

      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();

      // Verify user was updated
      expect(find.text('Jane Doe'), findsOneWidget);
      expect(find.text('John Doe'), findsNothing);
    });
  });
}
```

### 4. BLoC Tests 🧊

```dart
// test/presentation/bloc/user_bloc_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

void main() {
  late UserBloc bloc;
  late MockGetUser mockGetUser;

  setUp(() {
    mockGetUser = MockGetUser();
    bloc = UserBloc(getUser: mockGetUser);
  });

  tearDown(() {
    bloc.close();
  });

  group('UserBloc', () {
    const tUser = UserEntity(
      id: '1',
      name: 'Test',
      email: 'test@test.com',
      createdAt: DateTime(2024),
    );

    blocTest<UserBloc, UserState>(
      'emits [Loading, Loaded] when GetUserEvent is added successfully',
      build: () {
        when(mockGetUser(any))
            .thenAnswer((_) async => const Right(tUser));
        return bloc;
      },
      act: (bloc) => bloc.add(const GetUserEvent('1')),
      expect: () => [
        UserLoading(),
        const UserLoaded(tUser),
      ],
      verify: (_) {
        verify(mockGetUser('1'));
      },
    );

    blocTest<UserBloc, UserState>(
      'emits [Loading, Error] when GetUserEvent fails',
      build: () {
        when(mockGetUser(any))
            .thenAnswer((_) async => Left(ServerFailure()));
        return bloc;
      },
      act: (bloc) => bloc.add(const GetUserEvent('1')),
      expect: () => [
        UserLoading(),
        const UserError('Error del servidor. Por favor intenta de nuevo.'),
      ],
    );
  });
}
```

## 📦 Dependencias

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter

  # Mocking
  mockito: ^5.4.4
  mocktail: ^1.0.1

  # BLoC Testing
  bloc_test: ^9.1.5

  # Coverage
  test_coverage: ^0.2.0

  # Advanced Testing
  patrol: ^3.0.0
```

## ✅ Mejores Prácticas

1. **Arrange-Act-Assert:** Estructura clara de tests
2. **Isolation:** Cada test debe ser independiente
3. **Mocking:** Mock dependencias externas
4. **Coverage:** Mantén >80% de cobertura
5. **Naming:** Nombres descriptivos de tests
6. **Setup/Teardown:** Limpia después de cada test

## 📊 Coverage

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Generar reporte de cobertura
cd mobile
flutter test --coverage
cd ..
genhtml mobile/coverage/lcov.info -o mobile/coverage/html
open mobile/coverage/html/index.html
```

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
