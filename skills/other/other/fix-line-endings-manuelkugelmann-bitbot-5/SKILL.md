---
name: fix-line-endings
description: Fix CRLF (Windows) to LF (Unix) line endings in files. Use when encountering `/bin/bash: line 1: $'\r': command not found` errors.
---

# Fix Line Endings

Convert CRLF to LF line endings.

```bash
.claude/skills/fix-line-endings/scripts/fix-line-endings.sh file1.sh file2.sh
```

For combined fix + syntax check, use `fix-line-endings-check-bash` instead.
