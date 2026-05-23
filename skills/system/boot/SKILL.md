---
name: boot
description: |
  Boot configuration for Bazzite OS. BIOS/UEFI access, GRUB menu settings,
  secure boot key enrollment, and Windows dual-boot setup. Use when users
  need to configure boot options or access BIOS settings.
---

# Boot - Bazzite Boot Configuration

## Overview

The boot skill covers BIOS/UEFI access, GRUB configuration, secure boot key management, and Windows dual-boot setup.

## Quick Reference

| Command | Description |
|---------|-------------|
| `ujust bios` | Reboot to BIOS/UEFI setup |
| `ujust bios-info` | Display BIOS information |
| `ujust regenerate-grub` | Regenerate GRUB config |
| `ujust config-grub` | Configure GRUB menu visibility |
| `ujust enroll-secure-boot-key` | Enroll NVIDIA/KMOD secure boot key |
| `ujust setup-boot-windows-steam` | Add Windows to Steam boot options |

## BIOS/UEFI

### Reboot to BIOS

```bash
# Reboot directly to BIOS/UEFI setup
ujust bios
```

System will reboot and enter BIOS setup automatically.

### View BIOS Info

```bash
# Display BIOS information
ujust bios-info
```

Uses `dmidecode` to show BIOS vendor, version, and date.

## GRUB Configuration

### Regenerate GRUB

```bash
# Regenerate GRUB configuration
ujust regenerate-grub
```

Useful for:
- Dual-boot setup changes
- New kernel installations
- Boot parameter changes

### GRUB Menu Visibility

```bash
# Interactive: choose hide/unhide/show
ujust config-grub

# Non-interactive options
ujust config-grub hide     # Hide GRUB menu (instant boot)
ujust config-grub unhide   # Show GRUB menu briefly
ujust config-grub show     # Always show GRUB menu
```

## Secure Boot

### Enroll Secure Boot Key

```bash
# Enroll NVIDIA driver and KMOD signing key
ujust enroll-secure-boot-key
```

Required for:
- NVIDIA proprietary drivers with Secure Boot enabled
- Custom kernel modules
- Third-party drivers

**Process:**
1. Generates MOK (Machine Owner Key)
2. Prompts for password
3. Reboots to MOK Manager
4. Enter password to enroll key

## Windows Dual-Boot

### Add Windows to Steam

```bash
# Add Windows boot option to Steam non-Steam games
ujust setup-boot-windows-steam
```

Allows booting to Windows directly from Steam's game library.

**Requirements:**
- Windows installed on separate partition/drive
- GRUB detecting Windows entry
- Steam installed

## Common Workflows

### Dual-Boot Setup

```bash
# Regenerate GRUB to detect Windows
ujust regenerate-grub

# Show GRUB menu on boot
ujust config-grub show

# Add Windows to Steam
ujust setup-boot-windows-steam
```

### Secure Boot with NVIDIA

```bash
# Enroll the signing key
ujust enroll-secure-boot-key

# Follow prompts, set password
# Reboot and enroll in MOK Manager
```

### Hide Boot Menu

```bash
# For single-boot systems
ujust config-grub hide
```

## Troubleshooting

### GRUB Not Showing Windows

**Fix:**

```bash
# Regenerate GRUB config
ujust regenerate-grub

# Check os-prober
sudo os-prober
```

### Secure Boot Key Enrollment Fails

**Check:**
- Secure Boot enabled in BIOS
- No pending updates
- Reboot completely (not just suspend)

**Retry:**

```bash
ujust enroll-secure-boot-key
```

### Can't Boot After GRUB Change

**From GRUB menu:**
1. Press `e` to edit entry
2. Modify boot parameters if needed
3. Press `F10` to boot

**Recover:**

```bash
# Boot from live USB
# Mount system partition
# Regenerate GRUB
```

## Cross-References

- **bazzite:system** - System maintenance
- **bazzite:gpu** - NVIDIA driver configuration
- **bazzite:security** - LUKS/TPM unlock

## When to Use This Skill

Use when the user asks about:
- "reboot to BIOS", "enter UEFI", "BIOS setup"
- "BIOS version", "BIOS info", "dmidecode"
- "GRUB menu", "boot menu", "regenerate grub"
- "hide boot menu", "show grub", "grub timeout"
- "secure boot", "MOK", "enroll key", "signing key"
- "dual boot", "Windows boot", "boot to Windows"
- "Windows from Steam", "game mode Windows"
