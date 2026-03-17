---
name: url-shortener
description: 使用各种服务缩短URL，并为短链接生成二维码。
metadata:
  short-description: 缩短URL
source:
  repository: https://github.com/ellisonleao/pyshorteners
  license: MIT
---

# URL Shortener Tool

## Description
Shorten long URLs using various services and optionally generate QR codes for the shortened links.

## Trigger
- `/shorten` command
- User needs to shorten URLs
- User wants short links

## Usage

```bash
# Shorten URL
python scripts/url_shortener.py "https://example.com/very/long/path"

# Shorten with specific service
python scripts/url_shortener.py "https://example.com" --service tinyurl

# Generate QR code for shortened URL
python scripts/url_shortener.py "https://example.com" --qr --output qr.png
```

## Tags
`url`, `shortener`, `link`, `tinyurl`, `qr`

## Compatibility
- Codex: ✅
- Claude Code: ✅
