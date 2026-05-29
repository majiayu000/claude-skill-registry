---
name: shared-file-permissions
description: File read/write permissions for all Ralph agents. Use proactively when unsure about file ownership or write permissions.
category: infrastructure
tags: [permissions, ownership, files, concurrency]
dependencies: [shared-ralph-core, shared-atomic-updates]
---

# File Permissions

> "Single-writer principle prevents race conditions – know what you can write to."

## When to Use This Skill

Use **when**:
- Unsure if you can write to a file
- Need to know who owns a specific file
- Resolving file conflicts

Use **proactively**:
- Before writing to any shared file
- When coordinating between agents

---

## Quick Start

<examples>
Example 1: PM writing to prd.json
```json
// ✅ PM CAN write these fields:
{
  "items": [{ "status": "in_progress" }],  // ✅ PM only
  "session": { "iteration": 5 },           // ✅ PM only
  "agents": { "developer": { "status": "working" } }  // ✅ PM only
}
```

Example 2: Developer updating own status
```json
// ✅ Developer CAN update own agent fields:
{
  "agents": {
    "developer": { "lastHeartbeat": "2026-01-23T12:00:00Z", "status": "working" }  // ✅
  }
}
// ❌ CANNOT update other agents' fields
```

Example 3: QA updating validation results
```json
// ✅ QA CAN update validation fields:
{
  "items": [{ "id": "feat-001", "passes": true, "validationResults": {...} }]  // ✅
}
```
</examples>

---

## Core Principle

Each file has a **primary owner** to avoid conflicts. Only the owner may write to that file.

---

## File Ownership

| File | Primary Owner | Other Agents |
|------|---------------|--------------|
| `prd.json.session` | PM | Workers: own `agents.{role}.*` only |
| `prd.json.items[{taskId}]` | PM (creates) | Workers: `status`, `completedAt`, `commit`, `retryCount`, `bugNotes` |
| `prd.json` | PM (fields) | QA: `passes`, `validationResults`, `bugs` |
| Session files | PM | All agents (append-only) |
| Progress files | Respective agent | PM (append notes only) |

---

## Permission Rules

1. **Read-modify-write atomically** - See `shared-atomic-updates`
2. **Only update fields you own** - Never overwrite another agent's data
3. **Append-only for logs** - Never delete or reorder entries
4. **Retry on conflict** - If write fails, re-read and retry once
5. **Use per-agent files** for frequently updated data

---

## What Each Agent CAN Write To

### PM Coordinator

| ✅ Can Write | ❌ Cannot Write |
|-------------|----------------|
| `.claude/session/*` | Source code (`src/`, `server/`, `public/`) |
| `prd.json` - task status fields | Test files |
| `prd.json.session` | Configuration files |
| `prd.json.agents.*` | |
| `coordinator-progress.txt` | |
| `*-progress.txt` (append notes) | |

### Developer Worker

| ✅ Can Write | ❌ Cannot Write |
|-------------|----------------|
| Source code (`src/`, etc.) | `prd.json` (except assigned tasks) |
| `.claude/session/session.log` (append) | `coordinator-progress.txt` |
| `developer-progress.txt` | `qa-progress.txt` |
| `prd.json.agents.developer` | |
| `prd.json.items[{taskId}]` (assigned) | |

### QA Worker

| ✅ Can Write | ❌ Cannot Write |
|-------------|----------------|
| `.claude/session/session.log` (append) | Source code (read-only) |
| `qa-progress.txt` | `coordinator-progress.txt` |
| `prd.json.agents.qa` | `developer-progress.txt` |
| `prd.json.items[{taskId}]` (validation) | |
| `prd.json` (`passes`, `validationResults`, `bugs`) | |

### Tech Artist Worker

| ✅ Can Write | ❌ Cannot Write |
|-------------|----------------|
| `src/assets/` (3D models, textures) | Core game logic (`stores/`, `hooks/`, `utils/`) |
| `src/components/**/*.{materials,shaders,effects}*` | Network code (`server/`) |
| `src/styles/` | `prd.json` task descriptions |
| `src/vfx/` | |
| `techartist-progress.txt` | |

### Game Designer Worker

| ✅ Can Write | ❌ Cannot Write |
|-------------|----------------|
| `docs/design/` | Source code |
| Design artifacts | `prd.json` task descriptions |
| `gamedesigner-progress.txt` | |

---

## Commit Permissions

**ALL agents MUST commit their file changes.**

| Agent | Must Commit | Scope |
|-------|-------------|-------|
| **PM** | ✅ Yes | `prd.json`, session files, retrospectives |
| **Developer** | ✅ Yes | Source files, tests, own agent status |
| **Tech Artist** | ✅ Yes | Assets, visual components, shaders |
| **QA** | ✅ Yes | Validation fields, bug reports |
| **Game Designer** | ✅ Yes | Design docs, GDD, artifacts |

**No Commit Exceptions**: Heartbeat updates, temporary message files.

---

## Concurrency Rules

1. **Never overwrite entire files** - Update specific fields only
2. **Use atomic updates** - Read-modify-write to temp file, then rename
3. **Check file locks** - If `.lock` file exists, wait or retry
4. **Additive updates** - For logs, append only
5. **Field-level ownership** - Multiple agents can update different fields in same file

---

## Conflict Resolution

If you encounter a write conflict:

1. **Re-read the file** - Get latest state
2. **Re-apply your changes** - On top of new state
3. **Write again** - Using atomic pattern
4. **If still conflicts** - Log issue and wait 30 seconds

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-ralph-core` | Session structure and file ownership |
| `shared-atomic-updates` | Atomic update patterns |
| `shared-worker-worktree` | Parallel development coordination |
