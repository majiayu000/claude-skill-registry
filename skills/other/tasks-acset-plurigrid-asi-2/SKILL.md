---
name: tasks-acset
description: Google Tasks management via TasksACSet. Transforms task operations into GF(3)-typed Interactions, routes to triadic queues, detects saturation for task-zero-as-condensed-state.
---

# Tasks ACSet Skill

Transform Google Tasks into an ANIMA-condensed system with GF(3) conservation.

**Trit**: -1 (MINUS - validator)  
**Principle**: Task Zero = Condensed Equilibrium State (all tasks completed)  
**Implementation**: TasksACSet + TriadicQueues + SaturationDetector

## Overview

Tasks ACSet applies the ANIMA framework to task management:

1. **Transform** - Task operations → GF(3)-typed Interactions
2. **Route** - Interactions → Triadic queue fibers (MINUS/ERGODIC/PLUS)
3. **Detect** - Saturation → Task Zero condensed state
4. **Verify** - Narya proofs for consistency

## TasksACSet Schema

```
┌────────────────────────────────────────────────────────────────────┐
│                      TasksACSet Schema                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Interaction ─────┬────▶ Task                                     │
│  ├─ verb: String  │      ├─ task_id: String                       │
│  ├─ timebin: Int  │      ├─ status: {needsAction, completed}      │
│  ├─ trit: Trit    │      ├─ due: Timestamp                        │
│  └─ list ─────────┼──▶   └─ saturated: Bool                       │
│                   │                                                │
│  QueueItem ───────┼────▶ Agent3                                   │
│  ├─ interaction ──┘      ├─ fiber: Trit {-1, 0, +1}               │
│  └─ agent ───────────▶   └─ name: String                          │
│                                                                    │
│  TaskList ◀──────────── Subtask ─────────────────▶ Task           │
│  ├─ list_id: String      ├─ parent_task                           │
│  ├─ title: String        ├─ child_task                            │
│  └─ default: Bool        └─ position: Int                         │
│                                                                    │
│  Completion ─────────────▶ Task                                   │
│  ├─ completed_at: Timestamp                                       │
│  └─ gf3_cycle_sum: Int                                            │
└────────────────────────────────────────────────────────────────────┘
```

### Objects

| Object | Description | Trit Role |
|--------|-------------|-----------|
| `Interaction` | Single task action with verb + trit | Data |
| `Task` | GTD item with completion state | Aggregate |
| `TaskList` | Container for tasks | Container |
| `Subtask` | Parent-child relationship edge | Edge |
| `Completion` | Task completion event | Node |
| `Agent3` | Queue fiber (MINUS/ERGODIC/PLUS) | Router |
| `QueueItem` | Links Interaction → Agent3 | Edge |

## GF(3) Verb Typing

Task actions are assigned trits based on information flow:

```python
VERB_TRIT_MAP = {
    # MINUS (-1): Consumption/Validation
    "list_tasks": -1,      "get_task": -1,
    "list_task_lists": -1, "get_task_list": -1,
    
    # ERGODIC (0): Coordination/Metadata
    "update_task": 0,      "move_task": 0,
    "update_task_list": 0, "clear_completed_tasks": 0,
    
    # PLUS (+1): Generation/Execution
    "create_task": +1,     "create_task_list": +1,
    "delete_task": +1,     "delete_task_list": +1,
}
```

### MCP Tool → Trit Mapping

| Tool | Trit | Description |
|------|------|-------------|
| `list_task_lists` | -1 | List all lists (MINUS) |
| `list_tasks` | -1 | List tasks in list (MINUS) |
| `get_task` | -1 | Get task details (MINUS) |
| `get_task_list` | -1 | Get list details (MINUS) |
| `update_task` | 0 | Modify task (ERGODIC) |
| `move_task` | 0 | Reposition task (ERGODIC) |
| `clear_completed_tasks` | 0 | Clean up completed (ERGODIC) |
| `create_task` | +1 | Create new task (PLUS) |
| `create_task_list` | +1 | Create new list (PLUS) |
| `delete_task` | +1 | Delete task (PLUS) |

## Task-Thread Morphism

Tasks connect to Gmail threads and Calendar events:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cross-Skill Morphisms                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Thread ─────[action_item]────▶ Task                            │
│  ├─ gmail thread_id             ├─ notes: "from email: ..."     │
│  └─ needs_action: True          └─ status: needsAction          │
│                                                                  │
│  CalendarEvent ─────[reminder]────▶ Task                        │
│  ├─ event_id                      ├─ due: event.start_time      │
│  └─ summary                       └─ title: event.summary       │
│                                                                  │
│  Task ─────[deadline]────▶ CalendarEvent                        │
│  ├─ due: timestamp               ├─ start: task.due             │
│  └─ title                        └─ summary: "Due: {title}"     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Saturation Detection

Task saturation occurs when all tasks reach equilibrium:

```python
def is_task_zero(task_list_id: str) -> bool:
    """Task list is at Task Zero when:
    1. All tasks are completed or deferred
    2. GF(3) cycle closure: sum(trits) ≡ 0 (mod 3)
    3. No needsAction tasks remain
    """
    tasks = list_tasks(task_list_id, show_completed=True, show_hidden=True)
    active_tasks = [t for t in tasks if t['status'] == 'needsAction']
    
    cycle_sum = sum(t['gf3_trit'] for t in task_list.gf3_cycle[-3:])
    
    return (
        len(active_tasks) == 0 and  # All complete/deferred
        (cycle_sum % 3) == 0        # GF(3) conserved
    )

def detect_global_task_zero() -> Dict:
    """System at Task Zero when:
    1. All task lists saturated
    2. GF(3) conserved globally
    3. GTD weekly review complete
    """
    lists = list_task_lists()
    all_saturated = all(is_task_zero(l['id']) for l in lists)
    
    return {
        "at_task_zero": all_saturated,
        "condensed_fingerprint": sha256(sorted_completion_ids),
        "gtd_equilibrium": True,
    }
```

**Task Zero as ANIMA**: When all tasks reach completion with GF(3) conservation, the task system is in condensed equilibrium.

## Source Files

| File | Description | Trit |
|------|-------------|------|
| [tasks_acset.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/tasks_acset.py) | ACSet schema + GF(3) tracking | -1 |
| [task_saturation.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/task_saturation.py) | Task Zero detection | -1 |
| [task_thread_morphism.py](file:///Users/alice/agent-o-rama/agent-o-rama/src/task_thread_morphism.py) | Cross-skill morphisms | 0 |

## Workflows

### Workflow 1: Task Creation from Email

```python
from tasks_acset import TasksACSet
from gmail_acset import thread_to_task

# MINUS: Read email thread
thread = bridge.get_gmail_thread_content(thread_id)  # trit=-1

# Extract action items
actions = extract_action_items(thread)

# PLUS: Create tasks (balanced by prior MINUS)
for action in actions:
    bridge.create_task(
        task_list_id=default_list,
        title=action.summary,
        notes=f"From thread: {thread_id}",
        due=action.deadline
    )  # trit=+1
```

### Workflow 2: Task Completion with GF(3) Guard

```python
# MINUS first: Get task details
task = bridge.get_task(task_list_id, task_id)  # trit=-1

# ERGODIC: Update status to completed
bridge.update_task(
    task_list_id=task_list_id,
    task_id=task_id,
    status="completed"
)  # trit=0

# Check GF(3) conservation
assert ((-1) + 0) % 3 != 0  # Need PLUS to balance
# PLUS: Log completion
bridge.create_task(
    task_list_id="completions_log",
    title=f"Completed: {task['title']}"
)  # trit=+1, now sum=0 ✓
```

### Workflow 3: Weekly GTD Review with Saturation

```python
# Full GTD review workflow
for task_list in bridge.list_task_lists():  # trit=-1
    tasks = bridge.list_tasks(task_list['id'])  # trit=-1
    
    for task in tasks:
        if task['status'] == 'needsAction':
            # ERGODIC: Decide fate
            if should_defer(task):
                bridge.update_task(task_list['id'], task['id'], 
                                   due=next_week)  # trit=0
            elif should_delete(task):
                bridge.delete_task(task_list['id'], task['id'])  # trit=+1
            elif is_complete(task):
                bridge.update_task(task_list['id'], task['id'],
                                   status="completed")  # trit=0

# Check Task Zero
if detect_global_task_zero()["at_task_zero"]:
    say("GTD review complete. Task Zero achieved.")
```

## Integration

| Skill | Trit | Integration |
|-------|------|-------------|
| [google-workspace](file:///Users/alice/.claude/skills/google-workspace/SKILL.md) | 0 | MCP tool provider |
| [gmail-anima](file:///Users/alice/agent-o-rama/agent-o-rama/.agents/skills/gmail-anima/SKILL.md) | 0 | Thread → Task morphism |
| [calendar-acset](file:///Users/alice/agent-o-rama/agent-o-rama/.agents/skills/calendar-acset/SKILL.md) | +1 | Event ↔ Task morphism |
| [workspace-unified](file:///Users/alice/agent-o-rama/agent-o-rama/.agents/skills/workspace-unified/SKILL.md) | 0 | Cross-skill orchestration |

### GF(3) Triadic Conservation

```
tasks-acset (-1) ⊗ gmail-anima (0) ⊗ calendar-acset (+1) = 0 ✓
list_tasks (-1) ⊗ update_task (0) ⊗ create_task (+1) = 0 ✓
get_task (-1) ⊗ move_task (0) ⊗ delete_task (+1) = 0 ✓
```

---

**Skill Name**: tasks-acset  
**Type**: Task Management / ANIMA Framework  
**Trit**: -1 (MINUS - validator)  
**GF(3)**: Conserved via triadic queue routing  
**ANIMA**: Task Zero = Condensed Equilibrium State
