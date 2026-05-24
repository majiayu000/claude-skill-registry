---
name: complex-orchestrator
description: Orchestrates multi-file tasks by delegating to parallel sub-agents. Use when a task spans multiple files or components and can benefit from parallel execution to save context and time.
---

# Parallel Task Orchestrator

Distribute multi-file work across parallel sub-agents to save context and time.

## When to Use

```
Task spans multiple files?
    │
    ├─ Independent? ──────► Full Parallel
    ├─ Some dependencies? ─► Staged Parallel (waves)
    └─ Tightly coupled? ──► Sequential or single agent
```

## 4-Step Workflow

### 1. Decompose
Break into file-scoped units. Identify dependencies.

### 2. Choose Strategy
- **Full Parallel**: All units independent
- **Staged Parallel**: Wave 1 (dependencies) → Wave 2 (consumers)
- **Fan-out/Fan-in**: Setup → parallel work → integration

### 3. Delegate in Parallel
Launch multiple Tasks in **single message**:
```typescript
Task({ subagent_type: "general-purpose", description: "Edit file A", prompt: "..." })
Task({ subagent_type: "general-purpose", description: "Edit file B", prompt: "..." })
```

### 4. Integrate
- Verify each succeeded
- Check for conflicts
- Run integration tests

## Sub-agent Prompt Structure

```markdown
## Scope
File: [path] | Task: [what to do in THIS file only]

## Context
Pattern: [consistent approach across all units]

## Constraints
- Only modify [path]
- Follow existing style
```

## Agent Selection

| Sub-task | Agent |
|----------|-------|
| Simple edit | `general-purpose` |
| Exploration needed | `Explore` → `general-purpose` |
| Complex logic | `advanced-general-purpose` |

---

*For detailed examples and troubleshooting, see `examples.md`*
