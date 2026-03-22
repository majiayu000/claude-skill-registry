---
name: swift-testing
description: "Write and migrate tests using the Swift Testing framework with @Test, @Suite, #expect, #require, confirmation, parameterized tests, test tags, traits, withKnownIssue, XCTest UI testing, XCUITest, test plan, mocking, test doubles, testable architecture, snapshot testing, async test patterns, test organization, and test-driven development in Swift. Use when writing or migrating tests with Swift Testing framework, implementing parameterized tests, working with test traits, converting XCTest to Swift Testing, or setting up test organization and mocking patterns."
---

# Swift Testing

Swift Testing is the modern testing framework for Swift (Xcode 16+, Swift 6+). Prefer it over XCTest for all new unit tests. Use XCTest only for UI tests, performance benchmarks, and snapshot tests.

## Contents

- [Basic Tests](#basic-tests)
- [@Test Traits](#test-traits)
- [#expect and #require](#expect-and-require)
- [@Suite and Test Organization](#suite-and-test-organization)
- [Known Issues](#known-issues)
- [Additional Patterns](#additional-patterns)
- [Parameterized Tests In Depth](#parameterized-tests-in-depth)
- [Tags and Suites In Depth](#tags-and-suites-in-depth)
- [Async Testing Patterns](#async-testing-patterns)
- [Traits In Depth](#traits-in-depth)
- [Common Mistakes](#common-mistakes)
- [Test Attachments](#test-attachments)
- [Exit Testing](#exit-testing)
- [Review Checklist](#review-checklist)
- [References](#references)

---

## Basic Tests

```swift
import Testing

@Test("User can update their display name")
func updateDisplayName() {
    var user = User(name: "Alice")
    user.name = "Bob"
    #expect(user.name == "Bob")
}
```

## @Test Traits

```swift
@Test("Validates email format")                                    // display name
@Test(.tags(.validation, .email))                                  // tags
@Test(.disabled("Server migration in progress"))                   // disabled
@Test(.enabled(if: ProcessInfo.processInfo.environment["CI"] != nil)) // conditional
@Test(.bug("https://github.com/org/repo/issues/42"))               // bug reference
@Test(.timeLimit(.minutes(1)))                                     // time limit
@Test("Timeout handling", .tags(.networking), .timeLimit(.seconds(30))) // combined
```

## #expect and #require

```swift
// #expect records failure but continues execution
#expect(result == 42)
#expect(name.isEmpty == false)
#expect(items.count > 0, "Items should not be empty")

// #expect with error type checking
#expect(throws: ValidationError.self) {
    try validate(email: "not-an-email")
}

// #expect with specific error value
#expect {
    try validate(email: "")
} throws: { error in
    guard let err = error as? ValidationError else { return false }
    return err == .empty
}

// #require records failure AND stops test (like XCTUnwrap)
let user = try #require(await fetchUser(id: 1))
#expect(user.name == "Alice")

// #require for optionals -- unwraps or fails
let first = try #require(items.first)
#expect(first.isValid)
```

**Rule: Use `#require` when subsequent assertions depend on the value. Use `#expect` for independent checks.**

## @Suite and Test Organization

See `references/testing-patterns.md` for suite organization, confirmation patterns, and known-issue handling.

## Known Issues

Mark expected failures so they do not cause test failure:

```swift
withKnownIssue("Propane tank is empty") {
    #expect(truck.grill.isHeating)
}

// Intermittent / flaky failures
withKnownIssue(isIntermittent: true) {
    #expect(service.isReachable)
}

// Conditional known issue
withKnownIssue {
    #expect(foodTruck.grill.isHeating)
} when: {
    !hasPropane
}
```

If no known issues are recorded, Swift Testing records a distinct issue notifying you the problem may be resolved.

## Additional Patterns

See `references/testing-patterns.md` for complete examples of:

- **TestScoping** -- custom test lifecycle with setup/teardown consolidation
- **Mocking and Test Doubles** -- protocol-based doubles and testable architecture
- **View Model Testing** -- environment injection and dependency isolation
- **Async Patterns** -- clock injection and error path testing
- **XCUITest** -- page objects, performance testing, snapshot testing, and test file organization

## Parameterized Tests In Depth

### @Test with Arguments

Pass any `Sendable` & `Collection` to `arguments:`. Each element runs as an independent test case.

```swift
// Enum-based: runs one case per enum value
enum Environment: String, CaseIterable, Sendable {
    case development, staging, production
}

@Test("Base URL is valid for all environments", arguments: Environment.allCases)
func baseURLIsValid(env: Environment) throws {
    let url = try #require(URL(string: Config.baseURL(for: env)))
    #expect(url.scheme == "https")
}
```

### Ranges as Arguments

```swift
@Test("Fibonacci is positive for small inputs", arguments: 1...20)
func fibonacciPositive(n: Int) {
    #expect(fibonacci(n) > 0)
}
```

### Multiple Parameter Sources

Two argument collections produce a **cartesian product** (every combination):

```swift
@Test(arguments: ["light", "dark"], ["iPhone", "iPad"])
func snapshotTest(colorScheme: String, device: String) {
    // Runs 4 combinations: light+iPhone, light+iPad, dark+iPhone, dark+iPad
    let config = SnapshotConfig(colorScheme: colorScheme, device: device)
    #expect(config.isValid)
}
```

Use `zip` for **1:1 pairing** (avoids cartesian product):

```swift
@Test(arguments: zip(
    [200, 201, 204],
    ["OK", "Created", "No Content"]
))
func httpStatusDescription(code: Int, expected: String) {
    #expect(HTTPStatus(code).description == expected)
}
```

### Custom Argument Generators

Create a `CustomTestArgumentProviding` conformance or use computed static properties:

```swift
struct APIEndpoint: Sendable {
    let path: String
    let expectedStatus: Int

    static let testCases: [APIEndpoint] = [
        .init(path: "/users", expectedStatus: 200),
        .init(path: "/missing", expectedStatus: 404),
    ]
}

@Test("API returns expected status", arguments: APIEndpoint.testCases)
func apiStatus(endpoint: APIEndpoint) async throws {
    let response = try await client.get(endpoint.path)
    #expect(response.statusCode == endpoint.expectedStatus)
}
```

## Tags and Suites In Depth

### Custom Tag Definitions

Declare tags as static members on `Tag`:

```swift
extension Tag {
    @Tag static var networking: Self
    @Tag static var database: Self
    @Tag static var slow: Self
    @Tag static var critical: Self
    @Tag static var smoke: Self
}
```

### Filtering Tests by Tag

Run tagged tests from Xcode Test Plans or the command line:

```bash
# Run only tests tagged .networking
swift test --filter tag:networking

# Exclude slow tests
swift test --skip tag:slow
```

In Xcode, configure Test Plans to include/exclude tags for different CI configurations (smoke tests vs full suite).

### @Suite for Grouping

```swift
@Suite("Shopping Cart Operations")
struct ShoppingCartTests {
    let cart: ShoppingCart

    // init acts as setUp -- runs before each test in the suite
    init() {
        cart = ShoppingCart()
        cart.add(Product(name: "Widget", price: 9.99))
    }

    @Test func itemCount() {
        #expect(cart.items.count == 1)
    }

    @Test func totalPrice() {
        #expect(cart.total == 9.99)
    }
}
```

### Suite-Level Setup and Teardown

Use `init` for setup and `deinit` for teardown. For async cleanup, use a `TestScoping` trait:

```swift
@Suite(.tags(.database))
struct DatabaseTests {
    let db: TestDatabase

    init() async throws {
        db = try await TestDatabase.createTemporary()
    }

    // deinit works for synchronous cleanup (struct suites only use init)
    // For async teardown, use TestScoping trait instead

    @Test func insertRecord() async throws {
        try await db.insert(Record(id: 1, name: "Test"))
        let count = try await db.count()
        #expect(count == 1)
    }
}
```

## Async Testing Patterns

### Testing Async Functions

`@Test` functions can be `async` and `throws` directly:

```swift
@Test func fetchUserProfile() async throws {
    let service = UserService(client: MockHTTPClient())
    let user = try await service.fetchProfile(id: 42)
    #expect(user.name == "Alice")
}
```

### Testing Actor-Isolated Code

Access actor-isolated state with `await`:

```swift
actor Counter {
    private(set) var value = 0
    func increment() { value += 1 }
}

@Test func counterIncrements() async {
    let counter = Counter()
    await counter.increment()
    await counter.increment()
    let value = await counter.value
    #expect(value == 2)
}
```

### Timeout for Hanging Tests

Use `.timeLimit` to prevent tests from hanging indefinitely:

```swift
@Test(.timeLimit(.seconds(5)))
func networkCallCompletes() async throws {
    let result = try await api.fetchData()
    #expect(result.isEmpty == false)
}
```

If the test exceeds the time limit, it fails immediately with a clear timeout diagnostic.

### Confirmation (Replacing XCTestExpectation)

`confirmation` replaces `XCTestExpectation` / `fulfill()` / `waitForExpectations`. It verifies that an event occurs the expected number of times:

```swift
@Test func notificationPosted() async throws {
    // Expects the closure to call confirm() exactly once
    try await confirmation("UserDidLogin posted") { confirm in
        let center = NotificationCenter.default
        let observer = center.addObserver(
            forName: .userDidLogin, object: nil, queue: .main
        ) { _ in
            confirm()
        }
        await loginService.login(user: "test", password: "pass")
        center.removeObserver(observer)
    }
}

// Expect multiple confirmations
@Test func batchProcessing() async throws {
    try await confirmation("Items processed", expectedCount: 3) { confirm in
        processor.onItemComplete = { _ in confirm() }
        await processor.process(items: [a, b, c])
    }
}
```

## Traits In Depth

### Conditional Traits

```swift
// Enable only on CI
@Test(.enabled(if: ProcessInfo.processInfo.environment["CI"] != nil))
func integrationTest() async throws { ... }

// Disable with a reason
@Test(.disabled("Blocked by #123 -- server migration"))
func brokenEndpoint() async throws { ... }

// Bug reference -- links test to an issue tracker
@Test(.bug("https://github.com/org/repo/issues/42", "Intermittent timeout"))
func flakyNetworkTest() async throws { ... }
```

### Time Limits

```swift
@Test(.timeLimit(.minutes(2)))
func longRunningImport() async throws {
    try await importer.importLargeDataset()
}

// Apply time limit to entire suite
@Suite(.timeLimit(.seconds(30)))
struct FastTests {
    @Test func quick1() { ... }
    @Test func quick2() { ... }
}
```

### Custom Trait Definitions

Create reusable traits for common test configurations:

```swift
struct DatabaseTrait: TestTrait, SuiteTrait, TestScoping {
    func provideScope(
        for test: Test,
        testCase: Test.Case?,
        performing function: @Sendable () async throws -> Void
    ) async throws {
        let db = try await TestDatabase.setUp()
        defer { Task { await db.tearDown() } }
        try await function()
    }
}

extension Trait where Self == DatabaseTrait {
    static var database: Self { .init() }
}

// Usage: any test with .database trait gets a fresh database
@Test(.database)
func insertUser() async throws { ... }
```

## Common Mistakes

1. **Testing implementation, not behavior.** Test what the code does, not how.
2. **No error path tests.** If a function can throw, test the throw path.
3. **Flaky async tests.** Use `confirmation` with expected counts, not `sleep` calls.
4. **Shared mutable state between tests.** Each test sets up its own state via `init()` in `@Suite`.
5. **Missing accessibility identifiers in UI tests.** XCUITest queries rely on them.
6. **Using `sleep` in tests.** Use `confirmation`, clock injection, or `withKnownIssue`.
7. **Not testing cancellation.** If code supports `Task` cancellation, verify it cancels cleanly.
8. **Mixing XCTest and Swift Testing in one file.** Keep them in separate files.
9. **Non-Sendable test helpers shared across tests.** Ensure test helper types are Sendable when shared across concurrent test cases. Annotate MainActor-dependent test code with `@MainActor`.

## Test Attachments

Attach diagnostic data to test results for debugging failures. See `references/testing-patterns.md` for full examples.

```swift
@Test func generateReport() async throws {
    let report = try generateReport()
    Attachment(report.data, named: "report.json").record()
    #expect(report.isValid)
}
```

## Exit Testing

Test code that calls `exit()`, `fatalError()`, or `preconditionFailure()`. See `references/testing-patterns.md` for details.

```swift
@Test func invalidInputCausesExit() async {
    await #expect(processExitsWith: .failure) {
        processInvalidInput()  // calls fatalError()
    }
}
```

## Review Checklist

- [ ] All new tests use Swift Testing (`@Test`, `#expect`), not XCTest assertions
- [ ] Test names describe behavior (`fetchUserReturnsNilOnNetworkError` not `testFetchUser`)
- [ ] Error paths have dedicated tests
- [ ] Async tests use `confirmation()`, not `Task.sleep`
- [ ] Parameterized tests used for repetitive variations
- [ ] Tags applied for filtering (`.critical`, `.slow`)
- [ ] Mocks conform to protocols, not subclass concrete types
- [ ] No shared mutable state between tests
- [ ] Cancellation tested for cancellable async operations

## References

- Testing patterns: `references/testing-patterns.md`
