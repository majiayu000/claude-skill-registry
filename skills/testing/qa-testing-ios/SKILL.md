---
name: qa-testing-ios
description: "iOS testing with XCTest/XCUITest on simulators and devices: layered strategy, determinism/flake control, device matrix selection, CI ergonomics, and repeatable simulator automation."
---

# QA Testing (iOS, Dec 2025) — Quick Reference

This skill enables iOS testing automation via Xcode Simulator and `xcodebuild`, with a focus on reliable UI tests and layered coverage.

**Note**: Requires macOS with Xcode installed.

Core references: Apple XCTest docs (https://developer.apple.com/documentation/xctest), `simctl` (https://developer.apple.com/documentation/xcode/simctl), and Xcode testing guidance (https://developer.apple.com/documentation/xcode/testing-your-apps-in-xcode).

---

## Core QA (Default)

### Testing Layers (Use the Smallest Effective Layer)

- Unit tests: business logic, formatting, state machines (fast, deterministic).
- Snapshot tests: view rendering regressions (use sparingly; review diffs).
- Integration tests: persistence, networking adapters, serialization, feature flags.
- UI tests (XCUITest): critical user journeys only; keep thin.

### Device Matrix (Simulator vs Real Devices)

- Default: simulators for PR gates; real devices for nightly/release validation.
- Keep the matrix small and risk-based:
  - One “small phone”, one “large phone”, and one iPad if the UI supports it [Inference].
  - Add OS versions only when you support multiple major releases.

### UI Test Flake Control (Determinism)

- Disable/limit animations in test builds where possible.
- Control time: fixed timezone/locale; avoid relying on wall-clock.
- Control network: stub at the boundary for most UI tests; avoid third-party dependencies.
- Control permissions: set predictable permission states; avoid manual prompts.
- Isolation: reset app state between tests; avoid ordering dependence and shared accounts.

### CI Economics and Debugging Ergonomics

- PR gate: small smoke UI suite + unit/integration; full UI suite on schedule [Inference].
- Always collect actionable artifacts:
  - `xcresult` bundles, screenshots, and logs on failure.
- Prefer “fail fast” diagnostics: assert early on navigation/state instead of letting tests time out.

### Do / Avoid

Do:
- Make UI tests independent and idempotent.
- Use test data builders and dedicated test accounts/tenants.

Avoid:
- Relying on test ordering or global state.
- UI tests that require real network access for core flows.

## Quick Reference

| Task | Command | When to Use |
|------|---------|-------------|
| List simulators | `xcrun simctl list devices` | Check available devices |
| Boot simulator | `xcrun simctl boot "iPhone 16"` | Start simulator |
| Build app | `xcodebuild build` | Compile iOS app |
| Install app | `xcrun simctl install booted app.app` | Deploy to simulator |
| Run tests | `xcodebuild test` | Execute XCTest suite |
| Take screenshot | `xcrun simctl io booted screenshot` | Capture screen |
| Record video | `xcrun simctl io booted recordVideo` | Record session |

## When to Use This Skill

Claude should invoke this skill when a user requests:

- Build and run iOS app in simulator
- Test iOS app functionality
- Capture screenshots for documentation
- Automate UI testing with XCTest
- Debug iOS app behavior
- Set up iOS CI/CD pipeline

---

## Simulator Management

### List Available Simulators

```bash
# List all devices
xcrun simctl list devices

# List available runtimes
xcrun simctl list runtimes

# List booted devices only
xcrun simctl list devices | grep "Booted"
```

### Boot and Manage Simulators

```bash
# Boot a specific simulator
xcrun simctl boot "iPhone 16 Pro"

# Open Simulator app
open -a Simulator

# Shutdown simulator
xcrun simctl shutdown "iPhone 16 Pro"

# Shutdown all simulators
xcrun simctl shutdown all

# Erase simulator (reset to clean state)
xcrun simctl erase "iPhone 16 Pro"

# Create new simulator
xcrun simctl create "My iPhone" "iPhone 16" "iOS-18-0"
```

---

## Build and Deploy

### Build iOS App

```bash
# Build for simulator (Debug)
xcodebuild build \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -sdk iphonesimulator \
  -configuration Debug \
  -destination 'platform=iOS Simulator,name=iPhone 16'

# Build with workspace (CocoaPods/SPM)
xcodebuild build \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -sdk iphonesimulator \
  -configuration Debug

# Clean build folder
xcodebuild clean \
  -project MyApp.xcodeproj \
  -scheme MyApp
```

### Install and Launch App

```bash
# Install app on booted simulator
xcrun simctl install booted /path/to/MyApp.app

# Launch app
xcrun simctl launch booted com.example.myapp

# Launch and wait for debugger
xcrun simctl launch --wait-for-debugger booted com.example.myapp

# Terminate app
xcrun simctl terminate booted com.example.myapp

# Uninstall app
xcrun simctl uninstall booted com.example.myapp
```

---

## Testing

### Run XCTest Suite

```bash
# Run all tests
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 16'

# Run specific test class
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -only-testing:MyAppTests/LoginTests

# Run specific test method
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -only-testing:MyAppTests/LoginTests/testValidLogin

# Run UI tests
xcodebuild test \
  -project MyApp.xcodeproj \
  -scheme MyAppUITests \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 16'
```

### XCTest Example

```swift
// MyAppTests/LoginTests.swift
import XCTest
@testable import MyApp

final class LoginTests: XCTestCase {
    var sut: LoginViewModel!

    override func setUp() {
        super.setUp()
        sut = LoginViewModel()
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func testValidLogin() async throws {
        // Given
        let email = "user@example.com"
        let password = "password123"

        // When
        let result = try await sut.login(email: email, password: password)

        // Then
        XCTAssertTrue(result.isSuccess)
        XCTAssertNotNil(sut.currentUser)
    }

    func testInvalidEmail() {
        // Given
        let email = "invalid-email"

        // When
        let error = sut.validateEmail(email)

        // Then
        XCTAssertEqual(error, .invalidEmail)
    }
}
```

### XCUITest Example

```swift
// MyAppUITests/LoginUITests.swift
import XCTest

final class LoginUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }

    func testLoginFlow() {
        // Navigate to login
        app.buttons["Login"].tap()

        // Enter credentials
        let emailField = app.textFields["email"]
        emailField.tap()
        emailField.typeText("user@example.com")

        let passwordField = app.secureTextFields["password"]
        passwordField.tap()
        passwordField.typeText("password123")

        // Submit
        app.buttons["Submit"].tap()

        // Verify navigation to dashboard
        XCTAssertTrue(app.navigationBars["Dashboard"].waitForExistence(timeout: 5))
    }

    func testLoginValidation() {
        app.buttons["Login"].tap()
        app.buttons["Submit"].tap()

        // Verify error message
        XCTAssertTrue(app.staticTexts["Email is required"].exists)
    }
}
```

---

## Screenshots and Recording

### Capture Screenshots

```bash
# Take screenshot (PNG)
xcrun simctl io booted screenshot screenshot.png

# Screenshot with specific device
xcrun simctl io "iPhone 16 Pro" screenshot home.png

# Screenshot to clipboard
xcrun simctl io booted screenshot --type=png | pbcopy
```

### Record Video

```bash
# Start recording
xcrun simctl io booted recordVideo recording.mov

# Press Ctrl+C to stop recording

# Record with codec
xcrun simctl io booted recordVideo --codec=h264 recording.mp4
```

### Automated Screenshot Script

```bash
#!/bin/bash
# capture-screens.sh

DEVICE="iPhone 16 Pro"
OUTPUT_DIR="./screenshots"
APP_BUNDLE="com.example.myapp"

mkdir -p "$OUTPUT_DIR"

# Boot and launch
xcrun simctl boot "$DEVICE"
sleep 5
xcrun simctl install booted ./build/MyApp.app
xcrun simctl launch booted "$APP_BUNDLE"
sleep 3

# Capture screens
xcrun simctl io booted screenshot "$OUTPUT_DIR/01-home.png"

# Navigate and capture
xcrun simctl io booted tap 200 400  # Tap coordinates
sleep 1
xcrun simctl io booted screenshot "$OUTPUT_DIR/02-login.png"

# Cleanup
xcrun simctl shutdown "$DEVICE"
```

---

## Simulator Interaction

### Touch and Input

```bash
# Tap at coordinates
xcrun simctl io booted tap 200 400

# Swipe
xcrun simctl io booted swipe 100 500 100 200

# Type text
xcrun simctl io booted type "Hello World"

# Paste from clipboard
xcrun simctl io booted paste

# Press home button
xcrun simctl io booted home
```

### Device Settings

```bash
# Set location
xcrun simctl location booted set 37.7749,-122.4194

# Clear location
xcrun simctl location booted clear

# Open URL
xcrun simctl openurl booted "myapp://deep-link"

# Add photo to library
xcrun simctl addmedia booted photo.jpg

# Push notification
xcrun simctl push booted com.example.myapp notification.apns
```

### Notification Payload

```json
// notification.apns
{
  "aps": {
    "alert": {
      "title": "Test Notification",
      "body": "This is a test push notification"
    },
    "badge": 1,
    "sound": "default"
  }
}
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/ios.yml
name: iOS Build and Test
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.0.app

      - name: Install dependencies
        run: |
          brew install xcbeautify
          pod install || true

      - name: Build
        run: |
          xcodebuild build \
            -scheme MyApp \
            -sdk iphonesimulator \
            -destination 'platform=iOS Simulator,name=iPhone 16' \
            | xcbeautify

      - name: Test
        run: |
          xcodebuild test \
            -scheme MyApp \
            -sdk iphonesimulator \
            -destination 'platform=iOS Simulator,name=iPhone 16' \
            -resultBundlePath TestResults \
            | xcbeautify

      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: TestResults
```

---

## Optional: AI / Automation

Do:
- Use AI to expand test ideas from user journeys and failure modes; keep only cases you can automate deterministically.
- Use AI to summarize `xcresult` failures and cluster flakes; verify by reproducing with controlled conditions.

Avoid:
- Generating UI tests that depend on timing/sleeps or real network as the default.
- Accepting AI-proposed selectors/assertions without validating accessibility labels and stable UI structure.

---

## Navigation

**Resources**
- [resources/simulator-commands.md](resources/simulator-commands.md) — Complete simctl reference
- [resources/xctest-patterns.md](resources/xctest-patterns.md) — Testing patterns and fixtures
- [data/sources.json](data/sources.json) — Apple documentation links

**Templates**
- [templates/template-ios-ui-test-stability-checklist.md](templates/template-ios-ui-test-stability-checklist.md) — iOS UI test stability checklist (isolation/determinism/device matrix)

**Related Skills**
- [../software-mobile/SKILL.md](../software-mobile/SKILL.md) — iOS/Swift development
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) — General testing strategies
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — CI/CD pipelines
