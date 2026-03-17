---
name: adb-magisk
description: Magisk Manager automation - app launching, module installation, Zygisk configuration
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 3
category: adb-app-automation
last_updated: 2025-12-01
compliance_score: 100
dependencies:
  - adb-screen-detection
  - adb-navigation-base
  - adb-workflow-orchestrator
auto_trigger_keywords:
  - magisk
  - zygisk
  - module
  - installation
scripts:
  - name: adb-magisk-launch.py
    purpose: Launch Magisk Manager app
    type: python
    command: uv run .claude/skills/adb-magisk/scripts/adb-magisk-launch.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-magisk-enable-zygisk.py
    purpose: Enable Zygisk in Magisk settings
    type: python
    command: uv run .claude/skills/adb-magisk/scripts/adb-magisk-enable-zygisk.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-01

  - name: adb-magisk-install-module.py
    purpose: Install Magisk module from zip file
    type: python
    command: uv run .claude/skills/adb-magisk/scripts/adb-magisk-install-module.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-01

color: green
---

---

## Quick Reference (30 seconds)

**Magisk Manager Automation**

**What It Does**: Automates Magisk Manager application for module management and configuration. Handles app launching, Zygisk enabling, and module installation workflows.

**Core Capabilities**:
- 🚀 **App Launching**: Open Magisk Manager with auto-detection
- ⚙️ **Zygisk Configuration**: Enable/disable Zygisk subsystem
- 📦 **Module Installation**: Automated module zip installation
- 🔄 **State Verification**: Confirm configuration changes

**When to Use**:
- Need to configure Magisk for app modifications
- Installing custom modules (like PlayIntegrityFork)
- Enabling Zygisk for API hooking
- Automating Play Integrity bypass setup

---

## Scripts

### adb-magisk-launch.py

Launch Magisk Manager application.

```bash
# Launch on default device
uv run .claude/skills/adb-magisk/scripts/adb-magisk-launch.py

# Specify device
uv run .claude/skills/adb-magisk/scripts/adb-magisk-launch.py --device 127.0.0.1:5555

# Wait for app to load
uv run .claude/skills/adb-magisk/scripts/adb-magisk-launch.py --wait-text "Modules"

# JSON output
uv run .claude/skills/adb-magisk/scripts/adb-magisk-launch.py --json
```

---

### adb-magisk-enable-zygisk.py

Enable Zygisk in Magisk settings (prerequisite for API hooking).

```bash
# Enable Zygisk
uv run .claude/skills/adb-magisk/scripts/adb-magisk-enable-zygisk.py --device 127.0.0.1:5555

# Verify after enabling (auto-waits for reboot prompt)
uv run .claude/skills/adb-magisk/scripts/adb-magisk-enable-zygisk.py \
    --device 127.0.0.1:5555 \
    --auto-reboot

# JSON output
uv run .claude/skills/adb-magisk/scripts/adb-magisk-enable-zygisk.py --json
```

---

### adb-magisk-install-module.py

Install Magisk module from zip file.

```bash
# Install module
uv run .claude/skills/adb-magisk/scripts/adb-magisk-install-module.py \
    --device 127.0.0.1:5555 \
    --module-path /sdcard/PlayIntegrityFork.zip

# Verify after installation
uv run .claude/skills/adb-magisk/scripts/adb-magisk-install-module.py \
    --device 127.0.0.1:5555 \
    --module-path /sdcard/PlayIntegrityFork.zip \
    --verify

# JSON output
uv run .claude/skills/adb-magisk/scripts/adb-magisk-install-module.py \
    --device 127.0.0.1:5555 \
    --module-path /sdcard/PlayIntegrityFork.zip \
    --json
```

---

## Workflows

### magisk-setup.toon

Complete Magisk setup with Zygisk enablement.

```yaml
name: Setup Magisk with Zygisk
description: Configure Magisk for API hooking with Zygisk subsystem

parameters:
  device: "127.0.0.1:5555"
  timeout: 15

phases:
  - id: phase1_launch
    name: "Launch Magisk Manager"
    steps:
      - id: launch
        action: adb-magisk-launch
        params:
          device: "{{ device }}"
          wait_text: "Modules"
          timeout: "{{ timeout }}"

  - id: phase2_enable_zygisk
    name: "Enable Zygisk"
    steps:
      - id: enable
        action: adb-magisk-enable-zygisk
        params:
          device: "{{ device }}"
          auto_reboot: false

      - id: verify
        action: adb-wait-for
        params:
          method: text
          target: "Zygisk enabled"
          timeout: 10

recovery:
  - on_error: phase2_enable_zygisk
    action: retry
    max_attempts: 2
    delay: 2
```

### install-module.toon

Module installation workflow (used by Play Integrity bypass).

```yaml
name: Install Magisk Module
description: Install module zip file via Magisk Manager

parameters:
  device: "127.0.0.1:5555"
  module_path: "/sdcard/PlayIntegrityFork.zip"
  timeout: 20

phases:
  - id: phase1_launch
    name: "Launch Magisk Manager"
    steps:
      - id: launch
        action: adb-magisk-launch
        params:
          device: "{{ device }}"

  - id: phase2_navigate
    name: "Navigate to Modules"
    steps:
      - id: wait_modules_tab
        action: adb-wait-for
        params:
          method: text
          target: "Modules"
          timeout: 5

      - id: tap_modules
        action: adb-tap
        params:
          x: 100
          y: 100
          device: "{{ device }}"

  - id: phase3_install
    name: "Install Module"
    steps:
      - id: tap_fab
        action: adb-tap
        params:
          x: 400
          y: 800
          device: "{{ device }}"

      - id: wait_file_picker
        action: adb-wait-for
        params:
          method: text
          target: "Select file"
          timeout: 5

      - id: select_module
        action: adb-file-select
        params:
          path: "{{ module_path }}"

      - id: wait_completion
        action: adb-wait-for
        params:
          method: text
          target: "Installation complete"
          timeout: "{{ timeout }}"

recovery:
  - on_error: phase3_install
    action: adb-screenshot-capture
    then: continue
```

---

## Usage Patterns

### Pattern 1: Setup Magisk for Hooking

```bash
# Execute setup workflow
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
    --workflow .claude/skills/adb-magisk/workflows/magisk-setup.toon \
    --param device=127.0.0.1:5555
```

### Pattern 2: Install PlayIntegrityFork Module

```bash
# Execute installation workflow
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
    --workflow .claude/skills/adb-magisk/workflows/install-module.toon \
    --param device=127.0.0.1:5555 \
    --param module_path=/sdcard/PlayIntegrityFork.zip
```

### Pattern 3: Verify Magisk Configuration

```bash
# Launch and verify Zygisk is enabled
uv run .claude/skills/adb-magisk/scripts/adb-magisk-launch.py \
    --device 127.0.0.1:5555 \
    --wait-text "Zygisk" \
    --timeout 10
```

---

## Integration Points

**Depends On**:
- `adb-screen-detection` (screenshot, find-element, tap verification)
- `adb-navigation-base` (tap, swipe, wait-for)
- `adb-workflow-orchestrator` (orchestration of complex flows)

**Used By**:
- `adb-karrot` (for Play Integrity bypass setup)
- Custom automation workflows

---

## Magisk Manager UI Reference

```
Home Screen
  ├─ Modules tab (module list)
  ├─ Settings tab (Zygisk toggle)
  └─ Superuser tab (permission management)

Modules Tab
  ├─ + FAB (install module)
  ├─ Module list (installed modules)
  └─ Enable/disable toggles

File Picker
  ├─ /sdcard (default storage location)
  ├─ Select zip file
  └─ Confirm installation

Installation Dialog
  ├─ Progress bar
  ├─ Installation complete
  └─ Reboot required (optional)
```

---

**Version**: 1.0.0
**Status**: ✅ App-Specific Tier
**Scripts**: 3
**Workflows**: 2
**Last Updated**: 2025-12-01
**Tier**: 3 (App-Specific)

