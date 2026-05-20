---
name: maestro-usage
description: Reference for writing and debugging Maestro E2E test flows. Covers all YAML commands, selectors, JavaScript integration, CLI usage, and flow structure. Use when writing Maestro tests, looking up command syntax, troubleshooting flow failures, or asking how to do something with Maestro.
---

# Maestro Usage

Quick reference for writing Maestro E2E flows. For the full command API, see [resources/api-reference.md](resources/api-reference.md). For testing patterns and pitfalls, see [resources/best-practices.md](resources/best-practices.md).

## Flow File Structure

Every Maestro flow is a YAML file with an optional **header** section separated from **commands** by `---`:

```yaml
appId: com.example.app
name: "My Test Flow"
env:
  USERNAME: "test@example.com"
  PASSWORD: "password123"
tags:
  - smoke
  - regression
---
- launchApp:
    clearState: true
- tapOn: "Login"
- inputText: "test@example.com"
```

### Header Fields

| Field | Required | Description |
|-------|----------|-------------|
| `appId` | Yes | Bundle ID (iOS) or package name (Android) |
| `name` | No | Custom display name for the flow |
| `env` | No | Environment variables accessible via `${VAR_NAME}` |
| `tags` | No | Tags for filtering (`maestro test --include-tags smoke`) |
| `jsEngine` | No | `rhino` (default) or `graaljs` |
| `onFlowStart` | No | Commands to run before the flow starts |
| `onFlowComplete` | No | Commands to run after the flow ends (pass or fail) |

## Command Quick Reference

### Interaction

| Command | Simple Form | Purpose |
|---------|-------------|---------|
| `tapOn` | `- tapOn: "Text"` | Tap an element |
| `doubleTapOn` | `- doubleTapOn: "Text"` | Double-tap |
| `longPressOn` | `- longPressOn: "Text"` | Long press |
| `inputText` | `- inputText: "hello"` | Type text into focused field |
| `eraseText` | `- eraseText: 5` | Erase N characters (or all) |
| `pressKey` | `- pressKey: Enter` | Press a key (Enter, home, back, etc.) |
| `swipe` | `- swipe: { direction: LEFT }` | Swipe gesture |
| `scroll` | `- scroll` | Simple scroll down |
| `scrollUntilVisible` | see API ref | Scroll until element appears |
| `hideKeyboard` | `- hideKeyboard` | Dismiss keyboard |

### Navigation & App Lifecycle

| Command | Simple Form | Purpose |
|---------|-------------|---------|
| `launchApp` | `- launchApp` | Launch app (with optional `clearState`, `permissions`) |
| `stopApp` | `- stopApp` | Stop current app |
| `killApp` | `- killApp` | Force kill (Android: process death) |
| `openLink` | `- openLink: "https://..."` | Open URL or deep link |
| `back` | `- back` | Press back (Android only) |
| `clearState` | `- clearState` | Clear app data |

### Assertions

| Command | Simple Form | Purpose |
|---------|-------------|---------|
| `assertVisible` | `- assertVisible: "Text"` | Assert element is visible |
| `assertNotVisible` | `- assertNotVisible: "Text"` | Assert element is not visible |
| `assertTrue` | `- assertTrue: "1 + 1 === 2"` | Assert JS expression is truthy |

### Waiting

| Command | Purpose |
|---------|---------|
| `extendedWaitUntil` | Wait for element to appear/disappear with timeout |
| `waitForAnimationToEnd` | Wait until animations settle |

### Flow Control

| Command | Purpose |
|---------|---------|
| `runFlow` | Run a subflow from a file or inline, optionally conditional |
| `runScript` | Execute a JavaScript file |
| `repeat` | Repeat commands N times or while a condition is true |
| `retry` | Retry commands up to N times (max 3) on failure |

### Clipboard & Text

| Command | Purpose |
|---------|---------|
| `copyTextFrom` | Copy text from a UI element into `maestro.copiedText` |
| `setClipboard` | Set arbitrary text to clipboard |
| `pasteText` | Paste clipboard into focused field |

### Device & Media

| Command | Purpose |
|---------|---------|
| `setLocation` | Spoof GPS coordinates |
| `setOrientation` | Set portrait/landscape |
| `addMedia` | Add images/videos to device gallery |
| `toggleAirplaneMode` | Toggle airplane mode |
| `travel` | Simulate movement between GPS points |

### Recording & Screenshots

| Command | Purpose |
|---------|---------|
| `takeScreenshot` | Capture screenshot to file |
| `startRecording` | Begin video recording |
| `stopRecording` | End video recording |

### AI-Powered (Experimental)

| Command | Purpose |
|---------|---------|
| `assertWithAI` | AI-based visual assertion |
| `assertNoDefectsWithAI` | AI-based defect detection |
| `extractTextWithAI` | AI-based text extraction from screen |

## Selectors

Selectors identify which UI element a command targets. Combine them for precision.

### Core

- **`text`**: Visible text or accessibility label (regex). `- tapOn: "Login"` is shorthand for `text: "Login"`.
- **`id`**: Accessibility identifier / resource ID (regex).
- **`index`**: 0-based index when multiple elements match.
- **`point`**: Screen coordinates (`"50%, 50%"` or `"100, 250"`).
- **`css`**: CSS selector (web only).

### Relational

- **`above`** / **`below`** / **`leftOf`** / **`rightOf`**: Position relative to an anchor element.
- **`containsChild`**: Parent with a direct child matching criteria.
- **`childOf`**: Element that is a direct child of a parent.
- **`containsDescendants`**: Parent with specific descendants at any depth.

### State

- **`enabled`**: `true` / `false` — interactive state.
- **`checked`**: `true` / `false` — checkbox/switch state.
- **`focused`**: `true` / `false` — has keyboard focus.
- **`selected`**: `true` / `false` — selected tab/segment.

### Traits

- **`traits: text`**: Any element containing text.
- **`traits: long-text`**: Element with 200+ characters.
- **`traits: square`**: Element with ~1:1 aspect ratio.

## Common Arguments

Every command supports these optional fields:

- **`label`**: Custom display name for the step in output.
- **`optional`**: If `true`, flow continues even if the command fails (logged as warning).

## Conditions (`when`)

`runFlow` and `runScript` support conditional execution:

```yaml
- runFlow:
    when:
      visible: "Some Element"      # element is visible
      # notVisible: "Other"        # element is NOT visible
      # platform: iOS              # platform check (Android|iOS|Web)
      # true: ${MY_VAR == 'yes'}   # JavaScript expression
    commands:
      - tapOn: "Some Element"
```

Multiple conditions are ANDed together.

## Environment Variables

Access env vars with `${VAR_NAME}` syntax anywhere in YAML values:

```yaml
env:
  USERNAME: "default_user"
---
- inputText: ${USERNAME}
```

Override at runtime: `maestro test -e USERNAME=other_user flow.yaml`

## JavaScript Integration

Use `runScript` to execute JS files. Access env vars directly. Use `output` object to pass data back to the flow:

```javascript
// scripts/setup.js
var name = "User_" + Date.now();
output.generatedName = name;
```

```yaml
- runScript: scripts/setup.js
- inputText: ${output.generatedName}
```

### HTTP Requests in JS

```javascript
var response = http.get("https://api.example.com/data");
var data = json(response.body);
output.userId = data.id;
```

Methods: `http.get()`, `http.post()`, `http.put()`, `http.delete()`, `http.request()`.

## CLI Commands

| Command | Purpose |
|---------|---------|
| `maestro test flow.yaml` | Run a single flow |
| `maestro test dir/` | Run all flows in a directory |
| `maestro test --format junit dir/` | Generate JUnit report |
| `maestro test --format html dir/` | Generate HTML report |
| `maestro test -e KEY=VAL flow.yaml` | Pass env vars at runtime |
| `maestro test --include-tags smoke dir/` | Run only flows with tag |
| `maestro studio` | Launch interactive browser IDE |
| `maestro cloud` | Run tests in Maestro Cloud |

## Additional Resources

- Full command API with all options: [resources/api-reference.md](resources/api-reference.md)
- JavaScript & HTTP reference: [resources/javascript-reference.md](resources/javascript-reference.md)
- CLI commands & flags: [resources/cli-reference.md](resources/cli-reference.md)
- Best practices and patterns: [resources/best-practices.md](resources/best-practices.md)
- Maestro MCP tool reference: [resources/mcp-reference.md](resources/mcp-reference.md)
- Annotated examples: [examples/](examples/README.md) (utilities, test flows, advanced patterns, project structure)
- Official docs: https://maestro.mobile.dev
