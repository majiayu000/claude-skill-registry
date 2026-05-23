---
name: assign
description: |
  Task Assignment Agent - Assigns Native Tasks to worker terminals,
  updates ownership, and syncs progress tracking.

  Pipeline Position: After /orchestrate, Before /worker
  Handoff: Workers run /worker start
user-invocable: true
model: opus
version: "4.0.0"
argument-hint: "<task-id> <terminal-id> [--sub-orchestrator] | auto"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - TaskUpdate
  - TaskList
  - TaskGet
  - AskUserQuestion
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/parallel-agent.sh"
      timeout: 5000

# =============================================================================
# EFL Pattern Configuration (P1-P6)
# =============================================================================
agent_delegation:
  enabled: true
  default_mode: true
  max_sub_agents: 3
  delegation_strategy: "auto"

parallel_agent_config:
  enabled: true
  agent_count_by_complexity:
    simple: 1
    moderate: 2
    complex: 3

synthesis_config:
  phase_3a_l2_horizontal:
    enabled: true
    validation_criteria:
      - load_balance_check
      - dependency_order_validation
      - terminal_capacity_check
  phase_3b_l3_vertical:
    enabled: true
    validation_criteria:
      - task_terminal_compatibility
      - blocker_resolution_order

selective_feedback:
  enabled: true
  severity_filter: "warning"
  feedback_targets:
    - gate: "ASSIGN"
      action: "block_on_error"

agent_internal_feedback_loop:
  enabled: true
  max_iterations: 3
  validation_criteria:
    - "Each task has exactly one owner"
    - "Blocked tasks assigned after blockers"
    - "Terminal load is balanced"
---

# /assign - Task Assignment to Workers

> **Version:** 4.0.0 | **Model:** opus
> **Pipeline:** /orchestrate -> [/assign] -> /worker
> **EFL:** P1-P6 Complete

---

## 1. Purpose

Task Assignment Agent that:
1. Assigns Native Tasks to terminals via `TaskUpdate(owner=...)`
2. Updates workload-scoped `_progress.yaml`
3. Supports manual and auto-assignment modes
4. Validates dependencies before assignment
5. Enables Sub-Orchestrator mode for hierarchical decomposition

---

## 2. Task API Integration

### Assignment Pattern
```javascript
// Manual assignment
TaskUpdate({
  taskId: taskId,
  owner: terminalId,
  metadata: {
    hierarchyLevel: 0,
    subOrchestratorMode: isSubOrchestrator,
    canDecompose: isSubOrchestrator
  }
})

// Auto assignment - all tasks get Sub-Orchestrator mode
const unassigned = TaskList().filter(t => !t.owner)
for (let i = 0; i < unassigned.length; i++) {
  TaskUpdate({
    taskId: unassigned[i].id,
    owner: `terminal-${String.fromCharCode(98 + i)}`
  })
}
```

### Progress File Update
Updates `_progress.yaml` with:
- Terminal status (idle/working/completed)
- Assigned task ID and phase
- Sub-Orchestrator mode flag
- Hierarchy level

---

## 3. Invocation

```bash
# Manual assignment
/assign 1 terminal-b              # Assign Task #1 to Terminal B
/assign 2 terminal-c --sub-orchestrator  # With decomposition ability

# Auto assignment (Sub-Orchestrator default)
/assign auto                      # Assigns all unassigned tasks

# Workload-specific
/assign --workload {slug} auto
```

---

## 4. Execution Protocol

### Manual Assignment Flow
```javascript
function manualAssign(taskId, terminalId, options = {}) {
  // 1. Validate task exists
  const task = TaskGet({taskId})
  if (!task) return error(`Task #${taskId} not found`)

  // 2. Check if already assigned
  if (task.owner) {
    const confirm = askUser(`Reassign from ${task.owner}?`)
    if (!confirm) return
  }

  // 3. Warn about blockers (but allow assignment)
  if (task.blockedBy?.length > 0) {
    warn(`Task blocked by: ${task.blockedBy.join(', ')}`)
  }

  // 4. Update task owner
  TaskUpdate({
    taskId: taskId,
    owner: terminalId,
    metadata: {
      subOrchestratorMode: options.subOrchestrator || false
    }
  })

  // 5. Update _progress.yaml
  updateProgressFile(taskId, terminalId, task)
}
```

### Auto Assignment Flow
```javascript
function autoAssign() {
  // 1. Get unassigned tasks
  const unassigned = TaskList().filter(t => !t.owner)

  // 2. Prioritize unblocked tasks
  const unblocked = unassigned.filter(t => !t.blockedBy?.length)
  const blocked = unassigned.filter(t => t.blockedBy?.length > 0)

  // 3. Assign to available terminals
  const terminals = ['terminal-b', 'terminal-c', 'terminal-d']
  let assignments = []

  for (let i = 0; i < unblocked.length; i++) {
    assignments.push({
      taskId: unblocked[i].id,
      terminalId: terminals[i % terminals.length],
      canStart: true
    })
  }

  // 4. Execute assignments with Sub-Orchestrator mode
  for (const a of assignments) {
    TaskUpdate({
      taskId: a.taskId,
      owner: a.terminalId,
      metadata: { subOrchestratorMode: true }
    })
  }
}
```

---

## 5. Sub-Orchestrator Mode

When assigned with `--sub-orchestrator`, workers can:
- Decompose their task into subtasks
- Run `/orchestrate` to create child tasks
- Assign subtasks to themselves or other terminals

### Hierarchy Levels
```
Level 0 (Main):       /orchestrate by Main Agent
    |
    +-- Task #1 -----> terminal-b (--sub-orchestrator)
        |
        +-- Level 1:  terminal-b runs /orchestrate
            +-- Subtask #1.1
            +-- Subtask #1.2
```

---

## 6. Output

### Summary Format
```
=== Assignment Summary ===
Total assigned: 3
Can start now: 1
Blocked: 2

Ready to Start:
  terminal-b: /worker start -> Task #1

Blocked:
  terminal-c: Task #2 (blocked by #1)
  terminal-d: Task #3 (blocked by #2)
```

### Worker Instructions
```
terminal-b:
  /worker start
  -> Task #1: {subject}

terminal-c:
  (Wait for blockers)
  -> Task #2 blocked by: 1
```

---

## 7. Error Handling

| Error | Recovery |
|-------|----------|
| Task not found | Show available tasks via TaskList |
| Invalid terminal ID | Warn about naming convention |
| Progress file conflict | Regenerate from TaskList |

---

## 8. Handoff Contract

```yaml
handoff:
  skill: "assign"
  workload_slug: "{slug}"
  status: "completed"
  next_action:
    skill: "/worker"
    arguments: "start"
    reason: "Tasks assigned, workers can start"
```

---

## 9. Version History

| Version | Changes |
|---------|---------|
| 4.0.0 | Deduplicated, V2.1.19 frontmatter, Task API patterns |
| 3.0.0 | Full EFL P1-P6 implementation |
| 2.1.0 | Sub-Orchestrator mode added |
| 1.0.0 | Initial task assignment |

**End of Skill Documentation**
