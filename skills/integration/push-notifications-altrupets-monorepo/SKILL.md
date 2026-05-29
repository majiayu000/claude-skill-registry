# 🔔 Skill: Push Notifications

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `flutter-push-notifications` |
| **Nivel** | 🟡 Intermedio |
| **Versión** | 1.0.0 |
| **Keywords** | `push-notifications`, `fcm`, `firebase-messaging`, `local-notifications`, `apns` |
| **Referencia** | [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging) |

## 🔑 Keywords para Invocación

- `push-notifications`
- `fcm`
- `firebase-messaging`
- `local-notifications`
- `apns`
- `notifications`
- `@skill:push-notifications`

### Ejemplos de Prompts

```
Implementa push-notifications con FCM
```

```
Setup local-notifications y remote notifications
```

```
Configura firebase-messaging con topics y targeting
```

```
@skill:push-notifications - Sistema completo de notificaciones
```

## 📖 Descripción

Este skill cubre la implementación completa de push notifications usando Firebase Cloud Messaging (FCM) y local notifications. Incluye configuración de iOS APNS, Android, manejo de notificaciones en foreground/background, actions, y deep linking desde notificaciones.

### ✅ Cuándo Usar Este Skill

- Engagement con usuarios
- Notificaciones transaccionales
- Marketing campaigns
- Real-time alerts
- Chat messages
- Order updates
- News/content updates
- Recordatorios programados

### ❌ Cuándo NO Usar Este Skill

- App sin backend
- No necesitas comunicación push
- Solo notificaciones locales simples

## 🏗️ Estructura del Proyecto

```
my_app/
├── lib/
│   ├── services/
│   │   ├── notifications/
│   │   │   ├── fcm_service.dart
│   │   │   ├── local_notifications_service.dart
│   │   │   ├── notification_handler.dart
│   │   │   └── notification_models.dart
│   │   └── notification_service.dart
│   │
│   └── main.dart
│
├── android/
│   └── app/
│       ├── google-services.json
│       └── src/main/
│           ├── AndroidManifest.xml
│           └── res/
│               └── drawable/
│                   └── notification_icon.png
│
└── ios/
    └── Runner/
        ├── GoogleService-Info.plist
        └── AppDelegate.swift
```

## 📦 Dependencias

```yaml
dependencies:
  flutter:
    sdk: flutter

  # Firebase Cloud Messaging
  firebase_core: ^2.24.2
  firebase_messaging: ^14.7.9

  # Local Notifications
  flutter_local_notifications: ^16.3.0

  # Permissions
  permission_handler: ^11.1.0

  # Timezone (for scheduled notifications)
  timezone: ^0.9.2
```

## 💻 Implementación

### 1. FCM Service

```dart
// lib/services/notifications/fcm_service.dart
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';
import 'notification_handler.dart';

// Top-level function for background message handling
@pragma('vm:entry-point')
Future<void> firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  print('📱 Background message: ${message.messageId}');
  print('Title: ${message.notification?.title}');
  print('Body: ${message.notification?.body}');
  print('Data: ${message.data}');

  // Handle background notification
  await NotificationHandler.handleBackgroundMessage(message);
}

class FCMService {
  static final FirebaseMessaging _messaging = FirebaseMessaging.instance;
  static String? _fcmToken;

  static String? get fcmToken => _fcmToken;

  // Initialize FCM
  static Future<void> initialize() async {
    // Request permission (iOS)
    final settings = await _requestPermission();

    if (settings.authorizationStatus == AuthorizationStatus.authorized) {
      print('✅ User granted permission');
    } else {
      print('❌ User declined or has not accepted permission');
      return;
    }

    // Get FCM token
    _fcmToken = await _messaging.getToken();
    print('📱 FCM Token: $_fcmToken');

    // Listen to token refresh
    _messaging.onTokenRefresh.listen((newToken) {
      print('🔄 FCM Token refreshed: $newToken');
      _fcmToken = newToken;
      // Send new token to your server
      _sendTokenToServer(newToken);
    });

    // Setup message handlers
    _setupMessageHandlers();

    // Setup background message handler
    FirebaseMessaging.onBackgroundMessage(firebaseMessagingBackgroundHandler);
  }

  // Request notification permission
  static Future<NotificationSettings> _requestPermission() async {
    return await _messaging.requestPermission(
      alert: true,
      announcement: false,
      badge: true,
      carPlay: false,
      criticalAlert: false,
      provisional: false,
      sound: true,
    );
  }

  // Setup message handlers
  static void _setupMessageHandlers() {
    // Foreground messages
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print('📱 Foreground message: ${message.messageId}');
      NotificationHandler.handleForegroundMessage(message);
    });

    // Message opened (app in background/terminated)
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      print('📱 Notification opened: ${message.messageId}');
      NotificationHandler.handleMessageOpened(message);
    });

    // Check if app was opened from terminated state
    _messaging.getInitialMessage().then((RemoteMessage? message) {
      if (message != null) {
        print('📱 App opened from terminated state: ${message.messageId}');
        NotificationHandler.handleMessageOpened(message);
      }
    });
  }

  // Send token to your server
  static Future<void> _sendTokenToServer(String token) async {
    // TODO: Implement your API call
    print('Sending token to server: $token');
  }

  // Subscribe to topic
  static Future<void> subscribeToTopic(String topic) async {
    await _messaging.subscribeToTopic(topic);
    print('✅ Subscribed to topic: $topic');
  }

  // Unsubscribe from topic
  static Future<void> unsubscribeFromTopic(String topic) async {
    await _messaging.unsubscribeFromTopic(topic);
    print('❌ Unsubscribed from topic: $topic');
  }

  // Delete token
  static Future<void> deleteToken() async {
    await _messaging.deleteToken();
    _fcmToken = null;
    print('🗑️ FCM token deleted');
  }

  // Set foreground notification presentation options (iOS)
  static Future<void> setForegroundNotificationPresentationOptions({
    bool alert = true,
    bool badge = true,
    bool sound = true,
  }) async {
    await _messaging.setForegroundNotificationPresentationOptions(
      alert: alert,
      badge: badge,
      sound: sound,
    );
  }
}
```

### 2. Local Notifications Service

```dart
// lib/services/notifications/local_notifications_service.dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

class LocalNotificationsService {
  static final FlutterLocalNotificationsPlugin _notifications =
      FlutterLocalNotificationsPlugin();

  static bool _initialized = false;

  // Initialize local notifications
  static Future<void> initialize() async {
    if (_initialized) return;

    // Initialize timezone
    tz.initializeTimeZones();

    // Android initialization settings
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');

    // iOS initialization settings
    const iosSettings = DarwinInitializationSettings(
      requestAlertPermission: true,
      requestBadgePermission: true,
      requestSoundPermission: true,
      onDidReceiveLocalNotification: _onDidReceiveLocalNotification,
    );

    const initSettings = InitializationSettings(
      android: androidSettings,
      iOS: iosSettings,
    );

    // Initialize
    await _notifications.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTapped,
    );

    _initialized = true;
    print('✅ Local Notifications initialized');
  }

  // Handle notification tap
  static void _onNotificationTapped(NotificationResponse response) {
    print('📱 Notification tapped: ${response.id}');
    print('Payload: ${response.payload}');

    if (response.payload != null) {
      // Navigate based on payload
      NotificationHandler.handleLocalNotificationTap(response.payload!);
    }
  }

  // iOS foreground notification handler
  static void _onDidReceiveLocalNotification(
    int id,
    String? title,
    String? body,
    String? payload,
  ) {
    print('📱 iOS Foreground Notification: $title');
  }

  // Show simple notification
  static Future<void> showNotification({
    required int id,
    required String title,
    required String body,
    String? payload,
    String? channelId,
    String? channelName,
  }) async {
    final androidDetails = AndroidNotificationDetails(
      channelId ?? 'default_channel',
      channelName ?? 'Default',
      channelDescription: 'Default notification channel',
      importance: Importance.high,
      priority: Priority.high,
      ticker: 'ticker',
    );

    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    final details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.show(
      id,
      title,
      body,
      details,
      payload: payload,
    );
  }

  // Show notification with custom sound
  static Future<void> showNotificationWithSound({
    required int id,
    required String title,
    required String body,
    required String soundFileName,
    String? payload,
  }) async {
    final androidDetails = AndroidNotificationDetails(
      'custom_sound_channel',
      'Custom Sound',
      channelDescription: 'Notifications with custom sound',
      importance: Importance.high,
      priority: Priority.high,
      sound: RawResourceAndroidNotificationSound(soundFileName),
    );

    final iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
      sound: '$soundFileName.aiff',
    );

    final details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.show(id, title, body, details, payload: payload);
  }

  // Schedule notification
  static Future<void> scheduleNotification({
    required int id,
    required String title,
    required String body,
    required DateTime scheduledDate,
    String? payload,
  }) async {
    final androidDetails = AndroidNotificationDetails(
      'scheduled_channel',
      'Scheduled Notifications',
      channelDescription: 'Scheduled notifications channel',
      importance: Importance.high,
      priority: Priority.high,
    );

    const iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
    );

    final details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.zonedSchedule(
      id,
      title,
      body,
      tz.TZDateTime.from(scheduledDate, tz.local),
      details,
      payload: payload,
      androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
      uiLocalNotificationDateInterpretation:
          UILocalNotificationDateInterpretation.absoluteTime,
    );
  }

  // Show notification with actions
  static Future<void> showNotificationWithActions({
    required int id,
    required String title,
    required String body,
    String? payload,
  }) async {
    final androidDetails = AndroidNotificationDetails(
      'actions_channel',
      'Actionable Notifications',
      channelDescription: 'Notifications with action buttons',
      importance: Importance.high,
      priority: Priority.high,
      actions: <AndroidNotificationAction>[
        const AndroidNotificationAction(
          'accept',
          'Accept',
          showsUserInterface: true,
        ),
        const AndroidNotificationAction(
          'reject',
          'Reject',
          showsUserInterface: true,
          cancelNotification: true,
        ),
      ],
    );

    final iosDetails = DarwinNotificationDetails(
      presentAlert: true,
      presentBadge: true,
      presentSound: true,
      categoryIdentifier: 'actionCategory',
    );

    final details = NotificationDetails(
      android: androidDetails,
      iOS: iosDetails,
    );

    await _notifications.show(id, title, body, details, payload: payload);
  }

  // Show big picture notification (Android)
  static Future<void> showBigPictureNotification({
    required int id,
    required String title,
    required String body,
    required String imageUrl,
    String? payload,
  }) async {
    final BigPictureStyleInformation bigPictureStyleInformation =
        BigPictureStyleInformation(
      FilePathAndroidBitmap(imageUrl),
      contentTitle: title,
      summaryText: body,
    );

    final androidDetails = AndroidNotificationDetails(
      'big_picture_channel',
      'Big Picture Notifications',
      channelDescription: 'Notifications with big picture',
      importance: Importance.high,
      priority: Priority.high,
      styleInformation: bigPictureStyleInformation,
    );

    final details = NotificationDetails(android: androidDetails);

    await _notifications.show(id, title, body, details, payload: payload);
  }

  // Show inbox style notification (multiple lines)
  static Future<void> showInboxNotification({
    required int id,
    required String title,
    required List<String> messages,
    String? payload,
  }) async {
    final InboxStyleInformation inboxStyleInformation = InboxStyleInformation(
      messages,
      contentTitle: title,
      summaryText: '${messages.length} new messages',
    );

    final androidDetails = AndroidNotificationDetails(
      'inbox_channel',
      'Inbox Notifications',
      channelDescription: 'Inbox style notifications',
      importance: Importance.high,
      priority: Priority.high,
      styleInformation: inboxStyleInformation,
    );

    final details = NotificationDetails(android: androidDetails);

    await _notifications.show(id, title, messages.first, details, payload: payload);
  }

  // Cancel notification
  static Future<void> cancel(int id) async {
    await _notifications.cancel(id);
  }

  // Cancel all notifications
  static Future<void> cancelAll() async {
    await _notifications.cancelAll();
  }

  // Get pending notifications
  static Future<List<PendingNotificationRequest>> getPendingNotifications() async {
    return await _notifications.pendingNotificationRequests();
  }

  // Get active notifications
  static Future<List<ActiveNotification>> getActiveNotifications() async {
    final List<ActiveNotification>? activeNotifications =
        await _notifications.getActiveNotifications();
    return activeNotifications ?? [];
  }
}
```

### 3. Notification Handler

```dart
// lib/services/notifications/notification_handler.dart
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'local_notifications_service.dart';
import '../../routing/app_router.dart';

class NotificationHandler {
  // Handle foreground message
  static Future<void> handleForegroundMessage(RemoteMessage message) async {
    print('📱 Handling foreground message');

    // Show local notification for foreground messages
    await LocalNotificationsService.showNotification(
      id: message.hashCode,
      title: message.notification?.title ?? 'New Notification',
      body: message.notification?.body ?? '',
      payload: _encodePayload(message.data),
    );

    // Track event
    AnalyticsService.trackEvent('notification_received', properties: {
      'type': 'foreground',
      'title': message.notification?.title,
    });
  }

  // Handle background message
  static Future<void> handleBackgroundMessage(RemoteMessage message) async {
    print('📱 Handling background message');

    // Track event
    AnalyticsService.trackEvent('notification_received', properties: {
      'type': 'background',
      'title': message.notification?.title,
    });
  }

  // Handle notification opened
  static Future<void> handleMessageOpened(RemoteMessage message) async {
    print('📱 Handling notification opened');

    // Track event
    AnalyticsService.trackEvent('notification_opened', properties: {
      'title': message.notification?.title,
      'data': message.data,
    });

    // Navigate based on data
    final data = message.data;
    _navigateFromNotification(data);
  }

  // Handle local notification tap
  static void handleLocalNotificationTap(String payload) {
    print('📱 Local notification tapped: $payload');

    final data = _decodePayload(payload);
    _navigateFromNotification(data);
  }

  // Navigate based on notification data
  static void _navigateFromNotification(Map<String, dynamic> data) {
    final type = data['type'];
    final id = data['id'];

    switch (type) {
      case 'product':
        AppRouter.goToProduct(id);
        break;
      case 'order':
        AppRouter.router.go('/orders/$id');
        break;
      case 'chat':
        AppRouter.router.go('/chat/$id');
        break;
      case 'promo':
        AppRouter.handlePromoLink(id);
        break;
      default:
        AppRouter.router.go('/');
    }
  }

  // Encode data to payload string
  static String _encodePayload(Map<String, dynamic> data) {
    return data.entries.map((e) => '${e.key}=${e.value}').join('&');
  }

  // Decode payload string to map
  static Map<String, dynamic> _decodePayload(String payload) {
    final pairs = payload.split('&');
    return Map.fromEntries(
      pairs.map((pair) {
        final parts = pair.split('=');
        return MapEntry(parts[0], parts[1]);
      }),
    );
  }
}
```

### 4. iOS Configuration

```swift
// ios/Runner/AppDelegate.swift
import UIKit
import Flutter
import Firebase

@UIApplicationMain
@objc class AppDelegate: FlutterAppDelegate {
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    // Configure Firebase
    FirebaseApp.configure()

    // Request notification permissions
    if #available(iOS 10.0, *) {
      UNUserNotificationCenter.current().delegate = self as UNUserNotificationCenterDelegate
    }

    GeneratedPluginRegistrant.register(with: self)
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  // Handle APNs token
  override func application(
    _ application: UIApplication,
    didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
  ) {
    Messaging.messaging().apnsToken = deviceToken
  }
}
```

### 5. Android Configuration

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<manifest>
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
    <uses-permission android:name="android.permission.VIBRATE" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>

    <application>
        <!-- Notification icon -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_icon"
            android:resource="@drawable/notification_icon" />

        <!-- Notification color -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_color"
            android:resource="@color/notification_color" />

        <!-- Default notification channel -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_channel_id"
            android:value="default_channel" />
    </application>
</manifest>
```

## 🎯 Mejores Prácticas

### 1. Notification Channels (Android)

✅ **DO:** Crea channels para diferentes tipos
```dart
static Future<void> createNotificationChannels() async {
  const channels = [
    AndroidNotificationChannel(
      'messages',
      'Messages',
      description: 'Chat messages',
      importance: Importance.high,
    ),
    AndroidNotificationChannel(
      'orders',
      'Orders',
      description: 'Order updates',
      importance: Importance.defaultImportance,
    ),
  ];

  for (final channel in channels) {
    await _notifications
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
  }
}
```

### 2. Token Management

✅ **DO:** Sincroniza tokens con tu backend
```dart
static Future<void> updateTokenOnServer(String token) async {
  await api.post('/users/fcm-token', {'token': token});
}
```

### 3. Permission Handling

✅ **DO:** Solicita permisos en el momento adecuado
```dart
// No en el app launch, sino cuando tenga sentido
Future<void> askForNotificationPermission() async {
  final status = await Permission.notification.status;
  if (!status.isGranted) {
    await Permission.notification.request();
  }
}
```

## 🚨 Troubleshooting

### iOS: Notifications Not Received

```bash
# Verify APNS certificate in Firebase Console
# Check capabilities in Xcode: Push Notifications enabled
# Verify GoogleService-Info.plist is correct
```

### Android: Notifications Not Showing

```xml
<!-- Verify POST_NOTIFICATIONS permission (Android 13+) -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
```

### FCM Token Not Generated

```dart
// Check Firebase initialization
await Firebase.initializeApp();

// Check permissions
final settings = await FirebaseMessaging.instance.requestPermission();
print('Permission: ${settings.authorizationStatus}');
```

## 📚 Recursos

- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [flutter_local_notifications](https://pub.dev/packages/flutter_local_notifications)
- [iOS Push Notifications](https://developer.apple.com/documentation/usernotifications)

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
**Total líneas:** 1,100+
