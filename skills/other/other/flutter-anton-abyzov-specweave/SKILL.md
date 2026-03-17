---
description: Flutter and Dart 3+ expert for cross-platform mobile development. Covers widget composition, Riverpod state management, GoRouter navigation, platform channels, local storage, networking, testing strategies, build/deployment, performance profiling, theming, accessibility, FFI, and architecture patterns. Use for Flutter projects.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# Flutter Expert - Cross-Platform Development with Dart 3+

Comprehensive Flutter expertise for building production-grade cross-platform applications targeting iOS, Android, Web, macOS, Windows, and Linux. Covers the latest Dart 3+ language features and Flutter best practices.

## Project Setup

### Creating a New Flutter Project

```bash
# Create project with organization identifier
flutter create --org com.example --platforms ios,android,web my_app
cd my_app

# Recommended project structure (feature-first)
lib/
├── main.dart
├── app.dart                          # MaterialApp / GoRouter setup
├── core/
│   ├── constants/
│   │   ├── app_colors.dart
│   │   ├── app_strings.dart
│   │   └── api_endpoints.dart
│   ├── extensions/
│   │   ├── context_extensions.dart
│   │   └── string_extensions.dart
│   ├── theme/
│   │   ├── app_theme.dart
│   │   └── text_styles.dart
│   ├── network/
│   │   ├── dio_client.dart
│   │   ├── api_interceptor.dart
│   │   └── api_exceptions.dart
│   ├── storage/
│   │   └── local_storage.dart
│   └── utils/
│       ├── logger.dart
│       └── validators.dart
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── repositories/
│   │   │   └── models/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── screens/
│   │       ├── widgets/
│   │       └── providers/
│   ├── home/
│   └── profile/
├── shared/
│   ├── widgets/
│   │   ├── app_button.dart
│   │   ├── loading_indicator.dart
│   │   └── error_widget.dart
│   └── providers/
│       └── common_providers.dart
test/
├── unit/
├── widget/
├── golden/
└── integration/
```

### pubspec.yaml Essentials

```yaml
name: my_app
description: A production Flutter application.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.5.0 <4.0.0'
  flutter: '>=3.24.0'

dependencies:
  flutter:
    sdk: flutter

  # State management
  flutter_riverpod: ^2.6.1
  riverpod_annotation: ^2.6.1

  # Navigation
  go_router: ^14.6.2

  # Networking
  dio: ^5.7.0
  retrofit: ^4.4.1

  # Local storage
  hive_ce: ^2.7.0
  hive_ce_flutter: ^2.2.0
  shared_preferences: ^2.3.4

  # Serialization
  freezed_annotation: ^2.4.6
  json_annotation: ^4.9.0

  # UI
  flutter_screenutil: ^5.9.3
  cached_network_image: ^3.4.1
  shimmer: ^3.0.0

  # Utilities
  intl: ^0.19.0
  logger: ^2.5.0
  equatable: ^2.0.7

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
  build_runner: ^2.4.13
  freezed: ^2.5.7
  json_serializable: ^6.8.0
  riverpod_generator: ^2.6.3
  retrofit_generator: ^9.1.7
  mockito: ^5.4.4
  mocktail: ^1.0.4
  patrol: ^3.13.0
  golden_toolkit: ^0.15.0
```

## Dart 3+ Language Features

### Records and Patterns

```dart
// Records - lightweight data structures
(String name, int age) getUserInfo() {
  return ('Alice', 30);
}

// Destructuring records
final (name, age) = getUserInfo();

// Named records
({String city, String country}) getLocation() {
  return (city: 'Berlin', country: 'Germany');
}

// Pattern matching in switch expressions
String describeValue(Object value) => switch (value) {
  int n when n < 0 => 'negative',
  int n when n == 0 => 'zero',
  int() => 'positive integer',
  String s when s.isEmpty => 'empty string',
  String() => 'non-empty string',
  List(isEmpty: true) => 'empty list',
  List(length: final len) => 'list of $len items',
  _ => 'unknown',
};

// If-case with patterns
void processResponse(Map<String, dynamic> json) {
  if (json case {'status': 'ok', 'data': final List items}) {
    for (final item in items) {
      processItem(item);
    }
  }
}
```

### Sealed Classes and Class Modifiers

```dart
// Sealed classes for exhaustive pattern matching
sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  final User user;
  AuthAuthenticated(this.user);
}
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}

// Exhaustive switch (compiler enforces all cases)
Widget buildAuthUI(AuthState state) => switch (state) {
  AuthInitial() => const LoginScreen(),
  AuthLoading() => const LoadingScreen(),
  AuthAuthenticated(:final user) => HomeScreen(user: user),
  AuthError(:final message) => ErrorScreen(message: message),
};

// Class modifiers
final class DatabaseConfig {          // Cannot be extended or implemented
  final String host;
  final int port;
  const DatabaseConfig({required this.host, required this.port});
}

interface class Logger {              // Can only be implemented, not extended
  void log(String message);
}

base class Repository {               // Can be extended but not implemented
  void save(Object entity) { /* ... */ }
}

mixin class Trackable {               // Can be used as both mixin and class
  void track(String event) { /* ... */ }
}
```

### Freezed Data Classes

```dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:json_annotation/json_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatarUrl,
    @Default(false) bool isVerified,
    @Default([]) List<String> roles,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Usage - immutable with copyWith
final user = User(id: '1', name: 'Alice', email: 'alice@example.com');
final updated = user.copyWith(name: 'Alice Smith', isVerified: true);
```

## Widget Composition

### Custom Widgets

```dart
class AppCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final EdgeInsetsGeometry padding;
  final double borderRadius;

  const AppCard({
    super.key,
    required this.child,
    this.onTap,
    this.padding = const EdgeInsets.all(16),
    this.borderRadius = 12,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Material(
      borderRadius: BorderRadius.circular(borderRadius),
      elevation: 2,
      color: theme.colorScheme.surface,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(borderRadius),
        child: Padding(
          padding: padding,
          child: child,
        ),
      ),
    );
  }
}
```

### Sliver-Based Scrollable Layouts

```dart
class ProfileScreen extends StatelessWidget {
  final User user;
  const ProfileScreen({super.key, required this.user});

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        SliverAppBar(
          expandedHeight: 250,
          pinned: true,
          flexibleSpace: FlexibleSpaceBar(
            title: Text(user.name),
            background: CachedNetworkImage(
              imageUrl: user.coverUrl,
              fit: BoxFit.cover,
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: ProfileHeader(user: user),
        ),
        SliverPadding(
          padding: const EdgeInsets.all(16),
          sliver: SliverGrid.builder(
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 3,
              mainAxisSpacing: 4,
              crossAxisSpacing: 4,
            ),
            itemCount: user.photos.length,
            itemBuilder: (context, index) => PhotoThumbnail(photo: user.photos[index]),
          ),
        ),
      ],
    );
  }
}
```

## State Management with Riverpod

### Provider Types

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'providers.g.dart';

// Simple provider (auto-disposed by default with codegen)
@riverpod
String appVersion(Ref ref) => '1.0.0';

// FutureProvider for async data
@riverpod
Future<List<Product>> products(Ref ref) async {
  final repository = ref.watch(productRepositoryProvider);
  return repository.getAll();
}

// Notifier for mutable state
@riverpod
class CartNotifier extends _$CartNotifier {
  @override
  List<CartItem> build() => [];

  void addItem(Product product) {
    state = [
      ...state,
      CartItem(product: product, quantity: 1),
    ];
  }

  void removeItem(String productId) {
    state = state.where((item) => item.product.id != productId).toList();
  }

  double get totalPrice =>
      state.fold(0, (sum, item) => sum + item.product.price * item.quantity);
}

// Family provider (parameterized)
@riverpod
Future<Product> productDetail(Ref ref, String id) async {
  final repository = ref.watch(productRepositoryProvider);
  return repository.getById(id);
}

// Consuming in widgets
class ProductListScreen extends ConsumerWidget {
  const ProductListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final productsAsync = ref.watch(productsProvider);

    return productsAsync.when(
      data: (products) => ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) => ProductTile(product: products[index]),
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => Center(child: Text('Error: $error')),
    );
  }
}
```

### State Management Decision Framework

| Criteria | Riverpod | BLoC | Provider |
|----------|----------|------|----------|
| Learning curve | Medium | Higher | Low |
| Testability | Excellent | Excellent | Good |
| Compile-time safety | Yes (codegen) | Partial | No |
| DevTools support | Yes | Yes | Limited |
| Code generation | Recommended | Optional | No |
| Complex async flows | Great | Best (streams) | Adequate |
| Team size | Any | Large teams | Small teams |
| Recommendation | Default choice | Event-driven apps | Simple apps only |

## Navigation with GoRouter

```dart
import 'package:go_router/go_router.dart';

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authNotifierProvider);

  return GoRouter(
    initialLocation: '/',
    debugLogDiagnostics: true,
    redirect: (context, state) {
      final isLoggedIn = authState is AuthAuthenticated;
      final isLoginRoute = state.matchedLocation == '/login';

      if (!isLoggedIn && !isLoginRoute) return '/login';
      if (isLoggedIn && isLoginRoute) return '/';
      return null;
    },
    routes: [
      ShellRoute(
        builder: (context, state, child) => AppScaffold(child: child),
        routes: [
          GoRoute(
            path: '/',
            name: 'home',
            builder: (context, state) => const HomeScreen(),
          ),
          GoRoute(
            path: '/products/:id',
            name: 'product-detail',
            builder: (context, state) {
              final id = state.pathParameters['id']!;
              return ProductDetailScreen(productId: id);
            },
          ),
          GoRoute(
            path: '/profile',
            name: 'profile',
            builder: (context, state) => const ProfileScreen(),
            routes: [
              GoRoute(
                path: 'settings',
                name: 'settings',
                builder: (context, state) => const SettingsScreen(),
              ),
            ],
          ),
        ],
      ),
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
    ],
  );
});

// Navigation usage
context.go('/products/abc123');
context.goNamed('product-detail', pathParameters: {'id': 'abc123'});
context.push('/products/abc123');  // Push onto stack (preserves back navigation)
```

## Platform Channels and Native Interop

```dart
// Method channel for platform-specific code
class BatteryService {
  static const _channel = MethodChannel('com.example.app/battery');

  Future<int> getBatteryLevel() async {
    try {
      final level = await _channel.invokeMethod<int>('getBatteryLevel');
      return level ?? -1;
    } on PlatformException catch (e) {
      throw BatteryException('Failed to get battery level: ${e.message}');
    }
  }
}

// Event channel for continuous streams
class SensorService {
  static const _channel = EventChannel('com.example.app/accelerometer');

  Stream<AccelerometerData> get accelerometerStream {
    return _channel.receiveBroadcastStream().map((event) {
      final data = event as Map<dynamic, dynamic>;
      return AccelerometerData(
        x: data['x'] as double,
        y: data['y'] as double,
        z: data['z'] as double,
      );
    });
  }
}

// Pigeon for type-safe platform channels (recommended for complex APIs)
// See: https://pub.dev/packages/pigeon
```

## Local Storage

### Choosing the Right Storage

| Solution | Use Case | Async | Typed | Query |
|----------|----------|-------|-------|-------|
| shared_preferences | Simple key-value (settings) | Yes | Partial | No |
| Hive CE | Fast NoSQL, offline-first | Yes | Yes | Basic |
| Isar | Full-featured NoSQL DB | Yes | Yes | Full |
| Drift | Type-safe SQL (SQLite) | Yes | Yes | Full SQL |
| sqflite | Raw SQLite access | Yes | No | Raw SQL |

### Hive CE Example

```dart
import 'package:hive_ce/hive_ce.dart';
import 'package:hive_ce_flutter/hive_ce_flutter.dart';

// Adapter (generate with build_runner or write manually)
@HiveType(typeId: 0)
class CachedProduct extends HiveObject {
  @HiveField(0)
  final String id;
  @HiveField(1)
  final String name;
  @HiveField(2)
  final double price;
  @HiveField(3)
  final DateTime cachedAt;

  CachedProduct({
    required this.id,
    required this.name,
    required this.price,
    required this.cachedAt,
  });
}

// Initialization
Future<void> initStorage() async {
  await Hive.initFlutter();
  Hive.registerAdapter(CachedProductAdapter());
  await Hive.openBox<CachedProduct>('products');
}

// Repository
class ProductCacheRepository {
  Box<CachedProduct> get _box => Hive.box<CachedProduct>('products');

  List<CachedProduct> getAll() => _box.values.toList();

  Future<void> cacheProducts(List<CachedProduct> products) async {
    final map = {for (final p in products) p.id: p};
    await _box.putAll(map);
  }

  Future<void> clear() async => _box.clear();
}
```

## Networking with Dio

```dart
import 'package:dio/dio.dart';

class DioClient {
  late final Dio _dio;

  DioClient({required String baseUrl, required TokenStorage tokenStorage}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
      headers: {'Content-Type': 'application/json'},
    ));

    _dio.interceptors.addAll([
      _AuthInterceptor(tokenStorage),
      _LoggingInterceptor(),
      _RetryInterceptor(dio: _dio),
    ]);
  }

  Dio get dio => _dio;
}

class _AuthInterceptor extends Interceptor {
  final TokenStorage _tokenStorage;
  _AuthInterceptor(this._tokenStorage);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final token = _tokenStorage.accessToken;
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (err.response?.statusCode == 401) {
      try {
        await _tokenStorage.refreshToken();
        final retryResponse = await _retryRequest(err.requestOptions);
        handler.resolve(retryResponse);
        return;
      } catch (_) {
        _tokenStorage.clearTokens();
      }
    }
    handler.next(err);
  }
}
```

## Testing

### Widget Tests

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mocktail/mocktail.dart';

class MockProductRepository extends Mock implements ProductRepository {}

void main() {
  group('ProductListScreen', () {
    late MockProductRepository mockRepo;

    setUp(() {
      mockRepo = MockProductRepository();
    });

    testWidgets('displays loading indicator initially', (tester) async {
      when(() => mockRepo.getAll()).thenAnswer(
        (_) async => Future.delayed(const Duration(seconds: 1), () => []),
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productRepositoryProvider.overrideWithValue(mockRepo),
          ],
          child: const MaterialApp(home: ProductListScreen()),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('displays products after loading', (tester) async {
      when(() => mockRepo.getAll()).thenAnswer(
        (_) async => [
          Product(id: '1', name: 'Widget A', price: 9.99),
          Product(id: '2', name: 'Widget B', price: 19.99),
        ],
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productRepositoryProvider.overrideWithValue(mockRepo),
          ],
          child: const MaterialApp(home: ProductListScreen()),
        ),
      );

      await tester.pumpAndSettle();
      expect(find.text('Widget A'), findsOneWidget);
      expect(find.text('Widget B'), findsOneWidget);
    });

    testWidgets('shows error message on failure', (tester) async {
      when(() => mockRepo.getAll()).thenThrow(Exception('Network error'));

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            productRepositoryProvider.overrideWithValue(mockRepo),
          ],
          child: const MaterialApp(home: ProductListScreen()),
        ),
      );

      await tester.pumpAndSettle();
      expect(find.textContaining('Error'), findsOneWidget);
    });
  });
}
```

### Golden Tests

```dart
import 'package:golden_toolkit/golden_toolkit.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('ProductCard Golden Tests', () {
    testGoldens('renders correctly on different devices', (tester) async {
      final builder = DeviceBuilder()
        ..overrideDevicesForAllScenarios(devices: [
          Device.phone,
          Device.iphone11,
          Device.tabletLandscape,
        ])
        ..addScenario(
          name: 'default',
          widget: ProductCard(
            product: Product(id: '1', name: 'Test', price: 9.99),
          ),
        )
        ..addScenario(
          name: 'long name',
          widget: ProductCard(
            product: Product(
              id: '2',
              name: 'Very Long Product Name That Should Wrap',
              price: 199.99,
            ),
          ),
        );

      await tester.pumpDeviceBuilder(builder);
      await screenMatchesGolden(tester, 'product_card_variants');
    });
  });
}
```

### Integration Tests with Patrol

```dart
// integration_test/app_test.dart
import 'package:patrol/patrol.dart';

void main() {
  patrolTest('user can browse products and add to cart', ($) async {
    await $.pumpWidgetAndSettle(const MyApp());

    // Navigate to products
    await $(#productsTab).tap();
    await $.pumpAndSettle();

    // Verify product list loaded
    expect($('Product A'), findsOneWidget);

    // Tap first product
    await $('Product A').tap();
    await $.pumpAndSettle();

    // Add to cart
    await $(#addToCartButton).tap();
    await $.pumpAndSettle();

    // Verify cart badge
    expect($(#cartBadge).text, equals('1'));

    // Navigate to cart
    await $(#cartTab).tap();
    await $.pumpAndSettle();

    expect($('Product A'), findsOneWidget);
    expect($('\$9.99'), findsOneWidget);
  });
}
```

## Build and Deployment

### Flavors (Build Variants)

```dart
// lib/core/config/app_config.dart
enum Flavor { dev, staging, production }

class AppConfig {
  final Flavor flavor;
  final String apiBaseUrl;
  final bool enableLogging;

  const AppConfig._({
    required this.flavor,
    required this.apiBaseUrl,
    required this.enableLogging,
  });

  static late final AppConfig instance;

  static void init(Flavor flavor) {
    instance = switch (flavor) {
      Flavor.dev => const AppConfig._(
        flavor: Flavor.dev,
        apiBaseUrl: 'https://api-dev.example.com',
        enableLogging: true,
      ),
      Flavor.staging => const AppConfig._(
        flavor: Flavor.staging,
        apiBaseUrl: 'https://api-staging.example.com',
        enableLogging: true,
      ),
      Flavor.production => const AppConfig._(
        flavor: Flavor.production,
        apiBaseUrl: 'https://api.example.com',
        enableLogging: false,
      ),
    };
  }
}

// lib/main_dev.dart
void main() {
  AppConfig.init(Flavor.dev);
  runApp(const MyApp());
}

// lib/main_production.dart
void main() {
  AppConfig.init(Flavor.production);
  runApp(const MyApp());
}
```

```bash
# Running flavors
flutter run --target lib/main_dev.dart
flutter run --target lib/main_production.dart

# Building flavors
flutter build apk --target lib/main_production.dart --release
flutter build ipa --target lib/main_production.dart --release
```

## Performance Profiling

### Key Metrics and Tools

```bash
# Run in profile mode for accurate performance data
flutter run --profile

# Open DevTools
flutter pub global activate devtools
dart devtools
```

### Performance Best Practices

```dart
// Use const constructors wherever possible
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});  // const constructor

  @override
  Widget build(BuildContext context) {
    return const Column(       // const widget tree
      children: [
        Text('Static text'),
        Icon(Icons.star),
      ],
    );
  }
}

// RepaintBoundary for isolated repaints
RepaintBoundary(
  child: AnimatedWidget(animation: controller),
)

// Avoid rebuilding expensive widgets
class ExpensiveListScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Only watch what you need - use select() to narrow rebuilds
    final itemCount = ref.watch(
      cartNotifierProvider.select((cart) => cart.length),
    );
    return Text('Items: $itemCount');
  }
}

// Image optimization
CachedNetworkImage(
  imageUrl: url,
  maxWidthDiskCache: 800,   // Resize on disk cache
  memCacheWidth: 400,        // Resize in memory
  placeholder: (_, __) => const Shimmer(),
  errorWidget: (_, __, ___) => const Icon(Icons.error),
)
```

## Theming and Responsive Design

```dart
class AppTheme {
  static ThemeData light() => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF1A73E8),
      brightness: Brightness.light,
    ),
    textTheme: GoogleFonts.interTextTheme(),
    cardTheme: CardTheme(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
      filled: true,
    ),
  );

  static ThemeData dark() => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF1A73E8),
      brightness: Brightness.dark,
    ),
    textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
  );
}

// Responsive breakpoints
class Responsive extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet;
  final Widget desktop;

  const Responsive({
    super.key,
    required this.mobile,
    this.tablet,
    required this.desktop,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth >= 1200) return desktop;
        if (constraints.maxWidth >= 600) return tablet ?? desktop;
        return mobile;
      },
    );
  }
}
```

## Accessibility

```dart
class AccessibleProductCard extends StatelessWidget {
  final Product product;
  final VoidCallback onAddToCart;

  const AccessibleProductCard({
    super.key,
    required this.product,
    required this.onAddToCart,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: '${product.name}, \$${product.price}',
      hint: 'Double tap to view details',
      child: Card(
        child: Column(
          children: [
            // Exclude decorative image from semantics
            ExcludeSemantics(
              child: CachedNetworkImage(imageUrl: product.imageUrl),
            ),
            Text(
              product.name,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            Text(
              '\$${product.price.toStringAsFixed(2)}',
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            Semantics(
              button: true,
              label: 'Add ${product.name} to cart',
              child: IconButton(
                icon: const Icon(Icons.add_shopping_cart),
                onPressed: onAddToCart,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// Test accessibility
testWidgets('product card is accessible', (tester) async {
  final handle = tester.ensureSemantics();
  await tester.pumpWidget(/* ... */);

  expect(
    tester.getSemantics(find.byType(AccessibleProductCard)),
    matchesSemantics(label: 'Test Product, \$9.99', hasTapAction: true),
  );

  handle.dispose();
});
```

## FFI for Native Code

```dart
// Using dart:ffi for calling C/C++ code
import 'dart:ffi';
import 'dart:io';

typedef NativeAdd = Int32 Function(Int32 a, Int32 b);
typedef DartAdd = int Function(int a, int b);

class NativeMath {
  late final DartAdd _add;

  NativeMath() {
    final dylib = Platform.isAndroid
        ? DynamicLibrary.open('libnative_math.so')
        : DynamicLibrary.process();

    _add = dylib.lookupFunction<NativeAdd, DartAdd>('add_numbers');
  }

  int add(int a, int b) => _add(a, b);
}

// For complex FFI, use package:ffigen to auto-generate bindings
// flutter pub run ffigen --config ffigen.yaml
```

## Architecture Decision Framework

### Feature-First (Recommended)

```
When to choose:
- Most projects (default recommendation)
- Features are relatively independent
- Team members own entire features
- Scales well from small to large apps

Structure: lib/features/{feature}/data|domain|presentation/
```

### Layer-First

```
When to choose:
- Small apps with few features
- Heavy code sharing between features
- Team organized by specialization (frontend/backend)
- Migrating from legacy architecture

Structure: lib/data|domain|presentation/{feature}/
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| setState in large widgets | Use Riverpod/BLoC for state above widget level |
| Missing const constructors | Add `const` to all widget constructors that allow it |
| Building full widget tree on every change | Use `select()` with Riverpod or BlocSelector |
| Not disposing controllers | Use hooks (`flutter_hooks`) or dispose in State.dispose() |
| Platform-specific crashes | Always test on both iOS and Android; use `Platform.isIOS` guards |
| Slow builds | Enable Impeller, use `--no-sound-null-safety` only for debugging |
| Large image memory usage | Use `cacheWidth`/`cacheHeight` on Image widget, CachedNetworkImage |
| Hot reload not reflecting changes | Full restart (`Shift+R`) for changes to main(), providers, or native code |

## Related Skills

- `appstore` - **Recommended**: App Store Connect automation via `asc` CLI (TestFlight, submissions, metadata, signing)
- `expo` - Expo/React Native for cross-platform comparison
- `mobile-testing` - Comprehensive testing strategies
- `deep-linking-push` - Deep linking and push notification details
