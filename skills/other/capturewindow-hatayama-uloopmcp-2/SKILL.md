---
name: uloop-screenshot
description: "Take a screenshot of Unity Editor windows and save as PNG image. Use when you need to: (1) Screenshot the Game View, Scene View, Console, Inspector, or other windows, (2) Capture current visual state for debugging or documentation, (3) Save what the Editor looks like as an image file."
---

# uloop capture-window

Capture any Unity EditorWindow by name and save as PNG.

## Usage

```bash
uloop capture-window [--window-name <name>] [--resolution-scale <scale>] [--match-mode <mode>]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--window-name` | string | `Game` | Window name to capture (e.g., "Game", "Scene", "Console", "Inspector", "Project", "Hierarchy", or any EditorWindow title) |
| `--resolution-scale` | number | `1.0` | Resolution scale (0.1 to 1.0) |
| `--match-mode` | enum | `exact` | Window name matching mode: `exact`, `prefix`, or `contains`. All modes are case-insensitive. |

## Match Modes

| Mode | Description | Example |
|------|-------------|---------|
| `exact` | Window name must match exactly (case-insensitive) | "Project" matches "Project" only |
| `prefix` | Window name must start with the input | "Project" matches "Project" and "Project Settings" |
| `contains` | Window name must contain the input anywhere | "set" matches "Project Settings" |

## Window Name

The window name is the text displayed in the window's title bar (tab). The user (human) will tell you which window to capture. Common window names include:

- **Game**: Game View window
- **Scene**: Scene View window
- **Console**: Console window
- **Inspector**: Inspector window
- **Project**: Project browser window
- **Hierarchy**: Hierarchy window
- **Animation**: Animation window
- **Animator**: Animator window
- **Profiler**: Profiler window
- **Audio Mixer**: Audio Mixer window

You can also specify custom EditorWindow titles (e.g., "EditorWindow Capture Test").

## Examples

```bash
# Capture Game View at full resolution
uloop capture-window

# Capture Game View at half resolution
uloop capture-window --window-name Game --resolution-scale 0.5

# Capture Scene View
uloop capture-window --window-name Scene

# Capture Console window
uloop capture-window --window-name Console

# Capture Inspector window
uloop capture-window --window-name Inspector

# Capture Project browser (exact match - won't match "Project Settings")
uloop capture-window --window-name Project

# Capture all windows starting with "Project" (prefix match)
uloop capture-window --window-name Project --match-mode prefix

# Capture custom EditorWindow by title
uloop capture-window --window-name "My Custom Window"
```

## Output

Returns JSON with:
- `CapturedCount`: Number of windows captured
- `CapturedWindows`: Array of captured window info, each containing:
  - `ImagePath`: Absolute path to the saved PNG file
  - `FileSizeBytes`: Size of the saved file in bytes
  - `Width`: Captured image width in pixels
  - `Height`: Captured image height in pixels

When multiple windows match (e.g., multiple Inspector windows or when using `contains` mode), all matching windows are captured with numbered filenames (e.g., `Inspector_1_*.png`, `Inspector_2_*.png`).

## Notes

- Use `uloop focus-window` first if needed
- Target window must be open in Unity Editor
- Window name matching is always case-insensitive
