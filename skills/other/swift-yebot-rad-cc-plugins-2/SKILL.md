---
name: swift
description: >
  Comprehensive Swift and Apple platform development skill for building native iOS, macOS, tvOS, and iPadOS apps.
  Use when creating Swift projects, building SwiftUI views, implementing Swift concurrency (async/await, actors),
  working with SwiftData or Core Data, configuring Xcode projects, signing and capabilities, implementing
  platform-specific features (WidgetKit, App Intents, Live Activities), or troubleshooting Swift/Xcode issues.
---

# Swift & Apple Platform Development

Build native apps for iOS, macOS, tvOS, and iPadOS using Swift and SwiftUI.

## Instructions

1. For SwiftUI views, modifiers, and state management, see [references/swiftui-reference.md](references/swiftui-reference.md)
2. For async/await, actors, and structured concurrency, see [references/swift-concurrency.md](references/swift-concurrency.md)
3. For MVVM, @Observable, and SwiftData patterns, see [references/app-architecture.md](references/app-architecture.md)
4. For iOS/macOS/tvOS/iPadOS specific APIs, see [references/platform-apis.md](references/platform-apis.md)
5. For Xcode configuration, signing, and App Store, see [references/xcode-distribution.md](references/xcode-distribution.md)
6. PROACTIVELY use WebSearch to find current Apple Developer Documentation when you need deeper information on any Apple framework or API not covered in local references
7. PROACTIVELY fetch https://www.swift.org/documentation/ for Swift language documentation and evolution proposals

## Online Documentation Resources

When local references don't cover what you need:

| Topic | URL |
|-------|-----|
| Apple Developer Docs | https://developer.apple.com/documentation/ |
| Swift Language Guide | https://docs.swift.org/swift-book/documentation/the-swift-programming-language/ |
| SwiftUI Docs | https://developer.apple.com/documentation/swiftui |
| Swift Concurrency | https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/ |
| SwiftData | https://developer.apple.com/documentation/swiftdata |
| Human Interface Guidelines | https://developer.apple.com/design/human-interface-guidelines/ |
| App Store Review Guidelines | https://developer.apple.com/app-store/review/guidelines/ |

## Quick Start

```bash
# Create new Xcode project (use Xcode GUI or swift package init)
mkdir MyApp && cd MyApp
swift package init --type executable --name MyApp

# For iOS/macOS apps, use Xcode:
# File → New → Project → App
# Choose SwiftUI for Interface, Swift for Language
```

## Reference Files

Load these based on the task at hand:

| Task | Reference File |
|------|----------------|
| SwiftUI views, modifiers, state (@State, @Binding, @Observable) | `references/swiftui-reference.md` |
| async/await, actors, Task, structured concurrency | `references/swift-concurrency.md` |
| MVVM architecture, SwiftData, dependency injection | `references/app-architecture.md` |
| Platform-specific APIs (iOS, macOS, tvOS, iPadOS) | `references/platform-apis.md` |
| Xcode setup, signing, capabilities, App Store submission | `references/xcode-distribution.md` |

## Project Structure

```
MyApp/
├── MyApp.xcodeproj           # Xcode project
├── MyApp/
│   ├── MyAppApp.swift        # @main App entry point
│   ├── ContentView.swift     # Root view
│   ├── Views/                # SwiftUI views
│   │   ├── HomeView.swift
│   │   └── DetailView.swift
│   ├── Models/               # Data models
│   │   └── Item.swift
│   ├── ViewModels/           # View models (@Observable)
│   │   └── HomeViewModel.swift
│   ├── Services/             # API, persistence, etc.
│   │   └── DataService.swift
│   ├── Resources/
│   │   └── Assets.xcassets
│   └── Info.plist
├── MyAppTests/
└── MyAppUITests/
```

## Essential Patterns Quick Reference

### App Entry Point

```swift
import SwiftUI

@main
struct MyAppApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### SwiftUI View with State

```swift
import SwiftUI

struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
                .font(.largeTitle)

            Button("Increment") {
                count += 1
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

### @Observable ViewModel (iOS 17+)

```swift
import SwiftUI
import Observation

@Observable
class HomeViewModel {
    var items: [Item] = []
    var isLoading = false
    var error: Error?

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await ItemService.shared.fetchItems()
        } catch {
            self.error = error
        }
    }
}

struct HomeView: View {
    @State private var viewModel = HomeViewModel()

    var body: some View {
        List(viewModel.items) { item in
            Text(item.name)
        }
        .task {
            await viewModel.loadItems()
        }
    }
}
```

### Navigation (iOS 16+)

```swift
import SwiftUI

struct RootView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List {
                NavigationLink("Go to Detail", value: "detail-id")
            }
            .navigationDestination(for: String.self) { id in
                DetailView(id: id)
            }
            .navigationTitle("Home")
        }
    }
}
```

### Async/Await

```swift
func fetchData() async throws -> [Item] {
    let url = URL(string: "https://api.example.com/items")!
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw APIError.invalidResponse
    }

    return try JSONDecoder().decode([Item].self, from: data)
}

// Usage in SwiftUI
.task {
    do {
        items = try await fetchData()
    } catch {
        self.error = error
    }
}
```

### SwiftData Model (iOS 17+)

```swift
import SwiftData

@Model
class Item {
    var name: String
    var createdAt: Date
    var category: Category?

    init(name: String, createdAt: Date = .now) {
        self.name = name
        self.createdAt = createdAt
    }
}

// In App
@main
struct MyAppApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Item.self)
    }
}

// In View
struct ItemsView: View {
    @Query var items: [Item]
    @Environment(\.modelContext) private var modelContext

    var body: some View {
        List(items) { item in
            Text(item.name)
        }
    }

    func addItem() {
        let item = Item(name: "New Item")
        modelContext.insert(item)
    }
}
```

## Common Xcode Commands

```bash
# Build from command line
xcodebuild -project MyApp.xcodeproj -scheme MyApp -configuration Debug build

# Run tests
xcodebuild test -project MyApp.xcodeproj -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'

# Archive for distribution
xcodebuild archive -project MyApp.xcodeproj -scheme MyApp -archivePath MyApp.xcarchive

# List available simulators
xcrun simctl list devices

# Boot a simulator
xcrun simctl boot "iPhone 15"

# Install app on simulator
xcrun simctl install booted MyApp.app
```

## Troubleshooting

### Common Issues

**"Cannot find type 'X' in scope"**
- Check import statements
- Verify target membership of files
- Clean build folder: Cmd+Shift+K

**SwiftUI preview not working**
- Check for compile errors in the file
- Restart Xcode
- Clean derived data: `rm -rf ~/Library/Developer/Xcode/DerivedData`

**Signing issues**
- Open Signing & Capabilities in Xcode
- Select your team
- Let Xcode manage signing automatically

**"Module 'X' was not compiled with library evolution support"**
- Clean build folder
- Delete derived data
- Restart Xcode

## Best Practices

1. **Use SwiftUI** for all new UI work
2. **Prefer @Observable** over ObservableObject (iOS 17+)
3. **Use async/await** instead of completion handlers
4. **Follow Apple HIG** for each platform
5. **Support Dynamic Type** for accessibility
6. **Use SF Symbols** for icons
7. **Test on real devices** before release
8. **Use SwiftData** over Core Data for new projects (iOS 17+)
9. **Implement proper error handling** with Result or throws
10. **Keep views simple** - extract logic to view models
