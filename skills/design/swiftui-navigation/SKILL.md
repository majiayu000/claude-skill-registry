---
name: swiftui-navigation
description: Implement SwiftUI navigation with NavigationStack, NavigationSplitView, deep linking, and programmatic routing. Use when building navigation flows, handling deep links, implementing tab bars, or creating multi-column layouts.
user-invocable: false
---

# SwiftUI Navigation

## NavigationStack (iOS 16+)

```swift
// Type-safe routing with enum
enum AppRoute: Hashable, Codable {
    case home
    case profile(userId: String)
    case settings
    case detail(item: Item)
}

struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: AppRoute.self) { route in
                    destinationView(for: route)
                }
        }
    }

    @ViewBuilder
    private func destinationView(for route: AppRoute) -> some View {
        switch route {
        case .home: HomeView()
        case .profile(let id): ProfileView(userId: id)
        case .settings: SettingsView()
        case .detail(let item): DetailView(item: item)
        }
    }

    // Programmatic navigation
    func navigateTo(_ route: AppRoute) {
        path.append(route)
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}
```

## Deep Linking

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path)
            .onOpenURL { url in
                handleDeepLink(url)
            }
    }

    private func handleDeepLink(_ url: URL) {
        guard let routes = DeepLinkParser.parse(url) else { return }
        path = NavigationPath()
        for route in routes {
            path.append(route)
        }
    }
}

struct DeepLinkParser {
    static func parse(_ url: URL) -> [AppRoute]? {
        guard url.scheme == "myapp" else { return nil }

        switch url.host {
        case "profile":
            let id = url.pathComponents.dropFirst().first ?? ""
            return [.profile(userId: id)]
        case "settings":
            return [.settings]
        default:
            return nil
        }
    }
}
```

## NavigationSplitView (iPad/Mac)

```swift
struct MainView: View {
    @State private var selectedItem: Item?
    @State private var visibility = NavigationSplitViewVisibility.all

    var body: some View {
        NavigationSplitView(columnVisibility: $visibility) {
            // Sidebar
            List(items, selection: $selectedItem) { item in
                NavigationLink(value: item) {
                    Label(item.name, systemImage: item.icon)
                }
            }
            .navigationTitle("Items")
        } detail: {
            // Detail
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView("Select an item",
                    systemImage: "sidebar.left")
            }
        }
    }
}
```

## TabView

```swift
struct MainTabView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem { Label("Home", systemImage: "house") }
                .tag(0)

            SearchView()
                .tabItem { Label("Search", systemImage: "magnifyingglass") }
                .tag(1)

            ProfileView()
                .tabItem { Label("Profile", systemImage: "person") }
                .tag(2)
        }
    }
}
```
