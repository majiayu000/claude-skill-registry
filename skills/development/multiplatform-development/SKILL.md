---
name: multiplatform-development
description: Cross-platform Apple development patterns for sharing code between iOS, macOS, iPadOS, watchOS, tvOS, and visionOS. Includes conditional compilation, platform-specific extensions, shared packages, and adaptive UI patterns. Use when user asks about multiplatform apps, cross-platform code sharing, platform conditionals, or universal Apple apps.
allowed-tools: Bash, Read, Write, Edit
---

# Multiplatform Development

Comprehensive guide to sharing code across Apple platforms (iOS, macOS, iPadOS, watchOS, tvOS, visionOS) with modern Swift patterns.

## Prerequisites

- Xcode 26+
- Understanding of target platforms

---

## Project Setup

### Multiplatform Target Configuration

```swift
// Package.swift for a multiplatform library
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "SharedKit",
    platforms: [
        .iOS(.v17),
        .macOS(.v14),
        .watchOS(.v10),
        .tvOS(.v17),
        .visionOS(.v1)
    ],
    products: [
        .library(name: "SharedKit", targets: ["SharedKit"])
    ],
    targets: [
        .target(
            name: "SharedKit",
            dependencies: []
        ),
        .testTarget(
            name: "SharedKitTests",
            dependencies: ["SharedKit"]
        )
    ]
)
```

### Xcode Project Structure

```
MyApp/
├── Shared/                    # Shared code
│   ├── Models/
│   ├── ViewModels/
│   ├── Services/
│   └── Utilities/
├── iOS/                       # iOS-specific
│   ├── Views/
│   └── AppDelegate.swift
├── macOS/                     # macOS-specific
│   ├── Views/
│   └── Commands.swift
├── watchOS/                   # watchOS-specific
│   └── WatchApp.swift
└── Packages/                  # Local Swift packages
    └── CoreKit/
```

---

## Conditional Compilation

### Platform Checks

```swift
// Compile-time platform checks
#if os(iOS)
import UIKit
typealias PlatformColor = UIColor
typealias PlatformImage = UIImage
#elseif os(macOS)
import AppKit
typealias PlatformColor = NSColor
typealias PlatformImage = NSImage
#elseif os(watchOS)
import WatchKit
typealias PlatformColor = UIColor
#elseif os(tvOS)
import UIKit
typealias PlatformColor = UIColor
#elseif os(visionOS)
import UIKit
typealias PlatformColor = UIColor
#endif
```

### Combined Conditions

```swift
// Multiple conditions
#if os(iOS) || os(tvOS)
// Shared iOS/tvOS code
#endif

#if os(iOS) && !targetEnvironment(macCatalyst)
// iOS but NOT Mac Catalyst
#endif

#if targetEnvironment(macCatalyst)
// Mac Catalyst specific
#endif

#if targetEnvironment(simulator)
// Simulator only (testing)
#endif

#if canImport(UIKit)
import UIKit
// Any platform with UIKit (iOS, tvOS, watchOS, visionOS, Catalyst)
#endif

#if canImport(AppKit)
import AppKit
// macOS only
#endif
```

### Feature Availability

```swift
// API availability
@available(iOS 17, macOS 14, watchOS 10, tvOS 17, visionOS 1, *)
struct ModernFeature {
    // Available on all platforms with specified versions
}

// Exclude platforms
@available(iOS 17, macOS 14, *)
@available(watchOS, unavailable)
@available(tvOS, unavailable)
struct DesktopOnlyFeature {
    // Only iOS and macOS
}

// Runtime checks
if #available(iOS 18, macOS 15, *) {
    // Use new API
} else {
    // Fallback
}
```

---

## Cross-Platform Abstractions

### Platform-Agnostic Colors

```swift
import SwiftUI

extension Color {
    // Platform-adaptive semantic colors
    static var platformBackground: Color {
        #if os(macOS)
        Color(nsColor: .windowBackgroundColor)
        #else
        Color(uiColor: .systemBackground)
        #endif
    }

    static var platformSecondaryBackground: Color {
        #if os(macOS)
        Color(nsColor: .controlBackgroundColor)
        #else
        Color(uiColor: .secondarySystemBackground)
        #endif
    }

    static var platformLabel: Color {
        #if os(macOS)
        Color(nsColor: .labelColor)
        #else
        Color(uiColor: .label)
        #endif
    }
}

// Usage - works everywhere
struct ContentView: View {
    var body: some View {
        Text("Hello")
            .foregroundStyle(Color.platformLabel)
            .background(Color.platformBackground)
    }
}
```

### Cross-Platform Images

```swift
import SwiftUI

extension Image {
    /// Load image that works across platforms
    init(crossPlatform name: String) {
        #if os(macOS)
        if let nsImage = NSImage(named: name) {
            self.init(nsImage: nsImage)
        } else {
            self.init(systemName: "questionmark")
        }
        #else
        if let uiImage = UIImage(named: name) {
            self.init(uiImage: uiImage)
        } else {
            self.init(systemName: "questionmark")
        }
        #endif
    }
}

// Cross-platform image data handling
struct ImageData {
    let data: Data

    var image: Image? {
        #if os(macOS)
        guard let nsImage = NSImage(data: data) else { return nil }
        return Image(nsImage: nsImage)
        #else
        guard let uiImage = UIImage(data: data) else { return nil }
        return Image(uiImage: uiImage)
        #endif
    }
}
```

### Platform-Adaptive View Modifiers

```swift
extension View {
    /// Apply platform-specific navigation style
    @ViewBuilder
    func platformNavigationStyle() -> some View {
        #if os(macOS)
        self.frame(minWidth: 600, minHeight: 400)
        #elseif os(iOS)
        self.navigationViewStyle(.stack)
        #elseif os(watchOS)
        self.navigationViewStyle(.automatic)
        #else
        self
        #endif
    }

    /// Platform-appropriate list style
    @ViewBuilder
    func platformListStyle() -> some View {
        #if os(macOS)
        self.listStyle(.sidebar)
        #elseif os(iOS)
        self.listStyle(.insetGrouped)
        #elseif os(watchOS)
        self.listStyle(.carousel)
        #else
        self.listStyle(.automatic)
        #endif
    }

    /// Hover effect (only where supported)
    @ViewBuilder
    func platformHoverEffect() -> some View {
        #if os(macOS) || os(visionOS) || targetEnvironment(macCatalyst)
        self.onHover { isHovered in
            // Handle hover
        }
        #else
        self
        #endif
    }
}
```

---

## Adaptive Layouts

### Device-Aware Layouts

```swift
struct AdaptiveLayout: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    @Environment(\.verticalSizeClass) private var verticalSizeClass

    var body: some View {
        Group {
            #if os(macOS)
            // macOS: Always use sidebar
            NavigationSplitView {
                Sidebar()
            } detail: {
                DetailView()
            }
            #elseif os(iOS)
            // iOS: Adapt to size class
            if horizontalSizeClass == .regular {
                NavigationSplitView {
                    Sidebar()
                } detail: {
                    DetailView()
                }
            } else {
                NavigationStack {
                    CompactView()
                }
            }
            #elseif os(watchOS)
            // watchOS: Simple list
            NavigationStack {
                WatchList()
            }
            #elseif os(tvOS)
            // tvOS: Focus-based navigation
            TabView {
                ContentGrid()
            }
            #elseif os(visionOS)
            // visionOS: Spatial layout
            NavigationSplitView {
                Sidebar()
            } detail: {
                DetailView()
            }
            .ornament(attachmentAnchor: .scene(.bottom)) {
                ControlsView()
            }
            #endif
        }
    }
}
```

### ViewThatFits for Responsive Design

```swift
struct ResponsiveHeader: View {
    let title: String
    let subtitle: String

    var body: some View {
        ViewThatFits(in: .horizontal) {
            // Try full layout first
            HStack {
                VStack(alignment: .leading) {
                    Text(title).font(.largeTitle)
                    Text(subtitle).font(.subheadline)
                }
                Spacer()
                ActionButtons()
            }

            // Fall back to compact
            VStack {
                Text(title).font(.title)
                Text(subtitle).font(.caption)
                ActionButtons()
            }
        }
    }
}
```

---

## Shared Business Logic

### Platform-Agnostic ViewModels

```swift
import Foundation
import Observation

// Works on all platforms
@Observable
class NotesViewModel {
    var notes: [Note] = []
    var isLoading = false
    var error: Error?

    private let repository: NotesRepository

    init(repository: NotesRepository = .shared) {
        self.repository = repository
    }

    func load() async {
        isLoading = true
        defer { isLoading = false }

        do {
            notes = try await repository.fetchNotes()
        } catch {
            self.error = error
        }
    }

    func create(title: String, content: String) async {
        let note = Note(title: title, content: content)
        notes.append(note)

        do {
            try await repository.save(note)
        } catch {
            notes.removeLast()
            self.error = error
        }
    }
}
```

### Protocol-Based Platform Abstraction

```swift
// Shared protocol
protocol PlatformCapabilities {
    var supportsHaptics: Bool { get }
    var supportsPencil: Bool { get }
    var supportsKeyboard: Bool { get }
    var maxImageResolution: CGSize { get }
    func openURL(_ url: URL)
}

// iOS implementation
#if os(iOS)
class iOSCapabilities: PlatformCapabilities {
    var supportsHaptics: Bool { true }
    var supportsPencil: Bool { UIDevice.current.userInterfaceIdiom == .pad }
    var supportsKeyboard: Bool { true }
    var maxImageResolution: CGSize { CGSize(width: 4096, height: 4096) }

    func openURL(_ url: URL) {
        UIApplication.shared.open(url)
    }
}
#endif

// macOS implementation
#if os(macOS)
class macOSCapabilities: PlatformCapabilities {
    var supportsHaptics: Bool { true }
    var supportsPencil: Bool { false }
    var supportsKeyboard: Bool { true }
    var maxImageResolution: CGSize { CGSize(width: 16384, height: 16384) }

    func openURL(_ url: URL) {
        NSWorkspace.shared.open(url)
    }
}
#endif

// Factory
enum Platform {
    static var capabilities: PlatformCapabilities {
        #if os(iOS)
        return iOSCapabilities()
        #elseif os(macOS)
        return macOSCapabilities()
        #else
        fatalError("Platform not supported")
        #endif
    }
}
```

---

## Shared Swift Packages

### Creating a Shared Package

```swift
// Package.swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "AppCore",
    platforms: [
        .iOS(.v17),
        .macOS(.v14),
        .watchOS(.v10),
        .tvOS(.v17),
        .visionOS(.v1)
    ],
    products: [
        .library(name: "AppCore", targets: ["AppCore"]),
        .library(name: "AppUI", targets: ["AppUI"])
    ],
    dependencies: [
        // Shared dependencies
    ],
    targets: [
        // Core business logic - no UI dependencies
        .target(
            name: "AppCore",
            dependencies: []
        ),
        // Shared UI components
        .target(
            name: "AppUI",
            dependencies: ["AppCore"]
        ),
        .testTarget(
            name: "AppCoreTests",
            dependencies: ["AppCore"]
        )
    ]
)
```

### Package with Platform-Specific Code

```swift
// Sources/AppUI/PlatformButton.swift
import SwiftUI

public struct PlatformButton: View {
    let title: String
    let action: () -> Void

    public init(_ title: String, action: @escaping () -> Void) {
        self.title = title
        self.action = action
    }

    public var body: some View {
        Button(title, action: action)
            .platformButtonStyle()
    }
}

private extension View {
    @ViewBuilder
    func platformButtonStyle() -> some View {
        #if os(macOS)
        self.buttonStyle(.borderedProminent)
            .controlSize(.large)
        #elseif os(iOS)
        self.buttonStyle(.borderedProminent)
            .buttonBorderShape(.capsule)
        #elseif os(watchOS)
        self.buttonStyle(.bordered)
        #elseif os(tvOS)
        self.buttonStyle(.card)
        #else
        self
        #endif
    }
}
```

---

## Platform-Specific Entry Points

### Multiplatform App Entry

```swift
import SwiftUI

@main
struct MyMultiplatformApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        #if os(macOS)
        .commands {
            AppCommands()
        }

        Settings {
            SettingsView()
        }

        MenuBarExtra("Status", systemImage: "star") {
            StatusMenu()
        }
        #endif

        #if os(visionOS)
        ImmersiveSpace(id: "immersive") {
            ImmersiveView()
        }
        #endif
    }

    init() {
        configurePlatform()
    }

    private func configurePlatform() {
        #if os(iOS)
        configureIOS()
        #elseif os(macOS)
        configureMacOS()
        #elseif os(watchOS)
        configureWatchOS()
        #endif
    }

    #if os(iOS)
    private func configureIOS() {
        // iOS-specific setup
    }
    #endif

    #if os(macOS)
    private func configureMacOS() {
        // macOS-specific setup
    }
    #endif

    #if os(watchOS)
    private func configureWatchOS() {
        // watchOS-specific setup
    }
    #endif
}
```

---

## Testing Across Platforms

### Shared Test Utilities

```swift
import Testing
@testable import AppCore

// Works on all platforms
@Test
func testNoteCreation() {
    let note = Note(title: "Test", content: "Content")

    #expect(note.title == "Test")
    #expect(note.content == "Content")
    #expect(note.createdAt <= Date())
}

@Test
func testNoteSerialization() throws {
    let note = Note(title: "Test", content: "Content")
    let data = try JSONEncoder().encode(note)
    let decoded = try JSONDecoder().decode(Note.self, from: data)

    #expect(decoded.title == note.title)
}

// Platform-specific tests
#if os(iOS)
@Test
func testHapticFeedback() {
    let haptics = HapticManager()
    #expect(haptics.isSupported == true)
}
#endif
```

### Conditional Test Execution

```swift
import Testing

struct PlatformTests {
    @Test(.enabled(if: isIOS))
    func testIOSFeature() {
        // Only runs on iOS
    }

    @Test(.enabled(if: isMacOS))
    func testMacOSFeature() {
        // Only runs on macOS
    }

    private static var isIOS: Bool {
        #if os(iOS)
        return true
        #else
        return false
        #endif
    }

    private static var isMacOS: Bool {
        #if os(macOS)
        return true
        #else
        return false
        #endif
    }
}
```

---

## Best Practices

### DO

```swift
// ✓ Use canImport for optional framework dependencies
#if canImport(WidgetKit)
import WidgetKit
#endif

// ✓ Abstract platform differences behind protocols
protocol ClipboardService {
    func copy(_ text: String)
    func paste() -> String?
}

// ✓ Use SwiftUI's built-in adaptivity
.navigationSplitViewStyle(.balanced)

// ✓ Share ViewModels and business logic
@Observable class SharedViewModel { }

// ✓ Put platform code in separate files
// iOS/iOSSpecificView.swift
// macOS/macOSSpecificView.swift
```

### DON'T

```swift
// ✗ Don't scatter #if throughout views
struct MyView: View {
    var body: some View {
        #if os(iOS)
        // 50 lines of iOS code
        #elseif os(macOS)
        // 50 lines of macOS code
        #endif
    }
}

// ✗ Don't hardcode platform assumptions
let isPhone = UIDevice.current.userInterfaceIdiom == .phone  // Wrong

// ✗ Don't ignore size classes on iPad
// Always support both compact and regular

// ✗ Don't use UIKit/AppKit directly in shared code
// Wrap in platform abstractions
```

### File Organization

```
Shared/
├── Models/          # Pure Swift, no UI imports
├── Services/        # Platform-agnostic business logic
├── ViewModels/      # @Observable classes
└── Extensions/      # Swift extensions

Platform/
├── iOS/
│   └── Views/
├── macOS/
│   └── Views/
└── Shared/          # SwiftUI views that work everywhere
```

---

## Official Resources

- [Creating a multiplatform app](https://developer.apple.com/documentation/xcode/creating-a-multiplatform-app)
- [Configuring a multiplatform app](https://developer.apple.com/documentation/xcode/configuring-a-multiplatform-app-target)
- [WWDC22: Use SwiftUI with UIKit](https://developer.apple.com/videos/play/wwdc2022/10072/)
- [WWDC21: What's new in SwiftUI](https://developer.apple.com/videos/play/wwdc2021/10018/)
