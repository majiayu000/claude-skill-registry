---
name: file-archiver
description: 创建和解压ZIP、TAR和GZIP压缩包，支持密码保护。
metadata:
  short-description: 创建和解压压缩包
source:
  repository: https://docs.python.org/3/library/zipfile.html
  license: PSF
---

# File Archiver Tool

## Description
Create and extract compressed archives (ZIP, TAR, GZIP) with optional password protection.

## Trigger
- `/archive` command
- User requests file compression
- User needs to extract archives

## Usage

```bash
# Create ZIP archive
python scripts/file_archiver.py create --input folder/ --output archive.zip

# Extract archive
python scripts/file_archiver.py extract --input archive.zip --output extracted/

# Create with password
python scripts/file_archiver.py create --input folder/ --output secure.zip --password secret123

# List archive contents
python scripts/file_archiver.py list --input archive.zip
```

## Tags
`zip`, `archive`, `compress`, `extract`, `tar`

## Compatibility
- Codex: ✅
- Claude Code: ✅
