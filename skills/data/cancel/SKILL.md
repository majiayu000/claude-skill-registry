---
name: cancel
description: Cancel active Loop. Use when loop needs to stop early, done iterating manually, want to abort, or change direction. Triggers on "cancel loop", "stop iterating", "end loop", "terminate loop", "abort loop", "kill loop", "stop the loop", "halt". Graceful termination that preserves completed work.
model: haiku
allowed-tools: Read
---

# Cancel Loop

Gracefully terminate an active loop while preserving all completed work.

## When to Use

| Situation | Action |
|-----------|--------|
| **Need to change direction** | Cancel, then start new loop with updated spec |
| **Spec was wrong** | Cancel, clarify with `/hope:intent`, restart |
| **Good enough** | Cancel when partial progress is sufficient |
| **Taking too long** | Cancel to review approach before continuing |
| **Emergency stop** | Cancel immediately halts next iteration |

## Cancel vs Natural Completion

- **Natural completion:** Loop satisfied spec, clean exit with success summary
- **Cancel:** User-initiated stop, preserves progress, enables restart

Cancel when you want control back. Let it complete when spec is being satisfied.

## What Happens

1. **Read state** — Load `.loop/state.json`
2. **Set status** — Update status to `"cancelled"` in state file
3. **Find active task** — TaskList for in_progress task (subject starts with "Loop:")
4. **Mark terminated** — TaskUpdate status=completed with cancellation note
5. **Report state** — Iterations, cost, accomplished work, remaining items

Current iteration completes before cancel takes effect. No mid-operation interruption.

## State File Update (Required)

Update `.loop/state.json`:

```json
{
  "status": "cancelled",
  "exit_signal": false
}
```

This ensures the stop hook allows the cancellation to proceed.

## Output

```
Loop cancelled.

Completed: [N] iterations, $[X] cost
Accomplished:
- [list of completed steps]

Remaining:
- [list of incomplete steps]

Criteria status:
- [criterion 1]: ✓/✗
- [criterion 2]: ✓/✗

To restart: /loop [spec]
```

## Guarantees

- All completed work preserved (no rollback)
- State file updated to prevent resume
- Clean termination (no dangling state)
- Full accounting (iterations, cost, progress)
- Restart possible with same or modified spec
