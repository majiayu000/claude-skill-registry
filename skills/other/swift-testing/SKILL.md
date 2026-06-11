---
name: swift-testing
description: "Swift testing: XCTest, Swift Testing framework, async patterns."
user-invocable: false
context: fork
agent: swift-general-engineer
routing:
  triggers:
    - "swift testing"
    - "XCTest"
    - "Swift Testing framework"
    - "async test swift"
  category: swift
  pairs_with:
    - swift-concurrency
    - test-driven-development
---

# Swift Testing Patterns

## XCTest Basics

XCTest is Apple's foundational testing framework. Every test class inherits from `XCTestCase` and uses `setUp`/`tearDown` for lifecycle management.

```swift
import XCTest
@testable import MyApp

final class UserServiceTests: XCTestCase {
    var sut: UserService!
    var mockStore: MockUserStore!

    override func setUp() {
        super.setUp()
        mockStore = MockUserStore()
        sut = UserService(store: mockStore)
    }

    override func tearDown() {
        sut = nil
        mockStore = nil
        super.tearDown()
    }

    func testFetchUser_withValidID_returnsUser() {
        mockStore.stubbedUser = User(id: "1", name: "Alice")

        let user = sut.fetchUser(id: "1")

        XCTAssertNotNil(user)
        XCTAssertEqual(user?.name, "Alice")
    }

    func testFetchUser_withInvalidID_returnsNil() {
        mockStore.stubbedUser = nil

        let user = sut.fetchUser(id: "unknown")

        XCTAssertNil(user)
    }
}
```

## Swift Testing Framework (Swift 5.9+)

The Swift Testing framework replaces XCTest with a more expressive, macro-driven approach. Use `@Test` for individual tests, `#expect` for assertions, and `@Suite` for grouping.

```swift
import Testing
@testable import MyApp

@Suite("User Service")
struct UserServiceTests {
    let mockStore = MockUserStore()

    @Test("fetches user by valid ID")
    func fetchValidUser() {
        mockStore.stubbedUser = User(id: "1", name: "Alice")
        let service = UserService(store: mockStore)

        let user = service.fetchUser(id: "1")

        #expect(user?.name == "Alice")
    }

    @Test("returns nil for unknown ID")
    func fetchUnknownUser() {
        mockStore.stubbedUser = nil
        let service = UserService(store: mockStore)

        #expect(service.fetchUser(id: "unknown") == nil)
    }
}
```

### Parameterized Tests

Swift Testing supports parameterized tests natively, eliminating boilerplate for table-driven patterns.

```swift
@Test("validates email formats", arguments: [
    ("alice@example.com", true),
    ("bob@", false),
    ("", false),
    ("valid+tag@sub.domain.com", true),
])
func emailValidation(email: String, isValid: Bool) {
    #expect(EmailValidator.isValid(email) == isValid)
}
```

## Async Testing

### Async Test Methods (XCTest)

XCTest supports `async` test methods directly. For callback-based APIs, use `XCTestExpectation`.

```swift
// Direct async/await support
func testFetchProfile_async() async throws {
    let service = ProfileService(client: MockHTTPClient())

    let profile = try await service.fetchProfile(userID: "1")

    XCTAssertEqual(profile.name, "Alice")
}

// Callback-based APIs with expectations
func testFetchProfile_callback() {
    let expectation = expectation(description: "Profile fetched")
    let service = ProfileService(client: MockHTTPClient())

    service.fetchProfile(userID: "1") { result in
        switch result {
        case .success(let profile):
            XCTAssertEqual(profile.name, "Alice")
        case .failure(let error):
            XCTFail("Unexpected error: \(error)")
        }
        expectation.fulfill()
    }

    waitForExpectations(timeout: 5)
}
```

### Async Tests with Swift Testing

```swift
@Test("fetches profile asynchronously")
func fetchProfileAsync() async throws {
    let service = ProfileService(client: MockHTTPClient())

    let profile = try await service.fetchProfile(userID: "1")

    #expect(profile.name == "Alice")
}
```

## UI Testing

UI tests use `XCUIApplication` to interact with the app as a user would. Always prefer accessibility identifiers over text matching for resilient tests.

```swift
final class LoginUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func testSuccessfulLogin() {
        let emailField = app.textFields["login.emailField"]
        let passwordField = app.secureTextFields["login.passwordField"]
        let loginButton = app.buttons["login.submitButton"]

        emailField.tap()
        emailField.typeText("alice@example.com")

        passwordField.tap()
        passwordField.typeText("password123")

        loginButton.tap()

        let welcomeLabel = app.staticTexts["home.welcomeLabel"]
        XCTAssertTrue(welcomeLabel.waitForExistence(timeout: 5))
        XCTAssertEqual(welcomeLabel.label, "Welcome, Alice")
    }
}
```

Set accessibility identifiers in production code:

```swift
emailTextField.accessibilityIdentifier = "login.emailField"
passwordTextField.accessibilityIdentifier = "login.passwordField"
submitButton.accessibilityIdentifier = "login.submitButton"
```

## Test Doubles: Protocol-Based Mocking

Swift's protocol-oriented design makes mocking straightforward. Define dependencies as protocols, then provide mock implementations in tests.

```swift
// Production protocol
protocol HTTPClient {
    func data(from url: URL) async throws -> (Data, URLResponse)
}

// Production implementation
struct URLSessionHTTPClient: HTTPClient {
    let session: URLSession

    func data(from url: URL) async throws -> (Data, URLResponse) {
        try await session.data(from: url)
    }
}

// Test double
final class MockHTTPClient: HTTPClient {
    var stubbedData: Data = Data()
    var stubbedResponse: URLResponse = HTTPURLResponse()
    var capturedURLs: [URL] = []

    func data(from url: URL) async throws -> (Data, URLResponse) {
        capturedURLs.append(url)
        return (stubbedData, stubbedResponse)
    }
}
```

### Dependency Injection

Inject dependencies through initializers to make classes testable:

```swift
final class ProfileService {
    private let client: HTTPClient

    init(client: HTTPClient) {
        self.client = client
    }

    func fetchProfile(userID: String) async throws -> Profile {
        let url = URL(string: "https://api.example.com/users/\(userID)")!
        let (data, _) = try await client.data(from: url)
        return try JSONDecoder().decode(Profile.self, from: data)
    }
}
```

## Key Conventions

- **One assertion per concept** -- a single test can have multiple assertions if they verify the same logical behavior, but avoid testing unrelated things together.
- **Arrange-Act-Assert** -- structure every test into setup, execution, and verification phases.
- **Name tests descriptively** -- `testFetchUser_withExpiredToken_throwsAuthError` is better than `testFetch2`.
- **Prefer Swift Testing for new code** -- use `@Test` and `#expect` when targeting Swift 5.9+; fall back to XCTest for older targets or UI tests.
- **Ensure test independence** -- each test must be runnable in isolation; always produce self-contained test state.
