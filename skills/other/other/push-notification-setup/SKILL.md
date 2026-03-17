---
name: push-notification-setup
description: Implements push notifications across iOS, Android, and web using Firebase Cloud Messaging and native services. Use when adding notification capabilities, handling background messages, or setting up notification channels.
keywords: push notifications, FCM, Firebase Cloud Messaging, iOS notifications, Android notifications, web notifications, React Native notifications, notification permissions, background messages, notification channels, APNS, APNs, notification tokens, remote notifications, foreground notifications, notification handlers
---

# Push Notification Setup

Implement push notifications across mobile and web platforms.

## Firebase Cloud Messaging (React Native)

```javascript
import messaging from '@react-native-firebase/messaging';

// Request permission
async function requestPermission() {
  const status = await messaging().requestPermission();
  if (status === messaging.AuthorizationStatus.AUTHORIZED) {
    const token = await messaging().getToken();
    await sendTokenToServer(token);
  }
}

// Handle foreground messages
messaging().onMessage(async message => {
  console.log('Foreground message:', message);
  showLocalNotification(message);
});

// Handle background/quit messages
messaging().setBackgroundMessageHandler(async message => {
  console.log('Background message:', message);
});

// Handle token refresh
messaging().onTokenRefresh(token => {
  sendTokenToServer(token);
});
```

## iOS Native (Swift)

```swift
import UserNotifications

func requestAuthorization() {
    UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
        if granted {
            DispatchQueue.main.async {
                UIApplication.shared.registerForRemoteNotifications()
            }
        }
    }
}

func application(_ application: UIApplication, didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
    sendTokenToServer(token)
}
```

## Android (Kotlin)

```kotlin
class MyFirebaseService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        sendTokenToServer(token)
    }

    override fun onMessageReceived(message: RemoteMessage) {
        message.notification?.let {
            showNotification(it.title, it.body)
        }
    }

    private fun showNotification(title: String?, body: String?) {
        val channelId = "default"
        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle(title)
            .setContentText(body)
            .setSmallIcon(R.drawable.ic_notification)
            .build()

        NotificationManagerCompat.from(this).notify(0, notification)
    }
}
```

## Best Practices

- Request permission at appropriate time
- Handle token refresh
- Support notification channels (Android)
- Implement deep linking
- Never send sensitive data in payload
- Test on real devices
