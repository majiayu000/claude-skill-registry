---
name: lazygit
description: lazygit terminal UI for git. Use for git operations.
---

# Lazygit

Lazygit is a TUI for Git. It makes complex operations (interactive rebase, partial staging) accessible via intuitive keyboard shortcuts.

## When to Use

- **Staging**: Staging individual lines/hunks (`Space`).
- **Rebasing**: Drag-and-drop commits to reorder them (via keybindings).
- **Conflict Resolution**: A clear 3-way view to pick "Ours" or "Theirs".

## Core Concepts

### Panels

Status, Files, Local Branches, Commits, Stash. Navigate with `h/l` or arrows.

### Keybindings

- `c`: Commit
- `P`: Push
- `p`: Pull
- `s`: Stage

### Custom Commands

Define custom actions in `config.yml` (e.g. "Create PR").

## Best Practices (2025)

**Do**:

- **Interactive Rebase**: Press `i` on a past commit to fix it up.
- **Filter**: Press `/` to filter branches or files.
- **Bisect**: Use the built-in bisect wizard to find bugs.

**Don't**:

- **Don't fear the CLI**: Lazygit is a wrapper. Understanding underlying git concepts is still needed.

## References

- [Lazygit GitHub](https://github.com/jesseduffield/lazygit)
