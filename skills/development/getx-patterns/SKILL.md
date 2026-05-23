---
name: "GetX State Management Patterns"
description: "GetX controllers, reactive state, dependency injection, bindings, navigation, and best practices"
version: "1.0.0"
---

# GetX State Management Patterns

## Reactive State Management

### Reactive Variables
```dart
class UserController extends GetxController {
  // Simple reactive variable
  final count = 0.obs;
  
  // Complex reactive variable
  final user = Rx<User?>(null);
  
  // Reactive list
  final users = <User>[].obs;
  
  // Reactive map
  final settings = <String, dynamic>{}.obs;
  
  // Getters (recommended)
  int get countValue => count.value;
  User? get currentUser => user.value;
}
```

### Reactive Widgets
```dart
// Option 1: Obx (lightweight)
Obx(() => Text(controller.count.toString()))

// Option 2: GetX (with dependency injection)
GetX<UserController>(
  builder: (controller) => Text(controller.user?.name ?? 'Loading...'),
)

// Option 3: GetBuilder (no reactive variables needed)
GetBuilder<UserController>(
  builder: (controller) => Text(controller.userName),
)
```

## Dependency Injection

### Registration Methods
```dart
// Immediate instance
Get.put(UserController());

// Lazy instance (created when first used)
Get.lazyPut(() => UserController());

// Singleton (persists across routes)
Get.putAsync(() => StorageService().init());

// Fenix (recreates when route is accessed again)
Get.lazyPut(() => UserController(), fenix: true);
```

### Bindings Pattern
```dart
class UserBinding extends Bindings {
  @override
  void dependencies() {
    // Data sources
    Get.lazyPut(() => UserProvider(Get.find()));
    Get.lazyPut(() => UserLocalSource(Get.find()));
    
    // Repository
    Get.lazyPut<UserRepository>(
      () => UserRepositoryImpl(Get.find(), Get.find()),
    );
    
    // Use cases
    Get.lazyPut(() => GetUser(Get.find()));
    
    // Controller
    Get.lazyPut(() => UserController(getUserUseCase: Get.find()));
  }
}
```

## Navigation

### Basic Navigation
```dart
// Navigate to route
Get.to(() => ProfilePage());

// Navigate with name
Get.toNamed('/profile');

// Navigate and remove previous
Get.off(() => LoginPage());

// Navigate and remove all previous
Get.offAll(() => HomePage());

// Go back
Get.back();

// Go back with result
Get.back(result: user);
```

### Navigation with Arguments
```dart
// Send arguments
Get.toNamed('/profile', arguments: {'id': '123'});

// Receive arguments
final args = Get.arguments as Map<String, dynamic>;
final id = args['id'];
```

### Route Configuration
```dart
class AppRoutes {
  static const initial = '/splash';
  
  static final routes = [
    GetPage(
      name: '/splash',
      page: () => SplashPage(),
      binding: SplashBinding(),
    ),
    GetPage(
      name: '/login',
      page: () => LoginPage(),
      binding: AuthBinding(),
      transition: Transition.fadeIn,
    ),
    GetPage(
      name: '/home',
      page: () => HomePage(),
      binding: HomeBinding(),
      middlewares: [AuthMiddleware()],
    ),
  ];
}
```

## Controller Lifecycle

```dart
class UserController extends GetxController {
  @override
  void onInit() {
    super.onInit();
    // Called immediately after controller is allocated
    loadUser();
  }
  
  @override
  void onReady() {
    super.onReady();
    // Called after widget is rendered
    analytics.logScreenView();
  }
  
  @override
  void onClose() {
    // Clean up resources
    _subscription.cancel();
    super.onClose();
  }
}
```

## Snackbars & Dialogs

```dart
// Snackbar
Get.snackbar(
  'Success',
  'User created successfully',
  snackPosition: SnackPosition.BOTTOM,
  backgroundColor: Colors.green,
);

// Dialog
Get.dialog(
  AlertDialog(
    title: Text('Confirm'),
    content: Text('Are you sure?'),
    actions: [
      TextButton(
        onPressed: () => Get.back(),
        child: Text('Cancel'),
      ),
      TextButton(
        onPressed: () {
          deleteUser();
          Get.back();
        },
        child: Text('Delete'),
      ),
    ],
  ),
);

// Bottom sheet
Get.bottomSheet(
  Container(
    child: Column(
      children: [
        ListTile(
          title: Text('Option 1'),
          onTap: () => Get.back(result: 1),
        ),
      ],
    ),
  ),
);
```

## Best Practices

### ✅ DO
- Use bindings for dependency injection
- Use private reactive variables with public getters
- Clean up resources in `onClose()`
- Use meaningful controller names (e.g., `UserController`, not `Controller1`)
- Keep business logic in use cases, not controllers

### ❌ DON'T
- Don't create controllers directly in widgets
- Don't put business logic in controllers
- Don't forget to dispose streams and subscriptions
- Don't use global state excessively
- Don't create circular dependencies

## Anti-Patterns to Avoid

```dart
// ❌ BAD: Business logic in controller
class UserController extends GetxController {
  Future<void> createUser(String name, String email) async {
    // Direct API call in controller
    final response = await http.post(...);
    // Business logic in controller
    if (response.statusCode == 201) {
      user.value = User.fromJson(response.body);
    }
  }
}

// ✅ GOOD: Delegate to use case
class UserController extends GetxController {
  final CreateUser createUserUseCase;
  
  Future<void> createUser(String name, String email) async {
    final result = await createUserUseCase(name, email);
    result.fold(
      (failure) => _handleError(failure),
      (user) => user.value = user,
    );
  }
}
```
