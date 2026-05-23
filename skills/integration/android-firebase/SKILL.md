---
name: android-firebase
description: Firebase integration patterns for Android - Crashlytics, Analytics, Remote Config, FCM. Use when setting up crash reporting, analytics events, remote configuration, or push notifications.
license: MIT
version: 1.0.0
---

# Android Firebase Skill

Firebase integration patterns: Crashlytics, Analytics, Remote Config, FCM.

## When to Use

- Setting up Firebase SDK
- Implementing crash reporting
- Adding analytics events
- Using Remote Config
- Setting up FCM (Push Notifications)

## Setup

### Dependencies

```toml
[versions]
firebase-bom = "33.8.0"

[libraries]
firebase-bom = { module = "com.google.firebase:firebase-bom", version.ref = "firebase-bom" }
firebase-analytics = { module = "com.google.firebase:firebase-analytics-ktx" }
firebase-crashlytics = { module = "com.google.firebase:firebase-crashlytics-ktx" }
firebase-config = { module = "com.google.firebase:firebase-config-ktx" }
firebase-messaging = { module = "com.google.firebase:firebase-messaging-ktx" }
```

### Initialization

```kotlin
// In Application class
FirebaseApp.initializeApp(this)
```

## Crashlytics

```kotlin
// Log non-fatal exception
Firebase.crashlytics.recordException(exception)

// Custom keys for debugging
Firebase.crashlytics.setCustomKey("user_id", userId)
Firebase.crashlytics.setCustomKey("screen", currentScreen)

// Log message
Firebase.crashlytics.log("User clicked purchase button")

// Set user identifier
Firebase.crashlytics.setUserId(userId)

// Force crash (for testing)
throw RuntimeException("Test Crash")
```

## Analytics

```kotlin
// Log standard event
Firebase.analytics.logEvent(FirebaseAnalytics.Event.SELECT_ITEM) {
    param(FirebaseAnalytics.Param.ITEM_ID, itemId)
    param(FirebaseAnalytics.Param.ITEM_NAME, itemName)
}

// Custom event
Firebase.analytics.logEvent("game_completed") {
    param("score", finalScore.toLong())
    param("level", currentLevel.toLong())
    param("time_spent", timeInSeconds.toLong())
}

// Screen tracking
Firebase.analytics.logEvent(FirebaseAnalytics.Event.SCREEN_VIEW) {
    param(FirebaseAnalytics.Param.SCREEN_NAME, screenName)
    param(FirebaseAnalytics.Param.SCREEN_CLASS, screenClass)
}

// User properties
Firebase.analytics.setUserProperty("premium_user", "true")
Firebase.analytics.setUserId(userId)
```

## Remote Config

```kotlin
val remoteConfig = Firebase.remoteConfig
remoteConfig.setConfigSettingsAsync(remoteConfigSettings {
    minimumFetchIntervalInSeconds = 3600 // 1 hour
})

// Set defaults
remoteConfig.setDefaultsAsync(R.xml.remote_config_defaults)

// Fetch and activate
remoteConfig.fetchAndActivate().addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val featureEnabled = remoteConfig.getBoolean("new_feature_enabled")
        val welcomeMessage = remoteConfig.getString("welcome_message")
        val maxRetries = remoteConfig.getLong("max_retries")
    }
}

// Real-time config (auto-update)
remoteConfig.addOnConfigUpdateListener(object : ConfigUpdateListener {
    override fun onUpdate(configUpdate: ConfigUpdate) {
        remoteConfig.activate()
    }
    override fun onError(error: FirebaseRemoteConfigException) {}
})
```

## FCM (Push Notifications)

```kotlin
class MyFirebaseMessagingService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        // Send token to server
        sendTokenToServer(token)
    }

    override fun onMessageReceived(message: RemoteMessage) {
        // Handle notification
        message.notification?.let { notification ->
            showNotification(notification.title, notification.body)
        }

        // Handle data payload
        message.data.let { data ->
            handleDataPayload(data)
        }
    }
}

// Get current token
Firebase.messaging.token.addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val token = task.result
    }
}

// Subscribe to topic
Firebase.messaging.subscribeToTopic("news")
```

## Version Compatibility

| Firebase BOM | Min SDK | Compile SDK |
|--------------|---------|-------------|
| 33.8.0 | 21 | 35 |
| 33.0.0 | 21 | 34 |
| 32.0.0 | 19 | 33 |

## Error Handling

```kotlin
// Remote Config error handling
remoteConfig.fetchAndActivate()
    .addOnSuccessListener { activated ->
        if (activated) Timber.d("Config activated")
        else Timber.d("Config already up to date")
    }
    .addOnFailureListener { e ->
        when (e) {
            is FirebaseRemoteConfigException ->
                Timber.w("Remote config fetch failed: ${e.code}")
            else -> Timber.e("Unexpected error: ${e.message}")
        }
        // Use cached/default values
    }

// Crashlytics non-fatal reporting
try {
    riskyOperation()
} catch (e: Exception) {
    Firebase.crashlytics.recordException(e)
    // Handle gracefully
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not showing | Wait 24h or use DebugView |
| Crashes not reporting | Check google-services.json |
| FCM not receiving | Verify token registration |
| Config not updating | Check fetch interval |

## Security Checklist

- [ ] Disable Crashlytics in debug builds (optional)
- [ ] No PII in crash logs or analytics
- [ ] Validate FCM token before use
- [ ] Use App Check for backend protection
- [ ] Review analytics data retention settings

## Best Practices

- Enable Crashlytics in release builds only
- Use custom events sparingly (500 limit per app)
- Cache Remote Config values locally
- Handle FCM token refresh
- Set user ID consistently across services
- Use DebugView for testing analytics

## References

- [Firebase Android Setup](https://firebase.google.com/docs/android/setup)
- [Crashlytics](https://firebase.google.com/docs/crashlytics)
- [Analytics](https://firebase.google.com/docs/analytics)
- [Remote Config](https://firebase.google.com/docs/remote-config)
- [Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)

Use Firebase for robust analytics and crash reporting.
