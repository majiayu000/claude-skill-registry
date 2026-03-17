---
name: ios-watchos
cluster: mobile
description: "watchOS: WidgetKit complications, WatchConnectivity, SwiftUI on Watch, HealthKit, OpenClaw Watch extension"
tags: ["watchos","complications","healthkit","openclaw-watch"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "watchos complication watch extension healthkit workout openclaw"
---

# ios-watchos

## Purpose
This skill enables development of watchOS apps using Swift and Apple's frameworks, focusing on WidgetKit for complications, WatchConnectivity for device syncing, SwiftUI for interfaces, HealthKit for health data access, and OpenClaw Watch extensions for custom features.

## When to Use
Use this skill for building watchOS apps that need dynamic complications (e.g., updating timelines), real-time data transfer from iOS devices, custom SwiftUI layouts on the Watch, querying health metrics like workouts, or integrating OpenClaw for extended functionality. Apply it in scenarios like fitness tracking apps or notification-based tools.

## Key Capabilities
- WidgetKit complications: Create timeline-based updates for watch faces, e.g., using TimelineProvider to refresh data every 15 minutes.
- WatchConnectivity: Establish sessions for sending/receiving data between iOS and watchOS, handling transfers up to 100KB per message.
- SwiftUI on Watch: Build responsive interfaces with components like NavigationView and List, optimized for small screens (e.g., 44mm display).
- HealthKit: Access health data types such as HKWorkout and HKQuantityTypeStepCount, with background delivery for real-time updates.
- OpenClaw Watch extension: Leverage custom APIs for enhanced app features, requiring authentication via $OPENCLAW_API_KEY for secure connections.

## Usage Patterns
Follow these patterns for effective implementation:
1. For complications: Set up a WidgetKit extension in Xcode, implement a TimelineProvider subclass, and use getTimeline(in:completion:) to generate entries. Example: In your provider, return an array of TimelineEntry objects with dates and views.
2. For HealthKit integration: Request authorization for specific data types, then query samples. Example: Use HKSampleQuery to fetch workout data after checking permissions.
3. Common pattern: Use WatchConnectivity to sync data; activate WCSession in AppDelegate and handle incoming messages in didReceiveMessage.
4. For OpenClaw: Initialize the extension with an API key and handle events in a delegate. Example: Call OpenClawSession.shared.start(with: $OPENCLAW_API_KEY) in your app's launch sequence.
5. Concrete usage example 1: Build a complication for a fitness app—create a TimelineProvider that queries HealthKit for step count and updates every hour: let entry = TimelineEntry(date: Date(), stepCount: 500); provider.getTimeline(in: context, completion: { timeline in ... }).
6. Concrete usage example 2: Sync workout data from iOS to Watch—use WCSession.default.sendMessage(["workoutID": "123"], replyHandler: nil) in the iOS app, and process it in the Watch app's session(didReceiveMessage: handler).

## Common Commands/API
- Xcode command: Build and run a watchOS app with xcodebuild -scheme WatchAppExtension -destination 'platform=watchOS Simulator,name=Apple Watch Series 6' -configuration Debug. Use this in CI/CD pipelines.
- WidgetKit API: Implement a simple TimelineProvider: class MyProvider: TimelineProvider { func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> ()) { let entry = SimpleEntry(date: Date()); completion(entry) } }.
- WatchConnectivity API: Activate session with WCSession.default.activate(); send data: WCSession.default.sendMessage(["key": "value"], replyHandler: nil, errorHandler: nil).
- HealthKit API: Request authorization: let typesToRead = Set([HKObjectType.workoutType()]); HKHealthStore().requestAuthorization(toShare: nil, read: typesToRead) { granted, error in if granted { // Proceed } }.
- OpenClaw API: Initialize with auth: let session = OpenClawSession(apiKey: ProcessEnv.get("OPENCLAW_API_KEY")); session.connect(endpoint: "wss://api.openclaw.com/watch"); handle responses in session.delegate.didReceiveData.
- Config format: Use a JSON config for OpenClaw: { "apiKey": "$OPENCLAW_API_KEY", "endpoint": "wss://api.openclaw.com/watch", "watchID": "device-uuid" }. Load it via let config = try JSONDecoder().decode(OpenClawConfig.self, from: data).

## Integration Notes
Integrate this skill by adding a watchOS target in Xcode: Go to File > New > Target > watchOS > Watch App, then link it to your iOS app via group capabilities. For HealthKit, enable the HealthKit capability in project settings and add the NSHealthShareUsageDescription key to Info.plist. When using WatchConnectivity, ensure both iOS and watchOS apps share the same App Group entitlement. For OpenClaw, set the $OPENCLAW_API_KEY environment variable in your build script (e.g., export OPENCLAW_API_KEY=your_key) and import the OpenClaw SDK via Swift Package Manager: .package(url: "https://github.com/openclaw/sdk.git", from: "1.0.0"). Test integrations with Simulator: Run the watchOS app on Apple Watch Simulator and verify data flow using the Console app for logs.

## Error Handling
Handle errors proactively: For WidgetKit, check for timeline errors in getTimeline and retry on failures (e.g., if context invalid, log and return an empty timeline). For WatchConnectivity, catch WCSession errors like .notReachable and queue messages for later. In HealthKit, verify authorization before queries—e.g., if HKError.Code.errorAuthorizationDenied, prompt user via UIAlertController with a retry button. For OpenClaw, parse API errors (e.g., 401 Unauthorized) and refresh $OPENCLAW_API_KEY if expired. Use try-catch in Swift for API calls: do { try OpenClawSession.shared.connect() } catch let error as OpenClawError { print(error.localizedDescription); retry after delay }. Log all errors with os_log for debugging.

## Graph Relationships
- Related to: mobile cluster (e.g., shares tags with ios skill for cross-platform features).
- Links to: ios skill via WatchConnectivity for iOS-Watch syncing.
- Connected via: watchos tag, healthkit integration with fitness-related skills, and openclaw-watch for custom extensions.
