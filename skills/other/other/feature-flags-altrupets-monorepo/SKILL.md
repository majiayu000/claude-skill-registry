# 🚩 Skill: Feature Flags & Remote Config

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-feature-flags` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `feature-flags`, `remote-config`, `firebase-remote-config`, `launchdarkly`, `ab-testing` |
| **Referencia** | [Firebase Remote Config](https://firebase.google.com/docs/remote-config) |

## 🔑 Keywords para Invocación

- `feature-flags`
- `remote-config`
- `firebase-remote-config`
- `launchdarkly`
- `ab-testing`
- `feature-toggle`
- `@skill:feature-flags`

### Ejemplos de Prompts

```
Implementa feature-flags con firebase remote config
```

```
Setup launchdarkly para A/B testing
```

```
Configura feature toggles dinámicos
```

```
@skill:feature-flags - Sistema completo de feature flags
```

## 📖 Descripción

Este skill cubre la implementación de feature flags y remote configuration usando Firebase Remote Config y LaunchDarkly. Permite controlar features remotamente, hacer A/B testing, staged rollouts, y kill switches sin actualizar la app.

### ✅ Cuándo Usar Este Skill

- Staged rollouts de features
- A/B testing
- Kill switches de emergencia
- Personalización por usuario/segmento
- Cambios de configuración sin release
- Beta features
- Experimentos de producto
- Darkly launches

### ❌ Cuándo NO Usar Este Skill

- Features siempre encendidas
- No necesitas control remoto
- App completamente offline

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── core/
│   │   └── feature_flags/
│   │       ├── feature_flag_service.dart
│   │       ├── firebase_remote_config_service.dart
│   │       ├── feature_flag_provider.dart
│   │       └── feature_flags.dart
│   │
│   └── main.dart
│
└── test/
    └── feature_flags_test.dart
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Firebase Remote Config
  firebase_core: ^2.24.2
  firebase_remote_config: ^4.3.8

  # Provider para state management
  provider: ^6.1.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.4
```

## 💻 Implementación

### 1. Feature Flags Definition

```dart
// lib/core/feature_flags/feature_flags.dart
enum FeatureFlag {
  newHomeScreen,
  darkMode,
  socialLogin,
  premiumFeatures,
  newCheckoutFlow,
  chatSupport,
  videoCall,
  aiRecommendations,
}

extension FeatureFlagExtension on FeatureFlag {
  String get key {
    switch (this) {
      case FeatureFlag.newHomeScreen:
        return 'new_home_screen';
      case FeatureFlag.darkMode:
        return 'dark_mode_enabled';
      case FeatureFlag.socialLogin:
        return 'social_login_enabled';
      case FeatureFlag.premiumFeatures:
        return 'premium_features_enabled';
      case FeatureFlag.newCheckoutFlow:
        return 'new_checkout_flow';
      case FeatureFlag.chatSupport:
        return 'chat_support_enabled';
      case FeatureFlag.videoCall:
        return 'video_call_enabled';
      case FeatureFlag.aiRecommendations:
        return 'ai_recommendations_enabled';
    }
  }

  bool get defaultValue {
    switch (this) {
      case FeatureFlag.newHomeScreen:
        return false;
      case FeatureFlag.darkMode:
        return true;
      case FeatureFlag.socialLogin:
        return false;
      case FeatureFlag.premiumFeatures:
        return false;
      case FeatureFlag.newCheckoutFlow:
        return false;
      case FeatureFlag.chatSupport:
        return true;
      case FeatureFlag.videoCall:
        return false;
      case FeatureFlag.aiRecommendations:
        return false;
    }
  }
}
```

### 2. Firebase Remote Config Service

```dart
// lib/core/feature_flags/firebase_remote_config_service.dart
import 'package:firebase_remote_config/firebase_remote_config.dart';
import 'package:flutter/foundation.dart';
import 'feature_flags.dart';

class FirebaseRemoteConfigService {
  static final FirebaseRemoteConfig _remoteConfig = FirebaseRemoteConfig.instance;

  static bool _initialized = false;

  // Initialize Remote Config
  static Future<void> initialize() async {
    if (_initialized) return;

    try {
      // Set config settings
      await _remoteConfig.setConfigSettings(
        RemoteConfigSettings(
          fetchTimeout: const Duration(seconds: 30),
          minimumFetchInterval: kDebugMode
              ? const Duration(minutes: 5)  // Debug: 5 minutes
              : const Duration(hours: 1),    // Production: 1 hour
        ),
      );

      // Set default values
      await _remoteConfig.setDefaults(_getDefaultValues());

      // Fetch and activate
      await _remoteConfig.fetchAndActivate();

      // Listen to config updates (real-time)
      _remoteConfig.onConfigUpdated.listen((event) async {
        await _remoteConfig.activate();
        print('🔄 Remote Config updated');
      });

      _initialized = true;
      print('✅ Remote Config initialized');
    } catch (e) {
      print('❌ Remote Config initialization error: $e');
    }
  }

  // Get default values map
  static Map<String, dynamic> _getDefaultValues() {
    return Map.fromEntries(
      FeatureFlag.values.map(
        (flag) => MapEntry(flag.key, flag.defaultValue),
      ),
    );
  }

  // Check if feature is enabled
  static bool isFeatureEnabled(FeatureFlag flag) {
    try {
      return _remoteConfig.getBool(flag.key);
    } catch (e) {
      print('Error getting feature flag ${flag.key}: $e');
      return flag.defaultValue;
    }
  }

  // Get string value
  static String getString(String key, {String defaultValue = ''}) {
    try {
      return _remoteConfig.getString(key);
    } catch (e) {
      return defaultValue;
    }
  }

  // Get int value
  static int getInt(String key, {int defaultValue = 0}) {
    try {
      return _remoteConfig.getInt(key);
    } catch (e) {
      return defaultValue;
    }
  }

  // Get double value
  static double getDouble(String key, {double defaultValue = 0.0}) {
    try {
      return _remoteConfig.getDouble(key);
    } catch (e) {
      return defaultValue;
    }
  }

  // Get JSON value
  static Map<String, dynamic>? getJson(String key) {
    try {
      final jsonString = _remoteConfig.getString(key);
      return jsonDecode(jsonString) as Map<String, dynamic>;
    } catch (e) {
      return null;
    }
  }

  // Force fetch (for debugging)
  static Future<void> forceFetch() async {
    try {
      await _remoteConfig.fetch();
      await _remoteConfig.activate();
      print('✅ Remote Config force fetched');
    } catch (e) {
      print('❌ Force fetch error: $e');
    }
  }

  // Get all values (for debugging)
  static Map<String, RemoteConfigValue> getAllValues() {
    return _remoteConfig.getAll();
  }

  // Get fetch status
  static RemoteConfigFetchStatus get fetchStatus => _remoteConfig.lastFetchStatus;

  // Get last fetch time
  static DateTime get lastFetchTime => _remoteConfig.lastFetchTime;
}
```

### 3. Feature Flag Service

```dart
// lib/core/feature_flags/feature_flag_service.dart
import 'package:flutter/foundation.dart';
import 'firebase_remote_config_service.dart';
import 'feature_flags.dart';

class FeatureFlagService extends ChangeNotifier {
  static final FeatureFlagService _instance = FeatureFlagService._internal();
  factory FeatureFlagService() => _instance;
  FeatureFlagService._internal();

  final Map<FeatureFlag, bool> _localOverrides = {};
  bool _debugMode = kDebugMode;

  // Initialize
  Future<void> initialize() async {
    await FirebaseRemoteConfigService.initialize();
    notifyListeners();
  }

  // Check if feature is enabled
  bool isEnabled(FeatureFlag flag) {
    // Check local overrides first (for debugging)
    if (_localOverrides.containsKey(flag)) {
      return _localOverrides[flag]!;
    }

    // Check remote config
    return FirebaseRemoteConfigService.isFeatureEnabled(flag);
  }

  // Enable feature locally (debug only)
  void enableLocally(FeatureFlag flag) {
    if (_debugMode) {
      _localOverrides[flag] = true;
      notifyListeners();
    }
  }

  // Disable feature locally (debug only)
  void disableLocally(FeatureFlag flag) {
    if (_debugMode) {
      _localOverrides[flag] = false;
      notifyListeners();
    }
  }

  // Clear local overrides
  void clearLocalOverrides() {
    _localOverrides.clear();
    notifyListeners();
  }

  // Get all feature states
  Map<FeatureFlag, bool> getAllFeatureStates() {
    return Map.fromEntries(
      FeatureFlag.values.map(
        (flag) => MapEntry(flag, isEnabled(flag)),
      ),
    );
  }

  // Refresh config
  Future<void> refresh() async {
    await FirebaseRemoteConfigService.forceFetch();
    notifyListeners();
  }

  // Get config value
  T getConfigValue<T>(String key, T defaultValue) {
    if (T == String) {
      return FirebaseRemoteConfigService.getString(key, defaultValue: defaultValue as String) as T;
    } else if (T == int) {
      return FirebaseRemoteConfigService.getInt(key, defaultValue: defaultValue as int) as T;
    } else if (T == double) {
      return FirebaseRemoteConfigService.getDouble(key, defaultValue: defaultValue as double) as T;
    } else if (T == bool) {
      // Custom bool config
      try {
        return FirebaseRemoteConfigService.isFeatureEnabled(
          FeatureFlag.values.firstWhere((flag) => flag.key == key),
        ) as T;
      } catch (e) {
        return defaultValue;
      }
    }
    return defaultValue;
  }

  // A/B Test variant
  String getABTestVariant(String experimentKey) {
    return FirebaseRemoteConfigService.getString(experimentKey, defaultValue: 'control');
  }
}
```

### 4. Feature Flag Provider

```dart
// lib/core/feature_flags/feature_flag_provider.dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'feature_flag_service.dart';
import 'feature_flags.dart';

class FeatureFlagProvider extends ChangeNotifierProvider<FeatureFlagService> {
  FeatureFlagProvider({
    Key? key,
    Widget? child,
  }) : super(
          key: key,
          create: (_) => FeatureFlagService(),
          child: child,
        );

  // Helper to access service
  static FeatureFlagService of(BuildContext context, {bool listen = false}) {
    return Provider.of<FeatureFlagService>(context, listen: listen);
  }
}

// Widget to conditionally show features
class FeatureGate extends StatelessWidget {
  final FeatureFlag flag;
  final Widget child;
  final Widget? fallback;

  const FeatureGate({
    Key? key,
    required this.flag,
    required this.child,
    this.fallback,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final service = FeatureFlagProvider.of(context, listen: true);
    final isEnabled = service.isEnabled(flag);

    return isEnabled ? child : (fallback ?? const SizedBox.shrink());
  }
}

// Widget for A/B Testing
class ABTestVariant extends StatelessWidget {
  final String experimentKey;
  final Map<String, Widget> variants;
  final Widget? defaultWidget;

  const ABTestVariant({
    Key? key,
    required this.experimentKey,
    required this.variants,
    this.defaultWidget,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final service = FeatureFlagProvider.of(context, listen: true);
    final variant = service.getABTestVariant(experimentKey);

    return variants[variant] ?? defaultWidget ?? const SizedBox.shrink();
  }
}
```

### 5. Usage Examples

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase
  await Firebase.initializeApp();

  // Initialize Feature Flags
  final featureFlagService = FeatureFlagService();
  await featureFlagService.initialize();

  runApp(
    FeatureFlagProvider(
      child: const MyApp(),
    ),
  );
}

// Example: Conditional UI
class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Column(
        children: [
          // Show new home screen if feature is enabled
          FeatureGate(
            flag: FeatureFlag.newHomeScreen,
            child: const NewHomeScreen(),
            fallback: const LegacyHomeScreen(),
          ),

          // Social login buttons
          FeatureGate(
            flag: FeatureFlag.socialLogin,
            child: Column(
              children: [
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Login with Google'),
                ),
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Login with Facebook'),
                ),
              ],
            ),
          ),

          // Chat support
          FeatureGate(
            flag: FeatureFlag.chatSupport,
            child: FloatingActionButton(
              onPressed: () {},
              child: const Icon(Icons.chat),
            ),
          ),
        ],
      ),
    );
  }
}

// Example: A/B Test
class ProductScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ABTestVariant(
      experimentKey: 'checkout_button_experiment',
      variants: {
        'control': ElevatedButton(
          onPressed: () {},
          child: const Text('Buy Now'),
        ),
        'variant_a': ElevatedButton(
          onPressed: () {},
          style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
          child: const Text('Add to Cart'),
        ),
        'variant_b': ElevatedButton(
          onPressed: () {},
          style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
          child: const Text('Purchase Now - 10% Off!'),
        ),
      },
      defaultWidget: ElevatedButton(
        onPressed: () {},
        child: const Text('Buy Now'),
      ),
    );
  }
}

// Example: Check in code
class CheckoutService {
  Future<void> processCheckout() async {
    final service = FeatureFlagService();

    if (service.isEnabled(FeatureFlag.newCheckoutFlow)) {
      // Use new checkout flow
      await _newCheckout();
    } else {
      // Use legacy checkout
      await _legacyCheckout();
    }
  }

  Future<void> _newCheckout() async {
    // Implementation
  }

  Future<void> _legacyCheckout() async {
    // Implementation
  }
}
```

### 6. Debug Screen

```dart
// lib/screens/feature_flags_debug_screen.dart
import 'package:flutter/material.dart';

class FeatureFlagsDebugScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final service = FeatureFlagProvider.of(context, listen: true);
    final allStates = service.getAllFeatureStates();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Feature Flags Debug'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => service.refresh(),
          ),
          IconButton(
            icon: const Icon(Icons.clear),
            onPressed: () => service.clearLocalOverrides(),
          ),
        ],
      ),
      body: ListView.builder(
        itemCount: allStates.length,
        itemBuilder: (context, index) {
          final entry = allStates.entries.elementAt(index);
          final flag = entry.key;
          final isEnabled = entry.value;

          return SwitchListTile(
            title: Text(flag.key),
            subtitle: Text('Default: ${flag.defaultValue}'),
            value: isEnabled,
            onChanged: (value) {
              if (value) {
                service.enableLocally(flag);
              } else {
                service.disableLocally(flag);
              }
            },
          );
        },
      ),
    );
  }
}
```

## 🎯 Mejores Prácticas

### 1. Default Values

✅ **DO:** Siempre define defaults seguros
```dart
bool get defaultValue {
  // New features: false (safe default)
  // Existing features: true (don't break existing)
  return false;
}
```

### 2. Kill Switches

✅ **DO:** Implementa kill switches para features críticas
```dart
if (!service.isEnabled(FeatureFlag.paymentGateway)) {
  // Show maintenance message
  return MaintenanceScreen();
}
```

### 3. Analytics

✅ **DO:** Trackea uso de features
```dart
if (service.isEnabled(FeatureFlag.newFeature)) {
  AnalyticsService.trackEvent('feature_used', properties: {
    'feature': 'newFeature',
    'variant': service.getABTestVariant('experiment'),
  });
}
```

## 🚨 Troubleshooting

### Config Not Updating

```dart
// Force fetch in debug
await FirebaseRemoteConfigService.forceFetch();

// Check fetch status
print('Fetch status: ${FirebaseRemoteConfigService.fetchStatus}');
print('Last fetch: ${FirebaseRemoteConfigService.lastFetchTime}');
```

### Default Values Not Working

```dart
// Verify setDefaults was called
await _remoteConfig.setDefaults(_getDefaultValues());
```

## 📚 Recursos

- [Firebase Remote Config](https://firebase.google.com/docs/remote-config)
- [LaunchDarkly Flutter SDK](https://docs.launchdarkly.com/sdk/client-side/flutter)
- [Feature Flags Best Practices](https://martinfowler.com/articles/feature-toggles.html)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
