---
name: play-test
description: Visual play-testing via Automation MCP screenshots and numpad input
allowed-tools:
  - Bash
  - Read
  - mcp__automation__screenshot
  - mcp__automation__getWindows
  - mcp__automation__sleep
model: sonnet
---

# Play Test GridRacer

Launch the game and test it visually using Automation MCP with numpad keyboard input.

## Prerequisites
- Build must succeed first
- Automation MCP needs Accessibility + Screen Recording permissions

## Numpad Control Mapping

The game uses numpad keys (1-9) to select acceleration:

```
 7  8  9     ↖  ↑  ↗     (-1,+1) (0,+1) (+1,+1)
 4  5  6  =  ←  ·  →  =  (-1, 0) (0, 0) (+1, 0)
 1  2  3     ↙  ↓  ↘     (-1,-1) (0,-1) (+1,-1)
```

- **5** = coast (no acceleration, maintain velocity)
- **6** = accelerate right
- **4** = accelerate left
- **8** = accelerate up
- **2** = accelerate down
- Corners (1,3,7,9) = diagonal acceleration
- **r** = reset game

## Steps

### 1. Build and Install
```bash
xcodebuild -scheme GridRacer -configuration Debug -destination 'generic/platform=iOS Simulator' build 2>&1 | grep -E "(error:|BUILD|FAILED|SUCCEEDED)" | tail -10
APP_PATH=$(find ~/Library/Developer/Xcode/DerivedData -name "GridRacer.app" -path "*/Build/Products/Debug-iphonesimulator/*" -not -path "*Index.noindex*" -type d 2>/dev/null | head -1)
```

### 2. Boot and Launch
```bash
SIMULATOR=$(xcrun simctl list devices available | grep -E "iPhone (16|15|14)" | head -1 | sed -E 's/.*iPhone ([0-9]+).*/iPhone \1/')
xcrun simctl boot "$SIMULATOR" 2>/dev/null || true
xcrun simctl install booted "$APP_PATH"
xcrun simctl launch booted trouarat.GridRacer
```

### 3. Send Keyboard Input via AppleScript

**IMPORTANT:** The iOS Simulator requires AppleScript to receive keyboard input. Use this bash command pattern:

```bash
# Send a single key to the Simulator
osascript -e 'tell application "Simulator" to activate' && sleep 0.3 && osascript -e 'tell application "System Events" to keystroke "KEY"'
```

Replace `KEY` with the desired key (1-9 for moves, r for reset).

### 4. Play Test Loop

For each turn:
1. **Screenshot** the game state via `mcp__automation__screenshot(mode: "window", windowName: "iPhone 16 Pro")`
2. **Analyze**: Look at HUD for current player, velocity, and position
3. **Observe markers**: Green=safe, red=crash
4. **Send numpad key** via AppleScript bash command
5. **Wait** for animation: `mcp__automation__sleep(ms: 700)`
6. **Screenshot** result and verify:
   - Position changed correctly
   - Velocity updated (old + acceleration)
   - Crash detection works (life lost, respawn)
   - Lap counting works (finish line crossing)

### 5. Reset Game (if needed)
```bash
osascript -e 'tell application "Simulator" to activate' && sleep 0.3 && osascript -e 'tell application "System Events" to keystroke "r"'
```

### 6. Close App
```bash
xcrun simctl terminate booted trouarat.GridRacer
```

## Example Play Test Sequence

```bash
# Screenshot initial state
mcp__automation__screenshot(mode: "window", windowName: "iPhone 16 Pro")

# Player 1: accelerate right (key 6)
osascript -e 'tell application "Simulator" to activate' && sleep 0.3 && osascript -e 'tell application "System Events" to keystroke "6"'
mcp__automation__sleep(ms: 700)
mcp__automation__screenshot(...)

# Player 2: accelerate right (key 6)
osascript -e 'tell application "Simulator" to activate' && sleep 0.3 && osascript -e 'tell application "System Events" to keystroke "6"'
mcp__automation__sleep(ms: 700)
mcp__automation__screenshot(...)

# Continue alternating...
```

## Test Scenarios

### Basic Movement
1. Screenshot initial state (both players at start, vel=(0,0))
2. P1: Press `6` (accelerate right) → vel should become (1,0)
3. P2: Press `6` → P2 vel should become (1,0)
4. P1: Press `5` (coast) → P1 should move by current velocity

### Velocity Accumulation
1. P1: Press `6` three times (interspersed with P2 turns)
2. P1's velocity should grow: (1,0) → (2,0) → (3,0)

### Collision Test
1. Steer a player toward the wall (red markers)
2. Press numpad key for crash trajectory
3. Verify: life lost, respawn, velocity reset to (0,0)

### Lap Completion
1. Navigate around track crossing finish line
2. Verify lap counter increments
