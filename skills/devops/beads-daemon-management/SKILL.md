---
name: beads-daemon-management
description: Beads daemon lifecycle management, log analysis, socket recovery, and background sync operations. Covers start/stop/status, troubleshooting, and integration with git workflow.
model_invoked: true
triggers:
  - "daemon"
  - "bd daemon"
  - "beads daemon"
  - "daemon status"
  - "daemon stuck"
  - "socket"
  - "auto-sync"
---

# Beads Daemon Management

## Overview

The Beads daemon (`bd daemon`) runs as a background process that watches for issue mutations and automatically syncs changes to/from JSONL files. This skill covers daemon lifecycle, log analysis, troubleshooting, and integration with git workflows.

**Key Files:**
- `.beads/config.yaml` — Daemon configuration
- `.beads/daemon.log` — Runtime logs
- `.beads/daemon.pid` — Process ID file
- `.beads/daemon.sock` — Unix socket for IPC
- `.beads/issues.jsonl` — Serialized issue state

---

## Pattern 1: Daemon Lifecycle — START/STOP/STATUS

**When:** Managing the background sync process.

### Starting the Daemon

```bash
# Start in background (default)
bd daemon --start

# Start in foreground (for debugging)
bd daemon --start --foreground

# Start with metrics endpoint
bd daemon --start --metrics

# Start with auto-commit on changes
bd daemon --start --auto-commit

# Start with auto-push (implies auto-commit)
bd daemon --start --auto-push
```

### Checking Status

```bash
# Quick status check
bd daemon --status

# Health check (verifies socket responsiveness)
bd daemon --health

# Output examples:
# ✓ Daemon running (PID 12345)
# ✗ Daemon not running
# ⚠ Daemon unresponsive (stale socket)
```

### Stopping the Daemon

```bash
# Graceful stop
bd daemon --stop

# Force stop (if graceful fails)
kill -9 $(cat .beads/daemon.pid)
rm .beads/daemon.sock .beads/daemon.pid
```

### Restart Pattern

```bash
# Stop then start
bd daemon --stop && bd daemon --start

# Or with flags preserved
bd daemon --stop && bd daemon --start --auto-commit
```

---

## Pattern 2: Configuration Options

**When:** Customizing daemon behavior via `.beads/config.yaml`.

### Key Configuration Fields

```yaml
# .beads/config.yaml

# Auto-start daemon when bd commands run
auto-start-daemon: true

# Debounce time before flushing changes to JSONL
flush-debounce: "5s"

# Custom sync branch (for multi-repo setups)
sync-branch: "beads-sync"

# Multi-repo configuration
multi-repo:
  enabled: false
  repos:
    - path: "../other-repo"
      sync-branch: "beads-sync"
```

### Configuration Decision Tree

```
Need automatic sync?
│
├─ Yes, always
│  └─ auto-start-daemon: true
│
├─ Yes, with git integration
│  └─ --auto-commit or --auto-push flags
│
├─ No, manual control
│  └─ auto-start-daemon: false
│     (use bd sync --from-main manually)
│
└─ Cross-repo sync?
   └─ multi-repo.enabled: true
      (configure repos array)
```

---

## Pattern 3: Log Analysis — MUTATION/EXPORT/IMPORT

**When:** Debugging sync issues or understanding daemon behavior.

### Log Location

```bash
# View recent logs
tail -50 .beads/daemon.log

# Follow logs in real-time
tail -f .beads/daemon.log

# Search for specific patterns
grep "Export triggered" .beads/daemon.log
```

### Log Entry Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `Mutation detected: create <id>` | New issue created | Normal operation |
| `Mutation detected: update <id>` | Issue modified | Normal operation |
| `Mutation detected: close <id>` | Issue closed | Normal operation |
| `Export triggered by mutation events` | Flush to JSONL starting | Normal operation |
| `Exported to JSONL` | JSONL file updated | Verify with `cat .beads/issues.jsonl` |
| `Import triggered by file change` | JSONL file changed externally | Git pull or manual edit |
| `Skipping auto-import: JSONL content unchanged` | No-op optimization | Normal (prevents loops) |
| `Socket error` | IPC failure | Check socket recovery |
| `Daemon already running` | Duplicate start attempt | Use `--status` first |

### Example Log Sequence

```log
[2025-12-19 20:37:53] Mutation detected: create tmnl-ahym
[2025-12-19 20:37:55] Export triggered by mutation events
[2025-12-19 20:37:55] Starting export...
[2025-12-19 20:37:55] Exported to JSONL
[2025-12-19 20:37:56] Import triggered by file change
[2025-12-19 20:37:56] Skipping auto-import: JSONL content unchanged
```

**Interpretation:** Issue created → daemon detected → exported to JSONL → detected own file change → correctly skipped re-import.

---

## Pattern 4: Socket Recovery — STALE SOCKET/LOCK

**When:** Daemon appears stuck, commands hang, or status shows "unresponsive".

### Symptoms

- `bd` commands hang indefinitely
- `bd daemon --status` shows running but `--health` fails
- `bd daemon --start` says "already running" but no process found

### Diagnosis

```bash
# Check if process actually exists
ps aux | grep "bd daemon"

# Check PID file
cat .beads/daemon.pid
ps -p $(cat .beads/daemon.pid)

# Test socket responsiveness
bd daemon --health
```

### Recovery Steps

```bash
# Step 1: Try graceful stop
bd daemon --stop

# Step 2: If that fails, force cleanup
rm -f .beads/daemon.sock .beads/daemon.pid

# Step 3: Verify cleanup
ls -la .beads/daemon.*
# Should show no .sock or .pid files

# Step 4: Restart fresh
bd daemon --start
bd daemon --status
# Should show: ✓ Daemon running (PID <new-pid>)
```

### Prevention

- Don't kill terminal with daemon running without `--stop`
- Use `--foreground` during development for clean Ctrl+C handling
- Check `bd daemon --status` before assuming issues

---

## Pattern 5: Git Workflow Integration

**When:** Syncing beads changes across branches or with remote.

### Session Start (Ephemeral Branch)

```bash
# Ensure daemon is running
bd daemon --status || bd daemon --start

# Pull latest beads from main
bd sync --from-main
```

### Session End (Ephemeral Branch)

```bash
# Sync beads changes to main
bd sync --from-main  # Get any updates first

# Commit code changes
git add .
git commit -m "feat: implement feature X"

# Merge to main (local)
git checkout main
git merge feature-branch
git checkout feature-branch
```

### Auto-Commit Workflow

```bash
# Start daemon with auto-commit
bd daemon --start --auto-commit

# Now every mutation triggers:
# 1. Export to JSONL
# 2. git add .beads/issues.jsonl
# 3. git commit -m "beads: sync <issue-id>"
```

### Auto-Push Workflow (CI/CD)

```bash
# For CI pipelines or shared environments
bd daemon --start --auto-push

# Triggers on mutation:
# 1. Export to JSONL
# 2. git add + commit
# 3. git push
```

---

## Pattern 6: Metrics Endpoint

**When:** Monitoring daemon health in dashboards or scripts.

### Enable Metrics

```bash
bd daemon --start --metrics
# Starts HTTP endpoint on localhost:9090/metrics (default)
```

### Available Metrics

```
# Prometheus format
beads_mutations_total{type="create"} 42
beads_mutations_total{type="update"} 156
beads_mutations_total{type="close"} 23
beads_exports_total 89
beads_imports_total 12
beads_daemon_uptime_seconds 3600
beads_last_export_timestamp 1703012400
beads_last_import_timestamp 1703012350
```

### Scrape Example

```bash
curl -s localhost:9090/metrics | grep beads_
```

---

## Anti-Patterns

### 1. Killing Daemon Without Stop

```bash
# WRONG — Leaves stale socket/pid
kill -9 $(cat .beads/daemon.pid)
# Commands will hang on stale socket

# CORRECT — Graceful stop cleans up
bd daemon --stop
```

### 2. Running Multiple Daemons

```bash
# WRONG — Race conditions, duplicate exports
bd daemon --start  # First
bd daemon --start  # Second (should fail, but if socket stale...)

# CORRECT — Check status first
bd daemon --status || bd daemon --start
```

### 3. Ignoring Import Loops

```bash
# WRONG — Manual JSONL edit without daemon awareness
echo '{"id":"test"}' >> .beads/issues.jsonl
# Daemon imports, exports, imports, exports...

# CORRECT — Use bd commands
bd create --title="Test" --type=task
# Daemon handles export, skips self-import
```

### 4. Forgetting Sync on Branch Switch

```bash
# WRONG — Switch branch without sync
git checkout main
# Beads state may be stale or conflict

# CORRECT — Sync before/after switch
bd sync --from-main
git checkout main
git merge feature-branch
```

---

## Decision Tree: Daemon Troubleshooting

```
Daemon issues?
│
├─ Commands hang
│  ├─ Check: bd daemon --health
│  ├─ Health OK? → Issue is elsewhere
│  └─ Health fails? → Socket recovery (Pattern 4)
│
├─ Changes not syncing
│  ├─ Check: tail .beads/daemon.log
│  ├─ No recent entries? → Daemon not running
│  ├─ Errors in log? → Address specific error
│  └─ "Skipping import"? → Normal (no actual changes)
│
├─ Duplicate exports
│  ├─ Check: ps aux | grep "bd daemon"
│  ├─ Multiple processes? → Kill all, clean restart
│  └─ Single process? → Check flush-debounce timing
│
└─ Git conflicts on JSONL
   ├─ Stop daemon first
   ├─ Resolve conflict manually
   ├─ bd sync --from-main
   └─ Restart daemon
```

---

## CLI Reference

```bash
bd daemon [flags]

FLAGS:
  --start           Start the daemon
  --stop            Stop the daemon
  --status          Show daemon status
  --health          Check daemon health (socket test)
  --foreground      Run in foreground (no detach)
  --auto-commit     Auto-commit JSONL changes
  --auto-push       Auto-push after commit (implies --auto-commit)
  --interval <dur>  Polling interval (default: 1s)
  --local           Local mode (no remote sync)
  --metrics         Enable metrics endpoint

EXAMPLES:
  bd daemon --start                    # Background start
  bd daemon --start --foreground       # Foreground (Ctrl+C to stop)
  bd daemon --stop                     # Graceful stop
  bd daemon --status                   # Check if running
  bd daemon --health                   # Verify responsiveness
  bd daemon --start --auto-commit      # Auto-commit on changes
```

---

## File Locations Summary

| File | Purpose | When to Check |
|------|---------|---------------|
| `.beads/config.yaml` | Configuration | Setup, changing behavior |
| `.beads/daemon.log` | Runtime logs | Debugging, verification |
| `.beads/daemon.pid` | Process ID | Status check, recovery |
| `.beads/daemon.sock` | Unix socket | Recovery (stale socket) |
| `.beads/issues.jsonl` | Serialized state | Conflict resolution |

---

## Integration Points

- **beads-issue-management** — Creating/updating issues that daemon syncs
- **beads-session-workflow** — Session start/end protocols using sync
- **beads-dependency-tracking** — Dependency changes trigger daemon export

