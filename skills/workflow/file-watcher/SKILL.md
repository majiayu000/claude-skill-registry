---
name: file-watcher
description: 监视文件和目录变化，支持事件回调和过滤。
metadata:
  short-description: 监视文件变化
source:
  repository: https://github.com/gorakhargosh/watchdog
  license: Apache-2.0
---

# File Watcher Tool

## Description
Watch files and directories for changes with event callbacks, pattern filtering, and action triggers.

## Trigger
- `/watch` command
- User needs to monitor files
- User wants change notifications

## Usage

```bash
# Watch directory
python scripts/file_watcher.py ./src/

# Watch with pattern filter
python scripts/file_watcher.py ./src/ --pattern "*.py"

# Watch and run command on change
python scripts/file_watcher.py ./src/ --exec "npm run build"

# Watch specific file
python scripts/file_watcher.py config.json
```

## Tags
`watch`, `files`, `monitor`, `events`, `automation`

## Compatibility
- Codex: ✅
- Claude Code: ✅
