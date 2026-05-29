---
name: shared-atomic-updates
description: Atomic file update patterns to prevent corruption. Use proactively when writing to any shared file to prevent data loss from concurrent writes.
category: infrastructure
tags: [atomic, files, concurrency, safety]
dependencies: [shared-file-permissions, shared-ralph-core]
---

# Atomic Updates

> "Read-modify-write with temp file – prevents corruption from concurrent writes."

## When to Use This Skill

Use **proactively**:
- **ALWAYS** when updating `prd.json`
- **ALWAYS** when updating shared session files
- **ALWAYS** when multiple agents may write to same file

Use **when**:
- Updating high-contention files
- Writing to files from worktree branches

---

## Quick Start

<examples>
Example 1: Basic atomic update (bash)
```bash
# Read
STATE=$(cat file.json)

# Modify
NEW_STATE=$(echo "$STATE" | jq '.field = "value"')

# Write atomically
echo "$NEW_STATE" > file.json.tmp && mv file.json.tmp file.json
```

Example 2: PowerShell atomic update
```powershell
# Read
$state = Get-Content "file.json" | ConvertFrom-Json

# Modify
$state.field = "value"

# Write atomically
$tempPath = "file.json.tmp"
$state | ConvertTo-Json -Depth 10 | Set-Content -Path $tempPath
Move-Item -Path $tempPath -Destination "file.json" -Force
```

Example 3: From worktree to master branch
```bash
# When in worktree, update master prd.json
# Edit tool handles atomic writes automatically
Read("../master-branch/prd.json")  # Read from master
Edit("../master-branch/prd.json", ...)  # Atomic write to master
```
</examples>

---

## The Problem

If two agents write to the same file simultaneously:
- Data can be lost
- File can be corrupted
- Last write wins, losing previous changes

---

## The Solution: Atomic Updates

Always update files using the temp-file pattern:

```bash
# 1. Read
STATE=$(cat file.json)

# 2. Modify
NEW_STATE=$(echo "$STATE" | jq '.field = "value"')

# 3. Write atomically
echo "$NEW_STATE" > file.json.tmp && mv file.json.tmp file.json
```

The `mv` command is atomic on Unix-like systems – either the whole rename succeeds or fails, never leaving a partial file.

---

## Master Branch Coordination (CRITICAL)

**When working in a git worktree, ALL coordination files must be updated in the master branch.**

| File/Directory | Purpose | Who Updates |
|----------------|---------|-------------|
| `prd.json` | Task status, agent status | All agents |
| `.claude/session/messages/` | Event queue | All agents |
| `.claude/session/*.json` | State files | All agents |

| Directory | Purpose | Who Updates |
|-----------|---------|-------------|
| `src/` | Code changes | Developer |
| `src/assets/` | Asset changes | TechArtist |

### Pattern for Master Branch Updates

```bash
# For PRD updates from worktree:
# 1. Read master branch prd.json
# 2. Use Edit tool to make changes
# 3. Edit tool handles atomic writes automatically
```

---

## Update Specific Field (jq)

```bash
# Single field update
jq '.session.iteration += 1' prd.json > prd.json.tmp
mv prd.json.tmp prd.json

# Nested field - agent status
jq '.agents.developer.lastSeen = "2026-01-23T12:00:00Z"' prd.json > prd.json.tmp
mv prd.json.tmp prd.json

# Task status update
jq '.items[0].status = "in_progress"' prd.json > prd.json.tmp
mv prd.json.tmp prd.json
```

---

## PowerShell Update-JsonFile (if available)

```powershell
Update-JsonFile -FilePath "file.json" -UpdateScript {
    param($state)
    $state.field = "value"
    return $state
}
```

This wrapper handles the atomic pattern automatically.

---

## Error Handling

If atomic update fails:

1. **Log the error** - Write to progress file
2. **Wait 5 seconds** - Give other processes time to complete
3. **Re-read the file** - Get latest state
4. **Re-apply changes** - Merge your updates
5. **Try again** - Attempt atomic update once more

If it fails twice, log the conflict and continue polling.

---

## When Atomic Updates Matter Most

- **High-contention files**: `prd.json` (session state, agent status, task items)
- **Shared log files**: `session.log` (use append-only instead)
- **PRD file**: Multiple agents may update different fields

---

## When Atomic Updates Don't Apply

- **Agent-specific files**: `developer-progress.txt` (only one writer)
- **Append-only logs**: These don't need atomic pattern
- **New file creation**: No existing content to protect

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-file-permissions` | Who can write to what |
| `shared-ralph-core` | Session structure |
| `shared-worker-worktree` | Parallel development coordination |
