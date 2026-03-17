---
name: device-testing
description: Interact with iOS simulators and verify app behavior using xcobra
---

Use `bunx xcobra` to interact with iOS simulators and debug Expo apps.

## Inspecting the UI

Get the accessibility tree to understand current screen state:

```bash
bunx xcobra sim xml
```

This returns XML with all UI elements, their labels, identifiers, and positions. Use this to:
- Find element identifiers for tapping
- Verify UI state after actions
- Debug layout issues

## Tapping Elements

Tap by accessibility label (preferred):

```bash
bunx xcobra sim tap --label "Submit"
```

Tap by accessibility identifier:

```bash
bunx xcobra sim tap --id "submit-button"
```

Tap by coordinates:

```bash
bunx xcobra sim tap --x 200 --y 400
```

Add delays for animations:

```bash
bunx xcobra sim tap --label "Next" --pre-delay 500 --post-delay 300
```

## Typing Text

Type text into focused input:

```bash
bunx xcobra sim type "Hello World"
```

Type from stdin:

```bash
echo "test@example.com" | bunx xcobra sim type --stdin
```

## Gestures

Preset gestures:

```bash
bunx xcobra sim gesture scroll-up
bunx xcobra sim gesture scroll-down
bunx xcobra sim gesture swipe-from-left-edge
```

Custom swipe:

```bash
bunx xcobra sim swipe --start-x 200 --start-y 400 --end-x 200 --end-y 100
```

## Hardware Buttons

Press hardware buttons:

```bash
bunx xcobra sim button home
bunx xcobra sim button lock
bunx xcobra sim button siri
```

## Screenshots

Capture screenshot:

```bash
bunx xcobra sim screenshot --output screenshot.png
```

## Video Recording

Record simulator video:

```bash
bunx xcobra sim record-video --output recording.mp4
```

## Evaluating JavaScript

Execute JS in the running Expo app:

```bash
bunx xcobra expo eval "Date.now()"
```

Get app state:

```bash
bunx xcobra expo eval "global.__REDUX_STORE__?.getState()"
```

Call exposed functions:

```bash
bunx xcobra expo eval "globalThis.testHelper?.getCurrentRoute()"
```

## Console Logs

Stream console output:

```bash
bunx xcobra expo console
```

JSON format for parsing:

```bash
bunx xcobra expo console --json
```

## Network Monitoring

Monitor network requests:

```bash
bunx xcobra expo network
```

## Reloading the App

Trigger a reload to refresh the JavaScript bundle:

```bash
bunx xcobra expo reload
```

This is useful when:
- The Metro connection becomes stale
- Hot reload isn't picking up changes
- The app state needs a fresh start
- Deep links or navigation seem stuck

## Crash Reports

View latest crash:

```bash
bunx xcobra crash latest
```

List recent crashes:

```bash
bunx xcobra crash list
```

Show specific crash:

```bash
bunx xcobra crash show <crash-id>
```

## Source Inspection

List loaded scripts:

```bash
bunx xcobra expo src scripts
```

Get source code by script ID:

```bash
bunx xcobra expo src source <script-id>
```

List Metro modules:

```bash
bunx xcobra expo src modules
```

## Simulator Management

List all simulators:

```bash
bunx xcobra sim list
```

Target specific simulator:

```bash
bunx xcobra sim tap --udid "DEVICE-UDID" --label "OK"
```

## Testing Workflow

1. **Get current UI state**
   ```bash
   bunx xcobra sim xml
   ```

2. **Perform action**
   ```bash
   bunx xcobra sim tap --label "Login"
   ```

3. **Wait and verify**
   ```bash
   sleep 1
   bunx xcobra sim xml | grep "Welcome"
   ```

4. **Check for errors**
   ```bash
   bunx xcobra expo console --json | head -20
   ```

## Verifying Screen Content

After navigating, verify you're on the expected screen:

```bash
# Check for expected text content
bunx xcobra sim xml | grep -i "expected title"

# Get full accessibility tree and search for elements
bunx xcobra sim xml > /tmp/ui.xml && cat /tmp/ui.xml
```

Use JavaScript eval to check the current route:

```bash
bunx xcobra expo eval "window.location?.pathname"
```

## Troubleshooting Unexpected Routes

If deep links navigate to the wrong screen or you see unexpected content:

**1. Check the current route in the app:**

```bash
bunx xcobra expo eval "globalThis.testHelper?.getCurrentRoute()"
```

**2. Verify the app directory structure:**

Look for unexpected index routes that may be intercepting navigation:

```bash
# List all index files - these define default routes
find app -name "index.tsx" -o -name "index.ts" -o -name "index.js"

# Check for index routes inside groups that may override expected behavior
find app -path "*/(*)/*" -name "index.*"
```

**3. Common issues:**

- **Unexpected index in a group**: A file like `app/(tabs)/index.tsx` will be the default route for the `(tabs)` group, potentially overriding `app/index.tsx`
- **Missing layout**: Groups need a `_layout.tsx` to properly nest routes
- **Conflicting routes**: Two files resolving to the same URL path

**4. Verify route structure matches expectations:**

```bash
# List all route files
find app -name "*.tsx" | grep -v "_layout" | sort

# Check group structure
find app -type d -name "(*)"`
```

**5. Test deep link resolution:**

```bash
# Open a deep link and immediately check the route
xcrun simctl openurl booted "myapp://settings" && sleep 1 && bunx xcobra expo eval "window.location?.pathname"
```

## Exposing Test Helpers

Add global helpers in your app for testing:

```tsx
if (__DEV__) {
  globalThis.testHelper = {
    getCurrentRoute: () => navigationRef.current?.getCurrentRoute(),
    getState: () => store.getState(),
    resetApp: () => { /* reset logic */ },
  };
}
```

Then call via eval:

```bash
bunx xcobra expo eval "testHelper.getCurrentRoute()"
```
