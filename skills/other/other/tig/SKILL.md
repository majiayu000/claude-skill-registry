---
name: tig
description: tig text-mode git interface. Use for git browsing.
---

# Tig

Tig is an ncurses-based text-mode interface for git. It functions mainly as a Git repository browser.

## When to Use

- **Log Browsing**: `tig` shows the commit graph beautifully in the terminal.
- **Blame**: `tig blame file.txt` is faster than any GUI.
- **Staging**: `tig status` allows staging files quickly.

## Core Concepts

### Views

- **Main**: Commit graph.
- **Diff**: View changes.
- **Blame**: Who changed what.

### Navigation

Vim-like bindings (`j`, `k`) to scroll. `Enter` to drill down.

## Best Practices (2025)

**Do**:

- **Use as Pager**: Set `git config --global core.pager "tig"` (optional, but powerful).
- **Quick Blame**: Use it to find who broke the build in seconds.

**Don't**:

- **Don't use for complex writes**: Lazygit is better for rebasing/ops. Tig is better for reading.

## References

- [Tig Documentation](https://jonas.github.io/tig/)
