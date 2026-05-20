---
name: screen-recorder
description: Record the macOS screen for a fixed duration and always save the .mov in ~/Downloads. Use when the user asks to record the screen, make a QuickTime screen recording, or capture a short screen video for N seconds.
---

# Screen Recorder

## Overview
Record the screen for a specified number of seconds and save the video to `~/Downloads`.

## Quick Start

```bash
scripts/record_screen.sh --seconds 10
```

## Tasks

### Record screen for N seconds
- Run `scripts/record_screen.sh --seconds <N>`.
- The file is saved as `~/Downloads/screen-recording-YYYYMMDD-HHMMSS.mov`.
- The recording opens in QuickTime Player automatically.

## Resources

### scripts/
- `record_screen.sh`: Records screen video via `screencapture -V` and saves to `~/Downloads`.
