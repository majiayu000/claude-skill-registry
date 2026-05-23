---
name: navigation-menus
description: Modern SwiftUI navigation patterns, NavigationStack, NavigationSplitView, TabView, toolbars, context menus, and router patterns. Use when user asks about navigation, NavigationStack, TabView, menus, toolbars, routing, or deep linking.
allowed-tools: Bash, Read, Write, Edit
---

# SwiftUI Navigation and Menus

Comprehensive guide to modern SwiftUI navigation patterns, menus, toolbars, and routing for iOS 26 and macOS Tahoe development.

## Prerequisites

- iOS 16+ for NavigationStack (iOS 26 recommended)
- Xcode 26+

---

## NavigationStack (iOS 16+)

### Basic NavigationStack

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.title) {
                    ItemDetailView(item: item)
                }
            }
            .navigationTitle("Items")
        }
    }
}
```

### Programmatic Navigation with NavigationPath

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                Button(item.title) {
                    path.append(item)  // Push programmatically
                }
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
            }
            .navigationTitle("Items")
            .toolbar {
                Button("Go to Settings") {
                    path.append(Route.settings)
                }
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
    }
}

enum Route: Hashable {
    case settings
    case profile(userId: String)
}
```

### Navigation Path Operations

```swift
// Push a single value
path.append(item)

// Pop one view
path.removeLast()

// Pop multiple views
path.removeLast(2)

// Pop to root
path.removeLast(path.count)

// Clear and push new
path = NavigationPath()
path.append(newRoot)

// Check if empty
if path.isEmpty {
    // At root
}
```

### Type-Safe Navigation with Codable

```swift
struct ContentView: View {
    // Codable path for state restoration
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            RootView()
                .navigationDestination(for: Note.self) { note in
                    NoteDetailView(note: note)
                }
                .navigationDestination(for: Folder.self) { folder in
                    FolderView(folder: folder)
                }
        }
        .onAppear {
            restoreNavigationPath()
        }
        .onChange(of: path) {
            saveNavigationPath()
        }
    }

    func saveNavigationPath() {
        guard let data = try? JSONEncoder().encode(path.codable) else { return }
        UserDefaults.standard.set(data, forKey: "navigationPath")
    }

    func restoreNavigationPath() {
        guard let data = UserDefaults.standard.data(forKey: "navigationPath"),
              let codable = try? JSONDecoder().decode(
                NavigationPath.CodableRepresentation.self,
                from: data
              ) else { return }
        path = NavigationPath(codable)
    }
}
```

---

## NavigationSplitView

### Two-Column Layout

```swift
struct TwoColumnView: View {
    @State private var selectedNote: Note?

    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(notes, selection: $selectedNote) { note in
                NavigationLink(value: note) {
                    NoteRow(note: note)
                }
            }
            .navigationTitle("Notes")
        } detail: {
            // Detail
            if let note = selectedNote {
                NoteDetailView(note: note)
            } else {
                ContentUnavailableView(
                    "Select a Note",
                    systemImage: "doc.text",
                    description: Text("Choose a note from the sidebar")
                )
            }
        }
    }
}
```

### Three-Column Layout

```swift
struct ThreeColumnView: View {
    @State private var selectedFolder: Folder?
    @State private var selectedNote: Note?

    var body: some View {
        NavigationSplitView {
            // Sidebar
            List(folders, selection: $selectedFolder) { folder in
                NavigationLink(value: folder) {
                    Label(folder.name, systemImage: "folder")
                }
            }
            .navigationTitle("Folders")
        } content: {
            // Content column
            if let folder = selectedFolder {
                List(folder.notes, selection: $selectedNote) { note in
                    NavigationLink(value: note) {
                        Text(note.title)
                    }
                }
                .navigationTitle(folder.name)
            } else {
                ContentUnavailableView("Select a Folder", systemImage: "folder")
            }
        } detail: {
            // Detail column
            if let note = selectedNote {
                NoteDetailView(note: note)
            } else {
                ContentUnavailableView("Select a Note", systemImage: "doc.text")
            }
        }
    }
}
```

### Column Visibility Control

```swift
struct AdaptiveNavigationView: View {
    @State private var columnVisibility: NavigationSplitViewVisibility = .all
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            SidebarView(selection: $selectedItem)
        } detail: {
            DetailView(item: selectedItem)
        }
        .navigationSplitViewStyle(.balanced)  // or .prominentDetail
    }
}

// Visibility options:
// .all - Show all columns
// .doubleColumn - Hide sidebar
// .detailOnly - Show only detail
// .automatic - System decides
```

### NavigationSplitView in Portrait

On iPhone and narrow iPad, NavigationSplitView automatically collapses to NavigationStack behavior with a back button.

```swift
NavigationSplitView {
    SidebarView()
} detail: {
    DetailView()
}
.navigationSplitViewStyle(.balanced)

// Style options:
// .automatic - System decides
// .balanced - Equal column importance
// .prominentDetail - Detail takes priority
```

---

## TabView

### Basic TabView

```swift
struct MainTabView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)

            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(1)

            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
                .tag(2)
        }
    }
}
```

### Tab with Badge

```swift
TabView {
    NotificationsView()
        .tabItem {
            Label("Notifications", systemImage: "bell")
        }
        .badge(unreadCount)  // Shows badge number
        .badge("New")        // Shows text badge
}
```

### iOS 26 Search Tab Role

```swift
TabView {
    HomeView()
        .tabItem {
            Label("Home", systemImage: "house")
        }

    // Search tab morphs into search field when tapped
    SearchResultsView()
        .tabItem {
            Label("Search", systemImage: "magnifyingglass")
        }
        .tabItemRole(.search)  // iOS 26 - Morphs to search field
}
```

### TabView with NavigationStack

Each tab should have its own NavigationStack:

```swift
struct MainTabView: View {
    @State private var selectedTab = 0
    @State private var homePath = NavigationPath()
    @State private var searchPath = NavigationPath()

    var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack(path: $homePath) {
                HomeView()
                    .navigationDestination(for: Item.self) { item in
                        ItemDetailView(item: item)
                    }
            }
            .tabItem {
                Label("Home", systemImage: "house")
            }
            .tag(0)

            NavigationStack(path: $searchPath) {
                SearchView()
                    .navigationDestination(for: SearchResult.self) { result in
                        SearchResultDetailView(result: result)
                    }
            }
            .tabItem {
                Label("Search", systemImage: "magnifyingglass")
            }
            .tag(1)
        }
    }
}
```

### Programmatic Tab Switching

```swift
struct TabCoordinator: View {
    @State private var selectedTab = Tab.home

    enum Tab: Hashable {
        case home, search, profile
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView(switchTab: { selectedTab = $0 })
                .tabItem { Label("Home", systemImage: "house") }
                .tag(Tab.home)

            SearchView()
                .tabItem { Label("Search", systemImage: "magnifyingglass") }
                .tag(Tab.search)

            ProfileView()
                .tabItem { Label("Profile", systemImage: "person") }
                .tag(Tab.profile)
        }
    }
}
```

---

## Toolbars

### Basic Toolbar

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            ContentList()
                .navigationTitle("Items")
                .toolbar {
                    Button("Add", systemImage: "plus") {
                        addItem()
                    }
                }
        }
    }
}
```

### Toolbar Placements

```swift
.toolbar {
    // Leading position (left on LTR)
    ToolbarItem(placement: .topBarLeading) {
        Button("Edit") { }
    }

    // Trailing position (right on LTR)
    ToolbarItem(placement: .topBarTrailing) {
        Button("Done") { }
    }

    // Primary action (system decides best position)
    ToolbarItem(placement: .primaryAction) {
        Button("Save") { }
    }

    // Secondary action
    ToolbarItem(placement: .secondaryAction) {
        Button("Settings") { }
    }

    // Cancel/dismiss action
    ToolbarItem(placement: .cancellationAction) {
        Button("Cancel") { }
    }

    // Confirmation action
    ToolbarItem(placement: .confirmationAction) {
        Button("Confirm") { }
    }

    // Destructive action
    ToolbarItem(placement: .destructiveAction) {
        Button("Delete", role: .destructive) { }
    }

    // Bottom bar
    ToolbarItem(placement: .bottomBar) {
        Button("Action") { }
    }
}
```

### ToolbarItemGroup

```swift
.toolbar {
    ToolbarItemGroup(placement: .topBarTrailing) {
        Button("Share", systemImage: "square.and.arrow.up") { }
        Button("More", systemImage: "ellipsis.circle") { }
    }
}
```

### iOS 26 ToolbarSpacer

```swift
.toolbar {
    ToolbarItem(placement: .topBarTrailing) {
        Button("Edit") { }
    }

    // Fixed spacer - groups related items
    ToolbarSpacer(.fixed)

    ToolbarItem(placement: .topBarTrailing) {
        Button("Add", systemImage: "plus") { }
    }

    // Flexible spacer - expands
    ToolbarSpacer(.flexible)

    ToolbarItem(placement: .topBarTrailing) {
        Button("Settings", systemImage: "gear") { }
    }
}
```

### iOS 26 Close Button Role

```swift
.toolbar {
    ToolbarItem(placement: .cancellationAction) {
        Button("Dismiss", role: .close) {
            dismiss()
        }
        // Renders as glass X button in iOS 26
    }
}
```

### Toolbar Background with Liquid Glass

```swift
.toolbarBackgroundVisibility(.visible, for: .navigationBar)
.toolbarBackground(.ultraThinMaterial, for: .navigationBar)

// iOS 26 - Glass toolbar
.toolbarBackground(.glass, for: .navigationBar)
```

### Custom Toolbar Content

```swift
.toolbar {
    ToolbarItem(placement: .principal) {
        VStack {
            Text("Title")
                .font(.headline)
            Text("Subtitle")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }
}
```

---

## Context Menus

### Basic Context Menu

```swift
struct ItemRow: View {
    let item: Item

    var body: some View {
        Text(item.title)
            .contextMenu {
                Button("Copy") {
                    copyItem()
                }
                Button("Share") {
                    shareItem()
                }
                Divider()
                Button("Delete", role: .destructive) {
                    deleteItem()
                }
            }
    }
}
```

### Context Menu with Preview

```swift
Text(item.title)
    .contextMenu {
        Button("Open") { }
        Button("Share") { }
    } preview: {
        ItemPreviewView(item: item)
            .frame(width: 300, height: 200)
    }
```

### Conditional Menu Items

```swift
.contextMenu {
    if item.isFavorite {
        Button("Remove from Favorites") {
            toggleFavorite()
        }
    } else {
        Button("Add to Favorites") {
            toggleFavorite()
        }
    }

    if canEdit {
        Button("Edit") { }
    }
}
```

### Context Menu on Lists

```swift
List(items) { item in
    ItemRow(item: item)
        .contextMenu {
            Button("Edit") { editItem(item) }
            Button("Delete", role: .destructive) { deleteItem(item) }
        }
}
```

---

## Menus

### Menu Button

```swift
Menu {
    Button("Option 1") { }
    Button("Option 2") { }
    Button("Option 3") { }
} label: {
    Label("Menu", systemImage: "ellipsis.circle")
}
```

### Nested Menus

```swift
Menu {
    Button("Quick Action") { }

    Menu("Sort By") {
        Button("Name") { }
        Button("Date") { }
        Button("Size") { }
    }

    Menu("Filter") {
        Button("All") { }
        Button("Recent") { }
        Button("Favorites") { }
    }

    Divider()

    Button("Settings") { }
} label: {
    Image(systemName: "ellipsis.circle")
}
```

### Menu with Selection

```swift
@State private var sortOrder = SortOrder.name

Menu {
    Picker("Sort", selection: $sortOrder) {
        ForEach(SortOrder.allCases) { order in
            Text(order.displayName).tag(order)
        }
    }
} label: {
    Label("Sort", systemImage: "arrow.up.arrow.down")
}
```

### Primary Action Menu

```swift
Menu {
    Button("Edit") { }
    Button("Duplicate") { }
    Button("Delete", role: .destructive) { }
} label: {
    Label("Actions", systemImage: "ellipsis.circle")
} primaryAction: {
    // Primary tap action
    openItem()
}
```

---

## iPad Menu Bar (iOS 26)

### Adding Commands

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            // File menu
            CommandGroup(replacing: .newItem) {
                Button("New Document") {
                    createNewDocument()
                }
                .keyboardShortcut("n", modifiers: .command)
            }

            // Edit menu additions
            CommandGroup(after: .pasteboard) {
                Button("Duplicate") {
                    duplicateSelected()
                }
                .keyboardShortcut("d", modifiers: .command)
            }

            // Custom menu
            CommandMenu("View") {
                Button("Show Sidebar") {
                    showSidebar()
                }
                .keyboardShortcut("s", modifiers: [.command, .control])

                Toggle("Dark Mode", isOn: $isDarkMode)
            }
        }
    }
}
```

### Command Groups

```swift
.commands {
    // Replace existing group
    CommandGroup(replacing: .help) {
        Button("My App Help") { }
    }

    // Add before group
    CommandGroup(before: .sidebar) {
        Button("Toggle Inspector") { }
    }

    // Add after group
    CommandGroup(after: .toolbar) {
        Divider()
        Button("Reset Layout") { }
    }
}
```

---

## Searchable

### Basic Search

```swift
struct SearchableView: View {
    @State private var searchText = ""

    var filteredItems: [Item] {
        if searchText.isEmpty {
            return items
        }
        return items.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        NavigationStack {
            List(filteredItems) { item in
                ItemRow(item: item)
            }
            .searchable(text: $searchText, prompt: "Search items")
            .navigationTitle("Items")
        }
    }
}
```

### Search with Suggestions

```swift
.searchable(text: $searchText) {
    ForEach(suggestions) { suggestion in
        Text(suggestion.title)
            .searchCompletion(suggestion.title)
    }
}
```

### Search Scopes

```swift
@State private var searchScope = SearchScope.all

.searchable(text: $searchText)
.searchScopes($searchScope) {
    Text("All").tag(SearchScope.all)
    Text("Recent").tag(SearchScope.recent)
    Text("Favorites").tag(SearchScope.favorites)
}
```

### iOS 26 Search Placement

```swift
// NavigationStack - search in navigation bar
NavigationStack {
    ContentView()
        .searchable(text: $searchText)
}

// NavigationSplitView - search in sidebar
NavigationSplitView {
    SidebarView()
        .searchable(text: $searchText)
} detail: {
    DetailView()
}
```

### Search Tokens

```swift
@State private var tokens: [SearchToken] = []

.searchable(text: $searchText, tokens: $tokens) { token in
    Label(token.name, systemImage: token.icon)
}
.searchSuggestions {
    ForEach(suggestedTokens) { token in
        Label(token.name, systemImage: token.icon)
            .searchCompletion(token)
    }
}
```

---

## Router/Coordinator Pattern

### Central App Router

```swift
@Observable
class AppRouter {
    var homePath = NavigationPath()
    var searchPath = NavigationPath()
    var profilePath = NavigationPath()

    var selectedTab: Tab = .home

    enum Tab: Hashable {
        case home, search, profile
    }

    // MARK: - Navigation Actions

    func navigateToItem(_ item: Item) {
        switch selectedTab {
        case .home:
            homePath.append(item)
        case .search:
            searchPath.append(item)
        case .profile:
            profilePath.append(item)
        }
    }

    func navigateToProfile(userId: String) {
        selectedTab = .profile
        profilePath.append(ProfileDestination.user(userId))
    }

    func popToRoot() {
        switch selectedTab {
        case .home:
            homePath.removeLast(homePath.count)
        case .search:
            searchPath.removeLast(searchPath.count)
        case .profile:
            profilePath.removeLast(profilePath.count)
        }
    }

    func pop() {
        switch selectedTab {
        case .home where !homePath.isEmpty:
            homePath.removeLast()
        case .search where !searchPath.isEmpty:
            searchPath.removeLast()
        case .profile where !profilePath.isEmpty:
            profilePath.removeLast()
        default:
            break
        }
    }
}
```

### Router Usage

```swift
@main
struct MyApp: App {
    @State private var router = AppRouter()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(router)
        }
    }
}

struct RootView: View {
    @Environment(AppRouter.self) var router

    var body: some View {
        @Bindable var router = router

        TabView(selection: $router.selectedTab) {
            NavigationStack(path: $router.homePath) {
                HomeView()
                    .navigationDestination(for: Item.self) { item in
                        ItemDetailView(item: item)
                    }
            }
            .tabItem { Label("Home", systemImage: "house") }
            .tag(AppRouter.Tab.home)

            NavigationStack(path: $router.searchPath) {
                SearchView()
                    .navigationDestination(for: Item.self) { item in
                        ItemDetailView(item: item)
                    }
            }
            .tabItem { Label("Search", systemImage: "magnifyingglass") }
            .tag(AppRouter.Tab.search)

            NavigationStack(path: $router.profilePath) {
                ProfileView()
                    .navigationDestination(for: ProfileDestination.self) { dest in
                        ProfileDestinationView(destination: dest)
                    }
            }
            .tabItem { Label("Profile", systemImage: "person") }
            .tag(AppRouter.Tab.profile)
        }
    }
}
```

### Using Router in Child Views

```swift
struct ItemRow: View {
    @Environment(AppRouter.self) var router
    let item: Item

    var body: some View {
        Button(item.title) {
            router.navigateToItem(item)
        }
    }
}
```

---

## Deep Linking

### URL Handling

```swift
@main
struct MyApp: App {
    @State private var router = AppRouter()

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(router)
                .onOpenURL { url in
                    handleDeepLink(url)
                }
        }
    }

    func handleDeepLink(_ url: URL) {
        guard let components = URLComponents(url: url, resolvingAgainstBaseURL: true) else {
            return
        }

        // myapp://item/123
        // myapp://profile/user456

        let pathComponents = components.path.split(separator: "/")

        switch pathComponents.first {
        case "item":
            if let idString = pathComponents.dropFirst().first,
               let id = UUID(uuidString: String(idString)) {
                router.selectedTab = .home
                router.homePath.append(ItemDestination(id: id))
            }
        case "profile":
            if let userId = pathComponents.dropFirst().first {
                router.navigateToProfile(userId: String(userId))
            }
        default:
            break
        }
    }
}
```

### Universal Links

```swift
// In Info.plist, add Associated Domains capability
// applinks:yourdomain.com

// Handle in onOpenURL
.onOpenURL { url in
    // https://yourdomain.com/item/123
    if url.host == "yourdomain.com" {
        handleUniversalLink(url)
    }
}
```

---

## Sheets and Presentations

### Basic Sheet

```swift
struct ContentView: View {
    @State private var showingSheet = false

    var body: some View {
        Button("Show Sheet") {
            showingSheet = true
        }
        .sheet(isPresented: $showingSheet) {
            SheetContent()
        }
    }
}
```

### Sheet with Item

```swift
@State private var selectedItem: Item?

List(items) { item in
    Button(item.title) {
        selectedItem = item
    }
}
.sheet(item: $selectedItem) { item in
    ItemDetailSheet(item: item)
}
```

### Presentation Detents

```swift
.sheet(isPresented: $showingSheet) {
    SheetContent()
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
}

// Custom detent
.presentationDetents([
    .height(200),
    .fraction(0.4),
    .medium,
    .large
])
```

### Sheet Customization

```swift
.sheet(isPresented: $showingSheet) {
    SheetContent()
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
        .presentationCornerRadius(20)
        .presentationBackground(.thinMaterial)
        .presentationContentInteraction(.scrolls)
        .interactiveDismissDisabled(hasUnsavedChanges)
}
```

### Full Screen Cover

```swift
.fullScreenCover(isPresented: $showingFullScreen) {
    FullScreenView()
}
```

---

## Alerts and Confirmations

### Basic Alert

```swift
@State private var showingAlert = false

Button("Delete") {
    showingAlert = true
}
.alert("Delete Item?", isPresented: $showingAlert) {
    Button("Cancel", role: .cancel) { }
    Button("Delete", role: .destructive) {
        deleteItem()
    }
} message: {
    Text("This action cannot be undone.")
}
```

### Alert with Data

```swift
@State private var itemToDelete: Item?

.alert("Delete Item?", isPresented: .constant(itemToDelete != nil), presenting: itemToDelete) { item in
    Button("Cancel", role: .cancel) {
        itemToDelete = nil
    }
    Button("Delete", role: .destructive) {
        delete(item)
        itemToDelete = nil
    }
} message: { item in
    Text("Are you sure you want to delete \"\(item.title)\"?")
}
```

### Confirmation Dialog

```swift
@State private var showingConfirmation = false

.confirmationDialog("Choose Action", isPresented: $showingConfirmation) {
    Button("Share") { share() }
    Button("Duplicate") { duplicate() }
    Button("Delete", role: .destructive) { delete() }
    Button("Cancel", role: .cancel) { }
} message: {
    Text("What would you like to do with this item?")
}
```

---

## Best Practices

### 1. Place NavigationStack at Root

```swift
// GOOD: NavigationStack wraps content
NavigationStack {
    TabView {
        // Content
    }
}

// BETTER: Each tab has its own NavigationStack
TabView {
    NavigationStack {
        HomeView()
    }
    .tabItem { ... }
}
```

### 2. Use Type-Safe Navigation

```swift
// GOOD: Type-safe destinations
.navigationDestination(for: Item.self) { item in
    ItemDetailView(item: item)
}

// AVOID: String-based or untyped navigation
```

### 3. Keep Navigation State Observable

```swift
// Centralize navigation state
@Observable
class Router {
    var path = NavigationPath()
}

// Inject via environment
.environment(router)
```

### 4. Handle Empty States

```swift
NavigationSplitView {
    SidebarView()
} detail: {
    if let selected = selectedItem {
        DetailView(item: selected)
    } else {
        ContentUnavailableView(
            "No Selection",
            systemImage: "doc",
            description: Text("Select an item to view details")
        )
    }
}
```

### 5. Support Deep Linking

```swift
// Always handle URL schemes
.onOpenURL { url in
    handleDeepLink(url)
}
```

---

## Official Resources

- [NavigationStack Documentation](https://developer.apple.com/documentation/swiftui/navigationstack)
- [NavigationSplitView Documentation](https://developer.apple.com/documentation/swiftui/navigationsplitview)
- [TabView Documentation](https://developer.apple.com/documentation/swiftui/tabview)
- [WWDC22: The SwiftUI cookbook for navigation](https://developer.apple.com/videos/play/wwdc2022/10054/)
- [WWDC23: Bring your app to the new Navigation experience](https://developer.apple.com/videos/play/wwdc2023/10157/)
