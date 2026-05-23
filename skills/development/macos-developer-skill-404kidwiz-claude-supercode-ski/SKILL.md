---
name: macos-developer
description: Expert in macOS app development using AppKit, SwiftUI for Mac, and XPC. Specializes in system extensions, menu bar apps, and deep OS integration.
---

# macOS Developer

## Purpose

Provides native macOS application development expertise specializing in AppKit, SwiftUI for Mac, and system integration. Builds native desktop applications with XPC services, menu bar apps, and deep OS capabilities for the Apple ecosystem.

## When to Use

- Building native macOS apps (DMG/App Store)
- Developing Menu Bar apps (NSStatusItem)
- Implementing XPC Services for privilege separation
- Creating System Extensions (Endpoint Security, Network Extension)
- Porting iPad apps to Mac (Catalyst)
- Automating Mac admin tasks (AppleScript/JXA)

---
---

## 2. Decision Framework

### UI Framework

| Framework | Best For | Pros | Cons |
|-----------|----------|------|------|
| **SwiftUI** | Modern Apps | Declarative, simple code. | Limited AppKit feature parity. |
| **AppKit** | System Tools | Full control (NSWindow, NSView). | Imperative, verbose. |
| **Catalyst** | iPad Ports | Free Mac app from iPad code. | Looks like an iPad app. |

### Distribution Channel

*   **Mac App Store:** Sandboxed, verified, easy updates. (Required for System Extensions).
*   **Direct Distribution (DMG):** Notarization required. More freedom (Accessibility API, Full Disk Access).

### Process Architecture

*   **Monolith:** Simple apps.
*   **XPC Service:** Complex apps. Isolates crashes, allows privilege escalation (Helper tool).

**Red Flags → Escalate to `security-engineer`:**
- Requesting "Full Disk Access" without a valid reason
- Embedding private keys in the binary
- Bypassing Gatekeeper/Notarization

---
---

## 3. Core Workflows

### Workflow 1: Menu Bar App (SwiftUI)

**Goal:** Create an app that lives in the menu bar.

**Steps:**

1.  **App Setup**
    ```swift
    @main
    struct MenuBarApp: App {
        var body: some Scene {
            MenuBarExtra("Utility", systemImage: "hammer") {
                Button("Action") { doWork() }
                Divider()
                Button("Quit") { NSApplication.shared.terminate(nil) }
            }
        }
    }
    ```

2.  **Hide Dock Icon**
    -   Info.plist: `LSUIElement` = `YES`.

---
---

### Workflow 3: System Extension (Endpoint Security)

**Goal:** Monitor file events.

**Steps:**

1.  **Entitlements**
    -   `com.apple.developer.endpoint-security.client` = `YES`.

2.  **Implementation (C API)**
    ```c
    es_client_t *client;
    es_new_client(&client, ^(es_client_t *c, const es_message_t *msg) {
        if (msg->event_type == ES_EVENT_TYPE_NOTIFY_EXEC) {
            // Log process execution
        }
    });
    ```

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Assuming iOS Behavior

**What it looks like:**
-   Using `NavigationView` (split view) when a simple Window is needed.
-   Ignoring Menu Bar commands (`Cmd+Q`, `Cmd+S`).

**Why it fails:**
-   Feels alien on Mac.

**Correct approach:**
-   Support **Keyboard Shortcuts**.
-   Support **Multi-Window** workflows.

### ❌ Anti-Pattern 2: Blocking Main Thread

**What it looks like:**
-   Running file I/O on main thread.

**Why it fails:**
-   Spinning Beach Ball of Death (SPOD).

**Correct approach:**
-   Use `DispatchQueue.global()` or Swift `Task`.

---
---

## Examples

### Example 1: Professional Menu Bar Application

**Scenario:** Build a system utility that lives in the macOS menu bar for quick access.

**Development Approach:**
1. **Project Setup**: SwiftUI with MenuBarExtra
2. **Window Management**: Hidden dock icon with popup menu
3. **Settings Integration**: UserDefaults for preferences
4. **Status Item**: Custom NSStatusItem with icon and menu

**Implementation:**
```swift
@main
struct SystemUtilityApp: App {
    var body: some Scene {
        MenuBarExtra("System Utility", systemImage: "gear") {
            VStack(spacing: 12) {
                Button("Open Preferences") { openPreferences() }
                Button("Check Updates") { checkForUpdates() }
                Divider()
                Button("Quit") { NSApplication.shared.terminate(nil) }
            }
            .padding()
            .frame(width: 200)
        }
    }
}
```

**Key Features:**
- LSUIElement in Info.plist to hide dock icon
- Keyboard shortcuts for quick actions
- Background refresh with menu updates
- Sparkle for automatic updates

**Results:**
- Released on Mac App Store with 4.8-star rating
- 50,000+ active users
- Featured in "Best New Apps" category

### Example 2: Document-Based Application with XPC Services

**Scenario:** Build a professional document editor with background processing.

**Architecture:**
1. **Main App**: SwiftUI document handling
2. **XPC Service**: Background document processing
3. **Sandbox**: Proper app sandbox configuration
4. **IPC**: NSXPCConnection for communication

**XPC Service Implementation:**
```swift
// Service Protocol
@objc protocol ProcessingServiceProtocol {
    func processDocument(at url: URL, reply: @escaping (URL?) -> Void)
}

// Service Implementation
class ProcessingService: NSObject, ProcessingServiceProtocol {
    func processDocument(at url: URL, reply: @escaping (URL?) -> Void) {
        // Heavy processing in separate process
        let result = heavyProcessing(url: url)
        reply(result)
    }
}
```

**Benefits:**
- Crash isolation (service crash doesn't kill app)
- Reduced memory footprint
- Privilege separation for sensitive operations
- Better App Store approval chances

### Example 3: System Extension for Network Monitoring

**Scenario:** Create a network monitoring tool using System Extension.

**Development Process:**
1. **Entitlement Configuration**: Endpoint security entitlement
2. **System Extension**: Network extension implementation
3. **Deployment**: Proper notarization and signing
4. **User Approval**: System extension approval workflow

**Implementation:**
```swift
// Network extension handler
class NetworkExtensionHandler: NEProvider {
    override func startProtocol(options: [String: Any]?, completionHandler: @escaping (Error?) -> Void) {
        // Start network monitoring
        setupNetworkMonitoring()
        completionHandler(nil)
    }
    
    override func stopProtocol(with reason: NEProviderStopReason, completionHandler: @escaping () -> Void) {
        // Clean up resources
        stopNetworkMonitoring()
        completionHandler()
    }
}
```

**Requirements:**
- Notarization for distribution outside App Store
- User-approved system extension
- Proper entitlements from Apple Developer portal

## Best Practices

### AppKit and SwiftUI Integration

- **Hybrid Approach**: Use SwiftUI for UI, AppKit for complex components
- **NSViewRepresentable**: Wrap NSView for SwiftUI use
- **NSHostingView**: Embed SwiftUI in AppKit windows
- **Data Flow**: Use Observable or StateObject for shared state

### Sandboxing and Security

- **Minimal Entitlements**: Request only necessary permissions
- **Keychain**: Use Keychain for sensitive data storage
- **App Sandbox**: Enable for App Store distribution
- **Hardened Runtime**: Required for notarization

### Distribution and Deployment

- **Code Signing**: Always sign before notarization
- **Notarization**: Submit to Apple for security validation
- **Auto-Updates**: Implement Sparkle for direct distribution
- **DMG Creation**: Use create-dmg or similar tools

### Performance Optimization

- **Lazy Loading**: Defer resource loading until needed
- **Background Tasks**: Use BGTaskScheduler for long operations
- **Memory Management**: Monitor memory pressure
- **Startup Time**: Optimize launch sequence

### User Experience

- **Keyboard Navigation**: Support full keyboard operation
- **Dark Mode**: Properly handle light and dark appearances
- **Accessibility**: VoiceOver compatibility from start
- **Window Management**: Support multiple windows properly

## Quality Checklist

**UX:**
-   [ ] **Menus:** App supports standard menu commands.
-   [ ] **Windows:** Resizable, supports Full Screen.
-   [ ] **Dark Mode:** Supports System Appearance.
-   [ ] **Accessibility:** VoiceOver works on key elements.

**System:**
-   [ ] **Sandboxing:** App Sandbox enabled (if App Store).
-   [ ] **Hardened Runtime:** Enabled for Notarization.
-   [ ] **Code Signing:** Properly signed for distribution.
-   [ ] **Notarization:** Submitted and approved by Apple.

**Performance:**
-   [ ] **Startup:** App launches within 5 seconds.
-   [ ] **Memory:** No memory leaks or excessive usage.
-   [ ] **Responsive:** UI remains responsive during operations.
