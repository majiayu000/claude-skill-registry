---
name: fix-line-endings-check-bash
description: Fix line endings AND check bash syntax in one step (recommended). Use after creating or editing bash scripts.
allowed-tools: Bash
---

# Fix Line Endings + Check Bash

**Recommended tool** for bash script preparation.

```bash
.claude/skills/fix-line-endings-check-bash/scripts/fix-line-endings-check-bash.sh script1.sh script2.sh
```

Converts CRLF→LF, then validates syntax. Stops on first failure.
