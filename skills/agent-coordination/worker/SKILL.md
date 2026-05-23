---
name: worker
description: |
  Worker Self-Service Commands - start, done, status, block.
  Supports Sub-Orchestrator mode for hierarchical task decomposition.

  Pipeline Position: After /assign, Before /collect
  Commands: start, done, status, block, orchestrate, delegate, collect-sub
user-invocable: true
model: opus
version: "6.0.0"
argument-hint: "<start|done|status|block> [b|c|d|terminal-id] [taskId]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000
    - type: command
      command: "/home/palantir/.claude/hooks/worker-preflight.sh"
      timeout: 10000

# =============================================================================
# EFL Pattern Configuration (P1-P6)
# =============================================================================
agent_delegation:
  enabled: true
  default_mode: true
  max_sub_agents: 3
  delegation_strategy: "complexity-based"

parallel_agent_config:
  enabled: true
  agent_count_by_complexity:
    simple: 1
    moderate: 2
    complex: 3

agent_internal_feedback_loop:
  enabled: true
  max_iterations: 3
  validation_criteria:
    - "All subtasks identified and decomposed"
    - "Dependencies between subtasks mapped"
    - "Completion criteria defined for each subtask"
---

# /worker - Worker Self-Service Commands

> **Version:** 6.0.0 | **Model:** opus
> **Pipeline:** /assign -> [/worker] -> /collect
> **EFL:** P1, P2, P6 (Sub-Orchestrator mode)

---

## 1. Purpose

Worker Self-Service Agent that enables workers to:
1. Claim and start assigned tasks (`/worker start`)
2. Mark tasks as complete (`/worker done`)
3. Check current status and progress (`/worker status`)
4. Report blockers to orchestrator (`/worker block`)
5. Decompose tasks into subtasks (`/worker orchestrate`) - Sub-Orchestrator
6. Delegate subtasks (`/worker delegate`) - Sub-Orchestrator
7. Collect sub-results (`/worker collect-sub`) - Sub-Orchestrator

---

## 2. Task API Integration

### Start Task
```javascript
// Find and start assigned task
const myTasks = TaskList().filter(t => t.owner === workerId)
const taskToStart = myTasks.find(t =>
  t.status === "pending" &&
  (!t.blockedBy || t.blockedBy.length === 0)
)

TaskUpdate({
  taskId: taskToStart.id,
  status: "in_progress"
})
```

### Complete Task
```javascript
// Mark task as completed
TaskUpdate({
  taskId: currentTask.id,
  status: "completed"
})

// Move prompt file: pending -> completed
movePromptFile(taskId, "pending", "completed")

// Generate completion manifest with SHA256 hashes
generateCompletionManifest(taskId, workerId)
```

### Sub-Orchestrator Mode
```javascript
// When task.metadata.subOrchestratorMode === true
// Worker can create subtasks
TaskCreate({
  subject: "Subtask 1.1",
  metadata: {
    hierarchyLevel: task.metadata.hierarchyLevel + 1,
    parentTaskId: task.id
  }
})
```

---

## 3. Invocation

### Basic Commands
```bash
/worker start b           # Start as terminal-b
/worker start b 16        # Start terminal-b on task #16
/worker done              # Mark current task complete
/worker status            # Show progress
/worker status b --all    # Show all terminal-b tasks
/worker block "reason"    # Report blocker
```

### Sub-Orchestrator Commands
```bash
/worker orchestrate b     # Decompose current task
/worker delegate b        # Delegate subtasks
/worker collect-sub b     # Collect sub-results
```

### Terminal Shortcuts
| Shortcut | Full ID |
|----------|---------|
| `b` | `terminal-b` |
| `c` | `terminal-c` |
| `d` | `terminal-d` |

---

## 4. Execution Protocol

### /worker start
```javascript
function workerStart(terminalId, specificTaskId = null) {
  // 1. Set worker identity
  setWorkerId(terminalId)

  // 2. Get my tasks
  const myTasks = getMyTasks()
  if (myTasks.length === 0) {
    return { status: "no_tasks", message: "No tasks assigned" }
  }

  // 3. Find task to start (unblocked, pending)
  let taskToStart = specificTaskId
    ? myTasks.find(t => t.id === specificTaskId)
    : myTasks.find(t => t.status === "pending" && isUnblocked(t))

  // 4. Check blockers
  if (taskToStart.blockedBy?.length > 0) {
    const allComplete = taskToStart.blockedBy.every(id =>
      TaskGet({taskId: id}).status === "completed"
    )
    if (!allComplete) return { status: "blocked" }
  }

  // 5. Update status
  TaskUpdate({ taskId: taskToStart.id, status: "in_progress" })

  // 6. Display task details and prompt
  const promptFile = findPromptFile(taskToStart.id)
  displayTaskDetails(taskToStart, promptFile)

  // 7. Update _progress.yaml
  updateProgressFile(workerId, taskToStart.id, "in_progress")
}
```

### /worker done
```javascript
function workerDone(specificTaskId = null) {
  // 1. Find current task
  const currentTask = myTasks.find(t => t.status === "in_progress")

  // 2. Mark completed
  TaskUpdate({ taskId: currentTask.id, status: "completed" })

  // 3. Move prompt file
  movePromptFile(currentTask.id, "pending", "completed")

  // 4. Generate manifest with integrity hashes
  generateCompletionManifest(currentTask.id, workerId)

  // 5. Update progress
  updateProgressFile(workerId, currentTask.id, "completed")

  // 6. Show next task
  const nextTask = myTasks.find(t => t.status === "pending")
  if (nextTask) {
    console.log(`Next: Task #${nextTask.id}`)
  } else {
    console.log("All tasks complete! Ready for /collect")
  }
}
```

### /worker status
```javascript
function workerStatus(showAll = false) {
  const myTasks = getMyTasks()
  const completed = myTasks.filter(t => t.status === "completed")
  const inProgress = myTasks.filter(t => t.status === "in_progress")
  const pending = myTasks.filter(t => t.status === "pending")

  console.log(`
=== Worker Status: ${workerId} ===
Current: ${inProgress[0]?.subject || "None"}
Progress: ${completed.length}/${myTasks.length} (${percent}%)
Blockers: ${blockers.length}
  `)
}
```

### /worker block
```javascript
function workerBlock(reason, taskId = null) {
  const task = taskId ? TaskGet({taskId}) : getCurrentTask()

  // Record blocker
  const blocker = {
    taskId: task.id,
    worker: workerId,
    reason: reason,
    reportedAt: new Date().toISOString()
  }

  // Save to progress file and blocker notification
  addBlockerToProgress(blocker)
  writeBlockerNotification(blocker)
}
```

---

## 5. Sub-Orchestrator Mode

### When Enabled
- Task has `metadata.subOrchestratorMode: true`
- Or skill config has `agent_delegation.default_mode: true`

### Commands
| Command | Purpose |
|---------|---------|
| `/worker orchestrate b` | Decompose task into subtasks |
| `/worker delegate b` | Assign subtasks to sub-agents |
| `/worker collect-sub b` | Aggregate sub-results into L1 |

### Hierarchy Tracking
```javascript
// Parent task at level 0
task.metadata.hierarchyLevel = 0

// Subtasks at level 1
TaskCreate({
  metadata: {
    hierarchyLevel: 1,
    parentTaskId: task.id
  }
})
```

---

## 6. Context Pollution Prevention

L1 summaries are validated and sanitized:
```javascript
const L1_MAX_TOKENS = 500
const L1_MAX_CHARS = 2000

function validateL1Summary(l1Summary) {
  if (l1Summary.length > L1_MAX_CHARS) {
    return { isValid: false, reason: "exceeds size limit" }
  }
  // Check for L2/L3 content patterns
  // ...
}

function sanitizeL1Summary(l1Summary) {
  // Truncate large code blocks
  // Remove file content dumps
  // Limit total length
}
```

---

## 7. Output Files

| Output | Path |
|--------|------|
| L1 Summary | `.agent/prompts/{slug}/outputs/{terminal}/task-{id}-l1-summary.md` |
| L2 Details | `.agent/prompts/{slug}/outputs/{terminal}/task-{id}-l2-summaries.md` |
| L3 Full | `.agent/prompts/{slug}/outputs/{terminal}/task-{id}-l3-details.md` |
| Manifest | `.agent/prompts/{slug}/outputs/{terminal}/task-{id}-manifest.yaml` |

---

## 8. Error Handling

| Error | Recovery |
|-------|----------|
| No tasks assigned | Suggest `/assign` |
| Task not assigned to worker | Show correct owner |
| All tasks blocked | List blockers, suggest wait |
| Already in progress | Show current task |
| Missing blocker reason | Show usage |

---

## 9. Gate 5: Pre-Execution Validation

Via `worker-preflight.sh` hook:
- Verifies `blockedBy` dependencies are completed
- Checks target file access permissions
- Validates prompt file integrity

---

## 10. Version History

| Version | Changes |
|---------|---------|
| 6.0.0 | Deduplicated, V2.1.19 frontmatter, single hooks block |
| 5.2.0 | Auto-Delegation trigger |
| 5.0.0 | EFL Pattern P1, P2, P6 |
| 4.0.0 | Semantic Integrity Manifest |
| 3.2.0 | Context Pollution Prevention |
| 3.1.0 | Gate 5 Shift-Left Validation |
| 3.0.0 | Terminal ID shortcuts |
| 1.0.0 | Initial worker commands |

**End of Skill Documentation**
