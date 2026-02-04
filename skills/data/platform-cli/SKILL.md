---
name: platform-cli
description: "Design and implementation patterns for building command-line tools with modern UX conventions. Use when: (1) designing a new CLI tool, (2) reviewing CLI UX and behavior, (3) defining commands, flags, or help text, (4) implementing error handling or signal handling, (5) planning CLI distribution."
---

# CLI Development Patterns

Modern CLI design patterns for commands, flags, output, errors, signals, config, and distribution.

## References

See [references/cli-patterns.md](references/cli-patterns.md) for comprehensive guidance organized by:

- **Design & Naming** - Command structure, naming conventions, future-proofing
- **Flags & Arguments** - Standard flags, short forms, boolean negation
- **Output & Formatting** - stdout/stderr, TTY detection, colors, machine-readable formats
- **Error Handling** - Exit codes, error messages, signal-to-noise ratio
- **Signals & Lifecycle** - Ctrl-C handling, cleanup timeouts
- **Environment & Config** - Standard variables, precedence, naming
- **Distribution & Packaging** - Single binary distribution, uninstall instructions
- **Security & Privacy** - Secret handling, telemetry consent
