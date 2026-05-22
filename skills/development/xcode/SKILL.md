---
name: xcode
description: Xcode Apple development IDE with simulators. Use for iOS/macOS development.
---

# Xcode

Xcode is the only IDE for native Apple platforms. 2025 (Xcode 17) brings **Swift Assist** and **Predictive Code Completion** running locally on Apple Silicon.

## When to Use

- **iOS/macOS**: Building native apps.
- **SwiftUI**: "Previws" canvas is essential.
- **Instruments**: Deep performance profiling of Apple apps.

## Core Concepts

### Project/Workspace

`.xcodeproj` and `.xcworkspace`. Use Workspaces if using CocoaPods or multiple projects.

### SwiftUI Previews

`#Preview` macro (Swift 5.9+) allows instant rendering of views.

### Simulators

Run iOS on your Mac.

## Best Practices (2025)

**Do**:

- **Use Swift Testing**: The new `Testing` framework (macro-based) replaces XCTest.
- **Use `.xcstrings`**: The new String Catalog format for localization (replaces `.strings`).
- **Use CloudKit Console**: Debug database data directly from the IDE/Web.

**Don't**:

- **Don't fight the build system**: If weird errors occur, `Product > Clean Build Folder` (Cmd+Shift+K) is the first troubleshooting step.

## References

- [Xcode Documentation](https://developer.apple.com/xcode/)
