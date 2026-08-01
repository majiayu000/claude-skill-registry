---
name: riverpod
description: '| ID | flutter-riverpod-state |'
---

# 🎨 Skill: State Management con Riverpod

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-riverpod-state` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `riverpod`, `state-management`, `provider-riverpod`, `hooks-riverpod` |
| **Referencia** | [Riverpod Official Docs](https://riverpod.dev/) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `riverpod`
- `state-management-riverpod`
- `provider-riverpod`
- `hooks-riverpod`
- `@skill:riverpod`

### Ejemplos de Prompts

```
Crea una app de lista de tareas usando riverpod
```

```
Implementa state management con riverpod para un módulo de productos
```

```
@skill:riverpod - Genera una app de gestión de usuarios con providers
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Riverpod es una reimplementación completa de Provider que soluciona muchas de sus limitaciones. Ofrece gestión de estado reactiva, compile-time safety, mejor testabilidad y eliminación de BuildContext para acceso a providers.

### ✅ Cuándo Usar Este Skill

- Proyectos nuevos que necesitan gestión de estado robusta
- Necesitas compile-time safety y mejor IDE support
- Quieres testear tu estado fácilmente sin widgets
- Necesitas gestión de estado global sin BuildContext
- Quieres evitar problemas comunes de Provider (InheritedWidget)
- Proyectos medianos a grandes con estado complejo

### ❌ Cuándo NO Usar Este Skill

- Proyectos muy simples (usa setState)
- El equipo no está familiarizado con reactive programming
- Ya tienes un proyecto grande con otro state management estable

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── providers/
│   │   ├── app_providers.dart
│   │   ├── theme_provider.dart
│   │   └── auth_provider.dart
│   ├── constants/
│   │   └── app_constants.dart
│   └── utils/
│       └── logger.dart
│
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── models/
│   │   │       └── user_model.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_interface.dart
│   │   ├── presentation/
│   │   │   ├── providers/
│   │   │   │   ├── auth_provider.dart
│   │   │   │   └── login_provider.dart
│   │   │   ├── screens/
│   │   │   │   ├── login_screen.dart
│   │   │   │   └── register_screen.dart
│   │   │   └── widgets/
│   │   │       └── login_form.dart
│   │   └── auth_providers.dart
│   │
│   └── products/
│       ├── data/
│       │   ├── repositories/
│       │   │   └── product_repository.dart
│       │   └── models/
│       │       └── product_model.dart
│       ├── domain/
│       │   └── entities/
│       │       └── product.dart
│       ├── presentation/
│       │   ├── providers/
│       │   │   ├── products_provider.dart
│       │   │   └── product_detail_provider.dart
│       │   ├── screens/
│       │   │   ├── products_screen.dart
│       │   │   └── product_detail_screen.dart
│       │   └── widgets/
│       │       └── product_card.dart
│       └── products_providers.dart
│
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Riverpod para state management
  flutter_riverpod: ^2.4.9
  # O usa hooks_riverpod si prefieres hooks
  # hooks_riverpod: ^2.4.9
  # flutter_hooks: ^0.20.3

  # Freezed para immutability (opcional pero recomendado)
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1

dev_dependencies:
  # Code generation
  build_runner: ^2.4.6
  freezed: ^2.4.5
  json_serializable: ^6.7.1

  # Testing
  mockito: ^5.4.4
```

## 💻 Implementación

### 1. Setup Inicial

#### main.dart con ProviderScope

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/foundation.dart';
import 'features/auth/presentation/screens/login_screen.dart';

void main() {
  runApp(
    // ProviderScope es requerido en la raíz
    ProviderScope(
      // Observer para logging en desarrollo
      observers: [
        if (kDebugMode) _Logger(),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Acceso a providers sin BuildContext
    final themeMode = ref.watch(themeModeProvider);

    return MaterialApp(
      title: 'Riverpod App',
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      themeMode: themeMode,
      home: const LoginScreen(),
    );
  }
}

// Logger para debugging de providers
class _Logger extends ProviderObserver {
  @override
  void didUpdateProvider(
    ProviderBase provider,
    Object? previousValue,
    Object? newValue,
    ProviderContainer container,
  ) {
    debugPrint('''
{
  "provider": "${provider.name ?? provider.runtimeType}",
  "newValue": "$newValue"
}''');
  }
}
```

### 2. Tipos de Providers

#### Provider - Para valores inmutables

```dart
// lib/core/providers/app_providers.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

// Provider simple para valores que no cambian
final apiBaseUrlProvider = Provider<String>((ref) {
  return 'https://api.example.com';
});

// Provider que depende de otro provider
final httpClientProvider = Provider<HttpClient>((ref) {
  final baseUrl = ref.watch(apiBaseUrlProvider);
  return HttpClient(baseUrl: baseUrl);
});
```

#### StateProvider - Para estado simple

```dart
// Para estado simple que cambia frecuentemente
final counterProvider = StateProvider<int>((ref) => 0);

final themeModeProvider = StateProvider<ThemeMode>((ref) {
  return ThemeMode.system;
});

// Uso en widget
class CounterScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);

    return Scaffold(
      body: Center(
        child: Text('Count: $count'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Modificar el estado
          ref.read(counterProvider.notifier).state++;
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
```

#### StateNotifierProvider - Para estado complejo

```dart
// lib/features/products/domain/entities/product.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'product.freezed.dart';
part 'product.g.dart';

@freezed
class Product with _$Product {
  const factory Product({
    required String id,
    required String name,
    required double price,
    required String imageUrl,
    @Default(0) int stock,
  }) = _Product;

  factory Product.fromJson(Map<String, dynamic> json) =>
      _$ProductFromJson(json);
}
```

```dart
// lib/features/products/presentation/providers/products_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/product.dart';
import '../../data/repositories/product_repository.dart';

part 'products_provider.freezed.dart';

// Estado de la lista de productos
@freezed
class ProductsState with _$ProductsState {
  const factory ProductsState({
    @Default([]) List<Product> products,
    @Default(false) bool isLoading,
    String? error,
  }) = _ProductsState;
}

// StateNotifier para manejar la lógica
class ProductsNotifier extends StateNotifier<ProductsState> {
  final ProductRepository _repository;

  ProductsNotifier(this._repository) : super(const ProductsState());

  Future<void> loadProducts() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final products = await _repository.getProducts();
      state = state.copyWith(
        products: products,
        isLoading: false,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  void addProduct(Product product) {
    state = state.copyWith(
      products: [...state.products, product],
    );
  }

  void removeProduct(String productId) {
    state = state.copyWith(
      products: state.products.where((p) => p.id != productId).toList(),
    );
  }

  void updateProduct(Product product) {
    state = state.copyWith(
      products: state.products.map((p) {
        return p.id == product.id ? product : p;
      }).toList(),
    );
  }
}

// Provider del repository
final productRepositoryProvider = Provider<ProductRepository>((ref) {
  return ProductRepository();
});

// Provider del StateNotifier
final productsProvider = StateNotifierProvider<ProductsNotifier, ProductsState>((ref) {
  final repository = ref.watch(productRepositoryProvider);
  return ProductsNotifier(repository);
});
```

#### FutureProvider - Para datos asíncronos

```dart
// lib/features/products/presentation/providers/product_detail_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/product.dart';
import '../../data/repositories/product_repository.dart';

// Family permite pasar parámetros
final productDetailProvider = FutureProvider.family<Product, String>((ref, productId) async {
  final repository = ref.watch(productRepositoryProvider);
  return repository.getProductById(productId);
});

// Uso en widget
class ProductDetailScreen extends ConsumerWidget {
  final String productId;

  const ProductDetailScreen({required this.productId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productAsync = ref.watch(productDetailProvider(productId));

    return Scaffold(
      appBar: AppBar(title: Text('Product Detail')),
      body: productAsync.when(
        loading: () => Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Error: $error')),
        data: (product) => Column(
          children: [
            Image.network(product.imageUrl),
            Text(product.name),
            Text('\$${product.price}'),
          ],
        ),
      ),
    );
  }
}
```

#### StreamProvider - Para streams

```dart
// lib/features/auth/presentation/providers/auth_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/entities/user.dart';
import '../../data/repositories/auth_repository.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository();
});

// StreamProvider para el estado de autenticación
final authStateProvider = StreamProvider<User?>((ref) {
  final repository = ref.watch(authRepositoryProvider);
  return repository.authStateChanges();
});

// Provider computed que depende del stream
final isAuthenticatedProvider = Provider<bool>((ref) {
  final authState = ref.watch(authStateProvider);
  return authState.valueOrNull != null;
});
```

### 3. Consumir Providers en Widgets

#### ConsumerWidget

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ProductsScreen extends ConsumerWidget {
  const ProductsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsState = ref.watch(productsProvider);

    // Ejecutar acción al montar el widget
    ref.listen<ProductsState>(productsProvider, (previous, next) {
      if (next.error != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(next.error!)),
        );
      }
    });

    return Scaffold(
      appBar: AppBar(title: Text('Products')),
      body: productsState.isLoading
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: productsState.products.length,
              itemBuilder: (context, index) {
                final product = productsState.products[index];
                return ProductCard(product: product);
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Leer y ejecutar método
          ref.read(productsProvider.notifier).loadProducts();
        },
        child: Icon(Icons.refresh),
      ),
    );
  }
}
```

#### Consumer Widget (para optimización)

```dart
class OptimizedProductCard extends StatelessWidget {
  final Product product;

  const OptimizedProductCard({required this.product});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Image.network(product.imageUrl),
        title: Text(product.name),
        subtitle: Text('\$${product.price}'),
        trailing: Consumer(
          // Solo este Consumer se reconstruye cuando cambia el favorito
          builder: (context, ref, child) {
            final isFavorite = ref.watch(
              favoriteProvider(product.id),
            );
            return IconButton(
              icon: Icon(
                isFavorite ? Icons.favorite : Icons.favorite_border,
              ),
              onPressed: () {
                ref.read(favoriteProvider(product.id).notifier).toggle();
              },
            );
          },
        ),
      ),
    );
  }
}
```

#### HookConsumerWidget (con hooks_riverpod)

```dart
import 'package:flutter/material.dart';
import 'package:hooks_riverpod/hooks_riverpod.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class SearchProductsScreen extends HookConsumerWidget {
  const SearchProductsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Hooks para estado local
    final searchController = useTextEditingController();
    final searchQuery = useState('');

    // Provider que depende del query
    final searchResults = ref.watch(
      searchProductsProvider(searchQuery.value),
    );

    // Effect para ejecutar búsqueda
    useEffect(() {
      final timer = Timer(Duration(milliseconds: 500), () {
        searchQuery.value = searchController.text;
      });
      return timer.cancel;
    }, [searchController.text]);

    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: searchController,
          decoration: InputDecoration(
            hintText: 'Search products...',
          ),
        ),
      ),
      body: searchResults.when(
        loading: () => Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Error: $error')),
        data: (products) => ListView.builder(
          itemCount: products.length,
          itemBuilder: (context, index) {
            return ProductCard(product: products[index]);
          },
        ),
      ),
    );
  }
}
```

### 4. Modifiers de Providers

#### autoDispose - Limpieza automática

```dart
// Provider que se elimina automáticamente cuando no está en uso
final tempDataProvider = FutureProvider.autoDispose<Data>((ref) async {
  final data = await fetchData();

  // Limpieza al dispose
  ref.onDispose(() {
    debugPrint('Provider disposed');
  });

  return data;
});

// Con family
final productDetailProvider = FutureProvider.autoDispose.family<Product, String>(
  (ref, productId) async {
    final repository = ref.watch(productRepositoryProvider);
    return repository.getProductById(productId);
  },
);
```

#### keepAlive - Mantener cache

```dart
final cacheableProvider = FutureProvider.autoDispose<Data>((ref) async {
  // Mantener el provider vivo incluso si no hay listeners
  final link = ref.keepAlive();

  // Opcionalmente, configurar un timer para limpiar después
  Timer? timer;
  ref.onDispose(() => timer?.cancel());

  // Mantener cache por 5 minutos
  ref.onCancel(() {
    timer = Timer(Duration(minutes: 5), () {
      link.close();
    });
  });

  return fetchData();
});
```

### 5. Dependency Injection

```dart
// lib/core/providers/app_providers.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';

// Configuración de Dio
final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: Duration(seconds: 5),
      receiveTimeout: Duration(seconds: 3),
    ),
  );

  // Interceptors
  dio.interceptors.add(
    InterceptorsWrapper(
      onRequest: (options, handler) {
        // Agregar token de autenticación
        final token = ref.read(authTokenProvider);
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
      onError: (error, handler) {
        // Manejar errores globalmente
        debugPrint('Dio error: ${error.message}');
        return handler.next(error);
      },
    ),
  );

  return dio;
});

// Repository usando Dio
final productRepositoryProvider = Provider<ProductRepository>((ref) {
  final dio = ref.watch(dioProvider);
  return ProductRepository(dio);
});
```

### 6. Testing

#### Test de Providers

```dart
// test/features/products/presentation/providers/products_provider_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

@GenerateMocks([ProductRepository])
import 'products_provider_test.mocks.dart';

void main() {
  late MockProductRepository mockRepository;
  late ProviderContainer container;

  setUp(() {
    mockRepository = MockProductRepository();
    container = ProviderContainer(
      overrides: [
        // Override del repository con mock
        productRepositoryProvider.overrideWithValue(mockRepository),
      ],
    );
  });

  tearDown(() {
    container.dispose();
  });

  group('ProductsNotifier', () {
    test('initial state is empty', () {
      final notifier = container.read(productsProvider.notifier);
      final state = container.read(productsProvider);

      expect(state.products, isEmpty);
      expect(state.isLoading, false);
      expect(state.error, isNull);
    });

    test('loadProducts sets loading state and then products', () async {
      final mockProducts = [
        Product(id: '1', name: 'Product 1', price: 10.0, imageUrl: 'url'),
        Product(id: '2', name: 'Product 2', price: 20.0, imageUrl: 'url'),
      ];

      when(mockRepository.getProducts())
          .thenAnswer((_) async => mockProducts);

      final notifier = container.read(productsProvider.notifier);

      // Iniciar carga
      final loadFuture = notifier.loadProducts();

      // Verificar estado de loading
      expect(container.read(productsProvider).isLoading, true);

      // Esperar a que complete
      await loadFuture;

      // Verificar estado final
      final finalState = container.read(productsProvider);
      expect(finalState.isLoading, false);
      expect(finalState.products, mockProducts);
      expect(finalState.error, isNull);

      verify(mockRepository.getProducts()).called(1);
    });

    test('loadProducts sets error on failure', () async {
      when(mockRepository.getProducts())
          .thenThrow(Exception('Network error'));

      final notifier = container.read(productsProvider.notifier);
      await notifier.loadProducts();

      final state = container.read(productsProvider);
      expect(state.isLoading, false);
      expect(state.products, isEmpty);
      expect(state.error, isNotNull);
    });

    test('addProduct adds product to list', () {
      final notifier = container.read(productsProvider.notifier);
      final newProduct = Product(
        id: '1',
        name: 'New Product',
        price: 15.0,
        imageUrl: 'url',
      );

      notifier.addProduct(newProduct);

      final state = container.read(productsProvider);
      expect(state.products.length, 1);
      expect(state.products.first, newProduct);
    });
  });
}
```

#### Test de Widgets con Providers

```dart
// test/features/products/presentation/screens/products_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/mockito.dart';

void main() {
  testWidgets('ProductsScreen shows loading indicator', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        child: MaterialApp(
          home: ProductsScreen(),
        ),
      ),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
  });

  testWidgets('ProductsScreen shows products after loading', (tester) async {
    final mockProducts = [
      Product(id: '1', name: 'Product 1', price: 10.0, imageUrl: 'url'),
      Product(id: '2', name: 'Product 2', price: 20.0, imageUrl: 'url'),
    ];

    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          productsProvider.overrideWith((ref) {
            return ProductsNotifier(MockProductRepository())
              ..state = ProductsState(products: mockProducts);
          }),
        ],
        child: MaterialApp(
          home: ProductsScreen(),
        ),
      ),
    );

    await tester.pumpAndSettle();

    expect(find.text('Product 1'), findsOneWidget);
    expect(find.text('Product 2'), findsOneWidget);
  });
}
```

## 🎯 Mejores Prácticas

### 1. Organización de Providers

✅ **DO:**
```dart
// Agrupa providers relacionados en archivos específicos
// lib/features/auth/auth_providers.dart
final authRepositoryProvider = Provider<AuthRepository>(...);
final authStateProvider = StreamProvider<User?>(...);
final isAuthenticatedProvider = Provider<bool>(...);
```

❌ **DON'T:**
```dart
// No pongas todos los providers en un solo archivo gigante
// lib/providers/all_providers.dart (con 50+ providers)
```

### 2. Naming Conventions

✅ **DO:**
```dart
final userProvider = StateNotifierProvider<UserNotifier, User>(...);
final productsProvider = StateNotifierProvider<ProductsNotifier, ProductsState>(...);
final currentUserProvider = Provider<User?>(...);
```

❌ **DON'T:**
```dart
final user = StateNotifierProvider(...);  // Falta "Provider" al final
final getProducts = Provider(...);  // No uses verbos
```

### 3. Uso de .select para Optimización

✅ **DO:**
```dart
// Solo reconstruye cuando cambia el name
final name = ref.watch(userProvider.select((user) => user.name));

// O con StateNotifier
final isLoading = ref.watch(
  productsProvider.select((state) => state.isLoading),
);
```

❌ **DON'T:**
```dart
// Reconstruye cuando cambia cualquier propiedad del user
final user = ref.watch(userProvider);
final name = user.name;
```

### 4. Separación de Concerns

✅ **DO:**
```dart
// Repository en provider
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository();
});

// Lógica de negocio en StateNotifier
class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _repository;
  AuthNotifier(this._repository) : super(AuthState.initial());

  Future<void> login(String email, String password) async {
    // Lógica aquí
  }
}
```

❌ **DON'T:**
```dart
// No mezcles lógica de UI con lógica de negocio
class AuthNotifier extends StateNotifier<AuthState> {
  Future<void> login(String email, String password, BuildContext context) async {
    // ...
    Navigator.push(context, ...);  // ❌ No hagas esto
    ScaffoldMessenger.of(context).showSnackBar(...);  // ❌ No hagas esto
  }
}
```

### 5. Manejo de Errores

✅ **DO:**
```dart
@freezed
class ProductsState with _$ProductsState {
  const factory ProductsState({
    @Default([]) List<Product> products,
    @Default(false) bool isLoading,
    String? error,  // Error como parte del estado
  }) = _ProductsState;
}

// En el widget, usa ref.listen para side effects
ref.listen<ProductsState>(productsProvider, (previous, next) {
  if (next.error != null) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(next.error!)),
    );
  }
});
```

### 6. AutoDispose por Defecto

✅ **DO:**
```dart
// Usa autoDispose para providers temporales
final productDetailProvider = FutureProvider.autoDispose.family<Product, String>(
  (ref, id) async {
    return fetchProduct(id);
  },
);
```

❌ **DON'T:**
```dart
// No uses providers sin autoDispose para datos temporales
final productDetailProvider = FutureProvider.family<Product, String>(
  (ref, id) async {
    return fetchProduct(id);  // Esto queda en memoria indefinidamente
  },
);
```

## 📚 Recursos Adicionales

- [Riverpod Official Documentation](https://riverpod.dev/)
- [Riverpod Architecture](https://codewithandrea.com/articles/flutter-app-architecture-riverpod-introduction/)
- [Riverpod Best Practices](https://riverpod.dev/docs/concepts/modifiers/family#prefer-using-autodispose-when-possible)
- [Riverpod Examples](https://github.com/rrousselGit/riverpod/tree/master/examples)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md) - Combina Riverpod con Clean Architecture
- [Testing Strategy](../testing/SKILL.md) - Testing de providers
- [Project Setup](../project-setup/SKILL.md) - Setup inicial del proyecto

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
