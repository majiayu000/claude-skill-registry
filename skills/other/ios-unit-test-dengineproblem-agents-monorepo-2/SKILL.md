---
name: ios-unit-test
description: Эксперт iOS тестирования. Используй для XCTest, UI testing и iOS test patterns.
---

# iOS Unit Testing Expert

Expert in iOS testing with XCTest framework and best practices.

## Core Testing Principles

### Test Structure and Organization

- Follow the Arrange-Act-Assert (AAA) pattern
- Use descriptive test method names explaining scenario and expected outcome
- Group related tests using nested test classes or test suites
- Maintain test independence - each test should run in isolation

### XCTest Framework Fundamentals

```swift
import XCTest
@testable import YourApp

class UserServiceTests: XCTestCase {
    // System Under Test
    var sut: UserService!
    var mockNetworkManager: MockNetworkManager!

    override func setUpWithError() throws {
        try super.setUpWithError()
        mockNetworkManager = MockNetworkManager()
        sut = UserService(networkManager: mockNetworkManager)
    }

    override func tearDownWithError() throws {
        sut = nil
        mockNetworkManager = nil
        try super.tearDownWithError()
    }

    // MARK: - fetchUser Tests

    func test_fetchUser_withValidId_returnsUser() async throws {
        // Arrange
        let expectedUser = User(id: "123", name: "John Doe")
        mockNetworkManager.fetchUserResult = .success(expectedUser)

        // Act
        let result = try await sut.fetchUser(id: "123")

        // Assert
        XCTAssertEqual(result.id, expectedUser.id)
        XCTAssertEqual(result.name, expectedUser.name)
        XCTAssertEqual(mockNetworkManager.fetchUserCallCount, 1)
        XCTAssertEqual(mockNetworkManager.lastFetchedUserId, "123")
    }

    func test_fetchUser_withInvalidId_throwsError() async {
        // Arrange
        mockNetworkManager.fetchUserResult = .failure(NetworkError.notFound)

        // Act & Assert
        do {
            _ = try await sut.fetchUser(id: "invalid")
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertTrue(error is NetworkError)
            XCTAssertEqual(error as? NetworkError, .notFound)
        }
    }
}
```

## Mocking and Dependency Injection

### Protocol-Based Mocking

```swift
// Protocol definition
protocol NetworkManagerProtocol {
    func fetchUser(id: String) async throws -> User
    func saveUser(_ user: User) async throws
}

// Mock implementation
class MockNetworkManager: NetworkManagerProtocol {
    // Call tracking
    var fetchUserCallCount = 0
    var lastFetchedUserId: String?
    var saveUserCallCount = 0
    var lastSavedUser: User?

    // Configurable results
    var fetchUserResult: Result<User, Error>?
    var saveUserResult: Result<Void, Error> = .success(())

    func fetchUser(id: String) async throws -> User {
        fetchUserCallCount += 1
        lastFetchedUserId = id

        switch fetchUserResult {
        case .success(let user):
            return user
        case .failure(let error):
            throw error
        case .none:
            throw TestError.noMockResult
        }
    }

    func saveUser(_ user: User) async throws {
        saveUserCallCount += 1
        lastSavedUser = user

        switch saveUserResult {
        case .success:
            return
        case .failure(let error):
            throw error
        }
    }

    // Reset for reuse
    func reset() {
        fetchUserCallCount = 0
        lastFetchedUserId = nil
        saveUserCallCount = 0
        lastSavedUser = nil
        fetchUserResult = nil
        saveUserResult = .success(())
    }
}

enum TestError: Error {
    case noMockResult
}
```

### Spy Pattern

```swift
class NetworkManagerSpy: NetworkManagerProtocol {
    private(set) var messages: [Message] = []

    enum Message: Equatable {
        case fetchUser(id: String)
        case saveUser(User)
    }

    var stubbedFetchUserResult: Result<User, Error> = .failure(TestError.noMockResult)

    func fetchUser(id: String) async throws -> User {
        messages.append(.fetchUser(id: id))
        return try stubbedFetchUserResult.get()
    }

    func saveUser(_ user: User) async throws {
        messages.append(.saveUser(user))
    }
}
```

## Async Testing Patterns

### Testing async/await Code

```swift
func test_fetchUser_withValidId_returnsUser() async throws {
    // Arrange
    let expectedUser = User(id: "123", name: "John Doe")
    mockNetworkManager.fetchUserResult = .success(expectedUser)

    // Act
    let result = try await sut.fetchUser(id: "123")

    // Assert
    XCTAssertEqual(result, expectedUser)
}

func test_fetchUser_withNetworkError_throwsError() async {
    // Arrange
    mockNetworkManager.fetchUserResult = .failure(NetworkError.connectionFailed)

    // Act & Assert
    await XCTAssertThrowsError(try await sut.fetchUser(id: "123")) { error in
        XCTAssertEqual(error as? NetworkError, .connectionFailed)
    }
}
```

### Testing with Expectations

```swift
func test_notificationObserver_receivesNotification() {
    // Arrange
    let expectation = XCTestExpectation(description: "Notification received")
    let notificationName = Notification.Name("TestNotification")

    let observer = NotificationCenter.default.addObserver(
        forName: notificationName,
        object: nil,
        queue: nil
    ) { _ in
        expectation.fulfill()
    }

    // Act
    NotificationCenter.default.post(name: notificationName, object: nil)

    // Assert
    wait(for: [expectation], timeout: 1.0)

    // Cleanup
    NotificationCenter.default.removeObserver(observer)
}

func test_delegateCallback_isCalledOnSuccess() {
    // Arrange
    let expectation = XCTestExpectation(description: "Delegate called")
    let mockDelegate = MockDelegate()
    mockDelegate.onSuccessCalled = { expectation.fulfill() }
    sut.delegate = mockDelegate

    // Act
    sut.performOperation()

    // Assert
    wait(for: [expectation], timeout: 2.0)
    XCTAssertTrue(mockDelegate.successCallCount == 1)
}
```

### Testing Combine Publishers

```swift
import Combine

func test_userPublisher_emitsUser() {
    // Arrange
    var receivedUser: User?
    var receivedError: Error?
    let expectation = XCTestExpectation(description: "Publisher emits")

    let cancellable = sut.userPublisher
        .sink(
            receiveCompletion: { completion in
                if case .failure(let error) = completion {
                    receivedError = error
                }
                expectation.fulfill()
            },
            receiveValue: { user in
                receivedUser = user
            }
        )

    // Act
    sut.loadUser(id: "123")

    // Assert
    wait(for: [expectation], timeout: 2.0)
    XCTAssertNotNil(receivedUser)
    XCTAssertNil(receivedError)
    cancellable.cancel()
}
```

## View Controller Testing

```swift
class LoginViewControllerTests: XCTestCase {
    var sut: LoginViewController!
    var mockAuthService: MockAuthService!

    override func setUpWithError() throws {
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        sut = storyboard.instantiateViewController(
            withIdentifier: "LoginViewController"
        ) as? LoginViewController

        mockAuthService = MockAuthService()
        sut.authService = mockAuthService

        // Load view hierarchy
        sut.loadViewIfNeeded()
    }

    override func tearDownWithError() throws {
        sut = nil
        mockAuthService = nil
    }

    func test_outlets_areConnected() {
        XCTAssertNotNil(sut.emailTextField)
        XCTAssertNotNil(sut.passwordTextField)
        XCTAssertNotNil(sut.loginButton)
        XCTAssertNotNil(sut.errorLabel)
    }

    func test_loginButton_tap_callsAuthService() {
        // Arrange
        sut.emailTextField.text = "test@example.com"
        sut.passwordTextField.text = "password123"

        // Act
        sut.loginButton.sendActions(for: .touchUpInside)

        // Assert
        XCTAssertEqual(mockAuthService.loginCallCount, 1)
        XCTAssertEqual(mockAuthService.lastLoginEmail, "test@example.com")
        XCTAssertEqual(mockAuthService.lastLoginPassword, "password123")
    }

    func test_loginButton_withEmptyEmail_showsError() {
        // Arrange
        sut.emailTextField.text = ""
        sut.passwordTextField.text = "password"

        // Act
        sut.loginButton.sendActions(for: .touchUpInside)

        // Assert
        XCTAssertEqual(mockAuthService.loginCallCount, 0)
        XCTAssertFalse(sut.errorLabel.isHidden)
        XCTAssertEqual(sut.errorLabel.text, "Email is required")
    }

    func test_successfulLogin_navigatesToHome() {
        // Arrange
        mockAuthService.loginResult = .success(User(id: "1", name: "Test"))
        let mockNavigator = MockNavigator()
        sut.navigator = mockNavigator

        sut.emailTextField.text = "test@example.com"
        sut.passwordTextField.text = "password"

        // Act
        sut.loginButton.sendActions(for: .touchUpInside)

        // Assert
        XCTAssertTrue(mockNavigator.didNavigateToHome)
    }
}
```

## Performance Testing

```swift
func test_dataProcessing_performance() {
    let largeDataSet = generateLargeDataSet(count: 10000)

    measure {
        _ = sut.processData(largeDataSet)
    }
}

func test_dataProcessing_performanceWithOptions() {
    let options = XCTMeasureOptions()
    options.iterationCount = 10

    measure(options: options) {
        _ = sut.processData(generateLargeDataSet(count: 5000))
    }
}

func test_memoryUsage_withLargeDataSet() {
    let options = XCTMeasureOptions()
    options.iterationCount = 5

    measure(metrics: [XCTMemoryMetric()], options: options) {
        autoreleasepool {
            let data = sut.loadLargeDataSet()
            sut.processData(data)
        }
    }
}

func test_cpuUsage_duringOperation() {
    measure(metrics: [XCTCPUMetric()]) {
        sut.performCPUIntensiveOperation()
    }
}
```

## Parameterized Testing

```swift
func test_emailValidation_withVariousInputs() {
    let testCases: [(email: String, isValid: Bool)] = [
        ("valid@example.com", true),
        ("user.name@domain.co.uk", true),
        ("invalid.email", false),
        ("", false),
        ("@example.com", false),
        ("test@", false),
        ("test@.com", false),
        ("test@domain", false)
    ]

    for testCase in testCases {
        let result = sut.isValidEmail(testCase.email)
        XCTAssertEqual(
            result,
            testCase.isValid,
            "Failed for email: '\(testCase.email)' - expected \(testCase.isValid), got \(result)"
        )
    }
}

// Using XCTestCase subclass for cleaner parameterized tests
class EmailValidationTests: XCTestCase {
    struct TestCase {
        let input: String
        let expected: Bool
        let file: StaticString
        let line: UInt

        init(_ input: String, _ expected: Bool,
             file: StaticString = #file, line: UInt = #line) {
            self.input = input
            self.expected = expected
            self.file = file
            self.line = line
        }
    }

    func test_isValidEmail() {
        let testCases = [
            TestCase("test@example.com", true),
            TestCase("invalid", false),
            TestCase("", false)
        ]

        for testCase in testCases {
            let result = EmailValidator.isValid(testCase.input)
            XCTAssertEqual(result, testCase.expected,
                          file: testCase.file, line: testCase.line)
        }
    }
}
```

## UI Testing with XCUITest

```swift
class LoginUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func test_loginFlow_withValidCredentials_showsHomeScreen() {
        // Navigate to login
        let loginButton = app.buttons["LoginButton"]
        XCTAssertTrue(loginButton.waitForExistence(timeout: 5))

        // Enter credentials
        let emailField = app.textFields["EmailTextField"]
        emailField.tap()
        emailField.typeText("test@example.com")

        let passwordField = app.secureTextFields["PasswordTextField"]
        passwordField.tap()
        passwordField.typeText("password123")

        // Tap login
        loginButton.tap()

        // Verify home screen
        let homeTitle = app.staticTexts["Welcome"]
        XCTAssertTrue(homeTitle.waitForExistence(timeout: 10))
    }

    func test_loginFlow_withInvalidCredentials_showsError() {
        let emailField = app.textFields["EmailTextField"]
        emailField.tap()
        emailField.typeText("wrong@example.com")

        let passwordField = app.secureTextFields["PasswordTextField"]
        passwordField.tap()
        passwordField.typeText("wrongpassword")

        app.buttons["LoginButton"].tap()

        let errorLabel = app.staticTexts["ErrorLabel"]
        XCTAssertTrue(errorLabel.waitForExistence(timeout: 5))
        XCTAssertEqual(errorLabel.label, "Invalid credentials")
    }
}
```

## Test Configuration

### Test Scheme Setup

```yaml
test_scheme_configuration:
  unit_tests:
    targets: ["YourAppTests"]
    coverage: true
    parallel: true

  ui_tests:
    targets: ["YourAppUITests"]
    coverage: false
    parallel: false
    launch_arguments: ["--uitesting", "--reset-state"]

  integration_tests:
    targets: ["YourAppIntegrationTests"]
    coverage: true
    parallel: false
```

### Test Plan Configuration

```json
{
  "configurations" : [
    {
      "name" : "Unit Tests",
      "options" : {
        "targetForVariableExpansion" : { "target" : { "name" : "YourApp" } }
      }
    }
  ],
  "defaultOptions" : {
    "codeCoverage" : true,
    "testTimeoutsEnabled" : true,
    "defaultTestExecutionTimeAllowance" : 60
  },
  "testTargets" : [
    { "target" : { "name" : "YourAppTests" } }
  ],
  "version" : 1
}
```

## Лучшие практики

1. **AAA Pattern** — Arrange, Act, Assert для каждого теста
2. **One assertion per test** — один логический assert на тест
3. **Descriptive names** — `test_methodName_condition_expectedResult`
4. **Test isolation** — каждый тест независим от других
5. **Mock external dependencies** — сеть, БД, системные сервисы
6. **Fast tests** — unit tests должны выполняться за миллисекунды
