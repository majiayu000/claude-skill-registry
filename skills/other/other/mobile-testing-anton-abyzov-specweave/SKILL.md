---
description: Mobile testing expert across all platforms. iOS XCTest/XCUITest, Android JUnit/Espresso/Compose, React Native Jest/Detox, Flutter widget/integration tests, Maestro E2E, device farms, performance testing, accessibility. Activates for: mobile testing, XCTest, XCUITest, Espresso, Robolectric, Detox, Maestro, mobile e2e, device farm, Firebase Test Lab, AWS Device Farm, mobile CI.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
model: opus
context: fork
---

# Mobile Testing Expert

Comprehensive mobile testing expertise across **iOS**, **Android**, **React Native**, and **Flutter**. Covers the full testing pyramid from unit tests through E2E, plus CI/CD integration, device farms, performance testing, and accessibility automation.

## Fetching Current Documentation

**Before providing version-specific guidance, verify current versions.** Testing frameworks like Detox, Testing Library, and Maestro evolve frequently.

For library documentation, use WebSearch or install Context7 manually: `claude plugin install context7@claude-plugins-official`

## Test Strategy: The Mobile Testing Pyramid

```
         /  E2E  \          5-10% - Critical user flows (Detox, Maestro, XCUITest)
        /----------\
       / Integration \      15-25% - Screen-level, navigation, API integration
      /----------------\
     /    Unit Tests     \  65-80% - Business logic, state, utilities
    /______________________\
```

**Mobile-specific considerations:**
- E2E tests are slower and flakier on mobile than web -- keep them minimal
- Integration tests at the screen/widget level give the best ROI
- Unit test all business logic, state management, and data transformations
- Snapshot/screenshot tests catch visual regressions cheaply

## iOS Testing

### XCTest Unit Tests

```swift
import XCTest
@testable import MyApp

class AuthServiceTests: XCTestCase {

    var sut: AuthService!
    var mockNetwork: MockNetworkClient!

    override func setUp() {
        super.setUp()
        mockNetwork = MockNetworkClient()
        sut = AuthService(network: mockNetwork)
    }

    override func tearDown() {
        sut = nil
        mockNetwork = nil
        super.tearDown()
    }

    func testLoginSuccess() async throws {
        mockNetwork.mockResponse = LoginResponse(token: "abc123", user: .mock)

        let result = try await sut.login(email: "user@test.com", password: "pass")

        XCTAssertEqual(result.token, "abc123")
        XCTAssertEqual(mockNetwork.lastEndpoint, "/auth/login")
    }

    func testLoginInvalidCredentials() async {
        mockNetwork.mockError = AuthError.invalidCredentials

        do {
            _ = try await sut.login(email: "bad@test.com", password: "wrong")
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertEqual(error as? AuthError, .invalidCredentials)
        }
    }
}
```

### XCUITest UI Tests

```swift
import XCTest

class LoginUITests: XCTestCase {

    let app = XCUIApplication()

    override func setUp() {
        continueAfterFailure = false
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func testLoginFlow() {
        let emailField = app.textFields["email-input"]
        let passwordField = app.secureTextFields["password-input"]
        let loginButton = app.buttons["login-button"]

        emailField.tap()
        emailField.typeText("user@example.com")

        passwordField.tap()
        passwordField.typeText("password123")

        loginButton.tap()

        let homeScreen = app.otherElements["home-screen"]
        XCTAssertTrue(homeScreen.waitForExistence(timeout: 5))
    }

    func testLoginValidationErrors() {
        app.buttons["login-button"].tap()
        XCTAssertTrue(app.staticTexts["Email is required"].exists)
    }
}
```

### iOS Snapshot Testing

```swift
import XCTest
import SnapshotTesting
@testable import MyApp

class ProfileViewSnapshotTests: XCTestCase {

    func testProfileView_loggedIn() {
        let view = ProfileView(user: .mock)
        let vc = UIHostingController(rootView: view)

        assertSnapshot(of: vc, as: .image(on: .iPhone13))
        assertSnapshot(of: vc, as: .image(on: .iPadPro11))
    }

    func testProfileView_darkMode() {
        let view = ProfileView(user: .mock)
        let vc = UIHostingController(rootView: view)
        vc.overrideUserInterfaceStyle = .dark

        assertSnapshot(of: vc, as: .image(on: .iPhone13))
    }
}
```

## Android Testing

### JUnit Unit Tests

```kotlin
import org.junit.Test
import org.junit.Before
import org.junit.Assert.*
import io.mockk.coEvery
import io.mockk.mockk

class AuthRepositoryTest {

    private lateinit var sut: AuthRepository
    private val mockApi: AuthApi = mockk()
    private val mockTokenStore: TokenStore = mockk(relaxed = true)

    @Before
    fun setUp() {
        sut = AuthRepository(mockApi, mockTokenStore)
    }

    @Test
    fun `login returns user on success`() = runTest {
        coEvery { mockApi.login(any()) } returns LoginResponse("token123", UserDto.mock)

        val result = sut.login("user@test.com", "password")

        assertTrue(result.isSuccess)
        assertEquals("token123", result.getOrNull()?.token)
    }

    @Test
    fun `login returns error on network failure`() = runTest {
        coEvery { mockApi.login(any()) } throws IOException("Network error")

        val result = sut.login("user@test.com", "password")

        assertTrue(result.isFailure)
    }
}
```

### Espresso UI Tests (View-Based)

```kotlin
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import org.junit.Rule
import org.junit.Test

class LoginActivityTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(LoginActivity::class.java)

    @Test
    fun loginButton_displaysError_whenEmailEmpty() {
        onView(withId(R.id.loginButton)).perform(click())
        onView(withId(R.id.emailError))
            .check(matches(isDisplayed()))
            .check(matches(withText("Email is required")))
    }

    @Test
    fun successfulLogin_navigatesToHome() {
        onView(withId(R.id.emailInput)).perform(typeText("user@test.com"))
        onView(withId(R.id.passwordInput)).perform(typeText("password123"), closeSoftKeyboard())
        onView(withId(R.id.loginButton)).perform(click())

        onView(withId(R.id.homeScreen)).check(matches(isDisplayed()))
    }
}
```

### Compose UI Testing

```kotlin
import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createComposeRule
import org.junit.Rule
import org.junit.Test

class LoginScreenComposeTest {

    @get:Rule
    val composeRule = createComposeRule()

    @Test
    fun loginScreen_showsValidationError() {
        composeRule.setContent {
            LoginScreen(onLogin = {})
        }

        composeRule.onNodeWithTag("login-button").performClick()
        composeRule.onNodeWithText("Email is required").assertIsDisplayed()
    }

    @Test
    fun loginScreen_callsOnLogin_withCredentials() {
        var capturedEmail = ""
        composeRule.setContent {
            LoginScreen(onLogin = { email, _ -> capturedEmail = email })
        }

        composeRule.onNodeWithTag("email-input").performTextInput("user@test.com")
        composeRule.onNodeWithTag("password-input").performTextInput("pass123")
        composeRule.onNodeWithTag("login-button").performClick()

        assertEquals("user@test.com", capturedEmail)
    }
}
```

### Robolectric (JVM-Based Android Tests)

```kotlin
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.junit.runner.RunWith

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [35], manifest = Config.NONE)
class NotificationManagerTest {

    @Test
    fun `scheduleNotification creates pending intent`() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val manager = NotificationManager(context)

        manager.scheduleNotification("Test", delay = 5.minutes)

        val alarmManager = context.getSystemService<AlarmManager>()
        // Verify alarm was scheduled using shadow
        val shadow = Shadows.shadowOf(alarmManager)
        assertEquals(1, shadow.scheduledAlarms.size)
    }
}
```

## React Native Testing

### Jest + React Native Testing Library

```typescript
import { render, fireEvent, waitFor, screen } from '@testing-library/react-native';
import { LoginScreen } from '../screens/LoginScreen';
import { AuthProvider } from '../providers/AuthProvider';

const renderWithProviders = (component: React.ReactElement) => {
  return render(<AuthProvider>{component}</AuthProvider>);
};

describe('LoginScreen', () => {
  it('displays validation errors for empty fields', () => {
    renderWithProviders(<LoginScreen />);

    fireEvent.press(screen.getByTestId('login-button'));

    expect(screen.getByText('Email is required')).toBeTruthy();
    expect(screen.getByText('Password is required')).toBeTruthy();
  });

  it('calls login API with correct credentials', async () => {
    const mockLogin = jest.fn().mockResolvedValue({ token: 'abc' });
    renderWithProviders(<LoginScreen onLogin={mockLogin} />);

    fireEvent.changeText(screen.getByTestId('email-input'), 'user@test.com');
    fireEvent.changeText(screen.getByTestId('password-input'), 'password123');
    fireEvent.press(screen.getByTestId('login-button'));

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('user@test.com', 'password123');
    });
  });

  it('shows loading state during submission', async () => {
    const slowLogin = jest.fn(() => new Promise((r) => setTimeout(r, 1000)));
    renderWithProviders(<LoginScreen onLogin={slowLogin} />);

    fireEvent.changeText(screen.getByTestId('email-input'), 'user@test.com');
    fireEvent.changeText(screen.getByTestId('password-input'), 'pass');
    fireEvent.press(screen.getByTestId('login-button'));

    expect(screen.getByTestId('loading-indicator')).toBeTruthy();
  });
});
```

### Detox E2E Testing

```javascript
// .detoxrc.js
module.exports = {
  testRunner: { args: { config: 'e2e/jest.config.js' } },
  apps: {
    'ios.release': {
      type: 'ios.app',
      binaryPath: 'ios/build/MyApp.app',
      build: 'xcodebuild -workspace ios/MyApp.xcworkspace -scheme MyApp -configuration Release -sdk iphonesimulator',
    },
    'android.release': {
      type: 'android.apk',
      binaryPath: 'android/app/build/outputs/apk/release/app-release.apk',
      build: 'cd android && ./gradlew assembleRelease',
    },
  },
  devices: {
    simulator: { type: 'ios.simulator', device: { type: 'iPhone 16' } },
    emulator: { type: 'android.emulator', device: { avdName: 'Pixel_8_API_35' } },
  },
};
```

```javascript
// e2e/checkout.test.ts
describe('Checkout Flow', () => {
  beforeAll(async () => { await device.launchApp({ newInstance: true }); });
  beforeEach(async () => { await device.reloadReactNative(); });

  it('completes purchase end-to-end', async () => {
    await element(by.id('product-list')).scroll(200, 'down');
    await element(by.id('product-card-1')).tap();
    await element(by.id('add-to-cart')).tap();
    await element(by.id('cart-badge')).tap();
    await element(by.id('checkout-button')).tap();

    await expect(element(by.id('order-confirmation'))).toBeVisible();
    await expect(element(by.text('Order #'))).toBeVisible();
  });
});
```

## Flutter Testing

### Widget Tests

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/screens/login_screen.dart';

void main() {
  testWidgets('LoginScreen shows error on empty submit', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: LoginScreen()),
    );

    await tester.tap(find.byKey(const Key('login-button')));
    await tester.pumpAndSettle();

    expect(find.text('Email is required'), findsOneWidget);
  });

  testWidgets('LoginScreen navigates on success', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: const LoginScreen(),
        routes: {'/home': (_) => const HomeScreen()},
      ),
    );

    await tester.enterText(find.byKey(const Key('email')), 'user@test.com');
    await tester.enterText(find.byKey(const Key('password')), 'pass123');
    await tester.tap(find.byKey(const Key('login-button')));
    await tester.pumpAndSettle();

    expect(find.byType(HomeScreen), findsOneWidget);
  });
}
```

### Golden Tests (Screenshot Comparison)

```dart
testWidgets('ProfileCard matches golden', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(body: ProfileCard(user: User.mock())),
    ),
  );

  await expectLater(
    find.byType(ProfileCard),
    matchesGoldenFile('goldens/profile_card.png'),
  );
});
```

### Flutter Integration Tests

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('full login flow', (tester) async {
    app.main();
    await tester.pumpAndSettle();

    await tester.enterText(find.byKey(const Key('email')), 'test@example.com');
    await tester.enterText(find.byKey(const Key('password')), 'password');
    await tester.tap(find.byKey(const Key('login-button')));
    await tester.pumpAndSettle(const Duration(seconds: 3));

    expect(find.text('Welcome'), findsOneWidget);
  });
}
```

## Cross-Platform E2E: Maestro

Maestro is a declarative, YAML-based E2E testing framework that works across iOS, Android, React Native, and Flutter.

```yaml
# .maestro/login_flow.yaml
appId: com.example.myapp
---
- launchApp
- tapOn: "Email"
- inputText: "user@example.com"
- tapOn: "Password"
- inputText: "password123"
- tapOn: "Login"
- assertVisible: "Welcome"
- assertVisible: "Home"

# Scroll and interact
- scrollUntilVisible:
    element: "Load More"
    direction: DOWN
- tapOn: "Load More"
```

```bash
# Run Maestro tests
maestro test .maestro/login_flow.yaml

# Run entire suite
maestro test .maestro/

# Record a flow visually
maestro studio

# Run on CI
maestro cloud .maestro/ --apiKey $MAESTRO_API_KEY
```

## CI/CD Testing Pipelines

### GitHub Actions (React Native)

```yaml
# .github/workflows/test.yml
name: Mobile Tests
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v4

  e2e-ios:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22' }
      - run: npm ci
      - run: npx detox build --configuration ios.sim.release
      - run: npx detox test --configuration ios.sim.release --cleanup

  e2e-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: 'temurin', java-version: '17' }
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 35
          script: npx detox test --configuration android.emu.release
```

## Device Farms

| Service | Platforms | Best For |
|---------|-----------|----------|
| Firebase Test Lab | Android, iOS | Google ecosystem, free tier |
| AWS Device Farm | Android, iOS | AWS users, wide device selection |
| BrowserStack | Android, iOS | Large device catalog, parallel runs |
| Sauce Labs | Android, iOS | Enterprise, comprehensive reporting |

```bash
# Firebase Test Lab
gcloud firebase test android run \
  --type instrumentation \
  --app app-debug.apk \
  --test app-debug-androidTest.apk \
  --device model=Pixel8,version=35

# AWS Device Farm (via CLI)
aws devicefarm schedule-run \
  --project-arn $PROJECT_ARN \
  --app-arn $APP_ARN \
  --device-pool-arn $POOL_ARN \
  --test '{"type":"APPIUM_PYTHON","testPackageArn":"'$TEST_ARN'"}'
```

## Performance Testing

### Startup Time Measurement

```typescript
// React Native - measure TTI
import { PerformanceObserver, performance } from 'react-native-performance';

performance.mark('app_start');

// In your root component
useEffect(() => {
  performance.mark('app_interactive');
  performance.measure('time_to_interactive', 'app_start', 'app_interactive');
}, []);
```

### Frame Rate Monitoring

```kotlin
// Android - Choreographer frame callback
val frameCallback = object : Choreographer.FrameCallback {
    var lastFrameTime = 0L
    override fun doFrame(frameTimeNanos: Long) {
        if (lastFrameTime > 0) {
            val frameDuration = (frameTimeNanos - lastFrameTime) / 1_000_000
            if (frameDuration > 16) Log.w("PERF", "Dropped frame: ${frameDuration}ms")
        }
        lastFrameTime = frameTimeNanos
        Choreographer.getInstance().postFrameCallback(this)
    }
}
```

## Accessibility Testing

```typescript
// React Native - jest-axe equivalent
import { render } from '@testing-library/react-native';

it('has proper accessibility labels', () => {
  const { getByRole } = render(<LoginScreen />);

  expect(getByRole('button', { name: 'Log in' })).toBeTruthy();
  expect(getByRole('header', { name: 'Welcome' })).toBeTruthy();
});

// Ensure all interactive elements have accessibility props
it('all buttons have accessible names', () => {
  const { getAllByRole } = render(<SettingsScreen />);
  const buttons = getAllByRole('button');
  buttons.forEach((button) => {
    expect(button.props.accessibilityLabel || button.props.children).toBeTruthy();
  });
});
```

## Mocking Strategies

### Network Mocking

```typescript
// MSW (Mock Service Worker) for React Native
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const server = setupServer(
  http.post('/api/login', () => {
    return HttpResponse.json({ token: 'mock-token', user: { id: '1' } });
  }),
  http.get('/api/products', () => {
    return HttpResponse.json({ products: mockProducts });
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Sensor and Location Mocking

```typescript
// Mock geolocation in tests
jest.mock('expo-location', () => ({
  requestForegroundPermissionsAsync: jest.fn().mockResolvedValue({ status: 'granted' }),
  getCurrentPositionAsync: jest.fn().mockResolvedValue({
    coords: { latitude: 37.7749, longitude: -122.4194, accuracy: 10 },
  }),
  watchPositionAsync: jest.fn(),
}));
```

## Coverage Requirements

| Layer | Target | Measurement |
|-------|--------|-------------|
| Unit tests | > 80% | `jest --coverage` / `flutter test --coverage` |
| Integration | Key screens | Manual tracking |
| E2E | Critical paths | Flow count |
| Accessibility | All interactive | Automated audit |

```bash
# React Native coverage
npx jest --coverage --coverageThreshold='{"global":{"branches":80,"functions":80,"lines":80}}'

# Flutter coverage
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html

# Android coverage (JaCoCo)
./gradlew jacocoTestReport
```

## Related Skills

- `appstore` - **Recommended**: App Store Connect automation via `asc` CLI (TestFlight distribution, pre-submission validation)
- `expo` - Expo-specific testing setup
- `react-native-expert` - React Native debugging tools
- `react-native-expert` - Architecture for testability
- `deep-linking-push` - Testing deep links and notifications
