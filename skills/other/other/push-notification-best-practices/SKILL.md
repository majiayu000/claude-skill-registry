---
name: push-notification-best-practices
description: >
  Comprehensive mobile push notification guide for iOS (APNS) and Android (FCM).
  Use when setting up push notifications, debugging delivery issues, implementing
  background/foreground handlers, managing push tokens, integrating deep linking,
  or troubleshooting platform-specific issues.
---

# Push Notification Best Practices

## Overview

Comprehensive guide for implementing and troubleshooting push notifications in mobile applications. Covers iOS (APNS), Android (FCM), React Native, Expo, and Flutter platforms with platform-specific configurations, token management, message handling, and deep linking patterns.

## Platform Support Matrix

| Platform | Offline Push | Notification Bar | Click Navigation | In-App Toast | Background Handler |
|----------|--------------|------------------|------------------|--------------|-------------------|
| iOS | APNS | System | Deep Link | Custom | data-only payload |
| Android | FCM | System | Intent | Custom | data-only payload |
| React Native | APNS/FCM | System | React Navigation | Custom | setBackgroundMessageHandler |
| Expo | Expo Push | System | Linking | Custom | TaskManager |
| Flutter | APNS/FCM | System | Navigator | Custom | onBackgroundMessage |

## Decision Trees

### Permission Request Timing

**When to request notification permission?**

```
User installing app
        |
        v
  [First launch?] ──Yes──> [Show value proposition first]
        |                          |
        No                         v
        |                  [User action triggers need?]
        v                          |
  [Already granted?]              Yes
        |                          |
       Yes                         v
        |                  [Request permission] ──> 70-80% acceptance rate
        v
  [Notifications ready]
```

| Timing | Acceptance Rate | Use Case |
|--------|-----------------|----------|
| Immediate (app launch) | 15-20% | Low engagement apps |
| After onboarding | 40-50% | Standard apps |
| User-initiated action | 70-80% | High engagement apps |

**Recommendation:** Request after explaining value or when user enables a related feature.

### Silent vs Visible Notification

**Which payload type should I use?**

```
[What's the purpose?]
        |
        +──> Time-sensitive user alert ──> Visible (notification payload)
        |
        +──> Background data sync ──> Silent (data-only payload)
        |
        +──> Custom UI required ──> Silent (data-only payload)
        |
        +──> Need background processing ──> Silent (data-only payload)
```

| Scenario | Payload Type | Reason |
|----------|--------------|--------|
| New message alert | Visible | User needs immediate attention |
| Order status update | Visible | Time-sensitive information |
| Background sync | Silent | No user interruption needed |
| Custom notification UI | Silent | Full control over display |
| Update badge count | Silent | Background processing needed |

### Extension Strategy (iOS)

**When to use Notification Service Extension?**

- Need to modify notification content before display
- Need to download and attach media (images, videos)
- Need to decrypt end-to-end encrypted payloads
- Need to add action buttons dynamically

**When to use Notification Content Extension?**

- Need custom notification UI beyond system template
- Need interactive elements in expanded view

## Anti-patterns (NEVER Do)

### Permission Handling

| NEVER | Why | Instead |
|-------|-----|---------|
| Request permission on first launch without context | 15-20% acceptance rate | Explain value first, then request |
| Re-ask after user denies | System ignores repeated requests | Show settings redirect |
| Ignore provisional authorization | Misses iOS 12+ quiet delivery | Use `.provisional` option |

### Token Management

| NEVER | Why | Instead |
|-------|-----|---------|
| Cache tokens long-term | Tokens can change on reinstall/restore | Always use fresh token from callback |
| Assume token format | Format varies by platform/SDK | Treat as opaque string |
| Send token without user association | Can't target notifications | Associate with userId on backend |
| Store tokens without device ID | Duplicate tokens per user | Use deviceId as unique key |

### Message Handling

| NEVER | Why | Instead |
|-------|-----|---------|
| Use `notification` payload for background processing | onMessageReceived not called in background | Use data-only payload |
| Rely on silent notifications for time-critical delivery | Delivery not guaranteed | Use visible notifications |
| Execute heavy operations in background handler | System kills app after ~30 seconds | Queue work, process quickly |
| Forget to handle both payload types | Missing notifications | Handle notification + data payloads |

### iOS Specific

| NEVER | Why | Instead |
|-------|-----|---------|
| Register for notifications before delegate setup | Delegate methods not called | Set delegate before `registerForRemoteNotifications()` |
| Skip `serviceExtensionTimeWillExpire()` implementation | Content modification fails | Always implement fallback |
| Use .p12 certificates | Expires yearly, deprecated | Use .p8 authentication key |

### Android Specific

| NEVER | Why | Instead |
|-------|-----|---------|
| Skip NotificationChannel creation | Notifications don't appear on Android 8.0+ | Create channel at app start |
| Use priority `normal` for background handlers | Doze mode blocks delivery | Use priority `high` |
| Use colored notification icons | Android ignores colors, shows white square | Use white-on-transparent icons |

## Skill Format

Each rule file follows a hybrid format for fast lookup and deep understanding:

- **Quick Pattern**: Incorrect/Correct code snippets for immediate pattern matching
- **When to Apply**: Situations where this rule is relevant
- **Deep Dive**: Full context with step-by-step guides and platform-specific details
- **Common Pitfalls**: Common mistakes and how to avoid them
- **Related Rules**: Cross-references to related patterns

**Impact ratings**: CRITICAL (fix immediately), HIGH (significant improvement), MEDIUM (worthwhile optimization)

## When to Apply

Reference these guidelines when:
- Setting up push notifications in a mobile app
- Debugging push notification delivery issues
- Implementing background notification handlers
- Integrating deep linking with push notifications
- Managing push tokens and device registration
- Troubleshooting platform-specific push issues
- Reviewing push notification code for reliability

## Priority-Ordered Guidelines

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | iOS Setup | CRITICAL | `ios-` |
| 2 | Android Setup | CRITICAL | `android-` |
| 3 | Token Management | HIGH | `token-` |
| 4 | Message Handling | HIGH | `message-` |
| 5 | Deep Linking | MEDIUM | `deeplink-` |
| 6 | Infrastructure | MEDIUM | `infra-` |

## Quick Reference

### Critical: iOS Setup

**Setup checklist:**
- Generate APNs authentication key (.p8) from Apple Developer
- Upload to Firebase Console with Key ID and Team ID
- Enable Push Notifications capability in Xcode
- Set UNUserNotificationCenter delegate in didFinishLaunchingWithOptions
- Request notification authorization before registering
- Implement foreground presentation options

### Critical: Android Setup

**Setup checklist:**
- Add google-services.json to app/ directory
- Apply google-services Gradle plugin
- Create NotificationChannel (Android 8.0+)
- Request POST_NOTIFICATIONS permission (Android 13+)
- Implement FirebaseMessagingService
- Set notification icon (transparent background + white)
- Use priority 'high' for Doze mode compatibility

### High: Token Management

**Token lifecycle:**
```javascript
// 1. Register token with server
const token = await getToken();
await registerToken(token, userId);

// 2. Handle token refresh
onTokenRefresh((newToken) => {
  updateTokenOnServer(newToken, userId);
});

// 3. Handle invalidation
if (error.code === 'DeviceNotRegistered') {
  deleteTokenFromDatabase(token);
}
```

### High: Message Handling

**Payload types:**
- **data-only**: Background handler runs on both platforms
- **notification + data**: iOS/Android behavior differs
  - iOS: Always shows notification
  - Android: Background = system tray, Foreground = onMessageReceived

**Priority settings:**
- Use `priority: 'high'` for time-sensitive notifications
- Required for Android Doze mode background handlers

## Rules

Full documentation with code examples in `rules/`:

### iOS Setup (`ios-*`)

| File | Impact | Description |
|------|--------|-------------|
| `ios-apns-auth-key.md` | CRITICAL | APNs authentication key setup |
| `ios-delegate-setup.md` | CRITICAL | UNUserNotificationCenter delegate configuration |
| `ios-permission-request.md` | CRITICAL | Notification permission request flow |
| `ios-token-registration.md` | HIGH | APNS token registration and handling |
| `ios-foreground-display.md` | HIGH | Display notifications in foreground |
| `ios-method-swizzling.md` | MEDIUM | Method Swizzling management |
| `ios-extension-build.md` | MEDIUM | Notification Service Extension setup |

### Android Setup (`android-*`)

| File | Impact | Description |
|------|--------|-------------|
| `android-notification-channel.md` | CRITICAL | Notification channel creation (Android 8.0+) |
| `android-permission.md` | CRITICAL | POST_NOTIFICATIONS runtime permission (Android 13+) |
| `android-google-services.md` | CRITICAL | Firebase project configuration |
| `android-messaging-service.md` | HIGH | FirebaseMessagingService implementation |
| `android-notification-icon.md` | MEDIUM | Notification icon asset requirements |
| `android-priority-high.md` | HIGH | Priority 'high' for Doze mode |

### Token Management (`token-*`)

| File | Impact | Description |
|------|--------|-------------|
| `token-registration.md` | HIGH | Token registration with backend |
| `token-refresh.md` | HIGH | Token refresh handling |
| `token-invalidation.md` | MEDIUM | DeviceNotRegistered error handling |

### Message Handling (`message-*`)

| File | Impact | Description |
|------|--------|-------------|
| `message-data-vs-notification.md` | CRITICAL | data vs notification payload differences |
| `message-background-handler.md` | HIGH | Background message processing |
| `message-foreground-handler.md` | HIGH | Foreground notification display |

### Deep Linking (`deeplink-*`)

| File | Impact | Description |
|------|--------|-------------|
| `deeplink-navigation-conflict.md` | MEDIUM | React Navigation conflict resolution |
| `deeplink-terminated-state.md` | MEDIUM | Deep link handling when app is terminated |

### Infrastructure (`infra-*`)

| File | Impact | Description |
|------|--------|-------------|
| `infra-firewall-ports.md` | MEDIUM | Network firewall configuration |
| `infra-backup-fid.md` | MEDIUM | Firebase Installation ID backup exclusion |
| `infra-rate-limiting.md` | MEDIUM | Push notification rate limiting |

### Best Practices

| File | Impact | Description |
|------|--------|-------------|
| `permission-timing.md` | HIGH | Permission request timing optimization (70-80% acceptance) |
| `testing-debugging.md` | HIGH | Testing tools, debugging techniques, payload validation |

## Searching Rules

```bash
# Find rules by keyword
grep -l "apns" rules/
grep -l "fcm" rules/
grep -l "token" rules/
grep -l "background" rules/
grep -l "permission" rules/
grep -l "deeplink" rules/
```

## Problem → Rule Mapping

| Problem | Start With |
|---------|------------|
| iOS not receiving push | `ios-apns-auth-key` → `ios-delegate-setup` |
| Android not receiving push | `android-google-services` → `android-notification-channel` |
| Push not working in background | `android-priority-high` → `message-background-handler` |
| Push not visible in foreground | `ios-foreground-display` or `message-foreground-handler` |
| Token missing/expired | `token-registration` → `token-refresh` |
| Deep link conflict error | `deeplink-navigation-conflict` |
| Notification icon broken (Android) | `android-notification-icon` |
| Failed on corporate network | `infra-firewall-ports` |
| Background handler not called (Android) | `android-priority-high` → `message-data-vs-notification` |
| userNotificationCenter not called (iOS) | `ios-delegate-setup` |
| 404 error after backup restore | `infra-backup-fid` |
| Send failed (429 error) | `infra-rate-limiting` |
| Low permission acceptance rate | `permission-timing` → `ios-permission-request` |
| How to debug/test push | `testing-debugging` |
| Cannot test locally | `testing-debugging` → `ios-apns-auth-key` |

## Platform-Specific Notes

### iOS (APNS)
- Requires Apple Developer account and APNs authentication key (.p8)
- Different behavior for Development vs Production builds
- Delegate must be set before other SDK initialization
- Method Swizzling can interfere with delegate calls

### Android (FCM)
- Requires google-services.json from Firebase Console
- NotificationChannel required for Android 8.0+
- Runtime permission required for Android 13+
- Doze mode requires `priority: 'high'` for background handlers
- Notification icons must be monochrome (white on transparent)

### React Native
- Common issue: `gcm.message_id` required for foreground notifications
- Deep linking conflicts with React Navigation
- Terminated state requires native → JS bridge pattern

### Expo
- ExpoPushToken format: `ExponentPushToken[...]`
- Rate limit: 600 push notifications per second per project
- Development builds required for SDK 53+
- Use `eas credentials` for APNs key management

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

## Attribution

Based on push notification troubleshooting guides and Firebase Cloud Messaging official documentation.
