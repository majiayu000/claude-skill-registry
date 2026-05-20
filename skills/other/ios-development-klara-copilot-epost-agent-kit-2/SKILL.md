---
name: ios-development
description: Use when working with .swift files, Xcode projects, SwiftUI/UIKit, or iOS-specific features
user-invokable: false

metadata:
  agent-affinity: [epost-implementer, epost-tester, epost-debugger, epost-reviewer]
  keywords: [ios, swift, swiftui, uikit, xcode, iphone, ipad, mobile]
  platforms: [ios]
  triggers: [".swift", ".xcodeproj", ".xcworkspace", "ios", "iphone", "ipad"]
---

# iOS Development Skill

## Purpose
Modern iOS development (Swift 6, iOS 18+, SwiftUI, UIKit) with XcodeBuildMCP integration for autonomous Xcode operations.

## When Active
User mentions iOS, Swift, SwiftUI, UIKit, iPhone app, iPad app, or iOS-specific commands.

## Specialized Sub-Skills

This skill includes 3 specialized sub-skills for different iOS development aspects:

### 1. Development Patterns
Reference: `ios/development/references/development.md`

- Swift 6 concurrency (async/await, Sendable, Actors)
- SwiftUI vs UIKit strategy
- Architecture patterns (MVVM, TCA)
- State management (@Observable, property wrappers)
- NavigationStack implementation
- Networking with URLSession
- Persistence (SwiftData, Core Data)
- Common UI components (List, Grid, Sheet, Form)
- Debugging patterns

### 2. Build & Simulator Management
Reference: `ios/development/references/build.md`

- Xcode project configuration
- Build settings and schemes
- Swift Package Manager
- Dependency management (SPM, CocoaPods)
- Asset catalogs and resources
- Code signing and provisioning
- Build optimization
- Simulator management (xcrun simctl + XcodeBuildMCP)
- Common build errors and fixes
- MCP tool patterns (discover_projs, list_schemes, build_sim, etc.)

### 3. Testing Strategies
Reference: `ios/development/references/tester.md`

- XCTest patterns (unit tests)
- XCUITest patterns (UI tests)
- Mock dependencies setup
- Given-When-Then structure
- Async/await testing
- Coverage goals and reporting
- Test organization
- Accessibility identifiers for UI testing
- MCP test automation (test_sim, test_device)

## XcodeBuildMCP Integration

When XcodeBuildMCP is available, this skill provides autonomous Xcode operations:

### MCP Capabilities
- **Project Discovery**: Auto-discover projects and schemes
- **Build Automation**: Build for simulator, device, or macOS
- **Simulator Management**: Boot, install, launch, stop apps
- **Testing**: Run XCTest/XCUITest suites
- **UI Automation**: Tap, swipe, type, screenshot
- **Log Capture**: Stream simulator/device logs
- **Environment Validation**: Run diagnostics

### Prerequisites
- macOS 14.5+ with Xcode 16.x+
- XcodeBuildMCP server: `claude mcp add XcodeBuildMCP npx xcodebuildmcp@latest`

## Patterns

### @Observable (iOS 17+)
```swift
@Observable
class ProductsViewModel {
    var products: [Product] = []
    var isLoading = false

    func loadProducts() async {
        isLoading = true
        defer { isLoading = false }
        products = try await productService.fetch()
    }
}
```

### NavigationStack
```swift
enum Route: Hashable {
    case product(Product)
    case settings
}

struct AppView: View {
    @State private var path: [Route] = []

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: Route.self) { route in
                    // route handling
                }
        }
    }
}
```

### Actor for Thread-Safety
```swift
actor NetworkManager {
    func fetch(_ url: URL) async throws -> Data {
        // Thread-safe networking
    }
}
```

## MCP Workflow Examples

### Build for Simulator
```swift
// MCP approach:
mcp__xcodebuildmcp__discover_projs({ workspaceRoot: '.' })
mcp__xcodebuildmcp__list_schemes({ workspacePath: 'MyApp.xcworkspace' })
mcp__xcodebuildmcp__build_sim({
  workspacePath: 'MyApp.xcworkspace',
  scheme: 'MyApp',
  simulatorId: 'iPhone-16-Pro-UUID'
})
```

### Run Tests
```swift
mcp__xcodebuildmcp__test_sim({
  projectPath: 'MyApp.xcodeproj',
  scheme: 'MyApp',
  simulatorId: 'UUID'
})
```

### UI Automation
```swift
// IMPORTANT: Always use describe_ui first
mcp__xcodebuildmcp__describe_ui({ simulatorId: 'UUID' })
// Then parse UI hierarchy and interact
mcp__xcodebuildmcp__tap({ simulatorId: 'UUID', x: 100, y: 200 })
```

## Tech Stack
- iOS 18+ SDK, Swift 6.0+
- SwiftUI (primary), UIKit (fallback)
- SwiftData for persistence
- XCTest/XCUITest for testing
- XcodeBuildMCP for automation (optional)

## Sub-Skill Routing

When this skill is active and user intent matches a sub-skill, delegate:

| Intent | Sub-Skill | When |
|--------|-----------|------|
| UI components | `ios-ui-lib` | Theme components, design tokens |
| RAG search | `ios-rag` | Vector search iOS codebase |

## Rules
- SwiftUI first; UIKit only when required
- Use @Observable, not ObservableObject
- async/await, not completion handlers
- MainActor for all UI updates
- Write tests for business logic
- Build after each major implementation step
- Use Swift Testing framework for new tests (iOS 18+)
- Mock network calls with URLProtocol or dependency injection

## Build Commands
```bash
# MCP (preferred)
mcp__xcodebuildmcp__build_sim  # Build for simulator
mcp__xcodebuildmcp__test_sim   # Run tests

# Fallback
xcodebuild -project MyApp.xcodeproj -scheme MyApp -sdk iphonesimulator build
xcodebuild test -project MyApp.xcodeproj -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'
```

## Simulator Commands
```bash
xcrun simctl list devices          # List devices
xcrun simctl boot "iPhone 15 Pro"  # Boot
xcrun simctl install booted /path/to/MyApp.app  # Install
xcrun simctl launch booted com.example.MyApp    # Launch
xcrun simctl io booted screenshot screenshot.png  # Screenshot
xcrun simctl erase "iPhone 15 Pro"  # Reset
```
