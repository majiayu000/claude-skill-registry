---
name: dev-test-linux
description: This skill should be used when the user asks to "test Linux desktop apps", "automate GTK/Qt applications", "test with ydotool", "test with xdotool", "verify Linux UI interactions", "capture screenshots on Linux", "control D-Bus services", "test Wayland applications", "test X11 applications", or needs Linux desktop E2E testing. Provides comprehensive guidance for Linux automation with ydotool (Wayland), xdotool (X11), grim, and D-Bus.
version: 0.1.0
---

<EXTREMELY-IMPORTANT>
## Gate Reminder

Before taking screenshots or running E2E tests, you MUST complete all 6 gates from dev-tdd:

```
GATE 1: BUILD
GATE 2: LAUNCH (with file-based logging)
GATE 3: WAIT
GATE 4: CHECK PROCESS
GATE 5: READ LOGS ← MANDATORY, CANNOT SKIP
GATE 6: VERIFY LOGS
THEN: E2E tests/screenshots
```

**You loaded dev-tdd earlier. Follow the gates now.**
</EXTREMELY-IMPORTANT>

## Contents

- [Tool Availability Gate](#tool-availability-gate)
- [When to Use Linux Automation](#when-to-use-linux-automation)
- [Detect Display Server](#detect-display-server)
- [Wayland: ydotool](#wayland-ydotool)
- [X11: xdotool](#x11-xdotool)
- [Screenshots](#screenshots)
- [D-Bus Control](#d-bus-control)
- [Accessibility (AT-SPI)](#accessibility-at-spi)
- [Complete E2E Examples](#complete-e2e-examples)

# Linux Desktop Automation

<EXTREMELY-IMPORTANT>
## Tool Availability Gate

Verify automation tools are installed before proceeding.

```bash
# Detect display server (check for Wayland vs X11)
echo $XDG_SESSION_TYPE  # "wayland" or "x11"

# Wayland tools check (verify ydotool, wtype, grim, slurp)
which ydotool || echo "MISSING: ydotool"
which wtype || echo "MISSING: wtype"
which grim || echo "MISSING: grim"
which slurp || echo "MISSING: slurp"

# X11 tools check (verify xdotool, xclip, scrot)
which xdotool || echo "MISSING: xdotool"
which xclip || echo "MISSING: xclip"
which scrot || echo "MISSING: scrot"

# D-Bus check (verify dbus-send availability)
which dbus-send || echo "MISSING: dbus-send"
```

**If missing (Wayland):**
```
STOP: Cannot proceed with Wayland automation.

Missing tools for Wayland E2E testing.

Install with:
  # Arch
  sudo pacman -S ydotool wtype grim slurp

  # Debian/Ubuntu
  sudo apt install ydotool wtype grim slurp

  # Nix
  nix-env -iA nixpkgs.ydotool nixpkgs.wtype nixpkgs.grim nixpkgs.slurp

Start ydotool daemon:
  sudo systemctl enable --now ydotool
  # Or for user service:
  systemctl --user enable --now ydotool

Reply when installed and I'll continue testing.
```

**This gate is non-negotiable. Missing tools = full stop.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## When to Use Linux Automation

Use Linux automation (ydotool/xdotool) for:
- Linux native application automation
- GTK/Qt application testing
- System-wide keyboard/mouse control
- Window management testing
- D-Bus service interaction
- Accessibility testing (AT-SPI)

Do NOT use Linux automation for:
- Testing web applications (use Chrome MCP or Playwright)
- macOS desktop automation (use dev-test-hammerspoon)
- Cross-platform testing

For web testing, use:
- `Skill(skill="workflows:dev-test-chrome")` - debugging
- `Skill(skill="workflows:dev-test-playwright")` - CI/CD

### Rationalization Prevention

| Thought | Reality |
|---------|---------|
| "I can test the app manually" | AUTOMATE IT with ydotool/xdotool |
| "Web testing tools work for desktop apps" | NO. Use native Linux tools |
| "ydotool daemon is hard to set up" | One-time setup. Do it. |
| "X11 is deprecated, skip xdotool" | Many systems still use X11. Support both. |
| "D-Bus is too complex" | D-Bus gives precise control. Learn it. |

### Display Server Detection

```bash
# Detect display server and choose appropriate tools
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    # Use ydotool, wtype, grim
else
    # Use xdotool, xclip, scrot
fi
```

Always detect display server before choosing tools.
</EXTREMELY-IMPORTANT>

## Detect Display Server

```bash
# Check display server type (Wayland or X11)
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    echo "Using Wayland tools (ydotool, wtype, grim)"
else
    echo "Using X11 tools (xdotool, xclip, scrot)"
fi
```

## Wayland: ydotool

Requires ydotoold daemon running.

### Keyboard Input

```bash
# Type text (simple text input to focused window)
ydotool type "hello world"

# Type with delay (type text with microsecond delay between keys)
ydotool type --delay 50 "slow typing"

# Press Enter key (send Enter key using keycode format)
ydotool key 28:1 28:0

# Press Escape key (send Escape key)
ydotool key 1:1 1:0

# Press Ctrl+C (send Ctrl+C combination)
ydotool key 29:1 46:1 46:0 29:0

# Press Ctrl+V (send Ctrl+V combination)
ydotool key 29:1 47:1 47:0 29:0

# Press Alt+Tab (send Alt+Tab combination)
ydotool key 56:1 15:1 15:0 56:0

# Common keycodes reference
# 1=Escape, 14=Backspace, 15=Tab, 28=Enter, 29=Ctrl, 42=LShift
# 56=Alt, 57=Space, 100=RightAlt, 125=Super/Win
```

### Alternative: wtype (Wayland-native)

```bash
# Type text (simple text input to focused window)
wtype "hello world"

# Press Ctrl+C (send Ctrl+C combination)
wtype -M ctrl -k c

# Press Ctrl+Shift+S (send Ctrl+Shift+S combination)
wtype -M ctrl -M shift -k s

# Press Enter (send Enter key)
wtype -k Return

# Press Escape (send Escape key)
wtype -k Escape
```

Available modifiers: shift, ctrl, alt, logo (super)

### Mouse Input

```bash
# Move mouse to absolute position (move cursor to screen coordinates)
ydotool mousemove --absolute 100 200

# Move mouse relative (move cursor by relative offset)
ydotool mousemove 50 -30

# Click left button (send left mouse click)
ydotool click 1

# Click right button (send right mouse click)
ydotool click 3

# Double click (send double click)
ydotool click 1 1

# Click at position (move and click in one operation)
ydotool mousemove --absolute 500 300 && ydotool click 1

# Drag operation (move mouse while holding button)
ydotool mousemove --absolute 100 100
ydotool mousedown 1
ydotool mousemove --absolute 200 200
ydotool mouseup 1
```

## X11: xdotool

### Keyboard Input

```bash
# Type text (simple text input to focused window)
xdotool type "hello world"

# Press Return (send Return key)
xdotool key Return

# Press Escape (send Escape key)
xdotool key Escape

# Press Ctrl+C (send Ctrl+C combination)
xdotool key ctrl+c

# Press Ctrl+Shift+S (send Ctrl+Shift+S combination)
xdotool key ctrl+shift+s

# Press Alt+Tab (send Alt+Tab combination)
xdotool key alt+Tab

# Press Super+D (send Super+D combination)
xdotool key super+d

# Type with delay (type text with millisecond delay between keys)
xdotool type --delay 50 "slow typing"

# Hold key down (press and hold Ctrl)
xdotool keydown ctrl

# Press C (send C key)
xdotool key c

# Release key (release Ctrl)
xdotool keyup ctrl
```

### Mouse Input

```bash
# Move mouse absolute (move cursor to screen coordinates)
xdotool mousemove 100 200

# Move mouse relative (move cursor by relative offset)
xdotool mousemove --relative 50 30

# Click left button (send left mouse click)
xdotool click 1

# Click middle button (send middle mouse click)
xdotool click 2

# Click right button (send right mouse click)
xdotool click 3

# Double click (send double click)
xdotool click --repeat 2 1

# Click at position (move and click in one operation)
xdotool mousemove 500 300 click 1

# Drag operation (move mouse while holding button)
xdotool mousemove 100 100 mousedown 1 mousemove 200 200 mouseup 1
```

### Window Control (X11)

```bash
# Get active window ID (get numeric window identifier)
xdotool getactivewindow

# Focus window by name (find and focus window matching name)
xdotool search --name "Firefox" windowactivate

# Focus window by class (find and focus window matching class)
xdotool search --class "firefox" windowactivate

# Get window title (get title of active window)
xdotool getactivewindow getwindowname

# Move window (move active window to coordinates)
xdotool getactivewindow windowmove 100 100

# Resize window (resize active window to dimensions)
xdotool getactivewindow windowsize 800 600

# Minimize window (minimize active window)
xdotool getactivewindow windowminimize

# Focus window and wait (find, focus, and synchronize with window)
xdotool search --name "Firefox" windowactivate --sync
```

## Screenshots

<EXTREMELY-IMPORTANT>
### The Iron Law of Visual Verification

Every E2E test MUST include screenshot evidence.

Capture a screenshot after completing a workflow to prove success.
</EXTREMELY-IMPORTANT>

### Wayland: grim + slurp

```bash
# Capture full screen (capture all outputs)
grim /tmp/screenshot.png

# Capture specific output (capture single monitor/output)
grim -o DP-1 /tmp/screen.png

# Capture region interactively (select region with slurp then capture)
grim -g "$(slurp)" /tmp/region.png

# Capture specific region (capture region by coordinates and size)
grim -g "100,200 800x600" /tmp/region.png

# Capture Hyprland window (get window geometry and capture)
hyprctl clients -j | jq '.[] | select(.class=="firefox")'
grim -g "X,Y WxH" /tmp/window.png

# Capture Sway focused window (get focused window geometry and capture)
grim -g "$(swaymsg -t get_tree | jq -r '.. | select(.focused?) | .rect | "\(.x),\(.y) \(.width)x\(.height)"')" /tmp/window.png
```

### X11: scrot / import

```bash
# Capture full screen (screenshot of entire display)
scrot /tmp/screenshot.png

# Capture active window (screenshot of focused window)
scrot -u /tmp/window.png

# Capture interactive selection (select region with mouse then capture)
scrot -s /tmp/selection.png

# Capture with delay (wait before capturing)
scrot -d 3 /tmp/delayed.png

# Capture root window (screenshot using ImageMagick)
import -window root /tmp/screenshot.png

# Capture active window (screenshot of focused window using ImageMagick)
import -window "$(xdotool getactivewindow)" /tmp/window.png
```

### Image Comparison

```bash
# Compare screenshots (count different pixels using ImageMagick)
compare -metric AE baseline.png current.png diff.png

# Threshold comparison (allow 5% fuzz when comparing)
compare -metric AE -fuzz 5% baseline.png current.png diff.png
```

## D-Bus Control

Preferred for apps that expose D-Bus interfaces.

```bash
# List available services (enumerate all D-Bus services)
dbus-send --session --print-reply --dest=org.freedesktop.DBus \
  /org/freedesktop/DBus org.freedesktop.DBus.ListNames

# Open document in Zathura (get PID first, then use org.pwmt.zathura.PID-XXXX)
dbus-send --print-reply --dest=org.pwmt.zathura.PID-12345 \
  /org/pwmt/zathura org.pwmt.zathura.OpenDocument string:"/path/to/file.pdf"

# Go to page in Zathura (navigate to specific page)
dbus-send --print-reply --dest=org.pwmt.zathura.PID-12345 \
  /org/pwmt/zathura org.pwmt.zathura.GotoPage uint32:5

# Open file in GNOME Nautilus (open folder via D-Bus)
dbus-send --session --dest=org.gnome.Nautilus \
  /org/gnome/Nautilus org.freedesktop.Application.Open \
  array:string:"file:///home/user" dict:string:string:""

# Introspect D-Bus service (discover available methods and properties)
dbus-send --session --print-reply --dest=org.example.App \
  /org/example/App org.freedesktop.DBus.Introspectable.Introspect
```

## Accessibility (AT-SPI)

Use AT-SPI for UI element discovery and verification.

```python
#!/usr/bin/env python3
import pyatspi

# Find application (get desktop and search for app by name)
desktop = pyatspi.Registry.getDesktop(0)
for app in desktop:
    if "firefox" in app.name.lower():
        print(f"Found: {app.name}")

        # Traverse accessibility tree (recursively dump accessibility tree)
        def dump_tree(node, indent=0):
            print("  " * indent + f"{node.getRole()}: {node.name}")
            for child in node:
                dump_tree(child, indent + 1)

        dump_tree(app)

# Find specific element (search for button by name in tree)
def find_button(app, name):
    for child in app:
        if child.getRole() == pyatspi.ROLE_PUSH_BUTTON:
            if name.lower() in child.name.lower():
                return child
        found = find_button(child, name)
        if found:
            return found
    return None

# Click button via AT-SPI (trigger button action via accessibility interface)
button = find_button(app, "Submit")
if button:
    button.queryAction().doAction(0)
```

## Complete E2E Examples

<EXTREMELY-IMPORTANT>
### E2E Test Structure

Every Linux E2E test MUST:
1. Detect - Check display server (Wayland vs X11)
2. Launch - Start the application
3. Wait - Allow app to fully initialize
4. Interact - Perform user actions
5. Verify - Check expected state
6. Screenshot - Capture visual evidence
7. Cleanup - Close app, restore state
</EXTREMELY-IMPORTANT>

### Wayland E2E Test

```bash
#!/bin/bash
# test_workflow.sh - Wayland E2E test

set -e  # Exit on error

echo "Starting E2E test..."

# Launch Firefox
firefox &
sleep 3

# Focus address bar and navigate (focus address bar with Ctrl+L)
wtype -M ctrl -k l
sleep 0.2

# Type URL (type example.com URL)
wtype "https://example.com"

# Press Enter (send Return key)
wtype -k Return
sleep 2

# Capture initial screenshot (screenshot before interaction)
grim /tmp/test_before.png

# Move mouse and click (move to element and click)
ydotool mousemove --absolute 500 400
ydotool click 1
sleep 0.5

# Capture final screenshot (screenshot after interaction)
grim /tmp/test_after.png

# Compare screenshots (compare file sizes to detect changes)
SIZE_BEFORE=$(stat -c%s /tmp/test_before.png)
SIZE_AFTER=$(stat -c%s /tmp/test_after.png)

if [ "$SIZE_BEFORE" -ne "$SIZE_AFTER" ]; then
    echo "PASS: Screenshots differ (interaction worked)"
else
    echo "WARN: Screenshots identical"
fi

echo "Test complete"
```

### X11 E2E Test

```bash
#!/bin/bash
# test_workflow_x11.sh - X11 E2E test

set -e

echo "Starting X11 E2E test..."

# Launch gedit (start text editor application)
gedit &
sleep 2

# Focus gedit window (find and focus window by name)
xdotool search --name "gedit" windowactivate --sync

# Type test content (type test text into editor)
xdotool type "Hello, this is an automated test!"
sleep 0.5

# Select all text (select all with Ctrl+A)
xdotool key ctrl+a

# Copy to clipboard (copy selected text with Ctrl+C)
xdotool key ctrl+c

# Verify clipboard content (get clipboard and verify content)
CLIPBOARD=$(xclip -selection clipboard -o)
if [[ "$CLIPBOARD" == *"automated test"* ]]; then
    echo "PASS: Clipboard contains expected text"
else
    echo "FAIL: Clipboard mismatch"
    exit 1
fi

# Capture window screenshot (screenshot of active window)
scrot -u /tmp/test_result.png
echo "Screenshot saved"

# Close without saving (close window with Ctrl+W)
xdotool key ctrl+w
sleep 0.5

# Dismiss save dialog (press Tab and Return to skip save)
xdotool key Tab key Return

echo "Test complete"
```

## Output Requirements

Document every test run in LEARNINGS.md using this template:

```markdown
## Linux E2E Test: [Description]

**Display Server:** Wayland / X11

**Tool:** ydotool / xdotool

**Script:**
```bash
./test_workflow.sh
```

**Output:**
```
Starting E2E test...
PASS: Screenshots differ (interaction worked)
Test complete
```

**Result:** PASS

**Screenshot:** /tmp/test_result.png
```

## Integration

This skill integrates with `dev-test` for Linux desktop automation.

For TDD protocol, see: `Skill(skill="workflows:dev-tdd")`
