---
name: xctest-patterns
description: "Expert XCTest decisions for iOS/tvOS: test type selection trade-offs, mock vs stub vs spy judgment calls, async testing pitfalls, and coverage threshold calibration. Use when designing test strategy, debugging flaky tests, or deciding what to test. Trigger keywords: XCTest, unit test, integration test, UI test, mock, stub, spy, async test, expectation, test coverage, XCUITest, TDD, test pyramid"
version: "3.0.0"
---

# XCTest Patterns — Expert Decisions

Expert decision frameworks for testing choices. Claude knows XCTest syntax — this skill provides judgment calls for test strategy and mock design.

---

## Decision Trees

### Test Type Selection

```
What are you testing?
├─ Pure business logic (no I/O, no UI)
│  └─ Unit test
│     Fast, isolated, many of these
│
├─ Component interactions (services, repositories)
│  └─ Integration test
│     Test real interactions, fewer than unit
│
├─ User-visible behavior
│  └─ Does it require visual verification?
│     ├─ YES → Snapshot test or manual QA
│     └─ NO → UI test (XCUITest)
│        Slowest, fewest of these
│
└─ Performance characteristics
   └─ Performance test with measure {}
```

### Mock vs Stub vs Spy

```
What do you need from the test double?
├─ Just return canned data
│  └─ Stub
│     Simplest, no verification
│
├─ Verify interactions (was method called?)
│  └─ Spy
│     Records calls, verifiable
│
└─ Both return data AND verify calls
   └─ Mock (stub + spy)
      Most flexible, most complex
```

### When to Mock

```
Is this dependency...
├─ External (network, database, filesystem)?
│  └─ Always mock
│     Tests must be fast and deterministic
│
├─ Internal but slow or stateful?
│  └─ Mock if it makes test significantly faster
│
└─ Internal and fast?
   └─ Consider using real implementation
      Integration coverage > isolation purity
```

### Async Test Strategy

```
Is the async operation...
├─ Returning a value (async/await)?
│  └─ Use async test function
│     func testFetch() async throws { }
│
├─ Using completion handlers?
│  └─ Use XCTestExpectation
│     expectation.fulfill() in callback
│
└─ Publishing via Combine?
   └─ Use XCTestExpectation + sink
      Or use async-aware Combine helpers
```

---

## NEVER Do

### Test Design

**NEVER** test implementation details:
```swift
// ❌ Testing internal state
func testLogin() async {
    await sut.login(email: "test@example.com", password: "pass")

    XCTAssertEqual(sut.authService.callCount, 1)  // Implementation detail!
    XCTAssertEqual(sut.lastRequestTimestamp, Date())  // Internal state!
}

// ✅ Test observable behavior
func testLoginSuccess_SetsAuthenticatedState() async {
    await sut.login(email: "test@example.com", password: "pass")

    XCTAssertTrue(sut.isAuthenticated)  // Observable state
}
```

**NEVER** write tests that depend on execution order:
```swift
// ❌ Tests depend on each other
func testA_AddItem() {
    sut.add(item)  // sut state modified
    XCTAssertEqual(sut.count, 1)
}

func testB_RemoveItem() {
    // Depends on testA running first!
    sut.remove(item)
    XCTAssertEqual(sut.count, 0)
}

// ✅ Each test sets up its own state
func testRemoveItem() {
    sut.add(item)  // Explicit setup
    sut.remove(item)
    XCTAssertEqual(sut.count, 0)
}
```

**NEVER** use sleep() in tests:
```swift
// ❌ Flaky and slow
func testAsyncOperation() {
    sut.startOperation()
    Thread.sleep(forTimeInterval: 2.0)  // Arbitrary wait!
    XCTAssertTrue(sut.isComplete)
}

// ✅ Use expectations or async/await
func testAsyncOperation() async {
    await sut.startOperation()
    XCTAssertTrue(sut.isComplete)
}

// Or with expectations
func testAsyncOperation() {
    let expectation = expectation(description: "Operation completes")
    sut.startOperation { expectation.fulfill() }
    wait(for: [expectation], timeout: 5.0)
}
```

### Mock Design

**NEVER** create mocks that have real side effects:
```swift
// ❌ Mock does real work
final class MockNetworkService: NetworkServiceProtocol {
    func fetch(_ url: URL) async throws -> Data {
        try await URLSession.shared.data(from: url).0  // Real network!
    }
}

// ✅ Mock returns stubbed data
final class MockNetworkService: NetworkServiceProtocol {
    var stubbedData: Data = Data()
    var stubbedError: Error?

    func fetch(_ url: URL) async throws -> Data {
        if let error = stubbedError { throw error }
        return stubbedData
    }
}
```

**NEVER** verify everything in mocks:
```swift
// ❌ Over-specified — breaks if implementation changes
func testLogin() async {
    await sut.login()

    XCTAssertEqual(mockService.loginCallCount, 1)
    XCTAssertEqual(mockService.setTokenCallCount, 1)
    XCTAssertEqual(mockService.logAnalyticsCallCount, 1)
    XCTAssertEqual(mockService.updateUserCallCount, 1)
    // 10 more assertions...
}

// ✅ Verify only what matters for this test
func testLogin_StoresToken() async {
    await sut.login()
    XCTAssertNotNil(mockTokenStore.storedToken)
}
```

### Async Testing

**NEVER** forget to await async operations:
```swift
// ❌ Test passes before async work completes
func testFetchUser() {
    Task {
        await sut.fetchUser()  // Runs after test ends!
    }
    XCTAssertNotNil(sut.user)  // Always fails
}

// ✅ Make test function async
func testFetchUser() async {
    await sut.fetchUser()
    XCTAssertNotNil(sut.user)
}
```

**NEVER** forget to fulfill expectations:
```swift
// ❌ Test hangs if error path doesn't fulfill
func testNetworkCall() {
    let expectation = expectation(description: "Call completes")

    sut.fetch { result in
        if case .success = result {
            expectation.fulfill()
        }
        // Error case doesn't fulfill — test hangs!
    }

    wait(for: [expectation], timeout: 5.0)
}

// ✅ Fulfill in all paths
func testNetworkCall() {
    let expectation = expectation(description: "Call completes")

    sut.fetch { result in
        // Always fulfill, assert after
        expectation.fulfill()
    }

    wait(for: [expectation], timeout: 5.0)
    // Assert on result here
}
```

### UI Testing

**NEVER** use fixed delays in UI tests:
```swift
// ❌ Flaky — element might appear faster or slower
func testLoginFlow() {
    app.buttons["login"].tap()
    Thread.sleep(forTimeInterval: 3.0)
    XCTAssertTrue(app.staticTexts["Welcome"].exists)
}

// ✅ Use waitForExistence
func testLoginFlow() {
    app.buttons["login"].tap()
    let welcome = app.staticTexts["Welcome"]
    XCTAssertTrue(welcome.waitForExistence(timeout: 5.0))
}
```

**NEVER** rely on element positions:
```swift
// ❌ Breaks if UI layout changes
let firstButton = app.buttons.element(boundBy: 0)

// ✅ Use accessibility identifiers
let loginButton = app.buttons["loginButton"]
```

---

## Essential Patterns

### Structured Mock with Spy

```swift
final class MockUserService: UserServiceProtocol {
    // Stubs
    var stubbedUser: User?
    var stubbedError: Error?

    // Spy tracking
    private(set) var fetchUserCallCount = 0
    private(set) var fetchUserLastId: String?

    func fetchUser(id: String) async throws -> User {
        fetchUserCallCount += 1
        fetchUserLastId = id

        if let error = stubbedError { throw error }
        guard let user = stubbedUser else {
            throw MockError.notConfigured
        }
        return user
    }

    // Verification helpers
    func verify(fetchUserCalledWith id: String) -> Bool {
        fetchUserLastId == id
    }
}
```

### ViewModel Test Pattern

```swift
@MainActor
final class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockService: MockUserService!

    override func setUp() {
        super.setUp()
        mockService = MockUserService()
        sut = UserViewModel(userService: mockService)
    }

    override func tearDown() {
        sut = nil
        mockService = nil
        super.tearDown()
    }

    // Test initial state
    func testInitialState() {
        XCTAssertNil(sut.user)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.errorMessage)
    }

    // Test success path
    func testFetchUser_Success() async {
        mockService.stubbedUser = User(id: "1", name: "John")

        await sut.fetchUser(id: "1")

        XCTAssertEqual(sut.user?.name, "John")
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.errorMessage)
    }

    // Test error path
    func testFetchUser_Error() async {
        mockService.stubbedError = NetworkError.timeout

        await sut.fetchUser(id: "1")

        XCTAssertNil(sut.user)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNotNil(sut.errorMessage)
    }
}
```

### Test Data Builder

```swift
final class UserBuilder {
    private var id = "test-id"
    private var name = "Test User"
    private var email = "test@example.com"
    private var isActive = true

    func withId(_ id: String) -> Self {
        self.id = id
        return self
    }

    func withName(_ name: String) -> Self {
        self.name = name
        return self
    }

    func inactive() -> Self {
        self.isActive = false
        return self
    }

    func build() -> User {
        User(id: id, name: name, email: email, isActive: isActive)
    }
}

// Usage
let activeUser = UserBuilder().build()
let inactiveUser = UserBuilder().inactive().build()
let specificUser = UserBuilder().withId("123").withName("John").build()
```

### Async Expectation Helper

```swift
extension XCTestCase {
    func awaitPublisher<T: Publisher>(
        _ publisher: T,
        timeout: TimeInterval = 1.0,
        file: StaticString = #file,
        line: UInt = #line
    ) throws -> T.Output where T.Failure == Never {
        var result: T.Output?
        let expectation = expectation(description: "Awaiting publisher")

        let cancellable = publisher.sink { value in
            result = value
            expectation.fulfill()
        }

        wait(for: [expectation], timeout: timeout)
        cancellable.cancel()

        return try XCTUnwrap(result, file: file, line: line)
    }
}
```

---

## Quick Reference

### Test Pyramid Distribution

| Test Type | Quantity | Speed | Reliability |
|-----------|----------|-------|-------------|
| Unit | Many (70%) | Fast | High |
| Integration | Some (20%) | Medium | Medium |
| UI | Few (10%) | Slow | Lower |

### Coverage Thresholds by Layer

| Layer | Target | Rationale |
|-------|--------|-----------|
| Domain/Business Logic | 90%+ | Critical correctness |
| Services/Repositories | 85% | Error handling matters |
| ViewModels | 70-80% | State transitions |
| Views | Don't measure | Visual QA instead |

### Assertion Cheat Sheet

| Check | Assertion |
|-------|-----------|
| Equality | `XCTAssertEqual(a, b)` |
| Nil | `XCTAssertNil(x)` / `XCTAssertNotNil(x)` |
| Boolean | `XCTAssertTrue(x)` / `XCTAssertFalse(x)` |
| Throws | `XCTAssertThrowsError(try expr)` |
| No throw | `XCTAssertNoThrow(try expr)` |
| Fail | `XCTFail("message")` |

### Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Tests run > 10s | Too slow | More mocking, fewer UI tests |
| Tests fail randomly | Flaky | Remove timing dependencies |
| setUp() is huge | Tests coupled | Extract builders/helpers |
| Mock verifies everything | Over-specified | Only verify what matters |
| Tests share state | Order-dependent | Fresh sut in setUp() |
| sleep() in tests | Unreliable | Expectations or async |
| 100% coverage goal | Chasing metrics | Focus on behavior coverage |
