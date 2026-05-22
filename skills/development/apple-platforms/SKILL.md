---
name: apple-platforms
description: Build apps for macOS, iPadOS, watchOS, and visionOS with platform-specific features. Use when creating menu bar apps, iPad split views, Apple Watch complications, Vision Pro immersive experiences, or multi-platform adaptations.
user-invocable: false
---

# Apple Platform Development

## macOS Specifics

```swift
@main
struct MacApp: App {
    var body: some Scene {
        // Main window
        WindowGroup {
            ContentView()
        }
        .windowStyle(.hiddenTitleBar)
        .windowToolbarStyle(.unified(showsTitle: true))
        .defaultSize(width: 900, height: 600)
        .commands {
            CommandGroup(replacing: .newItem) {
                Button("New Document") { }
                    .keyboardShortcut("n", modifiers: .command)
            }
            ToolbarCommands()
        }

        // Menu bar app
        MenuBarExtra("Status", systemImage: "star.fill") {
            Button("Preferences...") { openSettings() }
            Divider()
            Button("Quit") { NSApp.terminate(nil) }
        }
        .menuBarExtraStyle(.window)

        // Settings window
        Settings {
            SettingsView()
        }
    }
}
```

## iPadOS Adaptive Layouts

```swift
struct AdaptiveView: View {
    @Environment(\.horizontalSizeClass) var sizeClass

    var body: some View {
        if sizeClass == .compact {
            // iPhone or iPad slide-over
            TabView {
                HomeTab()
                SearchTab()
            }
        } else {
            // iPad full screen
            NavigationSplitView {
                Sidebar()
            } detail: {
                DetailView()
            }
        }
    }
}

// Keyboard shortcuts for iPad
struct ContentView: View {
    var body: some View {
        List { }
            .keyboardShortcut("f", modifiers: .command)
            .focusable()
    }
}
```

## watchOS

```swift
@main
struct WatchApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// Workout tracking
class WorkoutManager: NSObject, ObservableObject {
    private var session: HKWorkoutSession?
    private var builder: HKLiveWorkoutBuilder?
    @Published var heartRate: Double = 0

    func startWorkout(type: HKWorkoutActivityType) async throws {
        let config = HKWorkoutConfiguration()
        config.activityType = type
        config.locationType = .outdoor

        session = try HKWorkoutSession(
            healthStore: HKHealthStore(),
            configuration: config
        )
        builder = session?.associatedWorkoutBuilder()
        session?.startActivity(with: .now)
        try await builder?.beginCollection(at: .now)
    }
}
```

## visionOS Spatial Computing

```swift
@main
struct VisionApp: App {
    var body: some Scene {
        // 2D window
        WindowGroup {
            ContentView()
        }

        // 3D volume
        WindowGroup(id: "globe") {
            Globe3DView()
        }
        .windowStyle(.volumetric)
        .defaultSize(width: 0.5, height: 0.5, depth: 0.5, in: .meters)

        // Immersive space
        ImmersiveSpace(id: "solar-system") {
            SolarSystemView()
        }
        .immersionStyle(selection: .constant(.mixed), in: .mixed)
    }
}

// RealityKit integration
struct ImmersiveView: View {
    var body: some View {
        RealityView { content in
            let sphere = ModelEntity(mesh: .generateSphere(radius: 0.1))
            sphere.position = [0, 1.5, -1]
            content.add(sphere)
        }
        .gesture(TapGesture().targetedToAnyEntity())
    }
}
```

## Multi-Platform Code

```swift
#if os(iOS)
typealias PlatformColor = UIColor
#elseif os(macOS)
typealias PlatformColor = NSColor
#endif

// Conditional compilation
struct ContentView: View {
    var body: some View {
        #if os(watchOS)
        CompactView()
        #elseif os(tvOS)
        LargeDisplayView()
        #else
        StandardView()
        #endif
    }
}
```
