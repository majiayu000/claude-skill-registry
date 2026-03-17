---
name: adb-magisk-installer
description: Complete Magisk system installation - from initial app setup to full system integration
version: 1.0.0
modularized: true
scripts_enabled: true
tier: 3
category: adb-system-installation
last_updated: 2025-12-02
compliance_score: 100
dependencies:
  - adb-screen-detection
  - adb-navigation-base
  - adb-uiautomator
  - adb-workflow-orchestrator
auto_trigger_keywords:
  - magisk
  - installation
  - system-integration
  - boot-image
  - fastboot
  - rooting
scripts:
  - name: adb-magisk-download.py
    purpose: Download Magisk APK and boot image from GitHub releases
    type: python
    command: uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-download.py
    zero_context: true
    version: 1.0.0
    last_updated: 2025-12-02

  - name: adb-magisk-install-app.py
    purpose: Install Magisk Manager app via adb install
    type: python
    command: uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-install-app.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02

  - name: adb-magisk-extract-boot.py
    purpose: Extract boot.img from device via adb pull
    type: python
    command: uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-extract-boot.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02

  - name: adb-magisk-patch-boot.py
    purpose: Patch boot image using Magisk app's patching mechanism
    type: python
    command: uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-patch-boot.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02

  - name: adb-magisk-flash-boot.py
    purpose: Flash patched boot image back to device via fastboot
    type: python
    command: uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-flash-boot.py
    zero_context: false
    version: 1.0.0
    last_updated: 2025-12-02

color: blue
---

---

## Quick Reference (30 seconds)

**Complete Magisk System Installation**

**What It Does**: Fully automates Magisk system installation from scratch. Handles app installation, boot image extraction, patching, and flashing. Transforms "Installed: N/A" to "Installed: Yes".

**Core Capabilities**:
- 📥 **Download**: Get latest Magisk APK and files from GitHub
- 📱 **App Install**: Install Magisk Manager via adb install
- 💾 **Boot Extract**: Pull boot.img from device
- 🔧 **Boot Patch**: Patch boot image using Magisk
- ⚡ **Boot Flash**: Flash patched image via fastboot

**When to Use**:
- Device shows "Installed: N/A" (Magisk not system-integrated)
- Fresh Magisk setup needed
- Upgrading Magisk version (27.0 → 30.6)
- Boot image needs patching

**Device Status Meaning**:
- ✅ `Installed: Yes` - Magisk integrated with system
- ⚠️ `Installed: N/A` - App installed, but boot image not patched/flashed
- ❌ `Installed: No` - Magisk app not installed

---

## Installation Workflow

The complete Magisk installation process (magisk-complete-install.toon):

### Phase 1: Download & Prepare
- Download Magisk APK from GitHub releases
- Download matching boot image (device-specific)
- Stage files on device storage (/sdcard)

### Phase 2: Install App
- Push Magisk Manager APK to device
- Install via `adb install`
- Verify app launches successfully

### Phase 3: Extract Boot Image
- Connect via adb
- Extract boot.img from active partition
- Store locally for patching

### Phase 4: Patch Boot Image
- Launch Magisk Manager app
- Select boot image for patching
- Magisk generates patched_boot.img
- Pull patched image from device

### Phase 5: Flash Boot Image
- Enable USB fastboot mode
- Flash patched_boot.img via fastboot
- Verify installation
- Device reboots with Magisk integrated

---

## Scripts

### adb-magisk-download.py

Download latest Magisk APK and boot image from GitHub releases.

```bash
# Download latest version
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-download.py \
    --output-dir /tmp/magisk

# Download specific version
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-download.py \
    --version 30.6 \
    --output-dir /tmp/magisk

# Include boot image
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-download.py \
    --version 30.6 \
    --include-boot \
    --output-dir /tmp/magisk

# JSON output
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-download.py \
    --version 30.6 \
    --json
```

---

### adb-magisk-install-app.py

Install Magisk Manager APK via adb install.

```bash
# Install APK on device
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-install-app.py \
    --device 127.0.0.1:5555 \
    --apk-path /tmp/magisk/Magisk-v30.6.apk

# Force reinstall
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-install-app.py \
    --device 127.0.0.1:5555 \
    --apk-path /tmp/magisk/Magisk-v30.6.apk \
    --force

# Verify after install
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-install-app.py \
    --device 127.0.0.1:5555 \
    --apk-path /tmp/magisk/Magisk-v30.6.apk \
    --verify

# JSON output
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-install-app.py \
    --device 127.0.0.1:5555 \
    --apk-path /tmp/magisk/Magisk-v30.6.apk \
    --json
```

---

### adb-magisk-extract-boot.py

Extract boot.img from device via adb pull.

```bash
# Extract boot image (auto-detects active partition)
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-extract-boot.py \
    --device 127.0.0.1:5555 \
    --output-path /tmp/magisk/boot.img

# Extract from specific partition
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-extract-boot.py \
    --device 127.0.0.1:5555 \
    --partition boot_a \
    --output-path /tmp/magisk/boot_a.img

# Verify integrity
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-extract-boot.py \
    --device 127.0.0.1:5555 \
    --output-path /tmp/magisk/boot.img \
    --verify

# JSON output
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-extract-boot.py \
    --device 127.0.0.1:5555 \
    --output-path /tmp/magisk/boot.img \
    --json
```

---

### adb-magisk-patch-boot.py

Patch boot image using Magisk Manager app.

```bash
# Patch boot image (interactive via Magisk app)
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-patch-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /sdcard/boot.img

# Wait for patching to complete
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-patch-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /sdcard/boot.img \
    --wait-completion

# Download patched image automatically
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-patch-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /sdcard/boot.img \
    --output-path /tmp/magisk/patched_boot.img

# JSON output
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-patch-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /sdcard/boot.img \
    --json
```

---

### adb-magisk-flash-boot.py

Flash patched boot image via fastboot.

```bash
# Flash patched boot image
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-flash-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /tmp/magisk/patched_boot.img

# Flash to specific partition
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-flash-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /tmp/magisk/patched_boot.img \
    --partition boot_b

# Auto-reboot after flash
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-flash-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /tmp/magisk/patched_boot.img \
    --reboot

# Verify before flashing
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-flash-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /tmp/magisk/patched_boot.img \
    --verify

# JSON output
uv run .claude/skills/adb-magisk-installer/scripts/adb-magisk-flash-boot.py \
    --device 127.0.0.1:5555 \
    --boot-path /tmp/magisk/patched_boot.img \
    --json
```

---

## Workflows

### magisk-complete-install.toon

Complete Magisk installation from scratch (14 steps, ~15 minutes).

```yaml
name: Complete Magisk Installation
description: Full system installation from "Installed: N/A" to "Installed: Yes"

parameters:
  device: "127.0.0.1:5555"
  version: "latest"
  timeout: 900

phases:
  - id: phase1_download
    name: Download Magisk Files
    steps:
      - id: download_apk
        action: adb-magisk-download
        params:
          version: "{{ version }}"
          include_boot: true
          output_dir: "/tmp/magisk"

  - id: phase2_app_install
    name: Install Magisk Manager App
    steps:
      - id: push_apk
        action: adb-magisk-install-app
        params:
          device: "{{ device }}"
          apk_path: "/tmp/magisk/Magisk-v{{ version }}.apk"
          force: true

      - id: verify_app
        action: adb-magisk-launch
        params:
          device: "{{ device }}"
          timeout: 15

  - id: phase3_extract_boot
    name: Extract Boot Image
    steps:
      - id: extract
        action: adb-magisk-extract-boot
        params:
          device: "{{ device }}"
          output_path: "/tmp/magisk/boot.img"

  - id: phase4_push_boot
    name: Push Boot to Device Storage
    steps:
      - id: push
        action: adb-push
        params:
          device: "{{ device }}"
          local: "/tmp/magisk/boot.img"
          remote: "/sdcard/boot.img"

  - id: phase5_patch_boot
    name: Patch Boot Image via Magisk
    steps:
      - id: open_magisk
        action: adb-magisk-launch
        params:
          device: "{{ device }}"

      - id: navigate_to_install
        action: adb-tap
        params:
          device: "{{ device }}"
          x: 100
          y: 400

      - id: select_boot
        action: adb-file-select
        params:
          path: "/sdcard/boot.img"

      - id: wait_patch
        action: adb-wait-for
        params:
          method: text
          target: "Patching complete"
          timeout: 120

  - id: phase6_pull_patched
    name: Pull Patched Boot Image
    steps:
      - id: pull
        action: adb-pull
        params:
          device: "{{ device }}"
          remote: "/sdcard/Download/magisk_patched*.img"
          local: "/tmp/magisk/patched_boot.img"

  - id: phase7_reboot_fastboot
    name: Reboot to Fastboot Mode
    steps:
      - id: reboot
        action: adb-reboot
        params:
          device: "{{ device }}"
          mode: fastboot

      - id: wait_fastboot
        action: adb-wait-fastboot
        params:
          device: "{{ device }}"
          timeout: 30

  - id: phase8_flash_boot
    name: Flash Patched Boot Image
    steps:
      - id: flash
        action: adb-magisk-flash-boot
        params:
          device: "{{ device }}"
          boot_path: "/tmp/magisk/patched_boot.img"
          reboot: true

      - id: wait_boot
        action: adb-wait-device
        params:
          device: "{{ device }}"
          timeout: 60

  - id: phase9_verify_installation
    name: Verify Magisk Installation
    steps:
      - id: launch_app
        action: adb-magisk-launch
        params:
          device: "{{ device }}"
          wait_text: "Installed"
          timeout: 30

recovery:
  - on_error: phase5_patch_boot
    action: retry
    max_attempts: 2
    delay: 5

  - on_error: phase8_flash_boot
    action: adb-screenshot-capture
    then: pause
```

---

## Decision Logic Integration

This skill follows **IndieDevDan Decision Logic Framework** patterns:

### Decision Point 1: Is Magisk Installed?
```
Device Status Check:
├─ Installed: Yes → Use adb-magisk skill
├─ Installed: No (app missing) → Phase 2 (install app)
└─ Installed: N/A (boot not patched) → Full workflow (Phase 1-9)
```

### Decision Point 2: Which Installation Method?
```
Installation Selection:
├─ Fresh device → Full workflow (download → install → patch → flash)
├─ App exists, needs patching → Skip Phase 1-2, start Phase 3
└─ Upgrade from older version → Full workflow with version override
```

### Decision Point 3: Boot Image Management
```
Boot Image Strategy:
├─ Extract → Patch → Flash workflow
├─ Auto-detect active partition (boot_a or boot_b)
├─ Verify integrity before flashing
└─ Rollback strategy if patch fails
```

---

## Integration Points

**Depends On**:
- `adb-screen-detection` (screenshot, OCR for "Patching complete")
- `adb-navigation-base` (tap, swipe, wait-for actions)
- `adb-uiautomator` (UI element interaction)
- `adb-workflow-orchestrator` (workflow execution and phase management)

**Used By**:
- `adb-karrot` (requires Magisk+PlayIntegrityFork for bypass)
- Any automation requiring system-level modifications
- ADB Auto Player setup workflows

**External Integration**:
- GitHub API (download Magisk releases)
- Fastboot protocol (flash boot images)
- ADB protocol (device communication)

---

## Troubleshooting

### "Installed: N/A" doesn't change after flashing
- Boot image may not be flashable on this device
- Try alternative partition (boot_b instead of boot_a)
- Some devices require vendor_boot patching (Magisk 30+)
- Check device bootloader version compatibility

### Fastboot connection fails
- Ensure device is in fastboot mode: `adb reboot fastboot`
- Check USB cable and host connection
- Verify fastboot binary is available in PATH
- Some devices need special drivers for fastboot

### Magisk patching fails
- Boot image format may be unsupported
- Try manual patching in Magisk app UI
- Check available storage on device (/sdcard)
- Ensure boot image file isn't corrupted

### Device bootloops after flashing
- Flash original boot.img to recover
- Use recovery mode if available
- Connect to custom recovery (TWRP) and flash backup
- Restore device via stock ROM if necessary

---

## Related Skills

- `adb-magisk` - Magisk Manager automation (module installation, configuration)
- `adb-karrot` - Uses Magisk for Play Integrity bypass
- `adb-workflow-orchestrator` - Orchestrates complex installation workflows

---

**Version**: 1.0.0
**Status**: ✅ Complete Installation Tier
**Scripts**: 5
**Workflows**: 1
**Last Updated**: 2025-12-02
**Tier**: 3 (System Installation)
