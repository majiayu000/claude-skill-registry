---
name: task-crud-skill
description: Reusable task CRUD operations skill. Use whenever implementing add, delete, update, view, or complete functionality for todo tasks.
---

# Task CRUD Skill

Use this skill when implementing task Create, Read, Update, Delete operations.

## When to Use

- Adding new tasks
- Deleting existing tasks
- Updating task details
- Viewing task lists
- Toggling task completion

## Task Model

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
```

## CRUD Operations Pattern

### Create
```python
def create_task(state: TaskState, title: str, description: str = "") -> Task:
    # Validate title (1-200 chars)
    if not title or len(title) > 200:
        raise ValueError("Title must be 1-200 characters")
    # Create task with auto-increment ID
    task = Task(id=state.next_id, title=title, description=description)
    state.tasks[task.id] = task
    state.next_id += 1
    return task
```

### Read
```python
def get_task(state: TaskState, task_id: int) -> Task | None:
    return state.tasks.get(task_id)

def list_tasks(state: TaskState, filter: str = "all") -> list[Task]:
    tasks = list(state.tasks.values())
    if filter == "pending":
        return [t for t in tasks if not t.completed]
    elif filter == "completed":
        return [t for t in tasks if t.completed]
    return tasks
```

### Update
```python
def update_task(state: TaskState, task_id: int, title: str = None,
                description: str = None) -> Task | None:
    task = state.tasks.get(task_id)
    if not task:
        return None
    if title:
        task.title = title
    if description is not None:
        task.description = description
    task.updated_at = datetime.now()
    return task
```

### Delete
```python
def delete_task(state: TaskState, task_id: int) -> bool:
    if task_id in state.tasks:
        del state.tasks[task_id]
        return True
    return False
```

### Toggle Complete
```python
def toggle_complete(state: TaskState, task_id: int) -> Task | None:
    task = state.tasks.get(task_id)
    if task:
        task.completed = not task.completed
        task.updated_at = datetime.now()
    return task
```

## Validation Rules

| Field | Rule |
|-------|------|
| title | Required, 1-200 characters |
| description | Optional, max 1000 characters |
| id | Auto-increment, unique |
| completed | Boolean, default False |

## Error Handling

```python
class TaskError(Exception):
    pass

def safe_task_operation(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            raise TaskError("Task not found")
        except ValueError as e:
            raise TaskError(str(e))
    return wrapper
```

## Examples

```python
# Add a task
task = create_task(state, "Buy groceries", "Milk, eggs, bread")

# List all tasks
tasks = list_tasks(state, filter="pending")

# Update a task
updated = update_task(state, 1, title="Buy groceries and fruits")

# Toggle completion
task = toggle_complete(state, 2)

# Delete a task
success = delete_task(state, 3)
```
