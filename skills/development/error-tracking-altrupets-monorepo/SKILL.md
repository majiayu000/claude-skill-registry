# 🐛 Skill: Error Tracking & Crash Reporting

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-error-tracking` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `error-tracking`, `sentry`, `crashlytics`, `crash-reporting`, `logging`, `monitoring` |
| **Referencia** | [Sentry Flutter](https://docs.sentry.io/platforms/flutter/) |

## 🔑 Keywords para Invocación

- `error-tracking`
- `sentry`
- `crashlytics`
- `crash-reporting`
- `error-monitoring`
- `logging`
- `@skill:error-tracking`

### Ejemplos de Prompts

```
Implementa error-tracking con sentry y crashlytics
```

```
Setup crash-reporting para producción
```

```
Configura logging y monitoring completo
```

```
@skill:error-tracking - Sistema completo de monitoreo de errores
```

## 📖 Descripción

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

Este skill cubre la implementación de sistemas de monitoreo y tracking de errores en Flutter apps usando Sentry y Firebase Crashlytics. Incluye captura automática de errores, contexto enriquecido, breadcrumbs, y integración con CI/CD para source maps y debug symbols.

### ✅ Cuándo Usar Este Skill

- Apps en producción
- Monitoreo de estabilidad
- Debug de errores en producción
- Performance monitoring
- User feedback sobre crashes
- Analytics de errores
- Release health tracking

### ❌ Cuándo NO Usar Este Skill

- Solo desarrollo local
- Prototipos sin usuarios reales
- MVP sin presupuesto para herramientas

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── core/
│   │   ├── error/
│   │   │   ├── error_tracker.dart
│   │   │   ├── sentry_service.dart
│   │   │   ├── crashlytics_service.dart
│   │   │   └── custom_error_widget.dart
│   │   └── logger/
│   │       ├── app_logger.dart
│   │       └── log_interceptor.dart
│   │
│   ├── services/
│   │   └── error_service.dart
│   │
│   └── main.dart
│
├── android/
│   └── app/
│       └── google-services.json
│
├── ios/
│   └── Runner/
│       └── GoogleService-Info.plist
│
└── scripts/
    ├── upload_symbols.sh
    └── upload_sourcemaps.sh
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Sentry
  sentry_flutter: ^7.14.0

  # Firebase Crashlytics
  firebase_core: ^2.24.2
  firebase_crashlytics: ^3.4.8

  # Logging
  logger: ^2.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
```

## 💻 Implementación

### 1. Sentry Integration

#### 1.1 Sentry Service

```dart
// lib/core/error/sentry_service.dart
import 'package:sentry_flutter/sentry_flutter.dart';
import 'package:flutter/foundation.dart';

class SentryService {
  static Future<void> initialize() async {
    await SentryFlutter.init(
      (options) {
        options.dsn = 'YOUR_SENTRY_DSN_HERE';

        // Environment
        options.environment = kReleaseMode ? 'production' : 'development';

        // Release versioning
        options.release = 'myapp@1.0.0+1';
        options.dist = '1';

        // Performance monitoring
        options.tracesSampleRate = kReleaseMode ? 0.1 : 1.0;
        options.profilesSampleRate = 0.1;

        // Debug options
        options.debug = kDebugMode;

        // Attach screenshots on errors
        options.attachScreenshot = true;
        options.screenshotQuality = SentryScreenshotQuality.medium;

        // Attach view hierarchy
        options.attachViewHierarchy = true;

        // Filter sensitive data
        options.beforeSend = (event, hint) {
          // Remove sensitive data
          if (event.request?.headers != null) {
            event.request!.headers!.remove('Authorization');
            event.request!.headers!.remove('Cookie');
          }
          return event;
        };

        // Filter breadcrumbs
        options.beforeBreadcrumb = (breadcrumb, hint) {
          // Don't log debug breadcrumbs in production
          if (kReleaseMode && breadcrumb.level == SentryLevel.debug) {
            return null;
          }
          return breadcrumb;
        };
      },
    );
  }

  // Capture exception with context
  static Future<void> captureException(
    dynamic exception,
    StackTrace? stackTrace, {
    String? hint,
    Map<String, dynamic>? extra,
    SentryLevel level = SentryLevel.error,
  }) async {
    await Sentry.captureException(
      exception,
      stackTrace: stackTrace,
      withScope: (scope) {
        scope.level = level;

        if (hint != null) {
          scope.setTag('hint', hint);
        }

        if (extra != null) {
          extra.forEach((key, value) {
            scope.setExtra(key, value);
          });
        }
      },
    );
  }

  // Capture message
  static Future<void> captureMessage(
    String message, {
    SentryLevel level = SentryLevel.info,
    Map<String, dynamic>? extra,
  }) async {
    await Sentry.captureMessage(
      message,
      level: level,
      withScope: (scope) {
        if (extra != null) {
          extra.forEach((key, value) {
            scope.setExtra(key, value);
          });
        }
      },
    );
  }

  // Add breadcrumb
  static void addBreadcrumb({
    required String message,
    String? category,
    SentryLevel level = SentryLevel.info,
    Map<String, dynamic>? data,
  }) {
    Sentry.addBreadcrumb(
      Breadcrumb(
        message: message,
        category: category,
        level: level,
        data: data,
        timestamp: DateTime.now(),
      ),
    );
  }

  // Set user context
  static void setUser({
    String? id,
    String? email,
    String? username,
    Map<String, dynamic>? extras,
  }) {
    Sentry.configureScope((scope) {
      scope.setUser(
        SentryUser(
          id: id,
          email: email,
          username: username,
          data: extras,
        ),
      );
    });
  }

  // Clear user context
  static void clearUser() {
    Sentry.configureScope((scope) {
      scope.setUser(null);
    });
  }

  // Set custom context
  static void setContext(String key, Map<String, dynamic> data) {
    Sentry.configureScope((scope) {
      scope.setContexts(key, data);
    });
  }

  // Set tag
  static void setTag(String key, String value) {
    Sentry.configureScope((scope) {
      scope.setTag(key, value);
    });
  }

  // Start transaction (performance monitoring)
  static ISentrySpan startTransaction(
    String name,
    String operation, {
    String? description,
  }) {
    return Sentry.startTransaction(
      name,
      operation,
      description: description,
    );
  }

  // Report network call
  static Future<T> traceNetworkCall<T>(
    String url,
    String method,
    Future<T> Function() request,
  ) async {
    final transaction = startTransaction(
      'http.client',
      'http.request',
      description: '$method $url',
    );

    try {
      final result = await request();
      transaction.status = const SpanStatus.ok();
      return result;
    } catch (e) {
      transaction.status = const SpanStatus.internalError();
      transaction.throwable = e;
      rethrow;
    } finally {
      await transaction.finish();
    }
  }
}
```

#### 1.2 Sentry HTTP Client Interceptor

```dart
// lib/core/logger/sentry_http_interceptor.dart
import 'package:dio/dio.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

class SentryHttpInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    // Add breadcrumb for request
    SentryService.addBreadcrumb(
      message: '${options.method} ${options.uri}',
      category: 'http',
      level: SentryLevel.info,
      data: {
        'method': options.method,
        'url': options.uri.toString(),
      },
    );

    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    // Add breadcrumb for successful response
    SentryService.addBreadcrumb(
      message: '${response.requestOptions.method} ${response.requestOptions.uri} - ${response.statusCode}',
      category: 'http.response',
      level: SentryLevel.info,
      data: {
        'status_code': response.statusCode,
        'method': response.requestOptions.method,
        'url': response.requestOptions.uri.toString(),
      },
    );

    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    // Capture HTTP errors in Sentry
    SentryService.captureException(
      err,
      err.stackTrace,
      hint: 'HTTP Error',
      extra: {
        'method': err.requestOptions.method,
        'url': err.requestOptions.uri.toString(),
        'status_code': err.response?.statusCode,
        'response': err.response?.data,
      },
      level: SentryLevel.error,
    );

    handler.next(err);
  }
}
```

### 2. Firebase Crashlytics Integration

#### 2.1 Crashlytics Service

```dart
// lib/core/error/crashlytics_service.dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';

class CrashlyticsService {
  static Future<void> initialize() async {
    // Enable Crashlytics in release mode only
    await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(kReleaseMode);

    // Pass all uncaught Flutter errors to Crashlytics
    FlutterError.onError = (details) {
      FirebaseCrashlytics.instance.recordFlutterFatalError(details);
    };

    // Pass all uncaught asynchronous errors to Crashlytics
    PlatformDispatcher.instance.onError = (error, stack) {
      FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
      return true;
    };
  }

  // Record error
  static Future<void> recordError(
    dynamic exception,
    StackTrace? stackTrace, {
    String? reason,
    bool fatal = false,
    Iterable<Object> information = const [],
  }) async {
    await FirebaseCrashlytics.instance.recordError(
      exception,
      stackTrace,
      reason: reason,
      fatal: fatal,
      information: information,
    );
  }

  // Log message
  static void log(String message) {
    FirebaseCrashlytics.instance.log(message);
  }

  // Set user identifier
  static Future<void> setUserIdentifier(String identifier) async {
    await FirebaseCrashlytics.instance.setUserIdentifier(identifier);
  }

  // Set custom key
  static Future<void> setCustomKey(String key, dynamic value) async {
    await FirebaseCrashlytics.instance.setCustomKey(key, value);
  }

  // Set custom keys
  static Future<void> setCustomKeys(Map<String, dynamic> keys) async {
    for (final entry in keys.entries) {
      await setCustomKey(entry.key, entry.value);
    }
  }

  // Force crash (testing only!)
  static void forceCrash() {
    FirebaseCrashlytics.instance.crash();
  }

  // Check if crash reporting is enabled
  static Future<bool> isCrashlyticsCollectionEnabled() async {
    return await FirebaseCrashlytics.instance.isCrashlyticsCollectionEnabled();
  }

  // Enable/disable crash reporting
  static Future<void> setCrashlyticsCollectionEnabled(bool enabled) async {
    await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(enabled);
  }

  // Send unhandled exception
  static Future<void> recordFlutterFatalError(FlutterErrorDetails details) async {
    await FirebaseCrashlytics.instance.recordFlutterFatalError(details);
  }
}
```

### 3. Unified Error Tracker

```dart
// lib/core/error/error_tracker.dart
import 'package:flutter/foundation.dart';
import 'sentry_service.dart';
import 'crashlytics_service.dart';

enum ErrorSeverity { info, warning, error, fatal }

class ErrorTracker {
  static bool _initialized = false;

  static Future<void> initialize() async {
    if (_initialized) return;

    // Initialize Sentry
    await SentryService.initialize();

    // Initialize Crashlytics
    await CrashlyticsService.initialize();

    _initialized = true;
  }

  // Report error to both services
  static Future<void> reportError(
    dynamic error,
    StackTrace? stackTrace, {
    String? hint,
    ErrorSeverity severity = ErrorSeverity.error,
    Map<String, dynamic>? extras,
  }) async {
    if (!_initialized) await initialize();

    // Log locally
    debugPrint('Error: $error\nStackTrace: $stackTrace');

    // Report to Sentry
    await SentryService.captureException(
      error,
      stackTrace,
      hint: hint,
      extra: extras,
      level: _sentryLevel(severity),
    );

    // Report to Crashlytics
    await CrashlyticsService.recordError(
      error,
      stackTrace,
      reason: hint,
      fatal: severity == ErrorSeverity.fatal,
    );
  }

  // Log message
  static void log(
    String message, {
    ErrorSeverity severity = ErrorSeverity.info,
    Map<String, dynamic>? extras,
  }) {
    // Sentry message
    SentryService.captureMessage(
      message,
      level: _sentryLevel(severity),
      extra: extras,
    );

    // Crashlytics log
    CrashlyticsService.log(message);
  }

  // Add breadcrumb
  static void addBreadcrumb(
    String message, {
    String? category,
    Map<String, dynamic>? data,
  }) {
    SentryService.addBreadcrumb(
      message: message,
      category: category,
      data: data,
    );

    CrashlyticsService.log('[$category] $message');
  }

  // Set user info
  static Future<void> setUser({
    required String id,
    String? email,
    String? username,
    Map<String, dynamic>? extras,
  }) async {
    // Sentry
    SentryService.setUser(
      id: id,
      email: email,
      username: username,
      extras: extras,
    );

    // Crashlytics
    await CrashlyticsService.setUserIdentifier(id);
    if (extras != null) {
      await CrashlyticsService.setCustomKeys(extras);
    }
  }

  // Clear user
  static void clearUser() {
    SentryService.clearUser();
    CrashlyticsService.setUserIdentifier('');
  }

  // Set custom data
  static Future<void> setCustomData(Map<String, dynamic> data) async {
    data.forEach((key, value) {
      SentryService.setContext(key, {'value': value});
    });

    await CrashlyticsService.setCustomKeys(data);
  }

  static SentryLevel _sentryLevel(ErrorSeverity severity) {
    switch (severity) {
      case ErrorSeverity.info:
        return SentryLevel.info;
      case ErrorSeverity.warning:
        return SentryLevel.warning;
      case ErrorSeverity.error:
        return SentryLevel.error;
      case ErrorSeverity.fatal:
        return SentryLevel.fatal;
    }
  }
}
```

### 4. Custom Error Widget

```dart
// lib/core/error/custom_error_widget.dart
import 'package:flutter/material.dart';
import 'error_tracker.dart';

class CustomErrorWidget extends StatelessWidget {
  final FlutterErrorDetails details;

  const CustomErrorWidget({
    Key? key,
    required this.details,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Material(
      child: Container(
        color: Colors.red.shade50,
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: Colors.red.shade700,
            ),
            const SizedBox(height: 16),
            Text(
              'Something went wrong',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.red.shade700,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'The error has been reported to our team.',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.red.shade600),
            ),
            if (kDebugMode) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.black87,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  details.exceptionAsString(),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 12,
                    fontFamily: 'monospace',
                  ),
                ),
              ),
            ],
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                // Restart app or navigate to home
                Navigator.of(context).popUntil((route) => route.isFirst);
              },
              child: const Text('Go to Home'),
            ),
          ],
        ),
      ),
    );
  }

  static void setupErrorWidget() {
    ErrorWidget.builder = (FlutterErrorDetails details) {
      // Report error
      ErrorTracker.reportError(
        details.exception,
        details.stack,
        hint: 'Widget Error',
        severity: ErrorSeverity.error,
      );

      return CustomErrorWidget(details: details);
    };
  }
}
```

### 5. Main.dart Setup

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'core/error/error_tracker.dart';
import 'core/error/custom_error_widget.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase
  await Firebase.initializeApp();

  // Initialize Error Tracking
  await ErrorTracker.initialize();

  // Setup custom error widget
  CustomErrorWidget.setupErrorWidget();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      home: const HomeScreen(),
      // Capture navigation errors
      onGenerateRoute: (settings) {
        ErrorTracker.addBreadcrumb(
          'Navigation: ${settings.name}',
          category: 'navigation',
        );
        return null;
      },
    );
  }
}
```

### 6. Logger Implementation

```dart
// lib/core/logger/app_logger.dart
import 'package:logger/logger.dart';
import '../error/error_tracker.dart';

class AppLogger {
  static final Logger _logger = Logger(
    printer: PrettyPrinter(
      methodCount: 2,
      errorMethodCount: 8,
      lineLength: 120,
      colors: true,
      printEmojis: true,
      printTime: true,
    ),
  );

  static void debug(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.d(message, error: error, stackTrace: stackTrace);
    ErrorTracker.log(message, severity: ErrorSeverity.info);
  }

  static void info(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.i(message, error: error, stackTrace: stackTrace);
    ErrorTracker.log(message, severity: ErrorSeverity.info);
  }

  static void warning(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.w(message, error: error, stackTrace: stackTrace);
    ErrorTracker.log(message, severity: ErrorSeverity.warning);
  }

  static void error(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.e(message, error: error, stackTrace: stackTrace);
    ErrorTracker.reportError(
      error ?? message,
      stackTrace,
      hint: message,
      severity: ErrorSeverity.error,
    );
  }

  static void fatal(String message, [dynamic error, StackTrace? stackTrace]) {
    _logger.f(message, error: error, stackTrace: stackTrace);
    ErrorTracker.reportError(
      error ?? message,
      stackTrace,
      hint: message,
      severity: ErrorSeverity.fatal,
    );
  }
}
```

### 7. CI/CD Integration

#### 7.1 Upload Debug Symbols (Android)

```bash
# scripts/upload_symbols_android.sh
#!/bin/bash

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Build with debug symbols
cd mobile
flutter build appbundle --release
cd ..

# Upload to Crashlytics
firebase crashlytics:symbols:upload \
  --app=1:123456789:android:abcd1234 \
  android/app/build/intermediates/merged_native_libs/release/out/lib
```

#### 7.2 Upload Source Maps (Sentry)

```bash
# scripts/upload_sourcemaps.sh
#!/bin/bash

VERSION="1.0.0+1"

# Install Sentry CLI
curl -sL https://sentry.io/get-cli/ | bash

# Upload debug symbols
sentry-cli upload-dif \
  --org your-org \
  --project your-project \
  build/app/intermediates/merged_native_libs/release/out/lib

# Upload source maps for web
sentry-cli releases files $VERSION \
  upload-sourcemaps build/web \
  --url-prefix '~/' \
  --validate
```

## 🎯 Mejores Prácticas

### 1. Error Context

✅ **DO:** Agrega contexto rico
```dart
ErrorTracker.reportError(
  error,
  stackTrace,
  hint: 'User checkout failed',
  extras: {
    'user_id': userId,
    'cart_items': cartItems.length,
    'total_amount': totalAmount,
  },
);
```

### 2. Breadcrumbs

✅ **DO:** Usa breadcrumbs para debugging
```dart
// En cada acción importante
ErrorTracker.addBreadcrumb('User tapped checkout button');
ErrorTracker.addBreadcrumb('Payment method selected: Credit Card');
ErrorTracker.addBreadcrumb('Processing payment...');
```

### 3. PII Protection

✅ **DO:** Filtra información sensible
```dart
options.beforeSend = (event, hint) {
  // Remove sensitive data
  event.request?.headers?.remove('Authorization');
  event.user?.email = '[FILTERED]';
  return event;
};
```

## 🚨 Troubleshooting

### Sentry DSN Not Working

```dart
// Verify DSN is correct and environment is set
options.dsn = 'https://[key]@[organization].ingest.sentry.io/[project]';
options.environment = kReleaseMode ? 'production' : 'development';
```

### Crashlytics Not Reporting

```bash
# Verify Firebase is initialized
flutter pub get
flutterfire configure
```

### Missing Debug Symbols

```bash
# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Build with debug symbols
cd mobile
flutter build apk --split-debug-info=build/symbols
flutter build appbundle --split-debug-info=build/symbols
cd ..
```

## 📚 Recursos

- [Sentry Flutter SDK](https://docs.sentry.io/platforms/flutter/)
- [Firebase Crashlytics](https://firebase.google.com/docs/crashlytics)
- [Flutter Error Handling](https://docs.flutter.dev/testing/errors)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,200+
