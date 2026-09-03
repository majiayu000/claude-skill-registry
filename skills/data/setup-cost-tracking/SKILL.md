---
name: setup-cost-tracking
description: Install genuine per-session cost tracking for Claude Code by wiring bundled logger scripts into the user's statusline — preserving any existing statusline and hooks. Use when the user asks to set up, install, enable, or repair cost tracking / cost logging / session cost capture. Idempotent; safe to re-run.
model: inherit
color: orange
---

# Setup Cost Tracking

Installs genuine cost capture for every Claude Code session on this machine. Cost data
(`cost.total_cost_usd` etc.) is computed by Claude Code itself and is available **only**
in the statusline payload — hooks never receive it. So this skill wires a logger into the
statusline path while preserving whatever statusline and hooks the user already has.

## What gets installed

Bundled in this skill's `scripts/` directory, copied to `~/.claude/scripts/`:

| Script | Role |
|---|---|
| `cost-logger.js` | Capture engine. Silent, crash-proof. Writes the log files below. |
| `statusline-wrapper.js` | Used when the user already has a statusline: logs cost, then delegates the payload to their original command and passes its output through untouched. |
| `statusline-command.js` | Used when the user has no statusline: full display (model, context bar, cost, cache stats) that also logs. |
| `turn-logger.js` | Stop hook: stamps turn boundaries so cost samples can later be grouped into turns for analytics. No cost data itself. |

Log outputs (created lazily, no setup needed):

- `~/.claude/cost-log.jsonl` — one row per session, exact cumulative totals (upserted).
- `~/.claude/projects/<mapped-dir>/<session>.cost.jsonl` — cost samples at ~5s resolution during activity.
- `~/.claude/projects/<mapped-dir>/<session>.turn-boundaries.jsonl` — one row per turn end, with `transcript_path` for deep-dive analytics.

## Installation procedure

Follow these steps exactly. Use real JSON manipulation (a `node -e` script or `jq`) for
every settings edit — never string/regex edits on settings files.

### Step 0 — Preflight

1. `command -v node` — if Node.js is missing, stop and tell the user it's required.
   Record the absolute path (call it `$NODE`). Use `$NODE` in every command you write
   into settings, not bare `node` (statusline/hook commands don't always get the user's
   full shell PATH).
2. Read `~/.claude/settings.json` (treat as `{}` if absent) and `~/.claude/settings.local.json`
   (if present). The **effective** `statusLine` is the local one if defined there, else the
   user one. Remember which file defines it — edits must go to that same file.

### Step 1 — Copy scripts

1. `mkdir -p ~/.claude/scripts`
2. Copy the four `.js` files from this skill's `scripts/` directory into `~/.claude/scripts/`
   and `chmod +x` them. Overwriting previous versions of these four files is fine (that's
   how upgrades work). **Never** overwrite `~/.claude/scripts/statusline-original.json`
   if it exists.

### Step 2 — Wire the statusline (the load-bearing step)

Decide by the effective `statusLine`:

- **Case A — already ours**: its command contains `statusline-wrapper.js` or
  `statusline-command.js`. Nothing to change; report "already installed" and continue to Step 3.
- **Case B — none configured**: set in `~/.claude/settings.json`:
  ```json
  "statusLine": { "type": "command", "command": "$NODE /Users/<user>/.claude/scripts/statusline-command.js", "padding": 0 }
  ```
  (expand `$NODE` and the home directory to absolute paths).
- **Case C — user has their own statusline**: preserve it.
  1. Write `~/.claude/scripts/statusline-original.json` containing exactly
     `{ "command": "<their current statusLine.command>" }`.
  2. In the file that defines `statusLine`, replace **only** the `command` value with
     `$NODE /Users/<user>/.claude/scripts/statusline-wrapper.js`. Keep `type`, `padding`,
     `refreshInterval`, and any other sibling keys untouched.

Before the first edit to any settings file, back it up:
`cp settings.json settings.json.bak-cost-tracking` (same pattern for the local file).
One backup per run is enough.

### Step 3 — Add the turn-boundary hook (additive, never replaces)

If no existing `hooks.Stop` entry's command mentions `turn-logger.js`, append this entry to
the `hooks.Stop` array (create the array/path if missing), leaving every existing hook alone:

```json
{ "matcher": "", "hooks": [ { "type": "command", "command": "$NODE /Users/<user>/.claude/scripts/turn-logger.js" } ] }
```

This hook carries no cost data — it only stamps turn boundaries and the idle timer. If the
user objects to hooks, skipping this step still leaves session cost capture fully working.

### Step 4 — Verify

1. Build a fake statusline payload with `session_id` `"cost-setup-verify"`, a `workspace.current_dir`
   of `/tmp/cost-setup-verify`, and nonzero `cost.total_cost_usd` / `cost.total_api_duration_ms` /
   `model.display_name` values.
2. Pipe it via stdin into the exact `statusLine.command` now in settings (run through `sh -c`).
   - Case B: expect the rendered multi-line statusline.
   - Case C: expect the *original* statusline's output (the wrapper delegates). If their original
     command errors on the synthetic payload, that's their script's quirk — check instead that
     the log file below was written.
3. Confirm `~/.claude/projects/-tmp-cost-setup-verify/cost-setup-verify.cost.jsonl` now exists
   and contains the fake cost.
4. Clean up all verification artifacts: that projects subdirectory, the `cost-setup-verify` line
   in `~/.claude/cost-log.jsonl`, and `/tmp/statusline-*-cost-setup-verify` state files.

### Step 5 — Report

Tell the user, concretely:
- which case applied (fresh install / wrapped their existing statusline / already installed),
- every file created or modified (settings edits, backups, copied scripts),
- where their cost data will accumulate (the three log paths above),
- that changes take effect in new sessions,
- how to uninstall: restore the `.bak-cost-tracking` settings backup (or, by hand: point
  `statusLine.command` back to the command saved in `~/.claude/scripts/statusline-original.json`
  and remove the turn-logger Stop hook entry), then delete the four scripts.

## Invariants

- **Never delete or rewrite the user's hooks, statusline command, or unrelated settings keys.**
  All changes are additive or a single-value swap that is recorded for reversal.
- Idempotent: re-running on an installed machine must change nothing and say so.
- If any step fails midway, restore the settings backup and report what happened.
