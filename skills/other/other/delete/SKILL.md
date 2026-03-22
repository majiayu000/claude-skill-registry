---
name: delete
description: Use when removing a Feishu document by token and cleaning the matching entry from local obshare-cli upload history.
---

# obshare-cli delete

Delete a Feishu document by token.

## Syntax

```bash
conda run -n obsd obshare-cli delete <token>
conda run -n obsd obshare-cli --json delete <token>
```

## Example

```bash
conda run -n obsd obshare-cli delete doxcnAbcDefGhi
conda run -n obsd obshare-cli --json delete doxcnAbcDefGhi
```

## Notes

- Use a document token from upload output or `obshare-cli list history`.
- Deleting also removes the matching record from `~/.obshare/history.json`.
- `--json` is a global flag and must appear before `delete`.
