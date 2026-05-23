---
name: faion-task-parallelizer
description: "Analyzes task dependencies and creates parallel execution waves. Optimizes implementation-plan.md for 3.5x speedup. Use after tasks are created."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep
---

# Task Parallelizer Skill

**Communication with user: User's language. Documents: English.**

## Purpose

Analyze task dependencies and group into parallel execution waves. Achieve 3.5x speedup through optimized execution order.

## Workflow

```
1. Read all TASK_*.md files
     ↓
2. Extract dependencies from each task
     ↓
3. Build dependency graph
     ↓
4. Group into waves (independent tasks together)
     ↓
5. Add checkpoints between waves
     ↓
6. Generate execution plan
```

---

## Dependency Detection

### Explicit Dependencies
From task files:
```markdown
## Dependencies
- TASK_001 must complete first
- Requires auth module from TASK_002
```

### Implicit Dependencies
Detect from:
- File modifications (same file = sequential)
- Module imports (importing from task output)
- Database schema (migrations order)
- API contracts (consumer after producer)

---

## Wave Pattern

```
Wave 1: [Independent tasks - run in parallel]
    ↓
Checkpoint 1: Verify all Wave 1 complete, merge results
    ↓
Wave 2: [Tasks depending on Wave 1 - run in parallel]
    ↓
Checkpoint 2: Verify, merge
    ↓
Wave N: [Final tasks]
    ↓
Final Checkpoint: Integration verification
```

---

## Output Format

```markdown
## Parallel Execution Plan

### Summary
- Total tasks: {N}
- Waves: {M}
- Estimated speedup: {X}x
- Critical path: TASK_A → TASK_D → TASK_G

### Wave 1 (Parallel)
| Task | Description | Est. Tokens |
|------|-------------|-------------|
| TASK_001 | Setup models | 3000 |
| TASK_002 | Setup serializers | 2500 |
| TASK_003 | Setup permissions | 2000 |

**Checkpoint 1:** Verify models, serializers, permissions created

### Wave 2 (Parallel)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_004 | TASK_001 | Create views |
| TASK_005 | TASK_001, TASK_002 | Create API endpoints |

**Checkpoint 2:** Verify API endpoints functional

### Wave 3 (Sequential - Critical Path)
| Task | Depends On | Description |
|------|------------|-------------|
| TASK_006 | TASK_004, TASK_005 | Integration tests |

**Final Checkpoint:** All tests pass

### Dependency Graph
```
TASK_001 ──┬──→ TASK_004 ──┐
           │               │
TASK_002 ──┼──→ TASK_005 ──┼──→ TASK_006
           │               │
TASK_003 ──┴───────────────┘
```

### Execution Commands
```bash
# Wave 1 (parallel)
/faion-execute-task {project}/{feature} TASK_001 &
/faion-execute-task {project}/{feature} TASK_002 &
/faion-execute-task {project}/{feature} TASK_003 &
wait

# Checkpoint 1
# Verify: models exist, serializers work, permissions set

# Wave 2 (parallel)
/faion-execute-task {project}/{feature} TASK_004 &
/faion-execute-task {project}/{feature} TASK_005 &
wait

# Wave 3 (sequential)
/faion-execute-task {project}/{feature} TASK_006
```
```

---

## Speedup Calculation

```
Sequential time = Sum of all task times
Parallel time = Sum of longest task per wave + checkpoints

Speedup = Sequential / Parallel
```

Example:
- 6 tasks, 30 min each = 180 min sequential
- 3 waves (2+2+1 tasks) + 2 checkpoints (5 min each)
- Parallel = 30 + 5 + 30 + 5 + 30 = 100 min
- Speedup = 180/100 = 1.8x

With more parallelizable tasks: up to 3.5x

---

## Checkpoint Types

| Type | When | Action |
|------|------|--------|
| Merge | After parallel wave | Combine outputs, resolve conflicts |
| Verify | Critical dependency | Run tests, check contracts |
| Review | Complex integration | Human review before continuing |
| Sync | State-dependent | Ensure consistent state |

---

## Integration

- After `faion-make-tasks` → Auto-analyze parallelization
- In implementation-plan.md → Add wave structure
- With `/faion-do-all-tasks` → Execute in wave order
