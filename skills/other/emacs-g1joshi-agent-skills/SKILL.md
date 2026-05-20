---
name: emacs
description: Emacs extensible text editor with Lisp. Use for terminal editing.
---

# GNU Emacs

Emacs is an operating system masquerading as an editor. v29+ (2025) features built-in **Eglot** (LSP), **Tree-sitter**, and **Native Compilation** for speed.

## When to Use

- **Lisp Hackers**: Configured in Elisp.
- **Org Mode**: The best note-taking/GTD system in existence.
- **Magit**: The best Git interface ever made.

## Core Concepts

### Buffers & Windows

Everything is a buffer (files, terminals, games). Windows display buffers.

### Key Chords

`C-x C-s` (Save). `M-x` (Execute command).
Emacs relies heavily on `Ctrl` and `Meta` (Alt/Option).

### Org Mode

Structured plain text. Todos, tables, code execution (Babel).

## Best Practices (2025)

**Do**:

- **Use `use-package`**: The standard macro for tidy configuration.
- **Enable Native Comp**: `(setq native-comp-async-report-warnings-errors nil)`. Massive speedup.
- **Try Doom Emacs**: A pre-configured distribution optimized for Vimmers (Evil mode).

**Don't**:

- **Don't fear the pinky**: Remap `Caps Lock` to `Ctrl` immediately.

## References

- [GNU Emacs Manual](https://www.gnu.org/software/emacs/manual/)
