---
name: color-converter
description: 在HEX、RGB、HSL、HSV和CMYK格式之间转换颜色，支持调色板生成。
metadata:
  short-description: 转换颜色格式
source:
  repository: https://github.com/vaab/colour
  license: BSD-3-Clause
---

# Color Converter Tool

## Description
Convert colors between different formats (HEX, RGB, HSL, HSV, CMYK) and generate color palettes.

## Trigger
- `/color` command
- User needs color conversion
- User wants to generate palettes

## Usage

```bash
# Convert HEX to RGB
python scripts/color_converter.py "#FF5733"

# Convert RGB to HEX
python scripts/color_converter.py "rgb(255,87,51)"

# Generate palette
python scripts/color_converter.py "#FF5733" --palette complementary

# List named colors
python scripts/color_converter.py --list
```

## Tags
`color`, `hex`, `rgb`, `hsl`, `palette`

## Compatibility
- Codex: ✅
- Claude Code: ✅
