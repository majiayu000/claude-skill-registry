---
name: xcode-build
description: Build and run iOS/macOS apps using xcodebuild and xcrun simctl directly. Use when building Xcode projects, running iOS simulators, managing devices, compiling Swift code, running UI tests, or automating iOS app interactions. Replaces XcodeBuildMCP with native CLI tools.
allowed-tools: Bash, Read, Grep, Glob
---

# Xcode Build Direct

Build and manage iOS/macOS projects using native Xcode CLI tools instead of MCP servers.

## When to Use This Skill

Use this skill when:
- Building iOS or macOS apps with Xcode
- Running apps in iOS simulators
- Managing simulator instances (boot, shutdown, list)
- Taking screenshots of simulators
- Capturing app logs
- Running tests (unit or UI)
- Automating UI interactions (tap, type, swipe)

**Preference**: Always use direct CLI commands (`xcodebuild`, `xcrun simctl`) instead of XcodeBuildMCP tools.

## Quick Start

### 1. Discover Project Structure
```bash
# List schemes in a workspace
xcodebuild -workspace /path/to/App.xcworkspace -list

# List schemes in a project
xcodebuild -project /path/to/App.xcodeproj -list

# Show build settings
xcodebuild -workspace /path/to/App.xcworkspace -scheme AppScheme -showBuildSettings
```

### 2. Find Available Simulators
```bash
# List all simulators
xcrun simctl list devices

# List as JSON (better for parsing)
xcrun simctl list devices --json

# List only available simulators
xcrun simctl list devices available
```

### 3. Build for Simulator
```bash
# Get simulator UUID first
UDID=$(xcrun simctl list devices --json | jq -r '.devices | .[].[] | select(.name=="iPhone 16 Pro") | .udid' | head -1)

# Build
xcodebuild \
  -workspace /path/to/App.xcworkspace \
  -scheme AppScheme \
  -destination "platform=iOS Simulator,id=$UDID" \
  -configuration Debug \
  -derivedDataPath /tmp/build \
  build
```

### 4. Install and Launch
```bash
# Find the built .app
APP_PATH=$(find /tmp/build -name "*.app" -type d | head -1)

# Install on simulator
xcrun simctl install $UDID "$APP_PATH"

# Launch app
xcrun simctl launch $UDID com.your.bundleid
```

### 5. Take Screenshot
```bash
xcrun simctl io $UDID screenshot /tmp/screenshot.png
```

## Detailed References

For comprehensive command documentation, see:
- **CLI_REFERENCE.md** - Full `xcodebuild` and `xcrun simctl` command reference
- **XCUITEST_GUIDE.md** - UI automation via XCUITest (tap, type, gestures, element queries)

## Common Patterns

### Build + Run Workflow
```bash
# 1. Boot simulator
xcrun simctl boot $UDID 2>/dev/null || true

# 2. Build
xcodebuild -workspace App.xcworkspace -scheme App \
  -destination "platform=iOS Simulator,id=$UDID" \
  -derivedDataPath /tmp/build build

# 3. Find and install app
APP=$(find /tmp/build -name "*.app" -type d | head -1)
xcrun simctl install $UDID "$APP"

# 4. Launch with console output
xcrun simctl launch --console $UDID com.bundle.id
```

### Log Capture
```bash
# Stream app logs (run in background)
/usr/bin/log stream \
  --predicate 'processImagePath CONTAINS[cd] "AppName"' \
  --style json &
LOG_PID=$!

# ... interact with app ...

# Stop logging
kill $LOG_PID
```

### Running Tests
```bash
# Unit tests
xcodebuild -workspace App.xcworkspace -scheme App \
  -destination "platform=iOS Simulator,id=$UDID" \
  test

# Specific test class
xcodebuild -workspace App.xcworkspace -scheme App \
  -destination "platform=iOS Simulator,id=$UDID" \
  -only-testing "AppTests/MyTestClass" \
  test
```

## UI Automation

For tapping, typing, and UI element queries, use **XCUITest** (Apple's native UI testing framework).

This is more powerful than MCP-based automation because:
- Native to iOS, always up-to-date
- Full access to accessibility tree
- Can wait for elements, handle animations
- Integrates with Xcode test runner

See **XCUITEST_GUIDE.md** for complete patterns.

Quick example:
```swift
// In a UI test file
func testLogin() {
    let app = XCUIApplication()
    app.launch()

    // Type in text field
    app.textFields["email"].tap()
    app.textFields["email"].typeText("user@example.com")

    // Tap button
    app.buttons["Login"].tap()

    // Verify result
    XCTAssertTrue(app.staticTexts["Welcome"].exists)
}
```

Run UI tests:
```bash
xcodebuild -workspace App.xcworkspace -scheme AppUITests \
  -destination "platform=iOS Simulator,id=$UDID" \
  test
```

## Session Configuration

Unlike MCP, CLI tools don't maintain session state. Use environment variables or a config file:

```bash
# Set up session variables
export XCODE_WORKSPACE="/path/to/App.xcworkspace"
export XCODE_SCHEME="App"
export SIM_UDID="DD5E339B-468E-43C7-B219-54112C9D3250"
export APP_BUNDLE_ID="com.your.app"

# Use in commands
xcodebuild -workspace "$XCODE_WORKSPACE" -scheme "$XCODE_SCHEME" ...
xcrun simctl launch "$SIM_UDID" "$APP_BUNDLE_ID"
```

## Troubleshooting

### Build fails with "no matching destination"
```bash
# Check available destinations
xcodebuild -workspace App.xcworkspace -scheme App -showDestinations

# Use exact destination string from output
```

### Simulator won't boot
```bash
# Check if already booted
xcrun simctl list devices | grep Booted

# Force shutdown and reboot
xcrun simctl shutdown $UDID
xcrun simctl boot $UDID
```

### Can't find built .app
```bash
# Check derived data path you specified
ls -la /tmp/build/Build/Products/Debug-iphonesimulator/

# Or use default derived data
ls ~/Library/Developer/Xcode/DerivedData/
```

## Key Differences from XcodeBuildMCP

| Feature | XcodeBuildMCP | This Skill |
|---------|---------------|------------|
| Build | `build_sim({...})` | `xcodebuild -workspace ... build` |
| List sims | `list_sims()` | `xcrun simctl list devices` |
| Launch app | `launch_app_sim({...})` | `xcrun simctl launch $UDID $BUNDLE` |
| Screenshot | `screenshot({...})` | `xcrun simctl io $UDID screenshot` |
| Tap/Type | `tap({x,y})`, `type_text({...})` | XCUITest framework |
| Session state | Built-in | Environment variables |
