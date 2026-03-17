---
name: warp
description: Warp modern terminal with AI. Use for terminal work.
---

# Warp

Warp is a modern, Rust-based terminal that works like a text editor. In 2025, it positions itself as an **Agentic Development Environment** for the CLI.

## When to Use

- **Productivity**: Input area works like an IDE (selection, cursor).
- **Teamwork**: Share "Blocks" (command + output) with a link.
- **AI**: Built-in "Warp AI" can explain errors or generate commands ("How do I undo the last git commit?").

## Core Concepts

### Blocks

Warp groups command and output into a visual block. You can navigate block-by-block, not character-by-character.

### Workflows

Save parameterized commands.
`npm run build --env={{env}}`

### Warp Drive

Cloud-synced configurations and workflows.

## Best Practices (2025)

**Do**:

- **Use AI Command Search**: Press `#` and type natural language to generate a command.
- **Use Workflows**: Don't memorize complex kubectl commands. Save them.
- **Enable "Notebook Mode"**: For a literate programming experience in the shell.

**Don't**:

- **Don't use for SSH (Legacy)**: Warp has its own "Warp SSH" wrapper to maintain features on remote servers. Use it instead of plain `ssh`.

## References

- [Warp Documentation](https://docs.warp.dev/)
