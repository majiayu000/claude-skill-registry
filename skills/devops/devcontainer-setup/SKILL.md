---
name: devcontainer-setup
description:
  Create Universal DevContainers optimized for AI agentic workflows with Claude Code, Snowflake CLI,
  Cortex Code, and dbt. Use when setting up development containers, configuring devcontainer.json,
  scaffolding AI-ready environments, or when the user mentions devcontainers, containerized
  development, or Docker development environments.
---

# DevContainer Setup Skill

## When to Use

- User asks to set up a DevContainer or development environment
- User mentions AI-ready development setup
- Project needs containerized development with multiple language runtimes

## Instructions

### Step 1: Create directory structure

```bash
mkdir -p .devcontainer/snowflake-ai-tools
```

### Step 2: Copy templates

Copy these files from the skill templates folder:

| Source                                                   | Destination                                                  |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| `templates/devcontainer.json`                            | `.devcontainer/devcontainer.json`                            |
| `templates/snowflake-ai-tools/devcontainer-feature.json` | `.devcontainer/snowflake-ai-tools/devcontainer-feature.json` |
| `templates/snowflake-ai-tools/install.sh`                | `.devcontainer/snowflake-ai-tools/install.sh`                |

If no `requirements.txt` exists in project root, also copy:

| Source                       | Destination        |
| ---------------------------- | ------------------ |
| `templates/requirements.txt` | `requirements.txt` |

### Step 3: Make scripts executable

```bash
chmod +x .devcontainer/snowflake-ai-tools/install.sh
```

### Step 4: Remind user to create host directories

Run this on their host machine before opening the devcontainer:

```bash
mkdir -p ~/.m2 ~/.npm ~/.cache/uv ~/.cargo ~/.snowflake ~/.claude ~/.cursor
```

### Step 5: Remind user about config files

These should exist on the host:

- `~/.snowflake/connections.toml` - Snowflake CLI config
- `~/.claude/` - Claude Code config

## Template Locations

All templates are in this skill's `templates/` folder:

- [templates/devcontainer.json](templates/devcontainer.json)
- [templates/snowflake-ai-tools/](templates/snowflake-ai-tools/)
- [templates/requirements.txt](templates/requirements.txt)

## Troubleshooting

| Issue                      | Solution                                                                                  |
| -------------------------- | ----------------------------------------------------------------------------------------- |
| NPM EACCES errors          | `sudo chown -R $(whoami) "$HOME/.npm"`                                                    |
| UID mismatch on Linux      | Verify `updateRemoteUserUID: true` in devcontainer.json                                   |
| Cache permission issues    | Run `snowflake-ai-tools-setup` to re-fix permissions                                      |
| Mount directory not found  | Run `mkdir -p ~/.m2 ~/.npm ~/.cache/uv ~/.cargo ~/.snowflake ~/.claude ~/.cursor` on host |
| Tools not found            | Check Docker build logs for install errors                                                |
| Different user than vscode | Update mount targets and containerEnv paths in devcontainer.json                          |

## Reference

See [README.md](README.md) for detailed documentation on:

- What's included (features, tools, mounts)
- Compatibility (base images, architectures)
- Python environment setup
