---
name: swift
description: Write Swift code for iOS/macOS following best practices. Use when developing with SwiftUI, UIKit, or Swift packages. Covers type safety, concurrency, and tooling.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Swift / iOS Development

## Project Setup

### Swift Package Manager
```bash
# Initialize new package
swift package init --type executable

# Add dependencies to Package.swift
# swift package update
```

### Package.swift
```swift
// swift-tools-version: 5.10
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [.iOS(.v17), .macOS(.v14)],
    products: [
        .library(name: "MyApp", targets: ["MyApp"]),
    ],
    dependencies: [
        // Add dependencies here
    ],
    targets: [
        .target(name: "MyApp", dependencies: []),
        .testTarget(name: "MyAppTests", dependencies: ["MyApp"]),
    ]
)
```

### Xcode Project
```bash
# Create new Xcode project via Xcode or:
# Use SwiftUI App template for new projects
# Target iOS 17+ for latest APIs
```

## Type Patterns

### Optionals
```swift
// Safe unwrapping
if let user = optionalUser {
    print(user.name)
}

// Guard for early exit
guard let user = optionalUser else {
    return
}

// Optional chaining
let name = user?.profile?.displayName ?? "Anonymous"

// Nil coalescing
let displayName = user?.name ?? "Guest"
```

### Result Type
```swift
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed
}

func fetchUser(id: String) async -> Result<User, NetworkError> {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        return .failure(.invalidURL)
    }

    do {
        let (data, _) = try await URLSession.shared.data(from: url)
        let user = try JSONDecoder().decode(User.self, from: data)
        return .success(user)
    } catch {
        return .failure(.decodingFailed)
    }
}

// Usage
switch await fetchUser(id: "123") {
case .success(let user):
    print("Got user: \(user.name)")
case .failure(let error):
    print("Error: \(error)")
}
```

### Protocols & Extensions
```swift
protocol Identifiable {
    var id: UUID { get }
}

protocol Displayable {
    var displayName: String { get }
}

extension User: Identifiable, Displayable {
    var displayName: String {
        "\(firstName) \(lastName)"
    }
}
```

## Error Handling

```swift
// Throwing functions
func loadConfig() throws -> Config {
    guard let data = FileManager.default.contents(atPath: configPath) else {
        throw ConfigError.fileNotFound
    }
    return try JSONDecoder().decode(Config.self, from: data)
}

// Do-catch
do {
    let config = try loadConfig()
    print(config)
} catch ConfigError.fileNotFound {
    print("Config file missing")
} catch {
    print("Unknown error: \(error)")
}

// Try? for optional result
let config = try? loadConfig()

// Try! only when failure is impossible
let bundledConfig = try! loadBundledConfig()
```

## Async/Await Patterns

### Basic Async
```swift
func fetchUsers() async throws -> [User] {
    let (data, _) = try await URLSession.shared.data(from: usersURL)
    return try JSONDecoder().decode([User].self, from: data)
}

// Calling async functions
Task {
    do {
        let users = try await fetchUsers()
        await MainActor.run {
            self.users = users
        }
    } catch {
        print("Failed: \(error)")
    }
}
```

### Structured Concurrency
```swift
// Parallel execution
async let users = fetchUsers()
async let posts = fetchPosts()
let (userList, postList) = try await (users, posts)

// Task groups
func fetchAllUserData(ids: [String]) async throws -> [UserData] {
    try await withThrowingTaskGroup(of: UserData.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUserData(id: id)
            }
        }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}
```

### Actors
```swift
actor UserCache {
    private var cache: [String: User] = [:]

    func get(_ id: String) -> User? {
        cache[id]
    }

    func set(_ user: User) {
        cache[user.id] = user
    }
}

// Usage
let cache = UserCache()
await cache.set(user)
let cached = await cache.get("123")
```

## SwiftUI Patterns

### View with State
```swift
struct ContentView: View {
    @State private var count = 0
    @State private var username = ""

    var body: some View {
        VStack(spacing: 16) {
            Text("Count: \(count)")
                .font(.title)

            Button("Increment") {
                count += 1
            }

            TextField("Username", text: $username)
                .textFieldStyle(.roundedBorder)
        }
        .padding()
    }
}
```

### Observable ViewModel
```swift
@Observable
class UserViewModel {
    var users: [User] = []
    var isLoading = false
    var error: Error?

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            users = try await userService.fetchAll()
        } catch {
            self.error = error
        }
    }
}

struct UserListView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        List(viewModel.users) { user in
            UserRow(user: user)
        }
        .task {
            await viewModel.loadUsers()
        }
        .overlay {
            if viewModel.isLoading {
                ProgressView()
            }
        }
    }
}
```

### Environment & Dependency Injection
```swift
// Define environment key
struct UserServiceKey: EnvironmentKey {
    static let defaultValue: UserService = .live
}

extension EnvironmentValues {
    var userService: UserService {
        get { self[UserServiceKey.self] }
        set { self[UserServiceKey.self] = newValue }
    }
}

// Use in view
struct ProfileView: View {
    @Environment(\.userService) private var userService

    var body: some View {
        // Use userService
    }
}
```

## Testing

### Swift Testing (Swift 6+)
```swift
import Testing

@Suite("UserService Tests")
struct UserServiceTests {
    let service = UserService()

    @Test("creates user with valid email")
    func createUser() async throws {
        let user = try await service.create(email: "test@example.com")
        #expect(user.email == "test@example.com")
    }

    @Test("throws on invalid email")
    func invalidEmail() async {
        await #expect(throws: ValidationError.self) {
            try await service.create(email: "invalid")
        }
    }

    @Test("fetches user by ID", arguments: ["user1", "user2", "user3"])
    func fetchUser(id: String) async throws {
        let user = try await service.fetch(id: id)
        #expect(user.id == id)
    }
}
```

### XCTest (Legacy)
```swift
import XCTest
@testable import MyApp

final class UserServiceTests: XCTestCase {
    var service: UserService!

    override func setUp() {
        super.setUp()
        service = UserService()
    }

    func testCreateUser() async throws {
        let user = try await service.create(email: "test@example.com")
        XCTAssertEqual(user.email, "test@example.com")
    }

    func testInvalidEmailThrows() async {
        do {
            _ = try await service.create(email: "invalid")
            XCTFail("Expected error")
        } catch {
            XCTAssertTrue(error is ValidationError)
        }
    }
}
```

## Tooling

```bash
# SwiftLint (linting)
brew install swiftlint
swiftlint lint
swiftlint lint --fix

# SwiftFormat (formatting)
brew install swiftformat
swiftformat .
swiftformat . --lint

# Run tests
swift test
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'

# Build
swift build
xcodebuild build -scheme MyApp

# fastlane (CI/CD)
brew install fastlane
fastlane init
fastlane ios test
fastlane ios beta  # Deploy to TestFlight
```

### .swiftlint.yml
```yaml
disabled_rules:
  - trailing_whitespace
  - line_length

opt_in_rules:
  - empty_count
  - empty_string

excluded:
  - Pods
  - .build
```

### .swiftformat
```
--indent 4
--allman false
--wraparguments before-first
--wrapparameters before-first
--self remove
--importgrouping alphabetized
```
