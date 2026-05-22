---
name: swift-testing
description: Swift Testing framework with @Test macro, #expect, #require, test organization, and Xcode Playgrounds. Use when user asks about testing, unit tests, @Test, #expect, #require, test suites, or Xcode Playgrounds.
allowed-tools: Bash, Read, Write, Edit
---

# Swift Testing Framework

Comprehensive guide to the modern Swift Testing framework, test organization, assertions, and Xcode Playgrounds for iOS 26 development.

## Prerequisites

- Swift 6.0+ (included in Xcode 16+)
- Xcode 26+ recommended

---

## Framework Overview

### Swift Testing vs XCTest

| Feature | Swift Testing | XCTest |
|---------|--------------|--------|
| Test marking | `@Test` macro | Method naming `test*` |
| Assertions | `#expect`, `#require` | `XCTAssert*` |
| Test organization | Structs, actors, classes | XCTestCase subclass |
| Parallelism | Parallel by default | Process-based |
| Setup/Teardown | `init`/`deinit` | `setUp`/`tearDown` |

### Import

```swift
import Testing
```

---

## @Test Macro

### Basic Test

```swift
import Testing

@Test
func additionWorks() {
    let result = 2 + 2
    #expect(result == 4)
}
```

### Test with Display Name

```swift
@Test("User can create account with valid email")
func createAccountWithValidEmail() async throws {
    let account = try await AccountService.create(email: "test@example.com")
    #expect(account.email == "test@example.com")
}
```

### Async Tests

```swift
@Test
func fetchUserReturnsData() async throws {
    let user = try await userService.fetch(id: "123")
    #expect(user.name == "John Doe")
}
```

### Throwing Tests

```swift
@Test
func invalidEmailThrows() throws {
    #expect(throws: ValidationError.invalidEmail) {
        try validate(email: "not-an-email")
    }
}
```

---

## Assertions

### #expect

Basic expectations:

```swift
@Test
func basicExpectations() {
    let value = 42

    // Equality
    #expect(value == 42)

    // Inequality
    #expect(value != 0)

    // Boolean
    #expect(value > 0)

    // With message
    #expect(value == 42, "Value should be 42")
}
```

### #expect with Expressions

```swift
@Test
func expressionExpectations() {
    let array = [1, 2, 3]

    #expect(array.count == 3)
    #expect(array.contains(2))
    #expect(!array.isEmpty)

    let optional: String? = "hello"
    #expect(optional != nil)
}
```

### #require

Unwrap optionals and fail fast:

```swift
@Test
func requireUnwrapping() throws {
    let optional: String? = "hello"

    // Unwrap or fail test
    let value = try #require(optional)

    #expect(value == "hello")
}

@Test
func requireCondition() throws {
    let array = [1, 2, 3]

    // Fail if condition is false
    try #require(array.count > 0)

    let first = try #require(array.first)
    #expect(first == 1)
}
```

### Testing Throws

```swift
@Test
func throwingBehavior() {
    // Expect any error
    #expect(throws: (any Error).self) {
        try riskyOperation()
    }

    // Expect specific error type
    #expect(throws: NetworkError.self) {
        try fetchData()
    }

    // Expect specific error value
    #expect(throws: NetworkError.timeout) {
        try fetchWithTimeout()
    }
}

@Test
func noThrow() {
    // Expect no error
    #expect(throws: Never.self) {
        safeOperation()
    }
}
```

### Custom Failure Messages

```swift
@Test
func customMessages() {
    let user = User(name: "Alice", age: 25)

    #expect(user.age >= 18, "User must be an adult, but age was \(user.age)")
}
```

---

## Test Organization

### Test Suites with Structs

```swift
@Suite("User Authentication Tests")
struct AuthenticationTests {
    @Test("Valid credentials succeed")
    func validLogin() async throws {
        let result = try await auth.login(user: "test", pass: "password")
        #expect(result.success)
    }

    @Test("Invalid credentials fail")
    func invalidLogin() async throws {
        let result = try await auth.login(user: "test", pass: "wrong")
        #expect(!result.success)
    }
}
```

### Nested Suites

```swift
@Suite("API Tests")
struct APITests {
    @Suite("User Endpoints")
    struct UserEndpoints {
        @Test func getUser() async { }
        @Test func createUser() async { }
    }

    @Suite("Post Endpoints")
    struct PostEndpoints {
        @Test func getPosts() async { }
        @Test func createPost() async { }
    }
}
```

### Using Actors for Isolation

```swift
@Suite
actor DatabaseTests {
    var database: TestDatabase

    init() async throws {
        database = try await TestDatabase.create()
    }

    @Test
    func insertWorks() async throws {
        try await database.insert(User(name: "Test"))
        let count = try await database.count(User.self)
        #expect(count == 1)
    }
}
```

### Setup and Teardown

```swift
@Suite
struct DatabaseTests {
    let database: Database

    init() async throws {
        // Setup - called before each test
        database = try await Database.createInMemory()
        try await database.migrate()
    }

    deinit {
        // Teardown - called after each test
        // Note: async cleanup should be done differently
    }

    @Test
    func testInsert() async throws {
        try await database.insert(item)
        #expect(try await database.count() == 1)
    }
}
```

---

## Parameterized Tests

### Basic Parameters

```swift
@Test("Validation", arguments: [
    "test@example.com",
    "user@domain.org",
    "name@company.co.uk"
])
func validEmails(email: String) {
    #expect(isValidEmail(email))
}
```

### Multiple Arguments

```swift
@Test("Addition", arguments: [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300)
])
func addition(a: Int, b: Int, expected: Int) {
    #expect(a + b == expected)
}
```

### Zip Arguments

```swift
@Test(arguments: zip(
    ["hello", "world", "test"],
    [5, 5, 4]
))
func stringLength(string: String, expectedLength: Int) {
    #expect(string.count == expectedLength)
}
```

### Custom Types as Arguments

```swift
struct TestCase: CustomTestStringConvertible {
    let input: String
    let expected: Int

    var testDescription: String {
        "'\(input)' should have length \(expected)"
    }
}

@Test("String lengths", arguments: [
    TestCase(input: "hello", expected: 5),
    TestCase(input: "", expected: 0),
    TestCase(input: "Swift", expected: 5)
])
func stringLength(testCase: TestCase) {
    #expect(testCase.input.count == testCase.expected)
}
```

---

## Test Traits

### .serialized

Run tests sequentially:

```swift
@Suite(.serialized)
struct OrderDependentTests {
    @Test func step1() { }
    @Test func step2() { }
    @Test func step3() { }
}
```

### .disabled

Skip tests:

```swift
@Test(.disabled("Known bug, see issue #123"))
func brokenFeature() {
    // Won't run
}

@Test(.disabled(if: isCI, "Flaky on CI"))
func flakyTest() {
    // Conditionally disabled
}
```

### .enabled

Conditionally enable:

```swift
@Test(.enabled(if: ProcessInfo.processInfo.environment["RUN_SLOW_TESTS"] != nil))
func slowIntegrationTest() async throws {
    // Only runs when environment variable is set
}
```

### .tags

Organize with tags:

```swift
extension Tag {
    @Tag static var critical: Self
    @Tag static var slow: Self
    @Tag static var integration: Self
}

@Test(.tags(.critical))
func criticalFeature() { }

@Test(.tags(.slow, .integration))
func slowIntegrationTest() async { }
```

### .timeLimit

Set execution limit:

```swift
@Test(.timeLimit(.seconds(5)))
func mustCompleteQuickly() async throws {
    // Fails if takes more than 5 seconds
}
```

### .bug

Reference known issues:

```swift
@Test(.bug("https://github.com/org/repo/issues/123", "Expected failure"))
func knownIssue() {
    // Test expected to fail
}
```

---

## Parallel Execution

### Default Parallel

Tests run in parallel by default:

```swift
@Suite
struct ParallelTests {
    // These run concurrently
    @Test func test1() async { }
    @Test func test2() async { }
    @Test func test3() async { }
}
```

### Serial When Needed

```swift
@Suite(.serialized)
struct SerialTests {
    static var sharedState = 0

    @Test func first() {
        Self.sharedState = 1
        #expect(Self.sharedState == 1)
    }

    @Test func second() {
        Self.sharedState = 2
        #expect(Self.sharedState == 2)
    }
}
```

---

## Mocking and Test Doubles

### Protocol-Based Mocking

```swift
protocol UserService {
    func fetch(id: String) async throws -> User
}

struct MockUserService: UserService {
    var userToReturn: User?
    var errorToThrow: Error?

    func fetch(id: String) async throws -> User {
        if let error = errorToThrow {
            throw error
        }
        guard let user = userToReturn else {
            throw TestError.notConfigured
        }
        return user
    }
}

@Suite
struct UserViewModelTests {
    @Test
    func fetchUserSuccess() async throws {
        var mockService = MockUserService()
        mockService.userToReturn = User(id: "1", name: "Test")

        let viewModel = UserViewModel(service: mockService)
        try await viewModel.loadUser(id: "1")

        #expect(viewModel.user?.name == "Test")
    }
}
```

### Spy for Verification

```swift
final class SpyUserService: UserService {
    var fetchCallCount = 0
    var lastFetchedId: String?

    func fetch(id: String) async throws -> User {
        fetchCallCount += 1
        lastFetchedId = id
        return User(id: id, name: "Test")
    }
}

@Test
func loadsUserOnAppear() async throws {
    let spy = SpyUserService()
    let viewModel = UserViewModel(service: spy)

    await viewModel.loadUser(id: "123")

    #expect(spy.fetchCallCount == 1)
    #expect(spy.lastFetchedId == "123")
}
```

---

## Testing SwiftUI

### Testing Observable ViewModels

```swift
@Observable
class CounterViewModel {
    var count = 0

    func increment() {
        count += 1
    }
}

@Suite
struct CounterViewModelTests {
    @Test
    func incrementIncreasesCount() {
        let viewModel = CounterViewModel()

        viewModel.increment()

        #expect(viewModel.count == 1)
    }

    @Test
    func multipleIncrements() {
        let viewModel = CounterViewModel()

        viewModel.increment()
        viewModel.increment()
        viewModel.increment()

        #expect(viewModel.count == 3)
    }
}
```

### Testing Async ViewModels

```swift
@Observable
@MainActor
class UserListViewModel {
    var users: [User] = []
    var isLoading = false
    private let service: UserService

    init(service: UserService) {
        self.service = service
    }

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }
        users = (try? await service.fetchAll()) ?? []
    }
}

@Suite
struct UserListViewModelTests {
    @Test
    @MainActor
    func loadUsersPopulatesArray() async {
        var mock = MockUserService()
        mock.usersToReturn = [User(id: "1", name: "Alice")]

        let viewModel = UserListViewModel(service: mock)
        await viewModel.loadUsers()

        #expect(viewModel.users.count == 1)
        #expect(viewModel.isLoading == false)
    }
}
```

---

## Migration from XCTest

### Side-by-Side

Both frameworks can coexist:

```swift
// XCTest
import XCTest

class LegacyTests: XCTestCase {
    func testOldStyle() {
        XCTAssertEqual(2 + 2, 4)
    }
}

// Swift Testing
import Testing

@Test
func newStyle() {
    #expect(2 + 2 == 4)
}
```

### Mapping Assertions

| XCTest | Swift Testing |
|--------|---------------|
| `XCTAssertTrue(x)` | `#expect(x)` |
| `XCTAssertFalse(x)` | `#expect(!x)` |
| `XCTAssertEqual(a, b)` | `#expect(a == b)` |
| `XCTAssertNil(x)` | `#expect(x == nil)` |
| `XCTAssertNotNil(x)` | `try #require(x)` |
| `XCTAssertThrowsError` | `#expect(throws:)` |
| `XCTUnwrap(x)` | `try #require(x)` |

### What to Keep in XCTest

- Performance tests (`measure {}`)
- UI tests (XCUITest)
- Existing stable test suites

---

## Xcode Playgrounds

### #Playground Macro (iOS 26)

```swift
import SwiftUI

#Playground {
    let greeting = "Hello, Playgrounds!"
    print(greeting)
}

#Playground("SwiftUI Preview") {
    struct ContentView: View {
        var body: some View {
            Text("Hello, World!")
        }
    }

    ContentView()
}
```

### Named Playground Blocks

```swift
#Playground("Data Processing") {
    let numbers = [1, 2, 3, 4, 5]
    let doubled = numbers.map { $0 * 2 }
    print(doubled)
}

#Playground("API Simulation") {
    struct User: Codable {
        let name: String
    }

    let json = #"{"name": "Alice"}"#
    let user = try? JSONDecoder().decode(User.self, from: json.data(using: .utf8)!)
    print(user?.name ?? "Unknown")
}
```

### SwiftUI in Playgrounds

```swift
#Playground("Interactive UI") {
    struct Counter: View {
        @State private var count = 0

        var body: some View {
            VStack {
                Text("Count: \(count)")
                Button("Increment") {
                    count += 1
                }
            }
        }
    }

    Counter()
}
```

---

## Best Practices

### 1. Descriptive Test Names

```swift
// GOOD
@Test("User cannot login with expired token")
func expiredTokenLogin() { }

// AVOID
@Test
func test1() { }
```

### 2. One Assertion Focus

```swift
// GOOD: Focused test
@Test
func userNameIsCapitalized() {
    let user = User(name: "alice")
    #expect(user.displayName == "Alice")
}

// AVOID: Multiple unrelated assertions
@Test
func userTests() {
    let user = User(name: "alice")
    #expect(user.displayName == "Alice")
    #expect(user.email != nil)
    #expect(user.createdAt <= Date())
}
```

### 3. Use Structs for Test Suites

```swift
// GOOD: Struct-based, each test gets fresh instance
@Suite
struct UserTests {
    let service = UserService()

    @Test func fetch() { }
    @Test func create() { }
}
```

### 4. Parameterize Repetitive Tests

```swift
// GOOD: Parameterized
@Test(arguments: ["", " ", "   "])
func emptyStringsAreInvalid(input: String) {
    #expect(!isValid(input))
}

// AVOID: Duplicated tests
@Test func emptyIsInvalid() { #expect(!isValid("")) }
@Test func spaceIsInvalid() { #expect(!isValid(" ")) }
@Test func spacesAreInvalid() { #expect(!isValid("   ")) }
```

### 5. Use Tags for Organization

```swift
extension Tag {
    @Tag static var unit: Self
    @Tag static var integration: Self
    @Tag static var slow: Self
}

// Filter in Xcode or command line
// swift test --filter "unit"
```

---

## Official Resources

- [Swift Testing Documentation](https://developer.apple.com/documentation/testing)
- [Testing with Xcode](https://developer.apple.com/documentation/xcode/testing-with-xcode)
- [WWDC24: Meet Swift Testing](https://developer.apple.com/videos/play/wwdc2024/10179/)
- [WWDC23: Prototype with Xcode Playgrounds](https://developer.apple.com/videos/play/wwdc2023/10250/)
- [Migrating a test from XCTest](https://developer.apple.com/documentation/testing/migratingfromxctest)
