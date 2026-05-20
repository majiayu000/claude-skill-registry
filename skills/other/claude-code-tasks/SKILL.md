---
name: claude-code-tasks
description: Reference for Claude Code's 6 Task Management tools — TaskCreate, TaskGet, TaskList, TaskUpdate (structured tracking) and TaskOutput, TaskStop (background execution). Covers tool parameters, status lifecycle, completion rules, dependency management, and conventions
user-invocable: false
disable-model-invocation: false
last-verified: 2026-03-07
---

# Claude Code Tasks Reference

This skill is a shared reference for Claude Code's 6 Task Management tools. Load it when your skill or agent needs to create, manage, or coordinate tasks.

The tools serve two distinct purposes:

- **Structured tracking** — TaskCreate, TaskGet, TaskList, TaskUpdate — for organizing work items, tracking progress, managing dependencies, and coordinating agents
- **Background execution** — TaskOutput, TaskStop — for monitoring and controlling background processes (shells, agents, remote sessions)

Both share the task ID namespace but serve different operational needs.

This reference covers:
- Complete tool parameter tables for all six Task tools
- Status lifecycle, transition rules, and completion rules
- Naming conventions (subject vs. activeForm)
- Dependency management with DAG design principles
- Metadata conventions for categorization and tracking

For deeper content, load the reference files listed at the end of this document.

---

## TaskCreate

Creates a new task. Returns the created task object with a system-assigned `id`.

Use TaskCreate for complex multi-step tasks (3+ distinct steps), plan mode tracking, or when the user provides multiple tasks or requests a todo list. Skip it for single straightforward tasks or trivial work completable in under 3 steps.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subject` | string | Yes | Short imperative title for the task (e.g., "Create user schema"). Displayed in the task list UI. |
| `description` | string | Yes | Detailed description including context and acceptance criteria. Supports markdown. |
| `activeForm` | string | No | Present-continuous description shown while the task is in progress (e.g., "Creating user schema"). Displayed in the task list UI during execution. Falls back to `subject` if omitted. |
| `metadata` | object | No | Key-value pairs for categorization and tracking. Keys and values are strings. Common keys documented in the Metadata Conventions section below. |

### Behavior

- All tasks are created with status `pending`
- No owner is assigned at creation — use TaskUpdate to assign
- Use TaskUpdate after creation to set up dependencies (`blocks`/`blockedBy`)

### Return Value

Returns the full task object including:
- `id` — System-assigned unique identifier
- `subject` — The subject provided
- `description` — The description provided
- `activeForm` — The activeForm provided (if any)
- `status` — Always `pending` for newly created tasks
- `metadata` — The metadata provided (if any)
- `blockedBy` — Empty array (no dependencies yet)
- `blocks` — Empty array (no dependents yet)

### Example

```
TaskCreate:
  subject: "Create user authentication module"
  description: "Implement JWT-based auth with login, logout, and token refresh endpoints."
  activeForm: "Creating user authentication module"
  metadata:
    priority: "high"
    complexity: "medium"
    task_group: "user-auth"
```

---

## TaskGet

Retrieves a single task by its ID. Use this to get full task details including description, metadata, and dependency information.

Use TaskGet before starting work on a task to get the full description with acceptance criteria. Also use it to verify the `blockedBy` list is empty before beginning work, and to read the latest state before calling TaskUpdate (staleness check). Use TaskList first for an overview, then TaskGet for full details on a specific task.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | The ID of the task to retrieve. |

### Return Value

Returns the full task object:
- `id` — Task identifier
- `subject` — Task title
- `description` — Full description (may be long)
- `activeForm` — Present-continuous form (if set)
- `status` — Current status (`pending`, `in_progress`, `completed`, `deleted`)
- `metadata` — Key-value pairs
- `blockedBy` — Array of task IDs this task depends on
- `blocks` — Array of task IDs that depend on this task
- `owner` — The agent or session that owns this task (if set)

---

## TaskUpdate

Updates an existing task. Only the fields you provide are changed; omitted fields remain unchanged.

Always read the latest state via TaskGet before updating to avoid acting on stale data.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskId` | string | Yes | The ID of the task to update. |
| `status` | string | No | New status. Valid values: `pending`, `in_progress`, `completed`, `deleted`. See Status Lifecycle below. |
| `subject` | string | No | Updated subject line. |
| `description` | string | No | Updated description. |
| `activeForm` | string | No | Updated present-continuous description. |
| `owner` | string | No | Set or change the task owner (agent name or session identifier). |
| `metadata` | object | No | Metadata keys to merge with existing metadata. Set a key to `null` to delete it. |
| `addBlocks` | string[] | No | Add task IDs to this task's `blocks` list (tasks that depend on this one). |
| `addBlockedBy` | string[] | No | Add task IDs to this task's `blockedBy` list (tasks this one depends on). |

### Return Value

Returns the updated task object with all current fields.

### Example

```
TaskUpdate:
  taskId: "5"
  status: "in_progress"
  activeForm: "Implementing user authentication module"
```

---

## TaskList

Lists all tasks in the current task list. Takes no parameters.

Use TaskList to see available work (pending, unblocked tasks), check overall progress, or find the next task after completing one. For teammate workflows: call TaskList, find tasks with `pending` status and empty `blockedBy`, prefer the highest-priority unblocked task, then claim it via TaskUpdate.

### Parameters

None.

### Return Value

Returns an array of task summary objects. Each summary includes:
- `id` — Task identifier
- `subject` — Task title
- `status` — Current status
- `owner` — Agent ID if assigned, empty if available
- `blockedBy` — Array of blocking task IDs
- `blocks` — Array of dependent task IDs
- `metadata` — Key-value pairs

Note: TaskList returns summary objects. Use TaskGet to retrieve the full `description` for a specific task.

---

## TaskOutput

Retrieves output from a running or completed background task. Works with background shells, async agents, and remote sessions.

Use TaskOutput to check on background task progress, retrieve results from completed background work, or monitor long-running operations.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `task_id` | string | Yes | — | The task ID to get output from. |
| `block` | boolean | Yes | `true` | Whether to wait for task completion before returning. |
| `timeout` | number | Yes | `30000` | Maximum wait time in milliseconds. Range: 0–600000 (0–10 minutes). |

### Behavior

- **`block: true`** — Waits for the task to finish (up to `timeout` ms), then returns the output. Use this when you need the result before proceeding.
- **`block: false`** — Returns immediately with current status and any available output. Use this for progress checks without blocking.

---

## TaskStop

Terminates a running background task.

Use TaskStop to cancel a long-running task that is no longer needed or to force-terminate a background process (e.g., a timed-out executor agent).

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_id` | string | No | The ID of the background task to stop. |
| `shell_id` | string | No | **Deprecated** — use `task_id` instead. |

### Return Value

Returns success or failure status of the stop operation.

---

## Status Lifecycle

Tasks follow a three-state lifecycle with an additional terminal state.

```
┌──────────┐    TaskUpdate     ┌─────────────┐    TaskUpdate     ┌───────────┐
│ pending  │ ──────────────→  │ in_progress │ ──────────────→  │ completed │
└──────────┘   status:         └─────────────┘   status:         └───────────┘
  TaskCreate   in_progress                       completed
      │                             │
      │ TaskUpdate                  │ TaskUpdate
      │ status: deleted             │ status: deleted
      ▼                             ▼
┌───────────┐                 ┌───────────┐
│  deleted   │                │  deleted   │
└───────────┘                 └───────────┘
```

### States

| Status | Meaning | Entry Condition |
|--------|---------|-----------------|
| `pending` | Task is created and waiting to be started | Default on creation via TaskCreate |
| `in_progress` | Task is actively being worked on | Explicitly set via TaskUpdate |
| `completed` | Task is finished | Explicitly set via TaskUpdate |
| `deleted` | Task is removed (soft delete) | Explicitly set via TaskUpdate from any state |

### Transition Rules

- **pending -> in_progress**: Set when an agent begins working on the task.
- **in_progress -> completed**: Set when the task is verified as done. Only mark complete after verification passes.
- **in_progress -> pending**: Valid for resetting a task (e.g., after a failed attempt or interrupted session).
- **pending -> deleted**: Remove a task that is no longer needed.
- **in_progress -> deleted**: Cancel a task that is in progress.
- **Blocked tasks**: A task with non-empty `blockedBy` (where blockers are not yet completed) should not be started. The system does not enforce this automatically — your orchestration logic must check dependencies before transitioning to `in_progress`.

### Completion Rules

These rules prevent premature completion, which wastes execution resources on retries:

- Only mark `completed` when the task is **fully** accomplished — all acceptance criteria met
- If errors or blockers are encountered, keep the task as `in_progress` and address them
- Never mark completed if: tests are failing, implementation is partial, errors are unresolved, or dependencies are missing
- Always read the latest state via TaskGet before updating status (staleness check)

---

## Naming Conventions

### Subject (Imperative)

The `subject` field uses **imperative mood** — a command that describes what the task will accomplish:

| Good | Bad |
|------|-----|
| "Create user schema" | "Creating user schema" |
| "Add JWT authentication" | "JWT authentication addition" |
| "Fix login timeout bug" | "Login timeout bug" |
| "Implement rate limiting" | "Rate limiting implementation" |

### activeForm (Present-Continuous)

The `activeForm` field uses **present-continuous tense** — describing what is happening while the task runs:

| Subject | activeForm |
|---------|------------|
| "Create user schema" | "Creating user schema" |
| "Add JWT authentication" | "Adding JWT authentication" |
| "Fix login timeout bug" | "Fixing login timeout bug" |
| "Implement rate limiting" | "Implementing rate limiting" |

The `activeForm` appears in the task list UI while the task status is `in_progress`. If omitted, the UI falls back to the `subject`.

---

## Dependency Management

Tasks support dependency tracking via `blockedBy` and `blocks` fields, forming a **Directed Acyclic Graph (DAG)**.

### Fields

- **`blockedBy`**: Array of task IDs that must complete before this task can start. Set via `addBlockedBy` in TaskUpdate.
- **`blocks`**: Array of task IDs that are waiting on this task. Set via `addBlocks` in TaskUpdate. This is the inverse of `blockedBy`.

### Setting Dependencies

Dependencies are set after task creation using TaskUpdate:

```
TaskUpdate:
  taskId: "5"
  addBlockedBy: ["3", "4"]
```

This means task 5 cannot start until tasks 3 and 4 are both completed.

### DAG Design Principles

1. **No cycles**: Never create circular dependencies (A blocks B, B blocks C, C blocks A). This creates deadlocks where no task can proceed.
2. **Minimize depth**: Prefer wider, shallower dependency graphs. Deep chains (A -> B -> C -> D -> E) serialize execution and slow throughput.
3. **Depend on producers, not peers**: A task should depend on the task that produces what it needs, not on unrelated tasks at the same level.
4. **One-way information flow**: Dependencies should follow the data flow — upstream tasks produce artifacts that downstream tasks consume.
5. **Independent tasks run in parallel**: Tasks at the same dependency level (no dependencies between them) can execute concurrently.

### Common Dependency Patterns

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| Linear chain | A -> B -> C | Sequential steps where each builds on the previous |
| Fan-out | A -> [B, C, D] | One task produces input for multiple parallel tasks |
| Fan-in | [A, B, C] -> D | Multiple tasks must complete before a summary/merge task |
| Diamond | A -> [B, C] -> D | Fan-out followed by fan-in; B and C are independent but D needs both |

---

## Metadata Conventions

The `metadata` field accepts arbitrary string key-value pairs. These common keys are used across the agent-alchemy ecosystem:

| Key | Values | Purpose |
|-----|--------|---------|
| `priority` | `critical`, `high`, `medium`, `low`, `unprioritized` | Execution ordering within a wave; higher priority tasks run first |
| `complexity` | `trivial`, `low`, `medium`, `high` | Estimate of implementation effort; used for planning |
| `task_group` | Any string (e.g., `user-auth`, `payments`) | Groups related tasks for filtered execution via `--task-group` |
| `spec_path` | File path (e.g., `internal/specs/auth-SPEC.md`) | Links the task back to its source specification |
| `feature_name` | Any string (e.g., `user-authentication`) | Associates the task with a feature for tracking |
| `task_uid` | Composite key (e.g., `auth:create-schema`) | Enables idempotent merge mode — matching UIDs update existing tasks instead of creating duplicates |
| `spec_phase` | Phase identifier (e.g., `phase-1`) | Tracks which spec phase generated this task |
| `source_section` | Section reference (e.g., `Section 5.1`) | Links to the specific spec section that defined this task |

### Metadata Merge Behavior

TaskUpdate's `metadata` field performs a **merge** with the existing metadata. Keys you provide are added or updated; keys you omit remain unchanged. Set a key to `null` to delete it.

```
# Task 5 currently has metadata: { priority: "high", task_group: "auth" }

# Add complexity without affecting existing keys:
TaskUpdate:
  taskId: "5"
  metadata:
    complexity: "medium"
# Result: { priority: "high", task_group: "auth", complexity: "medium" }

# Delete a key by setting it to null:
TaskUpdate:
  taskId: "5"
  metadata:
    task_group: null
# Result: { priority: "high", complexity: "medium" }
```

---

## Reference Files

For deeper content on task design patterns and common mistakes, load these reference files. These cover patterns for the structured tracking tools (TaskCreate, TaskGet, TaskList, TaskUpdate).

### Task Patterns

Covers dependency graph design patterns (linear, fan-out, fan-in, diamond), task right-sizing guidance, multi-agent coordination via tasks, and metadata strategies.

```
Read ${CLAUDE_PLUGIN_ROOT}/skills/claude-code-tasks/references/task-patterns.md
```

### Anti-Patterns

Documents common mistakes when using Tasks: circular dependencies, over-granular tasks, missing activeForm, batch status update pitfalls, duplicate task creation, and more. Each anti-pattern includes the problem, why it matters, and the correct alternative.

```
Read ${CLAUDE_PLUGIN_ROOT}/skills/claude-code-tasks/references/anti-patterns.md
```
