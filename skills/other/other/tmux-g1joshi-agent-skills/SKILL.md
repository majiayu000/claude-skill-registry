---
name: tmux
description: tmux terminal multiplexer. Use for terminal sessions.
---

# Tmux

Tmux decouples your terminal session from the window. Detach, go home, SSH in, attach, and your cursor is exactly where you left it. v3.5 adds extended keys.

## When to Use

- **Remote Work**: Mandatory for SSH. If connection drops, your run continues.
- **Pair Programming**: Two users can attach to the same session.
- **Layouts**: Run Editor, Server, and Logs in one window.

## Core Concepts

### Session / Window / Pane

Hierarchy: Session > Windows (Tabs) > Panes (Splits).

### Prefix Key

Default `Ctrl+b`. Most users remap to `Ctrl+a`.

### Plugins (TPM)

Tmux Plugin Manager. `tmux-resurrect` saves state across reboots.

## Best Practices (2025)

**Do**:

- **Use True Color**: Ensure `termguicolors` works in Vim inside Tmux.
- **Use `tmux-sensible`**: Sets sane defaults (utf8, history limit).
- **Script Layouts**: Use `tmuxinator` to launch standard workspace layouts.

**Don't**:

- **Don't nest tmux**: Running tmux inside tmux is a path to madness.

## References

- [Tmux Wiki](https://github.com/tmux/tmux/wiki)
