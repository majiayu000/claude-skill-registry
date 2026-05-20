---
name: list
description: Use when checking obshare-cli upload history, finding document tokens, or reviewing previous upload URLs and permission snapshots.
---

# obshare-cli list

Inspect locally saved upload history.

## Available Subcommand

| Command | Purpose |
|---------|---------|
| `history` | Show previous uploads saved in local history |

## Syntax

```bash
conda run -n obsd obshare-cli list history
conda run -n obsd obshare-cli --json list history
```

## What History Contains

- Document title
- Feishu document token
- Feishu document URL
- Upload time
- Saved permission flags

## Notes

- History is stored in `~/.obshare/history.json`.
- Use tokens from this output with `permission set` or `delete`.
- `--json` is a global flag and must appear before `list`.
