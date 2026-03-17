---
name: zsh
description: Zsh shell with oh-my-zsh. Use for terminal shell.
---

# Zsh

Zsh is the default shell on macOS. It is highly customizable and compatible with Bash.

## When to Use

- **macOS**: It's the default.
- **Customization**: The plugin ecosystem (`omz`, `zinit`) is massive.
- **Compatibility**: Runs most Bash scripts unmodified.

## Core Concepts

### Oh My Zsh (OMZ)

The community framework. 300+ plugins.
`plugins=(git docker kubectl)`

### Globbing

Zsh has powerful wildcard matching. `ls **/*.js` (Recursive).

### Themes

`Powerlevel10k` is the gold standard for performance and information density.

## Best Practices (2025)

**Do**:

- **Use a Fast Plugin Manager**: `antidote` or `sheldon` are faster than OMZ's built-in loader.
- **Enable Autosuggestions**: The `zsh-autosuggestions` plugin brings Fish-like behavior to Zsh.
- **Use Syntax Highlighting**: `zsh-syntax-highlighting`.

**Don't**:

- **Don't over-clutter prompt**: A prompt that takes 200ms to render makes the terminal feel sluggish.

## References

- [Zsh Documentation](https://zsh.sourceforge.io/Doc/Release/index.html)
