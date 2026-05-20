---
name: dk-local-logs
description: "Inspect and debug errors via logs across the harness-kit monorepo. Reads the right log file based on the error layer — backend, frontend, celery, odin CLI, or odin task execution. Use this skill whenever someone mentions a 500 error, a stack trace, a crash, 'check the logs', 'what went wrong', a service not starting, celery task failures, or any runtime error. Also triggers on: 'getting 500', 'backend error', 'celery error', 'odin failed', 'check logs', 'tail logs', 'debug this error', or /dk-local-logs."
argument-hint: "[backend | frontend | celery | odin | task <id>] [--lines N] [--search <pattern>]"
allowed-tools: Bash, Read, Grep
---

# /dk-local-logs — Log Inspector & Error Debugger

Read the right log for the right problem, from the right place. No more guessing which of 5 log locations to check.

## Quick Reference

| Symptom | Log to check | Command |
|---------|-------------|---------|
| 500 error, API broken | Backend | `/dk-local-logs backend` |
| UI not loading, build error | Frontend | `/dk-local-logs frontend` |
| Task not executing, queue stuck | Celery | `/dk-local-logs celery` |
| `odin plan`/`odin exec` failed | Odin | `/dk-local-logs odin` |
| Specific task execution trace | Task | `/dk-local-logs task <id>` |
| Migration error on startup | Backend | `/dk-local-logs backend --search migrate` |
| Don't know where the error is | Auto | `/dk-local-logs` (no args) |

## Arguments

Parse `$ARGUMENTS` to extract:
- **layer** (optional): `backend`, `frontend`, `celery`, `odin`, or `task`
- **id** (required for `task`): task ID or prefix
- **--lines N** (optional, default 50): how many lines from the end to show
- **--search <pattern>** (optional): grep for a pattern in the log

If no layer is specified, run **auto-detect mode** — check all logs for recent errors.

## Log Locations

All paths are relative to `REPO_ROOT` (use `git rev-parse --show-toplevel`).

| Layer | File | Format | Notes |
|-------|------|--------|-------|
| **backend** | `.dev-logs/backend.log` | Plain text | Django runserver stdout/stderr |
| **frontend** | `.dev-logs/frontend.log` | Plain text | Vite dev server output |
| **celery** | `.dev-logs/celery.log` | Plain text | Celery worker + beat |
| **backend-app** | `taskit/taskit-backend/logs/taskit.log` | Structured plain text | App-level logging, `[timestamp] LEVEL [file:line] - msg` |
| **backend-detail** | `taskit/taskit-backend/logs/taskit_detail.log` | Plain text | Full tracebacks (check here for exception details) |
| **odin-runs** | `.odin/logs/run_*.jsonl` (in working dir) | JSON lines | Structured orchestration log |
| **odin-app** | `.odin/logs/odin.log` (in working dir) | Plain text | Odin CLI logging |
| **odin-detail** | `.odin/logs/odin_detail.log` (in working dir) | Plain text | Full tracebacks from odin (`odin logs debug`) |
| **task-output** | `.odin/logs/task_<id>.out` (in working dir) | Plain text | Raw agent stdout for a task (`odin logs <id> -f`) |

## Execution

### Step 1: Resolve paths

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
```

Odin logs live in the **working directory** where odin was run, not the repo root. The standard working dir is `$REPO_ROOT/odin/temp_test_dir/`. Check both.

### Step 2: Read the log

Based on the layer argument:

#### `backend` (or auto-detect first choice for 500 errors)

Check two locations — `.dev-logs/backend.log` has startup/crash output, `taskit-backend/logs/taskit_detail.log` has full tracebacks:

```bash
# Recent backend output (startup errors, migration failures)
tail -n $LINES "$REPO_ROOT/.dev-logs/backend.log"

# Full tracebacks from app logging (the real errors)
tail -n $LINES "$REPO_ROOT/taskit/taskit-backend/logs/taskit_detail.log"
```

**When debugging 500s**: The `taskit_detail.log` has full exception tracebacks. The `.dev-logs/backend.log` has Django's console error output. Check both — the detail log is usually more informative.

Also check if the migration is current:
```bash
cd "$REPO_ROOT/taskit/taskit-backend" && python manage.py showmigrations tasks 2>&1 | grep '\[ \]'
```
If unapplied migrations exist, that's likely the cause.

#### `frontend`

```bash
tail -n $LINES "$REPO_ROOT/.dev-logs/frontend.log"
```

Look for: TypeScript errors, Vite build failures, module resolution errors.

#### `celery`

```bash
tail -n $LINES "$REPO_ROOT/.dev-logs/celery.log"
```

Look for: `Task exception`, `WorkerLostError`, broker connection failures.

#### `odin`

Check the most recent structured run log:

```bash
# Find latest run log
ODIN_WD="$REPO_ROOT/odin/temp_test_dir"
LATEST=$(ls -t "$ODIN_WD/.odin/logs/run_"*.jsonl 2>/dev/null | head -1)

# Show structured entries (formatted)
if [ -n "$LATEST" ]; then
    tail -n $LINES "$LATEST" | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        e = json.loads(line.strip())
        ts = e.get('timestamp','')[:19]
        action = e.get('action','')
        tid = (e.get('task_id','') or '')[:8]
        agent = e.get('agent','')
        dur = e.get('duration_ms','')
        meta = e.get('metadata','')
        print(f'{ts}  {action:<20s}  {tid:<10s}  {agent:<8s}  {dur}ms  {meta}')
    except: pass
"
fi

# Also check odin detail log for tracebacks
tail -n $LINES "$ODIN_WD/.odin/logs/odin_detail.log" 2>/dev/null
```

#### `task <id>`

Show the raw agent output for a specific task execution:

```bash
ODIN_WD="$REPO_ROOT/odin/temp_test_dir"

# Find the task output file (supports prefix matching)
TASK_FILE=$(ls "$ODIN_WD/.odin/logs/task_${ID}"*.out 2>/dev/null | head -1)

if [ -n "$TASK_FILE" ]; then
    tail -n $LINES "$TASK_FILE"
else
    echo "No output file found for task $ID"
    echo "Available task logs:"
    ls "$ODIN_WD/.odin/logs/task_"*.out 2>/dev/null | sed 's/.*task_/  task_/'
fi
```

Also check the backend's per-task execution logs:
```bash
ls "$REPO_ROOT/taskit/taskit-backend/logs/"*"${ID}"*.log 2>/dev/null | while read f; do
    echo "=== $(basename "$f") ==="
    tail -n $LINES "$f"
done
```

### Step 3: Search mode (--search)

If `--search <pattern>` is provided, grep across the relevant log(s):

```bash
grep -n -i "$PATTERN" "$LOG_FILE" | tail -n $LINES
```

For auto-detect with search, grep across ALL logs:
```bash
grep -rn -i "$PATTERN" "$REPO_ROOT/.dev-logs/" "$REPO_ROOT/taskit/taskit-backend/logs/taskit_detail.log" 2>/dev/null | tail -n 30
```

### Step 4: Auto-detect mode (no layer specified)

When no layer is given, scan all logs for recent errors:

1. Check `.dev-logs/backend.log` for recent `Traceback`, `Error`, `500`
2. Check `taskit-backend/logs/taskit_detail.log` for recent exceptions
3. Check `.dev-logs/celery.log` for `Task exception` or `ERROR`
4. Check odin detail log for recent tracebacks
5. Report which layer(s) have errors, show the most recent one

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
echo "=== Scanning all logs for errors ==="

for log_label_file in \
    "backend:.dev-logs/backend.log" \
    "backend-detail:taskit/taskit-backend/logs/taskit_detail.log" \
    "celery:.dev-logs/celery.log" \
    "odin:odin/temp_test_dir/.odin/logs/odin_detail.log"; do
    label="${log_label_file%%:*}"
    file="$REPO_ROOT/${log_label_file#*:}"
    if [ -f "$file" ]; then
        count=$(grep -c -iE "error|traceback|exception|500" "$file" 2>/dev/null || echo 0)
        if [ "$count" -gt 0 ]; then
            echo ""
            echo "--- $label ($count error lines) ---"
            grep -iE "error|traceback|exception|500" "$file" | tail -5
        fi
    fi
done
```

Then show the full traceback from whichever log has the most recent error.

## Handoff to other skills

- If the error points to a **specific task** (task ID visible), suggest: `/dk-local-inspect task <id>` for structured diagnostic data (status, metadata, comments, dependency chain)
- If the error points to a **spec run**, suggest: `/dk-local-inspect spec <id>`
- This skill reads raw logs; `/dk-local-inspect` reads structured Django ORM data. Use both together for full picture.

## Error handling

If `$ARGUMENTS` is empty, run auto-detect mode (scan all logs).

If a log file doesn't exist, say so and suggest:
- "Is the dev server running? Start it with `./dev.sh`"
- "No odin logs found — has `odin plan` or `odin exec` been run from this directory?"

If `.dev-logs/` doesn't exist at all:
- "The `.dev-logs/` directory doesn't exist. Run `./dev.sh` to start the dev stack, which creates logs there."
