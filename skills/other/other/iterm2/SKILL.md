---
name: iterm2
description: iTerm2 macOS terminal emulator. Use for terminal work.
---

# iTerm2

iTerm2 is the power-user terminal for Mac. v3.5/3.6 (2025) adds **AI Integration** (OpenAI key) and a built-in **Web Browser** panel.

## When to Use

- **macOS Power User**: Split panes, hotkey window (Quake style), search.
- **Remote Integration**: Shell integration allows downloading files via drag-drop from SSH.

## Core Concepts

### Profiles

Define colors, fonts, and keyboard behavior per environment.

### Triggers

Regex that watches output and performs actions (e.g., highlight "Error", run a script, ring incomplete).

### Tmux Integration

`tmux -CC` makes remote tmux sessions appear as native iTerm2 windows/tabs.

## Best Practices (2025)

**Do**:

- **Use Shell Integration**: Install it to enable features like "Status Bar" on the prompt line.
- **Use "Composer"**: Like Warp, iTerm2 has an input composer window (`Cmd+Shift+C`).
- **Map Option to Meta**: Ensure `Option` key acts as `Esc+` for proper Emacs/Vim navigation.

**Don't**:

- **Don't ignore the GPU renderer**: Enable Metal renderer for performance.

## References

- [iTerm2 Documentation](https://iterm2.com/documentation.html)
