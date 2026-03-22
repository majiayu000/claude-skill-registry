---
name: permission
description: Use when changing Feishu document visibility, copy permissions, or download permissions for an uploaded document token.
---

# obshare-cli permission

Adjust sharing permissions for an existing Feishu document.

## Available Subcommand

| Command | Purpose |
|---------|---------|
| `set <token>` | Update sharing flags for one document |

## Syntax

```bash
conda run -n obsd obshare-cli permission set <token> [--public] [--allow-copy] [--allow-download]
conda run -n obsd obshare-cli --json permission set <token> [--public] [--allow-copy] [--allow-download]
```

## Examples

```bash
conda run -n obsd obshare-cli permission set doxcnAbcDefGhi --public
conda run -n obsd obshare-cli permission set doxcnAbcDefGhi --allow-copy --allow-download
conda run -n obsd obshare-cli --json permission set doxcnAbcDefGhi --public --allow-copy
```

## Notes

- `--public` makes the document link-accessible.
- `--allow-copy` allows viewers to copy content.
- `--allow-download` allows download and create-copy behavior.
- Updated permission flags are also written back into local history when the token exists there.
