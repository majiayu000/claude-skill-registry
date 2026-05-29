---
name: tasks
description: Autonomous task management with execution loop. Creates tasks, executes them, spawns subtasks when blocked, and NEVER stops until all tasks are complete.
allowed-tools: TaskCreate, TaskUpdate, TaskList, TaskGet, Task, TaskOutput, Read, Write, Edit, Bash, Glob, Grep
user-invocable: true
---

# /tasks - Autonomous Task Management

**Core Principle: NEVER STOP until all tasks are complete.**

This skill manages tasks AND executes them autonomously. When blockers are found, it creates subtasks. When agents are spawned, it waits for them using `TaskOutput(block=true)`.

## Quick Commands

| Command | What It Does |
|---------|--------------|
| `/tasks` | List all current tasks |
| `/tasks add <description>` | Create a new task |
| `/tasks done <id>` | Mark task as completed |
| `/tasks fix <description>` | Create a fix/bug task |
| `/tasks test <description>` | Add a testing task |
| `/tasks run` | **Execute all pending tasks autonomously** |
| `/tasks run <id>` | Execute specific task |

---

## CRITICAL: Autonomous Execution Loop

When `/tasks run` is invoked (or when tasks exist and user expects work), the agent MUST follow this loop:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS EXECUTION LOOP                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. TaskList() → Get all tasks                                   │
│     │                                                            │
│     ▼                                                            │
│  2. Filter: pending tasks with no blockedBy                      │
│     │                                                            │
│     ├─► If none ready AND some blocked → resolve_blockers()      │
│     │                                                            │
│     ├─► If none ready AND all complete → EXIT (success)          │
│     │                                                            │
│     ▼                                                            │
│  3. Pick highest priority ready task                             │
│     │                                                            │
│     ▼                                                            │
│  4. TaskUpdate(taskId, status="in_progress")                     │
│     │                                                            │
│     ▼                                                            │
│  5. Execute task (may spawn sub-agents)                          │
│     │                                                            │
│     ├─► If sub-agent spawned:                                    │
│     │   TaskOutput(task_id, block=true, timeout=300000)          │
│     │   ⚠️ MUST WAIT - Never proceed without result              │
│     │                                                            │
│     ├─► If blocker found:                                        │
│     │   TaskCreate(blocker_task)                                 │
│     │   TaskUpdate(current_task, addBlockedBy=[blocker_id])      │
│     │   → Continue loop (pick next ready task)                   │
│     │                                                            │
│     ├─► If error/failure:                                        │
│     │   TaskCreate(fix_task) with "Fix:" prefix                  │
│     │   → Continue loop                                          │
│     │                                                            │
│     ▼                                                            │
│  6. TaskUpdate(taskId, status="completed")                       │
│     │                                                            │
│     ▼                                                            │
│  7. LOOP BACK TO STEP 1 (never exit early)                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ MANDATORY RULES

### Rule 1: ALWAYS Wait for Sub-Agents

When you spawn a sub-agent via `Task()`:

```javascript
// WRONG - Don't proceed without waiting
Task({ subagent_type: "Explore", prompt: "...", run_in_background: true })
// Continues immediately without result ❌

// CORRECT - Always wait with TaskOutput
const agent = Task({ subagent_type: "Explore", prompt: "...", run_in_background: true })
TaskOutput({ task_id: agent.id, block: true, timeout: 300000 })
// Only proceeds after agent completes ✅
```

### Rule 2: NEVER Stop Mid-Execution

These phrases are FORBIDDEN during execution:
- "I'll stop here and let you know..."
- "Would you like me to continue?"
- "The next step would be..."
- "I recommend we..."
- "⏸️ PAUSED PENDING DEPLOYMENT" (use polling instead!)

Instead: **Just do it.** Create tasks, execute them, spawn agents, wait for results.

**Special case - Deployments:** When a task requires waiting for deployment:
- **DO NOT** stop and ask user to verify
- **DO** poll using `scripts/wait_for_deployment.py`
- **DO** create timeout task if deployment fails
- **DO** continue with other unblocked tasks

### Rule 3: Create Subtasks for Blockers

When a blocker is discovered:

```javascript
// 1. Create the blocker task
const blockerTask = TaskCreate({
  subject: "Investigate API authentication failure",
  description: "Task X failed because API returned 401. Need to check token validity.",
  activeForm: "Investigating auth failure..."
})

// 2. Mark current task as blocked
TaskUpdate({
  taskId: currentTaskId,
  addBlockedBy: [blockerTask.id]
})

// 3. Continue loop - don't stop!
// The loop will pick up the blocker task next
```

### Rule 4: Dynamic Task Creation

When executing reveals new work:

```javascript
// During execution of "Implement user auth"
// Discovered: Need database migration first

TaskCreate({
  subject: "Create users table migration",
  description: "Discovered during auth implementation - users table doesn't exist",
  activeForm: "Creating migration..."
})

// Continue with current task or mark blocked as appropriate
```

---

## Execution Patterns

### Pattern 1: Sequential Task Execution

```javascript
async function executeAllTasks() {
  while (true) {
    const tasks = TaskList()
    const pending = tasks.filter(t => t.status === 'pending' && !t.blockedBy?.length)
    const inProgress = tasks.filter(t => t.status === 'in_progress')
    const completed = tasks.filter(t => t.status === 'completed')

    // Exit condition: all done
    if (pending.length === 0 && inProgress.length === 0) {
      console.log(`✅ All ${completed.length} tasks completed!`)
      return
    }

    // Get next ready task
    const nextTask = pending[0]
    if (!nextTask) {
      // All remaining tasks are blocked - resolve blockers
      await resolveBlockers(tasks)
      continue
    }

    // Execute
    TaskUpdate({ taskId: nextTask.id, status: 'in_progress' })
    await executeTask(nextTask)
    TaskUpdate({ taskId: nextTask.id, status: 'completed' })
  }
}
```

### Pattern 2: Context-Aware Parallel Execution

**CRITICAL: Limit parallel agents to prevent context overflow.**

```javascript
// ⚠️ CONTEXT LIMITS - NEVER exceed these:
const MAX_PARALLEL_AGENTS = 3  // Absolute max per wave
const WAVE_SIZE = 3            // Process in waves of 3

// WRONG - Will overflow context with 7 agents
for (const task of allTasks) {  // 7 tasks
  Task({ run_in_background: true })  // ❌ 7 concurrent = context overflow
}

// CORRECT - Process in waves of 3
const waves = chunkArray(independentTasks, WAVE_SIZE)

for (const wave of waves) {
  // Spawn wave (max 3 agents)
  const agents = wave.map(task => Task({
    subagent_type: "Explore",
    model: "haiku",  // Use haiku for investigations (less verbose)
    prompt: `${task.description}\n\nRETURN ONLY: 1-line status + 1-line action needed. MAX 50 words.`,
    run_in_background: true
  }))

  // Wait for this wave to complete BEFORE starting next
  for (const agent of agents) {
    TaskOutput({ task_id: agent.id, block: true, timeout: 120000 })
  }

  // Aggregate wave results, then continue to next wave
}
```

### Pattern 2b: File-Based Agent Output (for large investigations)

When agents may return large outputs, have them write to files:

```javascript
// Agent prompt for file-based output
Task({
  subagent_type: "Explore",
  prompt: `
    Investigate: ${task.description}

    IMPORTANT - OUTPUT FORMAT:
    1. Write full findings to: .claude/rlm_state/results/${task.id}.json
    2. Return ONLY this JSON to me:
       {"status": "done|blocked|error", "summary": "<20 words>", "file": "<path>"}

    Do NOT return full findings in your response.
  `,
  run_in_background: true
})

// Main agent reads summaries (small), then files if needed
```

### Pattern 2c: Investigation Wave Sizing

| Task Count | Strategy | Wave Size | Notes |
|------------|----------|-----------|-------|
| 1-3 | Direct parallel | All | Safe |
| 4-6 | 2 waves | 3 | Process, aggregate, continue |
| 7-10 | 3-4 waves | 3 | Risk of overflow if not careful |
| 10+ | Sequential or RLM | 1-2 | Use /rlm methodology instead |

### Pattern 3: Blocker Resolution

```javascript
function resolveBlockers(tasks) {
  const blocked = tasks.filter(t => t.blockedBy?.length > 0)

  for (const task of blocked) {
    for (const blockerId of task.blockedBy) {
      const blocker = TaskGet({ taskId: blockerId })
      if (blocker.status === 'pending') {
        // Execute the blocker first
        TaskUpdate({ taskId: blockerId, status: 'in_progress' })
        executeTask(blocker)
        TaskUpdate({ taskId: blockerId, status: 'completed' })
      }
    }
  }
}
```

### Pattern 4: Deployment Polling (CRITICAL FOR AUTONOMOUS EXECUTION)

**Problem:** Deployments (Frappe migrations, Vercel builds) are async. Stopping to wait for user = work blocked for hours.

**Solution:** Poll deployments using `scripts/wait_for_deployment.py`

**When to use:**
- After committing backend changes that require migration
- After pushing frontend changes that need Vercel build
- When tests are blocked by deployment status

**Frappe Migration Polling:**
```python
from scripts.wait_for_deployment import wait_for_frappe_migration
import os

# Get credentials from Doppler
FRAPPE_API_KEY = os.popen('doppler secrets get FRAPPE_API_KEY --project bei-erp --config dev --plain').read().strip()
FRAPPE_API_SECRET = os.popen('doppler secrets get FRAPPE_API_SECRET --project bei-erp --config dev --plain').read().strip()

# After triggering migration, wait for it
success = wait_for_frappe_migration(
    doctype="BEI Payment Request",
    field="rfp_type",
    api_key=FRAPPE_API_KEY,
    api_secret=FRAPPE_API_SECRET,
    max_wait_seconds=300,  # 5 minutes
    poll_interval=30
)

if not success:
    # Timeout - create task to verify manually later
    TaskCreate({
        subject: "[BUG] Migration timeout - needs verification",
        description: "Migration did not complete within 5 minutes. DocType changes may not be applied. Check GitHub Actions logs.",
        activeForm: "Documenting timeout..."
    })
    # Continue with other tasks anyway
```

**Vercel Deployment Polling:**
```python
from scripts.wait_for_deployment import wait_for_vercel_deployment

# After git push to main (auto-triggers Vercel)
success = wait_for_vercel_deployment(
    url="https://my.bebang.ph/dashboard/accounting",
    max_wait_seconds=120,  # 2 minutes
    poll_interval=15
)

if not success:
    # Timeout - create task
    TaskCreate({
        subject: "[BUG] Vercel deployment timeout",
        description: "Deployment did not go live within 2 minutes. Check Vercel dashboard for build status.",
        activeForm: "Documenting timeout..."
    })
```

**Integration with Task Loop:**
```javascript
async function executeTask(task) {
  // Normal execution
  await performTaskWork(task)

  // If task involved code changes requiring deployment
  if (taskRequiresDeployment(task)) {
    // Trigger deployment (commit, push, GitHub Action)
    await triggerDeployment()

    // POLL - Don't stop!
    const deployed = await pollDeployment()

    if (!deployed) {
      // Create timeout task but mark current task complete
      TaskCreate({
        subject: `[VERIFY] ${task.subject} - deployment timeout`,
        description: `Task completed but deployment timeout. Manual verification needed.`
      })
    }
  }

  // Mark complete and continue loop
  TaskUpdate({ taskId: task.id, status: 'completed' })
}
```

**Recommended Timeouts:**
| Deployment Type | Max Wait | Poll Interval | Rationale |
|-----------------|----------|---------------|-----------|
| Frappe Migration | 300s (5 min) | 30s | Migrations can be slow |
| Vercel Build | 120s (2 min) | 15s | Builds usually fast |
| Docker Build | 600s (10 min) | 60s | Can be very slow |

---

## Command Reference

### `/tasks` - List Tasks

```javascript
TaskList()
// Display as formatted table:
// | ID | Status | Subject                           | Blocked By |
// |----|--------|-----------------------------------|------------|
// | 1  | ✅     | Set up database                   |            |
// | 2  | 🔄     | Implement auth                    |            |
// | 3  | ⏳     | Build dashboard                   | #4         |
// | 4  | ⏳     | Create API endpoints              |            |
```

### `/tasks add <description>` - Create Task

```javascript
TaskCreate({
  subject: description,
  description: `Created during development.\n\nContext: Current work session.`,
  activeForm: `Working on ${description.substring(0, 30)}...`
})
```

### `/tasks done <id>` - Complete Task

```javascript
TaskUpdate({
  taskId: id,
  status: "completed"
})
```

### `/tasks fix <description>` - Create Fix Task

```javascript
TaskCreate({
  subject: `Fix: ${description}`,
  description: `Bug/issue discovered:\n\n${description}\n\nMust be fixed before continuing.`,
  activeForm: `Fixing ${description.substring(0, 25)}...`
})
```

### `/tasks test <description>` - Create Test Task

```javascript
TaskCreate({
  subject: `Test: ${description}`,
  description: `Testing task:\n\n${description}`,
  activeForm: `Testing ${description.substring(0, 25)}...`
})
```

### `/tasks run` - Execute All Tasks

Triggers the **Autonomous Execution Loop**. Will not stop until:
- All tasks are completed, OR
- An unrecoverable error occurs (creates fix task and continues)

---

## Status Icons

| Icon | Status |
|------|--------|
| ⏳ | Pending |
| 🔄 | In Progress |
| ✅ | Completed |
| 🚫 | Blocked (has blockedBy) |

---

## Error Handling

### Recoverable Errors

Create a fix task and continue:

```javascript
try {
  await executeTask(task)
} catch (error) {
  TaskCreate({
    subject: `Fix: ${task.subject} - ${error.message}`,
    description: `Task failed with error:\n\n${error.stack}\n\nOriginal task: ${task.description}`,
    activeForm: `Fixing error...`
  })
  // Don't stop - continue to next task
}
```

### Unrecoverable Errors

Only stop if the entire system is broken:

```javascript
// These warrant stopping:
// - Claude Code itself crashes
// - No tasks exist and user hasn't requested any
// - Explicit user interrupt

// These do NOT warrant stopping:
// - API errors (create retry task)
// - Missing files (create investigation task)
// - Test failures (create fix task)
// - Syntax errors (create fix task)
```

---

## Integration with Other Skills

| Skill | When to Use |
|-------|-------------|
| `/agent-kickoff` | Full development workflow (uses /tasks internally) |
| `/test-full-cycle` | Comprehensive E2E testing (spawns test tasks) |
| `/local-frappe` | Testing Python changes (task may reference) |
| `/pr-deploy` | Deployment (often final task in a chain) |

---

## Examples

### Example 1: Simple Task List

```
User: /tasks

Agent:
| ID | Status | Subject                           |
|----|--------|-----------------------------------|
| 1  | ✅     | Set up project structure          |
| 2  | 🔄     | Implement user authentication     |
| 3  | ⏳     | Create dashboard UI               |
```

### Example 2: Autonomous Execution

```
User: /tasks run

Agent: Starting autonomous execution loop...

📋 Task #2: Implement user authentication
   Status: in_progress

   Spawning agent to research auth patterns...
   [TaskOutput waiting with block=true]

   Agent returned: Recommend JWT with refresh tokens

   Creating auth middleware...
   [Code written to src/middleware/auth.ts]

   ⚠️ Blocker found: Database connection not configured

   Creating subtask: "Configure database connection"
   Task #2 now blocked by Task #4

📋 Task #4: Configure database connection
   Status: in_progress

   Reading existing config...
   Creating database config...
   [Code written to src/config/database.ts]

   ✅ Task #4 completed

📋 Task #2: Implement user authentication (unblocked)
   Continuing implementation...

   ✅ Task #2 completed

📋 Task #3: Create dashboard UI
   Status: in_progress
   ...

✅ All 4 tasks completed!
```

---

## Best Practices

1. **Atomic Tasks** - One task = one outcome
2. **Clear Subjects** - "Add login endpoint" not "Do login stuff"
3. **Immediate Creation** - Don't let work pile up untracked
4. **Always Wait** - Never proceed without sub-agent results
5. **Auto-Create Subtasks** - Blockers become tasks automatically
6. **Never Stop** - Keep looping until truly done

---

## Context Limit Prevention

**Problem:** Running many parallel agents causes context overflow when all return large outputs.

**Solution:** Wave-based execution with compressed outputs.

### Rules

| Rule | Limit | Reason |
|------|-------|--------|
| Max parallel agents | 3 | Each agent returns ~2-5K tokens |
| Agent output | 50 words max | Summary only, details to file |
| Model for investigations | haiku | Less verbose than sonnet |
| Wave completion | Required | Aggregate before next wave |

### Context Budget

```
Available context: ~180K tokens
Reserved for conversation: ~50K
Available for agent outputs: ~130K

Per-agent safe output: ~10K tokens
Max safe parallel agents: 130K / 10K = 13

BUT agent outputs vary widely, so use conservative limit:
Safe parallel agents: 3 (with full output)
Safe parallel agents: 5-6 (with compressed output)
```

### Compressed Output Prompt

Always include this in agent prompts for investigations:

```
IMPORTANT - CONTEXT LIMIT PREVENTION:
Return ONLY a brief summary (max 50 words):
- Status: done/blocked/needs-work
- Finding: 1-2 sentences
- Action: What to do next (if any)

If you have detailed findings, write them to:
.claude/rlm_state/results/<task_id>.md
```

### Recovery from Context Overflow

If context limit is hit:
1. Run `/compact` immediately
2. Reduce wave size to 2 agents
3. Enforce compressed output format
4. Consider using /rlm for file-based aggregation
