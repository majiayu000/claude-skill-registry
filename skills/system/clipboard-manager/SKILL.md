---
name: clipboard-manager
description: 复制和粘贴文本/文件到剪贴板，支持历史记录和格式转换。
metadata:
  short-description: 剪贴板操作
source:
  repository: https://github.com/asweigart/pyperclip
  license: BSD-3-Clause
---

# Clipboard Manager Tool

## Description
Copy and paste text and files to system clipboard with history tracking and format conversion.

## Trigger
- `/clipboard` command
- User needs clipboard operations
- User wants to copy/paste programmatically

## Usage

```bash
# Copy text to clipboard
python scripts/clipboard_manager.py copy "Hello World"

# Copy file content
python scripts/clipboard_manager.py copy --file document.txt

# Paste from clipboard
python scripts/clipboard_manager.py paste

# Paste to file
python scripts/clipboard_manager.py paste --output output.txt
```

## Tags
`clipboard`, `copy`, `paste`, `text`, `utility`

## Compatibility
- Codex: ✅
- Claude Code: ✅
