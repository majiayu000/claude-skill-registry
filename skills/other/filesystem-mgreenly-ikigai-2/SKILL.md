---
name: security/filesystem
description: Filesystem Security security skill
---

# Filesystem Security

File operations have race conditions, symlink attacks, and path traversal risks.

## ikigai Application

**Path traversal:**
- Reject paths containing `..` before canonicalization
- Use `realpath()` and verify result is under allowed directory
- Never concatenate user input directly into paths

**TOCTOU (Time-of-Check to Time-of-Use):**
```c
// BAD: Race between check and use
if (access(path, R_OK) == 0) { fd = open(path, O_RDONLY); }

// GOOD: Open first, then check
fd = open(path, O_RDONLY);
if (fd >= 0) { /* use fd */ }
```

**Symlink attacks:**
- Use `O_NOFOLLOW` when opening files in shared directories
- `lstat()` to check for symlinks before operations
- Create temp files with `mkstemp()`, never `mktemp()`

**Permissions:**
- Config files: `0600` (owner read/write only)
- Directories: `0700`
- Check permissions before reading sensitive files
- Set umask appropriately: `umask(077)`

**Review red flags:** `access()` before `open()`, path concatenation, missing `O_NOFOLLOW`, world-readable configs.
