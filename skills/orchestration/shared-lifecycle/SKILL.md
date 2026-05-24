---
name: shared-lifecycle
description: Process lifecycle management and auxiliary script rules for Ralph agents
category: orchestration
---

# Shared Lifecycle

> "Cleanup after yourself. Don't leave processes running when you exit."

---

## Process Management Golden Rules

1. **Check** the process registry before starting a process
2. **Register** processes you start
3. **Cleanup** your processes when done
4. **Never** start a duplicate process if one is running
5. **Never** leave background processes running when you exit

---

## Process Registry

**Location:** `.claude/session/process-registry.json`

The registry tracks all running processes across all agents.

**Format:**

```json
{
  "version": "1.0",
  "lastUpdated": "2026-01-26T10:00:00Z",
  "processes": {
    "dev-server-3000": {
      "name": "dev-server",
      "port": 3000,
      "pid": 12345,
      "agent": "qa",
      "startedAt": "2026-01-26T09:55:00Z",
      "command": "npm run dev",
      "status": "running",
      "purpose": "browser-validation"
    }
  },
  "agents": {
    "qa": ["dev-server-3000"],
    "developer": [],
    "pm": []
  }
}
```

### Using Read/Write Tools

**Check registry:**

```
Read: .claude/session/process-registry.json
```

**Update registry:**

```
Edit: .claude/session/process-registry.json
```

---

## Background Process Management

### Starting Background Processes

**Using Bash tool with `run_in_background=true`:**

```bash
# Start dev server in background
Bash(command="npm run dev", run_in_background=true)
# Returns: { shell_id: "abc123" }
```

**Capture the `shell_id`** — you need it for cleanup!

### Checking Port Availability

Before starting a process that binds to a port:

```bash
# Check if port is in use
Bash(command="netstat -an | grep :3000 || echo 'Port 3000 available'")
```

### Cleanup is MANDATORY

**Before updating status to "idle" or reporting task complete:**

```bash
# Kill the background process using shell_id
TaskStop(task_id="abc123")
```

### Cleanup Checklist

**CRITICAL: Always stop background processes before exit**

- [ ] Kill ALL background processes (use TaskStop with shell_id)
- [ ] Process registry updated (processes removed from agent's list)
- [ ] Ports are released (verify with netstat/lsof)
- [ ] No orphaned node/npm processes remain

---

## Cleanup Pattern (Even on Failure)

**Always cleanup in a finally pattern:**

```
1. Start background process (capture shell_id)
2. Try:
   - Do the work
3. Finally:
   - Stop background process (TaskStop with shell_id)
   - Update process registry
4. Only THEN: Update task status
```

**Anti-pattern:** ❌ Exiting without stopping background processes
**Good pattern:** ✅ Always cleanup, even if work fails

---

## Auxiliary Scripts

Scripts in `.claude/session/` help with automation and cleanup.

### Script Classification

| Classification | Pattern                                        | Retention                |
| -------------- | ---------------------------------------------- | ------------------------ |
| **Temporary**  | `*-runner.sh`, `msg-*.json`, `*.exit`, `*.tmp` | Auto-delete after 1 hour |
| **Reusable**   | Documented below                               | Persist across sessions  |
| **Unknown**    | Everything else                                | Manual cleanup           |

### Creating Reusable Scripts

If you create a helper script that provides value:

1. **Document purpose** — Add comment header
2. **Use descriptive naming** — `{agent}-{purpose}.sh`
3. **Track usage** — Note which agents use it
4. **Explain value** — Future sessions should understand why it exists

---

## Script Permissions

- Scripts in `.claude/session/` executable by all agents
- Never create scripts that modify source code without explicit task
- Scripts should only update session files or state files

---

## Anti-Patterns

| Don't                                       | Do Instead                          |
| ------------------------------------------- | ----------------------------------- |
| Start background processes without tracking | Capture shell_id, use for cleanup   |
| Leave processes running after exit          | Always cleanup before status update |
| Start same process multiple times           | Check registry first                |
| Assume someone else will cleanup            | Cleanup your own processes          |
| Use PowerShell Get-Content/Set-Content      | Use Read/Write tools                |
| Use manual temp file pattern                | Use Edit tool                       |

---
