---
name: apps
description: |
  Third-party application installation for Bazzite. CoolerControl, DisplayLink,
  JetBrains Toolbox, OpenRazer, tablet drivers, scrcpy, and more. Use when users
  need to install hardware-specific or specialized applications.
---

# Apps - Third-Party Application Installation

## Overview

Install specialized applications and hardware drivers on Bazzite that aren't in Flatpak or require system integration.

## Quick Reference

### Hardware Control

| Command | Description |
|---------|-------------|
| `ujust install-coolercontrol` | Fan/pump control software |
| `ujust install-openrazer` | Razer gaming hardware drivers |
| `ujust install-openrgb` | RGB lighting control |
| `ujust install-opentabletdriver` | Drawing tablet drivers |
| `ujust remove-opentabletdriver` | Remove tablet drivers |

### Connectivity

| Command | Description |
|---------|-------------|
| `ujust install-displaylink` | Laptop dock video output |
| `ujust install-scrcpy` | Android device mirroring |
| `ujust install-resilio-sync` | BitTorrent file sync |

### Development

| Command | Description |
|---------|-------------|
| `ujust install-jetbrains-toolbox` | JetBrains IDE manager |

### Utilities

| Command | Description |
|---------|-------------|
| `ujust setup-cdemu` | CD/DVD emulation |
| `ujust pick` | Interactive ujust picker |

## Hardware Control

### CoolerControl

```bash
# Install CoolerControl for fan/pump management
ujust install-coolercontrol
```

**Features:**
- Fan curve customization
- Pump speed control
- Temperature monitoring
- Profile management

**Supports:**
- AIO coolers
- Case fans
- GPU fans (some)

### OpenRazer

```bash
# Install OpenRazer for Razer hardware
ujust install-openrazer
```

**Supports:**
- Razer keyboards
- Razer mice
- Razer headsets
- RGB effects

**Companion apps:**
- Polychromatic (GUI)
- RazerGenie
- OpenRGB

### OpenRGB

```bash
# Install OpenRGB for RGB lighting
ujust install-openrgb
```

**Features:**
- Universal RGB control
- Multiple brand support
- Custom effects
- Profile sync

### Drawing Tablets

```bash
# Install OpenTabletDriver
ujust install-opentabletdriver

# Remove if needed
ujust remove-opentabletdriver
```

**Supports:**
- Wacom tablets
- Huion tablets
- XP-Pen tablets
- Generic tablets

## Connectivity

### DisplayLink

```bash
# Install DisplayLink for docking stations
ujust install-displaylink
```

**Use for:**
- USB-C docks with video
- DisplayLink-based docks
- External monitors via USB

### scrcpy

```bash
# Install scrcpy for Android mirroring
ujust install-scrcpy
```

**Features:**
- Mirror Android screen
- Control device from PC
- Low latency
- No root required

**Usage:**

```bash
# Connect via USB
scrcpy

# Wireless (after enabling)
scrcpy --tcpip=192.168.x.x
```

### Resilio Sync

```bash
# Install Resilio Sync
ujust install-resilio-sync
```

**Features:**
- BitTorrent-based sync
- P2P file sharing
- Encrypted transfers
- Cross-platform

## Development

### JetBrains Toolbox

```bash
# Install JetBrains Toolbox
ujust install-jetbrains-toolbox
```

**Manages:**
- IntelliJ IDEA
- PyCharm
- WebStorm
- All JetBrains IDEs

**After install:**
- Launch Toolbox
- Log in to JetBrains account
- Install desired IDEs

## Utilities

### CD/DVD Emulation

```bash
# Setup CDEmu for virtual drives
ujust setup-cdemu
```

**Features:**
- Mount ISO files
- Virtual CD/DVD drives
- Legacy software support

**Usage:**

```bash
# Load ISO
cdemu load 0 /path/to/image.iso

# Unload
cdemu unload 0
```

### Interactive ujust Picker

```bash
# Browse all ujust commands interactively
ujust pick
```

**Features:**
- Search commands
- Category browsing
- Command descriptions
- Direct execution

## Common Workflows

### Gaming Setup

```bash
# RGB control
ujust install-openrgb

# Razer hardware
ujust install-openrazer

# Fan control
ujust install-coolercontrol
```

### Digital Art Setup

```bash
# Tablet driver
ujust install-opentabletdriver

# Android tablet as input (via scrcpy)
ujust install-scrcpy
```

### Development Setup

```bash
# JetBrains IDEs
ujust install-jetbrains-toolbox

# For AI development, see bazzite-ai:install
```

### Docking Station

```bash
# DisplayLink for monitors
ujust install-displaylink

# May need reboot
systemctl reboot
```

## Troubleshooting

### CoolerControl Not Detecting Fans

**Check sensors:**

```bash
sensors-detect
sensors
```

**Verify service:**

```bash
systemctl status coolercontrold
```

### OpenRazer Device Not Found

**Check connection:**

```bash
# List USB devices
lsusb | grep -i razer
```

**Check daemon:**

```bash
systemctl --user status openrazer-daemon
```

### DisplayLink Not Working

**Check module:**

```bash
lsmod | grep evdi
```

**Reconnect dock and check:**

```bash
dmesg | tail -20
```

### Tablet Not Responding

**Check device:**

```bash
# List tablets
otd list
```

**Check daemon:**

```bash
systemctl --user status opentabletdriver
```

## Cross-References

- **bazzite-ai:install** - Development tools (Claude Code, pixi)
- **bazzite:gaming** - Gaming-specific apps (Decky, EmuDeck)
- **bazzite:distrobox** - Apps requiring containers

## When to Use This Skill

Use when the user asks about:
- "CoolerControl", "fan control", "pump speed"
- "Razer", "OpenRazer", "Razer keyboard", "Razer mouse"
- "RGB lighting", "OpenRGB", "LED control"
- "drawing tablet", "Wacom", "Huion", "tablet driver"
- "DisplayLink", "dock", "USB-C dock", "external monitors"
- "scrcpy", "Android mirror", "phone screen"
- "JetBrains", "IntelliJ", "PyCharm", "IDE"
- "CD emulation", "mount ISO", "virtual drive"
- "ujust picker", "browse commands"
