---
name: unity-playmode-testing
description: 'Supports Unity Play Mode control, input simulation, UI automation, and
  visual verification. Integrates test execution, screenshot/video capture, and console
  log checking. Use when: starting Play Mode,'
---

---
name: unity-playmode-testing
description: Supports Unity Play Mode control, input simulation, UI automation, and visual verification. Integrates test execution, screenshot/video capture, and console log checking. Use when: starting Play Mode, input simulation, UI clicks, screenshots, video recording, test execution
allowed-tools: Read, Grep, Glob
---

# Unity PlayMode & Testing

A guide for Play Mode control, input simulation, UI automation, and visual verification.

## Quick Start

### 1. Play Mode Control

```javascript
// Start Play Mode
mcp__unity-mcp-server__play_game()

// Check state
mcp__unity-mcp-server__get_editor_state()

// Stop
mcp__unity-mcp-server__stop_game()
```

### 2. Input Simulation

```javascript
// Keyboard input
mcp__unity-mcp-server__input_keyboard({
  action: "press",
  key: "w",
  holdSeconds: 1.0
})

// Mouse click
mcp__unity-mcp-server__input_mouse({
  action: "click",
  x: 500,
  y: 300,
  button: "left"
})
```

### 3. Screenshot

```javascript
// Capture Game View
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "game"
})
```

## Play Mode Control

### Start, Pause, Stop

```javascript
// Start Play Mode
mcp__unity-mcp-server__play_game()

// Pause/Resume (toggle)
mcp__unity-mcp-server__pause_game()

// Stop (return to Edit Mode)
mcp__unity-mcp-server__stop_game()
```

### Check State

```javascript
// Get current state
mcp__unity-mcp-server__get_editor_state()
// Returns: { isPlaying: true/false, isPaused: true/false }
```

### Wait for State

```javascript
// Wait until Play Mode starts
mcp__unity-mcp-server__playmode_wait_for_state({
  isPlaying: true,
  timeoutMs: 10000,  // 10 second timeout
  pollMs: 500        // Check every 500ms
})

// Wait until Edit Mode
mcp__unity-mcp-server__playmode_wait_for_state({
  isPlaying: false,
  timeoutMs: 5000
})
```

## Input Simulation

### Keyboard Input

```javascript
// Press key
mcp__unity-mcp-server__input_keyboard({
  action: "press",
  key: "space"
})

// Release key
mcp__unity-mcp-server__input_keyboard({
  action: "release",
  key: "space"
})

// Auto-release with holdSeconds
mcp__unity-mcp-server__input_keyboard({
  action: "press",
  key: "w",
  holdSeconds: 2.0  // Auto-release after 2 seconds
})

// Text input
mcp__unity-mcp-server__input_keyboard({
  action: "type",
  text: "Hello World",
  typingSpeed: 50  // 50ms interval
})

// Key combo
mcp__unity-mcp-server__input_keyboard({
  action: "combo",
  keys: ["ctrl", "shift", "s"],
  holdSeconds: 0.1
})
```

### Mouse Input

```javascript
// Move
mcp__unity-mcp-server__input_mouse({
  action: "move",
  x: 500,
  y: 300,
  absolute: true  // Screen coordinates
})

// Click
mcp__unity-mcp-server__input_mouse({
  action: "click",
  x: 500,
  y: 300,
  button: "left",  // left, right, middle
  clickCount: 2    // Double-click
})

// Drag
mcp__unity-mcp-server__input_mouse({
  action: "drag",
  startX: 100,
  startY: 100,
  endX: 300,
  endY: 300,
  button: "left"
})

// Scroll
mcp__unity-mcp-server__input_mouse({
  action: "scroll",
  deltaY: -120  // Negative=down, Positive=up
})

// Button hold
mcp__unity-mcp-server__input_mouse({
  action: "button",
  buttonAction: "press",
  button: "left",
  holdSeconds: 1.0
})
```

### Gamepad Input

```javascript
// Button press
mcp__unity-mcp-server__input_gamepad({
  action: "button",
  button: "a",  // a/cross, b/circle, x/square, y/triangle, start, select, etc.
  buttonAction: "press"
})

// Analog stick
mcp__unity-mcp-server__input_gamepad({
  action: "stick",
  stick: "left",
  x: 1.0,   // -1.0 to 1.0
  y: 0.5,
  holdSeconds: 1.0
})

// Trigger
mcp__unity-mcp-server__input_gamepad({
  action: "trigger",
  trigger: "right",
  value: 0.8,  // 0.0 to 1.0
  holdSeconds: 0.5
})

// D-Pad
mcp__unity-mcp-server__input_gamepad({
  action: "dpad",
  direction: "up",  // up, down, left, right, none
  holdSeconds: 0.3
})
```

### Touch Input

```javascript
// Tap
mcp__unity-mcp-server__input_touch({
  action: "tap",
  x: 500,
  y: 300,
  touchId: 0
})

// Swipe
mcp__unity-mcp-server__input_touch({
  action: "swipe",
  startX: 100,
  startY: 500,
  endX: 100,
  endY: 200,
  duration: 300  // ms
})

// Pinch (zoom)
mcp__unity-mcp-server__input_touch({
  action: "pinch",
  centerX: 400,
  centerY: 300,
  startDistance: 100,
  endDistance: 200  // Zoom in
})

// Multi-touch
mcp__unity-mcp-server__input_touch({
  action: "multi",
  touches: [
    { x: 100, y: 200, phase: "began" },
    { x: 300, y: 200, phase: "began" }
  ]
})
```

### Batch Input (Execute Multiple Actions Sequentially)

```javascript
// Keyboard batch
mcp__unity-mcp-server__input_keyboard({
  actions: [
    { action: "press", key: "w", holdSeconds: 1.0 },
    { action: "press", key: "space" },
    { action: "type", text: "test" }
  ]
})

// Mouse batch
mcp__unity-mcp-server__input_mouse({
  actions: [
    { action: "move", x: 100, y: 100 },
    { action: "click", button: "left" },
    { action: "move", x: 200, y: 200 },
    { action: "click", button: "left" }
  ]
})
```

## UI Automation

### elementPath (uGUI / UI Toolkit / IMGUI)

The `path` (= `elementPath`) returned by `find_ui_elements` differs in format depending on the UI system.

- uGUI: `/Canvas/...` (GameObject hierarchy path)
- UI Toolkit: `uitk:<UIDocument GameObject path>#<VisualElement.name>`
  - Example: `uitk:/UITK/UIDocument#UITK_Button`
- IMGUI: `imgui:<controlId>` (ID registered in OnGUI)
  - Example: `imgui:IMGUI/Button`

Test scenes:
- uGUI: `UnityMCPServer/Assets/Scenes/MCP_UI_UGUI_TestScene.unity`
- UI Toolkit: `UnityMCPServer/Assets/Scenes/MCP_UI_UITK_TestScene.unity`
- IMGUI: `UnityMCPServer/Assets/Scenes/MCP_UI_IMGUI_TestScene.unity`
- uGUI/UI Toolkit/IMGUI combined: `UnityMCPServer/Assets/Scenes/MCP_UI_AllSystems_TestScene.unity`
  - Note: UI is generated by `McpAllUiSystemsTestBootstrap` at Play Mode start, so it's not visible in Edit Mode
- MCP E2E tests (scene load → Play Mode → ui_* tool calls):
  - stdio / tools/call: `node --test mcp-server/tests/e2e/ui-automation-mcp-protocol.test.js`
  - UnityConnection direct: `node --test mcp-server/tests/e2e/ui-automation-scenes.test.js`

### Search UI Elements

```javascript
// Search by element type
mcp__unity-mcp-server__find_ui_elements({
  elementType: "Button"
})

// Search by name pattern
mcp__unity-mcp-server__find_ui_elements({
  namePattern: "Start.*",  // Regular expression
  includeInactive: true
})

// Search within Canvas
mcp__unity-mcp-server__find_ui_elements({
  elementType: "Toggle",
  canvasFilter: "SettingsCanvas"
})
```

### UI Click

```javascript
// Click by element path
mcp__unity-mcp-server__click_ui_element({
  elementPath: "/Canvas/StartButton"
})

// UI Toolkit (specify VisualElement by name under UIDocument)
mcp__unity-mcp-server__click_ui_element({
  elementPath: "uitk:/UITK/UIDocument#UITK_Button"
})

// IMGUI (specify controlId registered in OnGUI)
mcp__unity-mcp-server__click_ui_element({
  elementPath: "imgui:IMGUI/Button"
})

// Note: UI Toolkit / IMGUI ignore holdDuration / position (returned as warning)

// Right-click
mcp__unity-mcp-server__click_ui_element({
  elementPath: "/Canvas/ContextMenu",
  clickType: "right"
})

// Long press
mcp__unity-mcp-server__click_ui_element({
  elementPath: "/Canvas/HoldButton",
  holdDuration: 1000  // 1 second
})

// Click at specific position within element
mcp__unity-mcp-server__click_ui_element({
  elementPath: "/Canvas/Slider",
  position: { x: 0.8, y: 0.5 }  // Relative coordinates 0-1
})
```

### Get UI Element State

```javascript
// Get element state
mcp__unity-mcp-server__get_ui_element_state({
  elementPath: "/Canvas/StartButton",
  includeInteractableInfo: true
})
// Returns: interactable, visible, position, size, etc.

// Include children
mcp__unity-mcp-server__get_ui_element_state({
  elementPath: "/Canvas/Panel",
  includeChildren: true
})
```

### Set UI Value

```javascript
// Set text to InputField
mcp__unity-mcp-server__set_ui_element_value({
  elementPath: "/Canvas/NameInput",
  value: "PlayerName",
  triggerEvents: true  // Fire OnValueChanged etc.
})

// Set Slider value
mcp__unity-mcp-server__set_ui_element_value({
  elementPath: "/Canvas/VolumeSlider",
  value: 0.75
})

// Set Toggle state
mcp__unity-mcp-server__set_ui_element_value({
  elementPath: "/Canvas/MuteToggle",
  value: true
})

// Select Dropdown
mcp__unity-mcp-server__set_ui_element_value({
  elementPath: "/Canvas/DifficultyDropdown",
  value: "Hard"  // or index
})
```

### Compound UI Sequence

```javascript
// Execute multiple UI operations sequentially
mcp__unity-mcp-server__simulate_ui_input({
  inputSequence: [
    { type: "click", params: { elementPath: "/Canvas/NameInput" }},
    { type: "setvalue", params: { elementPath: "/Canvas/NameInput", value: "Player1" }},
    { type: "click", params: { elementPath: "/Canvas/StartButton" }}
  ],
  waitBetween: 500,     // Wait 500ms between actions
  validateState: true   // Validate state after each action
})
```

## Visual Capture

### Screenshot

```javascript
// Game View
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "game"
})

// Scene View
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "scene"
})

// Specify resolution
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "game",
  width: 1920,
  height: 1080
})

// Exclude UI
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "game",
  includeUI: false
})

// Get as Base64 (for immediate analysis)
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "game",
  encodeAsBase64: true
})
```

### Explorer Mode (LLM-Optimized Capture)

```javascript
// Focus on specific object
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "explorer",
  explorerSettings: {
    target: {
      type: "gameObject",
      name: "Player",
      includeChildren: true
    },
    camera: {
      autoFrame: true,
      padding: 0.2
    }
  }
})

// Capture multiple objects by tag
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "explorer",
  explorerSettings: {
    target: {
      type: "tag",
      tag: "Enemy"
    },
    display: {
      showBounds: true,
      highlightTarget: true
    }
  }
})

// Specify area
mcp__unity-mcp-server__capture_screenshot({
  captureMode: "explorer",
  explorerSettings: {
    target: {
      type: "area",
      center: { x: 0, y: 0, z: 0 },
      radius: 10
    }
  }
})
```

### Screenshot Analysis

```javascript
// Basic analysis (colors, size)
mcp__unity-mcp-server__analyze_screenshot({
  imagePath: "Assets/../.unity/capture/screenshot.png",
  analysisType: "basic"
})

// UI element detection
mcp__unity-mcp-server__analyze_screenshot({
  analysisType: "ui"
})

// Scene content analysis
mcp__unity-mcp-server__analyze_screenshot({
  analysisType: "content"
})

// Full analysis
mcp__unity-mcp-server__analyze_screenshot({
  analysisType: "full",
  prompt: "Find all buttons in the UI"
})
```

### Video Recording

```javascript
// Start recording
mcp__unity-mcp-server__capture_video_start({
  captureMode: "game",
  fps: 30,
  width: 1280,
  height: 720
})

// Check recording status
mcp__unity-mcp-server__capture_video_status()

// Stop recording
mcp__unity-mcp-server__capture_video_stop()

// One-shot recording (record for N seconds and auto-stop)
mcp__unity-mcp-server__video_capture_for({
  durationSec: 10,
  play: true,  // Auto-start Play Mode
  fps: 30
})
```

## Testing & Debugging

### Run Tests

```javascript
// Run EditMode tests
mcp__unity-mcp-server__run_tests({
  testMode: "EditMode"
})

// Run PlayMode tests
mcp__unity-mcp-server__run_tests({
  testMode: "PlayMode"
})

// Run both
mcp__unity-mcp-server__run_tests({
  testMode: "All"
})

// With filters
mcp__unity-mcp-server__run_tests({
  testMode: "EditMode",
  filter: "PlayerTests",          // Class name
  namespace: "Tests.Player",      // Namespace
  category: "Unit",               // Category
  includeDetails: true
})

// Export results to XML
mcp__unity-mcp-server__run_tests({
  testMode: "All",
  exportPath: "TestResults/results.xml"
})
```

### Check Test Status

```javascript
// Test execution status
mcp__unity-mcp-server__get_test_status()

// With result summary
mcp__unity-mcp-server__get_test_status({
  includeTestResults: true,
  includeFileContent: true
})
```

### Console Logs

```javascript
// Read logs
mcp__unity-mcp-server__read_console({
  count: 100,
  logTypes: ["Log", "Warning", "Error"]
})

// Errors only
mcp__unity-mcp-server__read_console({
  logTypes: ["Error"],
  includeStackTrace: true
})

// Text filter
mcp__unity-mcp-server__read_console({
  filterText: "Player",
  sortOrder: "newest"
})

// Time range specification
mcp__unity-mcp-server__read_console({
  sinceTimestamp: "2024-01-01T00:00:00Z"
})

// Clear console
mcp__unity-mcp-server__clear_console({
  preserveErrors: true  // Keep errors
})
```

## Common Workflows

### UI Automated Testing

```javascript
// 1. Start Play Mode
mcp__unity-mcp-server__play_game()
mcp__unity-mcp-server__playmode_wait_for_state({ isPlaying: true })

// 2. Menu operation
mcp__unity-mcp-server__click_ui_element({
  elementPath: "/Canvas/MainMenu/StartButton"
})

// 3. Wait
await new Promise(r => setTimeout(r, 1000))

// 4. Input
mcp__unity-mcp-server__set_ui_element_value({
  elementPath: "/Canvas/NameInput",
  value: "TestPlayer"
})

// 5. Confirm button
mcp__unity-mcp-server__click_ui_element({
  elementPath: "/Canvas/ConfirmButton"
})

// 6. Screenshot result
mcp__unity-mcp-server__capture_screenshot({ captureMode: "game" })

// 7. Check console for errors
mcp__unity-mcp-server__read_console({ logTypes: ["Error"] })

// 8. Stop
mcp__unity-mcp-server__stop_game()
```

### Gameplay Recording

```javascript
// 1. Start Play Mode with recording
mcp__unity-mcp-server__video_capture_for({
  durationSec: 30,
  play: true
})

// Or manual control:
mcp__unity-mcp-server__play_game()
mcp__unity-mcp-server__capture_video_start()

// 2. Gameplay input
mcp__unity-mcp-server__input_keyboard({
  actions: [
    { action: "press", key: "w", holdSeconds: 2.0 },
    { action: "press", key: "space" },
    { action: "press", key: "a", holdSeconds: 1.0 }
  ]
})

// 3. Stop recording
mcp__unity-mcp-server__capture_video_stop()
mcp__unity-mcp-server__stop_game()
```

### Bug Reproduction Automation

```javascript
// 1. Load scene
mcp__unity-mcp-server__load_scene({
  scenePath: "Assets/Scenes/BugScene.unity"
})

// 2. Start Play Mode
mcp__unity-mcp-server__play_game()
mcp__unity-mcp-server__playmode_wait_for_state({ isPlaying: true })

// 3. Reproduction steps
mcp__unity-mcp-server__input_keyboard({
  action: "press",
  key: "e",
  holdSeconds: 0.5
})

mcp__unity-mcp-server__input_mouse({
  action: "click",
  x: 500,
  y: 300
})

// 4. Check for errors
mcp__unity-mcp-server__read_console({
  logTypes: ["Error"],
  includeStackTrace: true
})

// 5. Screenshot
mcp__unity-mcp-server__capture_screenshot({ captureMode: "game" })

// 6. Stop
mcp__unity-mcp-server__stop_game()
```

## Common Mistakes

### 1. Missing Play Mode State Check

```javascript
// ❌ Input without state check
mcp__unity-mcp-server__input_keyboard({ action: "press", key: "w" })

// ✅ Input after confirming Play Mode
mcp__unity-mcp-server__play_game()
mcp__unity-mcp-server__playmode_wait_for_state({ isPlaying: true })
mcp__unity-mcp-server__input_keyboard({ action: "press", key: "w" })
```

### 2. Forgetting Immediate Key Release

```javascript
// ❌ Forgetting release after press (key stays pressed)
mcp__unity-mcp-server__input_keyboard({ action: "press", key: "shift" })

// ✅ Auto-release with holdSeconds
mcp__unity-mcp-server__input_keyboard({
  action: "press",
  key: "shift",
  holdSeconds: 0.5
})
```

### 3. Wrong UI Element Path

```javascript
// ❌ Relative path
elementPath: "Canvas/Button"

// ✅ Absolute path (leading slash)
elementPath: "/Canvas/Button"
```

### 4. Forgetting to Stop Recording

```javascript
// ✅ Always stop recording
mcp__unity-mcp-server__capture_video_start()
// ... recording process ...
mcp__unity-mcp-server__capture_video_stop()  // Don't forget!

// ✅ Or use video_capture_for for auto-stop
mcp__unity-mcp-server__video_capture_for({ durationSec: 10 })
```

### 5. Test Execution Timing

```javascript
// ❌ Trying to run PlayMode tests in Edit Mode
// (Unity automatically switches to Play Mode, but timing requires attention)

// ✅ Explicitly specify mode
mcp__unity-mcp-server__run_tests({
  testMode: "PlayMode",  // "EditMode" for EditMode tests
  includeDetails: true
})
```

## Tool Reference

| Tool | Purpose |
|------|---------|
| `play_game` | Start Play Mode |
| `pause_game` | Pause/Resume |
| `stop_game` | Stop Play Mode |
| `get_editor_state` | Get state |
| `playmode_wait_for_state` | Wait for state |
| `input_keyboard` | Keyboard input |
| `input_mouse` | Mouse input |
| `input_gamepad` | Gamepad input |
| `input_touch` | Touch input |
| `find_ui_elements` | Search UI elements |
| `click_ui_element` | UI click |
| `get_ui_element_state` | Get UI state |
| `set_ui_element_value` | Set UI value |
| `simulate_ui_input` | Compound UI sequence |
| `capture_screenshot` | Screenshot |
| `analyze_screenshot` | Screenshot analysis |
| `capture_video_start` | Start recording |
| `capture_video_stop` | Stop recording |
| `capture_video_status` | Recording status |
| `video_capture_for` | Record for specified seconds |
| `run_tests` | Run tests |
| `get_test_status` | Test status |
| `read_console` | Read logs |
| `clear_console` | Clear logs |
