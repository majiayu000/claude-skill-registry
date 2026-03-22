---
name: macos-programmer
description: macOS-specific development patterns, platform APIs, and decision frameworks. Use when developing Mac apps, macOS applications, Cocoa/AppKit code, or making SwiftUI vs AppKit decisions. Covers NSWindow management, NSDocument architecture, sandboxing, code signing, notarization, and macOS UI patterns. Applies to Mac Catalyst considerations.
---

# macOS Programming

<skill_scope skill="macos-programmer">
**Related skills:**
- `swift-programmer` — Swift language fundamentals and Swift 6 concurrency
- `software-engineer` — General software engineering principles and system architecture
- `test-driven-development` — Testing philosophy and practices

This skill covers macOS-specific development patterns, platform APIs, and decision frameworks. It applies when developing Mac apps, working with Cocoa/AppKit code, or making SwiftUI vs AppKit decisions.
</skill_scope>

## Core Philosophy

<core_philosophy>
**Critical Reality (2024-2025):** SwiftUI for macOS is powerful but incomplete for production apps. Expert macOS developers must master BOTH SwiftUI and AppKit—SwiftUI for 70% of UI, AppKit for the 30% that makes professional apps professional. This hybrid approach is not a stopgap; it's the current production reality.

**Platform Identity:** macOS is not iOS with a bigger screen. Multiple windows, menu bars, keyboard navigation, document-based architecture, and precise window management are first-class citizens. Respect macOS conventions; don't port iOS patterns blindly.
</core_philosophy>

## SwiftUI vs AppKit: The Critical Decision Framework

<swiftui_vs_appkit_decision>
**The Ground Truth from Production Apps:**

SwiftUI maturity varies dramatically by platform. The Ghostty Terminal case study demonstrates this: had to completely rip out SwiftUI's app/window lifecycle (+802/-239 lines) just to implement non-native fullscreen.[^ghostty-devlog] Multi.app's approach: moved to SwiftUI but noted they were "approaching the cusp of dropping macOS 11 support entirely" due to SwiftUI bugs on older versions.[^multi-swiftui]

**Use SwiftUI When:**
- New apps targeting macOS 14+, simple-to-medium complexity
- Standard UI elements suffice (lists, forms, navigation)
- Cross-platform iOS/macOS with acceptable compromises
- Rapid prototyping where bugs are acceptable
- Team willing to use NSViewRepresentable for 20-30% of features
- Can afford to drop users on macOS <14 (SwiftUI bugs improved significantly in Sonoma)

**Use AppKit When:**
- Complex text editing (code editors, word processors, NSTextView-dependent workflows)
- Large datasets (1000+ items—SwiftUI List has significant performance issues compared to NSTableView, especially during scrolling)
- Custom window management (non-standard fullscreen, window subclassing, utility panels)
- Performance-critical UI requiring 0% CPU baseline
- Production apps where bugs equal revenue loss
- Professional tools (IDEs, DAWs, design apps, terminals)
- Rock-solid stability across OS versions

**The Hybrid Reality (Recommended for Production):**

Multi.app's proven strategy: AppKit for window/app lifecycle, SwiftUI for views where appropriate, bridging via NSHostingController and NSViewRepresentable.

<swiftui_limitations>
**Key SwiftUI Limitations (as of macOS 15):**
- TextField doesn't update bindings per-character (works on iOS)
- List performance: seconds to render vs instant on iOS for identical code
- Cannot fully customize menu bar like AppKit
- Window subclassing impossible in pure SwiftUI
- Limited responder chain access
- Memory: SwiftUI on macOS can have memory issues (developers have reported significant memory growth compared to iOS for similar apps)
</swiftui_limitations>

**Decision Pattern:**
```
Production Mac App
├── AppKit: NSApplication, NSWindow, NSWindowController, NSDocument
├── SwiftUI: View content where appropriate
└── Bridge: NSHostingController, NSViewRepresentable
```
</swiftui_vs_appkit_decision>

## Platform Differences from iOS (Critical for iOS Developers)

<platform_differences>

**Coordinate Systems:**
- iOS origin: top-left, Y increases downward
- macOS origin: bottom-left, Y increases upward (mathematical convention)
- Override `isFlipped` to return `true` for iOS-style coordinates
- Drawing images without compensating results in upside-down images

**Layer Backing:**
- iOS views are layer-backed by default
- macOS requires explicit `wantsLayer = true`
- Layer-backed views enable GPU compositing but cost memory
- Use for animations and effects, not for static content

**Windows vs Views:**
- macOS users expect multiple windows, resizing, minimize/maximize
- NSWindow is critical—not a passive container like UIWindow
- Window management patterns (tabs, fullscreen, spaces) are first-class
- Custom window behaviors require AppKit (SwiftUI limitations)

**Text System:**
- NSTextView/TextKit vastly more powerful than UITextView
- Rulers, find/replace, grammar checking built-in
- TextKit 2 (macOS 13+) has production stability issues as of 2024
- Force TextKit 1 with `let _ = textView.layoutManager`

**Background Colors:**
- Many NSView subclasses use `drawsBackground` property
- Not universal `backgroundColor` like iOS
- Check class documentation for correct property

**Mouse vs Touch:**
- Must implement `updateTrackingAreas()` for hover effects
- Right-click context menus are standard expectation
- Mouse tracking differs from touch gesture handling
- `NSEvent` provides precise cursor position and modifier keys
</platform_differences>

## Window Management Mastery

<window_management>

**NSWindow Lifecycle (macOS 10.13+ Change):**

Pre-10.13 behavior required `releasedWhenClosed = NO` to prevent over-release crashes.

macOS 10.13+ SDK: NSWindows that are ordered-in are strongly referenced by AppKit until explicitly ordered-out or closed. Uses `CFExecutableLinkedOnOrAfter` check—deployment target 10.12 or lower cannot rely on new behavior even on 10.13+.

**Window Style and Collection Behavior:**

Style masks combine but have limitations:
- Borderless windows can't become key by default (workaround: subclass, override `canBecomeKey` → true)
- Style changes during fullscreen are unreliable
- Full-size content view opts into layer-backing automatically

Collection behavior controls Spaces/Exposé/fullscreen:
- `.canJoinAllSpaces`: Visible on all spaces (like menu bar)
- `.moveToActiveSpace`: Follows when space changes
- `.fullScreenPrimary`: Can be fullscreen window
- `.fullScreenAuxiliary`: Shown with fullscreen window
- `.stationary`: Unaffected by Exposé, visible on desktop

**Pattern for always-visible overlay:**
```swift
window.collectionBehavior = [.canJoinAllSpaces, .stationary]
```

**Multi-Window Document Architecture:**
```
NSDocumentController (singleton)
    ↓ manages
NSDocument instances (one per document)
    ↓ manages
NSWindowController instances (one per window)
```

**Modern Document Best Practice:**
```swift
override class var autosavesInPlace: Bool { true }
```

Enables automatic version browsing, asynchronous saving, system-managed version storage.
</window_management>

## Responder Chain and Menu Validation

<responder_chain>

**The Complete Action Message Responder Chain:**

1. Start with firstResponder in key window
2. Try every nextResponder in chain
3. Try key window's delegate
4. Try same for main window (if different from key)
5. NSApplication tries to respond
6. NSApplication.delegate is tried last

**Critical Insight:** App delegate is NOT part of nextResponder chain—you can never reach it through iteration. It's used as a fallback when current key window's responder chain returns nil.

**NSViewController Integration (Yosemite 10.10+):**

Pre-10.10: NSViewControllers were NOT in responder chain by default—had to manually patch nextResponder.

Yosemite+: Automatically wires view controllers right after their view, but ONLY if the view controller is added as a child view controller to a parent controller.

**Menu Validation Performance:**

NSMenu updates EVERY menu item on EVERY user event (mouse move, keypress). This is a performance killer for large menus.

How it works:
1. Determine item's target (explicit or via responder chain)
2. Check if target implements action method (if not, disable)
3. If target implements `validateMenuItem:` or `validateUserInterfaceItem:`, call it and use return value

**Optimization:**
- Disable auto-validation for static menus: `menu.autoenablesItems = false`
- Manually control `menuItem.isEnabled`
- Target must be set for validation to be called
</responder_chain>

## SwiftUI Integration with AppKit

<swiftui_appkit_integration>

**NSHostingController (Essential Bridge Pattern):**
```swift
// Embedding SwiftUI in AppKit
let swiftUIView = MySwiftUIView()
let hostingController = NSHostingController(rootView: swiftUIView)

// macOS 13+ sizing control
hostingController.sizingOptions = [.intrinsicContentSize]
```

**NSViewRepresentable (Critical Pattern):**

The golden rule: ONLY update NSView properties when they've changed. Otherwise you create infinite loops.

```swift
struct TextViewRepresentable: NSViewRepresentable {
    @Binding var text: String

    func updateNSView(_ nsView: NSTextView, context: Context) {
        // CRITICAL: Check before setting
        if nsView.string != text {
            nsView.string = text
        }
    }
}
```

**State Management with @Observable (macOS 14+):**

Critical gotcha: @State with @Observable calls init() on EVERY view rebuild.

Solution: Declare in App struct:
```swift
@main
struct MyApp: App {
    @State private var appModel = AppModel() // Declare here
    var body: some Scene {
        WindowGroup {
            ContentView().environment(appModel)
        }
    }
}
```

**Multi-Window Management:**
```swift
// WindowGroup - Multiple instances
WindowGroup { ContentView() }

// Window - Single unique instance
Window("Stats", id: "stats") { StatsView() }

// UtilityWindow (macOS 14+) - Floating palette
UtilityWindow("Palette", id: "palette") { PaletteView() }
    .keyboardShortcut("u")
```

**Menu Bar & Commands:**
```swift
.commands {
    CommandMenu("Custom") {
        Button("Action") {}
            .keyboardShortcut("x", modifiers: [.command, .shift])
    }
}

// Focus values for multi-window menus
@FocusedValue(\.messageState) var messageState
```
</swiftui_appkit_integration>

## Sandboxing and File System Access

<sandboxing>

**Sandboxing Strategy:**
- Mac App Store: REQUIRED
- Direct Distribution: OPTIONAL but strongly recommended

**Access Methods:**
1. **User Selection** (NSOpenPanel/NSSavePanel): Immediate access
2. **Security-Scoped Bookmarks:** Persistent access across launches
3. **Container Access:** Automatic for `~/Library/Containers/<bundle-id>`

**Security-Scoped Bookmarks (Critical Pattern):**
```swift
// Save bookmark
let bookmarkData = try url.bookmarkData(options: .withSecurityScope)

// Restore and use
let url = try URL(resolvingBookmarkData: bookmarkData, options: .withSecurityScope)
guard url.startAccessingSecurityScopedResource() else { throw error }
defer { url.stopAccessingSecurityScopedResource() }
// Access file
```

**Critical Rules:**
- Call `startAccessingSecurityScopedResource()` on resolved URL, not original
- Don't call for NSOpenPanel URLs (temporary access granted)
- Always pair start/stop calls—NOT nested
- Leaking access consumes kernel resources, requiring app relaunch

**Entitlements to Know:**
- `com.apple.security.app-sandbox`: Enable App Sandbox
- `com.apple.security.files.user-selected.read-write`: User-selected files
- `com.apple.security.files.bookmarks.app-scope`: App-scoped bookmarks
- `com.apple.security.network.client`: Outgoing network connections
- `com.apple.security.network.server`: Incoming network connections
</sandboxing>

## Code Signing and Notarization

<code_signing>

**Current Process (2024-2025):**

1. **Code Sign:**
```bash
codesign --deep --force --options runtime \
  --entitlements App.entitlements \
  --sign "Developer ID Application: Your Name (TEAMID)" \
  App.app

codesign --verify --verbose App.app
```

2. **Create Archive:**
```bash
ditto -c -k --keepParent App.app App.zip
```

3. **Submit for Notarization:**
```bash
xcrun notarytool submit App.zip \
  --apple-id "your@email.com" \
  --team-id "TEAMID" \
  --password "@keychain:AC_PASSWORD" \
  --wait
```

4. **Staple Ticket:**
```bash
xcrun stapler staple App.app
xcrun stapler validate App.app
```

**Critical Changes:**
- macOS Sequoia: Even stricter Gatekeeper enforcement
- **notarytool** replaced legacy **altool**
- Sign bottom-up in bundle hierarchy (frameworks first, then app)
- **Never use --deep**—sign each component individually

**Common Failures:**
- "Hardened runtime not enabled" → Add `--options runtime`
- "Invalid signature" → Re-sign with proper entitlements
</code_signing>

## Architecture Patterns

<architecture_patterns>
**For general architecture philosophy, see the `software-engineer` skill.** This section covers macOS-specific architectural considerations.

**Primary Patterns (Choose One):**

### MVC (Model-View-Controller)

**What it is:**
- Apple's classic pattern for AppKit development
- Model: Data and business logic
- View: UI components
- Controller: Coordinates between Model and View

**When to use:**
- AppKit-heavy applications
- Document-based apps (works naturally with NSDocument)
- Simple-to-medium complexity apps
- When following Apple's conventions makes sense

**Reality check:**
- Controllers tend to become large ("Massive View Controller")
- This is fine for many apps—just watch for controller bloat
- When controllers exceed ~300-400 lines, consider extracting logic

### MV (Model-View)

**What it is:**
- Apple's recommended pattern for simple SwiftUI apps
- Model: Data and business logic
- View: SwiftUI views with @State for local state
- No separate ViewModel layer - views call model methods directly

**When to use:**
- Simple-to-medium SwiftUI applications
- Prototypes and MVPs
- Apps without complex testability requirements
- When MVVM feels like overkill

**Reality check:**
- SwiftUI's reactive binding means views often serve as their own view models[^mv-pattern]
- Minimal boilerplate, fastest development velocity
- Works for most SwiftUI apps until models exceed ~500 lines
- When models get large, extract logic or move to MVVM

**Pattern:**
```swift
@Observable
class User {
    var name: String = ""
    var email: String = ""

    func save() {
        // Business logic here
    }
}

struct ProfileView: View {
    @State private var user = User()

    var body: some View {
        Form {
            TextField("Name", text: $user.name)
            Button("Save") { user.save() }
        }
    }
}
```

### MVVM (Model-View-ViewModel)

**What it is:**
- Model: Data and business logic
- View: SwiftUI views or AppKit views
- ViewModel: Presentation logic, formats data for View

**When to use:**
- SwiftUI applications needing testable presentation logic
- Multiple views display same data differently
- Need to separate view logic from view definition
- Models have grown too large in MV pattern

**Reality check:**
- Works beautifully with SwiftUI's reactive nature
- Less natural in pure AppKit (but still usable)
- ViewModels can also bloat—same solution as MVC (extract logic)
- Consider if you actually need it vs simpler MV pattern

### VIPER (View-Interactor-Presenter-Entity-Router)

**What it is:**
- Ultra-granular pattern splitting each screen into 5+ components
- View: Displays data
- Interactor: Business logic
- Presenter: Formats data for view
- Entity: Data models
- Router: Navigation

**When to use:**
- Rarely. Honest assessment: generally over-engineered
- Large enterprise apps with extreme testability requirements
- Teams that need architectural enforcement of separation
- **AppKit only** - actively fights SwiftUI's design

**Reality check:**
- Massive boilerplate (5+ files per screen)
- Most sources say "only if you really need it"
- **In SwiftUI:** Presenter layer redundant (auto-updates), Router obsolete (state-driven navigation)
- **Don't force this pattern into SwiftUI** - you'll fight the framework constantly
- Consider carefully whether the complexity is justified even in AppKit

**Complementary Pattern (Add When Needed):**

### Coordinator Pattern

**What it is:**
- Handles navigation and screen flow
- Works **on top of** MVC or MVVM (not instead of)
- Removes navigation logic from view controllers/view models
- Common combinations: MVVM-C, MVC-C
- **Primarily an AppKit/UIKit pattern**

**When to add Coordinator:**
- Complex navigation in AppKit apps (10+ screens)
- Deep linking (URLs open specific screens)
- Multiple entry points to same screen
- A/B testing different user flows
- Reusing view controllers in different contexts

**SwiftUI Reality:**
- **Don't force Coordinators into SwiftUI** - navigation is declarative and state-driven
- SwiftUI uses NavigationStack, NavigationPath, @State, .sheet(), .fullScreenCover()
- SwiftUI's view hierarchy is static at compile-time, not dynamically modifiable
- Use SwiftUI's built-in navigation patterns instead

**Pattern (AppKit/UIKit):**
```
App uses MVC or MVVM for view/logic organization
     +
Coordinator manages navigation between screens
```

**Other Concerns:**

Patterns like Repository (data access), networking layers, and business logic extraction emerge on a case-by-case basis during actual project design. Don't prematurely abstract.
</architecture_patterns>

## Performance Optimization

<performance>

**Profiling with Instruments:**

Essential templates:
- **Time Profiler:** CPU usage, call stacks, bottlenecks (use for 80% of profiling)
- **Allocations:** Memory allocation patterns
- **Leaks:** Memory leak detection
- **Metal System Trace:** GPU performance

Best practices:
- Profile in Release mode (optimization critical)
- Profile on target hardware (older devices reveal issues)
- Use Signposts for precise measurement intervals

**Main Thread Optimization:**

Main thread for UI updates and user input handling ONLY. Move off main thread:
- Network requests
- Data parsing
- File I/O
- Complex calculations
- Image processing

**Layer-Backed View Optimization:**

Layer-backed views have default redraw policy `NSViewLayerContentsRedrawDuringViewResize` which is "detrimental to animation performance" as it triggers the drawing step for each frame.[^layer-redraw]

Change to:
```swift
view.layerContentsRedrawPolicy = .onSetNeedsDisplay
```

**When to Enable Layer-Backing:**
- Animating multiple views simultaneously
- Need smooth 60fps animations
- Want Core Animation features
- Creating effects requiring GPU acceleration

**Avoid Layer-Backing When:**
- Simple static UI with no animations
- Memory extremely constrained (each layer has own backing store)
- Need precise pixel-level drawing control
</performance>

## Testing Strategy

<testing>
**For general testing philosophy and TDD principles, see the `test-driven-development` skill.**

**Swift Testing vs XCTest (2024-2025):**

Swift Testing (Xcode 16+):
- Modern replacement using macros (`@Test`, `#expect`, `#require`)
- Better parallelization (in-process using Swift Concurrency)
- Works with structs/actors/classes, not just XCTestCase
- Use for: New unit tests in Swift 6/Xcode 16+ projects

XCTest:
- Required for UI automation (XCUIApplication)
- Required for performance tests (XCTMetric)
- Necessary for Objective-C codebases
- Use for: UI automation tests, performance tests, existing test suites

**Recommended Distribution:**
1. **Unit Tests (70%):** View models, business logic, data models
2. **Integration Tests (20%):** Component interactions, API clients
3. **UI Tests (10%):** Critical user flows using XCTest

**Accessibility Testing:**

VoiceOver on macOS differs from iOS:
- Keyboard navigation primary (not touch)
- VoiceOver Utility for configuration
- Menu bar accessibility critical
- Multiple windows/spaces support

Testing workflow:
- Start VoiceOver: ⌘ + F5
- Navigate with Control + Option (VO keys)
- Verify all interactive elements accessible
- Test with Safari (best VoiceOver support)
</testing>

## Common Anti-Patterns

<anti_patterns>

### iOS Patterns Applied Incorrectly
- Assuming layer-backing is automatic
- Using UIKit coordinate conventions without override
- Treating NSWindow like UIWindow (passive container)
- Ignoring window management patterns
- Not implementing hover states (mouse tracking)
- Missing right-click context menus

### Web Developer Mistakes
- Expecting CSS-like layout flexibility (use Auto Layout constraints)
- Fighting native controls instead of embracing system appearance
- Ignoring accessibility (VoiceOver is expected, not optional)
- Single-window mentality (macOS users expect multi-window support)
- Not using native file dialogs (NSOpenPanel/NSSavePanel)
- Ignoring keyboard shortcuts and menu bar conventions

### Linux/Cross-Platform Developer Mistakes
- Assuming POSIX conventions apply to GUI (Cocoa is not GTK/Qt)
- Fighting sandboxing instead of designing around it
- Ignoring Apple's signing/notarization requirements
- Using raw file paths instead of security-scoped bookmarks
- Not adapting to macOS HIG (menu bar, dock, system preferences)

### Windows Developer Mistakes
- Expecting registry-like global preferences (use UserDefaults, sandboxed)
- Assuming all file access is available (sandbox constraints)
- Window chrome expectations (macOS uses unified toolbars, not separate title bars)
- Installation expectations (drag-to-Applications, no installer wizards)

**Over-Engineering Simple Apps:**
- Using VIPER for simple CRUD apps
- Complex architectural patterns for prototypes
- Custom state management when @EnvironmentObject suffices
- Premature abstraction before requirements are clear

**Ignoring macOS UI Conventions:**
- Not following macOS Human Interface Guidelines
- Poor keyboard shortcut support
- Ignoring standard menu bar conventions
- Misusing window management (minimize, zoom, full screen)
- Not respecting macOS-specific UI elements (toolbars, sidebars, split views)

### Premature SwiftUI Adoption
- Attempting 100% SwiftUI for complex Mac apps
- Ignoring AppKit when SwiftUI is insufficient
- Not budgeting for 20-30% AppKit fallback code
- Assuming iOS SwiftUI code will work on macOS
</anti_patterns>

## Mac App Store vs Direct Distribution

<distribution>

**Mac App Store:**
- **Pros:** Apple handles distribution/updates, user trust, search visibility
- **Cons:** REQUIRED full sandboxing, 30% commission, review delays, limited APIs

**Direct Distribution:**
- **Pros:** Greater API access, no commission, faster updates, custom pricing
- **Cons:** Must handle payments, notarization required, no built-in discoverability

**Recommendation:** Professional tools choose direct distribution for flexibility; consumer apps often choose MAS for trust and distribution.
</distribution>

## Decision Frameworks Summary

<decision_summary>

**SwiftUI vs AppKit:**
- Simple-medium apps targeting macOS 14+: SwiftUI
- Complex text editing, large datasets, custom windows: AppKit
- Production apps where bugs = revenue loss: AppKit
- Professional tools: Hybrid (AppKit foundation, SwiftUI where appropriate)

**Architecture Pattern:**
- AppKit apps: MVC
- Simple SwiftUI apps: MV (Model-View)
- SwiftUI apps needing testability: MVVM
- Complex AppKit navigation (10+ screens, deep linking): Add Coordinator (don't use in SwiftUI)
- Rarely: VIPER for AppKit only (if you genuinely need extreme architectural enforcement)

**State Management:**
- View-local: @State
- Simple global (1-2 objects): @EnvironmentObject
- Medium-to-complex apps: @Observable singleton or multiple @Observable types

**Cross-Platform:**
- Similar features, 70%+ overlap: SwiftUI multiplatform
- Premium Mac experience: Separate codebases with shared business logic
- Complex apps: Hybrid (shared Swift Package for logic, platform UIs)
</decision_summary>

## Resources

<resources>

**Local Documentation:**
- Xcode diagnostic docs: `/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/share/doc/swift/diagnostics/`
- LLM-optimized guides: `/Applications/Xcode.app/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources/AdditionalDocumentation/`

**Apple Official:**
- AppKit Documentation: https://developer.apple.com/documentation/appkit
- macOS HIG: https://developer.apple.com/design/human-interface-guidelines/macos
- SwiftUI Documentation: https://developer.apple.com/documentation/swiftui

**Expert Blogs:**
- NSHipster: https://nshipster.com (Overlooked Cocoa/Swift bits)
- objc.io: https://www.objc.io (Advanced techniques, essential "AppKit for UIKit Developers" article)
- Mike Ash Friday Q&A: https://www.mikeash.com/pyblog/ (Deep low-level technical articles)
- Brent Simmons Inessential: https://inessential.com (Veteran Mac developer, NetNewsWire author)
- Use Your Loaf: https://useyourloaf.com (Practical guides, WWDC viewing guides)

**Books:**
- "macOS by Tutorials" (v3.0) by TrozWare - Updated for macOS 15 & Xcode 16
- "Hacking with macOS" by Paul Hudson - 18 projects, free online
- "The Complete Friday Q&A" (Volumes I-III) by Mike Ash - Essential for Cocoa internals

**Open Source Examples:**
- Awesome Open Source Mac Apps: https://github.com/serhii-londar/open-source-mac-os-apps
- NetNewsWire: https://github.com/brentsimmons (Mature AppKit codebase)
- WWDC app (unofficial): https://github.com/insidegui/WWDC (Well-structured Mac app)

**Community:**
- Apple Developer Forums: https://developer.apple.com/forums/
- Stack Overflow (cocoa/appkit tags)
</resources>

## The Modern macOS Developer's Mindset

**Embrace Hybrid Solutions:** The best Mac apps in 2025 blend SwiftUI and AppKit strategically. Use each framework where it excels. Don't force SwiftUI where AppKit is superior.

**Leverage Platform Strengths:** macOS isn't iOS with a bigger screen. Multiple windows, menu bars, keyboard navigation, document architecture—these are first-class citizens. iOS developers transitioning to Mac: unlearn iOS assumptions.

**Test Relentlessly:** Swift Testing for unit tests, XCTest for UI automation. 70% unit, 20% integration, 10% UI. Profile with Instruments regularly. VoiceOver test every release.

**Stay Pragmatic:** The perfect architecture that ships beats the theoretical ideal that doesn't. Balance theoretical purity with practical delivery. Ship working software, iterate based on real problems, refactor when justified by pain.

**Final Wisdom:** The best Mac apps feel like Mac apps. They embrace platform conventions, leverage macOS strengths, and don't feel like iPad apps in disguise. Build for Mac users, not iOS users with keyboards. Master the frameworks, respect the platform, ship great software.

## Sources

<sources>
[^ghostty-devlog]: Mitchell Hashimoto. 2024. Ghostty Devlog 002. https://mitchellh.com/writing/ghostty-devlog-002

[^multi-swiftui]: Multi.app. 2023. Moving to SwiftUI from macOS Cocoa. https://multi.app/blog/moving-to-swiftui-from-macos-cocoa-or-ios-cocoa-touch

[^mv-pattern]: Mohammad Azam. 2022. SwiftUI Architecture — A Complete Guide to the MV Pattern Approach. https://betterprogramming.pub/swiftui-architecture-a-complete-guide-to-mv-pattern-approach-5f411eaaaf9e

[^layer-redraw]: objc.io. AppKit for UIKit Developers. Issue #14. https://www.objc.io/issues/14-mac/appkit-for-uikit-developers
</sources>
