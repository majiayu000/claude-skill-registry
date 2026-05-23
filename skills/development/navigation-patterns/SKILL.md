---
name: Navigation Patterns
description: GetX navigation patterns including routing, parameters, guards, deep linking, and custom transitions for Flutter applications
version: 1.0.0
---

# Navigation Patterns with GetX

Complete guide to implementing navigation in Flutter applications using GetX's powerful routing system.

## GetX Navigation Setup

### GetMaterialApp Configuration

Replace `MaterialApp` with `GetMaterialApp` to enable GetX navigation:

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'presentation/routes/app_pages.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'My App',
      initialRoute: AppRoutes.home,
      getPages: AppPages.pages,
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
    );
  }
}
```

## Route Definitions

### Define Route Constants

Create a centralized file for all route names:

```dart
// lib/presentation/routes/app_routes.dart
class AppRoutes {
  // Authentication routes
  static const login = '/login';
  static const register = '/register';
  static const forgotPassword = '/forgot-password';

  // Main app routes
  static const home = '/';
  static const profile = '/profile';
  static const settings = '/settings';

  // Feature routes with parameters
  static const productDetails = '/product/:id';
  static const userProfile = '/user/:userId';
  static const editPost = '/post/:postId/edit';

  // Nested routes
  static const dashboard = '/dashboard';
  static const dashboardHome = '/dashboard/home';
  static const dashboardStats = '/dashboard/stats';
}
```

**Naming Convention**:
- Use kebab-case for route names (`/product-details` not `/productDetails`)
- Use `:parameter` syntax for route parameters
- Group related routes with common prefixes

### Define GetPage Routes

Configure all routes with bindings and middleware:

```dart
// lib/presentation/routes/app_pages.dart
import 'package:get/get.dart';
import '../pages/home/home_page.dart';
import '../pages/home/home_binding.dart';
import '../pages/login/login_page.dart';
import '../pages/login/login_binding.dart';
import '../pages/profile/profile_page.dart';
import '../pages/profile/profile_binding.dart';
import 'app_routes.dart';
import 'middlewares/auth_middleware.dart';

class AppPages {
  static final pages = [
    // Public routes (no authentication required)
    GetPage(
      name: AppRoutes.login,
      page: () => LoginPage(),
      binding: LoginBinding(),
      transition: Transition.fadeIn,
      transitionDuration: const Duration(milliseconds: 300),
    ),
    GetPage(
      name: AppRoutes.register,
      page: () => RegisterPage(),
      binding: RegisterBinding(),
    ),

    // Protected routes (authentication required)
    GetPage(
      name: AppRoutes.home,
      page: () => HomePage(),
      binding: HomeBinding(),
      middlewares: [AuthMiddleware()],
      transition: Transition.fade,
    ),
    GetPage(
      name: AppRoutes.profile,
      page: () => ProfilePage(),
      binding: ProfileBinding(),
      middlewares: [AuthMiddleware()],
    ),

    // Routes with parameters
    GetPage(
      name: AppRoutes.productDetails,
      page: () => ProductDetailsPage(),
      binding: ProductDetailsBinding(),
      middlewares: [AuthMiddleware()],
    ),
  ];
}
```

## Navigation Methods

### Basic Navigation

```dart
// Navigate to named route
Get.toNamed(AppRoutes.profile);

// Navigate to route instance
Get.to(() => ProfilePage());

// Navigate and remove previous route
Get.off(() => HomePage());
Get.offNamed(AppRoutes.home);

// Navigate and remove all previous routes
Get.offAll(() => HomePage());
Get.offAllNamed(AppRoutes.home);

// Go back
Get.back();

// Go back with result
Get.back(result: {'success': true});
```

### Navigation with Parameters

**Route Parameters** (in URL path):
```dart
// Define route with parameter
static const productDetails = '/product/:id';

// Navigate with parameter
Get.toNamed('/product/123');

// Access parameter in controller
class ProductDetailsController extends GetxController {
  @override
  void onInit() {
    super.onInit();
    final productId = Get.parameters['id']; // '123'
  }
}
```

**Arguments** (passed separately):
```dart
// Navigate with arguments
Get.toNamed(
  AppRoutes.profile,
  arguments: {
    'userId': 123,
    'userName': 'John Doe',
    'isFollowing': true,
  },
);

// Access arguments in controller
class ProfileController extends GetxController {
  late final int userId;
  late final String userName;
  late final bool isFollowing;

  @override
  void onInit() {
    super.onInit();
    final args = Get.arguments as Map<String, dynamic>;
    userId = args['userId'];
    userName = args['userName'];
    isFollowing = args['isFollowing'];
  }
}
```

**Query Parameters**:
```dart
// Navigate with query parameters
Get.toNamed('/search?query=flutter&sort=relevance');

// Access query parameters
final query = Get.parameters['query']; // 'flutter'
final sort = Get.parameters['sort']; // 'relevance'
```

### Receiving Results from Navigation

```dart
// Navigate and await result
final result = await Get.toNamed(AppRoutes.editProfile);

if (result != null && result['updated'] == true) {
  // Profile was updated
  refreshProfile();
}

// In the destination page, return result
ElevatedButton(
  onPressed: () {
    Get.back(result: {'updated': true});
  },
  child: const Text('Save'),
)
```

## Navigation Guards (Middleware)

### Authentication Middleware

```dart
// lib/presentation/routes/middlewares/auth_middleware.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../app_routes.dart';

class AuthMiddleware extends GetMiddleware {
  @override
  int? get priority => 1; // Lower priority = higher execution order

  @override
  RouteSettings? redirect(String? route) {
    // Check if user is authenticated
    final authService = Get.find<AuthService>();

    if (!authService.isAuthenticated) {
      // Redirect to login if not authenticated
      return const RouteSettings(name: AppRoutes.login);
    }

    // Allow navigation if authenticated
    return null;
  }

  @override
  GetPage? onPageCalled(GetPage? page) {
    // Called before page is created
    // Can modify page configuration
    return page;
  }

  @override
  List<Bindings>? onBindingsStart(List<Bindings>? bindings) {
    // Called before bindings are initialized
    return bindings;
  }

  @override
  GetPageBuilder? onPageBuildStart(GetPageBuilder? page) {
    // Called before page widget is built
    return page;
  }

  @override
  Widget onPageBuilt(Widget page) {
    // Called after page widget is built
    // Can wrap page with additional widgets
    return page;
  }

  @override
  void onPageDispose() {
    // Called when page is disposed
  }
}
```

### Role-Based Access Middleware

```dart
class AdminMiddleware extends GetMiddleware {
  @override
  int? get priority => 2;

  @override
  RouteSettings? redirect(String? route) {
    final authService = Get.find<AuthService>();

    if (!authService.isAdmin) {
      // Redirect to home if not admin
      Get.snackbar(
        'Access Denied',
        'You do not have permission to access this page',
        snackPosition: SnackPosition.BOTTOM,
      );
      return const RouteSettings(name: AppRoutes.home);
    }

    return null;
  }
}
```

**Usage**:
```dart
GetPage(
  name: AppRoutes.adminPanel,
  page: () => AdminPanelPage(),
  binding: AdminBinding(),
  middlewares: [
    AuthMiddleware(),  // Check authentication first
    AdminMiddleware(), // Then check admin role
  ],
)
```

## Deep Linking

### Android Configuration

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<manifest>
  <application>
    <activity android:name=".MainActivity">
      <!-- App Links -->
      <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
          android:scheme="https"
          android:host="myapp.example.com"
          android:pathPrefix="/product" />
      </intent-filter>

      <!-- Custom URL Scheme -->
      <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="myapp" />
      </intent-filter>
    </activity>
  </application>
</manifest>
```

### iOS Configuration

```xml
<!-- ios/Runner/Info.plist -->
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleTypeRole</key>
    <string>Editor</string>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>myapp</string>
    </array>
  </dict>
</array>

<!-- Universal Links -->
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:myapp.example.com</string>
</array>
```

### Handle Deep Links in GetX

```dart
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'My App',
      initialRoute: AppRoutes.home,
      getPages: AppPages.pages,
      // Deep link will automatically match routes
      // For example: myapp://product/123 → /product/123
    );
  }
}
```

## Custom Transitions

### Built-in Transitions

```dart
GetPage(
  name: AppRoutes.profile,
  page: () => ProfilePage(),
  transition: Transition.fadeIn,
  transitionDuration: const Duration(milliseconds: 300),
)
```

**Available transitions**:
- `Transition.fade`
- `Transition.fadeIn`
- `Transition.rightToLeft`
- `Transition.leftToRight`
- `Transition.topToBottom`
- `Transition.bottomToTop`
- `Transition.rightToLeftWithFade`
- `Transition.leftToRightWithFade`
- `Transition.zoom`
- `Transition.size`
- `Transition.circularReveal`

### Custom Transition

```dart
GetPage(
  name: AppRoutes.productDetails,
  page: () => ProductDetailsPage(),
  customTransition: CustomSlideTransition(),
  transitionDuration: const Duration(milliseconds: 400),
)

class CustomSlideTransition extends CustomTransition {
  @override
  Widget buildTransition(
    BuildContext context,
    Curve? curve,
    Alignment? alignment,
    Animation<double> animation,
    Animation<double> secondaryAnimation,
    Widget child,
  ) {
    return SlideTransition(
      position: Tween<Offset>(
        begin: const Offset(1.0, 0.0),
        end: Offset.zero,
      ).animate(
        CurvedAnimation(
          parent: animation,
          curve: curve ?? Curves.easeInOut,
        ),
      ),
      child: child,
    );
  }
}
```

## Bottom Navigation with GetX

```dart
class MainPage extends StatelessWidget {
  final controller = Get.put(MainController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Obx(() => IndexedStack(
        index: controller.currentIndex.value,
        children: const [
          HomePage(),
          SearchPage(),
          ProfilePage(),
        ],
      )),
      bottomNavigationBar: Obx(() => BottomNavigationBar(
        currentIndex: controller.currentIndex.value,
        onTap: controller.changeTab,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      )),
    );
  }
}

class MainController extends GetxController {
  final currentIndex = 0.obs;

  void changeTab(int index) {
    currentIndex.value = index;
  }
}
```

## Nested Navigation

### TabView with Persistent Navigation

```dart
class DashboardPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Dashboard'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'Overview'),
              Tab(text: 'Stats'),
              Tab(text: 'Settings'),
            ],
          ),
        ),
        body: TabBarView(
          children: [
            // Each tab can have its own Navigator
            Navigator(
              onGenerateRoute: (settings) {
                return MaterialPageRoute(
                  builder: (context) => OverviewTab(),
                );
              },
            ),
            Navigator(
              onGenerateRoute: (settings) {
                return MaterialPageRoute(
                  builder: (context) => StatsTab(),
                );
              },
            ),
            Navigator(
              onGenerateRoute: (settings) {
                return MaterialPageRoute(
                  builder: (context) => SettingsTab(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
```

## Best Practices

1. **Route Naming**:
   - Use descriptive, hierarchical names (`/user/profile/edit`)
   - Keep route names consistent across platforms
   - Use constants for route names (avoid magic strings)

2. **Parameter Passing**:
   - Use route parameters for IDs (e.g., `/product/:id`)
   - Use arguments for complex data
   - Use query parameters for optional filters

3. **Navigation Guards**:
   - Keep middleware logic simple and focused
   - Use priority to control middleware execution order
   - Avoid heavy computations in middleware

4. **Deep Linking**:
   - Test deep links on both Android and iOS
   - Handle missing parameters gracefully
   - Validate deep link data before navigation

5. **Transitions**:
   - Use consistent transitions app-wide
   - Keep transition durations reasonable (200-400ms)
   - Consider accessibility (some users prefer reduced motion)

6. **Performance**:
   - Use `lazyPut` for route bindings to avoid loading all controllers at startup
   - Dispose controllers when routes are popped
   - Avoid complex animations for frequently navigated routes
