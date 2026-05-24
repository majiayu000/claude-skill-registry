---
name: shared-state
description: File ownership, atomic updates using Edit tool, concurrency rules for Ralph agents
category: orchestration
---

# Shared State

> "Single-writer principle prevents race conditions. Use Edit tool for atomic updates."

---

## Core Principle

Each file has a **primary owner** to avoid conflicts. Only the owner may write to that file.

---

## File Ownership Matrix (v2.0 - Per-Agent State Files)

### State Files

| File                          | Primary Owner   | Other Agents          | Size  | Purpose                       |
| ----------------------------- | --------------- | --------------------- | ----- | ------------------------------ |
| `current-task-developer.json`   | Developer       | PM (read-only)        | ~1KB  | Developer's task state        |
| `current-task-qa.json`          | QA              | PM (read-only)        | ~1KB  | QA's task state               |
| `current-task-techartist.json`  | Tech Artist     | PM (read-only)        | ~1KB  | Tech Artist's task state      |
| `current-task-gamedesigner.json | Game Designer   | PM (read-only)        | ~1KB  | Game Designer's task state    |
| `current-task-pm.json`          | PM              | Workers (read-only)   | ~2KB  | PM coordinator state          |
| `prd.json`                    | PM (full access) | **Workers DO NOT read** | 110KB | Full PRD (PM-ONLY in v2.0)     |

### Session Files

| File                       | Primary Owner    | Other Agents                                                                    |
| -------------------------- | ---------------- | ------------------------------------------------------------------------------- |
| `prd.json.session`         | PM               | Workers check their state file for sessionStatus (NOT prd.json directly)        |
| `prd.json.items[{taskId}]` | PM (creates)     | Workers do NOT update directly - PM updates based on messages                    |
| `prd.json`                 | PM (fields)      | Workers DO NOT read in v2.0 - PM handles all PRD updates                         |
| `session.log`              | All agents       | All append-only                                                                 |
| `coordinator-progress.txt` | PM               | All append-only                                                                 |
| `{agent}-progress.txt`     | Respective agent | PM may append notes                                                             |

### Key Changes in v2.0

**OLD (v1.x):**
- Workers read prd.json (110KB) for status
- Workers updated prd.json.agents.{role} directly

**NEW (v2.0):**
- Workers read ONLY their ~1KB state file
- Workers update ONLY their state file
- PM reads all state files and syncs to prd.json
- Workers NEVER read prd.json (saves 109KB per worker read)

---

## What Each Agent CAN Write To

### PM Coordinator

| Can Write                  | Notes                                                                             |
| -------------------------- | --------------------------------------------------------------------------------- |
| `.claude/session/*`        | All session files                                                                 |
| `prd.json`                 | **FULL ACCESS** - Task status fields: `passes`, `status`, `assignedAt`, `assignedTo`, `completedAt` |
| `prd.json.session`         | Full ownership of session state                                                   |
| `prd.json.agents.*`        | Full ownership of agent status tracking                                           |
| `current-task-pm.json`       | Full ownership of coordinator state                                               |
| `current-task-*.md`        | **Reads all** worker state files, **WRITES** to update worker task assignments     |
| `coordinator-progress.txt` | Full ownership                                                                    |
| `developer-progress.txt`   | May append notes                                                                  |
| `qa-progress.txt`          | May append notes                                                                  |
| ❌ Source code             | Read-only                                                                         |
| ❌ Test files              | Read-only                                                                         |
| ❌ Config files            | Read-only                                                                         |

### Developer Worker

| Can Write                                | Notes                                                         |
| ---------------------------------------- | ------------------------------------------------------------- |
| `.claude/session/session.log`            | Append log entries                                            |
| `.claude/session/developer-progress.txt` | Full ownership                                                |
| `current-task-developer.json`              | **PRIMARY STATE FILE** - Update: `status`, `lastSeen`, `currentTaskId` |
| ❌ `prd.json`                            | **DO NOT READ** (110KB - PM only)                             |
| Source files (`src/`, etc.)              | Full ownership                                                |
| ❌ `coordinator-progress.txt`            | Read-only                                                     |
| ❌ `qa-progress.txt`                     | Read-only                                                     |

### QA Worker

| Can Write                         | Notes                                                |
| --------------------------------- | ---------------------------------------------------- |
| `.claude/session/session.log`     | Append log entries                                   |
| `.claude/session/qa-progress.txt` | Full ownership                                       |
| `current-task-qa.json`              | **PRIMARY STATE FILE** - Update: `status`, `lastSeen`, `currentTaskId`, `passes` |
| ❌ `prd.json`                      | **DO NOT READ** (110KB - PM only)                    |
| Test files (`src/tests/`, `tests/e2e/`) | Full ownership                                    |
| ❌ Source code                    | Read-only (validates only)                           |
| ❌ `coordinator-progress.txt`     | Read-only                                            |
| ❌ `developer-progress.txt`       | Read-only                                            |

### Game Designer Worker

| Can Write                                   | Notes                                           |
| ------------------------------------------- | ----------------------------------------------- |
| `.claude/session/session.log`               | Append log entries                              |
| `.claude/session/gamedesigner-progress.txt` | Full ownership                                  |
| `current-task-gamedesigner.json`              | **PRIMARY STATE FILE** - Update: `status`, `lastSeen`, `currentTaskId` |
| `docs/design/`                              | Full ownership of design artifacts              |
| ❌ `prd.json`                                | **DO NOT READ** (110KB - PM only)               |
| ❌ Source code                              | Read-only                                       |
| ❌ `prd.json` task descriptions             | Read-only (PM only)                             |

### Tech Artist Worker

| Can Write                                          | Notes                                           |
| -------------------------------------------------- | ----------------------------------------------- |
| `.claude/session/session.log`                      | Append log entries                              |
| `.claude/session/techartist-progress.txt`          | Full ownership                                  |
| `current-task-techartist.json`                       | **PRIMARY STATE FILE** - Update: `status`, `lastSeen`, `currentTaskId` |
| `src/assets/`                                      | All 3D models, textures, materials              |
| `src/components/**/*.{materials,shaders,effects}*` | Visual components                               |
| `src/styles/`                                      | UI styles                                       |
| `src/vfx/`                                         | Particle systems                                |
| ❌ `prd.json`                                      | **DO NOT READ** (110KB - PM only)               |
| ❌ Core game logic                                 | Read-only (store/, hooks/, utils/)              |
| ❌ Network code                                    | Read-only (server/)                             |

---

## Commit Permissions

**ALL agents MUST commit their file changes.**

| Agent             | Must Commit | Commit Scope                                                                                |
| ----------------- | ----------- | ------------------------------------------------------------------------------------------- |
| **PM**            | ✅ Yes      | `prd.json`, `current-task-*.md` (all), `.claude/session/coordinator-progress.txt`, skill files, retrospectives |
| **Developer**     | ✅ Yes      | Source files, tests, `current-task-developer.json`, own progress files                       |
| **Tech Artist**   | ✅ Yes      | Assets, shaders, visual components, `current-task-techartist.json`, own progress files      |
| **QA**            | ✅ Yes      | `current-task-qa.json`, bug reports, own progress files, test files                         |
| **Game Designer** | ✅ Yes      | `docs/design/`, GDD, `current-task-gamedesigner.json`, own progress files                   |

**Commit Format** (from `shared-core`):

```
[ralph] [{AGENT}] {TASK_ID}: {Brief description}

- Change 1
- Change 2

PRD: {TASK_ID} | Agent: {AGENT} | Iteration: {N}
```

**No Commit Exceptions:**

- Heartbeat updates (`prd.json.agents.{agent}.lastSeen` timestamps)
- Temporary message files (deleted after processing)

---

## Atomic Updates Using Edit Tool

**The Edit tool handles atomic writes automatically.** No manual temp file pattern needed.

### Using Edit Tool

**Step 1:** Read the file

```
Read: prd.json
```

**Step 2:** Use Edit tool to make changes

```
Edit: prd.json
  Replace: "status": "pending"
  With: "status": "assigned"
```

The Edit tool internally:

1. Reads the file
2. Applies your changes
3. Writes atomically (temp file + rename)

### Edit Tool vs Manual Pattern

| Approach         | Lines of Code | Safe?                |
| ---------------- | ------------- | -------------------- |
| Manual temp file | 5+ lines      | Risky if interrupted |
| **Edit tool**    | 1 call        | ✅ Safe              |

**❌ DO NOT use manual temp file pattern:**

```bash
# Don't do this anymore
echo "$NEW_STATE" > file.json.tmp && mv file.json.tmp file.json
```

**✅ DO use Edit tool instead:**

```
Read: file.json
Edit: file.json
```

### Master Branch Coordination (Worktree System)

**When working in a git worktree, ALL coordination files must be updated in the master branch.**

Worktree system uses isolated branches for code/assets, but ALL state coordination must happen in master branch to ensure:

- PM sees worker status immediately
- Watchdog monitors heartbeats
- Message queue works for all agents

**What Goes to Master Branch:**
| File | Purpose |
|------|---------|
| `prd.json` | Task status, agent status, session state |
| `.claude/session/messages/` | Event queue |
| `.claude/session/*.json` | State files |

**What Goes to Worktree Branch:**
| Directory | Purpose |
|-----------|---------|
| `src/` | Code changes |
| `src/assets/` | Asset changes |

**From worktree, access master branch:**

```
Read: ../agentic-threejs/prd.json
Edit: ../agentic-threejs/prd.json
```

---

## Concurrency Rules

1. **Read-modify-write atomically** — Use Edit tool
2. **Only update fields you own** — Never overwrite another agent's data
3. **Append-only for logs** — Never delete or reorder entries
4. **Retry on conflict** — If write fails, re-read and retry once
5. **Use per-agent files** for frequently updated data

---

## Conflict Resolution

If you encounter a write conflict:

1. **Re-read the file** — Get latest state
2. **Re-apply your changes** — On top of new state
3. **Write again** — Using Edit tool
4. **If still conflicts** — Log issue, wait 30 seconds

---

## When Atomic Updates Matter Most

- **High-contention files** — `prd.json` (session state, agent status, task items)
- **Shared log files** — Use append-only instead
- **PRD file** — Multiple agents may update different fields

## When Atomic Updates Don't Apply

- **Agent-specific files** — `{agent}-progress.txt` (only one writer)
- **Append-only logs** — Don't need atomic pattern
- **New file creation** — No existing content to protect

---

## Logging Best Practices

- **Use structured logs** — JSON format where possible
- **Include timestamps** — ISO 8601 format
- **Include agent identifier** — Who made the change
- **Append only** — Never rewrite log files
- **Archive, don't delete** — PM may archive old logs

---

## Anti-Patterns

| Don't                                  | Do Instead                  |
| -------------------------------------- | --------------------------- |
| Use PowerShell Get-Content/Set-Content | Use Read/Write tools        |
| Manual temp file + Move-Item           | Use Edit tool               |
| Overwrite entire files                 | Update specific fields only |
| Modify other agents' sections          | Only update your own        |
| Delete log entries                     | Append only                 |

---

## References

- `shared-core` — Commit format, session structure
- `shared-messaging` — Message queue ownership
- `shared-worktree` — Git worktree setup
