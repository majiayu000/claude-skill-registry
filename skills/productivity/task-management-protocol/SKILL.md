---
name: task-management-protocol
description: Protocol for task synchronization, context handoff, and cross-session coordination using Claude Code task tools. Ensures agents properly update tasks with findings and enables seamless work continuation.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [TaskCreate, TaskList, TaskGet, TaskUpdate, Read, Write]
best_practices:
  - Always call TaskList() at session start and after completion
  - Update task descriptions with discoveries as they happen
  - Use structured metadata for context handoff
  - Never mark complete without summary metadata
  - Check for blocked tasks after completing work
error_handling: strict
streaming: supported
---

# Task Management Protocol

Standardized protocol for task synchronization, progress tracking, and context handoff between agents and sessions using Claude Code's native task tools.

## Problem Statement

Background agents complete work but main sessions don't receive notifications. Agents don't update task descriptions with findings. No protocol exists for structured context handoff between agents or sessions.

**This skill solves:**

1. Lost context when sessions end or agents complete
2. Background agent findings not surfacing to main session
3. Duplicate work due to poor task visibility
4. No structured way to pass information between agents

## Core Tools Reference

| Tool              | Purpose                    | When to Use                         |
| ----------------- | -------------------------- | ----------------------------------- |
| `TaskList()`      | List all tasks with status | Start of work, after completion     |
| `TaskGet(id)`     | Get full task details      | Before starting assigned task       |
| `TaskCreate(...)` | Create new task            | Planning phase, discovered subtasks |
| `TaskUpdate(...)` | Update status/metadata     | Progress, discoveries, completion   |

## The Protocol

### Phase 1: Session Start (MANDATORY)

**Before doing ANY work, execute this sequence:**

```javascript
// Step 1: Check existing tasks
TaskList();

// Step 2: If assigned task exists, read full details
TaskGet({ taskId: '<assigned-id>' });

// Step 3: Claim the task
TaskUpdate({
  taskId: '<assigned-id>',
  status: 'in_progress',
  activeForm: 'Working on <task-subject>',
});
```

**Why this matters:**

- Prevents duplicate work (see what's already in progress)
- Gets full context from task description
- Signals to other agents/sessions that work has started

### Phase 2: During Work (Progress Updates)

**Update tasks when you:**

- Discover important information
- Find blockers
- Identify subtasks
- Make significant progress

#### Discovery Update Pattern

```javascript
// When you discover something important
TaskUpdate({
  taskId: 'X',
  description: `ORIGINAL: <original-description>

## Discoveries (${new Date().toISOString().split('T')[0]})
- Found: <what you discovered>
- Files: <relevant files>
- Impact: <why this matters>`,
  metadata: {
    discoveredFiles: ['path/to/file1.ts', 'path/to/file2.ts'],
    discoveries: ['Pattern X found', 'Dependency Y required'],
    lastUpdated: new Date().toISOString(),
  },
});
```

#### Blocker Update Pattern

```javascript
// When you hit a blocker
TaskUpdate({
  taskId: 'X',
  description: `<existing-description>

## BLOCKED (${new Date().toISOString().split('T')[0]})
- Blocker: <what's blocking>
- Needs: <what's required to unblock>
- Workaround: <possible workaround if any>`,
  metadata: {
    status: 'blocked',
    blocker: 'Description of blocker',
    blockerType: 'dependency|permission|information|external',
    needsFrom: 'user|other-agent|external-system',
  },
});
```

#### Subtask Creation Pattern

```javascript
// When you discover subtasks
TaskCreate({
  subject: 'Subtask: <specific-task>',
  description: `Parent: Task #X

## Context
<why this subtask exists>

## Scope
<specific work to be done>

## Acceptance Criteria
- [ ] <criterion 1>
- [ ] <criterion 2>`,
  activeForm: 'Working on <subtask>',
});

// Link to parent
TaskUpdate({
  taskId: '<new-subtask-id>',
  addBlockedBy: ['X'], // This subtask blocks parent completion
});
```

### Phase 3: Completion (MANDATORY)

**Never mark a task complete without structured metadata:**

```javascript
TaskUpdate({
  taskId: 'X',
  status: 'completed',
  description: `<original-description>

## Completed (${new Date().toISOString().split('T')[0]})
- Summary: <one-line summary of what was done>
- Files modified: <list>
- Tests: <passed/added/none>`,
  metadata: {
    summary: 'Concise summary of completed work',
    filesModified: ['path/to/file1.ts', 'path/to/file2.ts'],
    filesCreated: ['path/to/new.ts'],
    testsAdded: true,
    testsPassing: true,
    outputArtifacts: ['.claude/context/reports/my-report.md'],
    nextSteps: ['Optional follow-up', 'Another consideration'],
    completedAt: new Date().toISOString(),
  },
});

// Check for newly unblocked tasks
TaskList();
```

### Phase 4: Session End / Handoff

**Before ending a session with incomplete work:**

```javascript
// Update all in-progress tasks with current state
TaskUpdate({
  taskId: 'X',
  description: `<existing-description>

## Session Paused (${new Date().toISOString().split('T')[0]})
- Progress: <what was accomplished>
- Current state: <where things stand>
- Next step: <immediate next action>
- Files to review: <key files>`,
  metadata: {
    sessionPaused: true,
    progress: '60%',
    currentState: 'Description of current state',
    immediateNextStep: 'The very next thing to do',
    keyFiles: ['file1.ts', 'file2.ts'],
    keyDecisions: ['Decision 1', 'Decision 2'],
    pausedAt: new Date().toISOString(),
  },
});
```

## Context Handoff Structure

### Metadata Schema for Handoff

Use this consistent structure for context handoff between agents:

```typescript
interface TaskHandoffMetadata {
  // Progress tracking
  status?: 'not_started' | 'in_progress' | 'blocked' | 'completed';
  progress?: string; // e.g., "60%", "3/5 steps"

  // Discovery context
  discoveredFiles?: string[];
  discoveries?: string[];
  patterns?: string[];

  // Blocker information
  blocker?: string;
  blockerType?: 'dependency' | 'permission' | 'information' | 'external';
  needsFrom?: string;

  // Completion context
  summary?: string;
  filesModified?: string[];
  filesCreated?: string[];
  outputArtifacts?: string[];

  // Continuation context
  currentState?: string;
  immediateNextStep?: string;
  keyFiles?: string[];
  keyDecisions?: string[];

  // Timestamps
  lastUpdated?: string;
  completedAt?: string;
  pausedAt?: string;
}
```

### Reading Handoff Context

When starting work on a task that another agent worked on:

```javascript
// Get full task details including metadata
const task = TaskGet({ taskId: 'X' });

// Check metadata for context
if (task.metadata?.sessionPaused) {
  // Previous session paused - read currentState and immediateNextStep
}
if (task.metadata?.discoveries) {
  // Previous agent found things - review discoveries array
}
if (task.metadata?.blocker) {
  // Task was blocked - check if blocker is resolved
}
```

## Cross-Session Coordination

### Environment Variable: CLAUDE_CODE_TASK_LIST_ID

Use this environment variable to share task lists across sessions:

```bash
# Set shared task list for all sessions
export CLAUDE_CODE_TASK_LIST_ID="my-project-tasks"

# Start claude code - will use shared task list
claude
```

**When to use:**

- Multiple terminals working on same project
- Background agents that should share task state
- Team collaboration on task lists

### Shared Task List Pattern

```javascript
// Session A creates task
TaskCreate({
  subject: 'Implement feature X',
  description: '...',
  metadata: {
    owner: 'session-a',
    priority: 'high',
  },
});

// Session B (same CLAUDE_CODE_TASK_LIST_ID) picks up task
TaskList(); // Sees task from Session A
TaskUpdate({
  taskId: '1',
  status: 'in_progress',
  metadata: {
    owner: 'session-b', // Claims ownership
    previousOwner: 'session-a',
  },
});
```

## Iron Laws (MUST FOLLOW)

### 1. Never Complete Without Summary

```javascript
// WRONG - No context for future reference
TaskUpdate({ taskId: 'X', status: 'completed' });

// CORRECT - Full context preserved
TaskUpdate({
  taskId: 'X',
  status: 'completed',
  metadata: {
    summary: 'Added auth middleware with JWT validation',
    filesModified: ['src/middleware/auth.ts'],
    completedAt: new Date().toISOString(),
  },
});
```

### 2. Always Update on Discovery

```javascript
// WRONG - Discoveries lost
// ... agent finds important pattern but doesn't record it ...

// CORRECT - Discoveries preserved
TaskUpdate({
  taskId: 'X',
  metadata: {
    discoveries: [...existingDiscoveries, 'Found circular dependency in module X'],
  },
});
```

### 3. Always TaskList After Completion

```javascript
// WRONG - May have unblocked other tasks
TaskUpdate({ taskId: "X", status: "completed" });
// ... session ends ...

// CORRECT - Check for follow-up work
TaskUpdate({ taskId: "X", status: "completed", metadata: {...} });
TaskList();  // Find newly unblocked tasks
```

### 4. Use Metadata for Structure, Description for Prose

```javascript
// WRONG - Structured data in prose
TaskUpdate({
  taskId: 'X',
  description: 'Files: a.ts, b.ts. Blocked by: auth issue. Progress: 50%',
});

// CORRECT - Structured metadata + prose description
TaskUpdate({
  taskId: 'X',
  description: 'Implementing auth flow. Hit a blocker with token refresh.',
  metadata: {
    filesModified: ['a.ts', 'b.ts'],
    blocker: 'auth issue',
    progress: '50%',
  },
});
```

## Integration with Memory Protocol

Task metadata complements but does not replace Memory Protocol:

| Information Type          | Task Metadata  | Memory Files       |
| ------------------------- | -------------- | ------------------ |
| Task-specific discoveries | Yes            | No                 |
| Project-wide patterns     | Reference only | Yes (learnings.md) |
| Architecture decisions    | Reference only | Yes (decisions.md) |
| Blocking issues           | Yes            | Yes (issues.md)    |
| Progress state            | Yes            | No                 |
| Completion summary        | Yes            | Yes (learnings.md) |

**Pattern:**

1. Record task-specific context in task metadata
2. Record project-wide learnings in memory files
3. Cross-reference between them

```javascript
// Task completion with memory reference
TaskUpdate({
  taskId: 'X',
  status: 'completed',
  metadata: {
    summary: 'Implemented auth flow',
    memoryUpdates: ['learnings.md: JWT refresh pattern', 'decisions.md: ADR-005 auth architecture'],
  },
});
```

## Examples

### Example 1: Developer Agent Completing Feature

```javascript
// Start
TaskList();
TaskGet({ taskId: '5' });
TaskUpdate({ taskId: '5', status: 'in_progress', activeForm: 'Implementing login flow' });

// Discovery during work
TaskUpdate({
  taskId: '5',
  metadata: {
    discoveries: ['Existing auth module at src/auth/', 'Uses JWT not sessions'],
    keyFiles: ['src/auth/jwt.ts', 'src/middleware/auth.ts'],
  },
});

// Completion
TaskUpdate({
  taskId: '5',
  status: 'completed',
  metadata: {
    summary: 'Added login endpoint with JWT auth',
    filesCreated: ['src/routes/login.ts', 'src/routes/login.test.ts'],
    filesModified: ['src/routes/index.ts'],
    testsAdded: true,
    testsPassing: true,
    completedAt: new Date().toISOString(),
  },
});
TaskList(); // Check for unblocked tasks
```

### Example 2: Background Agent with Handoff

```javascript
// Background agent starting long task
TaskUpdate({
  taskId: '10',
  status: 'in_progress',
  metadata: { runningInBackground: true },
});

// Progress update (multiple during execution)
TaskUpdate({
  taskId: '10',
  metadata: {
    progress: '40%',
    currentState: 'Processed 400/1000 files',
    discoveries: ['Found 12 security issues', '3 critical in auth module'],
  },
});

// Completion - main session can check this
TaskUpdate({
  taskId: '10',
  status: 'completed',
  metadata: {
    summary: 'Security scan complete: 12 issues found (3 critical)',
    outputArtifacts: ['.claude/context/reports/security-scan.md'],
    criticalFindings: 3,
    highFindings: 5,
    mediumFindings: 4,
    completedAt: new Date().toISOString(),
  },
});
```

### Example 3: Multi-Agent Coordination

```javascript
// Planner creates tasks with dependencies
TaskCreate({ subject: 'Design auth system', description: '...', activeForm: 'Designing auth' });
TaskCreate({
  subject: 'Implement auth backend',
  description: '...',
  activeForm: 'Implementing auth',
});
TaskCreate({ subject: 'Add auth tests', description: '...', activeForm: 'Testing auth' });

TaskUpdate({ taskId: '2', addBlockedBy: ['1'] }); // Implementation blocked by design
TaskUpdate({ taskId: '3', addBlockedBy: ['2'] }); // Tests blocked by implementation

// Architect completes design
TaskUpdate({
  taskId: '1',
  status: 'completed',
  metadata: {
    summary: 'Auth design complete - JWT with refresh tokens',
    outputArtifacts: ['.claude/context/plans/auth-design.md'],
    keyDecisions: ['JWT over sessions', 'Redis for token store'],
  },
});

// Developer can now start (task 2 unblocked)
TaskList(); // Shows task 2 now available
TaskGet({ taskId: '2' }); // Gets design context from task 1's metadata
```

## Related Skills

- `session-handoff` - Creates full session handoff documents (use for complex handoffs)
- `operational-modes` - Self-regulates tool usage during task execution
- `thinking-tools` - Checkpoints for verifying task completion quality

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New task pattern discovered -> `.claude/context/memory/learnings.md`
- Issue with task tools -> `.claude/context/memory/issues.md`
- Decision about task structure -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in task metadata, it didn't happen.
