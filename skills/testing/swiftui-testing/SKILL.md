---
name: swiftui-testing
description: Test SwiftUI apps with XCTest, UI tests, snapshot testing, and async testing. Use when writing unit tests for ViewModels, creating UI automation tests, implementing snapshot tests, or testing async code.
user-invocable: false
---

# SwiftUI Testing

## Unit Testing ViewModels

```swift
@MainActor
final class ProfileViewModelTests: XCTestCase {
    var sut: ProfileViewModel!
    var mockRepository: MockUserRepository!

    override func setUp() {
        super.setUp()
        mockRepository = MockUserRepository()
        sut = ProfileViewModel(repository: mockRepository)
    }

    override func tearDown() {
        sut = nil
        mockRepository = nil
        super.tearDown()
    }

    func testLoadUser_Success() async {
        // Given
        let expectedUser = User(id: "1", name: "John")
        mockRepository.stubbedUser = expectedUser

        // When
        await sut.loadUser(id: "1")

        // Then
        XCTAssertEqual(sut.user, expectedUser)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.error)
    }

    func testLoadUser_Failure() async {
        // Given
        mockRepository.shouldFail = true

        // When
        await sut.loadUser(id: "1")

        // Then
        XCTAssertNil(sut.user)
        XCTAssertNotNil(sut.error)
    }
}
```

## Mock Repository Pattern

```swift
final class MockUserRepository: UserRepositoryProtocol, @unchecked Sendable {
    var stubbedUser: User?
    var shouldFail = false
    var fetchCallCount = 0

    func fetch(id: String) async throws -> User {
        fetchCallCount += 1
        if shouldFail {
            throw NSError(domain: "Test", code: -1)
        }
        return stubbedUser ?? User(id: id, name: "Test")
    }
}
```

## UI Testing with Accessibility

```swift
final class ProfileUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["UI_TESTING"]
        app.launch()
    }

    func testProfileFlow() {
        // Navigate to profile
        let profileTab = app.tabBars.buttons["Profile"]
        XCTAssertTrue(profileTab.waitForExistence(timeout: 5))
        profileTab.tap()

        // Verify content
        let nameLabel = app.staticTexts["profileNameLabel"]
        XCTAssertTrue(nameLabel.exists)

        // Edit action
        app.buttons["editButton"].tap()
        let textField = app.textFields["nameTextField"]
        textField.clearAndType("New Name")
        app.buttons["saveButton"].tap()

        // Verify update
        XCTAssertEqual(nameLabel.label, "New Name")
    }
}

extension XCUIElement {
    func clearAndType(_ text: String) {
        guard let value = self.value as? String else { return }
        tap()
        let deleteString = String(repeating: XCUIKeyboardKey.delete.rawValue,
                                  count: value.count)
        typeText(deleteString)
        typeText(text)
    }
}
```

## Snapshot Testing

```swift
import XCTest
import SnapshotTesting

final class ComponentSnapshotTests: XCTestCase {
    func testProfileCard_Light() {
        let view = ProfileCard(user: .mock)
            .frame(width: 300)

        assertSnapshot(of: view, as: .image(traits: .init(userInterfaceStyle: .light)))
    }

    func testProfileCard_Dark() {
        let view = ProfileCard(user: .mock)
            .frame(width: 300)

        assertSnapshot(of: view, as: .image(traits: .init(userInterfaceStyle: .dark)))
    }

    func testProfileCard_DynamicType() {
        let view = ProfileCard(user: .mock)
            .frame(width: 300)
            .environment(\.sizeCategory, .accessibilityExtraLarge)

        assertSnapshot(of: view, as: .image)
    }
}
```

## Testing Async Code

```swift
func testAsyncDataLoad() async throws {
    // No need for expectations with async/await
    let result = try await sut.fetchData()
    XCTAssertFalse(result.isEmpty)
}

func testTaskCancellation() async {
    let task = Task {
        try await sut.longRunningOperation()
    }

    task.cancel()

    do {
        _ = try await task.value
        XCTFail("Should throw cancellation error")
    } catch is CancellationError {
        // Expected
    }
}
```
