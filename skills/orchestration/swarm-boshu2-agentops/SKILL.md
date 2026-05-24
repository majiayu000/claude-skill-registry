---
name: swarm
description: 'Spawn isolated agents for parallel task execution. Pure Claude-native using Task tool. Triggers: "swarm", "spawn agents", "parallel work".'
---

# Swarm Skill

Spawn isolated agents to execute tasks in parallel.

## Architecture (Mayor-First)

```
Mayor (this session)
    |
    +-> Plan: TaskCreate with dependencies
    |
    +-> Identify wave: tasks with no blockers
    |
    +-> Spawn: Task tool (run_in_background=true) for each
    |       Each agent completes its task atomically
    |
    +-> Wait: <task-notification> arrives
    |
    +-> Validate: Review changes when complete
    |
    +-> Repeat: New plan if more work needed
```

## Execution

Given `/swarm`:

### Step 1: Ensure Tasks Exist

Use TaskList to see current tasks. If none, create them:

```
TaskCreate(subject="Implement feature X", description="Full details...")
TaskUpdate(taskId="2", addBlockedBy=["1"])  # Add dependencies after creation
```

### Step 2: Identify Wave

Find tasks that are:
- Status: `pending`
- No blockedBy (or all blockers completed)

These can run in parallel.

### Step 3: Spawn Agents

For each ready task, spawn a background agent:

```
Task(
  subagent_type="general-purpose",
  run_in_background=true,
  prompt="Execute task #<id>: <subject>

<description>

Work autonomously. Create/edit files as needed. Verify your work."
)
```

**Important:** Agents cannot access TaskList/TaskUpdate. Mayor must:
1. Wait for `<task-notification>`
2. Verify work was done
3. Call `TaskUpdate(taskId, status="completed")`

### Step 4: Wait for Notifications

Agents send `<task-notification>` automatically when complete:
- No polling needed
- Mayor receives notification with task result
- Then Mayor updates TaskList and spawns next wave

### Step 5: Validate & Review

When agents complete:
1. Check git status for changes
2. Review diffs
3. Run tests/validation
4. Commit combined work if needed

### Step 6: Repeat if Needed

If more tasks remain:
1. Check TaskList for next wave
2. Spawn new agents
3. Continue until all done

## Example Flow

```
Mayor: "Let's build a user auth system"

1. /plan → Creates tasks:
   #1 [pending] Create User model
   #2 [pending] Add password hashing (blockedBy: #1)
   #3 [pending] Create login endpoint (blockedBy: #1)
   #4 [pending] Add JWT tokens (blockedBy: #3)
   #5 [pending] Write tests (blockedBy: #2, #3, #4)

2. /swarm → Spawns agent for #1 (only unblocked task)

3. Agent #1 completes → #1 now completed
   → #2 and #3 become unblocked

4. /swarm → Spawns agents for #2 and #3 in parallel

5. Continue until #5 completes

6. /vibe → Validate everything
```

## Key Points

- **Pure Claude-native** - No tmux, no external scripts
- **Background agents** - `run_in_background=true` for isolation
- **Wave execution** - Only unblocked tasks spawn
- **Mayor orchestrates** - You control the flow
- **Atomic execution** - Each agent works until task done

## Integration with AgentOps

This ties into the full workflow:

```
/research → Understand the problem
/plan → Decompose into tasks
/swarm → Execute in parallel
/vibe → Validate results
/post-mortem → Extract learnings
```

The knowledge flywheel captures learnings from each agent.

## Task Management Commands

```
# List all tasks
TaskList()

# Mark task complete after notification
TaskUpdate(taskId="1", status="completed")

# Add dependency between tasks
TaskUpdate(taskId="2", addBlockedBy=["1"])
```

## When to Use Swarm

| Scenario | Use |
|----------|-----|
| Multiple independent tasks | `/swarm` (parallel) |
| Sequential dependencies | `/swarm` with blockedBy |
| Mix of both | `/swarm` spawns waves, each wave parallel |

## Why This Works: Ralph Wiggum Pattern

This architecture follows the [Ralph Wiggum Pattern](https://ghuntley.com/ralph/) for autonomous agents.

**Core Insight:** Each `Task(run_in_background=true)` spawn = fresh context.

```
Ralph's bash loop:          Our swarm:
while :; do                 Mayor spawns Task → fresh context
  cat PROMPT.md | claude    Mayor spawns Task → fresh context
done                        Mayor spawns Task → fresh context
```

Both achieve the same thing: **fresh context per execution unit**.

### Why Fresh Context Matters

| Approach | Context | Problem |
|----------|---------|---------|
| Internal loop in agent | Accumulates | Degrades over iterations |
| Mayor spawns agents | Fresh each time | Stays effective at scale |

Making demigods loop internally would violate Ralph - context accumulates within the session. The loop belongs in Mayor (lightweight orchestration), fresh context belongs in demigods (heavyweight work).

### Key Properties

- **Mayor IS the loop** - Orchestration layer, manages state
- **Demigods are atomic** - One task, one spawn, one result
- **TaskList as memory** - State persists in task status, not context
- **Filesystem for artifacts** - Files written, commits made

This is **Ralph + parallelism**: the while loop is distributed across wave spawns, with multiple agents per wave.
