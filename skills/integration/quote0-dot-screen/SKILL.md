---
name: quote0-dot-screen
description: Control Quote/0 electronic screen devices via Dot API. Use when the user needs to interact with Quote/0 devices for - getting device information or status, displaying text content, displaying images, switching content, or listing device tasks.
license: MIT
compatibility: Requires Python 3.10+ (uses modern type hints like `str | None`). No external dependencies - uses only Python standard library (urllib, json, argparse).
metadata:
  author: ISON
  version: "1.0.0"
---

# Quote/0 Dot Screen Controller

## Overview

This skill provides control over Quote/0 electronic screen devices through the Dot Developer Platform APIs.

> **CRITICAL:** You MUST use the provided Python scripts in the `scripts/` directory for ALL operations. Do NOT attempt to make direct API calls (via `curl`, `requests`, or custom code). The scripts handle authentication, error handling, and response formatting.

## Prerequisites

Check for `DOT_API_KEY` environment variable before any operation. If not set, guide the user to:
1. Visit https://dot.mindreset.tech/docs/service/open/get_api
2. Create an API key in the Dot. App
3. Export the key: `export DOT_API_KEY=xxx`

## Scripts Reference

All scripts are located in `scripts/` directory. Run from the skill root directory.

### list_devices.py - List All Devices

Get all available devices and their serial numbers (device_id).

```bash
python3 scripts/list_devices.py [--format json|markdown]
```

- `--format`: Output format (default: markdown)
- Returns: Device serial numbers, series, model, edition

### device_status.py - Get Device Status

Query a device's current state and connection status.

```bash
python3 scripts/device_status.py <device_id> [--format json|markdown]
```

- `device_id`: Device serial number (required, get from list_devices.py)
- `--format`: Output format (default: markdown)

### display_text.py - Display Text on Device

Show text content on device screen.

```bash
python3 scripts/display_text.py <device_id> <message> [options]
```

**Required:**
- `device_id`: Device serial number
- `message`: Text content to display

**Optional:**
- `--title <title>`: Title to display
- `--signature <signature>`: Signature to display
- `--icon <base64>`: Base64-encoded PNG icon (40px×40px)
- `--link <url>`: NFC redirect link
- `--task-key <key>`: Task key for updating specific Text API content
- `--no-refresh`: Do not display immediately

### display_image.py - Display Image on Device

Show image content on device screen.

```bash
python3 scripts/display_image.py <device_id> <image> [options]
```

**Required:**
- `device_id`: Device serial number
- `image`: Base64-encoded PNG image data (296px×152px)

**Optional:**
- `--link <url>`: NFC redirect link
- `--border <0|1>`: Border color (0=white, 1=black, default: 0)
- `--dither-type <type>`: Dither type (DIFFUSION, ORDERED, NONE)
- `--dither-kernel <kernel>`: Dither kernel (FLOYD_STEINBERG, ATKINSON, BURKES)
- `--task-key <key>`: Task key for updating specific Image API content
- `--no-refresh`: Do not display immediately

### switch_next.py - Switch to Next Content

Navigate to next content item in device's display loop.

```bash
python3 scripts/switch_next.py <device_id> [--format json|markdown]
```

- `device_id`: Device serial number (required)

### list_tasks.py - List Device Tasks

Get list of content tasks configured on device.

```bash
python3 scripts/list_tasks.py <device_id> [task_type] [--format json|markdown]
```

- `device_id`: Device serial number (required)
- `task_type`: Task type (default: loop)
- `--format`: Output format (default: markdown)

## Device Specifications

- Screen resolution: 296px × 152px
- Icon size: 40px × 40px (for text display)
- Image format: PNG, Base64-encoded

## Troubleshooting

- **API key not found**: Check `DOT_API_KEY` environment variable is set
- **Device not updating**: Check device status, ensure WiFi connected
- **Image issues**: Verify Base64 encoding, check resolution, try different dither types
