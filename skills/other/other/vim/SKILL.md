---
name: vim
description: Vim text editor with motions, macros, and plugins. Use for terminal editing.
---

# Vim

Vim is the universal text editor installed on every UNIX system. While Neovim innovates, Vim focuses on backward compatibility and stability.

## When to Use

- **SSH / Servers**: It is _always_ there. `vi` usually aliases to `vim`.
- **Stability**: Scripts written in 2005 still work.
- **Resource Constraints**: Runs on embedded routers.

## Core Concepts

### Modes

- **Normal**: Navigation (`hjkl`).
- **Insert**: Typing (`i`, `a`).
- **Visual**: Selection (`v`).
- **Command**: Ex commands (`:w`, `:q`).

### Composability

Operator + Motion = Action.
`d` (delete) + `w` (word) = `dw`.
`c` (change) + `i` (inside) + `"` (quote) = `ci"`.

## Best Practices (2025)

**Do**:

- **Learn the Basics**: `vimtutor` is mandatory for every developer.
- **Use `.vimrc`**: Keep a minimal config for servers (line numbers, syntax on).
- **Use Neovim for IDE**: For daily coding, Neovim is preferred. Use Vim for quick edits.

**Don't**:

- **Don't use arrow keys**: Force yourself to use `hjkl`.

## References

- [Vim Documentation](https://www.vim.org/docs.php)
