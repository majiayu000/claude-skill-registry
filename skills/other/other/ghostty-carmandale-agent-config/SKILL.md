---
name: ghostty
description: "Control Ghostty terminal emulator via CLI. Manage windows, tabs, splits, and configuration."
---

# Ghostty Skill

Use the `ghostty` CLI to control and configure the Ghostty terminal emulator.

## CLI Location

```bash
/Applications/Ghostty.app/Contents/MacOS/ghostty
```

Or if symlinked: `ghostty`

## Actions (IPC Commands)

Ghostty supports actions via `+action` flag. These control the running instance.

List available actions:
```bash
ghostty +list-actions
```

Create new window:
```bash
ghostty +new-window
```

Create new tab:
```bash
ghostty +new-tab
```

Create splits:
```bash
ghostty +new-split:right
ghostty +new-split:down
```

Navigate splits:
```bash
ghostty +goto-split:previous
ghostty +goto-split:next
ghostty +goto-split:up
ghostty +goto-split:down
ghostty +goto-split:left
ghostty +goto-split:right
```

Close current surface:
```bash
ghostty +close-surface
```

Toggle fullscreen:
```bash
ghostty +toggle-fullscreen
```

Reload configuration:
```bash
ghostty +reload-config
```

## Font Management

Increase/decrease font size:
```bash
ghostty +increase-font-size:1
ghostty +decrease-font-size:1
```

Reset font size:
```bash
ghostty +reset-font-size
```

## Configuration

Config file location:
```
~/.config/ghostty/config
```

Show current config:
```bash
ghostty +show-config
```

List available themes:
```bash
ghostty +list-themes
```

List available fonts:
```bash
ghostty +list-fonts
```

List keybinds:
```bash
ghostty +list-keybinds
```

## Launch Options

Start with specific config:
```bash
ghostty --config-file=/path/to/config
```

Start with command:
```bash
ghostty -e "htop"
```

Start in directory:
```bash
ghostty --working-directory=/path/to/dir
```

## Debugging

Check version:
```bash
ghostty --version
```

Validate config:
```bash
ghostty +validate-config
```
