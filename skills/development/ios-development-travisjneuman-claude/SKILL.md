---
name: ios-development
description: iOS, iPadOS, and tvOS development with Swift, SwiftUI, and UIKit. Use when building Apple platform apps, implementing iOS-specific features, or following Apple Human Interface Guidelines.
---

# iOS/iPadOS/tvOS Development

Comprehensive guide for building native Apple platform applications.

## Platforms Covered

| Platform | Minimum Target | Current     |
| -------- | -------------- | ----------- |
| iOS      | iOS 15.0+      | iOS 17+     |
| iPadOS   | iPadOS 15.0+   | iPadOS 17+  |
| tvOS     | tvOS 15.0+     | tvOS 17+    |
| watchOS  | watchOS 8.0+   | watchOS 10+ |

---

## SwiftUI (Preferred for New Projects)

### Basic Structure

```swift
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 20) {
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

### State Management

```swift
// Local state
@State private var text = ""

// Binding (child components)
@Binding var isPresented: Bool

// Observable object
@StateObject private var viewModel = MyViewModel()
@ObservedObject var viewModel: MyViewModel

// Environment
@Environment(\.dismiss) private var dismiss
@Environment(\.colorScheme) private var colorScheme
@EnvironmentObject var appState: AppState

// App Storage (UserDefaults)
@AppStorage("username") private var username = ""
```

### Modern Concurrency

```swift
// Async/await
func fetchData() async throws -> [Item] {
    let url = URL(string: "https://api.example.com/items")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode([Item].self, from: data)
}

// In View
.task {
    do {
        items = try await fetchData()
    } catch {
        errorMessage = error.localizedDescription
    }
}

// Main actor for UI updates
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []

    func load() async {
        items = try? await fetchData()
    }
}
```

### Navigation (iOS 16+)

```swift
// NavigationStack with typed destinations
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: item) {
                    Text(item.name)
                }
            }
            .navigationDestination(for: Item.self) { item in
                DetailView(item: item)
            }
        }
    }
}
```

### Lists and Grids

```swift
// Modern List
List {
    ForEach(items) { item in
        ItemRow(item: item)
    }
    .onDelete(perform: delete)
    .onMove(perform: move)
}
.listStyle(.insetGrouped)
.searchable(text: $searchText)
.refreshable {
    await refresh()
}

// LazyVGrid
LazyVGrid(columns: [
    GridItem(.adaptive(minimum: 150))
]) {
    ForEach(items) { item in
        ItemCard(item: item)
    }
}
```

---

## UIKit (Legacy/Complex UI)

### View Controller Lifecycle

```swift
class MyViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // About to appear
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        // Fully visible
    }
}
```

### Auto Layout

```swift
// Programmatic constraints
NSLayoutConstraint.activate([
    label.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 20),
    label.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
    label.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16)
])
```

---

## Data Persistence

### Core Data

```swift
// Model
@objc(Item)
public class Item: NSManagedObject {
    @NSManaged public var id: UUID
    @NSManaged public var name: String
    @NSManaged public var createdAt: Date
}

// Fetch
@FetchRequest(
    sortDescriptors: [NSSortDescriptor(keyPath: \Item.createdAt, ascending: false)],
    animation: .default
)
private var items: FetchedResults<Item>
```

### SwiftData (iOS 17+)

```swift
@Model
class Item {
    var id: UUID
    var name: String
    var createdAt: Date

    init(name: String) {
        self.id = UUID()
        self.name = name
        self.createdAt = Date()
    }
}

// In View
@Query(sort: \Item.createdAt, order: .reverse)
private var items: [Item]

@Environment(\.modelContext) private var modelContext

func addItem() {
    let item = Item(name: "New Item")
    modelContext.insert(item)
}
```

### Keychain

```swift
// Store sensitive data
import Security

func saveToKeychain(key: String, data: Data) throws {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrAccount as String: key,
        kSecValueData as String: data
    ]
    SecItemDelete(query as CFDictionary)
    let status = SecItemAdd(query as CFDictionary, nil)
    guard status == errSecSuccess else {
        throw KeychainError.saveFailed
    }
}
```

---

## Networking

### URLSession

```swift
actor NetworkService {
    func fetch<T: Decodable>(_ type: T.Type, from url: URL) async throws -> T {
        let (data, response) = try await URLSession.shared.data(from: url)

        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.invalidResponse
        }

        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

---

## Apple Human Interface Guidelines

### iOS Design Principles

- **Clarity**: Text is legible, icons precise, adornments subtle
- **Deference**: Content is paramount, UI doesn't compete
- **Depth**: Visual layers and realistic motion convey hierarchy

### Key Metrics

| Element        | Size                           |
| -------------- | ------------------------------ |
| Touch target   | 44x44 pt minimum               |
| Navigation bar | 44 pt                          |
| Tab bar        | 49 pt                          |
| Status bar     | 47 pt (notch) / 20 pt (legacy) |

### Safe Areas

```swift
.safeAreaInset(edge: .bottom) {
    BottomBar()
}

// Ignore safe area
.ignoresSafeArea(.keyboard)
.ignoresSafeArea(.container, edges: .bottom)
```

---

## Platform-Specific

### iPadOS Specifics

```swift
// Split view
NavigationSplitView {
    Sidebar()
} content: {
    ContentList()
} detail: {
    DetailView()
}

// Keyboard shortcuts
.keyboardShortcut("n", modifiers: .command)

// Hover effects
.hoverEffect(.highlight)
```

### tvOS Specifics

```swift
// Focus management
@FocusState private var isFocused: Bool

Button("Action") { }
    .focused($isFocused)
    .focusable()

// Large text for 10-foot UI
.font(.system(size: 38))
```

---

## App Store Requirements

### Required Assets

- App icon (1024x1024)
- Screenshots for each device size
- Privacy policy URL
- App description (4000 char max)

### Privacy

```xml
<!-- Info.plist -->
<key>NSCameraUsageDescription</key>
<string>We need camera access to...</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>We need photo access to...</string>
```

### App Transport Security

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
</dict>
```

---

## Testing

### Unit Tests

```swift
import XCTest
@testable import MyApp

final class MyTests: XCTestCase {
    func testExample() async throws {
        let sut = MyViewModel()
        await sut.load()
        XCTAssertEqual(sut.items.count, 10)
    }
}
```

### UI Tests

```swift
import XCTest

final class MyUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUp() {
        continueAfterFailure = false
        app.launch()
    }

    func testNavigation() {
        app.buttons["Start"].tap()
        XCTAssertTrue(app.staticTexts["Welcome"].exists)
    }
}
```

---

## Project Structure

```
MyApp/
├── App/
│   └── MyApp.swift
├── Features/
│   ├── Home/
│   │   ├── HomeView.swift
│   │   └── HomeViewModel.swift
│   └── Settings/
│       └── SettingsView.swift
├── Core/
│   ├── Models/
│   ├── Services/
│   └── Extensions/
├── Resources/
│   ├── Assets.xcassets
│   └── Localizable.strings
└── Tests/
```

---

## Best Practices

### DO:

- Use SwiftUI for new projects
- Support Dynamic Type for accessibility
- Handle all device orientations
- Implement proper error handling
- Use Swift's type system fully

### DON'T:

- Force unwrap optionals without validation
- Block main thread with network calls
- Hardcode strings (use localization)
- Ignore memory management (retain cycles)
- Skip accessibility labels
