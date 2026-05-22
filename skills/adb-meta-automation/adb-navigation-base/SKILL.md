---
name: adb-navigation-base
description: Base navigation patterns for Android device automation - gestures, waits, and UI interaction
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 2
category: adb-automation
last_updated: 2025-12-01
compliance_score: 100
dependencies:
  - pytesseract>=0.3.10
  - pillow>=10.0.0
  - numpy>=1.24.0
auto_trigger_keywords:
  - adb-navigation
  - gesture
  - swipe
  - wait-for
  - ui-interaction
scripts:
  - name: adb-tap.py
    purpose: Smart tap with retry logic and verification
    type: python
    command: uv run .claude/skills/adb-navigation-base/scripts/adb-tap.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-swipe.py
    purpose: Perform swipe gesture on device screen
    type: python
    command: uv run .claude/skills/adb-navigation-base/scripts/adb-swipe.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-wait-for.py
    purpose: Wait for element or text to appear with timeout
    type: python
    command: uv run .claude/skills/adb-navigation-base/scripts/adb-wait-for.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

color: cyan
---

---

## Quick Reference (30 seconds)

**Base Navigation Patterns for Android Automation**

**What It Does**: Provides fundamental gesture and wait-for patterns used in all UI automation. Smart retry logic, verification, and timeout handling.

**Core Capabilities**:
- 👆 **Smart Tap**: Retry-enabled tapping with verification
- 👉 **Swipe Gesture**: Directional swiping for scrolling
- ⏱️ **Wait For**: Element/text waiting with polling

**When to Use**:
- Building reliable automation workflows
- Handling timing-sensitive UI transitions
- Creating reusable navigation patterns
- Combining with adb-screen-detection for full automation

---

## Scripts

### 1. adb-tap.py

Smart tap action with automatic retry logic.

```bash
# Basic tap
uv run .claude/skills/adb-navigation-base/scripts/adb-tap.py --x 100 --y 200

# Tap with retry (auto-retry on failure)
uv run .claude/skills/adb-navigation-base/scripts/adb-tap.py --x 100 --y 200 --retry 3

# Tap with verification
uv run .claude/skills/adb-navigation-base/scripts/adb-tap.py --x 100 --y 200 --verify-text "Next"

# Tap with both
uv run .claude/skills/adb-navigation-base/scripts/adb-tap.py \
    --x 100 --y 200 --retry 3 --verify-text "Loaded" --timeout 5
```

**Features**:
- Automatic retry on failure (configurable attempts)
- Post-tap screen verification
- Timeout protection
- Detailed logging

---

### 2. adb-swipe.py

Perform directional swipe gesture.

```bash
# Swipe up (scroll down content)
uv run .claude/skills/adb-navigation-base/scripts/adb-swipe.py --direction up --distance 300

# Swipe left (next page)
uv run .claude/skills/adb-navigation-base/scripts/adb-swipe.py --direction left --distance 500

# Swipe with verification
uv run .claude/skills/adb-navigation-base/scripts/adb-swipe.py \
    --direction down --distance 400 --verify-text "End of List"

# Custom start position
uv run .claude/skills/adb-navigation-base/scripts/adb-swipe.py \
    --direction up --distance 300 --start-x 500 --start-y 1000
```

**Directions**: up, down, left, right
**Features**:
- 4-direction swiping
- Configurable distance (pixels)
- Custom start position
- Post-swipe verification
- Momentum-aware (handles scroll inertia)

---

### 3. adb-wait-for.py

Wait for UI element or text to appear.

```bash
# Wait for text (default 10s timeout)
uv run .claude/skills/adb-navigation-base/scripts/adb-wait-for.py \
    --method text --target "Loaded"

# Wait for element by text with timeout
uv run .claude/skills/adb-navigation-base/scripts/adb-wait-for.py \
    --method text --target "Login" --timeout 5

# Wait with polling interval
uv run .claude/skills/adb-navigation-base/scripts/adb-wait-for.py \
    --method text --target "Results" --interval 0.5

# JSON output for scripting
uv run .claude/skills/adb-navigation-base/scripts/adb-wait-for.py \
    --method text --target "Ready" --json
```

**Detection Methods**: text (OCR-based)
**Features**:
- Configurable timeout (1-60s)
- Polling interval configuration
- Timeout exception handling
- Success/failure reporting
- Return element coordinates when found

---

## Usage Patterns

### Pattern 1: Basic Navigation Sequence

```bash
# 1. Tap login button
adb-tap.py --x 100 --y 200

# 2. Wait for login form
adb-wait-for.py --method text --target "Username" --timeout 5

# 3. Swipe down to see password field
adb-swipe.py --direction down --distance 200

# 4. Tap password field
adb-tap.py --x 100 --y 300
```

### Pattern 2: Reliable Action with Retry

```bash
# Tap with automatic retry (up to 3 times)
adb-tap.py --x 100 --y 200 --retry 3 --verify-text "Next Screen"
```

### Pattern 3: Scroll and Find

```bash
# 1. Start at top
# 2. Swipe up (scroll down) multiple times looking for element
for i in {1..5}; do
  adb-swipe.py --direction up --distance 300
  # Check if element appears
  if adb-wait-for.py --method text --target "Find Me" --timeout 1; then
    # Found! Tap it
    adb-tap.py --x 150 --y 400
    break
  fi
done
```

---

## Architecture

**Design Principles**:
- **Composable**: Chain together for complex workflows
- **Fault-Tolerant**: Automatic retry and timeout protection
- **Verifiable**: All actions can have post-action verification
- **Observable**: Detailed logging of all operations
- **Stateless**: No dependency on previous state

**Dependency Relationship**:
```
adb-screen-detection/ (provides capture, OCR, find-element)
         ↓
adb-navigation-base/ (uses for wait-for and verification)
         ↓
adb-workflow-orchestrator/ (coordinates these patterns)
```

---

## Integration Points

**Used By**:
- `adb-workflow-orchestrator` - Workflow step execution
- `adb-magisk` - Magisk Manager navigation
- `adb-karrot` - Karrot app automation

**Dependency On**:
- `adb-screen-detection` - Screen capture and OCR
- System: `adb` command-line tool

---

## Error Handling

### Retry Logic

```
Attempt 1: Try action
  ├─ Success → Return
  └─ Failure → Wait, Try again

Attempt 2: Try action
  ├─ Success → Return
  └─ Failure → Wait, Try again

Attempt 3: Try action
  ├─ Success → Return
  └─ Failure → Return error
```

### Timeout Handling

- Polls every N seconds (configurable)
- Returns TIMEOUT error if deadline exceeded
- Allows caller to handle timeout gracefully

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

**Example Workflows (adb-navigation-base):**
- `workflow/tap-and-wait.toon` - Tap element and wait for result
- `workflow/scroll-and-find.toon` - Scroll to find element
- `workflow/gesture-sequence.toon` - Complex gesture combinations

### Running a Workflow

Execute any workflow using the ADB workflow orchestrator:

```bash
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
  --workflow .claude/skills/adb-navigation-base/workflow/tap-and-wait.toon \
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
**Scripts**: 3
**Last Updated**: 2025-12-01
**Tier**: 2 (Foundation)

