---
name: delegation-triggers
description: Guidelines for when to delegate tasks to sub-agents vs handle directly. Use when deciding whether to use Explore, Plan, or other specialized agents for a task.
---

# Delegation Triggers

## Decision Tree

```
Is this task...
    │
    ├─ Multi-file, independent units? ─► Parallel Orchestration
    │                                     (see complex-orchestrator)
    │
    ├─ Deep analysis / reasoning? ─────► Advanced General Purpose (Opus)
    │   ⚠️ High cost - use sparingly
    │
    ├─ Exploration / Research? ────────► Explore Agent
    │
    ├─ Planning / Design? ─────────────► Plan Agent
    │
    ├─ Simple & Direct? ───────────────► Execute Directly
    │
    └─ Unclear scope? ─────────────────► Decompose First
```

## Quick Reference

| Signal | Agent | Trigger Phrases |
|--------|-------|-----------------|
| **Multi-file** | Parallel (complex-orchestrator) | "all files", "across codebase", "every X" |
| **Deep analysis** | Advanced (Opus) | "thoroughly", "しっかり", "implications" |
| **Find/Understand** | Explore | "where is", "how does", "find all" |
| **Design/Architect** | Plan | "how should I", "design", "best approach" |
| **Simple edit** | Direct | "fix", "add field", "update text" |

## 3-Question Test

1. **Enough context?** → No: Explore first
2. **Multiple approaches?** → Yes: Plan first
3. **Touch 3+ unseen files?** → Yes: Explore/Plan first

## Parallel Execution

Launch in **single message** for parallel:
```
Task({ description: "A", ... })
Task({ description: "B", ... })  // runs parallel with A
```

For dependencies, use **waves**:
```
Wave 1: shared dependency
Wave 2: parallel consumers (after Wave 1)
```

---

*For detailed examples and anti-patterns, see `reference.md`*
