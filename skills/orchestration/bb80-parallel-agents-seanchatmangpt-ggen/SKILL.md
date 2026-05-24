---
name: bb80-parallel-agents
description: "10-agent parallel orchestration for EPIC 9 atomic cycle (fan-out → construction → collision → convergence)."
allowed_tools: "Task"
---

# EPIC 9: Parallel Agents

## Core Concept

EPIC 9 = 2.8-4.4x speedup via 10 parallel agents:

```
1. FAN-OUT → 2. CONSTRUCTION → 3. COLLISION DETECTION
→ 4. CONVERGENCE → 5. REFACTORING → 6. CLOSURE
```

## When to Use

**Use EPIC 9** (default for non-trivial): Implementation, architecture, debugging, optimization

**Skip EPIC 9** (trivial): Read single file, run single command, display help

## Mandatory Phases

All phases must complete in order (no skipping, no reordering):
1. Fan-Out (10+ agents, independent)
2. Independent Construction (no coordination)
3. Collision Detection (overlap analysis)
4. Convergence (selection pressure)
5. Refactoring (merge/discard/rewrite)
6. Closure (deterministic receipts)

## Reference
See CLAUDE.md sections:
- Three Paradigms (EPIC 9)
- When to Use EPIC 9
- Agents: bb80-parallel-task-coordinator, bb80-collision-detector, bb80-convergence-orchestrator
