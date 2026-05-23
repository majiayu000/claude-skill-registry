---
name: gaming
description: |
  Gaming ecosystem for Bazzite. Steam fixes, Proton troubleshooting, EmuDeck emulation,
  Decky Loader plugins, Sunshine game streaming, frame generation, and media apps.
  Use when users need help with gaming on Bazzite.
---

# Gaming - Bazzite Gaming Ecosystem

## Overview

Bazzite is a gaming-focused OS with extensive Steam, emulation, and streaming support. This skill covers the gaming ecosystem.

## Quick Reference

### Steam & Proton

| Command | Description |
|---------|-------------|
| `ujust fix-gmod` | Patch GMod 64-bit for Linux |
| `ujust fix-proton-hang` | Kill hung wine/proton processes |
| `ujust fix-reset-steam` | Reset Steam (keeps games/saves) |
| `ujust steam-icons` | Manage Steam shortcuts on desktop |

### Streaming & Decky

| Command | Description |
|---------|-------------|
| `ujust setup-sunshine` | Setup Sunshine streaming server |
| `ujust setup-decky` | Install/uninstall Decky Loader |
| `ujust install-decky-plugins` | Install Decky plugins |

### Emulation & Tools

| Command | Description |
|---------|-------------|
| `ujust install-emudeck` | Install EmuDeck |
| `ujust get-emudeck` | Alias for install-emudeck |
| `ujust install-boxtron` | DOS games via Steam |
| `ujust install-steamcmd` | Install SteamCMD |
| `ujust get-lsfg` | Lossless Scaling frame gen layer |
| `ujust get-media-app` | Add streaming services to Steam |

## Steam Fixes

### GMod 64-bit Patch

```bash
# Patch Garry's Mod 64-bit beta for Linux
ujust fix-gmod
```

Fixes compatibility issues with the 64-bit branch.

### Kill Hung Proton

```bash
# Force-kill stuck wine/proton processes
ujust fix-proton-hang
```

Use when a game won't close or Steam shows a game as "running".

### Reset Steam

```bash
# Reset Steam folder to fresh state
ujust fix-reset-steam
```

**Preserves:**
- Game installations
- Save files
- Screenshots

**Resets:**
- Steam configuration
- Compatibility settings
- Shader cache

### Steam Shortcuts

```bash
# Manage Steam game shortcuts on desktop
ujust steam-icons
```

Creates/removes desktop shortcuts for Steam games.

## Game Streaming

### Sunshine Server

```bash
# Setup Sunshine (Moonlight protocol)
ujust setup-sunshine
```

**Features:**
- Host games for Moonlight clients
- Stream to phones, tablets, other PCs
- Hardware encoding (NVENC, VAAPI, QSV)

**After setup:**
- Access web UI at `https://localhost:47990`
- Pair with Moonlight client
- Configure apps and streaming settings

## Decky Loader

### Install/Uninstall

```bash
# Install or uninstall Decky Loader
ujust setup-decky
```

Decky Loader adds plugins to Steam's Game Mode.

### Install Plugins

```bash
# Install recommended plugins
ujust install-decky-plugins
```

**Installs:**
- Bazzite Buddy - Bazzite-specific features
- FrameGen - Frame generation
- LSFG-VK - Lossless Scaling Vulkan

## Emulation

### EmuDeck

```bash
# Install EmuDeck for emulation
ujust install-emudeck
```

EmuDeck configures:
- RetroArch cores
- Standalone emulators
- Steam ROM Manager
- Controller mappings

### Boxtron (DOS)

```bash
# Install Boxtron for DOS games via Steam
ujust install-boxtron
```

Enables DOSBox integration for Steam DOS games.

### SteamCMD

```bash
# Install SteamCMD
ujust install-steamcmd
```

Command-line Steam client for:
- Dedicated servers
- Game downloads
- Automation

## Frame Generation

### Lossless Scaling Layer

```bash
# Install/uninstall LSFG Vulkan layer
ujust get-lsfg
```

Adds frame generation to games via Vulkan layer.

## Media Apps

### Streaming Services

```bash
# Add streaming services to Steam
ujust get-media-app
```

**Adds:**
- YouTube
- Netflix
- Twitch
- Prime Video
- Other streaming services

Shows as non-Steam games in library for Game Mode access.

## Common Workflows

### Fresh Gaming Setup

```bash
# Install Decky with plugins
ujust setup-decky
ujust install-decky-plugins

# Install EmuDeck for emulation
ujust install-emudeck

# Add streaming apps
ujust get-media-app
```

### Game Streaming Host

```bash
# Setup Sunshine
ujust setup-sunshine

# On client devices, use Moonlight app
# Pair using PIN from Sunshine web UI
```

### Steam Troubleshooting

```bash
# Game won't close
ujust fix-proton-hang

# Major Steam issues
ujust fix-reset-steam
```

## Troubleshooting

### Proton Game Won't Launch

**Check Proton version:**

```bash
# Try different Proton version in Steam
# Right-click game > Properties > Compatibility
# Select specific Proton version
```

**Check logs:**

```bash
# Enable Proton logging
PROTON_LOG=1 steam steam://rungameid/<appid>
```

### Sunshine Not Streaming

**Check service:**

```bash
systemctl --user status sunshine
```

**Check ports:**
- TCP: 47984, 47989, 47990, 48010
- UDP: 47998-48000, 48002, 48010

### Decky Not Loading

**Reinstall:**

```bash
ujust setup-decky
```

**Check logs:**

```bash
journalctl --user -u decky -n 50
```

### EmuDeck Not Finding ROMs

**Check ROM paths:**
- Default: `~/Emulation/roms/<system>/`
- Ensure correct folder structure
- Run Steam ROM Manager to refresh

## Cross-References

- **bazzite:gpu** - GPU driver configuration
- **bazzite:audio** - Audio setup for gaming
- **bazzite-ai:configure** - Steam autostart, gamemode

## When to Use This Skill

Use when the user asks about:
- "Steam not working", "game won't launch", "Proton hang"
- "reset Steam", "Steam problems", "game stuck"
- "Sunshine", "game streaming", "Moonlight", "remote play"
- "Decky", "Steam Deck plugins", "Game Mode plugins"
- "EmuDeck", "emulation", "retro games", "ROMs"
- "frame generation", "LSFG", "Lossless Scaling"
- "Netflix on Steam", "streaming apps", "media in Game Mode"
- "GMod Linux", "Garry's Mod fix"
