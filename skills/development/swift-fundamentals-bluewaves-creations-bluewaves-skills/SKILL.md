---
name: swift-fundamentals
description: Swift 6.x language best practices, macros, project setup, and modern patterns. Use when user asks about Swift syntax, Package.swift configuration, project structure, macros like @Observable/@Model/@MainActor, property wrappers, or modern Swift development patterns.
allowed-tools: Bash, Read, Write, Edit
---

# Swift Fundamentals

Comprehensive guide to Swift 6.x language features, best practices, macros, and project configuration for iOS 26 and macOS Tahoe development.

## Prerequisites

- Xcode 26+ or Swift 6.x toolchain
- macOS 15.5+ (Sequoia) for full iOS 26 support

## Swift Version Check

```bash
swift --version
# Swift version 6.x
```

---

## Swift 6.x Key Features

### Swift 6.0 - Major Changes

1. **Complete Concurrency Checking** - Strict data-race safety by default
2. **Typed Throws** - Functions can specify error types: `throws(MyError)`
3. **Noncopyable Types** - `~Copyable` for unique ownership
4. **Pack Iteration** - Iterate over parameter packs
5. **128-bit Integer Types** - `Int128` and `UInt128`
6. **count(where:)** - Count elements matching predicate

### Swift 6.2 - Recent Improvements

1. **Approachable Concurrency** - Easier adoption path
2. **Single-threaded by default** - New `defaultIsolation` setting
3. **Observations Async Sequence** - Stream state changes
4. **Pre-built swift-syntax** - Faster macro compilation
5. **InlineArray** - Fixed-size inline storage

### Swift 6.3 - Latest (2025)

1. **Enhanced Type Inference** - Better generic inference
2. **Improved Error Messages** - Clearer diagnostics
3. **Performance Optimizations** - Faster compilation

---

## Core Macros

### @Observable (iOS 17+)

Modern replacement for `ObservableObject`. Automatically tracks property access.

```swift
import Observation

@Observable
class UserSettings {
    var username: String = ""
    var isLoggedIn: Bool = false
    var preferences: Preferences = Preferences()

    // Computed properties are also tracked
    var displayName: String {
        isLoggedIn ? username : "Guest"
    }
}

// Usage in SwiftUI
struct SettingsView: View {
    var settings: UserSettings  // No @ObservedObject needed

    var body: some View {
        Text(settings.displayName)
        // View automatically updates when displayName changes
    }
}
```

**Key Differences from ObservableObject:**
- No `@Published` property wrappers needed
- No `objectWillChange` publisher
- Finer-grained updates (per-property, not whole object)
- Use `@Bindable` for two-way bindings

```swift
struct EditView: View {
    @Bindable var settings: UserSettings

    var body: some View {
        TextField("Username", text: $settings.username)
    }
}
```

### @Model (SwiftData)

Declares a SwiftData model with automatic persistence.

```swift
import SwiftData

@Model
class Note {
    var title: String
    var content: String
    var createdAt: Date
    var tags: [Tag]?  // Optional relationship for CloudKit

    init(title: String, content: String = "") {
        self.title = title
        self.content = content
        self.createdAt = Date()
    }
}

@Model
class Tag {
    var name: String
    var notes: [Note]?  // Inverse relationship

    init(name: String) {
        self.name = name
    }
}
```

**Important for CloudKit Sync:**
- All relationships must be optional
- No `@Attribute(.unique)` constraints
- Default values required for non-optional properties

### @MainActor

Ensures code runs on the main thread/actor.

```swift
@MainActor
class ViewModel {
    var items: [Item] = []
    var isLoading = false

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        // Network call can be off main actor
        let fetched = await fetchItems()

        // Assignment happens on main actor
        items = fetched
    }

    nonisolated func fetchItems() async -> [Item] {
        // This can run on any thread
        try? await URLSession.shared.data(from: url)
        // ...
    }
}
```

### @Generable (Foundation Models - iOS 26)

Enables structured AI output generation.

```swift
import FoundationModels

@Generable
struct MovieRecommendation {
    var title: String
    var year: Int
    var genre: String
    var reason: String
}

// Usage
let session = LanguageModelSession()
let recommendation: MovieRecommendation = try await session.respond(
    to: "Recommend a sci-fi movie from the 2020s"
)
```

### @Test (Swift Testing)

Marks a function as a test case.

```swift
import Testing

@Test("User can create account with valid email")
func createAccountWithValidEmail() async throws {
    let result = try await authService.createAccount(email: "test@example.com")
    #expect(result.success)
    #expect(result.user?.email == "test@example.com")
}

@Test("Password validation", arguments: [
    ("abc", false),
    ("abc12345", true),
    ("ABC12345!", true)
])
func validatePassword(password: String, expected: Bool) {
    #expect(validator.isValid(password) == expected)
}
```

---

## Property Wrappers

### SwiftUI Property Wrappers

```swift
struct ContentView: View {
    // Local state - view owns this value
    @State private var count = 0

    // Two-way binding from parent
    @Binding var selectedTab: Int

    // Environment value from system or parent
    @Environment(\.colorScheme) var colorScheme

    // Custom environment object
    @Environment(AppState.self) var appState

    // SwiftData query
    @Query(sort: \Note.createdAt, order: .reverse)
    var notes: [Note]

    // Focus state for text fields
    @FocusState private var isFocused: Bool

    // Namespace for matched geometry effects
    @Namespace private var animation

    var body: some View {
        // ...
    }
}
```

### @Bindable (iOS 17+)

Creates bindings to @Observable properties.

```swift
struct EditorView: View {
    @Bindable var document: Document  // Document is @Observable

    var body: some View {
        TextEditor(text: $document.content)
        Toggle("Published", isOn: $document.isPublished)
    }
}
```

### @AppStorage

Persists values to UserDefaults.

```swift
struct SettingsView: View {
    @AppStorage("hasCompletedOnboarding") var hasCompletedOnboarding = false
    @AppStorage("preferredTheme") var preferredTheme = "system"
    @AppStorage("notificationsEnabled") var notificationsEnabled = true

    var body: some View {
        Toggle("Notifications", isOn: $notificationsEnabled)
    }
}
```

### @SceneStorage

Persists view state per scene (for state restoration).

```swift
struct DocumentView: View {
    @SceneStorage("selectedDocumentID") var selectedDocumentID: String?
    @SceneStorage("scrollPosition") var scrollPosition: Double = 0

    var body: some View {
        // State restored when scene is recreated
    }
}
```

---

## Package.swift Configuration

### Basic Package

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
        .iOS(.v26),
        .macOS(.v26)
    ],
    products: [
        .library(name: "MyApp", targets: ["MyApp"])
    ],
    dependencies: [
        // External dependencies
    ],
    targets: [
        .target(
            name: "MyApp",
            dependencies: [],
            swiftSettings: [
                .enableExperimentalFeature("StrictConcurrency")
            ]
        ),
        .testTarget(
            name: "MyAppTests",
            dependencies: ["MyApp"]
        )
    ]
)
```

### With Dependencies

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
        .iOS(.v26),
        .macOS(.v26)
    ],
    products: [
        .library(name: "MyApp", targets: ["MyApp"])
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-algorithms", from: "1.2.0"),
        .package(url: "https://github.com/apple/swift-collections", from: "1.1.0"),
        .package(url: "https://github.com/apple/swift-async-algorithms", from: "1.0.0")
    ],
    targets: [
        .target(
            name: "MyApp",
            dependencies: [
                .product(name: "Algorithms", package: "swift-algorithms"),
                .product(name: "Collections", package: "swift-collections"),
                .product(name: "AsyncAlgorithms", package: "swift-async-algorithms")
            ]
        )
    ]
)
```

### Strict Concurrency Settings

```swift
swiftSettings: [
    // Full Swift 6 concurrency
    .enableExperimentalFeature("StrictConcurrency"),

    // Or gradual adoption
    .swiftLanguageMode(.v6),

    // Enable upcoming features
    .enableUpcomingFeature("ExistentialAny"),
    .enableUpcomingFeature("InternalImportsByDefault")
]
```

---

## Project Structure

### Recommended Layout

```
MyApp/
├── Package.swift
├── Sources/
│   └── MyApp/
│       ├── App/
│       │   ├── MyAppApp.swift
│       │   └── AppState.swift
│       ├── Models/
│       │   ├── Note.swift
│       │   ├── Tag.swift
│       │   └── User.swift
│       ├── Views/
│       │   ├── ContentView.swift
│       │   ├── Notes/
│       │   │   ├── NoteListView.swift
│       │   │   ├── NoteDetailView.swift
│       │   │   └── NoteEditorView.swift
│       │   └── Settings/
│       │       └── SettingsView.swift
│       ├── Services/
│       │   ├── NetworkService.swift
│       │   └── StorageService.swift
│       ├── Utilities/
│       │   ├── Extensions/
│       │   └── Helpers/
│       └── Resources/
│           ├── Localizable.xcstrings
│           └── Assets.xcassets
└── Tests/
    └── MyAppTests/
        ├── ModelTests/
        ├── ServiceTests/
        └── ViewTests/
```

### App Entry Point

```swift
import SwiftUI
import SwiftData

@main
struct MyAppApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Note.self, Tag.self])
    }
}
```

### With Custom Container Configuration

```swift
@main
struct MyAppApp: App {
    let container: ModelContainer

    init() {
        let schema = Schema([Note.self, Tag.self])
        let config = ModelConfiguration(
            schema: schema,
            isStoredInMemoryOnly: false,
            cloudKitDatabase: .automatic  // Enable iCloud sync
        )

        do {
            container = try ModelContainer(for: schema, configurations: config)
        } catch {
            fatalError("Failed to configure SwiftData: \(error)")
        }
    }

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}
```

---

## Modern Swift Patterns

### Result Builders

```swift
@resultBuilder
struct HTMLBuilder {
    static func buildBlock(_ components: String...) -> String {
        components.joined()
    }

    static func buildOptional(_ component: String?) -> String {
        component ?? ""
    }

    static func buildEither(first component: String) -> String {
        component
    }

    static func buildEither(second component: String) -> String {
        component
    }
}

func html(@HTMLBuilder content: () -> String) -> String {
    "<html>\(content())</html>"
}

let page = html {
    "<head><title>Hello</title></head>"
    "<body>"
    if showHeader {
        "<h1>Welcome</h1>"
    }
    "<p>Content here</p>"
    "</body>"
}
```

### Typed Throws (Swift 6)

```swift
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed
}

func fetchUser(id: Int) throws(NetworkError) -> User {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        throw .invalidURL
    }
    // ...
}

// Caller knows exactly what errors to handle
do {
    let user = try fetchUser(id: 123)
} catch .invalidURL {
    // Handle invalid URL
} catch .noData {
    // Handle no data
} catch .decodingFailed {
    // Handle decoding error
}
```

### Noncopyable Types (Swift 6)

```swift
struct UniqueResource: ~Copyable {
    let handle: Int

    init(handle: Int) {
        self.handle = handle
    }

    deinit {
        // Clean up resource
        closeHandle(handle)
    }

    consuming func close() {
        // Explicitly consume the resource
    }
}

func useResource() {
    let resource = UniqueResource(handle: 42)
    // resource cannot be copied
    // processResource(resource)  // This moves resource
    // resource.doSomething()     // Error: resource was moved
}
```

### Parameter Packs (Swift 6)

```swift
func all<each T: Equatable>(
    _ values: repeat each T,
    equalTo comparisons: repeat each T
) -> Bool {
    for (value, comparison) in repeat (each values, each comparisons) {
        if value != comparison {
            return false
        }
    }
    return true
}

let result = all(1, "hello", true, equalTo: 1, "hello", true)  // true
```

---

## Error Handling Best Practices

### Define Domain Errors

```swift
enum AppError: LocalizedError {
    case networkUnavailable
    case unauthorized
    case notFound(resource: String)
    case validationFailed(field: String, reason: String)
    case unknown(underlying: Error)

    var errorDescription: String? {
        switch self {
        case .networkUnavailable:
            return "Network connection unavailable"
        case .unauthorized:
            return "You are not authorized to perform this action"
        case .notFound(let resource):
            return "\(resource) was not found"
        case .validationFailed(let field, let reason):
            return "\(field): \(reason)"
        case .unknown(let error):
            return error.localizedDescription
        }
    }
}
```

### Result Type Pattern

```swift
func fetchData() async -> Result<Data, AppError> {
    guard NetworkMonitor.shared.isConnected else {
        return .failure(.networkUnavailable)
    }

    do {
        let data = try await networkService.fetch()
        return .success(data)
    } catch {
        return .failure(.unknown(underlying: error))
    }
}

// Usage
switch await fetchData() {
case .success(let data):
    process(data)
case .failure(let error):
    showError(error)
}
```

---

## Extensions Best Practices

### Organize by Functionality

```swift
// String+Validation.swift
extension String {
    var isValidEmail: Bool {
        let pattern = #"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"#
        return range(of: pattern, options: .regularExpression) != nil
    }

    var isValidPassword: Bool {
        count >= 8 &&
        range(of: "[A-Z]", options: .regularExpression) != nil &&
        range(of: "[0-9]", options: .regularExpression) != nil
    }
}

// Date+Formatting.swift
extension Date {
    var relativeDescription: String {
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .short
        return formatter.localizedString(for: self, relativeTo: Date())
    }

    var iso8601String: String {
        ISO8601DateFormatter().string(from: self)
    }
}

// View+Modifiers.swift
extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }

    @ViewBuilder
    func `if`<Content: View>(_ condition: Bool, transform: (Self) -> Content) -> some View {
        if condition {
            transform(self)
        } else {
            self
        }
    }
}
```

---

## Code Quality

### SwiftLint Configuration

```yaml
# .swiftlint.yml
included:
  - Sources
  - Tests

excluded:
  - .build
  - Package.swift

disabled_rules:
  - trailing_whitespace
  - line_length

opt_in_rules:
  - empty_count
  - explicit_init
  - closure_spacing
  - overridden_super_call
  - redundant_nil_coalescing
  - private_outlet
  - nimble_operator
  - attributes
  - operator_usage_whitespace
  - closure_end_indentation
  - first_where
  - object_literal
  - number_separator
  - prohibited_super_call
  - fatal_error_message
  - weak_delegate

line_length:
  warning: 120
  error: 200

type_body_length:
  warning: 300
  error: 500

file_length:
  warning: 500
  error: 1000

identifier_name:
  min_length: 2
  max_length: 50
```

### Swift Format Configuration

```swift
// .swift-format
{
  "version": 1,
  "lineLength": 120,
  "indentation": {
    "spaces": 4
  },
  "tabWidth": 4,
  "maximumBlankLines": 1,
  "respectsExistingLineBreaks": true,
  "lineBreakBeforeControlFlowKeywords": false,
  "lineBreakBeforeEachArgument": false
}
```

---

## Official Resources

- [The Swift Programming Language](https://docs.swift.org/swift-book/)
- [Swift Evolution](https://github.com/apple/swift-evolution)
- [Swift 6.0 Release Notes](https://www.swift.org/blog/swift-6-release/)
- [Swift 6.2 Release Notes](https://www.swift.org/blog/swift-6.2-released/)
- [Swift Package Manager Documentation](https://www.swift.org/documentation/package-manager/)
- [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
