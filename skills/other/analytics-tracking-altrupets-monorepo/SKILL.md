# 📊 Skill: Analytics & Tracking

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-analytics-tracking` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `analytics`, `tracking`, `mixpanel`, `amplitude`, `firebase-analytics`, `events` |
| **Referencia** | [Firebase Analytics](https://firebase.google.com/docs/analytics) |

## 🔑 Keywords para Invocación

- `analytics`
- `tracking`
- `mixpanel`
- `amplitude`
- `firebase-analytics`
- `events`
- `user-tracking`
- `@skill:analytics`

### Ejemplos de Prompts

```
Implementa analytics con mixpanel y firebase-analytics
```

```
Setup tracking de eventos de usuario
```

```
Configura amplitude para product analytics
```

```
@skill:analytics - Sistema completo de analytics y tracking
```

## 📖 Descripción

Este skill cubre la implementación de analytics y tracking de eventos de usuario usando Firebase Analytics, Mixpanel, y Amplitude. Incluye tracking de eventos, propiedades de usuario, funnels, cohorts, y A/B testing.

### ✅ Cuándo Usar Este Skill

- Product analytics
- User behavior tracking
- Conversion funnels
- A/B testing
- Retention analytics
- Feature usage tracking
- Marketing attribution
- Revenue tracking

### ❌ Cuándo NO Usar Este Skill

- Apps sin usuarios reales
- Prototipos internos
- No necesitas métricas de uso

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── core/
│   │   └── analytics/
│   │       ├── analytics_service.dart
│   │       ├── firebase_analytics_service.dart
│   │       ├── mixpanel_service.dart
│   │       ├── amplitude_service.dart
│   │       ├── analytics_events.dart
│   │       └── analytics_properties.dart
│   │
│   ├── services/
│   │   └── tracking_service.dart
│   │
│   └── main.dart
│
└── test/
    └── analytics_test.dart
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Firebase Analytics
  firebase_core: ^2.24.2
  firebase_analytics: ^10.7.4

  # Mixpanel
  mixpanel_flutter: ^2.2.0

  # Amplitude
  amplitude_flutter: ^3.16.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.4
```

## 💻 Implementación

### 1. Event Definitions

```dart
// lib/core/analytics/analytics_events.dart
class AnalyticsEvents {
  // Authentication
  static const signUp = 'sign_up';
  static const signIn = 'login';
  static const signOut = 'logout';

  // User Actions
  static const viewItem = 'view_item';
  static const addToCart = 'add_to_cart';
  static const removeFromCart = 'remove_from_cart';
  static const beginCheckout = 'begin_checkout';
  static const purchase = 'purchase';

  // Content
  static const search = 'search';
  static const selectContent = 'select_content';
  static const share = 'share';

  // App Lifecycle
  static const appOpen = 'app_open';
  static const screenView = 'screen_view';
  static const tutorialBegin = 'tutorial_begin';
  static const tutorialComplete = 'tutorial_complete';

  // Engagement
  static const likePost = 'like_post';
  static const comment = 'comment';
  static const follow = 'follow';
  static const unfollow = 'unfollow';

  // Errors
  static const error = 'error';
  static const crashOccurred = 'crash_occurred';
}

class AnalyticsProperties {
  // Common
  static const userId = 'user_id';
  static const userEmail = 'user_email';
  static const userName = 'user_name';

  // Item properties
  static const itemId = 'item_id';
  static const itemName = 'item_name';
  static const itemCategory = 'item_category';
  static const itemPrice = 'price';
  static const currency = 'currency';
  static const quantity = 'quantity';

  // Screen
  static const screenName = 'screen_name';
  static const screenClass = 'screen_class';

  // Search
  static const searchTerm = 'search_term';
  static const searchResults = 'search_results';

  // Error
  static const errorMessage = 'error_message';
  static const errorCode = 'error_code';

  // Custom
  static const source = 'source';
  static const method = 'method';
  static const success = 'success';
}
```

### 2. Firebase Analytics Service

```dart
// lib/core/analytics/firebase_analytics_service.dart
import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:flutter/foundation.dart';

class FirebaseAnalyticsService {
  static final FirebaseAnalytics _analytics = FirebaseAnalytics.instance;
  static final FirebaseAnalyticsObserver _observer =
      FirebaseAnalyticsObserver(analytics: _analytics);

  static FirebaseAnalyticsObserver get observer => _observer;

  // Set user properties
  static Future<void> setUserId(String? id) async {
    await _analytics.setUserId(id: id);
  }

  static Future<void> setUserProperty(String name, String? value) async {
    await _analytics.setUserProperty(name: name, value: value);
  }

  // Log events
  static Future<void> logEvent(
    String name, {
    Map<String, Object?>? parameters,
  }) async {
    if (kDebugMode) {
      print('📊 Analytics Event: $name, Params: $parameters');
    }
    await _analytics.logEvent(name: name, parameters: parameters);
  }

  // Screen view
  static Future<void> logScreenView(String screenName) async {
    await _analytics.logScreenView(
      screenName: screenName,
      screenClass: screenName,
    );
  }

  // Predefined events
  static Future<void> logSignUp({String? method}) async {
    await _analytics.logSignUp(signUpMethod: method ?? 'email');
  }

  static Future<void> logLogin({String? method}) async {
    await _analytics.logLogin(loginMethod: method ?? 'email');
  }

  static Future<void> logSearch(String searchTerm) async {
    await _analytics.logSearch(searchTerm: searchTerm);
  }

  static Future<void> logSelectContent({
    required String contentType,
    required String itemId,
  }) async {
    await _analytics.logSelectContent(
      contentType: contentType,
      itemId: itemId,
    );
  }

  static Future<void> logShare({
    required String contentType,
    required String itemId,
    String? method,
  }) async {
    await _analytics.logShare(
      contentType: contentType,
      itemId: itemId,
      method: method,
    );
  }

  // E-commerce events
  static Future<void> logAddToCart({
    required String itemId,
    required String itemName,
    required double value,
    String? currency,
  }) async {
    await _analytics.logAddToCart(
      value: value,
      currency: currency ?? 'USD',
      items: [
        AnalyticsEventItem(
          itemId: itemId,
          itemName: itemName,
          price: value,
        ),
      ],
    );
  }

  static Future<void> logPurchase({
    required String transactionId,
    required double value,
    required String currency,
    required List<AnalyticsEventItem> items,
  }) async {
    await _analytics.logPurchase(
      transactionId: transactionId,
      value: value,
      currency: currency,
      items: items,
    );
  }

  static Future<void> logBeginCheckout({
    required double value,
    required String currency,
    required List<AnalyticsEventItem> items,
  }) async {
    await _analytics.logBeginCheckout(
      value: value,
      currency: currency,
      items: items,
    );
  }

  // App lifecycle
  static Future<void> logAppOpen() async {
    await _analytics.logAppOpen();
  }

  static Future<void> logTutorialBegin() async {
    await _analytics.logTutorialBegin();
  }

  static Future<void> logTutorialComplete() async {
    await _analytics.logTutorialComplete();
  }

  // Set user properties for segmentation
  static Future<void> setUserProperties({
    String? userType,
    String? subscription,
    String? country,
  }) async {
    if (userType != null) {
      await setUserProperty('user_type', userType);
    }
    if (subscription != null) {
      await setUserProperty('subscription', subscription);
    }
    if (country != null) {
      await setUserProperty('country', country);
    }
  }
}
```

### 3. Mixpanel Service

```dart
// lib/core/analytics/mixpanel_service.dart
import 'package:mixpanel_flutter/mixpanel_flutter.dart';
import 'package:flutter/foundation.dart';

class MixpanelService {
  static Mixpanel? _mixpanel;

  static Future<void> initialize(String token) async {
    _mixpanel = await Mixpanel.init(
      token,
      trackAutomaticEvents: true,
    );
  }

  // Identify user
  static void identify(String userId) {
    _mixpanel?.identify(userId);
  }

  // Set user properties (People properties)
  static void setUserProperties(Map<String, dynamic> properties) {
    _mixpanel?.getPeople().set('\$name', properties['name']);
    _mixpanel?.getPeople().set('\$email', properties['email']);

    properties.forEach((key, value) {
      if (key != 'name' && key != 'email') {
        _mixpanel?.getPeople().set(key, value);
      }
    });
  }

  // Increment user property
  static void incrementUserProperty(String property, [double by = 1]) {
    _mixpanel?.getPeople().increment(property, by);
  }

  // Track event
  static void track(String eventName, [Map<String, dynamic>? properties]) {
    if (kDebugMode) {
      print('📊 Mixpanel Event: $eventName, Props: $properties');
    }
    _mixpanel?.track(eventName, properties: properties);
  }

  // Track with revenue
  static void trackCharge(double amount, [Map<String, dynamic>? properties]) {
    _mixpanel?.getPeople().trackCharge(amount, properties: properties);
  }

  // Time event (for measuring duration)
  static void timeEvent(String eventName) {
    _mixpanel?.timeEvent(eventName);
  }

  // Register super properties (sent with every event)
  static void registerSuperProperties(Map<String, dynamic> properties) {
    _mixpanel?.registerSuperProperties(properties);
  }

  // Unregister super property
  static void unregisterSuperProperty(String propertyName) {
    _mixpanel?.unregisterSuperProperty(propertyName);
  }

  // Clear super properties
  static void clearSuperProperties() {
    _mixpanel?.clearSuperProperties();
  }

  // Alias user (link anonymous ID to identified ID)
  static void alias(String alias, String originalId) {
    _mixpanel?.alias(alias, originalId);
  }

  // Reset (clear all user data)
  static void reset() {
    _mixpanel?.reset();
  }

  // Flush events (send immediately)
  static void flush() {
    _mixpanel?.flush();
  }

  // Get distinct ID
  static Future<String?> getDistinctId() async {
    return await _mixpanel?.getDistinctId();
  }
}
```

### 4. Amplitude Service

```dart
// lib/core/analytics/amplitude_service.dart
import 'package:amplitude_flutter/amplitude.dart';
import 'package:amplitude_flutter/identify.dart';
import 'package:flutter/foundation.dart';

class AmplitudeService {
  static final Amplitude _amplitude = Amplitude.getInstance();

  static Future<void> initialize(String apiKey) async {
    await _amplitude.init(apiKey);

    // Enable tracking
    await _amplitude.enableCoppaControl();
    await _amplitude.trackingSessionEvents(true);
  }

  // Set user ID
  static Future<void> setUserId(String userId) async {
    await _amplitude.setUserId(userId);
  }

  // Set user properties
  static Future<void> setUserProperties(Map<String, dynamic> properties) async {
    final identify = Identify();

    properties.forEach((key, value) {
      if (value is String) {
        identify.set(key, value);
      } else if (value is int) {
        identify.set(key, value);
      } else if (value is double) {
        identify.set(key, value);
      } else if (value is bool) {
        identify.set(key, value);
      } else if (value is List) {
        identify.set(key, value);
      }
    });

    await _amplitude.identify(identify);
  }

  // Increment user property
  static Future<void> incrementUserProperty(String property, int by) async {
    final identify = Identify()..add(property, by);
    await _amplitude.identify(identify);
  }

  // Append to user property array
  static Future<void> appendToUserProperty(String property, dynamic value) async {
    final identify = Identify()..append(property, value);
    await _amplitude.identify(identify);
  }

  // Track event
  static Future<void> track(
    String eventName, {
    Map<String, dynamic>? properties,
  }) async {
    if (kDebugMode) {
      print('📊 Amplitude Event: $eventName, Props: $properties');
    }
    await _amplitude.logEvent(eventName, eventProperties: properties);
  }

  // Track revenue
  static Future<void> trackRevenue({
    required String productId,
    required int quantity,
    required double price,
  }) async {
    await _amplitude.logRevenue(productId, quantity, price);
  }

  // Track revenue with receipt (iOS)
  static Future<void> trackRevenueWithReceipt({
    required String productId,
    required int quantity,
    required double price,
    required String receipt,
  }) async {
    await _amplitude.logRevenueAmount(productId, quantity, price, receipt, null);
  }

  // Set user property once (won't override existing)
  static Future<void> setUserPropertyOnce(String property, dynamic value) async {
    final identify = Identify()..setOnce(property, value);
    await _amplitude.identify(identify);
  }

  // Unset user property
  static Future<void> unsetUserProperty(String property) async {
    final identify = Identify()..unset(property);
    await _amplitude.identify(identify);
  }

  // Clear user properties
  static Future<void> clearUserProperties() async {
    final identify = Identify()..clearAll();
    await _amplitude.identify(identify);
  }

  // Set group
  static Future<void> setGroup(String groupType, dynamic groupName) async {
    await _amplitude.setGroup(groupType, groupName);
  }

  // Regenerate device ID
  static Future<void> regenerateDeviceId() async {
    await _amplitude.regenerateDeviceId();
  }

  // Get device ID
  static Future<String?> getDeviceId() async {
    return await _amplitude.getDeviceId();
  }

  // Upload events
  static Future<void> uploadEvents() async {
    await _amplitude.uploadEvents();
  }
}
```

### 5. Unified Analytics Service

```dart
// lib/core/analytics/analytics_service.dart
import 'package:flutter/foundation.dart';
import 'firebase_analytics_service.dart';
import 'mixpanel_service.dart';
import 'amplitude_service.dart';
import 'analytics_events.dart';

class AnalyticsService {
  static bool _initialized = false;

  static Future<void> initialize({
    required String mixpanelToken,
    required String amplitudeApiKey,
  }) async {
    if (_initialized) return;

    // Initialize Mixpanel
    await MixpanelService.initialize(mixpanelToken);

    // Initialize Amplitude
    await AmplitudeService.initialize(amplitudeApiKey);

    // Firebase Analytics is initialized with Firebase Core

    _initialized = true;
  }

  // Identify user across all platforms
  static Future<void> identifyUser({
    required String userId,
    String? email,
    String? name,
    Map<String, dynamic>? properties,
  }) async {
    // Firebase
    await FirebaseAnalyticsService.setUserId(userId);
    if (properties != null) {
      await FirebaseAnalyticsService.setUserProperties(
        userType: properties['user_type'],
        subscription: properties['subscription'],
        country: properties['country'],
      );
    }

    // Mixpanel
    MixpanelService.identify(userId);
    final mixpanelProps = {
      'name': name,
      'email': email,
      ...?properties,
    };
    MixpanelService.setUserProperties(mixpanelProps);

    // Amplitude
    await AmplitudeService.setUserId(userId);
    await AmplitudeService.setUserProperties(mixpanelProps);
  }

  // Track event across all platforms
  static Future<void> trackEvent(
    String eventName, {
    Map<String, dynamic>? properties,
  }) async {
    if (kDebugMode) {
      print('📊 Track Event: $eventName');
      print('   Properties: $properties');
    }

    await Future.wait([
      FirebaseAnalyticsService.logEvent(eventName, parameters: properties),
      Future.sync(() => MixpanelService.track(eventName, properties)),
      AmplitudeService.track(eventName, properties: properties),
    ]);
  }

  // Screen view
  static Future<void> trackScreenView(String screenName) async {
    await trackEvent(
      AnalyticsEvents.screenView,
      properties: {
        AnalyticsProperties.screenName: screenName,
      },
    );
    await FirebaseAnalyticsService.logScreenView(screenName);
  }

  // Track purchase
  static Future<void> trackPurchase({
    required String transactionId,
    required List<PurchaseItem> items,
    required double totalValue,
    String currency = 'USD',
  }) async {
    // Firebase
    await FirebaseAnalyticsService.logPurchase(
      transactionId: transactionId,
      value: totalValue,
      currency: currency,
      items: items
          .map((item) => AnalyticsEventItem(
                itemId: item.id,
                itemName: item.name,
                price: item.price,
                quantity: item.quantity,
              ))
          .toList(),
    );

    // Mixpanel
    MixpanelService.trackCharge(totalValue, {
      'transaction_id': transactionId,
      'currency': currency,
      'items': items.length,
    });

    // Amplitude
    for (final item in items) {
      await AmplitudeService.trackRevenue(
        productId: item.id,
        quantity: item.quantity,
        price: item.price,
      );
    }
  }

  // Clear user data (on logout)
  static Future<void> clearUser() async {
    await FirebaseAnalyticsService.setUserId(null);
    MixpanelService.reset();
    await AmplitudeService.clearUserProperties();
  }

  // Flush events (send immediately)
  static void flush() {
    MixpanelService.flush();
    AmplitudeService.uploadEvents();
  }
}

class PurchaseItem {
  final String id;
  final String name;
  final double price;
  final int quantity;

  PurchaseItem({
    required this.id,
    required this.name,
    required this.price,
    this.quantity = 1,
  });
}
```

### 6. Usage Examples

```dart
// In main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp();

  await AnalyticsService.initialize(
    mixpanelToken: 'YOUR_MIXPANEL_TOKEN',
    amplitudeApiKey: 'YOUR_AMPLITUDE_API_KEY',
  );

  // Track app open
  await AnalyticsService.trackEvent(AnalyticsEvents.appOpen);

  runApp(MyApp());
}

// In authentication flow
Future<void> onUserSignIn(User user) async {
  await AnalyticsService.identifyUser(
    userId: user.id,
    email: user.email,
    name: user.name,
    properties: {
      'user_type': user.isPremium ? 'premium' : 'free',
      'signup_date': user.createdAt.toIso8601String(),
    },
  );

  await AnalyticsService.trackEvent(
    AnalyticsEvents.signIn,
    properties: {
      AnalyticsProperties.method: 'email',
    },
  );
}

// In product screen
Future<void> onProductViewed(Product product) async {
  await AnalyticsService.trackEvent(
    AnalyticsEvents.viewItem,
    properties: {
      AnalyticsProperties.itemId: product.id,
      AnalyticsProperties.itemName: product.name,
      AnalyticsProperties.itemCategory: product.category,
      AnalyticsProperties.itemPrice: product.price,
    },
  );
}

// In checkout flow
Future<void> onPurchaseCompleted(Order order) async {
  await AnalyticsService.trackPurchase(
    transactionId: order.id,
    items: order.items
        .map((item) => PurchaseItem(
              id: item.productId,
              name: item.productName,
              price: item.price,
              quantity: item.quantity,
            ))
        .toList(),
    totalValue: order.total,
    currency: order.currency,
  );
}
```

## 🎯 Mejores Prácticas

### 1. Consistent Naming

✅ **DO:** Usa naming conventions consistentes
```dart
// Good: snake_case for event names
const String BUTTON_CLICKED = 'button_clicked';
const String SCREEN_VIEWED = 'screen_viewed';
const String PURCHASE_COMPLETED = 'purchase_completed';
```

### 2. Event Properties

✅ **DO:** Incluye contexto relevante
```dart
await AnalyticsService.trackEvent(
  'product_purchased',
  properties: {
    'product_id': '123',
    'product_name': 'Premium Plan',
    'price': 29.99,
    'currency': 'USD',
    'source': 'in_app_banner',
    'discount_applied': true,
  },
);
```

### 3. Privacy Compliance

✅ **DO:** Respeta la privacidad del usuario
```dart
// Allow users to opt-out
Future<void> setAnalyticsEnabled(bool enabled) async {
  await FirebaseAnalytics.instance.setAnalyticsCollectionEnabled(enabled);
  // También deshabilitar Mixpanel y Amplitude
}
```

## 🚨 Troubleshooting

### Events Not Appearing in Dashboard

```dart
// Force flush events
AnalyticsService.flush();

// Check if analytics is enabled
await FirebaseAnalytics.instance.setAnalyticsCollectionEnabled(true);
```

### Debugging Events

```dart
// Enable debug mode
if (kDebugMode) {
  // Firebase: adb shell setprop debug.firebase.analytics.app com.example.myapp
  // Mixpanel: Enable debug logging
  // Amplitude: Check console logs
}
```

## 📚 Recursos

- [Firebase Analytics](https://firebase.google.com/docs/analytics)
- [Mixpanel Documentation](https://developer.mixpanel.com/)
- [Amplitude Developer Docs](https://www.docs.developers.amplitude.com/)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
