---
name: cancel-ultrawork
description: Cancel active Ultrawork mode
user-invocable: true
---

# Cancel Ultrawork

[ULTRAWORK CANCELLED]

The Ultrawork mode has been cancelled. Clearing state files.

## MANDATORY ACTION

**First**, check if ultrawork is linked to an active Ralph loop:

```bash
cat .omc/ultrawork-state.json 2>/dev/null | jq -r '.linked_to_ralph // false'
```

**If linked_to_ralph is true**: Use `/cancel-ralph` instead to cancel both Ralph and its linked Ultrawork.

**Otherwise**, execute this command to cancel Ultrawork:

```bash
mkdir -p .omc && \
echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ultrawork"}' > .omc/ultrawork-state.json && \
echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ultrawork"}' > ~/.claude/ultrawork-state.json
```

After running this command, ultrawork mode will be deactivated and the HUD will update.

## Note on Linked Modes

Since v3.0, Ralph automatically activates Ultrawork. If you see `linked_to_ralph: true` in the ultrawork state, it means Ultrawork was auto-activated by Ralph. In this case:
- Use `/cancel-ralph` to cancel both modes
- If you only cancel ultrawork, Ralph will continue but without parallel execution benefits

## To Start Fresh

- `/ultrawork "task"` - Start ultrawork only (standalone)
- `/ralph "task"` - Start ralph with ultrawork (default)
