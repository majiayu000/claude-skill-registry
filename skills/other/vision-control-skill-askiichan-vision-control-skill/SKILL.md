---
name: vision-control-skill
description: Computer vision-based mouse and keyboard control that enables AI to interact with the user's screen through visual understanding. Use this skill when the user requests AI to control their computer, click on screen elements, type text, use keyboard shortcuts, interact with applications visually, or perform mouse/keyboard actions based on what's visible on screen. This skill captures screenshots with grid overlays and determines precise locations for clicking, typing, dragging, scrolling, and keyboard input, allowing AI to simulate real user interactions instead of relying solely on command-line operations.
---

# Vision Control Skill

Control the user's computer through visual understanding with mouse and keyboard simulation.

## Core Workflow

1. **Capture screen with grid overlay** - Take screenshot with coordinate grid
2. **Analyze visual content** - Determine what needs to be clicked
3. **Identify target coordinates** - Find grid cell containing the target
4. **Execute click** - Perform mouse click at the specified location

## Scripts

### capture_grid.py

Captures a screenshot with grid overlay. By default, saves to a temporary file with automatic timestamping. Optionally accepts a custom output path.

```bash
python scripts/capture_grid.py [output_path]
```

Examples:
```bash
python scripts/capture_grid.py                    # Auto-saves to temp directory
python scripts/capture_grid.py screen_grid.png    # Save to specific path
```

Use this to get a visual representation of the screen with coordinate labels.

### click_location.py

Performs mouse clicks at the specified grid coordinate. Supports left-click, right-click, and double-click. Automatically captures a screenshot, performs the action, and cleans up the temporary screenshot file.

```bash
python scripts/click_location.py <grid_command> [--action ACTION] [--keep]
```

Examples:
```bash
python scripts/click_location.py S3                    # Left click
python scripts/click_location.py S3/2 --action right   # Right click at quadrant
python scripts/click_location.py A1 --action double    # Double click
python scripts/click_location.py M5 --keep             # Click and keep screenshot
```

Grid format: `[COLUMN][ROW]` or `[COLUMN][ROW]/[QUADRANT]`
- Columns: A-Z (left to right)
- Rows: 1-15 (top to bottom)
- Quadrants: 1=top-left, 2=top-right, 3=bottom-left, 4=bottom-right

Options:
- `--action click|right|double`: Mouse action type (default: click)
- `--keep`: Preserve the screenshot file instead of auto-deleting (useful for debugging)

### mouse_action.py

Comprehensive mouse control script supporting all mouse actions: click, right-click, double-click, move, drag, and scroll.

```bash
python scripts/mouse_action.py <action> <args...> [--keep]
```

Actions:
- `click <grid>` - Left click at grid location
- `right <grid>` - Right click at grid location
- `double <grid>` - Double click at grid location
- `move <grid>` - Move cursor to grid location (no click)
- `drag <from> <to>` - Drag from one grid to another
- `scroll <grid> <amount>` - Scroll at grid location (positive=up, negative=down)

Examples:
```bash
python scripts/mouse_action.py click S3        # Left click
python scripts/mouse_action.py right S3/2      # Right click at quadrant
python scripts/mouse_action.py double A1       # Double click
python scripts/mouse_action.py move M8         # Move cursor without clicking
python scripts/mouse_action.py drag S3 T5      # Drag from S3 to T5
python scripts/mouse_action.py scroll M8 5     # Scroll up 5 units
python scripts/mouse_action.py scroll M8 -3    # Scroll down 3 units
```

### keyboard_input.py

Comprehensive keyboard control script supporting text typing, key presses, and keyboard shortcuts.

```bash
python scripts/keyboard_input.py <action> <args...>
```

Actions:
- `type <text>` - Type text at current cursor position
- `press <key>` - Press a single key (enter, tab, esc, etc.)
- `hotkey <key1+key2+...>` - Press keyboard shortcut
- `click-type <grid> <text>` - Click at grid location then type text

Examples:
```bash
python scripts/keyboard_input.py type "Hello World"
python scripts/keyboard_input.py press enter
python scripts/keyboard_input.py press tab
python scripts/keyboard_input.py hotkey ctrl+c
python scripts/keyboard_input.py hotkey ctrl+shift+v
python scripts/keyboard_input.py click-type M8 "search query"
```

Common keys: `enter`, `tab`, `esc`, `space`, `backspace`, `delete`, `up`, `down`, `left`, `right`, `home`, `end`, `pageup`, `pagedown`, `f1-f12`

### vision_control_core.py

Core library providing the `VisionControl` class with comprehensive mouse and keyboard control methods:

**Mouse Methods:**
- `click_at_grid(command, button='left', clicks=1)` - Click at grid location
- `right_click_at_grid(command)` - Right click at grid location
- `double_click_at_grid(command)` - Double click at grid location
- `move_to_grid(command, duration=0.5)` - Move cursor to grid location
- `drag_to_grid(from_command, to_command, duration=1.0)` - Drag between locations
- `scroll_at_grid(command, amount)` - Scroll at grid location

**Keyboard Methods:**
- `type_text(text, interval=0.0)` - Type text at current position
- `press_key(key)` - Press a single key
- `press_keys(keys)` - Press keyboard shortcut (hotkey)
- `click_and_type(command, text, interval=0.0)` - Click then type

**Utility Methods:**
- `capture_with_grid(output_path=None, auto_temp=True)` - Capture screenshot with grid
- `cleanup_screenshot()` - Clean up temporary screenshot

Can be imported for custom workflows.

## Typical Usage Patterns

### Basic Click
When a user asks to click something on their screen:

1. Run `capture_grid.py` to get a screenshot with grid overlay (saved to temp directory)
2. Present the image to analyze where the target element is located
3. Identify the grid cell (e.g., "S3") or cell with quadrant (e.g., "S3/2")
4. Run `click_location.py` or `mouse_action.py` with the identified coordinate
5. Confirm the action was successful

### Right-Click Menu
When a user needs to open a context menu:

1. Capture screen with `capture_grid.py`
2. Identify the target location
3. Run `mouse_action.py right <grid>` to right-click

### Drag and Drop
When a user needs to drag something:

1. Capture screen with `capture_grid.py`
2. Identify source and target locations
3. Run `mouse_action.py drag <from> <to>`

### Scrolling
When a user needs to scroll:

1. Capture screen with `capture_grid.py`
2. Identify where to scroll
3. Run `mouse_action.py scroll <grid> <amount>` (positive=up, negative=down)

### Typing Text
When a user needs to type or enter text:

1. For typing at current cursor: Run `keyboard_input.py type "text"`
2. For filling a form field:
   - Capture screen with `capture_grid.py`
   - Identify the input field location
   - Run `keyboard_input.py click-type <grid> "text"`

### Keyboard Shortcuts
When a user needs to use keyboard shortcuts:

1. Run `keyboard_input.py hotkey <keys>` (e.g., `ctrl+c`, `ctrl+v`, `alt+tab`)
2. Common shortcuts: Copy (`ctrl+c`), Paste (`ctrl+v`), Save (`ctrl+s`), Undo (`ctrl+z`)

## Screenshot Management

The skill uses automatic temporary file management:

- **Auto-temp storage**: Screenshots are saved to the system temp directory with timestamps
- **Auto-cleanup**: `click_location.py` automatically deletes screenshots after clicking
- **Privacy-friendly**: No screenshot clutter on disk
- **Debug mode**: Use `--keep` flag to preserve screenshots when troubleshooting

Temp file format: `vision_control_YYYYMMDD_HHMMSS_microseconds.png`

## Reference Documentation

- **Grid System**: See [grid_system.md](references/grid_system.md) for coordinate system and quadrant layout
- **Keyboard Actions**: See [keyboard_actions.md](references/keyboard_actions.md) for comprehensive keyboard reference, key names, and shortcuts

## Dependencies

Required Python packages:
- pyautogui - Mouse control
- mss - Fast screenshot capture
- Pillow (PIL) - Image processing

Install with:
```bash
pip install pyautogui mss Pillow
```

## Supported Actions

### Mouse Actions
- ✅ **Left Click** - Single click with left mouse button
- ✅ **Right Click** - Open context menus
- ✅ **Double Click** - Open files or select text
- ✅ **Move** - Position cursor without clicking
- ✅ **Drag** - Drag and drop between locations
- ✅ **Scroll** - Scroll up or down at a location

### Keyboard Actions
- ✅ **Type Text** - Enter text at cursor position
- ✅ **Press Key** - Press single keys (enter, tab, esc, etc.)
- ✅ **Keyboard Shortcuts** - Execute hotkeys (ctrl+c, alt+tab, etc.)
- ✅ **Click and Type** - Click location then type text

## Safety Considerations

- This skill performs actual mouse actions on the user's system
- Always confirm the target location before performing actions
- Be aware that actions may trigger immediate effects in applications
- Consider asking for user confirmation before critical or destructive actions
- Drag operations may take 1+ seconds to complete
