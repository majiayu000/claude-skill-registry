---
name: adb-bypass
description: PlayIntegrityFork bypass verification and validation for Play Integrity spoofing detection
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 2
category: adb-automation
last_updated: 2025-12-02
compliance_score: 100
dependencies:
  - uiautomator2>=3.0.0
  - pyyaml>=6.0
  - click>=8.1.7
auto_trigger_keywords:
  - bypass
  - playintegrity
  - verification
  - validation
  - spoofing-detection
scripts:
  - name: preflight-validation.py
    purpose: Pre-flight checks for bypass prerequisites and configuration
    type: python
    command: uv run .claude/skills/adb-bypass/scripts/preflight-validation.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02

color: purple
---

---

## Quick Reference (30 seconds)

**PlayIntegrityFork Bypass Verification and Validation**

**What It Does**: Verifies PlayIntegrityFork installation status, validates bypass effectiveness, and checks device integrity spoofing detection. Used after Magisk module installation to confirm Play Integrity bypass is working.

**Core Capabilities**:
- ✅ **Bypass Verification**: Confirm PlayIntegrityFork is installed and active
- 🔍 **Detection Checking**: Verify app can't detect the bypass
- 📊 **Status Reporting**: Get detailed bypass status and metrics
- 🛡️ **Integrity Validation**: Validate device signature spoofing

**When to Use**:
- After installing PlayIntegrityFork Magisk module
- Before testing apps with Play Integrity checks
- Verifying bypass effectiveness across devices
- Troubleshooting bypass failures

---

## Scripts

### preflight-validation.py

Pre-flight checks for bypass prerequisites and configuration.

```bash
# Basic validation
uv run .claude/skills/adb-bypass/scripts/preflight-validation.py

# Specify device
uv run .claude/skills/adb-bypass/scripts/preflight-validation.py --device 127.0.0.1:5555

# Detailed check (verbose output)
uv run .claude/skills/adb-bypass/scripts/preflight-validation.py \
    --device 127.0.0.1:5555 \
    --detailed

# Check specific component
uv run .claude/skills/adb-bypass/scripts/preflight-validation.py \
    --check magisk \
    --check playintegrity \
    --check zygisk

# JSON output
uv run .claude/skills/adb-bypass/scripts/preflight-validation.py --json
```

**Features**:
- Magisk installation verification
- PlayIntegrityFork module check
- Zygisk enablement verification
- Device signature validation
- Detailed status reporting

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

**Example Workflows (adb-bypass):**
- `workflow/bypass-validation.toon` - Verify PlayIntegrityFork installation and bypass status
- `workflow/detection-check.toon` - Check if app detects the bypass
- `workflow/integrity-verification.toon` - Validate device signature spoofing

### Running a Workflow

Execute any workflow using the ADB workflow orchestrator:

```bash
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
  --workflow .claude/skills/adb-bypass/workflow/bypass-validation.toon \
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

## Usage Patterns

### Pattern 1: Pre-Flight Bypass Validation

```bash
# Run comprehensive pre-flight checks
uv run .claude/skills/adb-bypass/scripts/preflight-validation.py \
    --device 127.0.0.1:5555 \
    --detailed

# Check returns detailed status:
# - Magisk: installed, version, root status
# - PlayIntegrityFork: installed, version, enabled
# - Zygisk: enabled, subsystem status
# - Device: integrity signature, spoofing status
```

### Pattern 2: Workflow-Based Validation

```bash
# Complete validation workflow
uv run .claude/skills/adb-workflow-orchestrator/scripts/adb-run-workflow.py \
    --workflow .claude/skills/adb-bypass/workflow/bypass-validation.toon \
    --param device=127.0.0.1:5555 \
    --verbose
```

### Pattern 3: Integration with App Testing

```bash
# 1. Validate bypass is active
uv run .claude/skills/adb-bypass/scripts/preflight-validation.py \
    --device 127.0.0.1:5555

# 2. If validation passes, run app tests
if [ $? -eq 0 ]; then
  uv run .claude/skills/adb-karrot/scripts/adb-karrot-test-login.py \
      --device 127.0.0.1:5555
fi
```

---

## Integration Points

**Depends On**:
- System: `adb` command-line tool
- Python: uiautomator2, pyyaml, click

**Used By**:
- `adb-karrot` (for bypass validation before app testing)
- `adb-magisk` (for post-installation verification)
- Custom app automation workflows

**Complements**:
- `adb-magisk` (installs PlayIntegrityFork module)
- `adb-karrot` (tests apps after bypass activation)
- `adb-workflow-orchestrator` (orchestrates validation flows)

---

## PlayIntegrityFork Bypass Overview

**What is PlayIntegrityFork?**
PlayIntegrityFork is a Magisk module that hooks into Android's Play Integrity API to spoof device integrity and prevent detection of running on emulators or rooted devices.

**How It Works**:
```
Google Play Integrity API
  ├─ deviceIntegrity() check
  ├─ serverIntegrity() check
  └─ Error handling

PlayIntegrityFork Hook (via Zygisk)
  └─ Intercepts integrity requests
      └─ Returns spoofed device signature
          └─ App receives valid integrity response
```

**Prerequisites**:
- Magisk installed and functional
- Zygisk subsystem enabled
- PlayIntegrityFork module installed
- Module loaded and active

**Validation Checks**:
- Magisk root access confirmed
- PlayIntegrityFork module installed
- Zygisk subsystem enabled
- Device signature successfully spoofed
- No detection errors in logcat

---

## Troubleshooting

### Module Not Loaded

```bash
# Check Magisk modules
uv run .claude/skills/adb-magisk/scripts/adb-magisk-launch.py \
    --device 127.0.0.1:5555 \
    --wait-text "PlayIntegrityFork"

# Solution: Ensure Zygisk is enabled and device rebooted
```

### Zygisk Not Enabled

```bash
# Enable Zygisk
uv run .claude/skills/adb-magisk/scripts/adb-magisk-enable-zygisk.py \
    --device 127.0.0.1:5555 \
    --auto-reboot
```

### Device Detection Still Occurs

```bash
# Check logcat for errors
adb logcat | grep -i "integrity\|playintegrity"

# Common issues:
# - Module needs reboot to activate
# - Zygisk disabled or not loaded
# - Incompatible module version
```

---

## Architecture

**Design Principles**:
- **Validation-First**: Verify bypass before app testing
- **Comprehensive**: Check all bypass components
- **Detailed Reporting**: Clear status and error messages
- **Integration-Ready**: Works with workflow orchestrator

**Validation Sequence**:
```
1. Magisk Root Verification
   └─ Check root access, version

2. Module Installation Check
   └─ PlayIntegrityFork installed?

3. Zygisk Verification
   └─ Subsystem enabled and loaded?

4. Device Signature Check
   └─ Integrity spoofing active?

5. Status Reporting
   └─ Return detailed validation results
```

---

**Version**: 1.0.0
**Status**: ✅ Validation/Verification Tier
**Scripts**: 1 (comprehensive pre-flight)
**Workflows**: 3 (validation, detection, integrity)
**Last Updated**: 2025-12-02
**Tier**: 2 (Foundation)

