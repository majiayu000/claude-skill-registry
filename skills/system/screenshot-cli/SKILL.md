---
name: screenshot-cli
description: Take screenshots. Use when needing to see the screen or debug graphical issues.
---

# Usage

```bash
screenshot-cli                    # Fullscreen (default)
screenshot-cli -w                 # Focused window
screenshot-cli -r                 # Interactive region selection
screenshot-cli -d 3               # Delay 3s before capture
screenshot-cli /tmp/shot.png      # Custom output path
screenshot-cli -s 1               # Specific monitor (macOS only)
```

Prints the output file path on stdout. Default: `~/.claude/outputs/screenshot-TIMESTAMP.png`

View the result with the `read` tool:

```bash
path=$(screenshot-cli)
# read "$path"
```
