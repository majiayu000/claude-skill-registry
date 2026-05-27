---
name: cancel-ultraqa
description: Cancel active UltraQA cycling workflow
user-invocable: true
---

# Cancel UltraQA

[ULTRAQA CANCELLED]

The UltraQA cycling workflow has been cancelled. Clearing state file.

## MANDATORY ACTION

Execute this command to cancel UltraQA:

```bash
mkdir -p .sisyphus && echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ultraqa"}' > .omc/ultraqa-state.json
```

After running this command, the QA cycling will stop.

## To Start Fresh

- `/ultraqa --tests` - Run until all tests pass
- `/ultraqa --build` - Run until build succeeds
- `/ultraqa --lint` - Run until no lint errors
- `/ultraqa --typecheck` - Run until no type errors
- `/ultraqa --custom "pattern"` - Run until pattern matches
