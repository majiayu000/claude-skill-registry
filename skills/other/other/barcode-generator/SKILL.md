---
name: barcode-generator
description: 生成各种条形码格式，包括Code128、EAN、UPC等。
metadata:
  short-description: 生成条形码
source:
  repository: https://github.com/WhyNotHugo/python-barcode
  license: MIT
---

# Barcode Generator Tool

## Description
Generate various barcode formats including Code128, EAN-13, UPC-A, Code39, and more.

## Trigger
- `/barcode` command
- User needs to generate barcodes
- User wants product codes

## Usage

```bash
# Generate Code128 barcode
python scripts/barcode_generator.py "ABC123" --format code128 --output barcode.png

# Generate EAN-13
python scripts/barcode_generator.py "5901234123457" --format ean13

# Generate with custom size
python scripts/barcode_generator.py "12345" --format code39 --width 400 --height 100
```

## Tags
`barcode`, `code128`, `ean`, `upc`, `generator`

## Compatibility
- Codex: ✅
- Claude Code: ✅
