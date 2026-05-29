---
name: rsls-fix
description: Fix errors caused by corrupted rsls* files. Use when any operation fails mentioning rsls* files (e.g., "bad object *.rslsc", "missing *.rslsd", file not found *.rsls*).
---

# rsls* File Fix

When any operation fails with errors mentioning `rsls*` files (e.g., `*.rslsc`, `*.rslsd`, `*.rslsa`), these are corrupted/temporary files that should be deleted.

## Error Patterns

- `bad object refs/heads/<name>.rsls*`
- `fatal: <path>.rsls*`
- `No such file or directory: <path>.rsls*`
- Any error containing `.rsls` in a filename

## Fix

Delete the corrupted file mentioned in the error:

```bash
# Remove the specific file from the error message
rm <path-from-error>

# Or find and remove all rsls* files in a directory
find <directory> -name '*.rsls*' -delete
```

Then retry the failed operation.

## MUST DO

- Delete `rsls*` files without prompting - they are always safe to remove
- Extract the exact path from the error message
- Retry the failed operation after cleanup
