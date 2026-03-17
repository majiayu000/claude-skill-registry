---
name: screenshot-capture
description: 捕获屏幕、窗口或区域的截图，支持标注。
metadata:
  short-description: 捕获截图
source:
  repository: https://github.com/python-pillow/Pillow
  license: HPND
---

# Screenshot Capture Tool

## Description
Capture screenshots of the entire screen, specific windows, or custom regions with annotation support.

## Trigger
- `/screenshot` command
- User needs to capture screen
- User wants to take screenshots

## Usage

```bash
# Capture full screen
python scripts/screenshot_capture.py --output screen.png

# Capture region
python scripts/screenshot_capture.py --region 0,0,800,600 --output region.png

# Capture with delay
python scripts/screenshot_capture.py --delay 3 --output delayed.png
```

## Tags
`screenshot`, `capture`, `screen`, `image`, `automation`

## Compatibility
- Codex: ✅
- Claude Code: ✅
