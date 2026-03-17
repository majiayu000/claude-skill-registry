---
name: fish
description: Fish friendly interactive shell. Use for terminal shell.
---

# Fish (Friendly Interactive Shell)

Fish v4.0 (2025) is rewritten in **Rust**. It is famous for "It just works" – 90% of what you need (autosuggestions, coloring) is enabled by default.

## When to Use

- **Interactive Use**: It is arguably the best shell for _typing_ commands manually.
- **Discoverability**: Man page completions are generated automatically.

## Core Concepts

### Autosuggestions

Fish suggests commands as you type based on history and completions. Right arrow accepts.

### Universal Variables

`set -U my_var value` sets a variable across _all_ current and future shell instances instantly.

### Web Config

`fish_config` launches a browser UI to change colors and prompt.

## Best Practices (2025)

**Do**:

- **Use it as Interactive Shell**: Set it as your login shell.
- **Don't write scripts in Fish**: Write scripts in `bash` or `sh` for portability. Run them _from_ Fish.
- **Use "Fisher"**: The plugin manager for themes.

**Don't**:

- **Don't copy-paste Bash**: Fish syntax is different (`env var=val` -> `set -x var val`).

## References

- [Fish Shell Documentation](https://fishshell.com/docs/current/index.html)
