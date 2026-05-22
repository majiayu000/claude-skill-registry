---
name: env-update-secrets
description: Use when updating environment secrets like GITHUB_TOKEN, NPM_TOKEN, or API keys on the user's machine
---

# Updating Environment Secrets

## Location

All secrets live in: `~/.config/fish/config.secrets.fish`

This file is sourced by `~/.config/fish/config.fish` on shell startup.

## Format

```fish
export VAR_NAME='value'
```

## Current Secrets

| Variable | Purpose |
|----------|---------|
| `GITHUB_TOKEN` | GitHub CLI and API authentication |
| `NPM_TOKEN` | npm registry authentication |
| `NPM_PUBLISH_TOKEN` | npm package publishing |

## Workflow

1. Read `~/.config/fish/config.secrets.fish`
2. Edit the relevant `export` line with new value
3. Tell user to reload: `source ~/.config/fish/config.fish`

## Adding New Secrets

Add new `export` lines to the same file. Keep secrets consolidated here rather than scattered across dotfiles.
