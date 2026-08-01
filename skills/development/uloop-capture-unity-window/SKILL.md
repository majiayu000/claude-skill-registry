---
name: uloop-capture-unity-window
description: 'Capture Unity EditorWindow and save as PNG image. Use when you need
  to: (1) Take a screenshot of Game View, Scene View, Console, Inspector, etc., (2)
  Capture visual state for debugging or verification'
---

---
name: uloop-capture-unity-window
description: Capture Unity EditorWindow and save as PNG image. Use when you need to: (1) Take a screenshot of Game View, Scene View, Console, Inspector, etc., (2) Capture visual state for debugging or verification, (3) Save editor output as an image file.
---

# uloop capture-unity-window

Capture any Unity EditorWindow by name and save as PNG image.

## Usage

```bash
uloop capture-unity-window [--window-name <name>] [--resolution-scale <scale>]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--window-name` | string | `Game` | Window name to capture (e.g., "Game", "Scene", "Console", "Inspector", "Project", "Hierarchy", or any EditorWindow title) |
| `--resolution-scale` | number | `1.0` | Resolution scale (0.1 to 1.0) |

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
uloop capture-unity-window

# Capture Game View at half resolution
uloop capture-unity-window --window-name Game --resolution-scale 0.5

# Capture Scene View
uloop capture-unity-window --window-name Scene

# Capture Console window
uloop capture-unity-window --window-name Console

# Capture Inspector window
uloop capture-unity-window --window-name Inspector

# Capture Project browser
uloop capture-unity-window --window-name Project

# Capture custom EditorWindow by title
uloop capture-unity-window --window-name "My Custom Window"
```

## Output

Returns JSON with:
- `CapturedCount`: Number of windows captured
- `CapturedWindows`: Array of captured window info, each containing:
  - `ImagePath`: Absolute path to the saved PNG image
  - `FileSizeBytes`: Size of the saved file in bytes
  - `Width`: Captured image width in pixels
  - `Height`: Captured image height in pixels

When multiple windows of the same type are open (e.g., multiple Inspector windows), all matching windows are captured with numbered filenames (e.g., `Inspector_1_*.png`, `Inspector_2_*.png`).

## Notes

- Use `uloop focus-window` first if needed
- Target window must be open in Unity Editor
- Window name matching is case-insensitive
