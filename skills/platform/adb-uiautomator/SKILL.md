---
name: adb-uiautomator
description: Semantic UI element detection via uiautomator2
version: 1.0.0
modularized: True
scripts_enabled: True
tier: 3
category: adb-app-automation
last_updated: 2025-12-02
compliance_score: 100
dependencies:
  - adb-screen-detection
  - adb-navigation-base
  - adb-workflow-orchestrator
auto_trigger_keywords:
  - uiautomator
  - automation
  - testing
  - check
scripts:
  - name: adb-uiautomator-launch.py
    purpose: Uiautomator Launch automation
    type: python
    command: uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-launch.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-02
  - name: adb-uiautomator-check.py
    purpose: Uiautomator Check automation
    type: python
    command: uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-check.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02
  - name: adb-uiautomator-test.py
    purpose: Uiautomator Test automation
    type: python
    command: uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-test.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02
color: cyan
---

---

## Quick Reference (30 seconds)

**Semantic UI element detection via uiautomator2**

**What It Does**: Automates interactions and testing for the target app.

**Core Capabilities**:
- 🚀 **App Control**: Launch and interact with app
- 🔍 **Detection**: Monitor app behavior
- ✅ **Validation**: Verify functionality

**When to Use**:
- Testing app on various devices
- Automating app interactions
- Validating app functionality

---

## Scripts

### adb-uiautomator-launch.py

Uiautomator Launch automation.

```bash
# Basic usage
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-launch.py

# With device specification
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-launch.py \
    --device 127.0.0.1:5555

# JSON output
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-launch.py --json
```

---

### adb-uiautomator-check.py

Uiautomator Check automation.

```bash
# Basic usage
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-check.py

# With device specification
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-check.py \
    --device 127.0.0.1:5555

# JSON output
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-check.py --json
```

---

### adb-uiautomator-test.py

Uiautomator Test automation.

```bash
# Basic usage
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-test.py

# With device specification
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-test.py \
    --device 127.0.0.1:5555

# JSON output
uv run .claude/skills/adb-uiautomator/scripts/adb-uiautomator-test.py --json
```

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

**Example Workflows (adb-uiautomator):**
- `workflow/app-launch.toon` - Launch app with uiautomator2 verification
- `workflow/element-check.toon` - Find and verify UI elements
- `workflow/functional-test.toon` - Complete app functionality testing

### Running a Workflow

Execute any workflow using the ADB workflow orchestrator:

```bash
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
  --workflow .claude/skills/adb-uiautomator/workflow/app-launch.toon \
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
