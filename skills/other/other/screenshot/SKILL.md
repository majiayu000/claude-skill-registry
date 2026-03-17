---
name: screenshot
description: Take and analyze a screenshot of the current game state
model: haiku
allowed-tools:
  - Bash
  - mcp__automation__screenshot
  - mcp__automation__getWindows
  - mcp__automation__windowControl
---

# Screenshot Game State

Capture and analyze the current state of GridRacer.

## Steps

### 1. Find Simulator Window
```bash
# Check if simulator is running
xcrun simctl list devices booted
```

### 2. Focus Simulator
Use `mcp__automation__windowControl` to bring Simulator to front.

### 3. Capture Screenshot
Use `mcp__automation__screenshot` with mode "window" for Simulator.

### 4. Analyze

Describe what you see:
- **Track layout**: Shape, obstacles, boundaries
- **Racer position**: Grid coordinates
- **Velocity**: Current direction/speed indicators
- **Move markers**: 9 options, which are green/red
- **HUD**: Lives, laps, turn indicator
- **Game phase**: Setup, playing, ended

### 5. Report

```
Current State:
- Position: (X, Y)
- Velocity: (dX, dY)
- Lives: N
- Lap: M/Total

Valid Moves: N green markers
Crash Moves: M red markers

Observations:
- [Any issues or notable state]
```
