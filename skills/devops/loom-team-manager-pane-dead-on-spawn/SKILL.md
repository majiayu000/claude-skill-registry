---
name: loom-team-manager-pane-dead-on-spawn
description: Diagnose and fix Loom team manager pane dying immediately (tmux pane status 1).
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T09:27:53.279Z"
  updated_at: "2026-01-29T09:27:53.279Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# When To Use
- `loom team start <TEAM>` succeeds, but manager pane shows dead (status 1) and capture output is empty.

# Diagnose
- Confirm run exists:
  - `loom team status <TEAM> --show-dead`
- Capture manager:
  - `loom team capture <TEAM> manager --lines 200 --header`
- Open the capture metadata file under `.team/runs/<TEAM>/captures/*.json` and check:
  - `pane.start_command`
  - `pane.current_command`
  - `pane.dead`

# Common Root Cause: Missing `team` Binary
- If `pane.start_command` begins with `team tui ...`:
  - Verify: `command -v team` (likely missing)
  - Verify Loom exists: `command -v loom`
  - This means the pane died because tmux tried to run `team` directly.

# Fix Options
- Option A (fast local): add a `team` shim on PATH that forwards to Loom.
  - `team` should behave like: `loom team "$@"`
- Option B (proper): adjust Loom/runner config so tmux spawns `loom team tui ...` (not `team tui ...`).
- Option C: pass an explicit harness `--bin` that points to the correct executable if supported.

# Validate
- Restart run (or use `--force`):
  - `loom team start <TEAM> --force ...`
- Confirm manager pane is alive:
  - `loom team status <TEAM>`
  - `loom team capture <TEAM> manager --lines 40`
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
