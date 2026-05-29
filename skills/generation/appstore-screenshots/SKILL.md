---
name: appstore-screenshots
description: Resize screenshots to App Store required dimensions. Use when uploading screenshots to App Store Connect fails with "dimensions are wrong" error. Supports iPhone 6.7", 6.5", 5.5" and iPad sizes.
---

# App Store Screenshots

Resize screenshots for App Store Connect.

## Usage

```bash
python3 .claude/skills/appstore-screenshots/scripts/resize_screenshots.py <input_dir> [output_dir] [size]
```

## Examples

```bash
# Default: 6.5" iPhone (1284x2778)
python3 .claude/skills/appstore-screenshots/scripts/resize_screenshots.py website/assets/screenshots/mobile/ios

# Specify output and size
python3 .claude/skills/appstore-screenshots/scripts/resize_screenshots.py ./screenshots ./appstore 6.7
```

## Sizes

| Size | Dimensions | Devices |
|------|------------|---------|
| `6.7` | 1290×2796 | iPhone 15/14 Pro Max |
| `6.5` | 1284×2778 | iPhone 14 Plus, 13/12 Pro Max |
| `6.5-alt` | 1242×2688 | iPhone 11 Pro Max, XS Max |
| `5.5` | 1242×2208 | iPhone 8/7/6s Plus |
| `ipad-12.9` | 2048×2732 | iPad Pro 12.9" |
| `ipad-11` | 1668×2388 | iPad Pro 11" |

## Requirements

- Python 3
- Pillow: `pip install Pillow`
