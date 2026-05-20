---
name: push-notifications
description: "Implement, review, or debug push notifications in iOS/macOS apps — local notifications, remote (APNs) notifications, rich notifications, notification actions, silent pushes, and notification service/content extensions. Use when working with UNUserNotificationCenter, registering for remote notifications, handling notification payloads, setting up notification categories and actions, creating rich notification content, or debugging notification delivery. Also use when working with alerts, badges, sounds, background pushes, or user notification permissions in Swift apps."
---

# Push Notifications

Implement, review, and debug local and remote notifications on iOS/macOS using `UserNotifications` and APNs. Covers permission flow, token registration, payload structure, foreground handling, notification actions, grouping, and rich notifications. Targets iOS 26+ with Swift 6.2, backward-compatible to iOS 16 unless noted.

## Contents

- [Permission Flow](#permission-flow)
- [APNs Registration](#apns-registration)
- [Local Notifications](#local-notifications)
- [Remote Notification Payload](#remote-notification-payload)
- [Notification Handling](#notification-handling)
- [Notification Actions and Categories](#notification-actions-and-categories)
- [Notification Grouping](#notification-grouping)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Permission Flow

Request notification authorization before doing anything else. The system prompt appears only once; subsequent calls return the stored decision.

```swift
import UserNotifications

@MainActor
func requestNotificationPermission() async -> Bool {
    let center = UNUserNotificationCenter.current()
    do {
        let granted = try await center.requestAuthorization(
            options: [.alert, .sound, .badge]
        )
        return granted
    } catch {
        print("Authorization request failed: \(error)")
        return false
    }
}
```

### Checking Current Status

Always check status before assuming permissions. The user can change settings at any time.

```swift
@MainActor
func checkNotificationStatus() async -> UNAuthorizationStatus {
    let settings = await UNUserNotificationCenter.current().notificationSettings()
    return settings.authorizationStatus
    // .notDetermined, .denied, .authorized, .provisional, .ephemeral
}
```

### Provisional Notifications

Provisional notifications deliver quietly to the notification center without interrupting the user. The user can then choose to keep or turn them off. Use for onboarding flows where you want to demonstrate value before asking for full permission.

```swift
// Delivers silently -- no permission prompt shown to the user
try await center.requestAuthorization(options: [.alert, .sound, .badge, .provisional])
```

### Critical Alerts

Critical alerts bypass Do Not Disturb and the mute switch. Requires a special entitlement from Apple (request via developer portal). Use only for health, safety, or security scenarios.

```swift
// Requires com.apple.developer.usernotifications.critical-alerts entitlement
try await center.requestAuthorization(
    options: [.alert, .sound, .badge, .criticalAlert]
)
```

### Handling Denied Permissions

When the user has denied notifications, guide them to Settings. Do not repeatedly prompt or nag.

```swift
struct NotificationSettingsButton: View {
    @Environment(\.openURL) private var openURL

    var body: some View {
        Button("Open Settings") {
            if let url = URL(string: UIApplication.openSettingsURLString) {
                openURL(url)
            }
        }
    }
}

```

## APNs Registration

Use `UIApplicationDelegateAdaptor` to receive the device token in a SwiftUI app. The AppDelegate callbacks are the only way to receive APNs tokens.

```swift
@main
struct MyApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        UNUserNotificationCenter.current().delegate = NotificationDelegate.shared
        return true
    }

    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {
        let token = deviceToken.map { String(format: "%02x", $0) }.joined()
        print("APNs token: \(token)")
        // Send token to your server
        Task { await TokenService.shared.upload(token: token) }
    }

    func application(
        _ application: UIApplication,
        didFailToRegisterForRemoteNotificationsWithError error: Error
    ) {
        print("APNs registration failed: \(error.localizedDescription)")
        // Simulator always fails -- this is expected during development
    }
}
```

### Registration Order

Request authorization first, then register for remote notifications. Registration triggers the system to contact APNs and return a device token.

```swift
@MainActor
func registerForPush() async {
    let granted = await requestNotificationPermission()
    guard granted else { return }
    UIApplication.shared.registerForRemoteNotifications()
}
```

### Token Handling

Device tokens change. Re-send the token to your server every time `didRegisterForRemoteNotificationsWithDeviceToken` fires, not just the first time. The system calls this method on every app launch that calls `registerForRemoteNotifications()`.

## Local Notifications

Schedule notifications directly from the device without a server. Useful for reminders, timers, and location-based alerts.

### Creating Content

```swift
let content = UNMutableNotificationContent()
content.title = "Workout Reminder"
content.subtitle = "Time to move"
content.body = "You have a scheduled workout in 15 minutes."
content.sound = .default
content.badge = 1
content.userInfo = ["workoutId": "abc123"]
content.threadIdentifier = "workouts"  // groups in notification center
```

### Trigger Types

```swift
// Fire after a time interval (minimum 60 seconds for repeating)
let timeTrigger = UNTimeIntervalNotificationTrigger(timeInterval: 300, repeats: false)

// Fire at a specific date/time
var dateComponents = DateComponents()
dateComponents.hour = 8
dateComponents.minute = 30
let calendarTrigger = UNCalendarNotificationTrigger(
    dateMatching: dateComponents, repeats: true  // daily at 8:30 AM
)

// Fire when entering a geographic region
let region = CLCircularRegion(
    center: CLLocationCoordinate2D(latitude: 37.33, longitude: -122.01),
    radius: 100,
    identifier: "gym"
)
region.notifyOnEntry = true
region.notifyOnExit = false
let locationTrigger = UNLocationNotificationTrigger(region: region, repeats: false)
// Requires "When In Use" location permission at minimum
```

### Scheduling and Managing

```swift
let request = UNNotificationRequest(
    identifier: "workout-reminder-abc123",
    content: content,
    trigger: timeTrigger
)

let center = UNUserNotificationCenter.current()
try await center.add(request)

// Remove specific pending notifications
center.removePendingNotificationRequests(withIdentifiers: ["workout-reminder-abc123"])

// Remove all pending
center.removeAllPendingNotificationRequests()

// Remove delivered notifications from notification center
center.removeDeliveredNotifications(withIdentifiers: ["workout-reminder-abc123"])
center.removeAllDeliveredNotifications()

// List all pending requests
let pending = await center.pendingNotificationRequests()
```

## Remote Notification Payload

### Standard APNs Payload

```json
{
    "aps": {
        "alert": {
            "title": "New Message",
            "subtitle": "From Alice",
            "body": "Hey, are you free for lunch?"
        },
        "badge": 3,
        "sound": "default",
        "thread-id": "chat-alice",
        "category": "MESSAGE_CATEGORY"
    },
    "messageId": "msg-789",
    "senderId": "user-alice"
}
```

### Silent / Background Push

Set `content-available: 1` with no alert, sound, or badge. The system wakes the app in the background. Requires the "Background Modes > Remote notifications" capability.

```json
{
    "aps": {
        "content-available": 1
    },
    "updateType": "new-data"
}
```

Handle in AppDelegate:
```swift
func application(
    _ application: UIApplication,
    didReceiveRemoteNotification userInfo: [AnyHashable: Any]
) async -> UIBackgroundFetchResult {
    guard let updateType = userInfo["updateType"] as? String else {
        return .noData
    }
    do {
        try await DataSyncService.shared.sync(trigger: updateType)
        return .newData
    } catch {
        return .failed
    }
}
```

### Mutable Content

Set `mutable-content: 1` to allow a Notification Service Extension to modify content before display. Use for downloading images, decrypting content, or adding attachments.

```json
{
    "aps": {
        "alert": { "title": "Photo", "body": "Alice sent a photo" },
        "mutable-content": 1
    },
    "imageUrl": "https://example.com/photo.jpg"
}
```

### Localized Notifications

Use localization keys so the notification displays in the user's language:

```json
{
    "aps": {
        "alert": {
            "title-loc-key": "NEW_MESSAGE_TITLE",
            "loc-key": "NEW_MESSAGE_BODY",
            "loc-args": ["Alice"]
        }
    }
}
```

## Notification Handling

### UNUserNotificationCenterDelegate

Implement the delegate to control foreground display and handle user taps. Set the delegate as early as possible -- in `application(_:didFinishLaunchingWithOptions:)` or `App.init`.

```swift
@MainActor
final class NotificationDelegate: NSObject, UNUserNotificationCenterDelegate, Sendable {
    static let shared = NotificationDelegate()

    // Called when notification arrives while app is in FOREGROUND
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        // Return which presentation elements to show
        // Without this, foreground notifications are silently suppressed
        return [.banner, .sound, .badge]
    }

    // Called when user TAPS the notification
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {
        let userInfo = response.notification.request.content.userInfo
        let actionIdentifier = response.actionIdentifier

        switch actionIdentifier {
        case UNNotificationDefaultActionIdentifier:
            // User tapped the notification body
            await handleNotificationTap(userInfo: userInfo)
        case UNNotificationDismissActionIdentifier:
            // User dismissed the notification
            break
        default:
            // Custom action button tapped
            await handleCustomAction(actionIdentifier, userInfo: userInfo)
        }
    }
}
```

### Deep Linking from Notifications

Route notification taps to the correct screen using a shared `@Observable` router. The delegate writes a pending destination; the SwiftUI view observes and consumes it.

```swift
@Observable @MainActor
final class DeepLinkRouter {
    var pendingDestination: AppDestination?
}

// In NotificationDelegate:
func handleNotificationTap(userInfo: [AnyHashable: Any]) async {
    guard let id = userInfo["messageId"] as? String else { return }
    DeepLinkRouter.shared.pendingDestination = .chat(id: id)
}

// In SwiftUI -- observe and consume:
.onChange(of: router.pendingDestination) { _, destination in
    if let destination {
        path.append(destination)
        router.pendingDestination = nil
    }
}
```

See `references/notification-patterns.md` for the full deep-linking handler with tab switching.

## Notification Actions and Categories

Define interactive actions that appear as buttons on the notification. Register categories at launch.

### Defining Categories and Actions

```swift
func registerNotificationCategories() {
    let replyAction = UNTextInputNotificationAction(
        identifier: "REPLY_ACTION",
        title: "Reply",
        options: [],
        textInputButtonTitle: "Send",
        textInputPlaceholder: "Type a reply..."
    )

    let likeAction = UNNotificationAction(
        identifier: "LIKE_ACTION",
        title: "Like",
        options: []
    )

    let deleteAction = UNNotificationAction(
        identifier: "DELETE_ACTION",
        title: "Delete",
        options: [.destructive, .authenticationRequired]
    )

    let messageCategory = UNNotificationCategory(
        identifier: "MESSAGE_CATEGORY",
        actions: [replyAction, likeAction, deleteAction],
        intentIdentifiers: [],
        options: [.customDismissAction]  // fires didReceive on dismiss too
    )

    UNUserNotificationCenter.current().setNotificationCategories([messageCategory])
}
```

### Handling Action Responses

```swift
func handleCustomAction(_ identifier: String, userInfo: [AnyHashable: Any]) async {
    switch identifier {
    case "REPLY_ACTION":
        // response is UNTextInputNotificationResponse for text input actions
        break
    case "LIKE_ACTION":
        guard let messageId = userInfo["messageId"] as? String else { return }
        await MessageService.shared.likeMessage(id: messageId)
    case "DELETE_ACTION":
        guard let messageId = userInfo["messageId"] as? String else { return }
        await MessageService.shared.deleteMessage(id: messageId)
    default:
        break
    }
}
```

Action options:
- `.authenticationRequired` -- device must be unlocked to perform the action
- `.destructive` -- displayed in red; use for delete/remove actions
- `.foreground` -- launches the app to the foreground when tapped

## Notification Grouping

Group related notifications with `threadIdentifier` (or `thread-id` in the APNs payload). Each unique thread becomes a separate group in Notification Center.

```swift
content.threadIdentifier = "chat-alice"  // all messages from Alice group together
content.summaryArgument = "Alice"
content.summaryArgumentCount = 3         // "3 more notifications from Alice"
```

Customize the summary format string in the category:

```swift
let category = UNNotificationCategory(
    identifier: "MESSAGE_CATEGORY",
    actions: [replyAction],
    intentIdentifiers: [],
    categorySummaryFormat: "%u more messages from %@",
    options: []
)
```

## Common Mistakes

**DON'T:** Register for remote notifications before requesting authorization.
**DO:** Call `requestAuthorization` first, then `registerForRemoteNotifications()`.

**DON'T:** Convert device token with `String(data: deviceToken, encoding: .utf8)`.
**DO:** Use hex: `deviceToken.map { String(format: "%02x", $0) }.joined()`.

**DON'T:** Assume notifications always arrive. APNs is best-effort.
**DO:** Design features that degrade gracefully; use background refresh as fallback.

**DON'T:** Put sensitive data directly in the notification payload.
**DO:** Use `mutable-content: 1` with a Notification Service Extension.

**DON'T:** Forget foreground handling. Without `willPresent`, notifications are silently suppressed.
**DO:** Implement `willPresent` and return `.banner`, `.sound`, `.badge`.

**DON'T:** Set delegate too late or register from SwiftUI views without AppDelegate adaptor.
**DO:** Set delegate in `App.init`; use `UIApplicationDelegateAdaptor` for APNs.

**DON'T:** Send device token only once — tokens change. Re-send on every callback.

## Review Checklist

- [ ] Authorization requested before registering; denied case handled (Settings link)
- [ ] Device token converted to hex string (not `String(data:encoding:)`)
- [ ] `UNUserNotificationCenterDelegate` set in `App.init` or `application(_:didFinishLaunching:)`
- [ ] Foreground (`willPresent`) and tap (`didReceive`) handling implemented
- [ ] Categories/actions registered at launch if interactive notifications needed
- [ ] Silent push configured (Background Modes enabled); `UIApplicationDelegateAdaptor` for APNs

## References
- `references/notification-patterns.md` — AppDelegate setup, APNs callbacks, deep-link router, silent push, debugging
- `references/rich-notifications.md` — Service Extension, Content Extension, attachments, communication notifications