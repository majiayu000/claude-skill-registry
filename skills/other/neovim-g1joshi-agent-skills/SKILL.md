---
name: neovim
description: Neovim modern Vim fork with Lua plugins and LSP. Use for extensible terminal editing.
---

# Neovim

Neovim is the future of Vim. v0.11 (2025) brings built-in completion, enhanced LSP, and mature Tree-sitter integration.

## When to Use

- **Keyboard Centric**: You never want to touch the mouse.
- **Speed**: You want an editor that starts in 20ms.
- **Customization**: You want to build your _own_ editor using Lua.

## Core Concepts

### Lua Config (`init.lua`)

Configuration is code. Modules, loops, conditionals.
`vim.opt.number = true`

### LSP (Language Server Protocol)

Built-in client. Connects to `pyright`, `tsserver`, `rust-analyzer` natively.

### Tree-sitter

Parsing library for syntax highlighting. Understanding code structure (AST), not just Regex.

## Best Practices (2025)

**Do**:

- **Use a Distro** (Optional): LazyVim, AstroNvim, or NvChad are great starting points for 2025.
- **Use `lazy.nvim`**: The standard plugin manager.
- **Use Built-ins**: v0.11 has many features (commenting, diagnostics) that used to need plugins. Check `:help news`.

**Don't**:

- **Don't copy huge configs**: Understand every line you add to `init.lua`.

## References

- [Neovim Documentation](https://neovim.io/doc/)
