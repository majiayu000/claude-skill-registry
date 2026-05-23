# 🔥 Skill: Firebase Integration

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-firebase` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 2.0.0 |
| **Keywords** | `firebase`, `firestore`, `auth`, `cloud-messaging`, `analytics`, `storage`, `remote-config`, `crashlytics`, `provider` |
| **Referencia** | [FlutterFire](https://firebase.flutter.dev/) |

## 🔑 Keywords para Invocación

- `firebase`
- `firestore`
- `firebase-auth`
- `cloud-messaging`
- `firebase-analytics`
- `firebase-storage`
- `firebase-remote-config`
- `firebase-crashlytics`
- `provider`
- `@skill:firebase`

### Ejemplos de Prompts

```
Integra Firebase con auth y Firestore
```

```
Implementa Firebase Authentication y Cloud Messaging
```

```
@skill:firebase - Configura Firebase completo
```

## 📖 Descripción

Firebase Integration proporciona servicios backend completos: Authentication (Email/Password y Google Sign-In), Firestore Database, Cloud Storage, Push Notifications (FCM), Analytics (con tracking de screens, eventos personalizados, user ID y propiedades), Crashlytics y Remote Config. Incluye integración con Provider para state management y configuración multiplataforma con mejores prácticas.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

**⚠️ IMPORTANTE:** Todos los comandos de este skill deben ejecutarse desde la **raíz del proyecto** (donde existe el directorio `mobile/`). El skill incluye verificaciones para asegurar que se está en el directorio correcto antes de ejecutar cualquier comando.

### ✅ Cuándo Usar Este Skill

- Backend as a Service rápido
- Authentication con múltiples providers
- Base de datos en tiempo real
- Push notifications
- Analytics y Crashlytics
- Remote Config para A/B testing
- Rapid prototyping

### ❌ Cuándo NO Usar Este Skill

- Requieres control total del backend
- Costos de Firebase son prohibitivos
- Backend custom ya existe

## 🏗️ Estructura del Proyecto

```
lib/
├── core/
│   ├── firebase/
│   │   ├── firebase_options.dart (generado)
│   │   ├── firebase_config.dart
│   │   └── firebase_initialization.dart
│   └── services/
│       ├── analytics_service.dart
│       ├── crashlytics_service.dart
│       ├── remote_config_service.dart
│       └── storage_service.dart
│
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   └── firebase_auth_datasource.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository.dart
│   │   └── presentation/
│   │       ├── screens/
│   │       │   └── login_screen.dart
│   │       ├── providers/
│   │       │   └── auth_provider.dart
│   │       └── bloc/
│   │           └── auth_bloc.dart
│   │
│   ├── products/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   └── firestore_products_datasource.dart
│   │   │   └── models/
│   │   │       └── product_model.dart
│   │   └── domain/
│   │       └── entities/
│   │           └── product.dart
│   │
│   └── notifications/
│       ├── data/
│       │   ├── datasources/
│       │   │   └── fcm_datasource.dart
│       │   └── services/
│       │       └── notification_service.dart
│       └── presentation/
│           └── screens/
│               └── notifications_screen.dart
│
└── main.dart
```

## 📦 Dependencias Requeridas

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Firebase Core
  firebase_core: ^2.24.2

  # Firebase Authentication
  firebase_auth: ^4.15.3
  google_sign_in: ^6.2.1

  # Cloud Firestore
  cloud_firestore: ^4.13.6

  # Cloud Storage
  firebase_storage: ^11.5.6

  # Cloud Messaging
  firebase_messaging: ^14.7.9
  flutter_local_notifications: ^16.3.0

  # Firebase Analytics
  firebase_analytics: ^10.7.4

  # Crashlytics
  firebase_crashlytics: ^3.4.8

  # Remote Config
  firebase_remote_config: ^4.3.8

  # State Management
  provider: ^6.1.1

  # Image Picker (para Storage)
  image_picker: ^1.0.7

  # Utils
  equatable: ^2.0.5
  dartz: ^0.10.1

dev_dependencies:
  flutter_test:
    sdk: flutter
```

## ⚙️ Configuración Inicial

### 1. Firebase CLI Setup

```bash
# Instalar Firebase CLI
npm install -g firebase-tools

# Login a Firebase
firebase login

# Verificar que estamos en la raíz del proyecto
if [ ! -d "mobile" ]; then
    echo "Error: Ejecuta este comando desde la raíz del proyecto"
    exit 1
fi

# Instalar FlutterFire CLI
dart pub global activate flutterfire_cli

# Configurar Firebase para el proyecto
cd mobile
flutterfire configure
cd ..
flutterfire configure
```

### 2. Android Configuration

```gradle
// android/build.gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
        classpath 'com.google.firebase:firebase-crashlytics-gradle:2.9.9'
    }
}
```

```gradle
// android/app/build.gradle
apply plugin: 'com.google.gms.google-services'
apply plugin: 'com.google.firebase.crashlytics'

android {
    defaultConfig {
        minSdkVersion 21  // Firebase requires 21+
    }
}
```

### 3. iOS Configuration

```ruby
# ios/Podfile
platform :ios, '13.0'  # Firebase requires 13.0+

# Después de flutter_install_all_ios_pods
post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
    target.build_configurations.each do |config|
      config.build_settings['IPHONEOS_DEPLOYMENT_TARGET'] = '13.0'
    end
  end
end
```

## 💻 Implementación

### 1. Firebase Initialization

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Pass all uncaught errors to Crashlytics
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;

  runApp(const MyApp());
}
```

### 2. Firebase Authentication

```dart
// lib/features/authentication/data/datasources/firebase_auth_datasource.dart
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:google_sign_in/google_sign_in.dart';
import '../models/user_model.dart';

abstract class FirebaseAuthDataSource {
  Stream<UserModel?> get authStateChanges;
  Future<UserModel> signInWithEmailAndPassword(String email, String password);
  Future<UserModel> signUpWithEmailAndPassword(String email, String password);
  Future<UserModel> signInWithGoogle();
  Future<void> signOut();
  Future<void> sendPasswordResetEmail(String email);
  UserModel? getCurrentUser();
}

class FirebaseAuthDataSourceImpl implements FirebaseAuthDataSource {
  final firebase_auth.FirebaseAuth _firebaseAuth;
  final GoogleSignIn _googleSignIn;

  FirebaseAuthDataSourceImpl({
    firebase_auth.FirebaseAuth? firebaseAuth,
    GoogleSignIn? googleSignIn,
  })  : _firebaseAuth = firebaseAuth ?? firebase_auth.FirebaseAuth.instance,
        _googleSignIn = googleSignIn ?? GoogleSignIn();

  @override
  Stream<UserModel?> get authStateChanges {
    return _firebaseAuth.authStateChanges().map((firebaseUser) {
      return firebaseUser != null ? UserModel.fromFirebaseUser(firebaseUser) : null;
    });
  }

  @override
  Future<UserModel> signInWithEmailAndPassword(
    String email,
    String password,
  ) async {
    try {
      final credential = await _firebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );

      if (credential.user == null) {
        throw Exception('Sign in failed');
      }

      return UserModel.fromFirebaseUser(credential.user!);
    } on firebase_auth.FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    }
  }

  @override
  Future<UserModel> signUpWithEmailAndPassword(
    String email,
    String password,
  ) async {
    try {
      final credential = await _firebaseAuth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );

      if (credential.user == null) {
        throw Exception('Sign up failed');
      }

      return UserModel.fromFirebaseUser(credential.user!);
    } on firebase_auth.FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    }
  }

  @override
  Future<UserModel> signInWithGoogle() async {
    try {
      // Trigger the authentication flow
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();

      if (googleUser == null) {
        throw Exception('Google sign in was cancelled');
      }

      // Obtain the auth details from the request
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;

      // Create a new credential
      final credential = firebase_auth.GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );

      // Sign in to Firebase with the Google credential
      final userCredential = await _firebaseAuth.signInWithCredential(credential);

      if (userCredential.user == null) {
        throw Exception('Google sign in failed');
      }

      return UserModel.fromFirebaseUser(userCredential.user!);
    } on firebase_auth.FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    } catch (e) {
      throw Exception('Google sign in failed: $e');
    }
  }

  @override
  Future<void> signOut() async {
    await Future.wait([
      _firebaseAuth.signOut(),
      _googleSignIn.signOut(),
    ]);
  }

  @override
  Future<void> sendPasswordResetEmail(String email) async {
    try {
      await _firebaseAuth.sendPasswordResetEmail(email: email);
    } on firebase_auth.FirebaseAuthException catch (e) {
      throw _handleAuthException(e);
    }
  }

  @override
  UserModel? getCurrentUser() {
    final firebaseUser = _firebaseAuth.currentUser;
    return firebaseUser != null ? UserModel.fromFirebaseUser(firebaseUser) : null;
  }

  Exception _handleAuthException(firebase_auth.FirebaseAuthException e) {
    switch (e.code) {
      case 'user-not-found':
        return Exception('No user found with this email');
      case 'wrong-password':
        return Exception('Wrong password');
      case 'email-already-in-use':
        return Exception('Email already in use');
      case 'weak-password':
        return Exception('Password is too weak');
      case 'invalid-email':
        return Exception('Invalid email format');
      default:
        return Exception('Authentication failed: ${e.message}');
    }
  }
}
```

### 3. Cloud Firestore

```dart
// lib/features/products/data/datasources/firestore_products_datasource.dart
import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/product_model.dart';

abstract class FirestoreProductsDataSource {
  Stream<List<ProductModel>> getProductsStream();
  Future<List<ProductModel>> getProducts();
  Future<ProductModel> getProduct(String id);
  Future<ProductModel> createProduct(ProductModel product);
  Future<ProductModel> updateProduct(ProductModel product);
  Future<void> deleteProduct(String id);
}

class FirestoreProductsDataSourceImpl implements FirestoreProductsDataSource {
  final FirebaseFirestore _firestore;
  static const String _collection = 'products';

  FirestoreProductsDataSourceImpl({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  @override
  Stream<List<ProductModel>> getProductsStream() {
    return _firestore
        .collection(_collection)
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs
          .map((doc) => ProductModel.fromFirestore(doc))
          .toList();
    });
  }

  @override
  Future<List<ProductModel>> getProducts() async {
    final snapshot = await _firestore
        .collection(_collection)
        .orderBy('createdAt', descending: true)
        .get();

    return snapshot.docs
        .map((doc) => ProductModel.fromFirestore(doc))
        .toList();
  }

  @override
  Future<ProductModel> getProduct(String id) async {
    final doc = await _firestore.collection(_collection).doc(id).get();

    if (!doc.exists) {
      throw Exception('Product not found');
    }

    return ProductModel.fromFirestore(doc);
  }

  @override
  Future<ProductModel> createProduct(ProductModel product) async {
    final docRef = _firestore.collection(_collection).doc();

    final productWithId = product.copyWith(
      id: docRef.id,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );

    await docRef.set(productWithId.toFirestore());

    return productWithId;
  }

  @override
  Future<ProductModel> updateProduct(ProductModel product) async {
    final productWithTimestamp = product.copyWith(
      updatedAt: DateTime.now(),
    );

    await _firestore
        .collection(_collection)
        .doc(product.id)
        .update(productWithTimestamp.toFirestore());

    return productWithTimestamp;
  }

  @override
  Future<void> deleteProduct(String id) async {
    await _firestore.collection(_collection).doc(id).delete();
  }
}

// ProductModel extension for Firestore
extension ProductModelFirestore on ProductModel {
  static ProductModel fromFirestore(DocumentSnapshot doc) {
    final data = doc.data() as Map<String, dynamic>;

    return ProductModel(
      id: doc.id,
      name: data['name'] as String,
      description: data['description'] as String,
      price: (data['price'] as num).toDouble(),
      imageUrl: data['imageUrl'] as String,
      stock: data['stock'] as int,
      createdAt: (data['createdAt'] as Timestamp).toDate(),
      updatedAt: (data['updatedAt'] as Timestamp).toDate(),
    );
  }

  Map<String, dynamic> toFirestore() {
    return {
      'name': name,
      'description': description,
      'price': price,
      'imageUrl': imageUrl,
      'stock': stock,
      'createdAt': Timestamp.fromDate(createdAt),
      'updatedAt': Timestamp.fromDate(updatedAt),
    };
  }
}
```

### 4. Cloud Messaging (Push Notifications)

```dart
// lib/features/notifications/data/services/fcm_service.dart
import 'dart:io';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

// Handler para mensajes en background
@pragma('vm:entry-point')
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  print('Handling background message: ${message.messageId}');
}

class FCMService {
  final FirebaseMessaging _messaging;
  final FlutterLocalNotificationsPlugin _localNotifications;

  FCMService({
    FirebaseMessaging? messaging,
    FlutterLocalNotificationsPlugin? localNotifications,
  })  : _messaging = messaging ?? FirebaseMessaging.instance,
        _localNotifications =
            localNotifications ?? FlutterLocalNotificationsPlugin();

  Future<void> initialize() async {
    // Request permission (iOS)
    await _requestPermission();

    // Initialize local notifications
    await _initializeLocalNotifications();

    // Get FCM token
    final token = await _messaging.getToken();
    print('FCM Token: $token');

    // Listen to token refresh
    _messaging.onTokenRefresh.listen((newToken) {
      print('FCM Token refreshed: $newToken');
      // Send token to your backend
    });

    // Handle foreground messages
    FirebaseMessaging.onMessage.listen(_handleForegroundMessage);

    // Handle notification tap when app is in background
    FirebaseMessaging.onMessageOpenedApp.listen(_handleNotificationTap);

    // Handle notification tap when app is terminated
    final initialMessage = await _messaging.getInitialMessage();
    if (initialMessage != null) {
      _handleNotificationTap(initialMessage);
    }

    // Set background handler
    FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);
  }

  Future<void> _requestPermission() async {
    final settings = await _messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
      provisional: false,
    );

    print('Permission granted: ${settings.authorizationStatus}');
  }

  Future<void> _initializeLocalNotifications() async {
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');
    const iosSettings = DarwinInitializationSettings();

    const settings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    await _localNotifications.initialize(
      settings,
      onDidReceiveNotificationResponse: (details) {
        print('Notification tapped: ${details.payload}');
      },
    );

    // Create notification channel (Android)
    if (Platform.isAndroid) {
      const channel = AndroidNotificationChannel(
        'high_importance_channel',
        'High Importance Notifications',
        description: 'This channel is used for important notifications.',
        importance: Importance.high,
      );

      await _localNotifications
          .resolvePlatformSpecificImplementation<
              AndroidFlutterLocalNotificationsPlugin>()
          ?.createNotificationChannel(channel);
    }
  }

  Future<void> _handleForegroundMessage(RemoteMessage message) async {
    print('Foreground message: ${message.messageId}');

    // Show local notification
    await _showLocalNotification(message);
  }

  Future<void> _showLocalNotification(RemoteMessage message) async {
    final notification = message.notification;
    if (notification == null) return;

    await _localNotifications.show(
      notification.hashCode,
      notification.title,
      notification.body,
      const NotificationDetails(
        android: AndroidNotificationDetails(
          'high_importance_channel',
          'High Importance Notifications',
          importance: Importance.high,
          priority: Priority.high,
        ),
        iOS: DarwinNotificationDetails(),
      ),
      payload: message.data.toString(),
    );
  }

  void _handleNotificationTap(RemoteMessage message) {
    print('Notification tapped: ${message.messageId}');
    // Navigate to specific screen based on message data
  }

  Future<String?> getToken() async {
    return await _messaging.getToken();
  }

  Future<void> subscribeToTopic(String topic) async {
    await _messaging.subscribeToTopic(topic);
  }

  Future<void> unsubscribeFromTopic(String topic) async {
    await _messaging.unsubscribeFromTopic(topic);
  }
}
```

### 5. Firebase Analytics

Firebase Analytics permite rastrear el comportamiento de los usuarios, eventos personalizados, nombres de pantallas, user ID y propiedades de usuario.

**Características principales:**
- ✅ Tracking automático de nombres de pantallas
- ✅ Eventos personalizados con parámetros
- ✅ Configuración de User ID
- ✅ Propiedades de usuario personalizadas

```dart
// lib/core/services/analytics_service.dart
import 'package:firebase_analytics/firebase_analytics.dart';
import 'package:flutter/material.dart';

class AnalyticsService {
  final FirebaseAnalytics _analytics;

  AnalyticsService({FirebaseAnalytics? analytics})
      : _analytics = analytics ?? FirebaseAnalytics.instance;

  // Observer para tracking automático de screens
  FirebaseAnalyticsObserver get observer =>
      FirebaseAnalyticsObserver(analytics: _analytics);

  // Track screen view con nombre personalizado
  Future<void> logScreenView({
    required String screenName,
    String? screenClass,
  }) async {
    await _analytics.logScreenView(
      screenName: screenName,
      screenClass: screenClass ?? screenName,
    );
  }

  // Track custom events con parámetros
  Future<void> logCustomEvent({
    required String eventName,
    Map<String, Object?>? parameters,
  }) async {
    await _analytics.logEvent(
      name: eventName,
      parameters: parameters,
    );
  }

  // Set user ID (debe llamarse después del login)
  Future<void> setUserId(String userId) async {
    await _analytics.setUserId(id: userId);
  }

  // Clear user ID (debe llamarse en logout)
  Future<void> clearUserId() async {
    await _analytics.setUserId(id: null);
  }

  // Set user properties (máximo 25 propiedades)
  Future<void> setUserProperty({
    required String name,
    required String? value,
  }) async {
    await _analytics.setUserProperty(name: name, value: value);
  }

  // Set multiple user properties
  Future<void> setUserProperties(Map<String, String?> properties) async {
    for (final entry in properties.entries) {
      await setUserProperty(name: entry.key, value: entry.value);
    }
  }

  // E-commerce events
  Future<void> logAddToCart({
    required String productId,
    required String productName,
    required double price,
    String currency = 'USD',
  }) async {
    await _analytics.logAddToCart(
      currency: currency,
      value: price,
      items: [
        AnalyticsEventItem(
          itemId: productId,
          itemName: productName,
          price: price,
        ),
      ],
    );
  }

  Future<void> logPurchase({
    required double value,
    required List<AnalyticsEventItem> items,
    String currency = 'USD',
    String? transactionId,
  }) async {
    await _analytics.logPurchase(
      currency: currency,
      value: value,
      items: items,
      transactionId: transactionId,
    );
  }

  // Authentication events
  Future<void> logLogin({required String method}) async {
    await _analytics.logLogin(loginMethod: method);
  }

  Future<void> logSignUp({required String method}) async {
    await _analytics.logSignUp(signUpMethod: method);
  }
}

// Uso con NavigatorObserver para tracking automático de screens
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    final analyticsService = AnalyticsService();

    return MaterialApp(
      title: 'Firebase App',
      navigatorObservers: [
        analyticsService.observer, // Tracking automático de screens
      ],
      home: const HomeScreen(),
    );
  }
}

// Ejemplo de uso en un widget
class ProductScreen extends StatelessWidget {
  const ProductScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final analytics = AnalyticsService();

    // Track screen view manualmente (si no usas observer)
    WidgetsBinding.instance.addPostFrameCallback((_) {
      analytics.logScreenView(screenName: 'product_detail');
    });

    return Scaffold(
      appBar: AppBar(title: const Text('Product')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // Track custom event
            analytics.logCustomEvent(
              eventName: 'product_viewed',
              parameters: {
                'product_id': '123',
                'product_name': 'Example Product',
                'product_category': 'Electronics',
              },
            );
          },
          child: const Text('View Product'),
        ),
      ),
    );
  }
}

// Ejemplo de configuración de user properties después del login
class AuthService {
  final AnalyticsService _analytics = AnalyticsService();

  Future<void> onUserLogin(String userId, Map<String, String> userData) async {
    // Set user ID
    await _analytics.setUserId(userId);

    // Set user properties
    await _analytics.setUserProperties({
      'user_type': userData['type'] ?? 'regular',
      'subscription_status': userData['subscription'] ?? 'free',
      'sign_up_method': userData['method'] ?? 'email',
    });

    // Log login event
    await _analytics.logLogin(method: userData['method'] ?? 'email');
  }

  Future<void> onUserLogout() async {
    // Clear user ID
    await _analytics.clearUserId();
  }
}
```

### 6. Crashlytics

```dart
// lib/core/services/crashlytics_service.dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:flutter/foundation.dart';

class CrashlyticsService {
  final FirebaseCrashlytics _crashlytics;

  CrashlyticsService({FirebaseCrashlytics? crashlytics})
      : _crashlytics = crashlytics ?? FirebaseCrashlytics.instance;

  Future<void> initialize() async {
    // Enable collection in production only
    await _crashlytics.setCrashlyticsCollectionEnabled(!kDebugMode);
  }

  void logError(dynamic exception, StackTrace? stackTrace, {String? reason}) {
    _crashlytics.recordError(
      exception,
      stackTrace,
      reason: reason,
      fatal: false,
    );
  }

  void logFatalError(dynamic exception, StackTrace stackTrace, {String? reason}) {
    _crashlytics.recordError(
      exception,
      stackTrace,
      reason: reason,
      fatal: true,
    );
  }

  Future<void> log(String message) async {
    await _crashlytics.log(message);
  }

  Future<void> setCustomKey(String key, Object value) async {
    await _crashlytics.setCustomKey(key, value);
  }

  Future<void> setUserId(String userId) async {
    await _crashlytics.setUserIdentifier(userId);
  }
}
```

### 7. Remote Config

```dart
// lib/core/services/remote_config_service.dart
import 'package:firebase_remote_config/firebase_remote_config.dart';

class RemoteConfigService {
  final FirebaseRemoteConfig _remoteConfig;

  RemoteConfigService({FirebaseRemoteConfig? remoteConfig})
      : _remoteConfig = remoteConfig ?? FirebaseRemoteConfig.instance;

  Future<void> initialize() async {
    await _remoteConfig.setConfigSettings(
      RemoteConfigSettings(
        fetchTimeout: const Duration(seconds: 10),
        minimumFetchInterval: const Duration(hours: 1),
      ),
    );

    // Set default values
    await _remoteConfig.setDefaults({
      'feature_enabled': false,
      'max_items_per_page': 20,
      'app_version': '1.0.0',
      'maintenance_mode': false,
    });

    // Fetch and activate
    await fetchAndActivate();
  }

  Future<bool> fetchAndActivate() async {
    try {
      final fetched = await _remoteConfig.fetchAndActivate();
      return fetched;
    } catch (e) {
      print('Error fetching remote config: $e');
      return false;
    }
  }

  // Get values
  bool getBool(String key) => _remoteConfig.getBool(key);
  String getString(String key) => _remoteConfig.getString(key);
  int getInt(String key) => _remoteConfig.getInt(key);
  double getDouble(String key) => _remoteConfig.getDouble(key);

  // Listen to config updates
  Stream<void> get onConfigUpdated => _remoteConfig.onConfigUpdated;

  // Force fetch
  Future<void> fetch() async {
    await _remoteConfig.fetch();
  }

  // Activate fetched values
  Future<bool> activate() async {
    return await _remoteConfig.activate();
  }
}
```

### 8. Firebase Storage

```dart
// lib/core/services/storage_service.dart
import 'dart:io';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:image_picker/image_picker.dart';

class StorageService {
  final FirebaseStorage _storage;

  StorageService({FirebaseStorage? storage})
      : _storage = storage ?? FirebaseStorage.instance;

  // Upload file
  Future<String> uploadFile({
    required File file,
    required String path,
    String? fileName,
    Function(double)? onProgress,
  }) async {
    try {
      final ref = _storage.ref(path).child(fileName ?? file.path.split('/').last);

      final uploadTask = ref.putFile(
        file,
        SettableMetadata(
          contentType: _getContentType(file.path),
          customMetadata: {
            'uploaded_at': DateTime.now().toIso8601String(),
          },
        ),
      );

      // Listen to upload progress
      uploadTask.snapshotEvents.listen((taskSnapshot) {
        final progress = taskSnapshot.bytesTransferred / taskSnapshot.totalBytes;
        onProgress?.call(progress);
      });

      final snapshot = await uploadTask;
      final downloadUrl = await snapshot.ref.getDownloadURL();

      return downloadUrl;
    } on FirebaseException catch (e) {
      throw Exception('Upload failed: ${e.message}');
    }
  }

  // Upload image from image picker
  Future<String> uploadImage({
    required XFile image,
    required String path,
    Function(double)? onProgress,
  }) async {
    return await uploadFile(
      file: File(image.path),
      path: path,
      fileName: image.name,
      onProgress: onProgress,
    );
  }

  // Download file
  Future<File> downloadFile({
    required String url,
    required String localPath,
  }) async {
    try {
      final ref = _storage.refFromURL(url);
      final file = File(localPath);

      await ref.writeToFile(file);
      return file;
    } on FirebaseException catch (e) {
      throw Exception('Download failed: ${e.message}');
    }
  }

  // Get download URL
  Future<String> getDownloadUrl(String path) async {
    try {
      return await _storage.ref(path).getDownloadURL();
    } on FirebaseException catch (e) {
      throw Exception('Failed to get download URL: ${e.message}');
    }
  }

  // Delete file
  Future<void> deleteFile(String path) async {
    try {
      await _storage.ref(path).delete();
    } on FirebaseException catch (e) {
      throw Exception('Delete failed: ${e.message}');
    }
  }

  // List files in a path
  Future<List<Reference>> listFiles(String path) async {
    try {
      final listResult = await _storage.ref(path).listAll();
      return listResult.items;
    } on FirebaseException catch (e) {
      throw Exception('List failed: ${e.message}');
    }
  }

  // Get file metadata
  Future<FullMetadata> getMetadata(String path) async {
    try {
      return await _storage.ref(path).getMetadata();
    } on FirebaseException catch (e) {
      throw Exception('Failed to get metadata: ${e.message}');
    }
  }

  String _getContentType(String filePath) {
    final extension = filePath.split('.').last.toLowerCase();
    switch (extension) {
      case 'jpg':
      case 'jpeg':
        return 'image/jpeg';
      case 'png':
        return 'image/png';
      case 'gif':
        return 'image/gif';
      case 'pdf':
        return 'application/pdf';
      case 'mp4':
        return 'video/mp4';
      default:
        return 'application/octet-stream';
    }
  }
}
```

### 9. Provider State Management con Firebase

```dart
// lib/features/authentication/presentation/providers/auth_provider.dart
import 'package:flutter/foundation.dart';
import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import '../../domain/entities/user.dart';
import '../../data/repositories/auth_repository_impl.dart';

class AuthProvider with ChangeNotifier {
  final AuthRepositoryImpl _authRepository;

  User? _user;
  bool _isLoading = false;
  String? _error;

  AuthProvider({required AuthRepositoryImpl authRepository})
      : _authRepository = authRepository {
    _init();
  }

  User? get user => _user;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isAuthenticated => _user != null;

  void _init() {
    // Listen to auth state changes
    _authRepository.authStateChanges.listen((user) {
      _user = user;
      _error = null;
      notifyListeners();
    });
  }

  Future<void> signInWithEmailAndPassword(String email, String password) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      _user = await _authRepository.signInWithEmailAndPassword(email, password);
    } catch (e) {
      _error = e.toString();
      _user = null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> signUpWithEmailAndPassword(String email, String password) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      _user = await _authRepository.signUpWithEmailAndPassword(email, password);
    } catch (e) {
      _error = e.toString();
      _user = null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> signInWithGoogle() async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      _user = await _authRepository.signInWithGoogle();
    } catch (e) {
      _error = e.toString();
      _user = null;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> signOut() async {
    try {
      _isLoading = true;
      notifyListeners();

      await _authRepository.signOut();
      _user = null;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> sendPasswordResetEmail(String email) async {
    try {
      _isLoading = true;
      _error = null;
      notifyListeners();

      await _authRepository.sendPasswordResetEmail(email);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}

// lib/main.dart - Provider setup
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'features/authentication/presentation/providers/auth_provider.dart';
import 'features/authentication/data/repositories/auth_repository_impl.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => AuthProvider(
            authRepository: AuthRepositoryImpl(),
          ),
        ),
        // Add more providers here
      ],
      child: MaterialApp(
        title: 'Firebase App',
        home: const HomeScreen(),
      ),
    );
  }
}

// Usage in widget
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final authProvider = Provider.of<AuthProvider>(context);

    if (authProvider.isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (authProvider.isAuthenticated) {
      return Scaffold(
        appBar: AppBar(title: const Text('Home')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Welcome, ${authProvider.user?.email}'),
              ElevatedButton(
                onPressed: () => authProvider.signOut(),
                child: const Text('Sign Out'),
              ),
            ],
          ),
        ),
      );
    }

    return const LoginScreen();
  }
}
```

## 🎯 Mejores Prácticas

### 1. Security Rules (Firestore)

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Products collection
    match /products/{productId} {
      allow read: if true;
      allow write: if request.auth != null;
    }

    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### 2. Offline Persistence

```dart
// Enable offline persistence
await FirebaseFirestore.instance.enablePersistence(
  const PersistenceSettings(synchronizeTabs: true),
);
```

### 3. Error Handling

```dart
try {
  await _firestore.collection('products').add(data);
} on FirebaseException catch (e) {
  if (e.code == 'permission-denied') {
    // Handle permission error
  } else if (e.code == 'unavailable') {
    // Handle offline error
  }
}
```

### 4. Firebase Storage Security Rules

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    // User uploads - only authenticated users can upload
    match /users/{userId}/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.uid == userId;
    }

    // Public images
    match /public/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }

    // Private files
    match /private/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

### 5. Remote Config Best Practices

```dart
// Configurar valores por defecto locales
await _remoteConfig.setDefaults({
  'feature_enabled': false,
  'max_items': 20,
  'api_endpoint': 'https://api.example.com',
});

// Fetch en intervalos apropiados
// - Development: 0 segundos (fetch inmediato)
// - Production: 1 hora (fetch cada hora)
await _remoteConfig.setConfigSettings(
  RemoteConfigSettings(
    fetchTimeout: const Duration(seconds: 10),
    minimumFetchInterval: kDebugMode
      ? const Duration(seconds: 0)
      : const Duration(hours: 1),
  ),
);

// Siempre activar después de fetch
final fetched = await _remoteConfig.fetchAndActivate();
if (fetched) {
  print('Remote config updated');
}
```

### 6. Analytics Best Practices

```dart
// 1. Configurar user ID después del login
await analytics.setUserId(userId);

// 2. Configurar user properties (máximo 25)
await analytics.setUserProperties({
  'user_type': 'premium',
  'subscription_status': 'active',
  'sign_up_method': 'google',
});

// 3. Usar nombres consistentes para screens
await analytics.logScreenView(screenName: 'product_detail');

// 4. Usar eventos predefinidos cuando sea posible
await analytics.logLogin(method: 'google');
await analytics.logSignUp(method: 'email');

// 5. Limpiar user ID en logout
await analytics.clearUserId();
```

### 7. Provider State Management Best Practices

```dart
// 1. Usar ChangeNotifierProvider para estado local
ChangeNotifierProvider(
  create: (_) => AuthProvider(authRepository: AuthRepositoryImpl()),
)

// 2. Usar Consumer para rebuilds selectivos
Consumer<AuthProvider>(
  builder: (context, authProvider, child) {
    if (authProvider.isLoading) {
      return const CircularProgressIndicator();
    }
    return Text('Welcome, ${authProvider.user?.email}');
  },
)

// 3. Usar Selector para optimizar rebuilds
Selector<AuthProvider, bool>(
  selector: (_, provider) => provider.isAuthenticated,
  builder: (context, isAuthenticated, child) {
    return isAuthenticated ? const HomeScreen() : const LoginScreen();
  },
)

// 4. Separar providers por feature
MultiProvider(
  providers: [
    ChangeNotifierProvider(create: (_) => AuthProvider(...)),
    ChangeNotifierProvider(create: (_) => ProductProvider(...)),
    ChangeNotifierProvider(create: (_) => CartProvider(...)),
  ],
  child: MyApp(),
)
```

## 📚 Recursos Adicionales

- [FlutterFire Documentation](https://firebase.flutter.dev/)
- [Firebase Console](https://console.firebase.google.com/)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)

## 🔗 Skills Relacionados

- [Clean Architecture](../clean-architecture/SKILL.md)
- [Offline-First](../offline-first/SKILL.md)

---

**Versión:** 2.0.0
**Última actualización:** Diciembre 2025

## 📝 Changelog

### v2.0.0 (Diciembre 2025)
- ✅ Agregada sección completa de Firebase Storage con upload, download y gestión de archivos
- ✅ Agregada implementación detallada de Remote Config con valores por defecto y fetch
- ✅ Agregada integración con Provider para state management
- ✅ Mejorada sección de Analytics con ejemplos de screen tracking, custom events, user ID y user properties
- ✅ Agregadas mejores prácticas para Storage, Remote Config, Analytics y Provider
- ✅ Actualizada estructura del proyecto para incluir nuevos servicios
