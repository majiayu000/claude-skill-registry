---
name: swift-expert
version: 1.0.0
description: Expert-level Swift development for iOS, macOS with SwiftUI, Combine, and modern Swift 5.9+
category: languages
tags: [swift, ios, macos, swiftui, combine, async-await, apple]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(swift:*, xcodebuild:*)
---

# Swift Expert

Expert guidance for Swift development including iOS/macOS apps, SwiftUI, Combine, async/await, and Swift 5.9+ features.

## Core Concepts

### Modern Swift Features (5.9+)
- Async/await concurrency
- Actors for thread safety
- Property wrappers
- Result builders
- Protocols and generics
- Value types vs reference types
- Automatic Reference Counting (ARC)
- Macros (Swift 5.9+)

### SwiftUI
- Declarative UI framework
- State management
- View composition
- Layout system
- Animations
- Navigation

### Combine
- Reactive programming
- Publishers and subscribers
- Operators
- Error handling

## Swift Syntax

### Basics and Optionals
```swift
// Variables and constants
var mutableValue = 42
let constantValue = 100

// Optionals
var optionalName: String? = "Alice"

// Optional binding
if let name = optionalName {
    print("Hello, \(name)")
}

// Optional chaining
let length = optionalName?.count

// Nil coalescing
let displayName = optionalName ?? "Unknown"

// Guard statement
func greet(person: String?) {
    guard let name = person else {
        print("No name provided")
        return
    }
    print("Hello, \(name)")
}
```

### Functions and Closures
```swift
// Function with labeled parameters
func greet(person: String, from hometown: String) -> String {
    return "Hello \(person) from \(hometown)!"
}

// Closures
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }
let evens = numbers.filter { $0 % 2 == 0 }
let sum = numbers.reduce(0, +)

// Trailing closure
numbers.forEach { number in
    print(number)
}

// Capture values
func makeIncrementer(step: Int) -> () -> Int {
    var total = 0
    return {
        total += step
        return total
    }
}
```

### Structs and Classes
```swift
// Struct (value type, preferred)
struct User {
    let id: UUID
    var name: String
    var email: String

    // Computed property
    var displayName: String {
        name.isEmpty ? "Anonymous" : name
    }

    // Method
    mutating func updateEmail(_ newEmail: String) {
        email = newEmail
    }
}

// Class (reference type)
class ViewController {
    var title: String?
    weak var delegate: ViewControllerDelegate?

    init(title: String?) {
        self.title = title
    }

    deinit {
        print("Deallocated")
    }
}

// Protocol
protocol Identifiable {
    var id: UUID { get }
}

extension User: Identifiable {}
```

### Enums
```swift
// Simple enum
enum Direction {
    case north, south, east, west
}

// Associated values
enum Result<Success, Failure: Error> {
    case success(Success)
    case failure(Failure)
}

// Raw values
enum StatusCode: Int {
    case ok = 200
    case notFound = 404
    case serverError = 500
}

// Pattern matching
switch result {
case .success(let value):
    print("Success: \(value)")
case .failure(let error):
    print("Error: \(error)")
}
```

### Async/Await (Swift 5.5+)
```swift
// Async function
func fetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Call async function
Task {
    do {
        let user = try await fetchUser(id: "123")
        print(user.name)
    } catch {
        print("Error: \(error)")
    }
}

// Parallel execution with async let
func loadUserData(id: String) async throws -> (User, [Post], [Comment]) {
    async let user = fetchUser(id: id)
    async let posts = fetchPosts(userId: id)
    async let comments = fetchComments(userId: id)

    return try await (user, posts, comments)
}

// Task groups for dynamic parallelism
func fetchMultipleUsers(ids: [String]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }

        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}
```

### Actors (Thread Safety)
```swift
actor BankAccount {
    private var balance: Double = 0

    func deposit(amount: Double) {
        balance += amount
    }

    func withdraw(amount: Double) throws {
        guard balance >= amount else {
            throw BankError.insufficientFunds
        }
        balance -= amount
    }

    func getBalance() -> Double {
        balance
    }
}

// Usage (all access is async and serialized)
let account = BankAccount()
Task {
    await account.deposit(amount: 100)
    let balance = await account.getBalance()
    print(balance)
}
```

## SwiftUI

### Basic Views
```swift
import SwiftUI

struct ContentView: View {
    @State private var name = ""
    @State private var count = 0

    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, \(name.isEmpty ? "World" : name)!")
                .font(.title)
                .foregroundColor(.blue)

            TextField("Enter name", text: $name)
                .textFieldStyle(.roundedBorder)
                .padding()

            HStack {
                Button("Decrement") {
                    count -= 1
                }

                Text("\(count)")
                    .frame(minWidth: 50)

                Button("Increment") {
                    count += 1
                }
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}
```

### State Management
```swift
// @State - local view state
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        Button("Count: \(count)") {
            count += 1
        }
    }
}

// @Binding - pass state reference
struct ChildView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Setting", isOn: $isOn)
    }
}

// @ObservableObject - external state
class UserViewModel: ObservableObject {
    @Published var user: User?
    @Published var isLoading = false
    @Published var error: Error?

    func fetchUser() async {
        isLoading = true
        defer { isLoading = false }

        do {
            user = try await APIClient.shared.fetchUser()
        } catch {
            self.error = error
        }
    }
}

struct UserView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
            } else if let user = viewModel.user {
                UserDetailView(user: user)
            } else if let error = viewModel.error {
                ErrorView(error: error)
            }
        }
        .task {
            await viewModel.fetchUser()
        }
    }
}

// @EnvironmentObject - app-wide state
@main
struct MyApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
    }
}

struct SomeView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        Text(appState.currentUser?.name ?? "Guest")
    }
}
```

### Lists and Navigation
```swift
struct PostListView: View {
    let posts: [Post]
    @State private var selectedPost: Post?

    var body: some View {
        NavigationStack {
            List(posts) { post in
                NavigationLink(value: post) {
                    VStack(alignment: .leading) {
                        Text(post.title)
                            .font(.headline)
                        Text(post.excerpt)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                }
            }
            .navigationTitle("Posts")
            .navigationDestination(for: Post.self) { post in
                PostDetailView(post: post)
            }
        }
    }
}
```

### Custom Modifiers
```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color.white)
            .cornerRadius(10)
            .shadow(radius: 5)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}

// Usage
Text("Hello")
    .cardStyle()
```

## Networking

```swift
actor APIClient {
    static let shared = APIClient()

    private let baseURL = URL(string: "https://api.example.com")!
    private let decoder: JSONDecoder = {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return decoder
    }()

    func fetch<T: Decodable>(_ endpoint: String) async throws -> T {
        let url = baseURL.appendingPathComponent(endpoint)
        let (data, response) = try await URLSession.shared.data(from: url)

        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }

        return try decoder.decode(T.self, from: data)
    }

    func post<T: Encodable, R: Decodable>(
        _ endpoint: String,
        body: T
    ) async throws -> R {
        var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(body)

        let (data, _) = try await URLSession.shared.data(for: request)
        return try decoder.decode(R.self, from: data)
    }
}

enum APIError: LocalizedError {
    case invalidResponse
    case decodingError

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "Invalid server response"
        case .decodingError:
            return "Failed to decode response"
        }
    }
}
```

## Combine Framework

```swift
import Combine

class SearchViewModel: ObservableObject {
    @Published var searchText = ""
    @Published var results: [SearchResult] = []
    @Published var isLoading = false

    private var cancellables = Set<AnyCancellable>()

    init() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .sink { [weak self] text in
                self?.performSearch(text)
            }
            .store(in: &cancellables)
    }

    private func performSearch(_ text: String) {
        guard !text.isEmpty else {
            results = []
            return
        }

        isLoading = true

        Task {
            do {
                let searchResults: [SearchResult] = try await APIClient.shared
                    .fetch("search?q=\(text)")
                await MainActor.run {
                    self.results = searchResults
                    self.isLoading = false
                }
            } catch {
                await MainActor.run {
                    self.isLoading = false
                }
            }
        }
    }
}
```

## Testing

```swift
import XCTest
@testable import MyApp

final class UserViewModelTests: XCTestCase {
    var viewModel: UserViewModel!
    var mockAPIClient: MockAPIClient!

    override func setUp() {
        super.setUp()
        mockAPIClient = MockAPIClient()
        viewModel = UserViewModel(apiClient: mockAPIClient)
    }

    func testFetchUserSuccess() async throws {
        // Given
        let expectedUser = User(id: UUID(), name: "Alice", email: "alice@example.com")
        mockAPIClient.userToReturn = expectedUser

        // When
        await viewModel.fetchUser()

        // Then
        XCTAssertEqual(viewModel.user?.name, "Alice")
        XCTAssertNil(viewModel.error)
        XCTAssertFalse(viewModel.isLoading)
    }

    func testFetchUserFailure() async {
        // Given
        mockAPIClient.shouldFail = true

        // When
        await viewModel.fetchUser()

        // Then
        XCTAssertNil(viewModel.user)
        XCTAssertNotNil(viewModel.error)
        XCTAssertFalse(viewModel.isLoading)
    }
}

// Mock
class MockAPIClient {
    var userToReturn: User?
    var shouldFail = false

    func fetchUser() async throws -> User {
        if shouldFail {
            throw APIError.invalidResponse
        }
        return userToReturn ?? User(id: UUID(), name: "Test", email: "test@example.com")
    }
}
```

## Best Practices

### Code Organization
- Use MVVM pattern for SwiftUI
- Separate business logic from views
- Use dependency injection
- Keep views small and composable

### Memory Management
- Understand ARC (Automatic Reference Counting)
- Use weak references for delegates
- Break retain cycles with [weak self] or [unowned self]
- Use actors for mutable shared state

### Performance
- Use lazy loading where appropriate
- Avoid unnecessary view updates
- Profile with Instruments
- Use value types (structs) by default

### Swift Concurrency
- Prefer async/await over completion handlers
- Use actors for thread-safe mutable state
- Use @MainActor for UI updates
- Avoid blocking the main thread

## Anti-Patterns to Avoid

❌ **Force unwrapping**: Use optional binding instead
❌ **Massive view controllers**: Extract logic to view models
❌ **Strong reference cycles**: Use weak/unowned references
❌ **Blocking main thread**: Use async/await
❌ **Ignoring memory warnings**: Handle memory pressure
❌ **Not using guard**: Use guard for early exits
❌ **Implicit unwrapping**: Prefer explicit optionals

## Resources

- Swift Documentation: https://swift.org/documentation/
- SwiftUI Tutorials: https://developer.apple.com/tutorials/swiftui
- WWDC Sessions: https://developer.apple.com/videos/
- Swift by Sundell: https://www.swiftbysundell.com/
- Hacking with Swift: https://www.hackingwithswift.com/
