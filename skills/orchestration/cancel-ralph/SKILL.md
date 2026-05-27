---
name: cancel-ralph
description: Cancel active Ralph (and linked ultrawork if auto-activated)
user-invocable: true
---

# Cancel Ralph

[RALPH CANCELLED]

Ralph has been cancelled. You MUST now deactivate the state files.

## MANDATORY ACTION

Execute this command to fully cancel ALL persistent modes:

```bash
mkdir -p .omc ~/.claude && \
echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ralph"}' > .omc/ralph-state.json && \
echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ralph", "linked_to_ralph": false}' > .omc/ultrawork-state.json && \
echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ralph"}' > .omc/ralph-plan-state.json && \
echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ralph"}' > ~/.claude/ralph-state.json && \
echo '{"active": false, "cancelled_at": "'$(date -Iseconds)'", "reason": "User cancelled via /cancel-ralph"}' > ~/.claude/ultrawork-state.json && \
rm -f .omc/ralph-verification.json
```

After running this command, you are free to stop working. The persistent mode hook will no longer force continuation.

## What Was Cancelled

- **Ralph**: Self-referential completion loop
- **Ultrawork**: Parallel execution mode (auto-activated with Ralph by default)
- **Ralph Plan**: Iterative planning loop (if active via /ralplan)
- **Verification State**: Any pending architect verification

## Note on Linked Modes

Since v3.0, Ralph automatically activates Ultrawork for parallel execution. When you cancel Ralph, the linked Ultrawork is also cancelled. If you started Ultrawork separately (not via Ralph), use `/cancel-ultrawork` to cancel it independently.

## To Start Fresh

- `/ralph "task"` - Start ralph with ultrawork (default)
- `/ultrawork "task"` - Start ultrawork only (standalone)
