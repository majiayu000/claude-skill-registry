---
name: app-lifecycle
description: "Expert lifecycle decisions for iOS/tvOS: when SwiftUI lifecycle vs SceneDelegate, background task strategies, state restoration trade-offs, and launch optimization. Use when managing app state transitions, handling background work, or debugging lifecycle issues. Trigger keywords: lifecycle, scenePhase, SceneDelegate, AppDelegate, background task, state restoration, launch time, didFinishLaunching, applicationWillTerminate, sceneDidBecomeActive"
version: "3.0.0"
---

# App Lifecycle — Expert Decisions

Expert decision frameworks for app lifecycle choices. Claude knows scenePhase and SceneDelegate — this skill provides judgment calls for architecture decisions and background task trade-offs.

---

## Decision Trees

### Lifecycle API Selection

```
What's your project setup?
├─ Pure SwiftUI app (iOS 14+)
│  └─ @main App + scenePhase
│     Simplest approach, sufficient for most apps
│
├─ Need UIKit integration
│  └─ SceneDelegate + UIHostingController
│     Required for some third-party SDKs
│
├─ Need pre-launch setup
│  └─ AppDelegate + SceneDelegate
│     SDK initialization, remote notifications
│
└─ Legacy app (pre-iOS 13)
   └─ AppDelegate only
      window property on AppDelegate
```

**The trap**: Using SceneDelegate when pure SwiftUI suffices. scenePhase covers most use cases without the boilerplate.

### Background Task Strategy

```
What work needs to happen in background?
├─ Quick save (< 5 seconds)
│  └─ UIApplication.beginBackgroundTask
│     Request extra time in sceneDidEnterBackground
│
├─ Network sync (< 30 seconds)
│  └─ BGAppRefreshTask
│     System schedules, best-effort timing
│
├─ Large download/upload
│  └─ Background URL Session
│     Continues even after app termination
│
├─ Location tracking
│  └─ Location background mode
│     Significant change or continuous
│
└─ Long processing (> 30 seconds)
   └─ BGProcessingTask
      Runs during charging, overnight
```

### State Restoration Approach

```
What state needs restoration?
├─ Simple navigation state
│  └─ @SceneStorage
│     Per-scene, automatic, Codable types only
│
├─ Complex navigation + data
│  └─ @AppStorage + manual encoding
│     More control, cross-scene sharing
│
├─ UIKit-based navigation
│  └─ State restoration identifiers
│     encodeRestorableState/decodeRestorableState
│
└─ Don't need restoration
   └─ Start fresh each launch
      Some apps are better this way
```

### Launch Optimization Priority

```
What's blocking your launch time?
├─ SDK initialization
│  └─ Defer non-critical SDKs
│     Analytics can wait, auth cannot
│
├─ Database loading
│  └─ Lazy loading + skeleton UI
│     Show UI immediately, load data async
│
├─ Network requests
│  └─ Cache + background refresh
│     Never block launch for network
│
└─ Asset loading
   └─ Progressive loading
      Load visible content first
```

---

## NEVER Do

### Launch Time

**NEVER** block main thread during launch:
```swift
// ❌ UI frozen until network completes
func application(_ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    let data = try! Data(contentsOf: remoteURL)  // Synchronous network!
    processData(data)
    return true
}

// ✅ Defer non-critical work
func application(_ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    setupCriticalServices()  // Auth, crash reporting

    Task.detached(priority: .background) {
        await self.setupNonCriticalServices()  // Analytics, prefetch
    }
    return true
}
```

**NEVER** initialize all SDKs synchronously:
```swift
// ❌ Each SDK adds to launch time
func application(...) -> Bool {
    AnalyticsSDK.initialize()      // 100ms
    CrashReporterSDK.initialize()  // 50ms
    FeatureFlagsSDK.initialize()   // 200ms
    SocialSDK.initialize()         // 150ms
    // Total: 500ms added to launch!
    return true
}

// ✅ Prioritize and defer
func application(...) -> Bool {
    CrashReporterSDK.initialize()  // Critical — catches launch crashes

    DispatchQueue.main.async {
        AnalyticsSDK.initialize()  // Can wait one runloop
    }

    Task.detached(priority: .utility) {
        FeatureFlagsSDK.initialize()
        SocialSDK.initialize()
    }
    return true
}
```

### Background Tasks

**NEVER** assume background time is guaranteed:
```swift
// ❌ May not complete — iOS can terminate anytime
func sceneDidEnterBackground(_ scene: UIScene) {
    performLongSync()  // No protection!
}

// ✅ Request background time and handle expiration
func sceneDidEnterBackground(_ scene: UIScene) {
    var taskId: UIBackgroundTaskIdentifier = .invalid
    taskId = UIApplication.shared.beginBackgroundTask {
        // Expiration handler — save partial progress
        savePartialProgress()
        UIApplication.shared.endBackgroundTask(taskId)
    }

    Task {
        await performSync()
        UIApplication.shared.endBackgroundTask(taskId)
    }
}
```

**NEVER** forget to end background tasks:
```swift
// ❌ Leaks background task — iOS may terminate app
func saveData() {
    let taskId = UIApplication.shared.beginBackgroundTask { }
    saveToDatabase()
    // Missing: endBackgroundTask!
}

// ✅ Always end in both success and failure
func saveData() {
    var taskId: UIBackgroundTaskIdentifier = .invalid
    taskId = UIApplication.shared.beginBackgroundTask {
        UIApplication.shared.endBackgroundTask(taskId)
    }

    defer { UIApplication.shared.endBackgroundTask(taskId) }

    do {
        try saveToDatabase()
    } catch {
        Logger.app.error("Save failed: \(error)")
    }
}
```

### State Transitions

**NEVER** trust applicationWillTerminate to be called:
```swift
// ❌ May never be called — iOS can kill app without notice
func applicationWillTerminate(_ application: UIApplication) {
    saveCriticalData()  // Not guaranteed to run!
}

// ✅ Save on every background transition
func sceneDidEnterBackground(_ scene: UIScene) {
    saveCriticalData()  // Called reliably
}

// Also save periodically during use
Timer.scheduledTimer(withTimeInterval: 60, repeats: true) { _ in
    saveApplicationState()
}
```

**NEVER** do heavy work in sceneWillResignActive:
```swift
// ❌ Blocks app switcher animation
func sceneWillResignActive(_ scene: UIScene) {
    generateThumbnails()  // Visible lag in app switcher
    syncToServer()        // Delays user
}

// ✅ Only pause essential operations
func sceneWillResignActive(_ scene: UIScene) {
    pauseVideoPlayback()
    pauseAnimations()
    // Heavy work goes in sceneDidEnterBackground
}
```

### Scene Lifecycle

**NEVER** confuse scene disconnect with app termination:
```swift
// ❌ Wrong assumption
func sceneDidDisconnect(_ scene: UIScene) {
    // App is terminating!  <- WRONG
    cleanupEverything()
}

// ✅ Scene disconnect means scene released, not app death
func sceneDidDisconnect(_ scene: UIScene) {
    // Scene being released — save per-scene state
    // App may continue running with other scenes
    // Or system may reconnect this scene later
    saveSceneState(scene)
}
```

---

## Essential Patterns

### SwiftUI Lifecycle Handler

```swift
@main
struct MyApp: App {
    @Environment(\.scenePhase) private var scenePhase
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
        .onChange(of: scenePhase) { oldPhase, newPhase in
            handlePhaseChange(from: oldPhase, to: newPhase)
        }
    }

    private func handlePhaseChange(from old: ScenePhase, to new: ScenePhase) {
        switch (old, new) {
        case (_, .active):
            appState.refreshDataIfStale()

        case (.active, .inactive):
            // Transitioning away — pause but don't save yet
            appState.pauseActiveOperations()

        case (_, .background):
            appState.saveState()
            scheduleBackgroundRefresh()

        default:
            break
        }
    }
}
```

### Background Task Manager

```swift
final class BackgroundTaskManager {
    static let shared = BackgroundTaskManager()

    func registerTasks() {
        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: "com.app.refresh",
            using: nil
        ) { task in
            self.handleAppRefresh(task as! BGAppRefreshTask)
        }

        BGTaskScheduler.shared.register(
            forTaskWithIdentifier: "com.app.processing",
            using: nil
        ) { task in
            self.handleProcessing(task as! BGProcessingTask)
        }
    }

    func scheduleRefresh() {
        let request = BGAppRefreshTaskRequest(identifier: "com.app.refresh")
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60)

        try? BGTaskScheduler.shared.submit(request)
    }

    private func handleAppRefresh(_ task: BGAppRefreshTask) {
        scheduleRefresh()  // Schedule next refresh

        let refreshTask = Task {
            await performRefresh()
        }

        task.expirationHandler = {
            refreshTask.cancel()
        }

        Task {
            await refreshTask.value
            task.setTaskCompleted(success: true)
        }
    }
}
```

### Launch Time Optimization

```swift
@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    private var launchStartTime: CFAbsoluteTime = 0

    func application(_ application: UIApplication,
        willFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        launchStartTime = CFAbsoluteTimeGetCurrent()

        // Phase 1: Absolute minimum (crash reporting)
        CrashReporter.initialize()

        return true
    }

    func application(_ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Phase 2: Required for first frame
        configureAppearance()

        // Phase 3: Deferred to after first frame
        DispatchQueue.main.async {
            self.completePostLaunchSetup()
            let launchTime = CFAbsoluteTimeGetCurrent() - self.launchStartTime
            Logger.app.info("Launch completed in \(launchTime)s")
        }

        return true
    }

    private func completePostLaunchSetup() {
        // Analytics, feature flags, etc.
        Task.detached(priority: .utility) {
            Analytics.initialize()
            FeatureFlags.refresh()
        }
    }
}
```

---

## Quick Reference

### Lifecycle Events Order

| Event | When | Use For |
|-------|------|---------|
| willFinishLaunching | Before UI | Crash reporting only |
| didFinishLaunching | UI ready | Critical setup |
| sceneWillEnterForeground | Coming to front | Undo background changes |
| sceneDidBecomeActive | Fully active | Refresh, restart tasks |
| sceneWillResignActive | Losing focus | Pause playback |
| sceneDidEnterBackground | In background | Save state, start bg task |
| sceneDidDisconnect | Scene released | Save scene state |

### Background Task Limits

| Task Type | Time Limit | When Runs |
|-----------|-----------|-----------|
| beginBackgroundTask | ~30 seconds | Immediately |
| BGAppRefreshTask | ~30 seconds | System discretion |
| BGProcessingTask | Minutes | Charging, overnight |
| Background URL Session | Unlimited | System managed |

### State Restoration Options

| Approach | Scope | Types | Auto-save |
|----------|-------|-------|-----------|
| @SceneStorage | Per-scene | Codable | Yes |
| @AppStorage | App-wide | Primitives | Yes |
| Restoration ID | Per-VC | Custom | Manual |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Sync network in launch | Blocked UI | Async + skeleton UI |
| All SDKs in didFinish | Slow launch | Prioritize + defer |
| No beginBackgroundTask | Work may not complete | Always request time |
| Missing endBackgroundTask | Leaked task | Use defer |
| Heavy work in willResignActive | Laggy app switcher | Move to didEnterBackground |
| Trust applicationWillTerminate | May not be called | Save on background |
| Confuse sceneDidDisconnect | Scene != app termination | Save scene state only |
