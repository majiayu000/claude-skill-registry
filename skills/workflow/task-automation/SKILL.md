---
name: task-automation
description: "Execute development tasks from manifest, run parallel agents, verify builds, manage task pipeline. Use when user wants to run tasks, check task status, execute dev loop, or work through the backlog."
allowed-tools: Read, Edit, Bash, Glob, Grep, Task, TodoWrite
user-invocable: true
---

# Task Automation Skill

Automated task execution system for the Journey project. Manages a task manifest and executes tasks via parallel agents.

## When Claude Should Use This Skill

- User says "run tasks", "execute tasks", "dev loop", "work on backlog"
- User asks about task status or pipeline health
- User wants to run multiple tasks in parallel
- User mentions the manifest or available tasks

## Core Concepts

### Task Manifest
Located at `docs/planning/tasks/manifest.json`. Contains:
- Task definitions with ID, title, priority, complexity
- Status tracking (available, claimed, in_progress, completed)
- Dependencies between tasks
- Tags for categorization (backend, frontend, etc.)

### Task Lifecycle
```
available → claimed → in_progress → completed
                  ↓
              blocked/abandoned
```

### Conflict Detection
Tasks conflict if they:
1. Modify the same files (check task spec's "Files to Create/Modify")
2. Both have `backend` tag (may touch server/src/index.ts)
3. Both have `frontend` tag AND modify shared files (App.tsx, routes)

Safe parallel pairs: one backend + one frontend task.

## Workflows

### Single Task Execution
1. Read manifest, find highest priority available task
2. Claim task (update manifest status)
3. Read task file from `docs/planning/tasks/<file>`
4. Execute task (create/modify files per spec)
5. Run build verification (`npm run build`)
6. Update manifest to completed

### Parallel Execution (--parallel N)
1. **Acquire manifest lock** before reading
2. Read manifest, find N non-conflicting available tasks
3. Pre-claim all tasks in manifest (prevents race conditions)
4. **Release manifest lock** after claiming
5. Spawn N background agents via Task tool
6. Each agent works independently on its task
7. Monitor agent outputs for completion
8. **Acquire lock**, update manifest for completed tasks, **release lock**
9. Verify all builds pass

### Manifest Locking Protocol
To prevent race conditions when multiple agents access the manifest:

```bash
# Acquire lock (waits up to 10s if held by another agent)
npx ts-node scripts/manifest-lock.ts acquire <agent-id>

# Release lock when done
npx ts-node scripts/manifest-lock.ts release <agent-id>

# Check lock status
npx ts-node scripts/manifest-lock.ts status

# Force release stale lock (use with caution)
npx ts-node scripts/manifest-lock.ts force-release
```

**Lock Rules:**
- Always acquire lock before reading/modifying manifest
- Release lock immediately after changes are written
- Locks auto-expire after 60 seconds (stale lock protection)
- Lock file: `docs/planning/tasks/manifest.lock` (gitignored)

### Pipeline Check
1. Read manifest
2. Count by status: available, completed, blocked
3. Check if ideation needed (available < threshold)
4. Report pipeline health

### Debt Sweep Integration
Triggered every N cycles (default: 5) during continuous execution:

1. **Check cycle counter** - Track cycles since last debt sweep
2. **Pause execution** when counter hits debt-interval threshold
3. **Run debt sweep** - Scan codebase for new technical debt
4. **Fix eligible items** if `--debt-fix` level is set:
   - Only fix items with effort = trivial or low
   - Fix in severity order: critical → high → medium → low
   - Stop at specified severity level
5. **Update manifests** - `debt-manifest.json` and `debt-report.md`
6. **Report findings** - Show new debt, fixed items, remaining items
7. **Reset counter** and resume task execution

**Debt Sweep Trigger Logic:**
```
cycleCount = cycleCount + 1

if cycleCount >= debtInterval:
    cycleCount = 0
    runDebtSweep()
    
    if debtFixLevel:
        for item in debtItems.sortedBySeverity():
            if item.severity >= debtFixLevel and item.effort in ['trivial', 'low']:
                attemptAutoFix(item)
```

**Auto-Fixable Debt Categories:**
- Security: Remove debug logging of credentials
- Types: Add explicit return types to small functions
- Complexity: Extract obvious helper functions
- Dependencies: Update patch versions
- TODOs: Complete trivial TODOs with clear solutions

## Agent Output Format

All spawned agents MUST output this structured summary:

```
<!-- AGENT_SUMMARY_START -->
{
  "taskId": "<task-id>",
  "status": "completed|partial|failed|blocked",
  "filesCreated": ["<paths>"],
  "filesModified": ["<paths>"],
  "buildStatus": "passed|failed",
  "acceptanceCriteria": {"total": N, "met": N, "failed": N},
  "errors": [],
  "notes": "<summary>"
}
<!-- AGENT_SUMMARY_END -->
```

## Supporting Files

- [parallel-execution.md](parallel-execution.md) - Detailed parallel execution logic
- [manifest-schema.md](manifest-schema.md) - Task manifest structure
- [scripts/agent-status.sh](scripts/agent-status.sh) - Check running agent status

## Usage Examples

**Run single task:**
```
/dev-loop
```

**Run 2 tasks in parallel:**
```
/dev-loop --parallel 2
```

**Continuous with debt sweep every 3 cycles:**
```
/dev-loop --continuous --debt-interval 3
```

**Auto-fix high+ severity debt during continuous run:**
```
/dev-loop --continuous --debt-interval 5 --debt-fix high
```

**Focused feature work (skip debt sweeps):**
```
/dev-loop --continuous --no-debt-sweep
```

**Check status:**
```
/task-status
```

**Natural language (auto-detected):**
- "Let's knock out some tasks"
- "Run the dev loop"
- "What tasks are available?"
- "Execute P1 tasks in parallel"
- "Run tasks and clean up debt along the way"
- "Do a debt sweep every 3 tasks"
