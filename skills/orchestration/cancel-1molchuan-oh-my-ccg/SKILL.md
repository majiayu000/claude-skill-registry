---
name: cancel
description: 取消当前活跃的 oh-my-ccg 模式
---

# Cancel Active Modes

Cancel all active oh-my-ccg orchestration modes.

## Steps

1. Read all state files in `.oh-my-ccg/state/`:
   - `ralph-state.json`
   - `team-state.json`
   - `autopilot-state.json`

2. For each active mode:
   - Set `active: false`
   - Record cancellation timestamp
   - Save updated state

3. If Team mode was active:
   - Send shutdown_request to all teammates
   - Wait for acknowledgments
   - Clean up team resources

4. Report what was cancelled:
```
Cancelled modes:
  ✅ Ralph (was at iteration 3/10)
  ✅ Team (was running with 3 workers)
  — Autopilot was not active
```

5. Note: RPI state is preserved (not cancelled). Use `/oh-my-ccg:init` to reset RPI state.

## Force Mode
If `--force` flag is present, delete all state files completely rather than marking inactive.
