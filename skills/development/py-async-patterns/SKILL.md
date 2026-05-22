---
name: py-async-patterns
description: Async/await patterns for FastAPI and SQLAlchemy. Use when working with async code, database sessions, concurrent operations, or debugging async issues in Python.
---

# Python Async Patterns

## Problem Statement

Async Python is powerful but error-prone. Race conditions, session leaks, and connection pool issues are common pitfalls in async codebases.

---

## Pattern: AsyncSession Lifecycle

**Problem:** Session must be scoped to request. Leaking sessions causes stale data and connection exhaustion.

```python
# ✅ CORRECT: Session scoped to request via dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        # Session automatically closed after request

# Usage in endpoint
@router.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one()

# ❌ WRONG: Global session (stale data, connection leaks)
_global_session = None  # NEVER do this

async def get_user(user_id: UUID):
    result = await _global_session.execute(...)  # Stale, shared state
```

**Why it matters:** Each request needs isolated database state. Shared sessions see stale data and can't be safely committed.

---

## Pattern: Concurrent vs Sequential Queries

**Problem:** Running independent queries sequentially wastes time. But dependent queries must be sequential.

```python
# ✅ CORRECT: Concurrent independent queries
async def get_dashboard_data(user_id: UUID, session: AsyncSession):
    # These don't depend on each other - run in parallel
    user_result, stats_result, recent_result = await asyncio.gather(
        session.execute(select(User).where(User.id == user_id)),
        session.execute(select(UserStats).where(UserStats.user_id == user_id)),
        session.execute(
            select(Activity)
            .where(Activity.user_id == user_id)
            .order_by(Activity.created_at.desc())
            .limit(10)
        ),
    )
    
    return {
        "user": user_result.scalar_one(),
        "stats": stats_result.scalar_one_or_none(),
        "recent": recent_result.scalars().all(),
    }

# ❌ WRONG: Sequential when parallel is safe
async def get_dashboard_data_slow(user_id: UUID, session: AsyncSession):
    user = await session.execute(...)      # Wait...
    stats = await session.execute(...)     # Wait more...
    recent = await session.execute(...)    # Even more waiting
    # Total time = sum of all queries

# ✅ CORRECT: Sequential when queries depend on each other
async def get_user_with_team(user_id: UUID, session: AsyncSession):
    # Must get user first to know team_id
    user_result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = user_result.scalar_one()
    
    # Now we can query team
    team_result = await session.execute(
        select(Team).where(Team.id == user.team_id)
    )
    return user, team_result.scalar_one()
```

**Decision framework:**

| Queries share data? | Use |
|---------------------|-----|
| No (independent) | `asyncio.gather()` |
| Yes (dependent) | Sequential `await` |

---

## Pattern: Transaction Boundaries

**Problem:** Knowing when to commit, rollback, and refresh.

```python
# ✅ CORRECT: Explicit transaction for multi-step operations
async def transfer_player(
    player_id: UUID,
    from_team_id: UUID,
    to_team_id: UUID,
    session: AsyncSession,
):
    try:
        # All operations in one transaction
        player = await session.get(Player, player_id)
        player.team_id = to_team_id
        
        from_team = await session.get(Team, from_team_id)
        from_team.player_count -= 1
        
        to_team = await session.get(Team, to_team_id)
        to_team.player_count += 1
        
        await session.commit()
    except Exception:
        await session.rollback()
        raise

# ✅ CORRECT: Using context manager
async with session.begin():
    # All operations here are in a transaction
    # Auto-commits on success, auto-rollbacks on exception
    player.team_id = to_team_id
    from_team.player_count -= 1
    to_team.player_count += 1

# ✅ CORRECT: Refresh after commit to get DB-generated values
await session.commit()
await session.refresh(new_entity)  # Get id, created_at, etc.
return new_entity
```

**When to use what:**

| Scenario | Pattern |
|----------|---------|
| Single create/update | `session.add()` + `commit()` at request end |
| Multi-step operation | Explicit `begin()` / `commit()` / `rollback()` |
| Need DB-generated values | `refresh()` after commit |
| Read-only query | No commit needed |

---

## Pattern: Connection Pool Management

**Problem:** Exhausting connection pool causes requests to hang.

```python
# This codebase uses NullPool for async - understand why
engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # No connection pooling
)

# NullPool: Each request gets new connection, closes after
# Why: Avoids issues with asyncpg + connection reuse
# Tradeoff: Slightly more connection overhead

# ✅ CORRECT: Always close sessions (handled by Depends)
async with async_session() as session:
    # Work with session
    pass  # Session closed here

# ❌ WRONG: Forgetting to close
session = async_session()
result = await session.execute(query)
# Session never closed - connection leak!
```

---

## Pattern: Background Tasks

**Problem:** Long-running work shouldn't block the response.

```python
from fastapi import BackgroundTasks

# ✅ CORRECT: FastAPI BackgroundTasks for request-scoped work
@router.post("/assessments/{id}/submit")
async def submit_assessment(
    id: UUID,
    session: AsyncSession = Depends(get_session),
    background_tasks: BackgroundTasks,
) -> AssessmentResult:
    # Quick work - return response
    result = await process_submission(id, session)
    
    # Slow work - do after response
    background_tasks.add_task(send_completion_email, result.user_email)
    background_tasks.add_task(update_analytics, result)
    
    return result

# ✅ CORRECT: asyncio.create_task for fire-and-forget
async def process_with_side_effect():
    result = await main_operation()
    
    # Fire and forget - don't await
    asyncio.create_task(log_to_external_service(result))
    
    return result

# ❌ WRONG: Awaiting non-critical slow operations
async def slow_endpoint():
    result = await main_operation()
    await send_email(result)           # User waits for email...
    await update_analytics(result)     # User still waiting...
    return result
```

**When to use what:**

| Scenario | Pattern |
|----------|---------|
| Post-response cleanup | `BackgroundTasks` |
| Fire-and-forget logging | `asyncio.create_task()` |
| Must complete before response | Direct `await` |

---

## Pattern: Avoiding Deadlocks

**Problem:** Concurrent operations acquiring locks in different order.

```python
# ❌ WRONG: Potential deadlock
async def transfer_both_ways():
    # Task 1: Lock A, then B
    # Task 2: Lock B, then A
    # = Deadlock if interleaved
    pass

# ✅ CORRECT: Consistent lock ordering
async def transfer_credits(
    from_id: UUID,
    to_id: UUID,
    amount: int,
    session: AsyncSession,
):
    # Always lock in consistent order (e.g., by UUID)
    first_id, second_id = sorted([from_id, to_id])
    
    # Lock in consistent order
    first = await session.get(Account, first_id, with_for_update=True)
    second = await session.get(Account, second_id, with_for_update=True)
    
    # Now safe to modify
    if from_id == first_id:
        first.balance -= amount
        second.balance += amount
    else:
        second.balance -= amount
        first.balance += amount
    
    await session.commit()
```

---

## Pattern: Post-Condition Validation

Same principle as frontend - verify async operations succeeded:

```python
# ✅ CORRECT: Validate after async operations
async def create_assessment(data: AssessmentCreate, session: AsyncSession):
    assessment = Assessment(**data.model_dump())
    session.add(assessment)
    await session.commit()
    await session.refresh(assessment)
    
    # Validate post-condition
    if assessment.id is None:
        raise RuntimeError("Assessment creation failed - no ID assigned")
    
    return assessment

# ✅ CORRECT: Validate data was actually loaded
async def get_user_or_fail(user_id: UUID, session: AsyncSession) -> User:
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(404, f"User {user_id} not found")
    
    return user
```

---

## Pattern: Logging Async Operations

```python
import structlog

logger = structlog.get_logger()

async def complex_operation(user_id: UUID, session: AsyncSession):
    logger.info("complex_operation.start", user_id=str(user_id))
    
    try:
        result = await step_one(session)
        logger.debug("complex_operation.step_one_complete", result_count=len(result))
        
        await step_two(result, session)
        logger.debug("complex_operation.step_two_complete")
        
        await session.commit()
        logger.info("complex_operation.success", user_id=str(user_id))
        
    except Exception as e:
        logger.error("complex_operation.failed", 
            user_id=str(user_id), 
            error=str(e),
            step="unknown"
        )
        raise
```

---

## Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| "Session is closed" | Using session after request ends | Keep session in request scope |
| Connection timeout | Pool exhausted | Check for session leaks |
| Stale data | Shared session or missing refresh | Scope session to request, refresh after commit |
| Deadlock | Inconsistent lock ordering | Always acquire locks in same order |
| Slow endpoint | Sequential queries that could be parallel | Use `asyncio.gather()` |

---

## Detection Commands

```bash
# Find potential session leaks (global sessions)
grep -rn "async_session()" --include="*.py" | grep -v "async with\|Depends"

# Find sequential queries that might be parallelizable
grep -rn "await session.execute" --include="*.py" -A2 | grep -B1 "await session.execute"

# Find missing awaits
ruff check --select=RUF006  # asyncio dangling task
```
