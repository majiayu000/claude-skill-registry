---
name: parallel-dispatch
description: Coordinate simultaneous agent execution for independent tasks. Use when multiple tasks can run in parallel without dependencies.
---

# Parallel Dispatch

Coordinate multiple agents working simultaneously on independent tasks.

## Purpose

Maximize efficiency by:
1. Identifying parallelizable work
2. Dispatching multiple agents in a single message
3. Tracking parallel execution
4. Synthesizing results

## When to Use

- Multiple independent bug fixes
- Research across different features
- Frontend AND backend work (when API contract is clear)
- Multiple file/component updates
- Batch operations

## When NOT to Use

- Tasks have data dependencies
- One task's output is another's input
- Sequential workflow required
- Shared state being modified

## Parallelization Analysis

### Step 1: Identify Tasks

List all discrete tasks to be done:

```markdown
## Tasks Identified

1. [Task A]: [description]
2. [Task B]: [description]
3. [Task C]: [description]
```

### Step 2: Dependency Check

For each pair of tasks, check:

| Task A | Task B | Dependency? | Reason |
|--------|--------|-------------|--------|
| T1 | T2 | No | Different features |
| T1 | T3 | Yes | T3 needs T1's output |
| T2 | T3 | No | Independent |

### Step 3: Group into Waves

```markdown
## Execution Waves

### Wave 1 (Parallel)
- Task A → @frontend-agent
- Task B → @research-agent

### Wave 2 (After Wave 1)
- Task C → @backend-agent (needs T1 output)
```

### Step 4: Dispatch

**CRITICAL**: Send all parallel tasks in a **single message** with multiple Task tool calls.

```markdown
## Parallel Dispatch

Spawning agents in parallel for Wave 1:

@frontend-agent: [Task A instructions]
@research-agent: [Task B instructions]
```

### Step 5: Synthesize

When all agents return:

```markdown
## Results Synthesis

### From Frontend Agent
- Completed: [summary]
- Files changed: [list]
- Issues found: [if any]

### From Research Agent
- Findings: [summary]
- Recommendations: [list]

### Combined Status
- [ ] All tasks complete
- [ ] No conflicts between changes
- [ ] Ready for next wave / done
```

## Parallel Patterns

### Pattern 1: Multi-Feature Bug Fixes

```
Wave 1 (Parallel):
├── @frontend-agent: Fix button alignment in Dashboard
├── @frontend-agent: Fix modal close behavior in Settings
└── @backend-agent: Fix validation error in enrollment action
```

### Pattern 2: Research + Implementation

```
Wave 1 (Parallel):
├── @research-agent: Find all usages of deprecated API
└── @doc-agent: Load feature docs for migration

Wave 2 (After research):
└── @backend-agent: Update all usages per research findings
```

### Pattern 3: Frontend + Backend (Clear Contract)

```
Wave 1 (Parallel, when API contract defined):
├── @frontend-agent: Build UI for new feature (mock data)
└── @backend-agent: Implement server actions per spec

Wave 2 (Integration):
└── @frontend-agent: Connect UI to real API
```

## Cost Awareness

| Configuration | Relative Cost |
|---------------|---------------|
| Sequential agents | N × 4x = 4Nx |
| Parallel agents | N × 4x = 4Nx (same cost, faster) |
| **But**: Context duplication overhead | ~15x for many agents |

**Best practice**: Parallelize 2-4 agents max. Beyond that, overhead exceeds benefit.

## Output Format

```markdown
## Parallel Dispatch Report

### Wave 1 Dispatch
| Agent | Task | Status |
|-------|------|--------|
| @frontend-agent | [task] | Dispatched |
| @backend-agent | [task] | Dispatched |

### Wave 1 Results
| Agent | Outcome | Files Changed |
|-------|---------|---------------|
| @frontend-agent | Success | [files] |
| @backend-agent | Success | [files] |

### Synthesis
- Conflicts: [None / List]
- Follow-up needed: [None / List]
- Ready for: [Next wave / Testing / Done]
```

## Integration with Task Router

Use `/task-router` first to analyze task dependencies, then `/parallel-dispatch` to execute.

```
1. /task-router → Identifies tasks and dependencies
2. /parallel-dispatch → Groups into waves and executes
```
