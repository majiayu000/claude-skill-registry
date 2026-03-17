# 🔗 Skill: Deep Linking & Universal Links

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-deep-linking` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `deep-linking`, `universal-links`, `app-links`, `go-router`, `navigation` |
| **Referencia** | [Flutter Deep Linking](https://docs.flutter.dev/ui/navigation/deep-linking) |

## 🔑 Keywords para Invocación

- `deep-linking`
- `universal-links`
- `app-links`
- `go-router`
- `dynamic-links`
- `@skill:deep-linking`

### Ejemplos de Prompts

```
Implementa deep-linking con universal links para iOS y Android
```

```
Setup go-router con deep linking
```

```
Configura app-links y universal-links
```

```
@skill:deep-linking - Navigation completa con deep links
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Este skill cubre la implementación de deep linking, universal links (iOS) y app links (Android) usando go_router. Incluye configuración de dominios, asociación de archivos, y routing dinámico basado en URLs.

### ✅ Cuándo Usar Este Skill

- Links compartibles a contenido específico
- Marketing campaigns con attribution
- Email/SMS links que abren la app
- Social media sharing
- Push notifications con navegación
- QR codes que abren la app
- Web-to-app handoff

### ❌ Cuándo NO Usar Este Skill

- App sin contenido compartible
- No necesitas links externos
- Solo navegación interna

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── routing/
│   │   ├── app_router.dart
│   │   ├── route_paths.dart
│   │   └── deep_link_handler.dart
│   │
│   └── main.dart
│
├── android/
│   └── app/src/main/
│       ├── AndroidManifest.xml
│       └── res/values/
│           └── strings.xml
│
├── ios/
│   └── Runner/
│       ├── Info.plist
│       └── Runner.entitlements
│
└── .well-known/
    ├── assetlinks.json        # Android
    └── apple-app-site-association  # iOS
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter
  go_router: ^13.0.0
  uni_links: ^0.5.1  # Alternative simple approach
```

## 💻 Implementación

### 1. go_router Configuration

#### 1.1 Route Paths

```dart
// lib/routing/route_paths.dart
class RoutePaths {
  // Root
  static const home = '/';

  // Authentication
  static const login = '/login';
  static const signup = '/signup';
  static const resetPassword = '/reset-password';

  // Content
  static const product = '/product/:id';
  static const productDetails = '/product/:id/details';
  static const category = '/category/:slug';

  // User
  static const profile = '/profile/:userId';
  static const settings = '/settings';

  // Deep link specific
  static const share = '/share/:type/:id';
  static const invite = '/invite/:code';
  static const promo = '/promo/:code';

  // Error
  static const notFound = '/404';
}
```

#### 1.2 Router Configuration

```dart
// lib/routing/app_router.dart
import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';

class AppRouter {
  static final GoRouter router = GoRouter(
    initialLocation: RoutePaths.home,
    debugLogDiagnostics: true,

    // Redirect logic
    redirect: (context, state) {
      final isAuthenticated = AuthService.isAuthenticated;
      final isAuthRoute = state.matchedLocation.startsWith('/login') ||
          state.matchedLocation.startsWith('/signup');

      // Redirect to login if not authenticated
      if (!isAuthenticated && !isAuthRoute) {
        return '${RoutePaths.login}?redirect=${state.matchedLocation}';
      }

      // Redirect authenticated users away from auth pages
      if (isAuthenticated && isAuthRoute) {
        return RoutePaths.home;
      }

      return null;
    },

    // Error handling
    errorBuilder: (context, state) => NotFoundScreen(
      error: state.error.toString(),
    ),

    // Routes
    routes: [
      GoRoute(
        path: RoutePaths.home,
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),

      // Authentication
      GoRoute(
        path: RoutePaths.login,
        name: 'login',
        builder: (context, state) {
          final redirect = state.uri.queryParameters['redirect'];
          return LoginScreen(redirectTo: redirect);
        },
      ),

      GoRoute(
        path: RoutePaths.signup,
        name: 'signup',
        builder: (context, state) => const SignupScreen(),
      ),

      // Product with nested routes
      GoRoute(
        path: RoutePaths.product,
        name: 'product',
        builder: (context, state) {
          final productId = state.pathParameters['id']!;
          return ProductScreen(productId: productId);
        },
        routes: [
          GoRoute(
            path: 'details',
            name: 'product-details',
            builder: (context, state) {
              final productId = state.pathParameters['id']!;
              return ProductDetailsScreen(productId: productId);
            },
          ),
        ],
      ),

      // Category
      GoRoute(
        path: RoutePaths.category,
        name: 'category',
        builder: (context, state) {
          final slug = state.pathParameters['slug']!;
          final sort = state.uri.queryParameters['sort'];
          return CategoryScreen(slug: slug, sortBy: sort);
        },
      ),

      // Profile
      GoRoute(
        path: RoutePaths.profile,
        name: 'profile',
        builder: (context, state) {
          final userId = state.pathParameters['userId']!;
          return ProfileScreen(userId: userId);
        },
      ),

      // Share (deep link)
      GoRoute(
        path: RoutePaths.share,
        name: 'share',
        builder: (context, state) {
          final type = state.pathParameters['type']!;
          final id = state.pathParameters['id']!;
          return ShareScreen(contentType: type, contentId: id);
        },
      ),

      // Invite code
      GoRoute(
        path: RoutePaths.invite,
        name: 'invite',
        builder: (context, state) {
          final code = state.pathParameters['code']!;
          return InviteScreen(inviteCode: code);
        },
      ),

      // Promo code
      GoRoute(
        path: RoutePaths.promo,
        name: 'promo',
        builder: (context, state) {
          final code = state.pathParameters['code']!;
          return PromoScreen(promoCode: code);
        },
      ),
    ],
  );

  // Navigation helpers
  static void goToProduct(String productId) {
    router.go('/product/$productId');
  }

  static void goToCategory(String slug, {String? sortBy}) {
    final queryParams = sortBy != null ? '?sort=$sortBy' : '';
    router.go('/category/$slug$queryParams');
  }

  static void goToProfile(String userId) {
    router.go('/profile/$userId');
  }

  static void handleInviteLink(String code) {
    router.go('/invite/$code');
  }

  static void handlePromoLink(String code) {
    router.go('/promo/$code');
  }
}
```

### 2. iOS Universal Links Configuration

#### 2.1 Associated Domains

```xml
<!-- ios/Runner/Runner.entitlements -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.developer.associated-domains</key>
    <array>
        <string>applinks:yourdomain.com</string>
        <string>applinks:www.yourdomain.com</string>
    </array>
</dict>
</plist>
```

```xml
<!-- ios/Runner/Info.plist -->
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>CFBundleURLName</key>
        <string>com.example.myapp</string>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>myapp</string>
        </array>
    </dict>
</array>
```

#### 2.2 Apple App Site Association File

```json
// .well-known/apple-app-site-association
{
  "applinks": {
    "details": [
      {
        "appIDs": [
          "TEAMID.com.example.myapp"
        ],
        "components": [
          {
            "/": "/product/*",
            "comment": "Matches any product URL"
          },
          {
            "/": "/category/*",
            "comment": "Matches any category URL"
          },
          {
            "/": "/invite/*",
            "comment": "Matches invite links"
          },
          {
            "/": "/promo/*",
            "comment": "Matches promo links"
          }
        ]
      }
    ]
  },
  "webcredentials": {
    "apps": [
      "TEAMID.com.example.myapp"
    ]
  }
}
```

**Hosting Requirements:**
- Debe estar en `https://yourdomain.com/.well-known/apple-app-site-association`
- Content-Type: `application/json` (sin extensión .json)
- Debe ser accesible sin redirects
- HTTPS con certificado válido

### 3. Android App Links Configuration

#### 3.1 AndroidManifest.xml

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<manifest>
    <application>
        <activity
            android:name=".MainActivity"
            android:launchMode="singleTop">

            <!-- Deep Links (Custom Scheme) -->
            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="myapp" />
            </intent-filter>

            <!-- App Links (Verified HTTPS) -->
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />

                <data
                    android:scheme="https"
                    android:host="yourdomain.com"
                    android:pathPrefix="/product" />
                <data
                    android:scheme="https"
                    android:host="yourdomain.com"
                    android:pathPrefix="/category" />
                <data
                    android:scheme="https"
                    android:host="yourdomain.com"
                    android:pathPrefix="/invite" />
                <data
                    android:scheme="https"
                    android:host="yourdomain.com"
                    android:pathPrefix="/promo" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

#### 3.2 Android Asset Links File

```json
// .well-known/assetlinks.json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.example.myapp",
      "sha256_cert_fingerprints": [
        "YOUR_SHA256_FINGERPRINT_HERE"
      ]
    }
  }
]
```

**Obtener SHA-256 fingerprint:**
```bash
# Debug keystore
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android

# Release keystore
keytool -list -v -keystore /path/to/release.keystore -alias your-alias
```

**Hosting Requirements:**
- Debe estar en `https://yourdomain.com/.well-known/assetlinks.json`
- Content-Type: `application/json`
- Accesible sin autenticación

### 4. Deep Link Handler

```dart
// lib/routing/deep_link_handler.dart
import 'package:go_router/go_router.dart';
import 'package:uni_links/uni_links.dart';
import 'dart:async';

class DeepLinkHandler {
  static StreamSubscription? _linkSubscription;

  // Initialize deep link handling
  static Future<void> initialize(GoRouter router) async {
    // Handle initial link (app opened from link)
    try {
      final initialLink = await getInitialUri();
      if (initialLink != null) {
        _handleDeepLink(initialLink, router);
      }
    } catch (e) {
      print('Error getting initial link: $e');
    }

    // Handle links while app is running
    _linkSubscription = uriLinkStream.listen(
      (Uri? uri) {
        if (uri != null) {
          _handleDeepLink(uri, router);
        }
      },
      onError: (error) {
        print('Deep link error: $error');
      },
    );
  }

  static void _handleDeepLink(Uri uri, GoRouter router) {
    print('📱 Deep Link received: $uri');

    // Track deep link
    AnalyticsService.trackEvent('deep_link_opened', properties: {
      'url': uri.toString(),
      'scheme': uri.scheme,
      'host': uri.host,
      'path': uri.path,
    });

    // Parse and navigate
    if (uri.scheme == 'myapp') {
      // Custom scheme: myapp://product/123
      _handleCustomScheme(uri, router);
    } else if (uri.scheme == 'https') {
      // Universal link: https://yourdomain.com/product/123
      _handleUniversalLink(uri, router);
    }
  }

  static void _handleCustomScheme(Uri uri, GoRouter router) {
    // myapp://product/123
    final path = uri.host + uri.path;
    router.go('/$path');
  }

  static void _handleUniversalLink(Uri uri, GoRouter router) {
    // https://yourdomain.com/product/123
    final path = uri.path;
    final queryParams = uri.queryParameters;

    // Build path with query parameters
    final fullPath = queryParams.isEmpty
        ? path
        : '$path?${Uri(queryParameters: queryParams).query}';

    router.go(fullPath);
  }

  // Generate shareable link
  static String generateShareLink({
    required String type,
    required String id,
  }) {
    return 'https://yourdomain.com/share/$type/$id';
  }

  // Generate invite link
  static String generateInviteLink(String code) {
    return 'https://yourdomain.com/invite/$code';
  }

  // Generate promo link
  static String generatePromoLink(String code) {
    return 'https://yourdomain.com/promo/$code';
  }

  // Dispose
  static void dispose() {
    _linkSubscription?.cancel();
  }
}
```

### 5. Main.dart Setup

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'routing/app_router.dart';
import 'routing/deep_link_handler.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize deep link handling
  await DeepLinkHandler.initialize(AppRouter.router);

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'My App',
      routerConfig: AppRouter.router,
    );
  }
}
```

### 6. Testing Deep Links

#### 6.1 iOS Testing

```bash
# Test custom scheme
xcrun simctl openurl booted "myapp://product/123"

# Test universal link
xcrun simctl openurl booted "https://yourdomain.com/product/123"
```

#### 6.2 Android Testing

```bash
# Test custom scheme
adb shell am start -W -a android.intent.action.VIEW -d "myapp://product/123" com.example.myapp

# Test app link
adb shell am start -W -a android.intent.action.VIEW -d "https://yourdomain.com/product/123" com.example.myapp

# Verify app links
adb shell dumpsys package domain-preferred-apps
```

#### 6.3 Verification Tools

```bash
# iOS: Test AASA file
curl -v https://yourdomain.com/.well-known/apple-app-site-association

# Android: Test assetlinks.json
curl -v https://yourdomain.com/.well-known/assetlinks.json

# Android: Verify signature
adb shell pm get-app-links com.example.myapp
```

## 🎯 Mejores Prácticas

### 1. URL Structure

✅ **DO:** Usa URLs consistentes y descriptivas
```
https://yourdomain.com/product/123
https://yourdomain.com/category/electronics
https://yourdomain.com/invite/ABC123
```

### 2. Fallback Handling

✅ **DO:** Maneja casos donde la app no está instalada
```dart
// En el servidor, detecta si la app está instalada
// Si no está, redirige a App Store/Play Store
```

### 3. Analytics

✅ **DO:** Trackea origen de deep links
```dart
AnalyticsService.trackEvent('deep_link_opened', properties: {
  'source': 'email',
  'campaign': 'summer_sale',
  'url': uri.toString(),
});
```

## 🚨 Troubleshooting

### Universal Links Not Working (iOS)

1. Verificar Associated Domains en Xcode
2. Verificar Team ID correcto en AASA file
3. Verificar hosting correcto del archivo
4. Probar con dispositivo real (simulador puede no funcionar siempre)

### App Links Not Verified (Android)

```bash
# Verificar estado
adb shell pm get-app-links com.example.myapp

# Forzar verificación
adb shell pm set-app-links --package com.example.myapp 0 all

# Re-verificar
adb shell pm verify-app-links --re-verify com.example.myapp
```

### Deep Link Opens Browser Instead of App

- Verificar que autoVerify="true" en Android
- Verificar SHA-256 fingerprint correcto
- Verificar hosting de archivos de asociación

## 📚 Recursos

- [go_router Documentation](https://pub.dev/packages/go_router)
- [iOS Universal Links](https://developer.apple.com/ios/universal-links/)
- [Android App Links](https://developer.android.com/training/app-links)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
