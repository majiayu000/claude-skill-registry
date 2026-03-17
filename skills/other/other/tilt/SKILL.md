---
name: tilt
description: Manages Tilt development environments via CLI and Tiltfile authoring. Must use when working with Tilt or Tiltfiles.
---

# Tilt Development Environment

## Automatic Reload Behaviors

Tilt live-reloads aggressively. **Never suggest restarting `tilt up` or manually refreshing resources**—Tilt handles this automatically in nearly all cases.

### What Reloads Automatically

| Change Type | What Happens | Your Action |
|------------|--------------|-------------|
| **Tiltfile edits** | Tilt re-evaluates the entire Tiltfile on save | Just save the file |
| **Source code with `live_update`** | Files sync to container without rebuild | Just save the file |
| **Source code without `live_update`** | Full image rebuild triggers automatically | Just save the file |
| **Kubernetes manifests** | Resources re-apply automatically | Just save the file |
| **Frontend with HMR** | Browser updates via Hot Module Replacement | Just save the file |
| **Backend with watch tools** | Process restarts via nodemon/air/watchexec | Just save the file |

### When Restart IS Actually Needed

Restarting `tilt up` is required only for:
- Tilt version upgrades
- Changing Tilt's port or host settings
- Recovering from Tilt crashes
- Kubernetes context changes (switching clusters)

### Verifying Updates Applied

Instead of restarting, verify updates propagated:

```bash
# Check resource status after saving
tilt get uiresource/<name> -o json | jq '.status.updateStatus'

# Watch for update completion
tilt wait --for=condition=Ready uiresource/<name> --timeout=60s

# Check recent logs for reload confirmation
tilt logs <resource> --since 1m
tilt logs <resource> --since 5m | rg -i "reload|restart|updated|synced"
```

## Running tilt up

**Always run `tilt up` in a tmux session using send-keys.** This ensures:
- Tilt survives Claude Code session reloads
- Shell initialization runs (PATH, direnv, etc.)

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# Start tilt in tmux (idempotent, send-keys for proper shell init)
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux new-session -d -s "$SESSION" -n tilt
  tmux send-keys -t "$SESSION:tilt" 'tilt up' Enter
  echo "Started tilt in tmux session: $SESSION"
elif ! tmux list-windows -t "$SESSION" -F '#{window_name}' | grep -q "^tilt$"; then
  tmux new-window -t "$SESSION" -n tilt
  tmux send-keys -t "$SESSION:tilt" 'tilt up' Enter
  echo "Added tilt window to session: $SESSION"
else
  echo "Tilt already running in session: $SESSION"
fi
```

To check tilt output:
```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)
tmux capture-pane -p -t "$SESSION:tilt" -S -50
```

To stop tilt:
```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)
tmux send-keys -t "$SESSION:tilt" C-c
```

Never run `tilt up` directly in foreground or with `run_in_background`. Always use tmux.

## Instructions

- Use `tilt get uiresources -o json` to query resource status programmatically
- Use `tilt get uiresource/<name> -o json` for detailed single resource state
- Use `tilt logs` with `--since`, `--tail`, `--json` flags for log retrieval
- Use `tilt trigger <resource>` to force updates when auto-reload didn't trigger
- Use `tilt wait` to block until resources reach ready state
- For Tiltfile authoring, see @TILTFILE_API.md
- For complete CLI reference with JSON parsing patterns, see @CLI_REFERENCE.md

## Quick Reference

### Check Resource Status

```bash
tilt get uiresources -o json | jq '.items[] | {name: .metadata.name, runtime: .status.runtimeStatus, update: .status.updateStatus}'
```

### Wait for Resource Ready

```bash
tilt wait --for=condition=Ready uiresource/<name> --timeout=120s
```

### Get Resource Logs

```bash
tilt logs <resource>              # Current logs
tilt logs <resource> --since 5m   # Logs from last 5 minutes
tilt logs <resource> --tail 100   # Last 100 lines
tilt logs --json                  # JSON Lines output
```

### Trigger Update

```bash
tilt trigger <resource>
```

### Lifecycle Commands

```bash
tilt up        # Start Tilt
tilt down      # Stop and clean up
tilt ci        # CI/batch mode
```

## Resource Status Values

- **RuntimeStatus**: `unknown`, `none`, `pending`, `ok`, `error`, `not_applicable`
- **UpdateStatus**: `none`, `pending`, `in_progress`, `ok`, `error`, `not_applicable`

## References

- Tilt Documentation: https://docs.tilt.dev/
- CLI Reference: https://docs.tilt.dev/cli/tilt.html
- Tiltfile API: https://docs.tilt.dev/api.html
- Extensions: https://github.com/tilt-dev/tilt-extensions
