---
name: close
description: "Close task in tracker. Use when the user invokes /close or asks to close a tracker issue."
---

# Close Command

Follow `CLAUDE.md`, `conventions.md`, and `ARCHITECTURE.md`.

## Task

Close a task in tracker.

## Interaction Contract

| Phase | Action | STOP until | Steps |
|-------|--------|------------|-------|
| 1. Find task | Locate task | - | 1-2 |
| 2. Confirm | Show what will be closed | User says "da" / "ok" / "yes" | 3 |
| 3. Execute | Close in tracker | - | 4-5 |

Closing without phase 2 confirmation is a critical violation.

## Algorithm

1. **Check arguments:**
   - If empty: ask "Which task to close? Provide task ID."
   - Otherwise: use as task ID

2. **Normalize task ID:**
   - If ID does not contain prefix "DCATgBot-": add prefix
   - Store normalized ID as `<full_id>`
   - Store short ID (without prefix) as `<short_id>`

3. **Confirm with user:**
   - Show task ID to close
   - Wait for confirmation

4. **Close task in tracker:**
   - Use `beads` to close task with reason "Completed"
   - If not found/already closed: report and stop

5. **Report result:**
   ```
   Task closed: <full_id>
   ```

## Error Handling

- Task not found: report and stop
- Task already closed: report and stop
