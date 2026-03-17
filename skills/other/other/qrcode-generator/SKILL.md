---
name: qrcode-generator
description: 从文本、URL或数据生成二维码，支持自定义颜色、Logo和多种输出格式。
metadata:
  short-description: 生成二维码
source:
  repository: https://github.com/lincolnloop/python-qrcode
  license: BSD
---

# QR Code Generator Tool

## Description
Generate QR codes with custom styling, colors, and embedded logos.

## Trigger
- `/qrcode` command
- User requests QR code generation
- User needs to encode data as QR

## Usage

```bash
# Generate simple QR code
python scripts/qrcode_generator.py --data "https://example.com" --output qr.png

# Generate with custom colors
python scripts/qrcode_generator.py --data "Hello" --output qr.png --fill-color "#000000" --back-color "#FFFFFF"

# Generate with logo
python scripts/qrcode_generator.py --data "https://example.com" --output qr.png --logo logo.png
```

## Tags
`qrcode`, `barcode`, `image`, `encoding`

## Compatibility
- Codex: ✅
- Claude Code: ✅
