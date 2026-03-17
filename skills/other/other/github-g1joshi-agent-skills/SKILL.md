---
name: github
description: GitHub platform with Actions, Copilot, and code review. Use for collaboration.
---

# GitHub (Tool)

Beyond the platform, GitHub provides powerful **CLI tools (`gh`)** and **Desktop** apps that streamline workflows.

## When to Use

- **PR Management**: `gh pr create`, `gh pr checkout`.
- **CLI**: Scripting GitHub Actions or releases.
- **Copilot**: Managing AI settings.

## Core Concepts

### GitHub CLI (`gh`)

The official CLI.
`gh repo create my-new-repo --public --clone`

### Codespaces

Cloud dev environment. `gh codespace create`.

### Gists

Code snippets. `gh gist create file.txt`.

## Best Practices (2025)

**Do**:

- **Use `gh dash`**: A dashboard extension for the CLI to view PRs/Issues.
- **Use `gh copilot`**: CLI interface for Copilot ("Explain this command").

**Don't**:

- **Don't use password auth**: It's disabled. Use PAT or SSH.

## References

- [GitHub CLI Manual](https://cli.github.com/manual/)
