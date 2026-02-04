---
name: hecras_explore_gui
description: |
  Explores the HEC-RAS GUI to document menus, dialogs, controls, and workflows
  using win32com automation with screenshot capture. Use when needing to discover
  menu structure, document dialog controls, capture screenshots for documentation,
  or explore unfamiliar GUI elements in HEC-RAS.

  Triggers: explore GUI, screenshot, capture dialog, document menu, HEC-RAS interface,
  discover controls, GUI automation, menu exploration, dialog documentation, visual documentation.
---

# Exploring HEC-RAS GUI

This skill enables agents to explore the HEC-RAS graphical interface, capture screenshots, and document menus/dialogs for automation development and documentation.

## Prerequisites

**Required Python packages**:
```bash
pip install pywin32 Pillow
```

**Required conditions**:
1. HEC-RAS must be installed
2. Running on Windows (win32 APIs required)
3. A HEC-RAS project must be available to open

## Core Capabilities

### 1. RasScreenshot Module

The `RasScreenshot` class provides window-specific screenshot capture:

```python
from ras_commander import RasScreenshot, RasGuiAutomation

# Core screenshot methods
RasScreenshot.capture_window(hwnd)                     # Capture by window handle
RasScreenshot.capture_hecras_main(pid)                 # Capture main HEC-RAS window
RasScreenshot.capture_dialog(title_pattern)            # Capture dialog by title
RasScreenshot.capture_all_ras_windows(pid)             # Capture all windows
RasScreenshot.capture_foreground()                     # Capture active window
RasScreenshot.capture_with_delay(hwnd, delay=1.0)      # Capture after delay
RasScreenshot.capture_menu_exploration(hwnd, menu_id)  # Click menu and capture result
RasScreenshot.document_dialog(hwnd)                    # Document dialog controls
```

### 2. RasGuiAutomation Integration

Use `RasGuiAutomation` for window discovery and menu operations:

```python
from ras_commander import RasGuiAutomation

# Window discovery
windows = RasGuiAutomation.get_windows_by_pid(pid)
hwnd, title = RasGuiAutomation.find_main_hecras_window(windows)

# Menu enumeration
menus = RasGuiAutomation.enumerate_all_menus(hwnd)

# Menu interaction
success = RasGuiAutomation.click_menu_item(hwnd, menu_id)

# Dialog discovery
dialog_hwnd = RasGuiAutomation.find_dialog_by_title("Unsteady Flow")
button_hwnd = RasGuiAutomation.find_button_by_text(dialog_hwnd, "Compute")
```

## Exploration Workflows

### Workflow 1: Launch HEC-RAS and Capture Main Window

```python
import subprocess
import time
from pathlib import Path
from ras_commander import RasScreenshot, RasGuiAutomation

# Configuration
ras_exe = Path(r"C:\Program Files\HEC\HEC-RAS\6.6\Ras.exe")
project_file = Path(r"C:\Models\MyProject\MyProject.prj")

# Launch HEC-RAS
process = subprocess.Popen([str(ras_exe), str(project_file)])
pid = process.pid
print(f"Launched HEC-RAS with PID: {pid}")

# Wait for window to appear
time.sleep(8)

# Find main window
windows = RasGuiAutomation.get_windows_by_pid(pid)
hwnd, title = RasGuiAutomation.find_main_hecras_window(windows)
print(f"Main window: {title} (HWND: {hwnd})")

# Capture screenshot
screenshot = RasScreenshot.capture_hecras_main(pid)
print(f"Screenshot saved: {screenshot}")

# Agent can view the screenshot with Read tool
# Read(file_path=str(screenshot))
```

### Workflow 2: Explore Menu Structure

```python
import time
from ras_commander import RasScreenshot, RasGuiAutomation

# Assuming HEC-RAS is already running with known hwnd
hwnd = ...  # From previous discovery

# Enumerate all menus
menus = RasGuiAutomation.enumerate_all_menus(hwnd)

print("Menu Structure:")
for menu in menus:
    print(f"  [{menu['menu_id']:4d}] {menu['menu_path']}")

# Common HEC-RAS menu IDs (from exploration):
# File menu items: 32872 (New Project), 41, 42 (Open), 45 (Save)
# Edit menu items: 40001 (Undo), 40002 (Cut), 40003 (Copy)
# Run menu items: 47 (Unsteady Flow Analysis), 46 (Steady Flow Analysis)
# View menu items: 49 (RAS Mapper)
```

### Workflow 3: Click Menu and Document Dialog

```python
import time
from ras_commander import RasScreenshot, RasGuiAutomation

# Click "Unsteady Flow Analysis" menu (ID typically 47)
UNSTEADY_FLOW_MENU_ID = 47

# Capture before and after
success, before_ss, after_ss = RasScreenshot.capture_menu_exploration(
    hwnd=hwnd,
    menu_id=UNSTEADY_FLOW_MENU_ID,
    delay_after_click=2.0
)

if success:
    print(f"Before screenshot: {before_ss}")
    print(f"After screenshot: {after_ss}")

    # Find the dialog that appeared
    dialog_hwnd = RasGuiAutomation.find_dialog_by_title("Unsteady Flow Analysis")

    if dialog_hwnd:
        # Document all controls in the dialog
        doc = RasScreenshot.document_dialog(dialog_hwnd)

        print(f"\nDialog: {doc['window_title']}")
        print(f"Controls found: {len(doc['controls'])}")

        for ctrl in doc['controls']:
            if ctrl['visible'] and ctrl['text']:
                print(f"  [{ctrl['class']:15s}] ID={ctrl['control_id']:5d}: {ctrl['text']}")
```

### Workflow 4: Systematic Menu Crawl

```python
import time
from pathlib import Path
from ras_commander import RasScreenshot, RasGuiAutomation

def explore_menu_item(hwnd, menu_id, menu_name, output_folder):
    """Explore a single menu item: click, screenshot, document, close."""
    print(f"\nExploring: {menu_name} (ID: {menu_id})")

    # Capture before state
    before_path = RasScreenshot.capture_window(hwnd)

    # Click menu
    success = RasGuiAutomation.click_menu_item(hwnd, menu_id)
    if not success:
        print(f"  Failed to click menu {menu_id}")
        return None

    time.sleep(1.5)  # Wait for dialog

    # Find new foreground window
    import win32gui
    fg_hwnd = win32gui.GetForegroundWindow()

    if fg_hwnd != hwnd:
        # New dialog appeared
        dialog_title = win32gui.GetWindowText(fg_hwnd)
        print(f"  Dialog opened: {dialog_title}")

        # Document the dialog
        doc = RasScreenshot.document_dialog(fg_hwnd)

        # Save documentation to file
        doc_path = output_folder / f"{menu_name.replace(' ', '_')}_controls.txt"
        with open(doc_path, 'w') as f:
            f.write(f"Dialog: {doc['window_title']}\n")
            f.write(f"Class: {doc['window_class']}\n")
            f.write(f"Screenshot: {doc['screenshot']}\n\n")
            f.write("Controls:\n")
            for ctrl in doc['controls']:
                if ctrl['visible']:
                    f.write(f"  [{ctrl['class']:15s}] ID={ctrl['control_id']:5d}: {ctrl['text']}\n")

        print(f"  Documentation saved: {doc_path}")

        # Close dialog (ESC or Cancel button)
        cancel_btn = RasGuiAutomation.find_button_by_text(fg_hwnd, "Cancel")
        if cancel_btn:
            import win32api
            import win32con
            win32api.PostMessage(cancel_btn, win32con.BM_CLICK, 0, 0)
        else:
            # Send ESC key
            win32api.PostMessage(fg_hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)

        time.sleep(0.5)
        return doc

    return None

# Example: Explore common menus
output_folder = Path(".claude/outputs/win32com-automation-expert/gui_exploration")
output_folder.mkdir(parents=True, exist_ok=True)

menus_to_explore = [
    (47, "Unsteady_Flow_Analysis"),
    (46, "Steady_Flow_Analysis"),
    (49, "RAS_Mapper"),
    # Add more menu IDs as discovered
]

for menu_id, menu_name in menus_to_explore:
    doc = explore_menu_item(hwnd, menu_id, menu_name, output_folder)
```

### Workflow 5: Agent-Driven Interactive Exploration

When an agent needs to explore unfamiliar parts of the HEC-RAS interface:

```python
# Agent exploration session template
import time
from ras_commander import RasScreenshot, RasGuiAutomation, RasExamples, init_ras_project
import subprocess

# 1. Extract and open a test project
project_folder = RasExamples.extract_project("Muncie", suffix="gui_explore")
init_ras_project(project_folder, "6.6")

# Get project file path
from ras_commander import ras
prj_file = ras.prj_file

# 2. Launch HEC-RAS
ras_exe = ras.ras_exe_path
process = subprocess.Popen([str(ras_exe), str(prj_file)])
time.sleep(10)

# 3. Initial discovery
windows = RasGuiAutomation.get_windows_by_pid(process.pid)
hwnd, title = RasGuiAutomation.find_main_hecras_window(windows)

# 4. Capture initial state
screenshot = RasScreenshot.capture_hecras_main(process.pid)
# Read(file_path=str(screenshot))  # Agent views this

# 5. Enumerate menus for reference
menus = RasGuiAutomation.enumerate_all_menus(hwnd)
# Agent can now decide which menus to explore based on menu structure

# 6. Interactive exploration loop
# Agent decides menu_id to click based on goals
# menu_id = <agent decides based on menu structure>
# success, before, after = RasScreenshot.capture_menu_exploration(hwnd, menu_id)
# Read(file_path=str(after))  # Agent views result

# 7. Close HEC-RAS when done
process.terminate()
```

## Output Location

Screenshots are saved to:
```
.claude/outputs/win32com-automation-expert/screenshots/
```

This folder is gitignored, keeping the repository clean.

**Naming convention**:
```
YYYYMMDD_HHMMSS_fff_<window_title>.png
```

Example: `20251221_143025_123_Unsteady_Flow_Analysis.png`

## Agent Viewing Screenshots

The agent can "see" captured screenshots using Claude's multimodal capability:

```python
# After capturing
screenshot_path = RasScreenshot.capture_dialog("Unsteady Flow Analysis")

# Agent views with Read tool (automatically interprets as image)
# Read(file_path=str(screenshot_path))
```

## Listing Previous Screenshots

```python
# List all captured screenshots
screenshots = RasScreenshot.list_screenshots()

print(f"Found {len(screenshots)} screenshots:")
for path in screenshots[:10]:  # Show 10 most recent
    print(f"  {path.name}")

# View a specific screenshot
# Read(file_path=str(screenshots[0]))
```

## Known Menu IDs (HEC-RAS 6.6)

Based on exploration, common HEC-RAS menu IDs include:

### Main Window Menus

| Menu Item | ID | Notes |
|-----------|-----|-------|
| Geometric Data (Edit menu) | 37 | Opens Geometry Editor |
| Steady Flow Analysis | 46 | Opens Steady Flow dialog |
| Unsteady Flow Analysis | 47 | Opens Unsteady Flow dialog |
| Quasi-Unsteady (Sediment) | 48 | Sediment transport |
| RAS Mapper | 49 | Opens RAS Mapper window |

### Unsteady Flow Analysis → Options Menu

| Menu Item | ID | Notes |
|-----------|-----|-------|
| Stage and Flow Output Locations | 13 | Output configuration |
| Dam (Inline Structure) Breach | 23 | Inline breach parameters |
| Levee (Lateral Structure) Breach | 24 | Lateral breach parameters |
| **SA Connection Breach** | **25** | **Storage Area breach params** |
| Computation Options and Tolerances | 27 | Solver settings |
| Output Options | 29 | Output configuration |

### Navigation Path: Breach Parameters

```
Run > Unsteady Flow Analysis (ID: 47)
  > Options menu > SA Connection Breach (ID: 25)
    → Opens "Storage Area Connection Breach Data" dialog
```

**Note**: Menu IDs may vary between HEC-RAS versions. Always enumerate menus first.

## Error Handling

```python
from ras_commander import RasScreenshot

# Check dependencies before operations
if not hasattr(RasScreenshot, '_check_dependencies'):
    print("RasScreenshot module not available")
else:
    available, msg = RasScreenshot._check_dependencies()
    if not available:
        print(f"Missing dependency: {msg}")
```

## Tips for Effective Exploration

1. **Handle "already running" dialog**: Call `RasGuiAutomation.handle_already_running_dialog()` 3 seconds after launch
2. **Use retry loop for window discovery**: HEC-RAS takes 15-30s to start; poll every 2s
3. **Wait after menu clicks**: Dialogs take time to render (1-2 seconds)
4. **Match menu items precisely**: "Quasi-Unsteady" contains "Unsteady" - use exact match
5. **Bring window to foreground**: Call `SetForegroundWindow()` before clicking
6. **Check foreground window**: After menu click, check if new window appeared
7. **Document controls first**: Before interacting with a dialog
8. **Close dialogs cleanly**: Use Cancel button or ESC key
9. **Custom toolbar buttons**: HEC-RAS uses owner-drawn controls - may need position-based clicking

## Primary Sources

- **RasScreenshot module**: `ras_commander/RasScreenshot.py`
- **RasGuiAutomation module**: `ras_commander/RasGuiAutomation.py`
- **Win32 automation notebook**: `examples/120_automating_ras_with_win32com.ipynb`
- **Win32com automation agent**: `.claude/agents/win32com-automation-expert.md`

## Related Skills

- `hecras_compute_plans` - After documenting GUI, automate plan execution
- `win32com-automation-expert` - Agent for developing GUI automation workflows

---

**Remember**: This skill enables GUI exploration for documentation and automation development. For production automation workflows, use the deterministic functions in `RasGuiAutomation` that were developed from exploration findings.
