---
name: lang-swift-dev
description: Foundational Swift development patterns covering modern Swift syntax, SwiftUI, protocol-oriented programming, and Cocoa Touch frameworks. Use when writing Swift code, building iOS/macOS/watchOS/tvOS applications, working with SwiftUI or UIKit, understanding Swift concurrency, or needing guidance on Swift project structure.
---

# Swift Development Fundamentals

Foundational Swift patterns and modern language features for Apple platform development. This skill covers core Swift syntax, SwiftUI, UIKit integration, and protocol-oriented design patterns.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Swift Development Ecosystem                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌──────────────────┐                         │
│                    │  lang-swift-dev  │ ◄── You are here        │
│                    │   (foundation)   │                         │
│                    └────────┬─────────┘                         │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   SwiftUI   │    │    UIKit    │    │   Swift     │         │
│  │ Mastery     │    │  Advanced   │    │  Package    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Core Swift syntax (optionals, closures, generics, protocols)
- SwiftUI basics (views, state management, modifiers)
- Protocol-oriented programming patterns
- Swift concurrency (async/await, actors, tasks)
- UIKit fundamentals and integration
- Xcode project structure and organization

**This skill does NOT cover:**
- Advanced SwiftUI architecture - see `swiftui-patterns-advanced`
- Complex UIKit patterns - see `uikit-advanced-patterns`
- Swift Package Manager publishing - see `swift-package-dev`
- iOS app distribution and App Store submission
- Combine framework (prefer Swift concurrency for new code)

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Define optional | `var name: String?` |
| Unwrap safely | `if let name = name { }` |
| Guard unwrap | `guard let name = name else { return }` |
| Define protocol | `protocol Named { var name: String { get } }` |
| Conform to protocol | `extension MyType: Named { }` |
| Async function | `func fetch() async throws -> Data` |
| Call async | `let data = try await fetch()` |
| SwiftUI view | `struct ContentView: View { var body: some View { } }` |
| State variable | `@State private var count = 0` |

---

## Core Swift Patterns

### Optionals and Unwrapping

```swift
// Optional declaration
var username: String?
var age: Int? = nil

// Safe unwrapping with if let
if let username = username {
    print("Hello, \(username)")
} else {
    print("No username set")
}

// Guard for early exit
func greet(name: String?) {
    guard let name = name else {
        print("Name required")
        return
    }
    print("Hello, \(name)")
}

// Nil coalescing
let displayName = username ?? "Guest"

// Optional chaining
let uppercased = username?.uppercased()

// Force unwrap (use sparingly!)
let name = username!  // Crashes if nil
```

### Closures

```swift
// Basic closure
let multiply = { (a: Int, b: Int) -> Int in
    return a * b
}

// Type inference
let add = { a, b in a + b }

// Trailing closure syntax
[1, 2, 3].map { number in
    number * 2
}

// Shorthand argument names
[1, 2, 3].map { $0 * 2 }

// Capturing values
func makeIncrementer(amount: Int) -> () -> Int {
    var total = 0
    return {
        total += amount
        return total
    }
}

let incrementByTwo = makeIncrementer(amount: 2)
print(incrementByTwo())  // 2
print(incrementByTwo())  // 4

// Escaping closures (stored beyond function scope)
func fetchData(completion: @escaping (Result<Data, Error>) -> Void) {
    DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
        completion(.success(Data()))
    }
}
```

### Protocols and Protocol-Oriented Programming

```swift
// Define a protocol
protocol Drawable {
    func draw()
}

protocol Identifiable {
    var id: String { get }
}

// Conform to protocols
struct Circle: Drawable {
    func draw() {
        print("Drawing circle")
    }
}

// Protocol composition
struct User: Identifiable, Codable {
    let id: String
    let name: String
}

// Protocol extensions (add default implementations)
extension Drawable {
    func draw() {
        print("Default drawing")
    }

    func render() {
        print("Rendering...")
        draw()
    }
}

// Protocol with associated types
protocol Container {
    associatedtype Item
    var items: [Item] { get }
    mutating func add(_ item: Item)
}

struct IntStack: Container {
    typealias Item = Int
    var items: [Int] = []

    mutating func add(_ item: Int) {
        items.append(item)
    }
}
```

### Generics

```swift
// Generic function
func swap<T>(_ a: inout T, _ b: inout T) {
    let temp = a
    a = b
    b = temp
}

// Generic type
struct Stack<Element> {
    private var items: [Element] = []

    mutating func push(_ item: Element) {
        items.append(item)
    }

    mutating func pop() -> Element? {
        return items.popLast()
    }
}

// Generic constraints
func findIndex<T: Equatable>(of value: T, in array: [T]) -> Int? {
    for (index, element) in array.enumerated() {
        if element == value {
            return index
        }
    }
    return nil
}

// Where clauses
func allItemsMatch<C1: Container, C2: Container>(
    _ container1: C1,
    _ container2: C2
) -> Bool where C1.Item == C2.Item, C1.Item: Equatable {
    guard container1.items.count == container2.items.count else {
        return false
    }
    return zip(container1.items, container2.items).allSatisfy { $0 == $1 }
}
```

### Enums and Pattern Matching

```swift
// Simple enum
enum Direction {
    case north, south, east, west
}

// Enum with associated values
enum Result<Success, Failure: Error> {
    case success(Success)
    case failure(Failure)
}

// Enum with raw values
enum HTTPStatus: Int {
    case ok = 200
    case notFound = 404
    case serverError = 500
}

// Pattern matching
let result: Result<String, Error> = .success("Data")

switch result {
case .success(let value):
    print("Success: \(value)")
case .failure(let error):
    print("Error: \(error)")
}

// If case pattern matching
if case .success(let value) = result {
    print("Got value: \(value)")
}

// Recursive enums
indirect enum Expression {
    case number(Int)
    case addition(Expression, Expression)
    case multiplication(Expression, Expression)
}
```

### Property Wrappers

```swift
// Built-in property wrappers
@State private var count = 0
@Published var username = ""
@Environment(\.colorScheme) var colorScheme

// Custom property wrapper
@propertyWrapper
struct Clamped<Value: Comparable> {
    private var value: Value
    private let range: ClosedRange<Value>

    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }

    init(wrappedValue: Value, _ range: ClosedRange<Value>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

// Usage
struct Game {
    @Clamped(0...100) var health = 100
}

var game = Game()
game.health = 150  // Clamped to 100
game.health = -10  // Clamped to 0
```

---

## Swift Concurrency

### Async/Await

```swift
// Define async function
func fetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Call async function
Task {
    do {
        let user = try await fetchUser(id: "123")
        print("Fetched user: \(user.name)")
    } catch {
        print("Error: \(error)")
    }
}

// Async let (parallel execution)
func loadData() async throws -> (User, [Post]) {
    async let user = fetchUser(id: "123")
    async let posts = fetchPosts(userId: "123")
    return try await (user, posts)
}

// Async sequences
func processLines(url: URL) async throws {
    for try await line in url.lines {
        print("Line: \(line)")
    }
}
```

### Actors

```swift
// Actor for thread-safe state
actor BankAccount {
    private var balance: Double = 0

    func deposit(amount: Double) {
        balance += amount
    }

    func withdraw(amount: Double) -> Bool {
        guard balance >= amount else {
            return false
        }
        balance -= amount
        return true
    }

    func getBalance() -> Double {
        return balance
    }
}

// Usage (automatically synchronized)
let account = BankAccount()

Task {
    await account.deposit(amount: 100)
    let balance = await account.getBalance()
    print("Balance: \(balance)")
}
```

### Tasks and Task Groups

```swift
// Detached task
Task.detached {
    await performBackgroundWork()
}

// Task group (structured concurrency)
func fetchAllUsers() async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in 1...10 {
            group.addTask {
                try await fetchUser(id: String(id))
            }
        }

        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}

// Task cancellation
let task = Task {
    for i in 1...100 {
        if Task.isCancelled {
            print("Task cancelled at \(i)")
            return
        }
        await doWork(i)
    }
}

// Cancel after delay
Task {
    try await Task.sleep(nanoseconds: 1_000_000_000)
    task.cancel()
}
```

---

## SwiftUI Fundamentals

### View Basics

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Text("Hello, World!")
                .font(.largeTitle)
                .foregroundColor(.blue)

            Image(systemName: "star.fill")
                .font(.system(size: 50))

            Button("Tap Me") {
                print("Button tapped")
            }
        }
        .padding()
    }
}
```

### State Management

```swift
struct CounterView: View {
    // State for view-local data
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
                .font(.largeTitle)

            Button("Increment") {
                count += 1
            }
        }
    }
}

// ObservableObject for shared state
class UserViewModel: ObservableObject {
    @Published var username = ""
    @Published var isLoggedIn = false

    func login() {
        // Perform login
        isLoggedIn = true
    }
}

struct LoginView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        VStack {
            TextField("Username", text: $viewModel.username)
                .textFieldStyle(.roundedBorder)

            Button("Login") {
                viewModel.login()
            }

            if viewModel.isLoggedIn {
                Text("Welcome, \(viewModel.username)!")
            }
        }
        .padding()
    }
}

// Environment values
struct ThemedView: View {
    @Environment(\.colorScheme) var colorScheme

    var body: some View {
        Text("Theme: \(colorScheme == .dark ? "Dark" : "Light")")
    }
}
```

### Lists and Navigation

```swift
struct Item: Identifiable {
    let id = UUID()
    let title: String
}

struct ItemListView: View {
    let items = [
        Item(title: "First"),
        Item(title: "Second"),
        Item(title: "Third")
    ]

    var body: some View {
        NavigationView {
            List(items) { item in
                NavigationLink(destination: DetailView(item: item)) {
                    Text(item.title)
                }
            }
            .navigationTitle("Items")
        }
    }
}

struct DetailView: View {
    let item: Item

    var body: some View {
        Text("Detail for \(item.title)")
            .navigationTitle(item.title)
    }
}
```

### Custom Modifiers and ViewBuilder

```swift
// Custom view modifier
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

// ViewBuilder pattern
@ViewBuilder
func conditionalView(showText: Bool) -> some View {
    if showText {
        Text("Visible")
    } else {
        Image(systemName: "eye.slash")
    }
}
```

---

## UIKit Integration

### UIKit in SwiftUI (UIViewRepresentable)

```swift
import UIKit
import SwiftUI

struct TextView: UIViewRepresentable {
    @Binding var text: String

    func makeUIView(context: Context) -> UITextView {
        let textView = UITextView()
        textView.delegate = context.coordinator
        return textView
    }

    func updateUIView(_ uiView: UITextView, context: Context) {
        uiView.text = text
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(text: $text)
    }

    class Coordinator: NSObject, UITextViewDelegate {
        @Binding var text: String

        init(text: Binding<String>) {
            _text = text
        }

        func textViewDidChange(_ textView: UITextView) {
            text = textView.text
        }
    }
}
```

### SwiftUI in UIKit (UIHostingController)

```swift
import UIKit
import SwiftUI

class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        // Embed SwiftUI view in UIKit
        let swiftUIView = ContentView()
        let hostingController = UIHostingController(rootView: swiftUIView)

        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.view.frame = view.bounds
        hostingController.didMove(toParent: self)
    }
}
```

### Basic UIKit Patterns

```swift
// UIViewController lifecycle
class MyViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        // Setup after view loads
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // Before view appears
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        // After view appears
    }
}

// Delegation pattern
protocol DataSourceDelegate: AnyObject {
    func didReceiveData(_ data: String)
}

class DataSource {
    weak var delegate: DataSourceDelegate?

    func fetchData() {
        // Fetch data
        delegate?.didReceiveData("Data")
    }
}
```

---

## Project Structure

### Swift Package Structure

```
MyPackage/
├── Package.swift
├── Sources/
│   └── MyPackage/
│       ├── MyPackage.swift
│       └── Models/
│           └── User.swift
├── Tests/
│   └── MyPackageTests/
│       └── MyPackageTests.swift
└── README.md
```

### iOS App Structure

```
MyApp/
├── MyApp/
│   ├── App/
│   │   ├── MyAppApp.swift
│   │   └── ContentView.swift
│   ├── Models/
│   │   └── User.swift
│   ├── Views/
│   │   ├── HomeView.swift
│   │   └── DetailView.swift
│   ├── ViewModels/
│   │   └── UserViewModel.swift
│   ├── Services/
│   │   └── NetworkService.swift
│   ├── Resources/
│   │   └── Assets.xcassets
│   └── Supporting Files/
│       └── Info.plist
└── MyAppTests/
    └── MyAppTests.swift
```

### Package.swift Example

```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "MyPackage",
    platforms: [
        .iOS(.v16),
        .macOS(.v13)
    ],
    products: [
        .library(
            name: "MyPackage",
            targets: ["MyPackage"]
        ),
    ],
    dependencies: [
        .package(url: "https://github.com/example/package.git", from: "1.0.0"),
    ],
    targets: [
        .target(
            name: "MyPackage",
            dependencies: []
        ),
        .testTarget(
            name: "MyPackageTests",
            dependencies: ["MyPackage"]
        ),
    ]
)
```

---

## Common Idioms

### Result Builders

```swift
@resultBuilder
struct StringBuilder {
    static func buildBlock(_ components: String...) -> String {
        components.joined(separator: " ")
    }
}

@StringBuilder
func makeGreeting() -> String {
    "Hello"
    "World"
    "from"
    "Swift"
}

print(makeGreeting())  // "Hello World from Swift"
```

### Codable for JSON

```swift
struct User: Codable {
    let id: Int
    let name: String
    let email: String

    // Custom coding keys
    enum CodingKeys: String, CodingKey {
        case id
        case name
        case email = "email_address"
    }
}

// Decode JSON
let json = """
{
    "id": 1,
    "name": "John",
    "email_address": "john@example.com"
}
""".data(using: .utf8)!

let user = try JSONDecoder().decode(User.self, from: json)

// Encode to JSON
let data = try JSONEncoder().encode(user)
```

### Error Handling

```swift
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed
}

func fetchData(from urlString: String) throws -> Data {
    guard let url = URL(string: urlString) else {
        throw NetworkError.invalidURL
    }

    // Fetch data...
    guard let data = try? Data(contentsOf: url) else {
        throw NetworkError.noData
    }

    return data
}

// Using do-catch
do {
    let data = try fetchData(from: "https://api.example.com")
    print("Fetched \(data.count) bytes")
} catch NetworkError.invalidURL {
    print("Invalid URL")
} catch {
    print("Error: \(error)")
}
```

---

## Troubleshooting

### Optional Unwrapping Crashes

**Problem:** `Fatal error: Unexpectedly found nil while unwrapping an Optional value`

```swift
// Bad: Force unwrapping
let name = user.name!  // Crashes if nil

// Good: Safe unwrapping
if let name = user.name {
    print(name)
}

// Or: Guard
guard let name = user.name else {
    return
}
```

### Retain Cycles in Closures

**Problem:** Memory leaks from strong reference cycles

```swift
// Bad: Strong reference to self
class ViewController {
    var completion: (() -> Void)?

    func setup() {
        completion = {
            self.doSomething()  // Strong reference cycle
        }
    }
}

// Good: Weak or unowned self
class ViewController {
    var completion: (() -> Void)?

    func setup() {
        completion = { [weak self] in
            self?.doSomething()
        }
    }
}
```

### SwiftUI View Not Updating

**Problem:** View doesn't update when data changes

```swift
// Bad: No property wrapper
class ViewModel {
    var count = 0  // Changes won't trigger updates
}

// Good: Use @Published in ObservableObject
class ViewModel: ObservableObject {
    @Published var count = 0
}

struct ContentView: View {
    @StateObject var viewModel = ViewModel()

    var body: some View {
        Text("Count: \(viewModel.count)")
    }
}
```

### Actor Reentrancy Issues

**Problem:** Unexpected state changes in async actor methods

```swift
actor Counter {
    private var value = 0

    // Potential reentrancy issue
    func increment() async {
        await Task.sleep(1_000_000_000)
        value += 1  // Value might have changed during await
    }

    // Better: Check state after await
    func safeIncrement() async -> Int {
        let currentValue = value
        await Task.sleep(1_000_000_000)
        value = currentValue + 1
        return value
    }
}
```

---

## Testing

### XCTest Basics

```swift
import XCTest
@testable import MyApp

final class UserTests: XCTestCase {
    var sut: User!  // System Under Test

    override func setUp() {
        super.setUp()
        sut = User(name: "Alice", age: 30)
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func testUserInitialization() {
        // Arrange & Act (done in setUp)

        // Assert
        XCTAssertEqual(sut.name, "Alice")
        XCTAssertEqual(sut.age, 30)
    }

    func testUserValidation() {
        // Arrange
        let invalidUser = User(name: "", age: -1)

        // Act
        let isValid = invalidUser.validate()

        // Assert
        XCTAssertFalse(isValid)
    }
}
```

### Swift Testing (@Test Macro)

```swift
import Testing
@testable import MyApp

struct UserTests {
    // Simple test
    @Test func userInitialization() {
        let user = User(name: "Alice", age: 30)
        #expect(user.name == "Alice")
        #expect(user.age == 30)
    }

    // Test with custom name
    @Test("User validation rejects empty names")
    func userValidation() {
        let user = User(name: "", age: 30)
        #expect(!user.validate())
    }

    // Parameterized tests
    @Test("Age validation", arguments: [
        (18, true),
        (17, false),
        (65, true),
        (0, false),
        (-1, false)
    ])
    func ageValidation(age: Int, expected: Bool) {
        let user = User(name: "Test", age: age)
        #expect(user.isValidAge() == expected)
    }

    // Tests with tags
    @Test(.tags(.critical))
    func criticalFeature() {
        let result = performCriticalOperation()
        #expect(result != nil)
    }
}

// Custom tags
extension Tag {
    @Tag static var critical: Self
    @Tag static var integration: Self
    @Tag static var performance: Self
}
```

### XCTest Assertions

```swift
// Boolean assertions
XCTAssertTrue(condition)
XCTAssertFalse(condition)

// Nil assertions
XCTAssertNil(value)
XCTAssertNotNil(value)

// Equality assertions
XCTAssertEqual(actual, expected)
XCTAssertNotEqual(actual, unexpected)
XCTAssertIdentical(object1, object2)  // Same instance

// Numeric comparisons
XCTAssertGreaterThan(5, 3)
XCTAssertLessThan(3, 5)
XCTAssertGreaterThanOrEqual(5, 5)
XCTAssertLessThanOrEqual(3, 5)

// Floating point equality with accuracy
XCTAssertEqual(3.14, 3.14159, accuracy: 0.01)

// Error assertions
XCTAssertThrowsError(try riskyOperation()) { error in
    XCTAssertEqual(error as? MyError, MyError.notFound)
}
XCTAssertNoThrow(try safeOperation())

// Custom failure
XCTFail("Test failed: \(reason)")
```

### Async Testing

```swift
// Async/await testing
func testAsyncFetch() async throws {
    // Act
    let user = try await networkService.fetchUser(id: "123")

    // Assert
    XCTAssertEqual(user.id, "123")
    XCTAssertNotNil(user.name)
}

// Testing with expectations
func testCompletionHandler() {
    let expectation = expectation(description: "Data fetched")

    networkService.fetchUser(id: "123") { result in
        switch result {
        case .success(let user):
            XCTAssertEqual(user.id, "123")
            expectation.fulfill()
        case .failure(let error):
            XCTFail("Failed with error: \(error)")
        }
    }

    waitForExpectations(timeout: 5.0)
}

// Multiple expectations
func testMultipleAsync() async throws {
    async let user = fetchUser(id: "123")
    async let posts = fetchPosts(userId: "123")

    let (fetchedUser, fetchedPosts) = try await (user, posts)

    XCTAssertEqual(fetchedUser.id, "123")
    XCTAssertFalse(fetchedPosts.isEmpty)
}

// Swift Testing async
@Test func asyncFetch() async throws {
    let user = try await networkService.fetchUser(id: "123")
    #expect(user.id == "123")
}

// Testing actors
func testActorIsolation() async {
    let counter = Counter()

    await counter.increment()
    await counter.increment()

    let value = await counter.value
    XCTAssertEqual(value, 2)
}
```

### Mocking Protocols

```swift
// Define protocol
protocol NetworkService {
    func fetchUser(id: String) async throws -> User
    func updateUser(_ user: User) async throws
}

// Mock implementation
class MockNetworkService: NetworkService {
    var fetchUserCalled = false
    var fetchUserCallCount = 0
    var userToReturn: User?
    var errorToThrow: Error?

    func fetchUser(id: String) async throws -> User {
        fetchUserCalled = true
        fetchUserCallCount += 1

        if let error = errorToThrow {
            throw error
        }

        return userToReturn ?? User(id: id, name: "Mock User", age: 30)
    }

    var updateUserCalled = false
    var updatedUser: User?

    func updateUser(_ user: User) async throws {
        updateUserCalled = true
        updatedUser = user

        if let error = errorToThrow {
            throw error
        }
    }
}

// Using mock in tests
func testUserViewModel() async throws {
    // Arrange
    let mockService = MockNetworkService()
    mockService.userToReturn = User(id: "123", name: "Alice", age: 30)
    let viewModel = UserViewModel(service: mockService)

    // Act
    await viewModel.loadUser(id: "123")

    // Assert
    XCTAssertTrue(mockService.fetchUserCalled)
    XCTAssertEqual(mockService.fetchUserCallCount, 1)
    XCTAssertEqual(viewModel.user?.name, "Alice")
}
```

### Spy Pattern

```swift
// Spy records all calls and arguments
class SpyNetworkService: NetworkService {
    var calls: [(method: String, arguments: Any)] = []

    func fetchUser(id: String) async throws -> User {
        calls.append((method: "fetchUser", arguments: id))
        return User(id: id, name: "Spy User", age: 30)
    }

    func updateUser(_ user: User) async throws {
        calls.append((method: "updateUser", arguments: user))
    }
}

// Using spy
func testCallSequence() async throws {
    let spy = SpyNetworkService()
    let viewModel = UserViewModel(service: spy)

    await viewModel.loadUser(id: "123")
    await viewModel.updateUserName("Bob")

    XCTAssertEqual(spy.calls.count, 2)
    XCTAssertEqual(spy.calls[0].method, "fetchUser")
    XCTAssertEqual(spy.calls[1].method, "updateUser")
}
```

### Stub Pattern

```swift
// Stub returns predetermined responses
class StubNetworkService: NetworkService {
    var stubbedUsers: [String: User] = [:]

    func fetchUser(id: String) async throws -> User {
        guard let user = stubbedUsers[id] else {
            throw NetworkError.notFound
        }
        return user
    }

    func updateUser(_ user: User) async throws {
        // No-op for stub
    }
}

// Using stub
func testWithPresetData() async throws {
    let stub = StubNetworkService()
    stub.stubbedUsers = [
        "123": User(id: "123", name: "Alice", age: 30),
        "456": User(id: "456", name: "Bob", age: 25)
    ]

    let user = try await stub.fetchUser(id: "123")
    XCTAssertEqual(user.name, "Alice")
}
```

### Testing SwiftUI Views

```swift
import ViewInspector

struct ContentViewTests: XCTestCase {
    func testButtonTap() throws {
        var viewModel = ViewModel()
        let view = ContentView(viewModel: viewModel)

        // Find button and simulate tap
        let button = try view.inspect().find(button: "Increment")
        try button.tap()

        // Verify state changed
        XCTAssertEqual(viewModel.count, 1)
    }

    func testTextDisplayed() throws {
        let view = ContentView(title: "Hello")
        let text = try view.inspect().find(text: "Hello")
        XCTAssertNotNil(text)
    }
}

// Snapshot testing (with SnapshotTesting library)
func testViewSnapshot() {
    let view = ContentView()
    assertSnapshot(matching: view, as: .image)
}
```

### UI Testing Basics

```swift
import XCTest

final class AppUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }

    func testLoginFlow() {
        // Find elements
        let usernameField = app.textFields["Username"]
        let passwordField = app.secureTextFields["Password"]
        let loginButton = app.buttons["Login"]

        // Interact with UI
        usernameField.tap()
        usernameField.typeText("alice@example.com")

        passwordField.tap()
        passwordField.typeText("password123")

        loginButton.tap()

        // Verify navigation
        let welcomeText = app.staticTexts["Welcome, Alice!"]
        XCTAssertTrue(welcomeText.waitForExistence(timeout: 5))
    }

    func testSwipeToDelete() {
        let firstCell = app.cells.firstMatch
        XCTAssertTrue(firstCell.waitForExistence(timeout: 2))

        firstCell.swipeLeft()

        let deleteButton = firstCell.buttons["Delete"]
        deleteButton.tap()

        XCTAssertFalse(firstCell.exists)
    }
}
```

### Performance Testing

```swift
func testPerformance() {
    measure {
        // Code to measure
        _ = heavyComputation()
    }
}

// Metrics-based performance testing
func testPerformanceMetrics() {
    let options = XCTMeasureOptions()
    options.iterationCount = 10

    measure(metrics: [XCTClockMetric(), XCTMemoryMetric()], options: options) {
        processLargeDataset()
    }
}

// Swift Testing performance
@Test(.timeLimit(.minutes(1)))
func performanceSensitiveOperation() {
    let result = expensiveComputation()
    #expect(result != nil)
}
```

### Test Organization

```swift
// Group related tests
class UserValidationTests: XCTestCase {
    func testEmailValidation() { }
    func testPasswordValidation() { }
    func testAgeValidation() { }
}

class UserPersistenceTests: XCTestCase {
    func testSaveUser() { }
    func testLoadUser() { }
    func testDeleteUser() { }
}

// Swift Testing suites
@Suite("User Management")
struct UserManagementTests {
    @Suite("Validation")
    struct ValidationTests {
        @Test func emailValidation() { }
        @Test func passwordValidation() { }
    }

    @Suite("Persistence")
    struct PersistenceTests {
        @Test func saveUser() { }
        @Test func loadUser() { }
    }
}
```

### Test Helpers

```swift
// Custom assertions
func assertUserValid(_ user: User, file: StaticString = #file, line: UInt = #line) {
    XCTAssertFalse(user.name.isEmpty, "User name is empty", file: file, line: line)
    XCTAssertGreaterThan(user.age, 0, "User age is invalid", file: file, line: line)
    XCTAssertNotNil(user.email, "User email is nil", file: file, line: line)
}

// Test fixtures
extension User {
    static func fixture(
        name: String = "Test User",
        age: Int = 30,
        email: String = "test@example.com"
    ) -> User {
        User(name: name, age: age, email: email)
    }
}

// Usage
func testUserFeature() {
    let user = User.fixture(name: "Alice")
    assertUserValid(user)
}
```

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - async/await, actors, task groups
- `patterns-serialization-dev` - Codable, JSON, property lists
- `patterns-metaprogramming-dev` - Reflection, type introspection

---

## References

- [Swift Language Guide](https://docs.swift.org/swift-book/LanguageGuide/TheBasics.html)
- [SwiftUI Tutorials](https://developer.apple.com/tutorials/swiftui)
- [Swift Evolution Proposals](https://github.com/apple/swift-evolution)
- [WWDC Videos](https://developer.apple.com/videos/)
- [Swift by Sundell](https://www.swiftbysundell.com/)
- [Hacking with Swift](https://www.hackingwithswift.com/)
- [Swift Testing Documentation](https://developer.apple.com/documentation/testing)
- [XCTest Documentation](https://developer.apple.com/documentation/xctest)
