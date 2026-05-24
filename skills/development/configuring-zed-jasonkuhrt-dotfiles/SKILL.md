---
name: configuring-zed
description: Provides guidance for configuring and customizing the Zed editor. Use when modifying Zed settings, keybindings, themes, or extensions.
---

# Configuring Zed

## Configuration Paths

| File                          | Purpose                |
| ----------------------------- | ---------------------- |
| `~/.config/zed/settings.json` | Global settings        |
| `~/.config/zed/keymap.json`   | Custom keybindings     |
| `.zed/settings.json`          | Project-local settings |

## Rules

* Modify global config (`~/.config/zed/`) unless project-specific override is requested
* Zed uses JSONC (JSON with comments) for config files
* Settings are merged: project settings override global settings

## Common Tasks

### Adding a keybinding

```jsonc
// ~/.config/zed/keymap.json
[
  {
    "context": "Editor",
    "bindings": {
      "cmd-shift-l": "editor::SelectAllMatches"
    }
  }
]
```

### Configuring language settings

```jsonc
// ~/.config/zed/settings.json
{
  "languages": {
    "TypeScript": {
      "tab_size": 2,
      "formatter": "language_server"
    }
  }
}
```
