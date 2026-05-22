---
name: build-macos-apps
description: Build professional native macOS apps in Swift with SwiftUI and AppKit. Full lifecycle development - build, debug, test, optimize, ship. CLI-focused workflow. Use when building macOS apps, adding features, debugging, testing, or optimizing Mac applications.
---

# Build macOS Apps - Professional Mac Development

Expert guidance for building native macOS apps using Swift, SwiftUI, and AppKit with CLI-first workflow.

## Core Principles

### 1. Prove, Don't Promise
Never say "this should work." Always verify:
```bash
xcodebuild -scheme AppName build
xcodebuild -scheme AppName test
open ./build/Build/Products/Debug/AppName.app
```

### 2. Tests for Correctness, Eyes for Quality
Tests verify correctness. Users verify desirability.

### 3. Report Outcomes, Not Code
✅ Good: "Fixed memory leak. 0 leaks, stable for 5 minutes."
❌ Bad: "Refactored DataService to use async/await"

### 4. Small Steps, Always Verified
Change → Verify → Report → Next change

### 5. Ask Before, Not After
Clarify requirements before building.

### 6. Always Leave It Working
Every stop = working state.

---

## Verification Loop

After every change:
```bash
xcodebuild -scheme AppName build
xcodebuild -scheme AppName test
open ./build/Build/Products/Debug/AppName.app
```

---

## macOS App Types

### Document-Based
```swift
@main
struct MyApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MyDocument()) { file in
            ContentView(document: file.$document)
        }
    }
}
```

### Menu Bar Apps
```swift
class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem?
    func applicationDidFinishLaunching(_ notification: Notification) {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
    }
}
```

---

## SwiftUI + AppKit

```swift
struct MyAppKitView: NSViewRepresentable {
    func makeNSView(context: Context) -> NSView { /* ... */ }
    func updateNSView(_ nsView: NSView, context: Context) { /* ... */ }
}
```

---

## CLI Commands

```bash
# Build
xcodebuild -scheme AppName build

# Test
xcodebuild test -scheme AppName

# Archive
xcodebuild archive -scheme AppName -archivePath ./App.xcarchive

# Code sign
codesign --force --sign "Developer ID" --timestamp --options runtime ./AppName.app

# Notarize
xcrun notarytool submit AppName.dmg --keychain-profile "AC_PASSWORD" --wait
xcrun stapler staple AppName.dmg
```

---

## Remember

1. Prove it works - build, test, launch
2. Small verified steps
3. Ask first
4. Report outcomes
5. Leave it working
6. Tests for logic, eyes for UI
