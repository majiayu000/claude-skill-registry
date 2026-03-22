---
name: obshare-cli
description: Use when setting up obshare-cli 0.2.0, reviewing available commands, or choosing the right command for config, upload, permission, history, delete, and the plugin-first direct-share workflow.
---

# obshare-cli

`obshare-cli` uploads Markdown documents to Feishu and keeps local upload history. In `V0.2.0`, the Obsidian companion plugin is the primary direct-share UI, while the CLI remains the execution backend. The recommended runtime for this stack is the `obsd` conda environment.

## Setup

```bash
conda create -n obsd python -y
conda run -n obsd python -m pip install --upgrade pip
conda run -n obsd python -m pip install --upgrade obshare-cli
conda run -n obsd obshare-cli --version
conda run -n obsd obshare-cli --help
```

## Global Options

| Option | Purpose |
|--------|---------|
| `--json` | Return machine-friendly JSON output |
| `--debug` | Enable debug logging |
| `--version` | Show installed version |

`--json` and `--debug` are global flags. Put them before the command, for example `obshare-cli --json config show`.

## Commands

| Command | Purpose |
|---------|---------|
| `config` | Save credentials and optional Obsidian bridge settings |
| `upload` | Upload a Markdown file to Feishu |
| `permission` | Change document sharing permissions |
| `list` | Show local upload history |
| `delete` | Delete a document by token |

## Quick Start

```bash
conda run -n obsd obshare-cli config set-app-id "cli_xxx"
conda run -n obsd obshare-cli config set-app-secret "xxx"
conda run -n obsd obshare-cli config set-user-id "ou_xxx"
conda run -n obsd obshare-cli config set-folder "fldcnxxx"
conda run -n obsd obshare-cli config test
conda run -n obsd obshare-cli upload note.md
conda run -n obsd obshare-cli list history
```

## Optional Obsidian Bridge

If you use the companion Obsidian plugin, also set:

```bash
conda run -n obsd obshare-cli config set-obsidian-cli obsidian
conda run -n obsd obshare-cli config set-obsidian-bridge-dir /path/to/shared/bridge
conda run -n obsd obshare-cli config set-obsidian-command-id obshare-cli:process-render-request
```
