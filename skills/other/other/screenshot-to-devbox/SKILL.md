---
name: screenshot-to-devbox
description: Use when you need to share a screenshot with Claude Code running on the devbox over SSH, since Ctrl+V image paste doesn't work remotely
---

# Screenshot to Devbox

## Overview

Claude Code supports pasting images from the clipboard with Ctrl+V, but this only works when Claude Code can access the local OS clipboard. Over SSH, the remote Claude Code process can't see your Mac's clipboard.

**Solution:** Take a screenshot locally, upload it to the devbox, and reference the path.

## Usage

From your Mac terminal (not inside SSH):

```bash
screenshot-to-devbox
```

Or use the alias:

```bash
ssdb
```

This will:
1. Open macOS screenshot selection (crosshairs)
2. Upload the selection to `~/.cache/claude-images/` on devbox
3. Copy the remote path to your clipboard

Then in your SSH session with Claude Code:
```
Analyze this image: /home/dev/.cache/claude-images/screenshot-20240115-143022-12345-67890.png
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DEVBOX_HOST` | `devbox` | SSH host alias |
| `SCREENSHOT_REMOTE_DIR` | `~/.cache/claude-images` | Remote directory for uploads |

## How It Works

The script:
1. Uses `screencapture -i -x` to capture a selection silently
2. Generates a unique filename with timestamp and PID
3. Creates the remote directory with 700 permissions
4. Uploads via `scp` and sets 600 permissions on the file
5. Copies the remote path to clipboard via `pbcopy`

## Troubleshooting

**"Screenshot cancelled"**: You pressed Escape or clicked outside the selection. This is expected behavior.

**SSH connection fails**: Ensure your `devbox` host alias is configured in `~/.ssh/config` and SSH keys are set up.

**Permission denied on remote**: The script creates directories with `umask 077` and files with 600 permissions. If the parent directory has issues, check `~/.cache` permissions.

## Why Not Just Use iTerm2's it2ul?

iTerm2's `it2ul` upload tool can be flaky inside tmux (proprietary escape sequences don't always pass through cleanly for large files). This script uses standard `scp` which works reliably through any tmux session.

## Related

- [OSC 52 Clipboard](../osc52-clipboard/SKILL.md) - For text copy/paste over SSH
