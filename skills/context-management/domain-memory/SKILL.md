# Domain Memory Skill

> Standardized boot-up ritual and memory access patterns for stateless agent workflows.

## Overview

The Domain Memory pattern enables agents to work effectively across sessions without shared context. All state lives on DISK in `domain-memory.yaml`. Agents read from disk, work, write to disk, and exit.

## Core Principle

**Disk is the only source of truth.**

- Agents are STATELESS - no memory of previous runs
- State is PERSISTENT - survives agent restarts
- Progress is OBSERVABLE - logged to disk
- Work is ATOMIC - one feature at a time

## Boot-Up Ritual

**Every agent session MUST follow this sequence:**

```
┌─────────────────────────────────────────┐
│ 1. READ domain-memory.yaml              │
│    - Load current state from disk       │
│    - Understand goals, features, status │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 2. VERIFY test baseline                 │
│    - Run existing tests                 │
│    - Ensure no regressions              │
│    - STOP if baseline fails             │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 3. SELECT one work item                 │
│    - Pick failing features first        │
│    - Then untested by priority          │
│    - Check dependencies are met         │
│    - Lock the selected feature          │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 4. EXECUTE with logging                 │
│    - Implement the feature              │
│    - Run feature-specific tests         │
│    - Log approach taken                 │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 5. UPDATE domain-memory.yaml            │
│    - Mark feature status                │
│    - Record what was tried              │
│    - Add log entry                      │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 6. EXIT cleanly                         │
│    - Unlock the feature                 │
│    - Commit changes                     │
│    - Return structured result           │
│    - DO NOT continue to next feature    │
└─────────────────────────────────────────┘
```

## Domain Memory CLI

All operations go through `.spec-flow/scripts/bash/domain-memory.sh`:

### Initialization
```bash
# Create new domain memory
domain-memory.sh init specs/001-auth

# Generate from existing tasks.md
domain-memory.sh generate-from-tasks specs/001-auth
```

### Reading State
```bash
# Get full status
domain-memory.sh status specs/001-auth

# Get next feature to work on (JSON)
domain-memory.sh pick specs/001-auth

# Validate structure
domain-memory.sh validate specs/001-auth
```

### Updating State
```bash
# Update feature status
domain-memory.sh update specs/001-auth F001 passing

# Lock feature for work
domain-memory.sh lock specs/001-auth F001

# Unlock feature
domain-memory.sh unlock specs/001-auth
```

### Logging
```bash
# Add log entry
domain-memory.sh log specs/001-auth "worker" "completed_feature" "Implemented login" F001

# Record tried approach
domain-memory.sh tried specs/001-auth F001 "Used async pattern" "Failed: race condition"
```

## Feature Status Values

| Status | Meaning | Worker Action |
|--------|---------|---------------|
| `untested` | No tests run yet | Implement and test |
| `passing` | Tests pass | Skip (done) |
| `failing` | Tests fail | Fix (priority) |
| `in_progress` | Currently locked | Skip (wait) |
| `blocked` | Cannot proceed | Skip (manual help needed) |

## Priority Rules

Workers select features by:
1. **Failing features first** - Fix regressions before new work
2. **Priority order** - Lower number = higher priority
3. **Dependencies met** - All dependencies must be passing

## The "Tried" Mechanism

Prevent infinite loops by tracking what approaches have failed:

```yaml
tried:
  F001:
    - approach: "Used async/await"
      result: "Failed: race condition"
      timestamp: "2025-01-15T10:00:00Z"
    - approach: "Used callbacks"
      result: "Failed: callback hell"
      timestamp: "2025-01-15T11:00:00Z"
```

Before implementing, check if your approach has already failed. Try something fundamentally different.

## Orchestrator Responsibilities

The orchestrator (main Claude Code session) is LIGHTWEIGHT:

```
WHILE features remain (failing or untested):
    1. Read domain-memory.yaml
    2. Spawn Task(Worker) with feature_dir
    3. Wait for Worker to complete
    4. Check domain-memory.yaml status
    5. If all passing: DONE
    6. If failures remain: Spawn next Worker
```

The orchestrator:
- Does NOT implement code
- Does NOT carry implementation context
- ONLY spawns Workers and checks disk state

## Epic Workflow

For epics, domain memory is hierarchical:

```
epics/001-ecom/
├── domain-memory.yaml          # Epic-level overview
└── sprints/
    ├── S01/
    │   └── domain-memory.yaml  # Sprint 1 features
    ├── S02/
    │   └── domain-memory.yaml  # Sprint 2 features
    └── S03/
        └── domain-memory.yaml  # Sprint 3 features
```

Parallel sprints get parallel Workers (spawned in single message):
```
Task(Worker for S01) + Task(Worker for S02)  # Same message = parallel
```

## Anti-Patterns to Avoid

### ❌ Working on Multiple Features
```
# WRONG: Worker picks F001, then continues to F002
implement(F001)
implement(F002)  # Should have EXITED after F001!
```

### ❌ In-Memory State
```
# WRONG: Tracking progress in variable
completed_features = []
completed_features.append("F001")  # Lost on restart!
```

### ❌ Repeating Failed Approaches
```
# WRONG: Trying same thing that failed before
# Should check "tried" section first
```

### ❌ Skipping Boot-Up Ritual
```
# WRONG: Starting implementation without reading disk
implement()  # What features exist? What's their status? Unknown!
```

## Integration Points

### With /feature Command
```
/feature "description"
    ↓
Task(Initializer) → Creates domain-memory.yaml
    ↓
/spec, /plan, /tasks → Normal phases
    ↓
/implement → Worker loop until all passing
```

### With /epic Command
```
/epic "description"
    ↓
Task(Initializer) → Creates sprint-level domain-memory.yaml files
    ↓
/implement-epic → Parallel Workers per sprint
```

### With /feature continue
```
/feature continue
    ↓
If domain-memory.yaml exists:
    Check for remaining features
    Spawn Worker if needed
Else:
    Generate from tasks.md
    Then spawn Worker
```

## Debugging

When things go wrong:

1. **Check domain-memory.yaml directly**
   - Is the feature status correct?
   - Are dependencies properly marked?
   - What does the log show?

2. **Check the "tried" section**
   - What approaches have been attempted?
   - Why did they fail?

3. **Validate the file**
   ```bash
   domain-memory.sh validate specs/001-auth
   ```

4. **Reset a stuck feature**
   ```bash
   domain-memory.sh update specs/001-auth F001 untested
   domain-memory.sh unlock specs/001-auth
   ```
