---
name: generate-screenshots
description: Generate screenshots for Extension Index submission and documentation
allowed-tools:
  - Bash
  - Read
context: manual
---

# Generate Screenshots Skill

Generate screenshots for Extension Index submission and documentation.

## When to Use

- Preparing for Extension Index submission
- Updating documentation images
- After significant UI changes

## Prerequisites

- 3D Slicer installed
- SLICER_PATH configured in `.env` file
- MouseMaster module available

## Screenshot Requirements

For Extension Index submission, need at minimum:

| Screenshot | Purpose | Required |
|------------|---------|----------|
| `main-ui.png` | Primary submission screenshot | Yes |
| `button-mapping.png` | Detail of mapping interface | Optional |
| `preset-selector.png` | Preset management | Optional |

## Method 1: Fully Automated (Recommended)

Run from terminal - launches Slicer, captures screenshots, exits:

```bash
# First, ensure .env has SLICER_PATH set
cp .env.example .env
# Edit .env to set your Slicer path

# Then run:
./scripts/run_in_slicer.sh scripts/capture_screenshots.py --exit
```

This will:
1. Launch Slicer
2. Load MouseMaster module
3. Capture all screenshots to `Screenshots/`
4. Generate `manifest.json`
5. Exit Slicer
6. Save log to `logs/`

## Method 2: Interactive in Slicer Console

If Slicer is already running, in Python console:

```python
exec(open('/home/ben/projects/slicer-extensions/SlicerMouseMaster/SlicerMouseMaster/scripts/capture_screenshots.py').read())
capture_all_screenshots()
generate_manifest()
```

Or capture individually:

```python
capture_main_ui()          # Main UI (required for submission)
capture_button_mapping()   # Button mapping detail
capture_preset_selector()  # Preset management
```

## Method 3: Manual Capture

If automated capture fails:

1. Open Slicer
2. Navigate to MouseMaster module
3. Set up desired view (select mouse, show bindings)
4. Use OS screenshot tool:
   - Linux: `gnome-screenshot -w` or Print Screen
   - macOS: Cmd+Shift+4
   - Windows: Win+Shift+S
5. Save to `Screenshots/main-ui.png`
6. Crop/resize to ~1200x800 if needed

## Method 3: Slicer Built-in Capture

In Slicer Python console:

```python
import slicer
import qt

# Switch to MouseMaster
slicer.util.selectModule("MouseMaster")

# Capture main window
pixmap = qt.QPixmap.grabWidget(slicer.util.mainWindow())
pixmap.save("/home/ben/projects/slicer-extensions/SlicerMouseMaster/SlicerMouseMaster/Screenshots/main-ui.png")
```

## After Capturing

### Step 1: Verify files exist

```bash
ls Screenshots/*.png
```

### Step 2: Check file sizes (should be >10KB)

```bash
du -h Screenshots/*.png
```

### Step 3: Update CMakeLists.txt

After pushing to GitHub, update screenshot URL:

```cmake
set(EXTENSION_SCREENSHOTURLS "https://raw.githubusercontent.com/benzwick/SlicerMouseMaster/main/SlicerMouseMaster/Screenshots/main-ui.png")
```

### Step 4: Commit screenshots

```bash
git add Screenshots/*.png Screenshots/manifest.json
git commit -m "docs: add screenshots for Extension Index submission"
```

## Verification Checklist

- [ ] `main-ui.png` exists and shows module interface
- [ ] Image is at least 800x600 pixels
- [ ] Image file size is reasonable (50KB - 500KB)
- [ ] No personal data visible in screenshot
- [ ] MouseMaster module is clearly visible
- [ ] UI elements are readable

## Troubleshooting

### Script not found

Ensure path is correct:
```python
import os
os.path.exists('/home/ben/projects/slicer-extensions/SlicerMouseMaster/SlicerMouseMaster/scripts/capture_screenshots.py')
```

### Module not visible

```python
import slicer
slicer.util.selectModule("MouseMaster")
```

### Screenshot is blank/wrong

Try manual capture method instead.

### Permission denied

Check write permissions:
```bash
ls -la Screenshots/
```

## Output

After successful capture:

```
Screenshots/
├── main-ui.png           # Primary screenshot (required)
├── button-mapping.png    # Button mapping detail
├── preset-selector.png   # Preset interface
├── manifest.json         # Screenshot metadata
└── README.md             # Documentation
```

## Integration

This skill is part of the Extension Index submission workflow:

```
1. /generate-screenshots      # This skill
2. /prepare-extension-metadata # Update CMakeLists.txt with URLs
3. /validate-extension-submission
4. /submit-to-extension-index
```
