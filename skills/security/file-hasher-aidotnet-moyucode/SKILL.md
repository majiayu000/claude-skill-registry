---
name: file-hasher
description: 计算文件哈希值（MD5、SHA1、SHA256、SHA512）用于完整性验证和比较。
metadata:
  short-description: 计算文件哈希值
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# File Hasher Tool

## Description
Calculate cryptographic hashes for files to verify integrity, detect duplicates, or generate checksums.

## Trigger
- `/hash` command
- User needs file checksums
- User wants to verify file integrity

## Usage

```bash
# Calculate SHA256 hash
python scripts/file_hasher.py file.zip

# Calculate multiple hash types
python scripts/file_hasher.py file.zip --all

# Verify against known hash
python scripts/file_hasher.py file.zip --verify abc123...

# Hash multiple files
python scripts/file_hasher.py *.zip --algorithm sha256

# Find duplicate files
python scripts/file_hasher.py --find-duplicates ./folder/
```

## Tags
`hash`, `checksum`, `md5`, `sha256`, `integrity`

## Compatibility
- Codex: ✅
- Claude Code: ✅
