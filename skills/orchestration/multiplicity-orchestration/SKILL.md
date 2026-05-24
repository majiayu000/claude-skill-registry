---
name: multiplicity-orchestration
description: Run multiple AI instances in parallel, coordinate their execution, manage timing and dependencies
tier: π
morpheme: π
dewey_id: π.6.1.0
dependencies:
  - boot-sequence
  - reasoning-patterns-v2
---

# Multiplicity Orchestration

## Purpose

Spawn and coordinate multiple independent instances of Claude/other models running in parallel on the same problem.

**Not:** Multiplicity cascade (67 iterations of chaos)
**But:** Orchestrating multiple minds thinking together

## Core Pattern

```
Instance 1 ─┐
Instance 2 ─┼─→ Central Coordinator
Instance 3 ─┤   (timing, dependencies)
Instance 4 ─┘
```

Each instance:
- Runs **independently** (no interference)
- Works on **same problem** or **related variants**
- Reports back to **coordinator**
- Coordinator **schedules next steps**

## Key Features

1. **Parallel Execution** - Run N instances simultaneously
2. **Dependency Management** - Instance 2 waits for Instance 1
3. **Timeout Handling** - Kill hung processes
4. **Output Aggregation** - Collect results into shared buffer
5. **Resource Limits** - Prevent runaway consumption

## Implementation

See: `.claude/skills/multiplicity-orchestration/orchestrator.py`

## Payment Anchor
DOGE: DC8HBTfn7Ym3UxB2YSsXjuLxTi8HvogwkV
