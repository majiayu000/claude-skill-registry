---
name: vscode
description: Visual Studio Code editor with extensions and debugging. Use for code editing.
---

# Visual Studio Code

VS Code is the industry standard editor. In 2025, it has evolved into an **AI-First** editor with a native AI Companion and generic **Agent Mode**.

## When to Use

- **Everyday Coding**: TypeScript, Python, Go, Rust. It wins almost everywhere.
- **Remote Dev**: `Remote - SSH` and `Dev Containers` are best-in-class.
- **AI-Assisted**: GitHub Copilot integration is deepest here.

## Quick Start

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "files.autoSave": "onFocusChange"
}
```

## Core Concepts

### Extensions

The ecosystem is the key. 50k+ extensions.

- `Python` (Microsoft)
- `ESLint` (Microsoft)
- `GitLens`

### Dev Containers

Define your dev environment in `.devcontainer/devcontainer.json`. VS Code spins up a Docker container and connects to it. 100% reproducible dev environments.

### Profiles (2025)

Switch between "Work", "Personal", and "Demo" profiles with different settings/extensions enabled.

## Best Practices (2025)

**Do**:

- **Use Sync**: Turn on Settings Sync (`GitHub` account) to keep keybindings across machines.
- **Use `code .`**: Launch from terminal.
- **Use Inline Chat**: `Cmd+I` to ask Copilot to refactor code in-place.

**Don't**:

- **Don't minimalize too much**: Hiding the sidebar/activity bar makes you slower. Learn the toggle shortcuts (`Cmd+B`) instead.

## References

- [VS Code Documentation](https://code.visualstudio.com/docs)
