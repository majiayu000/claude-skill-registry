---
name: swiftui-patterns
description: Modern SwiftUI architecture patterns, @Observable, view composition, state management, and the MV vs MVVM debate. Use when user asks about SwiftUI architecture, @Observable vs ObservableObject, state management, view composition, ViewModels, or structuring SwiftUI apps.
allowed-tools: Bash, Read, Write, Edit
---

# SwiftUI Architecture Patterns

Comprehensive guide to modern SwiftUI architecture, @Observable macro, state management, view composition, and the ongoing MV vs MVVM debate for iOS 26 development.

## Prerequisites

- iOS 17+ for @Observable (iOS 26 recommended)
- Xcode 26+
- SwiftUI framework

---

## The Architecture Debate: MV vs MVVM

### The Modern Reality

With `@Observable` (iOS 17+), SwiftUI has evolved. The traditional MVVM pattern is **not always necessary**.

### When to Use MV (Model-View)

```swift
// Simple screens with straightforward logic
// Model is directly observable

@Observable
class Note {
    var title: String
    var content: String
    var lastModified: Date

    init(title: String = "", content: String = "") {
        self.title = title
        self.content = content
        self.lastModified = Date()
    }
}

struct NoteEditorView: View {
    @Bindable var note: Note  // Direct model binding

    var body: some View {
        VStack {
            TextField("Title", text: $note.title)
            TextEditor(text: $note.content)
        }
        .onChange(of: note.content) {
            note.lastModified = Date()
        }
    }
}
```

**Use MV when:**
- Simple data display and editing
- Logic is minimal or can live in the model
- No complex async operations
- Rapid prototyping

### When to Use MVVM

```swift
// Complex screens needing presentation logic, async operations,
// or coordination between multiple data sources

@Observable
class NoteListViewModel {
    var notes: [Note] = []
    var searchQuery = ""
    var isLoading = false
    var error: Error?

    var filteredNotes: [Note] {
        guard !searchQuery.isEmpty else { return notes }
        return notes.filter {
            $0.title.localizedCaseInsensitiveContains(searchQuery)
        }
    }

    @MainActor
    func loadNotes() async {
        isLoading = true
        defer { isLoading = false }

        do {
            notes = try await noteService.fetchAll()
        } catch {
            self.error = error
        }
    }

    func deleteNote(_ note: Note) async {
        await noteService.delete(note)
        notes.removeAll { $0.id == note.id }
    }
}

struct NoteListView: View {
    @State private var viewModel = NoteListViewModel()

    var body: some View {
        List(viewModel.filteredNotes) { note in
            NoteRow(note: note)
        }
        .searchable(text: $viewModel.searchQuery)
        .task {
            await viewModel.loadNotes()
        }
        .overlay {
            if viewModel.isLoading {
                ProgressView()
            }
        }
    }
}
```

**Use MVVM when:**
- Complex business logic
- Multiple data sources to coordinate
- Async operations (network, database)
- Need testability
- Team prefers clear separation

---

## @Observable vs @ObservableObject

### @Observable (iOS 17+ - Recommended)

```swift
import Observation

@Observable
class UserSettings {
    var username = ""
    var theme: Theme = .system
    var notificationsEnabled = true

    // Computed properties are tracked
    var displayName: String {
        username.isEmpty ? "Guest" : username
    }
}

struct SettingsView: View {
    var settings: UserSettings  // No property wrapper needed

    var body: some View {
        Form {
            TextField("Username", text: Bindable(settings).username)
            // Or with @Bindable
        }
    }
}

struct SettingsViewWithBindable: View {
    @Bindable var settings: UserSettings

    var body: some View {
        Form {
            TextField("Username", text: $settings.username)
            Toggle("Notifications", isOn: $settings.notificationsEnabled)
        }
    }
}
```

**Benefits:**
- Per-property tracking (not whole object)
- No `@Published` needed
- Cleaner syntax
- Better performance

### @ObservableObject (Legacy)

```swift
import Combine

class LegacySettings: ObservableObject {
    @Published var username = ""
    @Published var theme: Theme = .system
    @Published var notificationsEnabled = true

    var displayName: String {
        username.isEmpty ? "Guest" : username
    }
}

struct LegacySettingsView: View {
    @ObservedObject var settings: LegacySettings
    // Or @StateObject if this view owns the object

    var body: some View {
        Form {
            TextField("Username", text: $settings.username)
        }
    }
}
```

**When to use:**
- Supporting iOS 16 or earlier
- Existing codebase migration
- Combine integration needed

---

## Property Wrappers Deep Dive

### @State

Local, view-owned mutable state:

```swift
struct CounterView: View {
    @State private var count = 0
    @State private var history: [Int] = []

    var body: some View {
        VStack {
            Text("Count: \(count)")

            Button("+1") {
                count += 1
                history.append(count)
            }
        }
    }
}
```

**Rules:**
- Always `private`
- View owns the source of truth
- Value types preferred

### @Binding

Two-way connection to parent's state:

```swift
struct ParentView: View {
    @State private var isOn = false

    var body: some View {
        ToggleView(isOn: $isOn)
    }
}

struct ToggleView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Switch", isOn: $isOn)
    }
}

// Creating bindings manually
struct ManualBindingExample: View {
    @State private var value = 0

    var body: some View {
        ChildView(value: Binding(
            get: { value },
            set: { newValue in
                value = min(100, max(0, newValue))  // Clamp
            }
        ))
    }
}
```

### @Bindable

Creates bindings for @Observable:

```swift
@Observable
class Document {
    var title = ""
    var content = ""
}

struct DocumentEditor: View {
    @Bindable var document: Document

    var body: some View {
        VStack {
            TextField("Title", text: $document.title)
            TextEditor(text: $document.content)
        }
    }
}
```

### @Environment

Access shared values from view hierarchy:

```swift
struct ThemedView: View {
    @Environment(\.colorScheme) var colorScheme
    @Environment(\.dismiss) var dismiss
    @Environment(\.horizontalSizeClass) var sizeClass
    @Environment(\.dynamicTypeSize) var dynamicType

    var body: some View {
        VStack {
            if colorScheme == .dark {
                Text("Dark Mode")
            }

            Button("Close") {
                dismiss()
            }
        }
    }
}

// Custom environment values
struct ThemeKey: EnvironmentKey {
    static let defaultValue = AppTheme.default
}

extension EnvironmentValues {
    var appTheme: AppTheme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

// Usage
ContentView()
    .environment(\.appTheme, customTheme)
```

### @Environment with @Observable

```swift
@Observable
class AppState {
    var user: User?
    var isAuthenticated: Bool { user != nil }
}

struct RootView: View {
    @State private var appState = AppState()

    var body: some View {
        ContentView()
            .environment(appState)
    }
}

struct ContentView: View {
    @Environment(AppState.self) var appState

    var body: some View {
        if appState.isAuthenticated {
            MainView()
        } else {
            LoginView()
        }
    }
}
```

---

## View Composition Patterns

### Extract Subviews

```swift
// Before: Monolithic view
struct MessyProfileView: View {
    var user: User

    var body: some View {
        VStack {
            // 50 lines of header code
            // 30 lines of stats code
            // 40 lines of activity code
        }
    }
}

// After: Composed views
struct ProfileView: View {
    var user: User

    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                ProfileHeader(user: user)
                ProfileStats(user: user)
                ProfileActivity(user: user)
            }
        }
    }
}

struct ProfileHeader: View {
    var user: User

    var body: some View {
        VStack {
            AsyncImage(url: user.avatarURL)
            Text(user.name)
        }
    }
}
```

### ViewBuilder Methods

```swift
struct ContentView: View {
    var items: [Item]
    var isEditing: Bool

    var body: some View {
        VStack {
            header
            itemsList
            if isEditing {
                editingControls
            }
        }
    }

    private var header: some View {
        Text("Items")
            .font(.largeTitle)
    }

    @ViewBuilder
    private var itemsList: some View {
        if items.isEmpty {
            ContentUnavailableView("No Items", systemImage: "tray")
        } else {
            List(items) { item in
                ItemRow(item: item)
            }
        }
    }

    @ViewBuilder
    private var editingControls: some View {
        HStack {
            Button("Select All") { }
            Button("Delete", role: .destructive) { }
        }
    }
}
```

### Generic Views

```swift
struct LoadingView<Content: View, T>: View {
    let state: LoadingState<T>
    let content: (T) -> Content

    var body: some View {
        switch state {
        case .idle:
            Color.clear
        case .loading:
            ProgressView()
        case .loaded(let data):
            content(data)
        case .error(let error):
            ErrorView(error: error)
        }
    }
}

enum LoadingState<T> {
    case idle
    case loading
    case loaded(T)
    case error(Error)
}

// Usage
struct UserProfileView: View {
    @State private var state: LoadingState<User> = .idle

    var body: some View {
        LoadingView(state: state) { user in
            ProfileContent(user: user)
        }
        .task {
            state = .loading
            do {
                let user = try await fetchUser()
                state = .loaded(user)
            } catch {
                state = .error(error)
            }
        }
    }
}
```

---

## State Management Patterns

### Single Source of Truth

```swift
@Observable
class AppState {
    var user: User?
    var settings: Settings
    var notifications: [Notification]

    static let shared = AppState()

    private init() {
        self.settings = Settings()
        self.notifications = []
    }
}

// Inject at root
@main
struct MyApp: App {
    @State private var appState = AppState.shared

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(appState)
        }
    }
}
```

### Feature-Based State

```swift
// Each feature has its own state
@Observable
class NotesFeature {
    var notes: [Note] = []
    var selectedNote: Note?
    var searchQuery = ""

    func loadNotes() async { }
    func createNote() -> Note { }
    func deleteNote(_ note: Note) { }
}

@Observable
class SettingsFeature {
    var appearance: Appearance = .system
    var notifications: NotificationSettings = .default

    func save() async { }
    func reset() { }
}

// Compose features
@Observable
class AppFeatures {
    let notes = NotesFeature()
    let settings = SettingsFeature()
}
```

### Action-Based Updates

```swift
@Observable
class Store {
    private(set) var state: AppState

    init(initialState: AppState = .init()) {
        self.state = initialState
    }

    func dispatch(_ action: Action) {
        state = reduce(state, action)
    }

    private func reduce(_ state: AppState, _ action: Action) -> AppState {
        var newState = state

        switch action {
        case .addItem(let item):
            newState.items.append(item)
        case .removeItem(let id):
            newState.items.removeAll { $0.id == id }
        case .updateItem(let item):
            if let index = newState.items.firstIndex(where: { $0.id == item.id }) {
                newState.items[index] = item
            }
        }

        return newState
    }
}

enum Action {
    case addItem(Item)
    case removeItem(UUID)
    case updateItem(Item)
}
```

---

## Dependency Injection

### Environment-Based DI

```swift
// Protocol for abstraction
protocol DataServiceProtocol {
    func fetchItems() async throws -> [Item]
}

// Production implementation
class DataService: DataServiceProtocol {
    func fetchItems() async throws -> [Item] {
        // Real network call
    }
}

// Mock for testing/previews
class MockDataService: DataServiceProtocol {
    func fetchItems() async throws -> [Item] {
        [Item(name: "Mock 1"), Item(name: "Mock 2")]
    }
}

// Environment key
struct DataServiceKey: EnvironmentKey {
    static let defaultValue: DataServiceProtocol = DataService()
}

extension EnvironmentValues {
    var dataService: DataServiceProtocol {
        get { self[DataServiceKey.self] }
        set { self[DataServiceKey.self] = newValue }
    }
}

// Usage in views
struct ItemListView: View {
    @Environment(\.dataService) var dataService
    @State private var items: [Item] = []

    var body: some View {
        List(items) { item in
            Text(item.name)
        }
        .task {
            items = try? await dataService.fetchItems() ?? []
        }
    }
}

// Preview with mock
#Preview {
    ItemListView()
        .environment(\.dataService, MockDataService())
}
```

### Constructor Injection

```swift
@Observable
class ItemViewModel {
    private let service: DataServiceProtocol
    var items: [Item] = []

    init(service: DataServiceProtocol = DataService()) {
        self.service = service
    }

    func load() async {
        items = (try? await service.fetchItems()) ?? []
    }
}
```

---

## Navigation Patterns

### Coordinator Pattern

```swift
@Observable
class AppCoordinator {
    var path = NavigationPath()

    func showDetail(for item: Item) {
        path.append(item)
    }

    func showSettings() {
        path.append(Route.settings)
    }

    func pop() {
        path.removeLast()
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}

enum Route: Hashable {
    case settings
    case profile(userId: String)
}

struct CoordinatedApp: View {
    @State private var coordinator = AppCoordinator()

    var body: some View {
        NavigationStack(path: $coordinator.path) {
            HomeView()
                .navigationDestination(for: Item.self) { item in
                    ItemDetailView(item: item)
                }
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .settings:
                        SettingsView()
                    case .profile(let userId):
                        ProfileView(userId: userId)
                    }
                }
        }
        .environment(coordinator)
    }
}
```

---

## Best Practices

1. **Start Simple** - Use MV pattern first, add ViewModel when needed
2. **Prefer @Observable** - Over @ObservableObject for new code
3. **Extract Early** - Break views at 50-100 lines
4. **Single Responsibility** - Each view does one thing
5. **Testable Design** - Use protocols for dependencies
6. **Environment for Shared State** - Pass global state via environment
7. **Local State is Fine** - Not everything needs to be in a store

---

## Official Resources

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Observation Framework](https://developer.apple.com/documentation/observation)
- [WWDC23: Discover Observation in SwiftUI](https://developer.apple.com/videos/play/wwdc2023/10149/)
- [Managing model data in your app](https://developer.apple.com/documentation/swiftui/managing-model-data-in-your-app)
