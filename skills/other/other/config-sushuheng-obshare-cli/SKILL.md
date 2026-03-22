---
name: config
description: Use when configuring obshare-cli credentials, checking saved settings, testing connectivity, clearing local config, or setting optional Obsidian bridge values used by the V0.2.0 direct-share stack.
---

# obshare-cli config

Manage saved configuration for Feishu uploads and optional Obsidian bridge integration. These settings are consumed by both the CLI and the Obsidian companion plugin's direct-share flow in `V0.2.0`.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `set-app-id <app_id>` | Save Feishu App ID |
| `set-app-secret <app_secret>` | Save Feishu App Secret |
| `set-user-id <user_id>` | Save Feishu user ID |
| `set-folder <folder_token>` | Save target folder token |
| `set-obsidian-cli <command>` | Save Obsidian CLI command name/path |
| `set-obsidian-bridge-dir <dir>` | Save shared bridge directory |
| `set-obsidian-command-id <id>` | Save Obsidian render command ID |
| `show` | Show current config with sensitive values masked |
| `test` | Test Feishu connectivity |
| `clear` | Remove saved local config |

## Common Usage

```bash
# Required Feishu settings
conda run -n obsd obshare-cli config set-app-id "cli_xxx"
conda run -n obsd obshare-cli config set-app-secret "xxx"
conda run -n obsd obshare-cli config set-user-id "ou_xxx"
conda run -n obsd obshare-cli config set-folder "fldcnxxx"

# Optional Obsidian bridge settings for Mermaid rendering
conda run -n obsd obshare-cli config set-obsidian-cli obsidian
conda run -n obsd obshare-cli config set-obsidian-bridge-dir /path/to/shared/bridge
conda run -n obsd obshare-cli config set-obsidian-command-id obshare-cli:process-render-request

# Inspect and test
conda run -n obsd obshare-cli config show
conda run -n obsd obshare-cli --json config show
conda run -n obsd obshare-cli config test
```

## Notes

- Uploads require `app_id`, `app_secret`, `user_id`, and `folder_token`.
- Config is stored in `~/.obshare/config.json`.
- Sensitive fields are stored encrypted when cryptography support is available.
- `--json` is a global option: place it before the subcommand, not after `show` or `test`.
