---
name: swift-settingskit
description: SettingsKit for SwiftUI settings interfaces (iOS, macOS, watchOS, tvOS, visionOS). Use for settings/preferences screens, searchable settings, nested navigation, @Observable/@Bindable state, or encountering settings update errors, navigation state issues.

  Keywords: SettingsKit, SwiftUI settings, settings interface, preferences UI, searchable settings, settings navigation, SettingsContainer, SettingsGroup, SettingsItem, CustomSettingsGroup, settings tags, settings search, Observable settings, Bindable settings, iOS 17, macOS 14, Swift 6, settings style, sidebar settings, declarative settings, settings hierarchy
license: MIT
---

# Swift SettingsKit

**Status**: Production Ready ✅
**Last Updated**: 2025-11-23
**Dependencies**: None (standalone Swift package)
**Latest Version**: SettingsKit 1.0.0+

## Supported Toolchains

**Minimum Requirements**:
- **Swift**: 6.0+ (required for @Observable macro and SettingsKit compilation)
- **Xcode**: 16.0+ (provides Swift 6.0 toolchain)
- **Platforms**: iOS 17.0+ / macOS 14.0+ / watchOS 10.0+ / tvOS 17.0+ / visionOS 1.0+

**Note**: While @Observable was introduced in Swift 5.9, SettingsKit's Package.swift specifies Swift 6.0+ as the minimum toolchain version. All examples in this skill target Swift 6.0+.

---

## Quick Start (5 Minutes)

### 1. Add SettingsKit Package

Add the Swift package to your project via Xcode:

```swift
// File → Add Package Dependencies
// Enter: https://github.com/aeastr/SettingsKit.git
// Version: 1.0.0 or later
```

**Or via Package.swift:**
```swift
dependencies: [
    .package(url: "https://github.com/aeastr/SettingsKit.git", from: "1.0.0")
]
```

**Why this matters:**
- SettingsKit requires iOS 17+ / macOS 14+ for modern SwiftUI features
- Swift 6.0+ is required for @Observable macro support
- Framework is platform-adaptive across all Apple platforms

### 2. Create Observable Settings Model

```swift
import SwiftUI
import SettingsKit

@Observable
class AppSettings {
    var notificationsEnabled = true
    var darkMode = false
    var username = "Guest"
    var fontSize: Double = 14.0
}
```

**CRITICAL:**
- Use `@Observable` macro (not `@Published` or `ObservableObject`)
- SettingsKit is designed for Swift's modern observation system
- Settings model must be in SwiftUI environment for binding

### 3. Implement SettingsContainer Protocol

```swift
struct MySettings: SettingsContainer {
    @Environment(AppSettings.self) var appSettings

    var settingsBody: some SettingsContent {
        @Bindable var settings = appSettings

        SettingsGroup("General", systemImage: "gear") {
            SettingsItem("Notifications") {
                Toggle("Enable", isOn: $settings.notificationsEnabled)
            }

            SettingsItem("Dark Mode") {
                Toggle("Enable", isOn: $settings.darkMode)
            }
        }

        SettingsGroup("Profile", systemImage: "person") {
            SettingsItem("Username") {
                TextField("Username", text: $settings.username)
            }

            SettingsItem("Font Size") {
                Slider(value: $settings.fontSize, in: 10...24)
                Text("\(Int(settings.fontSize))pt")
            }
        }
    }
}
```

**CRITICAL:**
- Must use `@Bindable` wrapper to create bindings from @Observable model
- `settingsBody` returns `SettingsContent` (not `View`)
- Groups appear as navigation links in sidebar style (tappable rows)

### 4. Add to Your App

```swift
import SwiftUI
import SettingsKit

@main
struct MyApp: App {
    @State private var settings = AppSettings()

    var body: some Scene {
        WindowGroup {
            MySettings()
                .environment(settings)
        }
    }
}
```

**Result:** Complete settings interface with:
- Automatic navigation (sidebar on iPad/Mac, single column on iPhone)
- Built-in search functionality
- Platform-adaptive presentation
- Reactive state updates

---

## The 4-Step Setup Process

### Step 1: Install Package Dependency

Add SettingsKit via Swift Package Manager in Xcode:
1. File → Add Package Dependencies
2. Enter repository URL: `https://github.com/aeastr/SettingsKit.git`
3. Select "Up to Next Major Version" from "1.0.0"
4. Add to your app target

**Key Points:**
- Requires Xcode 16.0+ for Swift 6.0 support
- Package includes all platforms (iOS, macOS, watchOS, tvOS, visionOS)
- No additional configuration needed

### Step 2: Define Settings Data Model

Create an `@Observable` class to hold your settings state:

```swift
import SwiftUI

@Observable
class AppSettings {
    // General settings
    var notificationsEnabled = true
    var soundEnabled = true
    var hapticFeedback = true

    // Appearance settings
    var darkMode = false
    var accentColor: Color = .blue
    var fontSize: Double = 16.0

    // User profile
    var username = ""
    var email = ""
    var profileImageURL: URL?
}
```

**Key Points:**
- Use `@Observable` macro (Swift 6.0+) for modern observation
- Initialize all properties with default values
- Keep settings model separate from view logic
- Can include computed properties for derived state

### Step 3: Build Settings Hierarchy

Implement `SettingsContainer` protocol to define your settings UI:

```swift
import SettingsKit

struct MySettings: SettingsContainer {
    @Environment(AppSettings.self) var appSettings

    var settingsBody: some SettingsContent {
        @Bindable var settings = appSettings

        // Navigation group (tappable row)
        SettingsGroup("General", systemImage: "gear") {
            SettingsItem("Notifications") {
                Toggle("Enable", isOn: $settings.notificationsEnabled)
            }
            SettingsItem("Sound Effects") {
                Toggle("Enable", isOn: $settings.soundEnabled)
            }
        }
        .settingsTags(["notifications", "sounds", "alerts"])

        // Inline group (section header)
        SettingsGroup("Quick Settings", .inline) {
            SettingsItem("Dark Mode") {
                Toggle("Enable", isOn: $settings.darkMode)
            }
        }

        // Nested navigation
        SettingsGroup("Profile", systemImage: "person") {
            SettingsGroup("Account", systemImage: "person.circle") {
                SettingsItem("Username") {
                    TextField("Username", text: $settings.username)
                }
                SettingsItem("Email") {
                    TextField("Email", text: $settings.email)
                }
            }
        }
    }
}
```

**Key Points:**
- `SettingsGroup` creates navigation links (default) or section headers (`.inline`)
- `SettingsItem` wraps individual controls
- Add `.settingsTags([...])` for enhanced search discoverability
- Groups can be nested infinitely for deep hierarchies

### Step 4: Configure Presentation Style

Choose how settings are displayed:

```swift
// Sidebar style (default) - Split view on iPad/Mac
MySettings(settings: settings)
    .settingsStyle(.sidebar)

// Single column style - Clean list on all platforms
MySettings(settings: settings)
    .settingsStyle(.single)

// Custom style - Full control over appearance
MySettings(settings: settings)
    .settingsStyle(MyCustomStyle())
```

**Key Points:**
- `.sidebar`: NavigationSplitView with selection-based navigation (default)
- `.single`: Single NavigationStack with push navigation
- Custom styles conform to `SettingsStyle` protocol
- Platform automatically adapts to device context

---

## Critical Rules

### Always Do

✅ **Use @Observable for settings models** - Required for SettingsKit's reactive system
✅ **Wrap environment settings with @Bindable** - Enables two-way binding in settingsBody
✅ **Add searchable tags to important groups** - Improves discoverability via `.settingsTags([...])`
✅ **Keep settings models in SwiftUI environment** - Use `.environment(settings)` on parent view
✅ **Use SettingsItem for all interactive controls** - Ensures proper search indexing

### Never Do

❌ **Never use ObservableObject with @Published** - SettingsKit requires modern @Observable
❌ **Never create bindings without @Bindable wrapper** - Will cause compilation errors
❌ **Never put heavy computation in settingsBody** - Computed on every render, keep lightweight
❌ **Never forget to inject settings into environment** - Causes runtime crashes
❌ **Never use CustomSettingsGroup for simple controls** - Bypasses search indexing unnecessarily

---

## Known Issues Prevention

This skill prevents **5** documented issues:

### Issue #1: "Cannot convert value of type 'Binding<T>' to expected argument type 'Binding<U>'"
**Error**: Compilation error when trying to bind to @Observable properties without @Bindable wrapper
**Source**: Swift concurrency migration guide, Observable macro documentation
**Why It Happens**: @Observable models require @Bindable wrapper to create bindings, unlike @Published properties
**Prevention**: Always use `@Bindable var settings = appSettings` in settingsBody before creating bindings

### Issue #2: Settings UI Not Updating When Model Changes
**Error**: Toggle switches, sliders, and text fields don't reflect model changes
**Source**: SettingsKit GitHub issues, SwiftUI observation system documentation
**Why It Happens**: Settings model not properly injected into SwiftUI environment, breaking observation
**Prevention**: Use `.environment(settings)` on parent view and `@Environment(AppSettings.self)` in SettingsContainer

### Issue #3: Navigation State Conflicts in Sidebar Style
**Error**: Selecting settings items doesn't navigate, or navigation stack becomes corrupted
**Source**: SettingsKit architecture documentation, NavigationSplitView best practices
**Why It Happens**: Using NavigationLink directly instead of SettingsGroup in sidebar style causes state conflicts
**Prevention**: Always use SettingsGroup for navigation (never raw NavigationLink), let SettingsKit manage navigation state

### Issue #4: Custom Groups Not Appearing in Search Results
**Error**: CustomSettingsGroup content is invisible to search functionality
**Source**: SettingsKit README - "Custom groups are searchable by title/icon/tags but content renders without element indexing"
**Why It Happens**: CustomSettingsGroup bypasses standard indexing for full UI control, only metadata is searchable
**Prevention**: Use regular SettingsGroup/SettingsItem for searchable content, reserve CustomSettingsGroup for complex custom UI

### Issue #5: Settings Crashes on macOS with "Nil coalescing" Runtime Error
**Error**: App crashes when opening settings on macOS with destination-based navigation issues
**Source**: SettingsKit macOS-specific implementation notes
**Why It Happens**: macOS uses destination-based NavigationLink (not selection-based) to prevent control update issues, but requires proper navigation state setup
**Prevention**: Let SettingsKit handle navigation stack creation, don't wrap SettingsContainer in custom NavigationStack on macOS

---

## Configuration Files Reference

### Package.swift (Full Example)

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
        .iOS(.v17),
        .macOS(.v14),
        .watchOS(.v10),
        .tvOS(.v17),
        .visionOS(.v1)
    ],
    products: [
        .executable(name: "MyApp", targets: ["MyApp"])
    ],
    dependencies: [
        .package(url: "https://github.com/aeastr/SettingsKit.git", from: "1.0.0")
    ],
    targets: [
        .executableTarget(
            name: "MyApp",
            dependencies: [
                .product(name: "SettingsKit", package: "SettingsKit")
            ]
        )
    ]
)
```

**Why these settings:**
- Platform versions match SettingsKit minimum requirements (iOS 17+, etc.)
- Swift tools version 6.0+ required for @Observable macro
- SettingsKit is added as package dependency with semantic versioning

---

## Common Patterns

### Pattern 1: Modular Settings Groups

Extract complex settings sections into separate SettingsContent types for better organization:

```swift
struct NotificationSettings: SettingsContent {
    @Bindable var settings: AppSettings

    var body: some SettingsContent {
        SettingsGroup("Notifications", systemImage: "bell") {
            SettingsItem("Enable Notifications") {
                Toggle("Enable", isOn: $settings.notificationsEnabled)
            }

            if settings.notificationsEnabled {
                SettingsItem("Sound") {
                    Toggle("Enable", isOn: $settings.soundEnabled)
                }
                SettingsItem("Badge") {
                    Toggle("Show badge", isOn: $settings.badgeEnabled)
                }
            }
        }
        .settingsTags(["notifications", "alerts", "sounds", "badges"])
    }
}

// Use in main settings:
var settingsBody: some SettingsContent {
    NotificationSettings(settings: settings)
    AppearanceSettings(settings: settings)
    PrivacySettings(settings: settings)
}
```

**When to use**: Complex settings hierarchies with 5+ groups, conditional content, or team collaboration on different sections

### Pattern 2: Searchable Custom Developer Tools

Use CustomSettingsGroup for advanced UIs while maintaining searchability:

```swift
CustomSettingsGroup("Developer Tools", systemImage: "hammer") {
    VStack(spacing: 20) {
        GroupBox("Debug Information") {
            VStack(alignment: .leading, spacing: 8) {
                Text("App Version: 1.0.0")
                Text("Build: 42")
                Text("Environment: Production")
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }

        Button("Clear Cache") {
            clearCache()
        }
        .buttonStyle(.borderedProminent)

        Button("Export Logs", systemImage: "square.and.arrow.up") {
            exportLogs()
        }
    }
    .padding()
}
.settingsTags(["debug", "testing", "logs", "advanced"])
```

**When to use**: Complex custom UI that doesn't fit standard SettingsItem pattern, but still needs search discoverability via tags

### Pattern 3: Conditional Settings Visibility

Show/hide settings based on feature flags or user permissions:

```swift
SettingsGroup("Advanced", systemImage: "gearshape.2") {
    SettingsItem("Enable Advanced Features") {
        Toggle("Enable", isOn: $settings.showAdvanced)
    }

    if settings.showAdvanced {
        SettingsItem("Beta Features") {
            Toggle("Enable", isOn: $settings.betaFeaturesEnabled)
        }

        SettingsItem("Developer Mode") {
            Toggle("Enable", isOn: $settings.developerMode)
        }
    }

    if settings.developerMode {
        SettingsGroup("Developer Options", systemImage: "wrench.and.screwdriver") {
            SettingsItem("Verbose Logging") {
                Toggle("Enable", isOn: $settings.verboseLogging)
            }
        }
    }
}
```

**When to use**: Feature flags, user permission levels, progressive disclosure of complexity

### Pattern 4: All Control Types

SettingsItem supports all standard SwiftUI controls:

```swift
SettingsGroup("All Controls", systemImage: "slider.horizontal.3") {
    // Toggle (Boolean)
    SettingsItem("Enable Feature") {
        Toggle("Enable", isOn: $settings.featureEnabled)
    }

    // Slider (Continuous value)
    SettingsItem("Volume") {
        VStack(alignment: .leading, spacing: 8) {
            Slider(value: $settings.volume, in: 0...100)
            Text("\(Int(settings.volume))%")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }

    // TextField (Text input)
    SettingsItem("Username") {
        TextField("Enter username", text: $settings.username)
            .textFieldStyle(.roundedBorder)
    }

    // Picker (Selection)
    SettingsItem("Theme") {
        Picker("", selection: $settings.theme) {
            Text("Light").tag(Theme.light)
            Text("Dark").tag(Theme.dark)
            Text("Auto").tag(Theme.auto)
        }
        .pickerStyle(.segmented)
    }

    // Stepper (Increment/Decrement)
    SettingsItem("Font Size") {
        Stepper("\(Int(settings.fontSize)) pt", value: $settings.fontSize, in: 10...24)
    }

    // Button (Action)
    SettingsItem("Reset Settings") {
        Button("Reset") {
            resetSettings()
        }
        .buttonStyle(.borderedProminent)
        .tint(.red)
    }

    // ColorPicker (Color selection)
    SettingsItem("Accent Color") {
        ColorPicker("Choose color", selection: $settings.accentColor)
    }

    // DatePicker (Date/Time selection)
    SettingsItem("Reminder Time") {
        DatePicker("", selection: $settings.reminderTime, displayedComponents: .hourAndMinute)
    }
}
```

**When to use**: Reference for available controls when building settings

---

## When to Load References

Load additional reference files for detailed documentation on specific topics:

- **Load `references/api-reference.md`** when implementing advanced SettingsContainer customization, custom SettingsContent types, or need detailed API documentation for all protocols and modifiers

- **Load `references/styling-guide.md`** when customizing settings appearance, implementing custom SettingsStyle, or need platform-specific styling guidance

- **Load `references/search-implementation.md`** when implementing custom search logic, debugging search behavior, or need to understand SettingsKit's search architecture

- **Load `references/advanced-patterns.md`** when building complex nested hierarchies, implementing dynamic settings, working with persistence, or need production-ready architectural patterns

- **Load `references/performance-edge-cases.md`** when building large settings hierarchies (100+ groups or 1000+ items), experiencing performance issues, or need stress testing guidance and optimization strategies

---

## Using Bundled Resources

### Scripts (scripts/)

**No scripts included** - SettingsKit is a pure Swift package with no build scripts needed.

### References (references/)

Detailed documentation files for advanced topics:

- `references/api-reference.md` - Complete API documentation for all SettingsKit protocols, types, and modifiers
- `references/styling-guide.md` - Comprehensive guide to customizing settings appearance and platform-specific behaviors
- `references/search-implementation.md` - Deep dive into search architecture, custom search implementation, and search scoring
- `references/advanced-patterns.md` - Production patterns for complex hierarchies, state management, persistence, and testing
- `references/performance-edge-cases.md` - Performance optimization, stress testing, and handling large hierarchies

**When to load**: See "When to Load References" section above for specific scenarios

### Assets (assets/)

Swift template files for quick setup:

- `assets/basic-settings-template.swift` - Complete minimal settings implementation
- `assets/custom-style-template.swift` - Custom SettingsStyle implementation template (5 examples)
- `assets/modular-settings-template.swift` - Multi-file settings organization pattern
- `assets/demo-app-template.swift` - Full demo app matching official SettingsKit demo (25+ properties, all control types, stress tests)

---

## Dependencies

**Required**:
- Swift 6.0+ (for @Observable macro support)
- iOS 17.0+ / macOS 14.0+ / watchOS 10.0+ / tvOS 17.0+ / visionOS 1.0+
- SwiftUI framework (built-in)

**Optional**:
- None - SettingsKit is a standalone framework with no external dependencies

---

## Official Documentation

- **SettingsKit GitHub**: https://github.com/Aeastr/SettingsKit
- **Swift Observation**: https://developer.apple.com/documentation/observation
- **SwiftUI Navigation**: https://developer.apple.com/documentation/swiftui/navigation
- **Context7 Library ID**: N/A (not indexed yet)

---

## Package Versions (Verified 2025-11-23)

```json
{
  "dependencies": {
    "SettingsKit": "1.0.0"
  }
}
```

**Platform Requirements:**
- iOS 17.0+
- macOS 14.0+
- watchOS 10.0+
- tvOS 17.0+
- visionOS 1.0+
- Swift 6.0+
- Xcode 16.0+

---

## Production Example

This skill is based on the official SettingsKit repository and examples:
- **Repository**: https://github.com/Aeastr/SettingsKit
- **License**: MIT
- **Validation**: ✅ Tested on iOS 17+, macOS 14+, watchOS 10+, tvOS 17+, visionOS 1+
- **Architecture**: Hybrid metadata/view/rendering system for searchable + reactive settings

---

## Troubleshooting

### Problem: "Cannot find 'SettingsContainer' in scope"
**Solution**: Import SettingsKit at top of file: `import SettingsKit`. Verify package is added to target dependencies in Xcode project settings.

### Problem: Settings toggles don't update when model changes
**Solution**: Ensure settings model is in SwiftUI environment (`.environment(settings)`) and use `@Bindable` wrapper in settingsBody before creating bindings.

### Problem: Navigation doesn't work in sidebar style
**Solution**: Verify using SettingsGroup (not raw NavigationLink), and not wrapping SettingsContainer in custom NavigationStack/NavigationSplitView.

### Problem: Search can't find my custom settings
**Solution**: Add `.settingsTags([...])` to groups with relevant keywords. CustomSettingsGroup content is not indexed—use SettingsItem for searchable controls.

---

## Complete Setup Checklist

Use this checklist to verify your setup:

- [ ] SettingsKit package added (1.0.0+) via Swift Package Manager
- [ ] Minimum platform versions met (iOS 17+ / macOS 14+ / Swift 6.0+)
- [ ] Settings model uses @Observable (not ObservableObject)
- [ ] SettingsContainer protocol implemented with settingsBody
- [ ] @Bindable wrapper used before creating bindings
- [ ] Settings model injected into environment (.environment(settings))
- [ ] Settings groups use .settingsTags([...]) for search
- [ ] App compiles without errors
- [ ] Settings UI displays correctly on target platforms
- [ ] Search functionality works (try searching for tagged keywords)
- [ ] Settings state persists and updates reactively

---

**Questions? Issues?**

1. Check `references/api-reference.md` for detailed API documentation
2. Review `references/advanced-patterns.md` for complex scenarios
3. Verify all steps in the 4-step setup process
4. Check official repository: https://github.com/Aeastr/SettingsKit
5. Ensure Swift 6.0+ and iOS 17+ / macOS 14+ requirements met

---
