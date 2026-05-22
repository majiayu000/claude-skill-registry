---
name: commit-protocol
version: 1.0
triggers: ["commit", "git"]
---

# Commit Protocol SKILL

## USER_APPROVED Pattern

```bash
# CORRECT
USER_APPROVED=yes git commit -m "feat: Add hybrid search"

# WRONG
git commit -m "feat: Add hybrid search"
```

## Commit Format

```
<type>: <description>

Types: feat, fix, docs, test, refactor
```

**Simplified from:** WHRESUME (feature branches removed)
