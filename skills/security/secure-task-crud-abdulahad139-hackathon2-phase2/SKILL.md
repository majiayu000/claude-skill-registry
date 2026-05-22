---
name: secure-task-crud
description: This skill should be used when implementing secure, high-performance REST API endpoints for task management with strictly enforced multi-tenant isolation and async performance.
---

# Secure Task CRUD Routes

This skill providing guidance on implementing secure REST API endpoints for task management.

## Purpose
Implementing secure, high-performance REST API endpoints for task management with strictly enforced multi-tenant isolation and async performance.

## Capabilities
- **Strict Isolation**: Implicit filtering of all queries by `current_user.id`.
- **Ownership Validation**: Explicit checks to ensure users can only modify/delete their own tasks.
- **RESTful Design**: Standardized routes for list, create, get, update, delete, and status toggling.
- **Payload Validation**: Integration with Pydantic/SQLModel for request/response serialization.
- **Async Execution**: Full utilization of async database sessions for non-blocking I/O.

## Implementation Details

### Route Structure
Prefixing all routes with `/api/{user_id}/tasks` to anchor resource ownership in the URL.

### Endpoint Implementation
```python
router = APIRouter(prefix="/api/{user_id}/tasks")

@router.get("/", response_model=List[TaskRead])
async def list_tasks(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Task).where(Task.user_id == current_user.id)
    results = await session.execute(statement)
    return results.scalars().all()

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    db_task = await session.get(Task, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    # ... update logic ...
```

## Best Practices
- Never trusting the `user_id` from the path without comparing it to the `current_user.id` from the token.
- Returning `404` for unauthorized access to specific IDs to prevent leakage of Task existence.
- Using specialized schemas (`TaskCreate`, `TaskRead`, `TaskUpdate`) to separate API models from DB models.
