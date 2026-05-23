---
name: Advanced GetX Patterns
description: Advanced GetX features including Workers, GetxService, SmartManagement, GetConnect, GetSocket, bindings composition, and testing patterns
version: 1.0.0
---

# Advanced GetX Patterns

Advanced GetX patterns for building sophisticated reactive applications with proper state management, dependency injection, and network communication.

## Workers - Reactive Side Effects

Workers allow you to execute callbacks when observable values change.

### ever - Execute on Every Change

```dart
class UserController extends GetxController {
  final user = Rx<User?>(null);
  final isAuthenticated = false.obs;

  @override
  void onInit() {
    super.onInit();

    // Execute callback every time user changes
    ever(user, (User? userData) {
      if (userData != null) {
        print('User logged in: ${userData.name}');
        isAuthenticated.value = true;
      } else {
        print('User logged out');
        isAuthenticated.value = false;
      }
    });
  }
}
```

### once - Execute Only Once

```dart
class OnboardingController extends GetxController {
  final hasCompletedOnboarding = false.obs;

  @override
  void onInit() {
    super.onInit();

    // Execute only the first time value becomes true
    once(hasCompletedOnboarding, (_) {
      Get.offAllNamed(AppRoutes.home);
      // This won't run again even if value changes back to false and then true
    });
  }
}
```

### debounce - Delay Execution

```dart
class SearchController extends GetxController {
  final searchQuery = ''.obs;
  final searchResults = <Product>[].obs;
  final isSearching = false.obs;

  @override
  void onInit() {
    super.onInit();

    // Wait 800ms after user stops typing before searching
    debounce(
      searchQuery,
      (_) => performSearch(),
      time: const Duration(milliseconds: 800),
    );
  }

  Future<void> performSearch() async {
    if (searchQuery.value.isEmpty) {
      searchResults.clear();
      return;
    }

    isSearching.value = true;
    final result = await repository.search(searchQuery.value);
    result.fold(
      (failure) => searchResults.clear(),
      (products) => searchResults.value = products,
    );
    isSearching.value = false;
  }
}
```

### interval - Execute Periodically

```dart
class DashboardController extends GetxController {
  final stats = Rx<DashboardStats?>(null);

  @override
  void onInit() {
    super.onInit();

    // Refresh stats every 30 seconds while value changes
    interval(
      stats,
      (_) => refreshStats(),
      time: const Duration(seconds: 30),
    );

    // Initial load
    refreshStats();
  }

  Future<void> refreshStats() async {
    final result = await repository.getStats();
    result.fold(
      (failure) => {},
      (data) => stats.value = data,
    );
  }
}
```

### Worker Best Practices

```dart
class MyController extends GetxController {
  final count = 0.obs;
  Worker? _countWorker;

  @override
  void onInit() {
    super.onInit();

    // Store worker reference for manual disposal
    _countWorker = ever(count, (value) {
      print('Count changed to: $value');
    });
  }

  @override
  void onClose() {
    // Dispose worker manually if needed
    _countWorker?.dispose();
    super.onClose();
  }
}
```

## GetxService - Permanent Services

GetxService instances are never disposed, perfect for app-wide services.

### Creating a Service

```dart
import 'package:get/get.dart';

class AuthService extends GetxService {
  final _isAuthenticated = false.obs;
  bool get isAuthenticated => _isAuthenticated.value;

  final _currentUser = Rx<User?>(null);
  User? get currentUser => _currentUser.value;

  // Called when service is first created
  @override
  Future<void> onInit() async {
    super.onInit();
    await _loadSavedAuth();
  }

  Future<void> _loadSavedAuth() async {
    final storage = Get.find<GetStorage>();
    final token = storage.read<String>('auth_token');
    if (token != null) {
      await validateToken(token);
    }
  }

  Future<void> login(String email, String password) async {
    final result = await repository.login(email, password);
    result.fold(
      (failure) => throw Exception(failure.message),
      (user) {
        _currentUser.value = user;
        _isAuthenticated.value = true;
        Get.find<GetStorage>().write('auth_token', user.token);
      },
    );
  }

  void logout() {
    _currentUser.value = null;
    _isAuthenticated.value = false;
    Get.find<GetStorage>().remove('auth_token');
  }

  @override
  void onClose() {
    // GetxService onClose is never called
    // Service persists throughout app lifecycle
    super.onClose();
  }
}
```

### Registering Services

```dart
// In main.dart or dependency injection setup
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await GetStorage.init();

  // Register permanent services
  Get.putAsync(() => AuthService().init(), permanent: true);
  Get.put(ThemeService(), permanent: true);
  Get.put(LocalizationService(), permanent: true);

  runApp(MyApp());
}

// With async initialization
class AuthService extends GetxService {
  Future<AuthService> init() async {
    await _loadSavedAuth();
    return this;
  }
}
```

## SmartManagement - Lifecycle Control

Control how GetX manages controller lifecycle.

### SmartManagement Modes

```dart
void main() {
  runApp(
    GetMaterialApp(
      smartManagement: SmartManagement.full, // Default
      home: HomePage(),
    ),
  );
}
```

**SmartManagement.full** (Default):
- Disposes controllers when routes are closed
- Most memory efficient
- Recommended for most apps

**SmartManagement.onlyBuilder**:
- Only disposes controllers created with `GetBuilder`
- `Get.find()` instances persist
- Use when you need manual control

**SmartManagement.keepFactory**:
- Keeps factory instances
- Controllers can be recreated with same dependencies
- Use for complex dependency graphs

### Manual Controller Disposal

```dart
class ManualController extends GetxController {
  // This controller won't auto-dispose
}

// Register without auto-dispose
Get.put(ManualController(), permanent: true);

// Manually dispose when needed
Get.delete<ManualController>();

// Or with tag
Get.put(ManualController(), tag: 'unique-tag');
Get.delete<ManualController>(tag: 'unique-tag');
```

## GetConnect - HTTP Client

GetConnect provides a powerful HTTP client with interceptors and base URL configuration.

### Basic Setup

```dart
class ApiProvider extends GetConnect {
  @override
  void onInit() {
    // Base URL
    httpClient.baseUrl = 'https://api.example.com';

    // Default timeout
    httpClient.timeout = const Duration(seconds: 30);

    // Request interceptor
    httpClient.addRequestModifier<dynamic>((request) {
      // Add auth token to all requests
      final token = Get.find<AuthService>().token;
      if (token != null) {
        request.headers['Authorization'] = 'Bearer $token';
      }
      request.headers['Content-Type'] = 'application/json';
      return request;
    });

    // Response interceptor
    httpClient.addResponseModifier((request, response) {
      // Log responses in debug mode
      if (kDebugMode) {
        print('Response: ${response.statusCode} ${response.bodyString}');
      }
      return response;
    });

    // Auth interceptor
    httpClient.addAuthenticator<dynamic>((request) async {
      // Refresh token if 401
      final token = await refreshToken();
      request.headers['Authorization'] = 'Bearer $token';
      return request;
    });
  }

  // GET request
  Future<Response<List<Product>>> getProducts() {
    return get<List<Product>>(
      '/products',
      decoder: (data) => (data as List)
          .map((item) => Product.fromJson(item))
          .toList(),
    );
  }

  // POST request
  Future<Response<User>> createUser(User user) {
    return post<User>(
      '/users',
      user.toJson(),
      decoder: (data) => User.fromJson(data),
    );
  }

  // PUT request
  Future<Response<User>> updateUser(String id, User user) {
    return put<User>(
      '/users/$id',
      user.toJson(),
      decoder: (data) => User.fromJson(data),
    );
  }

  // DELETE request
  Future<Response> deleteUser(String id) {
    return delete('/users/$id');
  }
}
```

### Using GetConnect in Repository

```dart
class UserRepositoryImpl implements UserRepository {
  final ApiProvider apiProvider;

  UserRepositoryImpl({required this.apiProvider});

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    try {
      final response = await apiProvider.get<List<User>>(
        '/users',
        decoder: (data) => (data as List)
            .map((json) => User.fromJson(json))
            .toList(),
      );

      if (response.hasError) {
        return Left(ServerFailure(response.statusText ?? 'Unknown error'));
      }

      return Right(response.body!);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
```

## Bindings Composition

Combine multiple bindings for complex features.

### Creating Bindings

```dart
// Feature binding
class ProductBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => ProductRemoteDataSource(api: Get.find()));
    Get.lazyPut(() => ProductLocalDataSource(storage: Get.find()));
    Get.lazyPut<ProductRepository>(
      () => ProductRepositoryImpl(
        remoteDataSource: Get.find(),
        localDataSource: Get.find(),
      ),
    );
    Get.lazyPut(() => GetProducts(repository: Get.find()));
    Get.lazyPut(() => ProductController(getProducts: Get.find()));
  }
}

// Another feature binding
class CartBinding extends Bindings {
  @override
  void dependencies() {
    Get.lazyPut(() => CartLocalDataSource(storage: Get.find()));
    Get.lazyPut<CartRepository>(
      () => CartRepositoryImpl(localDataSource: Get.find()),
    );
    Get.lazyPut(() => AddToCart(repository: Get.find()));
    Get.lazyPut(() => RemoveFromCart(repository: Get.find()));
    Get.lazyPut(() => CartController(
      addToCart: Get.find(),
      removeFromCart: Get.find(),
    ));
  }
}

// Combine bindings
class ProductDetailsBinding extends Bindings {
  @override
  void dependencies() {
    // Register product dependencies
    ProductBinding().dependencies();
    // Register cart dependencies
    CartBinding().dependencies();
    // Register page-specific controller
    Get.lazyPut(() => ProductDetailsController(
      product: Get.find(),
      cart: Get.find(),
    ));
  }
}
```

### Using BindingsBuilder

```dart
GetPage(
  name: '/checkout',
  page: () => CheckoutPage(),
  binding: BindingsBuilder(() {
    // Quick inline bindings
    Get.lazyPut(() => CheckoutController());
    Get.lazyPut(() => PaymentService());
    Get.lazyPut(() => ShippingService());
  }),
)

// Or with multiple bindings
GetPage(
  name: '/checkout',
  page: () => CheckoutPage(),
  bindings: [
    CartBinding(),
    PaymentBinding(),
    ShippingBinding(),
  ],
)
```

## Rx Advanced Patterns

### Custom Rx Classes

```dart
class RxUser extends Rx<User> {
  RxUser(User initial) : super(initial);

  String get fullName => value.firstName + ' ' + value.lastName;

  bool get isAdmin => value.role == 'admin';

  void updateEmail(String email) {
    value = value.copyWith(email: email);
  }
}

// Usage
final user = RxUser(User(firstName: 'John', lastName: 'Doe'));
user.updateEmail('john@example.com');
```

### Rx Transformations

```dart
class DataController extends GetxController {
  final rawData = <Item>[].obs;

  // Computed observable
  List<Item> get filteredData => rawData.where((item) => item.isActive).toList();

  // Or use Rx.map
  late final activeItems = rawData.map((data) =>
      data.where((item) => item.isActive).toList()
  ).obs;
}
```

## GetQueue - Background Tasks

```dart
class UploadQueue extends GetxService {
  final _queue = <UploadTask>[].obs;

  void addTask(UploadTask task) {
    _queue.add(task);
    processQueue();
  }

  Future<void> processQueue() async {
    while (_queue.isNotEmpty) {
      final task = _queue.first;
      try {
        await _uploadFile(task);
        _queue.removeAt(0);
      } catch (e) {
        // Retry logic
        task.retryCount++;
        if (task.retryCount >= 3) {
          _queue.removeAt(0); // Give up after 3 retries
        } else {
          await Future.delayed(Duration(seconds: task.retryCount * 2));
        }
      }
    }
  }

  Future<void> _uploadFile(UploadTask task) async {
    // Upload logic
  }
}
```

## Testing GetX Controllers

### Unit Testing

```dart
void main() {
  late ProductController controller;
  late MockGetProducts mockGetProducts;

  setUp(() {
    mockGetProducts = MockGetProducts();
    controller = ProductController(getProducts: mockGetProducts);
  });

  tearDown(() {
    controller.dispose();
  });

  test('loads products successfully', () async {
    // Arrange
    final products = [Product(id: '1', name: 'Product 1')];
    when(() => mockGetProducts())
        .thenAnswer((_) async => Right(products));

    // Act
    await controller.loadProducts();

    // Assert
    expect(controller.products, products);
    expect(controller.isLoading, false);
    verify(() => mockGetProducts()).called(1);
  });

  test('handles failure when loading products', () async {
    // Arrange
    when(() => mockGetProducts())
        .thenAnswer((_) async => Left(ServerFailure('Error')));

    // Act
    await controller.loadProducts();

    // Assert
    expect(controller.products, isEmpty);
    expect(controller.error, isNotNull);
    expect(controller.isLoading, false);
  });
}
```

### Widget Testing with GetX

```dart
testWidgets('displays products when loaded', (tester) async {
  // Mock controller
  final controller = ProductController(getProducts: mockGetProducts);
  Get.put(controller);

  // Pump widget
  await tester.pumpWidget(
    GetMaterialApp(
      home: ProductListPage(),
    ),
  );

  // Simulate loading
  controller.products.value = [Product(id: '1', name: 'Product 1')];
  await tester.pumpAndSettle();

  // Assert
  expect(find.text('Product 1'), findsOneWidget);

  // Cleanup
  Get.delete<ProductController>();
});
```

## Best Practices

1. **Workers**:
   - Use `debounce` for search inputs (800ms delay)
   - Use `ever` for side effects (analytics, navigation)
   - Use `once` for one-time actions (onboarding)
   - Use `interval` for periodic updates (30s+)
   - Always dispose workers in `onClose()`

2. **GetxService**:
   - Use for app-wide services (Auth, Theme, Localization)
   - Register with `permanent: true`
   - Initialize async operations in `init()` method
   - Services should be stateless or immutable where possible

3. **SmartManagement**:
   - Stick with `SmartManagement.full` (default) for most apps
   - Only change if you have specific memory management needs
   - Document why you're using non-default management

4. **GetConnect**:
   - Create one `GetConnect` instance per API
   - Use interceptors for auth, logging, error handling
   - Implement retry logic in `addAuthenticator`
   - Handle errors consistently in repositories

5. **Bindings**:
   - One binding per feature/route
   - Use `lazyPut` for dependencies (loaded when first used)
   - Use `put` for singletons needed immediately
   - Compose bindings for complex features

6. **Testing**:
   - Always dispose controllers in `tearDown()`
   - Use `Get.reset()` to clear all dependencies between tests
   - Mock use cases, not repositories
   - Test reactive state changes with `pumpAndSettle()`
