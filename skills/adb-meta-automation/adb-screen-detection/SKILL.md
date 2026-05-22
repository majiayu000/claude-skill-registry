---
name: adb-screen-detection
description: Screen understanding with OCR and template matching for Android device automation
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 2
category: adb-automation
last_updated: 2025-12-01
compliance_score: 100
dependencies:
  - pytesseract>=0.3.10
  - opencv-python>=4.8.0
  - pillow>=10.0.0
  - numpy>=1.24.0
auto_trigger_keywords:
  - adb-screen
  - ocr
  - template-match
  - element-detection
  - screen-understanding
scripts:
  - name: adb-screen-capture.py
    purpose: Capture Android device screen via ADB screencap
    type: python
    command: uv run .claude/skills/adb-screen-detection/scripts/adb-screen-capture.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-ocr-extract.py
    purpose: Extract text from screen using Tesseract OCR
    type: python
    command: uv run .claude/skills/adb-screen-detection/scripts/adb-ocr-extract.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-find-element.py
    purpose: Find UI element by template matching or OCR text
    type: python
    command: uv run .claude/skills/adb-screen-detection/scripts/adb-find-element.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-tap-coordinate.py
    purpose: Tap device screen at specific coordinates
    type: python
    command: uv run .claude/skills/adb-screen-detection/scripts/adb-tap-coordinate.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

color: blue
---

---

## Quick Reference (30 seconds)

**Screen Understanding for Android Automation**

**What It Does**: Provides OCR-based text detection and template matching to understand Android device screens. Enables reliable UI automation by verifying screen state before and after actions.

**Core Capabilities**:
- 📸 **Screen Capture**: ADB screencap with local storage
- 🔍 **OCR Detection**: Tesseract-based text extraction
- 🎯 **Template Matching**: OpenCV-based element detection
- 👆 **Coordinate Tapping**: ADB input tap with verification

**When to Use**:
- Need to verify UI state before taking actions
- Finding UI elements by text or appearance
- Building reliable automation workflows
- Screen-dependent decision making

---

## Scripts

### 1. adb-screen-capture.py

Capture Android device screen and save locally.

```bash
# Basic usage
uv run .claude/skills/adb-screen-detection/scripts/adb-screen-capture.py

# Specify device
uv run .claude/skills/adb-screen-detection/scripts/adb-screen-capture.py --device 127.0.0.1:5555

# Custom output path
uv run .claude/skills/adb-screen-detection/scripts/adb-screen-capture.py --output /tmp/screen.png

# JSON output
uv run .claude/skills/adb-screen-detection/scripts/adb-screen-capture.py --json
```

**Output**:
```json
{
  "device": "127.0.0.1:5555",
  "timestamp": "2025-12-01T10:30:45Z",
  "local_path": "/tmp/screenshot.png",
  "size": [1080, 2400],
  "success": true
}
```

---

### 2. adb-ocr-extract.py

Extract all visible text from device screen using Tesseract OCR.

```bash
# Basic usage (uses most recent screenshot)
uv run .claude/skills/adb-screen-detection/scripts/adb-ocr-extract.py

# Specify screenshot path
uv run .claude/skills/adb-screen-detection/scripts/adb-ocr-extract.py --image /tmp/screen.png

# Search for specific text
uv run .claude/skills/adb-screen-detection/scripts/adb-ocr-extract.py --search "Login"

# JSON output with coordinates
uv run .claude/skills/adb-screen-detection/scripts/adb-ocr-extract.py --json
```

**Output**:
```json
{
  "text": ["Login", "Username", "Password", "Submit"],
  "detected": true,
  "search_found": true,
  "search_term": "Login",
  "coordinates": {
    "Login": [[100, 200, 150, 230]]
  }
}
```

---

### 3. adb-find-element.py

Find UI element by template matching or OCR text search.

```bash
# Find by OCR text
uv run .claude/skills/adb-screen-detection/scripts/adb-find-element.py \
    --method ocr \
    --target "Login Button" \
    --threshold 0.8

# Find by template image
uv run .claude/skills/adb-screen-detection/scripts/adb-find-element.py \
    --method template \
    --template /path/to/template.png \
    --threshold 0.8

# JSON output
uv run .claude/skills/adb-screen-detection/scripts/adb-find-element.py \
    --method ocr \
    --target "Login" \
    --json
```

**Output**:
```json
{
  "found": true,
  "method": "ocr",
  "target": "Login",
  "coordinates": {
    "x": 100,
    "y": 200,
    "width": 150,
    "height": 30
  },
  "confidence": 0.95,
  "message": "Element found at (100, 200)"
}
```

---

### 4. adb-tap-coordinate.py

Tap device screen at specific coordinates.

```bash
# Tap at coordinates
uv run .claude/skills/adb-screen-detection/scripts/adb-tap-coordinate.py \
    --x 100 \
    --y 200 \
    --device 127.0.0.1:5555

# Tap with verification (check screen after tap)
uv run .claude/skills/adb-screen-detection/scripts/adb-tap-coordinate.py \
    --x 100 \
    --y 200 \
    --verify-text "Next Screen" \
    --timeout 5

# JSON output
uv run .claude/skills/adb-screen-detection/scripts/adb-tap-coordinate.py \
    --x 100 \
    --y 200 \
    --json
```

**Output**:
```json
{
  "device": "127.0.0.1:5555",
  "tap": {
    "x": 100,
    "y": 200
  },
  "success": true,
  "verified": true,
  "verify_text": "Next Screen",
  "verification_match": true
}
```

---

## Usage Patterns

### Pattern 1: Verify Screen State Before Action

```bash
# 1. Capture current screen
adb-screen-capture.py

# 2. Check for expected element
adb-find-element.py --method ocr --target "Login Button"

# 3. If found, tap it
adb-tap-coordinate.py --x 100 --y 200 --verify-text "Welcome"
```

### Pattern 2: OCR-Based Automation

```bash
# 1. Capture screen
adb-screen-capture.py

# 2. Extract all text
adb-ocr-extract.py --search "Settings"

# 3. Get coordinates and tap
adb-find-element.py --method ocr --target "Settings"
adb-tap-coordinate.py --x 150 --y 300
```

### Pattern 3: Template-Based Element Detection

```bash
# 1. Have known UI template images in ./templates/
# 2. Capture screen
adb-screen-capture.py

# 3. Match against templates
adb-find-element.py --method template --template ./templates/button.png

# 4. Tap matched location
adb-tap-coordinate.py --x $(jq -r '.coordinates.x') --y $(jq -r '.coordinates.y')
```

---

## Architecture

**Design Principles**:
- **Independent**: Each script can run standalone
- **Chainable**: Scripts output JSON for piping
- **Stateless**: No dependencies between executions
- **Verifiable**: Always verify screen state before proceeding
- **Timeout Protected**: All network operations have timeouts

**Dependency Relationship**:
```
adb-screen-capture.py (foundation)
    ↓
adb-ocr-extract.py (uses capture)
adb-find-element.py (uses capture or templates)
    ↓
adb-tap-coordinate.py (uses find-element for verification)
```

---

## Integration Points

**Used By**:
- `adb-navigation-base` - Wait for elements between actions
- `adb-magisk` - Verify Magisk UI state
- `adb-karrot` - Verify app state during automation
- `adb-workflow-orchestrator` - Screen verification in workflows

**Dependencies**:
- System: `adb` command-line tool
- Python: pytesseract, opencv-python, pillow, numpy

---

## Troubleshooting

### OCR Not Working
- Install Tesseract: `brew install tesseract` (macOS) or `apt-get install tesseract-ocr` (Linux)
- Set TESSDATA_PREFIX: `export TESSDATA_PREFIX=/usr/local/share/tessdata`

### Template Matching Too Strict/Loose
- Adjust `--threshold` parameter (0.0-1.0)
- Higher threshold = stricter matching
- Recommended: 0.8-0.9 for reliable detection

### Device Offline
- Check ADB connection: `adb devices`
- Reconnect: `adb connect <device>`
- Restart ADB: `adb kill-server && adb start-server`

---

## Workflows

This skill includes TOON-based workflow definitions for automation.

### What is TOON?
TOON (Task-Oriented Orchestration Notation) is a structured workflow definition language that pairs with Markdown documentation. Each workflow consists of:
- **[name].toon** - Orchestration logic and execution steps
- **[name].md** - Complete documentation and usage guide

This TOON+MD pairing approach is inspired by the BMAD METHOD pattern, adapted to use TOON instead of YAML for better orchestration support.

### Available Workflows

Workflow files are located in `workflow/` directory:

**Example Workflows (adb-screen-detection):**
- `workflow/screen-verification.toon` - Capture and verify screen state
- `workflow/element-detection.toon` - Find elements via OCR or template matching
- `workflow/screen-monitoring.toon` - Continuous screen monitoring and analysis

### Running a Workflow

Execute any workflow using the ADB workflow orchestrator:

```bash
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
  --workflow .claude/skills/adb-screen-detection/workflow/screen-verification.toon \
  --param device="127.0.0.1:5555"
```

### Workflow Documentation

Each workflow includes comprehensive documentation in the corresponding `.md` file:
- Purpose and use case
- Prerequisites and requirements
- Available parameters
- Execution phases and steps
- Success criteria
- Error handling and recovery
- Example commands

See the `workflow/` directory for complete TOON file definitions and documentation.

### Creating New Workflows

To create custom workflows for this skill:
1. Create a new `.toon` file in the `workflow/` directory
2. Define phases, steps, and parameters using TOON v4.0 syntax
3. Create corresponding `.md` file with comprehensive documentation
4. Test with the workflow orchestrator

For more information, refer to the TOON specification and the workflow orchestrator documentation.

---

**Version**: 1.0.0
**Status**: ✅ Foundation Tier
**Scripts**: 4 (all MCP-ready)
**Last Updated**: 2025-12-01
**Tier**: 2 (Foundation)

