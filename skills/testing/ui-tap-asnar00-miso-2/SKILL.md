---
name: ui-tap
description: Trigger UI elements programmatically via HTTP automation. Use when you need to press buttons, interact with UI, or verify UI changes. Invoke with "tap the X button", "press X", "trigger X", or "click X".
---

# UI Tap

## Overview

This skill allows Claude to programmatically trigger UI elements in the running iOS or Android app by sending HTTP requests to the test server. Each UI element is registered with a unique ID and can be triggered remotely, enabling automated UI interaction and testing workflows.

## When to Use

Invoke this skill when you need to:
- Press a button or interact with a UI element programmatically
- Test UI interactions without manual intervention
- Verify that a UI change produces the expected result
- Coordinate button presses with screenshot capture
- Automate multi-step UI workflows

Trigger phrases:
- "tap the [element] button"
- "press [element]"
- "trigger [element]"
- "click [element]"
- "interact with [element]"

## Prerequisites

1. **Port forwarding must be active**: The test server on port 8081 must be forwarded from the device to localhost:
   ```bash
   # iOS (keep running in background)
   pymobiledevice3 usbmux forward 8081 8081 &

   # Android
   adb forward tcp:8081 tcp:8081
   ```

2. **App must be running**: The iOS or Android app must be running on the connected device with the test server active.

3. **Element must be registered**: The UI element must have been registered with the UIAutomationRegistry using a unique ID. Common registered elements include:
   - `toolbar-home` - Home button in toolbar
   - `toolbar-plus` - New post button in toolbar
   - `toolbar-search` - Search button in toolbar
   - `toolbar-profile` - Profile button in toolbar

## Instructions

### 1. Verify Prerequisites

Check that port forwarding is active and the app is running:

```bash
curl http://localhost:8081/test/ping
```

Should return "succeeded". If not, set up port forwarding first.

### 2. Identify Element ID

Determine the ID of the UI element you want to trigger. Element IDs are defined in the app code when registering with UIAutomationRegistry. Common patterns:
- Toolbar buttons: `toolbar-[icon-name]` (e.g., `toolbar-plus`, `toolbar-home`)
- Custom elements: Check the registration code in the relevant View file

### 3. Trigger the Element

Send a POST request to the test server:

```bash
curl -X POST 'http://localhost:8081/test/tap?id=ELEMENT_ID'
```

Replace `ELEMENT_ID` with the actual element identifier.

### 4. Verify Response

The response will be JSON indicating success or failure:

**Success**:
```json
{"status": "success", "id": "toolbar-plus"}
```

**Failure (element not found)**:
```json
{"status": "error", "message": "Element not found: invalid-id"}
```

### 5. Optional: Capture Screenshot

After triggering the element, capture a screenshot to verify the UI change:

```bash
# iOS
/Users/asnaroo/Desktop/experiments/miso/miso/platforms/ios/development/screen-capture/imp/screenshot.sh /tmp/ui-result.png

# Android
adb exec-out screencap -p > /tmp/ui-result.png
```

Then read the screenshot to verify the expected UI change occurred.

## Example Workflows

### Trigger New Post Editor

```bash
# Tap the + button to open new post editor
curl -X POST 'http://localhost:8081/test/tap?id=toolbar-plus'

# Capture screenshot to verify editor appeared
/Users/asnaroo/Desktop/experiments/miso/miso/platforms/ios/development/screen-capture/imp/screenshot.sh /tmp/new-post-editor.png
```

### Navigate Home

```bash
# Tap home button to return to recent posts view
curl -X POST 'http://localhost:8081/test/tap?id=toolbar-home'

# Verify we're on the home view
/Users/asnaroo/Desktop/experiments/miso/miso/platforms/ios/development/screen-capture/imp/screenshot.sh /tmp/home-view.png
```

### Multi-Step Workflow

```bash
# 1. Navigate to profile
curl -X POST 'http://localhost:8081/test/tap?id=toolbar-profile'
sleep 0.5  # Wait for navigation

# 2. Open new post editor from profile
curl -X POST 'http://localhost:8081/test/tap?id=toolbar-plus'
sleep 0.5  # Wait for sheet to appear

# 3. Verify final state
/Users/asnaroo/Desktop/experiments/miso/miso/platforms/ios/development/screen-capture/imp/screenshot.sh /tmp/profile-new-post.png
```

## Expected Behavior

1. **Immediate execution**: The UI action should occur within milliseconds of the HTTP request
2. **Main thread safety**: All UI actions are automatically dispatched to the main thread
3. **No app restart needed**: The automation system is always active once the app is running
4. **Visual feedback**: Most UI actions produce visible changes (button highlights, sheets appearing, navigation)
5. **Idempotent**: Multiple taps of the same element should be safe (though effects may differ)

## Troubleshooting

### "Connection refused" or curl fails

**Problem**: Port forwarding is not active or test server is not running.

**Solutions**:
1. For iOS: Run `pymobiledevice3 usbmux forward 8081 8081`
2. For Android: Run `adb forward tcp:8081 tcp:8081`
3. Verify app is running on device
4. Test basic connectivity: `curl http://localhost:8081/test/ping`

### "Element not found" error

**Problem**: The element ID is not registered or misspelled.

**Solutions**:
1. Check the element registration code in the View file (e.g., Toolbar.swift)
2. Verify the exact ID string (case-sensitive)
3. Ensure the view has appeared (registration often happens in `.onAppear`)
4. Check app logs for registration messages: `[TESTSERVER]` prefix

### Action triggers but wrong behavior

**Problem**: The registered action doesn't match expectations.

**Solutions**:
1. Review the action closure in the registration code
2. Check if state bindings are correct
3. Verify the action is using the correct callbacks
4. Add logging inside the action closure for debugging

### Screenshot doesn't show expected change

**Problem**: Screenshot captured before UI update completed.

**Solutions**:
1. Add a small delay before screenshot: `sleep 0.5`
2. For sheets/modals, use longer delay: `sleep 1.0`
3. For animations, wait for animation duration
4. Capture multiple screenshots to see transition

## Technical Details

### How It Works

1. **Registration**: UI elements register actions with `UIAutomationRegistry.shared.register(id:action:)`
2. **Storage**: Actions stored in thread-safe dictionary with concurrent queue
3. **HTTP Endpoint**: TestServer handles `POST /test/tap?id=X` requests
4. **Lookup**: TestServer queries registry for the element ID
5. **Execution**: Action dispatched to main thread via `DispatchQueue.main.async`
6. **Response**: JSON response indicates success or failure

### Platform Support

- **iOS**: Fully implemented in UIAutomationRegistry.swift and TestServer.swift
- **Android**: Fully implemented in UIAutomationRegistry.kt and TestServer.kt

### Element Registration Pattern

**Recommended: View Modifier Pattern** (Clean, declarative)

In SwiftUI views, use the `.uiAutomationId()` modifier directly on buttons or other interactive elements:

```swift
Button(action: {
    // Normal button action
    isEditing = true
}) {
    Image(systemName: "pencil.circle.fill")
}
.uiAutomationId("edit-button") {
    // Automation action (usually same as button action)
    isEditing = true
}
```

**Benefits**:
- No state management in ViewModels required
- Annotation lives right next to the UI element definition
- Automatically registers on `.onAppear`, no manual registration needed
- Works with SwiftUI's struct-based view system

**Legacy: Manual Registration Pattern** (Verbose, requires plumbing)

In SwiftUI views:
```swift
.onAppear {
    UIAutomationRegistry.shared.register(id: "unique-id") {
        // Action to perform (state changes, navigation, etc.)
    }
}
```

**Note**: Manual registration is still useful for non-button elements like gesture recognizers or complex views. For buttons, prefer the modifier pattern.

In Kotlin composables (recommended pattern):
```kotlin
@Composable
fun MyButton() {
    // Register for automation (auto-unregisters on dispose)
    RegisterUIElement("my-button") {
        // Action to perform
    }

    Button(onClick = { /* same action */ }) {
        Text("Click")
    }
}
```

Or using the modifier extension:
```kotlin
Button(
    onClick = { /* action */ },
    modifier = Modifier.uiAutomationId("my-button") { /* action */ }
) {
    Text("Click")
}
```

## Notes

- Element IDs should be descriptive and prefixed by component (e.g., `toolbar-plus`, `profile-edit`)
- Actions should be idempotent where possible
- Complex workflows may need delays between steps for animations
- Screenshots are the best way to verify UI changes
- This system is for testing/automation only, not production features
- All registered elements are logged when the test server starts

## Related Skills

- `ios-deploy-usb` - Deploy app with new UI elements
- `iphone-screen-capture` - Continuous screen mirroring
- `update-skill` - Improve this skill based on usage

## Additional Endpoints

### List Registered Elements

```bash
curl http://localhost:8081/test/list-elements
```

Response:
```json
{"elements": ["toolbar-plus", "refresh-button"], "textFields": ["search-field"]}
```

### Set Text in a Field

```bash
curl -X POST 'http://localhost:8081/test/set-text?id=search-field&text=hello'
```

Response:
```json
{"status": "success", "id": "search-field", "text": "hello"}
```

## Future Enhancements

- Support for element state queries (is button enabled? is view visible?)
- Batch operations (trigger multiple elements in sequence)
- Screenshot comparison (verify expected vs actual)
- Record and replay interaction sequences
