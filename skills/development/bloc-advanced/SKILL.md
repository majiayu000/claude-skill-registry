# 🎨 Skill: State Management con BLoC Avanzado

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-bloc-advanced` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `bloc`, `cubit`, `state-management-bloc`, `flutter-bloc`, `hydrated-bloc` |
| **Referencia** | [BLoC Official Docs](https://bloclibrary.dev/) |

## 🔑 Keywords para Invocación

Usa cualquiera de estos keywords en tus prompts para invocar este skill:

- `bloc`
- `cubit`
- `flutter-bloc`
- `bloc-advanced`
- `hydrated-bloc`
- `@skill:bloc-advanced`

### Ejemplos de Prompts

```
Crea una app con bloc avanzado y persistencia
```

```
Implementa state management con cubit para un módulo de productos
```

```
@skill:bloc-advanced - Genera una app con BLoC y manejo de eventos complejos
```

## 📖 Descripción

BLoC (Business Logic Component) es un patrón de gestión de estado que separa la lógica de negocio de la UI mediante streams. Este skill cubre técnicas avanzadas como Hydrated BLoC para persistencia, Replay BLoC para debugging, transformers para control de eventos, y estrategias de testing exhaustivas.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Aplicaciones enterprise con lógica compleja
- Necesitas separación estricta entre UI y lógica
- Requieres testing exhaustivo de lógica de negocio
- Necesitas persistencia automática del estado
- Quieres replay/undo de estados para debugging
- Aplicaciones con flujos de eventos complejos
- Necesitas transformers para debounce/throttle/retry

### ❌ Cuándo NO Usar Este Skill

- Proyectos muy simples (usa setState o Provider)
- El equipo no está familiarizado con reactive programming
- No necesitas la robustez que ofrece BLoC

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── bloc/
│   │   ├── bloc_observer.dart
│   │   └── app_bloc_observer.dart
│   ├── error/
│   │   ├── failures.dart
│   │   └── exceptions.dart
│   └── utils/
│       └── bloc_transformers.dart
│
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   ├── auth_local_datasource.dart
│   │   │   │   └── auth_remote_datasource.dart
│   │   │   ├── models/
│   │   │   │   └── user_model.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   │       ├── login_usecase.dart
│   │   │       ├── logout_usecase.dart
│   │   │       └── get_current_user_usecase.dart
│   │   └── presentation/
│   │       ├── bloc/
│   │       │   ├── auth_bloc.dart
│   │       │   ├── auth_event.dart
│   │       │   ├── auth_state.dart
│   │       │   └── login/
│   │       │       ├── login_cubit.dart
│   │       │       └── login_state.dart
│   │       ├── screens/
│   │       │   ├── login_screen.dart
│   │       │   └── register_screen.dart
│   │       └── widgets/
│   │           └── login_form.dart
│   │
│   └── products/
│       ├── data/
│       │   ├── datasources/
│       │   │   └── product_remote_datasource.dart
│       │   ├── models/
│       │   │   └── product_model.dart
│       │   └── repositories/
│       │       └── product_repository_impl.dart
│       ├── domain/
│       │   ├── entities/
│       │   │   └── product.dart
│       │   ├── repositories/
│       │   │   └── product_repository.dart
│       │   └── usecases/
│       │       ├── get_products_usecase.dart
│       │       ├── search_products_usecase.dart
│       │       └── add_to_cart_usecase.dart
│       └── presentation/
│           ├── bloc/
│           │   ├── products_bloc.dart
│           │   ├── products_event.dart
│           │   ├── products_state.dart
│           │   ├── product_detail/
│           │   │   ├── product_detail_cubit.dart
│           │   │   └── product_detail_state.dart
│           │   └── cart/
│           │       ├── cart_bloc.dart
│           │       ├── cart_event.dart
│           │       └── cart_state.dart
│           ├── screens/
│           │   ├── products_screen.dart
│           │   ├── product_detail_screen.dart
│           │   └── cart_screen.dart
│           └── widgets/
│               ├── product_card.dart
│               └── cart_item.dart
│
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # BLoC core
  flutter_bloc: ^8.1.3
  bloc: ^8.1.2
  
  # BLoC extras
  hydrated_bloc: ^9.1.2  # Persistencia automática
  replay_bloc: ^0.2.3    # Replay/undo functionality
  
  # Utilities
  equatable: ^2.0.5      # Para comparación de estados
  freezed_annotation: ^2.4.1  # Immutability
  json_annotation: ^4.8.1
  
  # Dependency Injection
  get_it: ^7.6.4
  injectable: ^2.3.2
  
  # Storage para Hydrated BLoC
  path_provider: ^2.1.1

dev_dependencies:
  # Code generation
  build_runner: ^2.4.6
  freezed: ^2.4.5
  json_serializable: ^6.7.1
  injectable_generator: ^2.4.1
  
  # Testing
  bloc_test: ^9.1.4
  mocktail: ^1.0.1
```

## 💻 Implementación

### 1. Setup Inicial con BLoC Observer

#### main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:hydrated_bloc/hydrated_bloc.dart';
import 'package:path_provider/path_provider.dart';
import 'core/bloc/app_bloc_observer.dart';
import 'core/di/injection.dart';
import 'features/auth/presentation/bloc/auth_bloc.dart';
import 'features/auth/presentation/screens/login_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Configurar storage para Hydrated BLoC
  HydratedBloc.storage = await HydratedStorage.build(
    storageDirectory: await getApplicationDocumentsDirectory(),
  );
  
  // Configurar BLoC observer para logging
  Bloc.observer = AppBlocObserver();
  
  // Configurar dependency injection
  configureDependencies();
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        // BLoC global de autenticación
        BlocProvider<AuthBloc>(
          create: (context) => getIt<AuthBloc>()
            ..add(const AuthCheckRequested()),
        ),
        // Puedes agregar más BLoCs globales aquí
      ],
      child: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, state) {
          return MaterialApp(
            title: 'BLoC Advanced App',
            theme: ThemeData.light(),
            darkTheme: ThemeData.dark(),
            home: state.maybeWhen(
              authenticated: (user) => const HomeScreen(),
              unauthenticated: () => const LoginScreen(),
              orElse: () => const SplashScreen(),
            ),
          );
        },
      ),
    );
  }
}
```

#### BLoC Observer para Logging

```dart
// lib/core/bloc/app_bloc_observer.dart
import 'package:flutter/foundation.dart';
import 'package:bloc/bloc.dart';

class AppBlocObserver extends BlocObserver {
  @override
  void onCreate(BlocBase bloc) {
    super.onCreate(bloc);
    debugPrint('📦 onCreate -- ${bloc.runtimeType}');
  }

  @override
  void onEvent(Bloc bloc, Object? event) {
    super.onEvent(bloc, event);
    debugPrint('📨 onEvent -- ${bloc.runtimeType}, $event');
  }

  @override
  void onChange(BlocBase bloc, Change change) {
    super.onChange(bloc, change);
    if (kDebugMode) {
      debugPrint('🔄 onChange -- ${bloc.runtimeType}');
      debugPrint('   currentState: ${change.currentState}');
      debugPrint('   nextState: ${change.nextState}');
    }
  }

  @override
  void onTransition(Bloc bloc, Transition transition) {
    super.onTransition(bloc, transition);
    if (kDebugMode) {
      debugPrint('🔀 onTransition -- ${bloc.runtimeType}');
      debugPrint('   event: ${transition.event}');
      debugPrint('   currentState: ${transition.currentState}');
      debugPrint('   nextState: ${transition.nextState}');
    }
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    debugPrint('❌ onError -- ${bloc.runtimeType}, $error');
    debugPrint('StackTrace: $stackTrace');
    super.onError(bloc, error, stackTrace);
  }

  @override
  void onClose(BlocBase bloc) {
    super.onClose(bloc);
    debugPrint('🗑️ onClose -- ${bloc.runtimeType}');
  }
}
```

### 2. BLoC Pattern Completo

#### Domain Layer

```dart
// lib/features/products/domain/entities/product.dart
import 'package:equatable/equatable.dart';

class Product extends Equatable {
  final String id;
  final String name;
  final String description;
  final double price;
  final String imageUrl;
  final int stock;
  final List<String> tags;

  const Product({
    required this.id,
    required this.name,
    required this.description,
    required this.price,
    required this.imageUrl,
    required this.stock,
    this.tags = const [],
  });

  @override
  List<Object?> get props => [id, name, description, price, imageUrl, stock, tags];
}
```

```dart
// lib/features/products/domain/usecases/get_products_usecase.dart
import 'package:dartz/dartz.dart';
import '../../../core/error/failures.dart';
import '../entities/product.dart';
import '../repositories/product_repository.dart';

class GetProductsUseCase {
  final ProductRepository repository;

  GetProductsUseCase(this.repository);

  Future<Either<Failure, List<Product>>> call({
    String? category,
    String? searchQuery,
    int page = 1,
    int limit = 20,
  }) async {
    return await repository.getProducts(
      category: category,
      searchQuery: searchQuery,
      page: page,
      limit: limit,
    );
  }
}
```

#### Presentation Layer - Events

```dart
// lib/features/products/presentation/bloc/products_event.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'products_event.freezed.dart';

@freezed
class ProductsEvent with _$ProductsEvent {
  const factory ProductsEvent.started() = ProductsStarted;
  
  const factory ProductsEvent.loadProducts({
    String? category,
    @Default(1) int page,
  }) = ProductsLoadRequested;
  
  const factory ProductsEvent.refreshProducts() = ProductsRefreshRequested;
  
  const factory ProductsEvent.searchProducts(String query) = ProductsSearchRequested;
  
  const factory ProductsEvent.loadMoreProducts() = ProductsLoadMoreRequested;
  
  const factory ProductsEvent.filterByCategory(String category) = ProductsFilterByCategoryRequested;
  
  const factory ProductsEvent.clearFilters() = ProductsClearFiltersRequested;
}
```

#### Presentation Layer - States

```dart
// lib/features/products/presentation/bloc/products_state.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/product.dart';

part 'products_state.freezed.dart';

@freezed
class ProductsState with _$ProductsState {
  const factory ProductsState.initial() = ProductsInitial;
  
  const factory ProductsState.loading() = ProductsLoading;
  
  const factory ProductsState.loaded({
    required List<Product> products,
    @Default(false) bool hasReachedMax,
    @Default(1) int currentPage,
    String? category,
    String? searchQuery,
  }) = ProductsLoaded;
  
  const factory ProductsState.loadingMore({
    required List<Product> products,
    @Default(1) int currentPage,
    String? category,
    String? searchQuery,
  }) = ProductsLoadingMore;
  
  const factory ProductsState.error(String message) = ProductsError;
}
```

#### Presentation Layer - BLoC

```dart
// lib/features/products/presentation/bloc/products_bloc.dart
import 'dart:async';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/product.dart';
import '../../domain/usecases/get_products_usecase.dart';
import 'products_event.dart';
import 'products_state.dart';

part 'products_bloc.freezed.dart';

class ProductsBloc extends Bloc<ProductsEvent, ProductsState> {
  final GetProductsUseCase getProductsUseCase;

  ProductsBloc({
    required this.getProductsUseCase,
  }) : super(const ProductsState.initial()) {
    on<ProductsStarted>(_onStarted);
    on<ProductsLoadRequested>(
      _onLoadRequested,
      transformer: restartable(),
    );
    on<ProductsRefreshRequested>(_onRefreshRequested);
    on<ProductsSearchRequested>(
      _onSearchRequested,
      transformer: debounce(const Duration(milliseconds: 300)),
    );
    on<ProductsLoadMoreRequested>(_onLoadMoreRequested);
    on<ProductsFilterByCategoryRequested>(_onFilterByCategoryRequested);
    on<ProductsClearFiltersRequested>(_onClearFiltersRequested);
  }

  Future<void> _onStarted(
    ProductsStarted event,
    Emitter<ProductsState> emit,
  ) async {
    emit(const ProductsState.loading());
    await _loadProducts(emit: emit);
  }

  Future<void> _onLoadRequested(
    ProductsLoadRequested event,
    Emitter<ProductsState> emit,
  ) async {
    emit(const ProductsState.loading());
    await _loadProducts(
      emit: emit,
      category: event.category,
      page: event.page,
    );
  }

  Future<void> _onRefreshRequested(
    ProductsRefreshRequested event,
    Emitter<ProductsState> emit,
  ) async {
    final currentState = state;
    
    // Mantener filtros si existen
    String? category;
    String? searchQuery;
    
    currentState.mapOrNull(
      loaded: (state) {
        category = state.category;
        searchQuery = state.searchQuery;
      },
    );
    
    await _loadProducts(
      emit: emit,
      category: category,
      searchQuery: searchQuery,
      page: 1,
    );
  }

  Future<void> _onSearchRequested(
    ProductsSearchRequested event,
    Emitter<ProductsState> emit,
  ) async {
    emit(const ProductsState.loading());
    await _loadProducts(
      emit: emit,
      searchQuery: event.query,
      page: 1,
    );
  }

  Future<void> _onLoadMoreRequested(
    ProductsLoadMoreRequested event,
    Emitter<ProductsState> emit,
  ) async {
    final currentState = state;
    
    await currentState.mapOrNull(
      loaded: (state) async {
        if (state.hasReachedMax) return;
        
        final nextPage = state.currentPage + 1;
        
        emit(ProductsState.loadingMore(
          products: state.products,
          currentPage: state.currentPage,
          category: state.category,
          searchQuery: state.searchQuery,
        ));
        
        await _loadProducts(
          emit: emit,
          category: state.category,
          searchQuery: state.searchQuery,
          page: nextPage,
          existingProducts: state.products,
        );
      },
    );
  }

  Future<void> _onFilterByCategoryRequested(
    ProductsFilterByCategoryRequested event,
    Emitter<ProductsState> emit,
  ) async {
    emit(const ProductsState.loading());
    await _loadProducts(
      emit: emit,
      category: event.category,
      page: 1,
    );
  }

  Future<void> _onClearFiltersRequested(
    ProductsClearFiltersRequested event,
    Emitter<ProductsState> emit,
  ) async {
    emit(const ProductsState.loading());
    await _loadProducts(emit: emit, page: 1);
  }

  Future<void> _loadProducts({
    required Emitter<ProductsState> emit,
    String? category,
    String? searchQuery,
    int page = 1,
    List<Product> existingProducts = const [],
  }) async {
    final result = await getProductsUseCase(
      category: category,
      searchQuery: searchQuery,
      page: page,
    );

    result.fold(
      (failure) => emit(ProductsState.error(failure.message)),
      (newProducts) {
        final allProducts = page > 1
            ? [...existingProducts, ...newProducts]
            : newProducts;

        emit(ProductsState.loaded(
          products: allProducts,
          hasReachedMax: newProducts.isEmpty,
          currentPage: page,
          category: category,
          searchQuery: searchQuery,
        ));
      },
    );
  }
}

// Transformers personalizados
EventTransformer<T> debounce<T>(Duration duration) {
  return (events, mapper) => events.debounceTime(duration).flatMap(mapper);
}

EventTransformer<T> restartable<T>() {
  return (events, mapper) => events.switchMap(mapper);
}
```

### 3. Cubit Pattern (más simple que BLoC)

```dart
// lib/features/products/presentation/bloc/product_detail/product_detail_cubit.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../../domain/entities/product.dart';
import '../../../domain/usecases/get_product_by_id_usecase.dart';

part 'product_detail_state.dart';
part 'product_detail_cubit.freezed.dart';

class ProductDetailCubit extends Cubit<ProductDetailState> {
  final GetProductByIdUseCase getProductByIdUseCase;

  ProductDetailCubit({
    required this.getProductByIdUseCase,
  }) : super(const ProductDetailState.initial());

  Future<void> loadProduct(String productId) async {
    emit(const ProductDetailState.loading());

    final result = await getProductByIdUseCase(productId);

    result.fold(
      (failure) => emit(ProductDetailState.error(failure.message)),
      (product) => emit(ProductDetailState.loaded(product)),
    );
  }

  void incrementQuantity() {
    state.mapOrNull(
      loaded: (state) {
        if (state.quantity < state.product.stock) {
          emit(state.copyWith(quantity: state.quantity + 1));
        }
      },
    );
  }

  void decrementQuantity() {
    state.mapOrNull(
      loaded: (state) {
        if (state.quantity > 1) {
          emit(state.copyWith(quantity: state.quantity - 1));
        }
      },
    );
  }

  void toggleFavorite() {
    state.mapOrNull(
      loaded: (state) {
        emit(state.copyWith(isFavorite: !state.isFavorite));
      },
    );
  }
}
```

```dart
// lib/features/products/presentation/bloc/product_detail/product_detail_state.dart
part of 'product_detail_cubit.dart';

@freezed
class ProductDetailState with _$ProductDetailState {
  const factory ProductDetailState.initial() = ProductDetailInitial;
  
  const factory ProductDetailState.loading() = ProductDetailLoading;
  
  const factory ProductDetailState.loaded(
    Product product, {
    @Default(1) int quantity,
    @Default(false) bool isFavorite,
  }) = ProductDetailLoaded;
  
  const factory ProductDetailState.error(String message) = ProductDetailError;
}
```

### 4. Hydrated BLoC para Persistencia

```dart
// lib/features/auth/presentation/bloc/auth_bloc.dart
import 'package:hydrated_bloc/hydrated_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/user.dart';
import '../../domain/usecases/login_usecase.dart';
import '../../domain/usecases/logout_usecase.dart';
import '../../domain/usecases/get_current_user_usecase.dart';
import 'auth_event.dart';
import 'auth_state.dart';

part 'auth_bloc.freezed.dart';
part 'auth_bloc.g.dart';

class AuthBloc extends HydratedBloc<AuthEvent, AuthState> {
  final LoginUseCase loginUseCase;
  final LogoutUseCase logoutUseCase;
  final GetCurrentUserUseCase getCurrentUserUseCase;

  AuthBloc({
    required this.loginUseCase,
    required this.logoutUseCase,
    required this.getCurrentUserUseCase,
  }) : super(const AuthState.initial()) {
    on<AuthCheckRequested>(_onCheckRequested);
    on<AuthLoginRequested>(_onLoginRequested);
    on<AuthLogoutRequested>(_onLogoutRequested);
  }

  Future<void> _onCheckRequested(
    AuthCheckRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthState.loading());

    final result = await getCurrentUserUseCase();

    result.fold(
      (failure) => emit(const AuthState.unauthenticated()),
      (user) => emit(AuthState.authenticated(user)),
    );
  }

  Future<void> _onLoginRequested(
    AuthLoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    emit(const AuthState.loading());

    final result = await loginUseCase(
      email: event.email,
      password: event.password,
    );

    result.fold(
      (failure) => emit(AuthState.error(failure.message)),
      (user) => emit(AuthState.authenticated(user)),
    );
  }

  Future<void> _onLogoutRequested(
    AuthLogoutRequested event,
    Emitter<AuthState> emit,
  ) async {
    await logoutUseCase();
    emit(const AuthState.unauthenticated());
  }

  // Persistencia: serializar estado a JSON
  @override
  AuthState? fromJson(Map<String, dynamic> json) {
    try {
      return AuthState.fromJson(json);
    } catch (_) {
      return null;
    }
  }

  // Persistencia: deserializar estado de JSON
  @override
  Map<String, dynamic>? toJson(AuthState state) {
    // Solo persistir estado authenticated
    return state.maybeMap(
      authenticated: (state) => state.toJson(),
      orElse: () => null,
    );
  }
}
```

### 5. Replay BLoC para Debugging

```dart
// lib/features/products/presentation/bloc/cart/cart_bloc.dart
import 'package:replay_bloc/replay_bloc.dart';
import 'package:freezed_annotation/freezed_annotation.dart';
import '../../domain/entities/product.dart';
import 'cart_event.dart';
import 'cart_state.dart';

part 'cart_bloc.freezed.dart';

class CartBloc extends ReplayBloc<CartEvent, CartState> {
  CartBloc() : super(const CartState.empty()) {
    on<CartAddProduct>(_onAddProduct);
    on<CartRemoveProduct>(_onRemoveProduct);
    on<CartUpdateQuantity>(_onUpdateQuantity);
    on<CartClear>(_onClear);
  }

  void _onAddProduct(CartAddProduct event, Emitter<CartState> emit) {
    state.map(
      empty: (_) => emit(CartState.loaded(
        items: {event.product.id: CartItem(product: event.product, quantity: 1)},
      )),
      loaded: (state) {
        final items = Map<String, CartItem>.from(state.items);
        
        if (items.containsKey(event.product.id)) {
          final existingItem = items[event.product.id]!;
          items[event.product.id] = existingItem.copyWith(
            quantity: existingItem.quantity + 1,
          );
        } else {
          items[event.product.id] = CartItem(
            product: event.product,
            quantity: 1,
          );
        }
        
        emit(state.copyWith(items: items));
      },
    );
  }

  void _onRemoveProduct(CartRemoveProduct event, Emitter<CartState> emit) {
    state.mapOrNull(
      loaded: (state) {
        final items = Map<String, CartItem>.from(state.items);
        items.remove(event.productId);
        
        if (items.isEmpty) {
          emit(const CartState.empty());
        } else {
          emit(state.copyWith(items: items));
        }
      },
    );
  }

  void _onUpdateQuantity(CartUpdateQuantity event, Emitter<CartState> emit) {
    state.mapOrNull(
      loaded: (state) {
        final items = Map<String, CartItem>.from(state.items);
        final item = items[event.productId];
        
        if (item != null) {
          if (event.quantity <= 0) {
            items.remove(event.productId);
          } else {
            items[event.productId] = item.copyWith(quantity: event.quantity);
          }
          
          if (items.isEmpty) {
            emit(const CartState.empty());
          } else {
            emit(state.copyWith(items: items));
          }
        }
      },
    );
  }

  void _onClear(CartClear event, Emitter<CartState> emit) {
    emit(const CartState.empty());
  }
}

// Uso de Replay BLoC en UI
class CartScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => CartBloc(),
      child: Scaffold(
        appBar: AppBar(
          title: Text('Cart'),
          actions: [
            // Botones de undo/redo
            BlocBuilder<CartBloc, CartState>(
              builder: (context, state) {
                final bloc = context.read<CartBloc>();
                return Row(
                  children: [
                    IconButton(
                      icon: Icon(Icons.undo),
                      onPressed: bloc.canUndo ? bloc.undo : null,
                    ),
                    IconButton(
                      icon: Icon(Icons.redo),
                      onPressed: bloc.canRedo ? bloc.redo : null,
                    ),
                  ],
                );
              },
            ),
          ],
        ),
        body: BlocBuilder<CartBloc, CartState>(
          builder: (context, state) {
            return state.map(
              empty: (_) => Center(child: Text('Cart is empty')),
              loaded: (state) => ListView.builder(
                itemCount: state.items.length,
                itemBuilder: (context, index) {
                  final item = state.items.values.elementAt(index);
                  return CartItemWidget(item: item);
                },
              ),
            );
          },
        ),
      ),
    );
  }
}
```

### 6. Uso de BLoC en Widgets

#### BlocBuilder

```dart
class ProductsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Products')),
      body: BlocBuilder<ProductsBloc, ProductsState>(
        builder: (context, state) {
          return state.map(
            initial: (_) => Center(child: Text('Press button to load')),
            loading: (_) => Center(child: CircularProgressIndicator()),
            loaded: (state) => ProductsList(products: state.products),
            loadingMore: (state) => ProductsList(
              products: state.products,
              isLoadingMore: true,
            ),
            error: (state) => ErrorWidget(message: state.message),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          context.read<ProductsBloc>().add(
            const ProductsEvent.loadProducts(),
          );
        },
        child: Icon(Icons.refresh),
      ),
    );
  }
}
```

#### BlocListener para Side Effects

```dart
class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => LoginCubit(
        loginUseCase: getIt<LoginUseCase>(),
      ),
      child: Scaffold(
        appBar: AppBar(title: Text('Login')),
        body: BlocListener<LoginCubit, LoginState>(
          listener: (context, state) {
            // Side effects aquí
            state.mapOrNull(
              success: (state) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Login successful!')),
                );
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => HomeScreen()),
                );
              },
              error: (state) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(state.message),
                    backgroundColor: Colors.red,
                  ),
                );
              },
            );
          },
          child: LoginForm(),
        ),
      ),
    );
  }
}
```

#### BlocConsumer (Builder + Listener combinados)

```dart
class ProductDetailScreen extends StatelessWidget {
  final String productId;
  
  const ProductDetailScreen({required this.productId});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => ProductDetailCubit(
        getProductByIdUseCase: getIt<GetProductByIdUseCase>(),
      )..loadProduct(productId),
      child: Scaffold(
        appBar: AppBar(title: Text('Product Detail')),
        body: BlocConsumer<ProductDetailCubit, ProductDetailState>(
          listener: (context, state) {
            // Side effects
            state.mapOrNull(
              error: (state) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(state.message)),
                );
              },
            );
          },
          builder: (context, state) {
            // UI
            return state.map(
              initial: (_) => SizedBox.shrink(),
              loading: (_) => Center(child: CircularProgressIndicator()),
              loaded: (state) => ProductDetailContent(
                product: state.product,
                quantity: state.quantity,
                isFavorite: state.isFavorite,
              ),
              error: (state) => ErrorWidget(message: state.message),
            );
          },
        ),
      ),
    );
  }
}
```

### 7. Testing con BLoC Test

```dart
// test/features/products/presentation/bloc/products_bloc_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockGetProductsUseCase extends Mock implements GetProductsUseCase {}

void main() {
  late ProductsBloc bloc;
  late MockGetProductsUseCase mockGetProductsUseCase;

  setUp(() {
    mockGetProductsUseCase = MockGetProductsUseCase();
    bloc = ProductsBloc(getProductsUseCase: mockGetProductsUseCase);
  });

  tearDown(() {
    bloc.close();
  });

  group('ProductsBloc', () {
    final tProducts = [
      Product(
        id: '1',
        name: 'Product 1',
        description: 'Description 1',
        price: 10.0,
        imageUrl: 'url1',
        stock: 5,
      ),
      Product(
        id: '2',
        name: 'Product 2',
        description: 'Description 2',
        price: 20.0,
        imageUrl: 'url2',
        stock: 10,
      ),
    ];

    test('initial state is ProductsInitial', () {
      expect(bloc.state, equals(const ProductsState.initial()));
    });

    blocTest<ProductsBloc, ProductsState>(
      'emits [loading, loaded] when load products succeeds',
      build: () {
        when(() => mockGetProductsUseCase(
              category: any(named: 'category'),
              searchQuery: any(named: 'searchQuery'),
              page: any(named: 'page'),
              limit: any(named: 'limit'),
            )).thenAnswer((_) async => Right(tProducts));
        return bloc;
      },
      act: (bloc) => bloc.add(const ProductsEvent.loadProducts()),
      expect: () => [
        const ProductsState.loading(),
        ProductsState.loaded(
          products: tProducts,
          hasReachedMax: false,
          currentPage: 1,
        ),
      ],
      verify: (_) {
        verify(() => mockGetProductsUseCase(
              category: null,
              searchQuery: null,
              page: 1,
              limit: 20,
            )).called(1);
      },
    );

    blocTest<ProductsBloc, ProductsState>(
      'emits [loading, error] when load products fails',
      build: () {
        when(() => mockGetProductsUseCase(
              category: any(named: 'category'),
              searchQuery: any(named: 'searchQuery'),
              page: any(named: 'page'),
              limit: any(named: 'limit'),
            )).thenAnswer((_) async => Left(ServerFailure('Server error')));
        return bloc;
      },
      act: (bloc) => bloc.add(const ProductsEvent.loadProducts()),
      expect: () => [
        const ProductsState.loading(),
        const ProductsState.error('Server error'),
      ],
    );

    blocTest<ProductsBloc, ProductsState>(
      'emits correct states when loading more products',
      build: () {
        when(() => mockGetProductsUseCase(
              category: any(named: 'category'),
              searchQuery: any(named: 'searchQuery'),
              page: any(named: 'page'),
              limit: any(named: 'limit'),
            )).thenAnswer((_) async => Right(tProducts));
        return bloc;
      },
      seed: () => ProductsState.loaded(
        products: tProducts,
        currentPage: 1,
      ),
      act: (bloc) => bloc.add(const ProductsEvent.loadMoreProducts()),
      expect: () => [
        ProductsState.loadingMore(products: tProducts, currentPage: 1),
        ProductsState.loaded(
          products: [...tProducts, ...tProducts],
          currentPage: 2,
        ),
      ],
    );

    blocTest<ProductsBloc, ProductsState>(
      'debounces search events',
      build: () {
        when(() => mockGetProductsUseCase(
              category: any(named: 'category'),
              searchQuery: any(named: 'searchQuery'),
              page: any(named: 'page'),
              limit: any(named: 'limit'),
            )).thenAnswer((_) async => Right(tProducts));
        return bloc;
      },
      act: (bloc) async {
        bloc.add(const ProductsEvent.searchProducts('test1'));
        bloc.add(const ProductsEvent.searchProducts('test2'));
        bloc.add(const ProductsEvent.searchProducts('test3'));
      },
      wait: const Duration(milliseconds: 400),
      expect: () => [
        const ProductsState.loading(),
        ProductsState.loaded(
          products: tProducts,
          searchQuery: 'test3',
          currentPage: 1,
        ),
      ],
      verify: (_) {
        // Solo debe llamar una vez debido al debounce
        verify(() => mockGetProductsUseCase(
              category: null,
              searchQuery: 'test3',
              page: 1,
              limit: 20,
            )).called(1);
      },
    );
  });
}
```

## 🎯 Mejores Prácticas

### 1. Event Naming

✅ **DO:**
```dart
const factory ProductsEvent.loadProducts() = ProductsLoadRequested;
const factory ProductsEvent.refreshProducts() = ProductsRefreshRequested;
```

❌ **DON'T:**
```dart
const factory ProductsEvent.load() = LoadProducts;  // Poco descriptivo
const factory ProductsEvent.getProducts() = GetProducts;  // Usa verbos de UI
```

### 2. State Naming y Estructura

✅ **DO:**
```dart
@freezed
class ProductsState with _$ProductsState {
  const factory ProductsState.initial() = ProductsInitial;
  const factory ProductsState.loading() = ProductsLoading;
  const factory ProductsState.loaded({
    required List<Product> products,
    @Default(false) bool hasReachedMax,
  }) = ProductsLoaded;
  const factory ProductsState.error(String message) = ProductsError;
}
```

❌ **DON'T:**
```dart
// No uses un solo estado con flags
class ProductsState {
  final List<Product> products;
  final bool isLoading;
  final bool hasError;
  final String? errorMessage;
}
```

### 3. Uso de Transformers

✅ **DO:**
```dart
on<ProductsSearchRequested>(
  _onSearchRequested,
  transformer: debounce(const Duration(milliseconds: 300)),
);

on<ProductsLoadRequested>(
  _onLoadRequested,
  transformer: restartable(),  // Cancela eventos anteriores
);
```

### 4. Separación de Concerns

✅ **DO:**
```dart
// BLoC solo coordina
class ProductsBloc extends Bloc<ProductsEvent, ProductsState> {
  final GetProductsUseCase getProductsUseCase;  // Use case hace el trabajo
  
  Future<void> _onLoadRequested(...) async {
    final result = await getProductsUseCase();  // Delega al use case
    // ... maneja resultado
  }
}
```

❌ **DON'T:**
```dart
// BLoC con lógica de negocio acoplada
class ProductsBloc extends Bloc<ProductsEvent, ProductsState> {
  final Dio dio;
  
  Future<void> _onLoadRequested(...) async {
    final response = await dio.get('/products');  // ❌ Lógica de API aquí
    final products = (response.data as List).map(...).toList();  // ❌ Parsing aquí
  }
}
```

### 5. Testing Exhaustivo

✅ **DO:**
```dart
// Usa bloc_test para tests claros y concisos
blocTest<ProductsBloc, ProductsState>(
  'emits [loading, loaded] when successful',
  build: () => ProductsBloc(getProductsUseCase: mockUseCase),
  act: (bloc) => bloc.add(const ProductsEvent.loadProducts()),
  expect: () => [
    const ProductsState.loading(),
    ProductsState.loaded(products: tProducts),
  ],
);
```

### 6. Manejo de Streams y Subscriptions

✅ **DO:**
```dart
class NotificationsBloc extends Bloc<NotificationsEvent, NotificationsState> {
  final NotificationService _notificationService;
  StreamSubscription<Notification>? _notificationSubscription;

  NotificationsBloc(this._notificationService) : super(...) {
    on<NotificationsStarted>(_onStarted);
    on<NotificationsReceived>(_onReceived);
  }

  Future<void> _onStarted(...) async {
    await _notificationSubscription?.cancel();
    _notificationSubscription = _notificationService.stream.listen(
      (notification) => add(NotificationsEvent.received(notification)),
    );
  }

  @override
  Future<void> close() {
    _notificationSubscription?.cancel();
    return super.close();
  }
}
```

## 📚 Recursos Adicionales

- [BLoC Official Documentation](https://bloclibrary.dev/)
- [Hydrated BLoC](https://pub.dev/packages/hydrated_bloc)
- [Replay BLoC](https://pub.dev/packages/replay_bloc)
- [BLoC Test](https://pub.dev/packages/bloc_test)
- [BLoC Architecture Tutorial](https://bloclibrary.dev/#/architecture)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md) - Arquitectura completa con BLoC
- [Testing Strategy](../testing/SKILL.md) - Testing de BLoCs
- [Riverpod](../riverpod/SKILL.md) - Alternativa a BLoC

---

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2025

