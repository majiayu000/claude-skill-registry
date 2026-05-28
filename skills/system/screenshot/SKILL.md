---
name: screenshot
description: >-
  Capture desktop screenshots from the terminal across macOS, Linux, and
  Windows. Supports full-screen, active-window, app-specific, pixel-region,
  and window-ID captures. Use when the user explicitly requests a system
  screenshot or when tool-specific capture (Playwright, Figma MCP) cannot
  reach the target content.
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - automation
    - screenshot
    - desktop-capture
    - cross-platform
  provenance:
    upstream_source: "screenshot"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T20:30:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.61
---

# Desktop Screenshot Capture

Capture screenshots of the full screen, a specific application window, or a pixel region from the terminal on macOS, Linux, and Windows.

## Overview

This skill automates OS-level screenshot capture through a cross-platform Python helper and platform-native fallback commands. It handles save-location logic, multi-display setups, and macOS permission preflight so the assistant never has to re-derive platform-specific commands from scratch.

**What it automates:**

- Full-screen, active-window, app-window, region, and window-ID captures
- Save-path resolution (user path, OS default, or temp directory)
- macOS Screen Recording permission checks
- Multi-display file splitting (one file per display on macOS)

**When to use this skill vs. other tools:**

| Scenario | Tool |
|----------|------|
| Browser page or Electron app content | Playwright MCP screenshot |
| Figma design frame | Figma MCP/skill |
| Desktop app, system UI, or cross-app comparison | This skill |
| User explicitly says "take a screenshot" | This skill |

## Triggers

### When to Run

- User explicitly asks for a desktop or system screenshot
- A visual comparison requires an OS-level capture (e.g., comparing a Figma design against a running app)
- Tool-specific capture (browser, Figma) cannot reach the target content
- User asks to "look at" a desktop application

### Save-Location Rules

Apply these rules in order every time:

1. **User specifies a path** -- save there
2. **User asks for a screenshot without a path** -- save to the OS default screenshot directory
3. **Assistant needs a screenshot for its own inspection** -- save to the temp directory (`--mode temp`)

## Process

### Step 1: Detect Platform

The helper script detects the OS automatically. Confirm prerequisites:

| Platform | Prerequisite |
|----------|-------------|
| macOS | `screencapture` (built-in), Screen Recording permission |
| Linux | One of: `scrot`, `gnome-screenshot`, or ImageMagick `import` |
| Windows | PowerShell (built-in) |

### Step 2: Choose Capture Mode

Select the appropriate flags based on what the user wants:

```bash
SKILL_DIR="<path-to-skill>"

# Full screen (OS default location)
python3 "$SKILL_DIR/scripts/take_screenshot.py"

# Full screen to temp (for assistant inspection)
python3 "$SKILL_DIR/scripts/take_screenshot.py" --mode temp

# Explicit output path
python3 "$SKILL_DIR/scripts/take_screenshot.py" --path output/screen.png

# Active/focused window
python3 "$SKILL_DIR/scripts/take_screenshot.py" --active-window --mode temp

# Pixel region (x,y,width,height)
python3 "$SKILL_DIR/scripts/take_screenshot.py" --region 100,200,800,600

# Specific window by ID
python3 "$SKILL_DIR/scripts/take_screenshot.py" --window-id 12345
```

**macOS-only options:**

```bash
# Capture all windows of an app (substring match)
python3 "$SKILL_DIR/scripts/take_screenshot.py" --app "Safari"

# Specific window title within an app
python3 "$SKILL_DIR/scripts/take_screenshot.py" --app "Terminal" --window-name "bash"

# List matching windows before capturing
python3 "$SKILL_DIR/scripts/take_screenshot.py" --list-windows --app "Xcode"
```

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy Bypass -File "$SKILL_DIR/scripts/take_screenshot.ps1"
powershell -ExecutionPolicy Bypass -File "$SKILL_DIR/scripts/take_screenshot.ps1" -Mode temp
powershell -ExecutionPolicy Bypass -File "$SKILL_DIR/scripts/take_screenshot.ps1" -Region 100,200,800,600
powershell -ExecutionPolicy Bypass -File "$SKILL_DIR/scripts/take_screenshot.ps1" -ActiveWindow
```

### Step 3: macOS Permission Preflight

On macOS, run the preflight helper **once** before any window or app capture. It checks Screen Recording permission, explains why it is needed, and requests it:

```bash
bash "$SKILL_DIR/scripts/ensure_macos_permissions.sh"
```

Combine preflight with capture in a single command to reduce sandbox approval prompts:

```bash
bash "$SKILL_DIR/scripts/ensure_macos_permissions.sh" && \
python3 "$SKILL_DIR/scripts/take_screenshot.py" --app "Finder" --mode temp
```

### Step 4: Read Output Paths

The script prints one absolute path per captured image. When multiple windows or displays match, it prints multiple paths with suffixes like `-w<windowId>` or `-d<display>`. View each path with the image viewer tool.

## Verification

### Success Indicators

- Script exits with code 0
- One or more file paths printed to stdout
- Each printed path points to a valid PNG file

### Failure Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `screen capture checks are blocked in the sandbox` | macOS sandbox prevents permission check | Rerun with escalated permissions |
| `could not create image from display` | Screen Recording permission denied | Run `ensure_macos_permissions.sh`, enable in System Settings |
| `no matching macOS window found` | App not running or window not visible | Run `--list-windows --app "Name"` to inspect, verify app is on-screen |
| `no supported screenshot tool found` | Linux missing scrot/gnome-screenshot/import | Ask user to install: `sudo apt install scrot` |
| `region capture requires scrot or ImageMagick` | Linux region capture needs specific tools | Install scrot or ImageMagick |
| `swift needs module-cache access` | Swift ModuleCache permission error | Rerun with escalated permissions |
| `choose either --region or --window-id` | Mutually exclusive flags used together | Use only one targeting flag per invocation |

## Examples

### Example 1: User Asks for a Screenshot

```
User: Take a screenshot of my desktop
Assistant:
  1. python3 "$SKILL_DIR/scripts/take_screenshot.py"
  Result: /home/user/Pictures/Screenshots/screenshot-2026-02-04_14-30-00.png
  [Views the image and describes what is visible]
```

### Example 2: Inspect a Running App (macOS)

```
User: Take a look at Safari and tell me what you see
Assistant:
  1. bash "$SKILL_DIR/scripts/ensure_macos_permissions.sh"
  2. python3 "$SKILL_DIR/scripts/take_screenshot.py" --app "Safari" --mode temp
  Result: /tmp/codex-shot-2026-02-04_14-31-00-w1234.png
  [Views each captured window image in sequence]
```

### Example 3: Compare Design vs Implementation

```
User: The Figma design doesn't match the running app
Assistant:
  1. [Uses Figma MCP to capture the design frame]
  2. bash "$SKILL_DIR/scripts/ensure_macos_permissions.sh" && \
     python3 "$SKILL_DIR/scripts/take_screenshot.py" --app "MyApp" --mode temp
  3. [Views both screenshots side by side and describes differences]
```

### Example 4: Capture a Specific Region on Linux

```
User: Screenshot the top-left 800x600 area of the screen
Assistant:
  1. python3 "$SKILL_DIR/scripts/take_screenshot.py" --region 0,0,800,600 --path region.png
  Result: region.png
```

## Safety

### Idempotency

Each invocation creates a new timestamped file. Running the skill multiple times produces multiple screenshots without overwriting previous captures.

### Prerequisites

Before running on each platform, ensure:

- **macOS**: Screen Recording permission granted (preflight script handles this)
- **Linux**: At least one of `scrot`, `gnome-screenshot`, or ImageMagick `import` installed
- **Windows**: PowerShell available (standard on Windows 10+)

### Multi-Display Behavior

| Platform | Behavior |
|----------|----------|
| macOS | Full-screen captures produce one file per display (`-d1`, `-d2`) |
| Linux | Full-screen captures the virtual desktop (all monitors combined) |
| Windows | Full-screen captures the virtual desktop (all monitors combined) |

Use `--region` to isolate a single display on Linux or Windows when multiple monitors are connected.

## Script Reference

### take_screenshot.py

Cross-platform Python screenshot helper. Detects the OS and delegates to native tools.

**Arguments:**

| Flag | Description | Platform |
|------|-------------|----------|
| `--path <path>` | Output file path or directory | All |
| `--mode default\|temp` | Save to OS default or temp directory | All |
| `--format <ext>` | Image format (default: `png`) | All |
| `--region x,y,w,h` | Capture pixel region | All |
| `--window-id <id>` | Capture specific window by ID | macOS, Linux |
| `--active-window` | Capture focused window | All |
| `--app <name>` | Capture all windows of named app | macOS only |
| `--window-name <title>` | Filter by window title substring | macOS only |
| `--list-windows` | List matching windows without capture | macOS only |
| `--interactive` | Interactive selection mode | macOS only |

**Mutual exclusions:** `--region`, `--window-id`, `--active-window`, `--app`, and `--interactive` cannot be combined.

### take_screenshot.ps1

PowerShell screenshot helper for Windows. Supports `-Path`, `-Mode`, `-Region`, `-ActiveWindow`, and `-WindowHandle` parameters.

### ensure_macos_permissions.sh

Checks and requests macOS Screen Recording permission. Run once before window or app capture. Routes Swift module cache to `$TMPDIR/codex-swift-module-cache` to avoid extra sandbox prompts.

## References

Load on demand when deeper platform-specific detail is needed:

- **Platform commands**: `references/platform-commands.md` -- native OS screenshot commands and tool installation
