---
name: swiftui
description: |
  SwiftUI framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with SwiftUI projects, or when the user mentions SwiftUI.
  Provides declarative UI patterns, state management, Combine, navigation, and accessibility guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: swift
  extensions: ".swift"
---

# SwiftUI Framework Guide

> Applies to: SwiftUI 5.0+ (iOS 17+, macOS 14+, watchOS 10+, tvOS 17+, visionOS 1.0+)
> Language Guide: @.claude/skills/swift-guide/SKILL.md

## Overview

SwiftUI is Apple's declarative UI framework for building native apps across all Apple platforms. It uses a reactive, data-driven approach where the UI automatically updates when state changes.

**Use SwiftUI when:**
- Building new Apple platform apps (iOS, macOS, watchOS, tvOS, visionOS)
- Cross-platform Apple development from a single codebase
- Declarative, reactive UI with minimal boilerplate
- Leveraging latest platform features (widgets, App Intents, Live Activities)

**Consider alternatives when:**
- Supporting iOS < 14 (use UIKit)
- Need fine-grained UIKit control (embed via `UIViewRepresentable`)
- Existing large UIKit codebase (migrate incrementally)

## Guardrails

### View Rules

- Keep views under 200 lines; decompose `body` into private computed properties at 30+ lines
- Use `// MARK: - Subviews` to group computed subview properties
- Prefer composition over deep nesting; extract reusable components as separate structs
- Never perform heavy computation inside `body` (use view models or `.task`)
- Mark subview properties as `private`; use `@ViewBuilder` for conditional helpers

### State Management Rules

- `@State`: View-local value-type state (booleans, strings, simple structs)
- `@Binding`: Two-way connection to parent state
- `@Observable` (iOS 17+): Preferred for view models; replaces ObservableObject
- `@StateObject`: Owned ObservableObject (iOS 14-16; created once, survives re-renders)
- `@ObservedObject`: Non-owned ObservableObject passed from parent
- `@EnvironmentObject` / `@Environment`: Shared state and system values
- Never use `@ObservedObject` for state the view owns
- Never create `@StateObject` in a computed property
- Never mutate state during a view update cycle

### Naming Conventions

- Screen views: `PascalCase` + `View` suffix (`ProfileView`, `SettingsView`)
- Reusable components: `PascalCase` without suffix (`StatCard`, `AvatarImage`)
- View modifiers: `camelCase` (`cardStyle()`, `loading(_:)`)
- View models: `PascalCase` descriptive name (`UserViewModel`, `AuthManager`)

### Performance Rules

- Use `LazyVStack`/`LazyHStack` for scrollable lists, `LazyVGrid`/`LazyHGrid` for grids
- Use `.task` for async data loading (auto-cancels on disappear)
- Avoid `AnyView` type erasure; use `@ViewBuilder` or `Group` instead
- Use `AsyncImage` with placeholder and error states for remote images
- Use `Equatable` conformance with `.equatable()` for expensive views

## Project Structure

```
MyApp/
├── MyApp/
│   ├── App/
│   │   └── MyApp.swift              # @main entry point
│   ├── Features/
│   │   ├── Authentication/
│   │   │   ├── Views/               # LoginView.swift, SignUpView.swift
│   │   │   ├── ViewModels/          # AuthViewModel.swift
│   │   │   └── Models/              # User.swift
│   │   ├── Home/
│   │   │   ├── Views/ | ViewModels/ | Components/
│   │   └── Settings/
│   ├── Core/
│   │   ├── Network/                 # APIClient.swift, Endpoints.swift
│   │   ├── Storage/
│   │   └── Extensions/              # View+Extensions.swift
│   ├── Shared/
│   │   ├── Components/              # LoadingView, ErrorView, PrimaryButton
│   │   └── Modifiers/               # CardModifier.swift
│   ├── Resources/                   # Assets.xcassets, Localizable.strings
│   └── Preview Content/
├── MyAppTests/
└── MyAppUITests/
```

- `Features/` groups by domain with Views, ViewModels, Models, Components
- `Shared/` for cross-feature reusable views and custom modifiers
- `Core/` for non-UI infrastructure (networking, storage, extensions)

## App Entry Point

```swift
@main
struct MyApp: App {
    @State private var appState = AppState()
    @State private var authManager = AuthManager()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(appState)
                .environment(authManager)
        }
    }
}

struct ContentView: View {
    @Environment(AuthManager.self) private var authManager

    var body: some View {
        Group {
            if authManager.isAuthenticated { MainTabView() }
            else { AuthenticationView() }
        }
        .animation(.easeInOut, value: authManager.isAuthenticated)
    }
}
```

Use `@Environment(\.scenePhase)` with `.onChange(of:)` for active/inactive/background transitions.

## View Composition

Decompose views with computed properties; extract reusable pieces as separate structs.

```swift
struct UserProfileView: View {
    let user: User
    @State private var isEditing = false

    var body: some View {
        VStack(spacing: 16) { profileHeader; statsSection; actionButtons }
            .padding()
            .navigationTitle("Profile")
            .sheet(isPresented: $isEditing) { EditProfileView(user: user) }
    }

    // MARK: - Subviews
    private var profileHeader: some View {
        VStack(spacing: 8) {
            AsyncImage(url: URL(string: user.avatarURL)) { image in
                image.resizable().aspectRatio(contentMode: .fill)
            } placeholder: { Circle().fill(Color.gray.opacity(0.3)) }
            .frame(width: 100, height: 100).clipShape(Circle())
            Text(user.name).font(.title2).fontWeight(.semibold)
            Text(user.email).font(.subheadline).foregroundStyle(.secondary)
        }
    }

    private var statsSection: some View {
        HStack(spacing: 32) {
            StatView(title: "Posts", value: user.postCount)
            StatView(title: "Followers", value: user.followerCount)
        }.padding(.vertical)
    }

    private var actionButtons: some View {
        HStack(spacing: 16) {
            Button("Edit Profile") { isEditing = true }.buttonStyle(.borderedProminent)
            Button("Share") { }.buttonStyle(.bordered)
        }
    }
}
```

### Custom View Modifiers

```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 4)
    }
}

extension View {
    func cardStyle() -> some View { modifier(CardModifier()) }
    func loading(_ isLoading: Bool) -> some View { modifier(LoadingModifier(isLoading: isLoading)) }
}
```

## State Management with @Observable

```swift
@Observable
final class UserViewModel {
    var user: User?
    var isLoading = false
    var errorMessage: String?
    private let userService: UserServiceProtocol

    init(userService: UserServiceProtocol = UserService()) {
        self.userService = userService
    }

    func loadUser(id: String) async {
        isLoading = true; errorMessage = nil
        do { user = try await userService.fetchUser(id: id) }
        catch { errorMessage = error.localizedDescription }
        isLoading = false
    }
}

struct UserView: View {
    @State private var viewModel = UserViewModel()
    let userId: String

    var body: some View {
        Group {
            if viewModel.isLoading { ProgressView() }
            else if let user = viewModel.user { UserProfileView(user: user) }
            else if let error = viewModel.errorMessage {
                ErrorView(message: error) { Task { await viewModel.loadUser(id: userId) } }
            }
        }
        .task { await viewModel.loadUser(id: userId) }
    }
}
```

### Environment-Based Dependency Injection

```swift
struct APIClientKey: EnvironmentKey {
    static let defaultValue: APIClientProtocol = APIClient()
}
extension EnvironmentValues {
    var apiClient: APIClientProtocol {
        get { self[APIClientKey.self] }
        set { self[APIClientKey.self] = newValue }
    }
}

// Usage
struct PostListView: View {
    @Environment(\.apiClient) private var apiClient
    @State private var posts: [Post] = []
    var body: some View {
        List(posts) { post in PostRowView(post: post) }
            .task { posts = (try? await apiClient.fetchPosts()) ?? [] }
    }
}

// Mock in previews
#Preview { PostListView().environment(\.apiClient, MockAPIClient()) }
```

## Navigation

### NavigationStack with Typed Routes

```swift
enum Route: Hashable {
    case settings
    case profile(userId: String)
    case notifications
}

struct MainView: View {
    @State private var navigationPath = NavigationPath()

    var body: some View {
        NavigationStack(path: $navigationPath) {
            HomeView(navigationPath: $navigationPath)
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .settings: SettingsView()
                    case .profile(let id): ProfileView(userId: id)
                    case .notifications: NotificationsView()
                    }
                }
        }
    }
}
```

### TabView with NavigationStack per Tab

```swift
struct MainTabView: View {
    @State private var selectedTab = Tab.home

    enum Tab: String, CaseIterable {
        case home, search, profile
        var icon: String {
            switch self { case .home: "house"; case .search: "magnifyingglass"; case .profile: "person" }
        }
        var title: String { rawValue.capitalized }
    }

    var body: some View {
        TabView(selection: $selectedTab) {
            ForEach(Tab.allCases, id: \.self) { tab in
                NavigationStack { tabContent(for: tab) }
                    .tabItem { Label(tab.title, systemImage: tab.icon) }
                    .tag(tab)
            }
        }
    }

    @ViewBuilder
    private func tabContent(for tab: Tab) -> some View {
        switch tab { case .home: HomeView(); case .search: SearchView(); case .profile: ProfileView() }
    }
}
```

## Lists and Grids

```swift
struct PostListView: View {
    @State private var posts: [Post] = []
    @State private var searchText = ""

    var filteredPosts: [Post] {
        guard !searchText.isEmpty else { return posts }
        return posts.filter { $0.title.localizedCaseInsensitiveContains(searchText) }
    }

    var body: some View {
        List {
            ForEach(filteredPosts) { post in
                PostRowView(post: post)
                    .swipeActions(edge: .trailing) {
                        Button(role: .destructive) { deletePost(post) } label: {
                            Label("Delete", systemImage: "trash")
                        }
                    }
            }
        }
        .searchable(text: $searchText, prompt: "Search posts")
        .refreshable { await loadPosts() }
        .overlay {
            if filteredPosts.isEmpty { ContentUnavailableView.search(text: searchText) }
        }
        .task { await loadPosts() }
    }

    private func loadPosts() async { /* fetch */ }
    private func deletePost(_ post: Post) { posts.removeAll { $0.id == post.id } }
}
```

For photo grids, use `LazyVGrid` with `GridItem(.adaptive(minimum:maximum:))`. See [references/patterns.md](references/patterns.md) for grid and horizontal scroll patterns.

## Forms

```swift
struct RegistrationView: View {
    @State private var form = RegistrationForm()
    @State private var isSubmitting = false

    var body: some View {
        Form {
            Section("Personal Information") {
                TextField("Full Name", text: $form.name).textContentType(.name)
                TextField("Email", text: $form.email).textContentType(.emailAddress).autocapitalization(.none)
            }
            Section("Account") {
                SecureField("Password", text: $form.password)
                SecureField("Confirm", text: $form.confirmPassword)
                if !form.passwordsMatch && !form.confirmPassword.isEmpty {
                    Text("Passwords do not match").font(.caption).foregroundStyle(.red)
                }
            }
            Section {
                Button("Create Account") { Task { await submit() } }
                    .disabled(!form.isValid || isSubmitting)
            }
        }
        .loading(isSubmitting)
    }

    private func submit() async { /* validate and submit */ }
}
```

## Previews

```swift
#Preview("User Profile") {
    NavigationStack { UserProfileView(user: .preview) }
}

#Preview("Dark Mode") {
    NavigationStack { UserProfileView(user: .preview) }.preferredColorScheme(.dark)
}

extension User {
    static var preview: User { User(id: "preview", name: "John Doe", email: "john@example.com") }
}
```

## Testing

### Standards

- Use `XCTest` for unit and UI tests
- Test view models with `async throws` test methods
- Use protocol-based mocks injected via initializers
- Coverage target: >80% for business logic, >60% overall
- Test names describe behavior: `test_loadUser_success_updatesUser()`

### View Model Test

```swift
final class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockService: MockUserService!

    override func setUp() {
        super.setUp(); mockService = MockUserService()
        sut = UserViewModel(userService: mockService)
    }

    func test_loadUser_success_updatesUser() async {
        mockService.userToReturn = User(id: "1", name: "John")
        await sut.loadUser(id: "1")
        XCTAssertEqual(sut.user?.name, "John")
        XCTAssertFalse(sut.isLoading)
    }

    func test_loadUser_failure_setsErrorMessage() async {
        mockService.errorToThrow = APIError.invalidResponse
        await sut.loadUser(id: "1")
        XCTAssertNil(sut.user)
        XCTAssertNotNil(sut.errorMessage)
    }
}
```

## Commands Reference

```bash
xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'  # Build
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'  # Test
swift build                          # SPM build
swift test                           # SPM test
swift format .                       # Format
swiftlint                            # Lint
swiftlint --fix                      # Auto-fix
```

## Best Practices

**Do:** Decompose views with computed properties | Use `@Observable` (iOS 17+) | Inject via `@Environment` | Use `.task` for async | Use `NavigationStack` with typed routes | Provide multiple `#Preview` configs | Use `LazyVStack`/`LazyHStack` for scrollable content

**Don't:** Mutate state during view updates | Create `@StateObject` in computed properties | Use `@ObservedObject` for owned state | Put heavy computation in `body` | Force-unwrap outside tests | Use `AnyView` (use `@ViewBuilder`) | Nest views 4+ levels deep without extraction

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Animation, Combine, Core Data/SwiftData, accessibility, platform adaptations, networking, ObservableObject migration, advanced testing

## External References

- [SwiftUI Documentation](https://developer.apple.com/documentation/swiftui)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [SwiftUI by Example](https://www.hackingwithswift.com/quick-start/swiftui)
- [WWDC SwiftUI Sessions](https://developer.apple.com/videos/swiftui)
