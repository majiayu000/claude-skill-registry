---
name: text-diff
description: 比较文件和文本，支持统一diff、并排视图和补丁生成。
metadata:
  short-description: 比较文件/文本
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# Text Diff Tool

## Description
Compare files and text content with unified diff output, side-by-side view, and patch generation.

## Trigger
- `/diff` command
- User needs to compare files
- User wants to see changes

## Usage

```bash
# Compare two files
python scripts/text_diff.py file1.txt file2.txt

# Unified diff format
python scripts/text_diff.py old.py new.py --unified

# Side-by-side view
python scripts/text_diff.py file1.txt file2.txt --side-by-side

# Generate patch
python scripts/text_diff.py old.txt new.txt --patch > changes.patch
```

## Tags
`diff`, `compare`, `patch`, `text`, `files`

## Compatibility
- Codex: ✅
- Claude Code: ✅
