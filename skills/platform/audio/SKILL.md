---
name: audio
description: |
  Audio configuration for Bazzite. Virtual audio channels for Game/Voice/Browser/Music,
  7.1 surround for headphones, Bluetooth headset profiles, and PipeWire management.
  Use when users need to configure audio on Bazzite.
---

# Audio - Bazzite Audio Configuration

## Overview

Bazzite uses PipeWire for audio. This skill covers virtual audio channels, surround sound emulation, Bluetooth audio, and PipeWire management.

## Quick Reference

| Command | Description |
|---------|-------------|
| `ujust setup-virtual-channels` | Create Game/Voice/Browser/Music sinks |
| `ujust setup-virtual-surround` | Setup 7.1 surround for headphones |
| `ujust toggle-bt-mic` | Toggle Bluetooth headset profile fix |
| `ujust restart-pipewire` | Restart PipeWire service |

## Virtual Audio Channels

### Setup Virtual Channels

```bash
# Create virtual audio sinks
ujust setup-virtual-channels
```

**Creates sinks:**
- **Game** - Game audio
- **Voice** - Discord, voice chat
- **Browser** - Web browser audio
- **Music** - Music players

**Use case:** Route different apps to different channels for:
- Separate volume control
- Stream audio isolation
- Recording specific sources

### Using Virtual Channels

After setup, select sinks in PipeWire/PulseAudio-compatible apps:

1. Open app settings
2. Select output device
3. Choose Game/Voice/Browser/Music

In `pavucontrol`:
1. Go to "Playback" tab
2. Click app dropdown
3. Select virtual sink

## Surround Sound

### Virtual 7.1 Surround

```bash
# Setup 7.1 surround for headphones
ujust setup-virtual-surround
```

Creates a virtual 7.1 surround sink that:
- Takes stereo headphone output
- Uses HRTF spatializer
- Simulates surround positioning

**Best for:**
- Gaming with positional audio
- Movies with surround tracks
- Stereo headphones

## Bluetooth Audio

### Toggle BT Mic Fix

```bash
# Toggle Bluetooth headset profile mitigation
ujust toggle-bt-mic
```

Fixes issues with Bluetooth headsets switching profiles when:
- Mic is enabled/disabled
- Switching between A2DP and HSP/HFP
- Audio quality drops unexpectedly

## PipeWire Management

### Restart PipeWire

```bash
# Restart PipeWire and related services
ujust restart-pipewire
```

Restarts:
- pipewire
- pipewire-pulse
- wireplumber

Use when:
- Audio stops working
- Bluetooth audio issues
- After configuration changes

## Common Workflows

### Streaming Setup

```bash
# Create virtual channels
ujust setup-virtual-channels

# In OBS:
# - Capture "Game" sink for game audio
# - Capture "Voice" sink for Discord
# - Exclude browser/music from stream
```

### Gaming Audio

```bash
# Enable 7.1 surround for headphones
ujust setup-virtual-surround

# In game settings:
# - Select 7.1 surround output
# - Enable spatial audio
```

### Bluetooth Troubleshooting

```bash
# If BT audio drops or switches profiles
ujust toggle-bt-mic

# Restart audio stack
ujust restart-pipewire
```

## Advanced Configuration

### PipeWire Config Location

```
~/.config/pipewire/
~/.config/wireplumber/
```

### Check Audio Devices

```bash
# List sinks
pactl list sinks short

# List sources
pactl list sources short

# PipeWire info
pw-cli info
```

### Volume Control

```bash
# GUI volume control
pavucontrol

# CLI volume control
pactl set-sink-volume @DEFAULT_SINK@ 50%
```

## Troubleshooting

### No Audio

**Check PipeWire status:**

```bash
systemctl --user status pipewire
systemctl --user status pipewire-pulse
```

**Restart:**

```bash
ujust restart-pipewire
```

### Virtual Channels Not Showing

**Verify sinks:**

```bash
pactl list sinks short | grep -E "Game|Voice|Browser|Music"
```

**Recreate:**

```bash
ujust setup-virtual-channels
```

### Bluetooth Audio Choppy

**Check codec:**

```bash
pactl list cards | grep -A10 "bluez"
```

**Switch to SBC-XQ or AAC if available:**
Use `pavucontrol` > Configuration tab

### Surround Not Working

**Check sink:**

```bash
pactl list sinks short | grep surround
```

**Verify game audio settings:**
- Game must output 5.1/7.1
- Virtual sink must be selected

## Cross-References

- **bazzite:gaming** - Gaming audio setup
- **bazzite:network** - Bluetooth considerations
- **bazzite-ai:configure** - Service configuration

## When to Use This Skill

Use when the user asks about:
- "audio channels", "virtual sinks", "separate audio"
- "surround sound", "7.1 headphones", "spatial audio"
- "Bluetooth mic", "BT audio", "headset profile"
- "restart audio", "PipeWire restart", "audio not working"
- "Game audio", "Voice chat audio", "streaming audio"
- "audio routing", "OBS audio", "Discord audio"
