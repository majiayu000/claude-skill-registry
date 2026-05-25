---
name: adb-workflow-orchestrator
description: TOON workflow orchestration engine for coordinating ADB automation scripts across phases with error recovery
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 2
category: adb-automation
last_updated: 2025-12-01
compliance_score: 100
dependencies:
  - click>=8.1.7
  - pyyaml>=6.0
  - python-dateutil>=2.8.0
auto_trigger_keywords:
  - adb-workflow
  - toon
  - orchestration
  - workflow-executor
  - phase-coordination
scripts:
  - name: adb-run-workflow.py
    purpose: Execute TOON YAML workflow with phase-based coordination
    type: python
    command: uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

color: magenta
---

---

## Quick Reference (30 seconds)

**Workflow Orchestration for ADB Automation**

**What It Does**: Parses and executes TOON YAML workflow files that coordinate multiple ADB scripts across phases with error recovery, verification, and state management.

**Core Capabilities**:
- 🔄 **Phase-Based Execution**: Multi-stage workflows
- 🔀 **Parameter Templating**: {{ variable }} substitution
- ✅ **Verification Steps**: Validate state after each action
- 🔁 **Error Recovery**: Retry with fallback logic
- 📊 **State Tracking**: Progress through phases
- ⏱️ **Timeout Management**: Per-action timeout control

**When to Use**:
- Running complex multi-step automation sequences
- Coordinating multiple scripts with dependencies
- Need error recovery and retry logic
- Building reusable workflow definitions

---

## TOON Workflow Format

### Basic Structure

```yaml
name: Workflow Name
description: What this workflow does
version: 1.0.0

parameters:
  device_id: "127.0.0.1:5555"
  timeout: 10

phases:
  - id: phase1_setup
    name: "Setup Phase"
    steps:
      - id: step1
        action: adb-tap
        params:
          x: 100
          y: 200
          device: "{{ device_id }}"
      - id: step2
        action: adb-wait-for
        params:
          method: text
          target: "Loaded"
          timeout: "{{ timeout }}"

recovery:
  - on_error: phase1_setup
    action: retry
    max_attempts: 3
  - on_error: step1
    action: adb-screen-capture
    then: continue
```

### Parameter Templating

```yaml
parameters:
  device: "127.0.0.1:5555"
  search_text: "Login"
  timeout: 10

steps:
  - action: adb-find-element
    params:
      method: ocr
      target: "{{ search_text }}"
      device: "{{ device }}"
      timeout: "{{ timeout }}"
```

### Phase-Based Organization

```yaml
phases:
  - id: phase1_init
    name: "Initialization"
    steps:
      # Steps execute sequentially
      - id: capture
        action: adb-screen-capture

  - id: phase2_interact
    name: "User Interaction"
    steps:
      # Each phase waits for previous to complete
      - id: tap_button
        action: adb-tap
        params:
          x: 100
          y: 200

  - id: phase3_verify
    name: "Verification"
    steps:
      - id: check_result
        action: adb-wait-for
        params:
          method: text
          target: "Success"
```

### Error Recovery

```yaml
recovery:
  # Retry on phase error
  - on_error: phase2_interact
    action: retry
    max_attempts: 3
    delay: 1

  # Fallback action
  - on_error: step_tap
    action: adb-swipe
    params:
      direction: up
      distance: 300
    then: retry

  # Custom recovery script
  - on_error: phase3_verify
    action: adb-screenshot-capture  # Run script
    then: continue
```

---

## Scripts

### adb-run-workflow.py

Execute TOON YAML workflow file.

```bash
# Basic execution
uv run adb-run-workflow.py --workflow magisk-setup.toon

# With parameters override
uv run adb-run-workflow.py --workflow magisk-setup.toon \
    --param device_id=192.168.1.100:5555 \
    --param timeout=15

# Dry run (show what would execute)
uv run adb-run-workflow.py --workflow magisk-setup.toon --dry-run

# With detailed logging
uv run adb-run-workflow.py --workflow magisk-setup.toon --verbose

# JSON output for integration
uv run adb-run-workflow.py --workflow magisk-setup.toon --json
```

**Output**:
```
✅ Workflow: Magisk Setup
   Phase 1: Initialization
     ├─ Step 1: capture       [✅ Success]
     ├─ Step 2: verify       [✅ Success]

   Phase 2: User Interaction
     ├─ Step 1: tap_button   [✅ Success - attempt 1/3]
     ├─ Step 2: wait_load    [✅ Success]

   Phase 3: Verification
     ├─ Step 1: check_result [✅ Success]

✅ Workflow completed successfully in 23.5s
```

---

## Usage Patterns

### Pattern 1: Simple Sequential Workflow

```yaml
name: Simple Login
phases:
  - id: login
    steps:
      - id: tap_username
        action: adb-tap
        params: {x: 100, y: 200}

      - id: wait_password_field
        action: adb-wait-for
        params: {method: text, target: "Password"}

      - id: tap_password
        action: adb-tap
        params: {x: 100, y: 300}
```

### Pattern 2: Error Recovery with Retry

```yaml
name: Resilient Login
parameters:
  max_attempts: 3

phases:
  - id: attempt_login
    steps:
      - id: tap_login
        action: adb-tap
        params: {x: 100, y: 200}

recovery:
  - on_error: attempt_login
    action: retry
    max_attempts: "{{ max_attempts }}"
    delay: 2
```

### Pattern 3: Fallback Action

```yaml
name: Scroll and Find
phases:
  - id: find_element
    steps:
      - id: wait_element
        action: adb-wait-for
        params: {method: text, target: "Target", timeout: 3}

recovery:
  - on_error: wait_element
    action: adb-swipe
    params: {direction: up, distance: 300}
    then: retry
```

### Pattern 4: Multi-Phase Coordination

```yaml
name: Complex Workflow
phases:
  - id: phase1_setup
    name: "Setup"
    steps:
      - id: init
        action: adb-screenshot-capture

  - id: phase2_interact
    name: "Interaction"
    steps:
      - id: tap
        action: adb-tap
        params: {x: 100, y: 200}

  - id: phase3_verify
    name: "Verification"
    steps:
      - id: verify
        action: adb-wait-for
        params: {method: text, target: "Done"}
```

---

## Architecture

**Design Principles**:
- **Declarative**: Workflows defined as YAML, not code
- **Composable**: Reuse workflows via parameters
- **Resilient**: Built-in error recovery and retry
- **Observable**: Detailed logging and state tracking
- **Extensible**: Easy to add new action types

**Execution Flow**:
```
Load YAML → Validate → Parse Parameters → Execute Phases
                                              ↓
                                        Execute Steps
                                              ↓
                                        Verify Results
                                              ↓
                                        Handle Errors
                                              ↓
                                        Report Status
```

**State Machine**:
```
IDLE → VALIDATING → EXECUTING → VERIFYING → COMPLETE
  ↑                      ↓
  └──────← ERROR RECOVERY ←──────┘
```

---

## Integration Points

**Calls**:
- `adb-screen-detection` (capture, find-element)
- `adb-navigation-base` (tap, swipe, wait-for)
- Any `adb-*` script via command name

**Used By**:
- `adb-magisk` (magisk-setup.toon, install-module.toon)
- `adb-karrot` (karrot-bypass-playintegrity.toon)
- Custom workflows

---

## Example Workflows

### Magisk Module Installation Workflow

```yaml
name: Install Magisk Module
version: 1.0.0

parameters:
  device: "127.0.0.1:5555"
  module_path: "/sdcard/PlayIntegrityFork.zip"

phases:
  - id: phase1_launch
    name: "Launch Magisk Manager"
    steps:
      - id: launch
        action: adb-magisk-launch
        params: {device: "{{ device }}"}

  - id: phase2_navigate
    name: "Navigate to Modules"
    steps:
      - id: wait_home
        action: adb-wait-for
        params: {method: text, target: "Modules", timeout: 5}
      - id: tap_modules
        action: adb-tap
        params: {x: 100, y: 200, device: "{{ device }}"}

  - id: phase3_install
    name: "Install Module"
    steps:
      - id: tap_fab
        action: adb-tap
        params: {x: 400, y: 800, device: "{{ device }}"}
      - id: select_file
        action: adb-file-select
        params: {path: "{{ module_path }}"}
      - id: wait_complete
        action: adb-wait-for
        params: {method: text, target: "Installation complete", timeout: 10}

recovery:
  - on_error: phase2_navigate
    action: retry
    max_attempts: 2
  - on_error: phase3_install
    action: adb-screenshot-capture
    then: continue
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

**Example Workflows (adb-workflow-orchestrator):**
- `workflow/phase-execution.toon` - Multi-phase workflow coordination
- `workflow/error-recovery.toon` - Error handling and recovery patterns
- `workflow/parameter-templating.toon` - Parameter substitution examples

### Running a Workflow

Execute any workflow using the ADB workflow orchestrator:

```bash
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
  --workflow .claude/skills/adb-workflow-orchestrator/workflow/phase-execution.toon \
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
**Status**: ✅ Orchestration Layer
**Scripts**: 1 main + 2 lib modules
**Last Updated**: 2025-12-01
**Tier**: 2 (Foundation)

