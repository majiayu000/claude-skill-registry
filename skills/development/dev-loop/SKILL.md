---
name: dev-loop
description: Run ./dev.sh in background, monitor logs, iterate on code changes until the expected behavior is observed. Use when making changes that need runtime verification — UI behavior, protocol handling, camera capture, keyboard events. Spawns cargo-watch, tails logs, checks for expected output.
---

# Dev Loop Workflow

Run the app via `./dev.sh` in the background, monitor its logs, make code changes, and verify the expected behavior appears in the output. cargo-watch auto-rebuilds on file changes, so you just edit and check logs.

## Quick Start

```
1. Spawn ./dev.sh in background using Bash tool (run_in_background: true)
2. Wait ~10s for initial build + app startup
3. Read the log output (tail the task output)
4. Make code changes
5. cargo-watch auto-rebuilds — wait ~15s, then check logs again
6. Repeat until expected output appears
7. Stop the background task when done
```

## Step 1: Launch dev.sh

Use the Bash tool with `run_in_background: true`:

```bash
cd /Users/johnlindquist/dev/script-kit-gpui && ./dev.sh
```

This starts cargo-watch which auto-rebuilds on any `src/` file change. Save the **task_id** from the result.

## Step 2: Check Logs

Use `TaskOutput` with `block: false` to read current output without waiting:

```
TaskOutput(task_id=<id>, block=false, timeout=5000)
```

Or use Bash to tail the session log file:

```bash
tail -50 ~/.scriptkit/logs/latest-session.jsonl
```

The app uses compact AI log format by default (`SS.mmm|L|C|message`):
- `SS.mmm` = seconds.milliseconds since start
- `L` = level (i=info, d=debug, w=warn, e=error)
- `C` = component (EXEC, KEY, FOCUS, RENDER, etc.)

## Step 3: Edit Code and Wait for Rebuild

After editing files in `src/`, cargo-watch detects the change and rebuilds automatically. Wait ~15 seconds for:
- File change detection (~1s)
- Incremental compile (~10-14s)
- App restart (~1-2s)

Then check logs again via TaskOutput or tail.

## Step 4: Verify Expected Behavior

Look for specific log patterns that confirm the change worked. Examples:

| What you're verifying | Log pattern to look for |
|----------------------|------------------------|
| Webcam opens | `EXEC.*Opening Webcam` |
| Camera started | `EXEC.*start_capture` or camera frames flowing |
| Key handled | `KEY.*<keyname>` |
| View changed | `RENDER.*current_view` |
| Error occurred | `e\|` (error level) or `ERROR` |
| Script executed | `EXEC.*Running script` |

## Step 5: Interact with the Running App

Send stdin JSON commands to the app via its session log or interact directly. Common commands:

```bash
# Show the window (it starts hidden)
echo '{"type":"show"}' | socat - UNIX-CONNECT:/tmp/scriptkit.sock

# Or use the log to confirm manual interaction
# (click the app, press keys, watch logs)
```

## Step 6: Stop When Done

Use `TaskStop` with the task_id to kill the background dev.sh process.

## Iteration Patterns

### "I changed X, did it work?"

1. Make the edit
2. Wait 15s for rebuild
3. `TaskOutput(block=false)` — scan for rebuild success (`Compiling...` → `Finished`)
4. Check for your specific log output
5. If not present, check for compile errors in the output

### "The app crashes on startup"

1. `TaskOutput(block=false)` — look for panic/error in output
2. Fix the code
3. cargo-watch auto-rebuilds
4. Check output again

### "I need to test a specific interaction"

1. Make sure app is running (check TaskOutput for `Finished` + startup logs)
2. Manually interact with the app window (or send stdin commands)
3. Check logs for the expected behavior

## Log File Locations

| File | Contents |
|------|----------|
| Task output | cargo-watch build output + app stdout/stderr |
| `~/.scriptkit/logs/latest-session.jsonl` | Structured session logs |
| `/tmp/sk-test-stdout.log` | Test script output (if using visual-test) |

## Gotchas

- **First build takes ~60s.** Incremental rebuilds are ~10-15s.
- **cargo-watch needs to be installed.** `cargo install cargo-watch` if missing.
- **App starts hidden.** You need to trigger it via global hotkey or stdin commands.
- **Don't edit test files** — cargo-watch ignores them, so changes won't trigger rebuild.
- **Multiple dev.sh instances conflict.** Stop the old one before starting a new one.
- **Check compile errors first.** If TaskOutput shows `error[E...]`, fix the code before checking behavior.
