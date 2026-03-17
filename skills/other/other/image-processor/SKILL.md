---
name: image-processor
description: 处理图片 - 调整大小、转换格式、添加水印、生成缩略图。基于Pillow。
metadata:
  short-description: 调整大小、转换和处理图片
source:
  repository: https://github.com/python-pillow/Pillow
  license: HPND
---

# Image Processor Tool

## Description
Process images with resize, format conversion, watermarks, and thumbnail generation.

## Trigger
- `/process-image` command
- User requests image manipulation
- User needs to resize or convert images

## Usage

```bash
# Resize image
python scripts/process_image.py resize --input photo.jpg --output resized.jpg --width 800

# Convert format
python scripts/process_image.py convert --input photo.png --output photo.webp

# Add watermark
python scripts/process_image.py watermark --input photo.jpg --output marked.jpg --text "© 2024"

# Generate thumbnails
python scripts/process_image.py thumbnail --input photo.jpg --sizes 64,128,256
```

## Tags
`image`, `resize`, `convert`, `thumbnail`, `watermark`

## Compatibility
- Codex: ✅
- Claude Code: ✅
