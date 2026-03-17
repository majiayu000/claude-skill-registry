---
name: mobile-app-testing
description: Comprehensive mobile app testing strategies for iOS and Android. Covers unit tests, UI tests, integration tests, performance testing, and test automation with Detox, Appium, and XCTest.
---

# Mobile App Testing

## Overview

Implement comprehensive testing strategies for mobile applications including unit tests, UI tests, integration tests, and performance testing.

## When to Use

- Creating reliable mobile applications with test coverage
- Automating UI testing across iOS and Android
- Performance testing and optimization
- Integration testing with backend services
- Regression testing before releases

## Instructions

### 1. **React Native Testing with Jest & Detox**

```javascript
// Unit test with Jest
import { calculate } from '../utils/math';

describe('Math utilities', () => {
  test('should add two numbers', () => {
    expect(calculate.add(2, 3)).toBe(5);
  });

  test('should handle negative numbers', () => {
    expect(calculate.add(-2, 3)).toBe(1);
  });
});

// Component unit test
import React from 'react';
import { render, screen } from '@testing-library/react-native';
import { UserProfile } from '../components/UserProfile';

describe('UserProfile Component', () => {
  test('renders user name correctly', () => {
    const mockUser = { id: '1', name: 'John Doe', email: 'john@example.com' };
    render(<UserProfile user={mockUser} />);

    expect(screen.getByText('John Doe')).toBeTruthy();
  });

  test('handles missing user gracefully', () => {
    render(<UserProfile user={null} />);
    expect(screen.getByText(/no user data/i)).toBeTruthy();
  });
});

// E2E Testing with Detox
describe('Login Flow E2E Test', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should login successfully with valid credentials', async () => {
    await waitFor(element(by.id('emailInput')))
      .toBeVisible()
      .withTimeout(5000);

    await element(by.id('emailInput')).typeText('user@example.com');
    await element(by.id('passwordInput')).typeText('password123');
    await element(by.id('loginButton')).multiTap();

    await waitFor(element(by.text('Home Feed')))
      .toBeVisible()
      .withTimeout(5000);
  });

  it('should show error with invalid credentials', async () => {
    await element(by.id('emailInput')).typeText('invalid@example.com');
    await element(by.id('passwordInput')).typeText('wrongpass');
    await element(by.id('loginButton')).multiTap();

    await waitFor(element(by.text(/invalid credentials/i)))
      .toBeVisible()
      .withTimeout(5000);
  });

  it('should navigate between tabs', async () => {
    await element(by.id('profileTab')).tap();
    await waitFor(element(by.text('Profile')))
      .toBeVisible()
      .withTimeout(2000);

    await element(by.id('homeTab')).tap();
    await waitFor(element(by.text('Home Feed')))
      .toBeVisible()
      .withTimeout(2000);
  });
});
```

### 2. **iOS Testing with XCTest**

```swift
import XCTest
@testable import MyApp

class UserViewModelTests: XCTestCase {
  var viewModel: UserViewModel!
  var mockNetworkService: MockNetworkService!

  override func setUp() {
    super.setUp()
    mockNetworkService = MockNetworkService()
    viewModel = UserViewModel(networkService: mockNetworkService)
  }

  func testFetchUserSuccess() async {
    let expectedUser = User(id: UUID(), name: "John", email: "john@example.com")
    mockNetworkService.mockUser = expectedUser

    await viewModel.fetchUser(id: expectedUser.id)

    XCTAssertEqual(viewModel.user?.name, "John")
    XCTAssertNil(viewModel.errorMessage)
    XCTAssertFalse(viewModel.isLoading)
  }

  func testFetchUserFailure() async {
    mockNetworkService.shouldFail = true

    await viewModel.fetchUser(id: UUID())

    XCTAssertNil(viewModel.user)
    XCTAssertNotNil(viewModel.errorMessage)
    XCTAssertFalse(viewModel.isLoading)
  }
}

class MockNetworkService: NetworkService {
  var mockUser: User?
  var shouldFail = false

  override func fetch<T: Decodable>(
    _: T.Type,
    from endpoint: String
  ) async throws -> T {
    if shouldFail {
      throw NetworkError.unknown
    }
    return mockUser as! T
  }
}

// UI Test
class LoginUITests: XCTestCase {
  override func setUp() {
    super.setUp()
    continueAfterFailure = false
    XCUIApplication().launch()
  }

  func testLoginFlow() {
    let app = XCUIApplication()

    let emailTextField = app.textFields["emailInput"]
    let passwordTextField = app.secureTextFields["passwordInput"]
    let loginButton = app.buttons["loginButton"]

    emailTextField.tap()
    emailTextField.typeText("user@example.com")

    passwordTextField.tap()
    passwordTextField.typeText("password123")

    loginButton.tap()

    let homeText = app.staticTexts["Home Feed"]
    XCTAssertTrue(homeText.waitForExistence(timeout: 5))
  }

  func testNavigationBetweenTabs() {
    let app = XCUIApplication()
    let profileTab = app.tabBars.buttons["Profile"]
    let homeTab = app.tabBars.buttons["Home"]

    profileTab.tap()
    XCTAssertTrue(app.staticTexts["Profile"].exists)

    homeTab.tap()
    XCTAssertTrue(app.staticTexts["Home"].exists)
  }
}
```

### 3. **Android Testing with Espresso**

```kotlin
@RunWith(AndroidJUnit4::class)
class UserViewModelTest {
  private lateinit var viewModel: UserViewModel
  private val mockApiService = mock<ApiService>()

  @Before
  fun setUp() {
    viewModel = UserViewModel(mockApiService)
  }

  @Test
  fun fetchUserSuccess() = runTest {
    val expectedUser = User("1", "John", "john@example.com")
    `when`(mockApiService.getUser("1")).thenReturn(expectedUser)

    viewModel.fetchUser("1")

    assertEquals(expectedUser.name, viewModel.user.value?.name)
    assertEquals(null, viewModel.errorMessage.value)
  }

  @Test
  fun fetchUserFailure() = runTest {
    `when`(mockApiService.getUser("1"))
      .thenThrow(IOException("Network error"))

    viewModel.fetchUser("1")

    assertEquals(null, viewModel.user.value)
    assertNotNull(viewModel.errorMessage.value)
  }
}

// UI Test with Espresso
@RunWith(AndroidJUnit4::class)
class LoginActivityTest {
  @get:Rule
  val activityRule = ActivityScenarioRule(LoginActivity::class.java)

  @Test
  fun testLoginWithValidCredentials() {
    onView(withId(R.id.emailInput))
      .perform(typeText("user@example.com"))

    onView(withId(R.id.passwordInput))
      .perform(typeText("password123"))

    onView(withId(R.id.loginButton))
      .perform(click())

    onView(withText("Home"))
      .check(matches(isDisplayed()))
  }

  @Test
  fun testLoginWithInvalidCredentials() {
    onView(withId(R.id.emailInput))
      .perform(typeText("invalid@example.com"))

    onView(withId(R.id.passwordInput))
      .perform(typeText("wrongpassword"))

    onView(withId(R.id.loginButton))
      .perform(click())

    onView(withText(containsString("Invalid credentials")))
      .check(matches(isDisplayed()))
  }

  @Test
  fun testNavigationBetweenTabs() {
    onView(withId(R.id.profileTab)).perform(click())
    onView(withText("Profile")).check(matches(isDisplayed()))

    onView(withId(R.id.homeTab)).perform(click())
    onView(withText("Home")).check(matches(isDisplayed()))
  }
}
```

### 4. **Performance Testing**

```swift
import XCTest

class PerformanceTests: XCTestCase {
  func testListRenderingPerformance() {
    let viewModel = ItemsViewModel()
    viewModel.items = (0..<1000).map { i in
      Item(id: UUID(), title: "Item \(i)", price: Double(i))
    }

    measure {
      _ = viewModel.items.filter { $0.price > 50 }
    }
  }

  func testNetworkResponseTime() {
    let networkService = NetworkService()

    measure {
      let expectation = XCTestExpectation(description: "Fetch user")

      Task {
        do {
          _ = try await networkService.fetch(User.self, from: "/users/test")
          expectation.fulfill()
        } catch {
          XCTFail("Network request failed")
        }
      }

      wait(for: [expectation], timeout: 10)
    }
  }
}
```

## Best Practices

### ✅ DO
- Write tests for business logic first
- Use dependency injection for testability
- Mock external API calls
- Test both success and failure paths
- Automate UI testing for critical flows
- Run tests on real devices
- Measure performance on target devices
- Keep tests isolated and independent
- Use meaningful test names
- Maintain >80% code coverage

### ❌ DON'T
- Skip testing UI-critical flows
- Use hardcoded test data
- Ignore performance regressions
- Test implementation details
- Make tests flaky or unreliable
- Skip testing on actual devices
- Ignore accessibility testing
- Create interdependent tests
- Test without mocking APIs
- Deploy untested code
