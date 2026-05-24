---
name: shared-process-lifecycle
description: Unified process lifecycle management for all Ralph agents. Use proactively when starting any background process (dev server, test watcher, etc.).
category: infrastructure
tags: [processes, lifecycle, cleanup, watchdog]
dependencies: [shared-ralph-core, shared-file-permissions]
---

# Process Lifecycle Management

> "Always check registry before starting, always cleanup when done – no orphaned processes."

## When to Use This Skill

Use **proactively**:
- **BEFORE** starting any background process
- **AFTER** completing task that used processes
- When managing dev servers, test watchers, build processes

---

## Quick Start

<examples>
Example 1: QA starting dev server
```powershell
# Check if already running
$server = Get-ManagedProcess -Name "dev-server" -Port 3000

if (-not $server) {
    $server = Start-ManagedProcess -Name "dev-server" -Port 3000 -Command "npm run dev"
}

# Run tests...

# MANDATORY: Cleanup after validation
Stop-ManagedProcess -Agent "qa"
```

Example 2: Developer with build watcher
```powershell
# Start watcher
$watcher = Start-ManagedProcess -Name "build-watcher" -Command "npm run build:watch"

# Work...

# Cleanup before going idle
Stop-ManagedProcess -Agent "developer"
```

Example 3: Check port availability
```powershell
$portInUse = Test-Port -Port 3000
if ($portInUse) {
    $owner = Get-ProcessByPort -Port 3000
    # Reuse or terminate
}
```
</examples>

---

## The Golden Rules

1. **ALWAYS** check the process registry before starting
2. **ALWAYS** register processes you start
3. **ALWAYS** cleanup your processes when done
4. **NEVER** start duplicate processes
5. **NEVER** leave background processes running when you exit

---

## Process Registry

**Location**: `.claude/session/process-registry.json`

Tracks all running processes across all agents.

**Format**:
```json
{
  "version": "1.0",
  "lastUpdated": "2026-01-23T10:00:00Z",
  "processes": {
    "dev-server-3000": {
      "name": "dev-server",
      "port": 3000,
      "pid": 12345,
      "agent": "qa",
      "startedAt": "2026-01-23T09:55:00Z",
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

---

## Before Starting Any Process

### 1. Check if Already Running

```powershell
$existing = Get-ManagedProcess -Name "dev-server" -Port 3000

if ($existing) {
    # Reuse existing process
    Write-Host "Reusing existing (PID: $($existing.pid))"
} else {
    # Start new process
    $process = Start-ManagedProcess -Name "dev-server" -Port 3000 -Command "npm run dev"
}
```

### 2. Check Port Availability

```powershell
$portInUse = Test-Port -Port 3000

if ($portInUse) {
    $owner = Get-ProcessByPort -Port 3000
    # Decide: reuse or terminate
}
```

---

## When You're Done

**Cleanup is MANDATORY before marking task complete.**

```powershell
# Stop all processes you started
Stop-ManagedProcess -Agent "qa"  # or "developer" or "pm"

# Only AFTER cleanup, update status to "idle"
```

---

## Process Types

| Type | Port | Reuse? | Cleanup |
|------|------|--------|---------|
| dev-server | 3000 | Yes | After validation |
| test-server | varies | No | After tests |
| build-watcher | N/A | Yes | After commit |
| storybook | 6006 | Yes | After review |

---

## Agent-Specific Rules

| Agent | Processes | Behavior |
|-------|-----------|----------|
| **QA** | Dev server, test watcher | Start once, reuse for all tests, cleanup after |
| **Developer** | Build watcher, dev server | Start if testing, cleanup immediately |
| **PM** | Research server (rare) | Cleanup after research |

---

## Anti-Patterns

❌ **DON'T**:
- Start processes without tracking
- Use `&` or `Start-Process` without registration
- Leave processes running after task completes
- Start same process multiple times
- Assume someone else will cleanup

✅ **DO**:
- Always use `Start-ManagedProcess` helper
- Always register in process-registry.json
- Always cleanup with `Stop-ManagedProcess`
- Check for existing processes before starting
- Cleanup your own processes before going idle

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-ralph-core` | Session structure |
| `shared-file-permissions` | File permissions |
| `shared-atomic-updates` | Safe file updates |
