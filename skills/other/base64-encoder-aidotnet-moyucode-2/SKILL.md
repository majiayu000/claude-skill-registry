---
name: base64-encoder
description: 编码和解码Base64、URL安全Base64和十六进制字符串，支持文件处理。
metadata:
  short-description: Base64编码/解码
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# Base64 Encoder Tool

## Description
Encode and decode Base64, URL-safe Base64, and hexadecimal strings with support for files.

## Trigger
- `/base64` command
- User needs to encode/decode data
- User wants to convert binary to text

## Usage

```bash
# Encode text
python scripts/base64_encoder.py encode "Hello World"

# Decode Base64
python scripts/base64_encoder.py decode "SGVsbG8gV29ybGQ="

# Encode file
python scripts/base64_encoder.py encode --file image.png --output image.b64

# URL-safe encoding
python scripts/base64_encoder.py encode "data" --url-safe
```

## Tags
`base64`, `encode`, `decode`, `binary`, `text`

## Compatibility
- Codex: ✅
- Claude Code: ✅
