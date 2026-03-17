---
name: memory-management
version: 1.0.0
description: "[Utilities] Use when saving or retrieving important patterns, decisions, and learnings across sessions. Also use for external memory checkpoints during long-running tasks to prevent context loss. Triggers on keywords like "remember", "save pattern", "recall", "memory", "persist", "knowledge base", "learnings", "checkpoint", "save context", "preserve progress"."
allowed-tools: Read, Write, Edit, Glob, Grep, TaskCreate, mcp__memory__*
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Persist patterns, decisions, and task progress across sessions using two complementary memory systems.

**Workflow:**

1. **File Checkpoints** — Save task-specific context to `plans/reports/checkpoint-*.md` every 30-60 min
2. **MCP Memory Graph** — Store reusable knowledge (patterns, decisions, bug fixes) as typed entities with relations
3. **Recovery** — On context loss, find latest checkpoint via Glob, read it, resume from documented next steps

**Key Rules:**

- Use file checkpoints for task-specific progress; MCP memory for cross-session knowledge
- Create checkpoints before expected context compaction and at key milestones
- Always include Recovery Instructions in checkpoint files

# Memory Management & Knowledge Persistence

Build and maintain a knowledge graph of patterns, decisions, and learnings across sessions. Also provides external file-based checkpoints for long-running tasks.

## Two Memory Systems

| System               | Storage                  | Use Case                       | Persistence     |
| -------------------- | ------------------------ | ------------------------------ | --------------- |
| **MCP Memory Graph** | In-memory graph database | Patterns, decisions, learnings | Cross-session   |
| **File Checkpoints** | `plans/reports/*.md`     | Task progress, analysis        | Permanent files |

Use MCP Memory for **reusable knowledge**. Use File Checkpoints for **task-specific context**.

---

## Part 1: File-Based External Memory (Checkpoints)

### When to Create File Checkpoints

- Starting complex multi-step tasks (investigation, planning, implementation)
- Every 30-60 minutes during long tasks
- At key milestones
- Before expected context compaction
- After completing significant analysis phases

### Checkpoint File Location

Files saved to: `plans/reports/checkpoint-{timestamp}-{slug}.md`

### CHECKPOINT_CREATE Protocol

Create a checkpoint file with this structure:

```markdown
# Memory Checkpoint: {Task Description}

> Created: {ISO timestamp}
> Task Type: {investigation|planning|bugfix|feature|docs}
> Phase: {current phase number/name}

## Task Context

{What you're working on and why}

## Key Findings

{Critical discoveries and insights - be specific with file paths and line numbers}

## Files Analyzed

| File              | Purpose     | Status   |
| ----------------- | ----------- | -------- |
| path/file.cs:line | description | ✅/🔄/⏳ |

## Progress

- [x] Completed items
- [ ] In-progress items
- [ ] Remaining items

## Important Context

{Information that must be preserved - decisions, assumptions, rationale}

## Next Steps

1. {Immediate next action}
2. {Following action}

## Recovery Instructions

{Exact steps to resume: which file to read, which line to continue from}
```

### CHECKPOINT_RECOVER Protocol

When recovering from a checkpoint:

1. Search for latest checkpoint: `Glob("plans/reports/checkpoint-*.md")`
2. Read the checkpoint file
3. Load any referenced analysis files
4. Review Progress section
5. Continue from documented Next Steps
6. Create new checkpoint after resuming

### Auto-Checkpoint (PreCompact Hook)

The system automatically creates checkpoints before context compaction. These auto-checkpoints are minimal - for better context preservation, create manual checkpoints using `/checkpoint`.

---

## Part 2: MCP Memory Graph (Knowledge Persistence)

---

## Memory Entity Types

| Entity Type       | Purpose                                | Examples                       |
| ----------------- | -------------------------------------- | ------------------------------ |
| `Pattern`         | Recurring code patterns                | CQRS, Validation, Repository   |
| `Decision`        | Architectural/design decisions         | Why we chose X over Y          |
| `BugFix`          | Bug solutions for future reference     | Race condition fixes           |
| `ServiceBoundary` | Service ownership and responsibilities | Growth owns Employees          |
| `SessionSummary`  | End-of-session progress snapshots      | Task progress, next steps      |
| `Dependency`      | Cross-service dependencies             | Growth depends on Accounts     |
| `AntiPattern`     | Patterns to avoid                      | Don't call side effects in cmd |

---

## Memory Operations

### Create New Entity

```javascript
mcp__memory__create_entities([
    {
        name: 'EmployeeValidationPattern',
        entityType: 'Pattern',
        observations: [
            'Use PlatformValidationResult fluent API',
            'Chain with .And() and .AndAsync()',
            "Return validation result, don't throw",
            'Location: Growth.Application/UseCaseCommands/'
        ]
    }
]);
```

### Create Relationships

```javascript
mcp__memory__create_relations([
    {
        from: 'GrowthService',
        to: 'AccountsService',
        relationType: 'depends_on'
    },
    {
        from: 'EmployeeEntity',
        to: 'UserEntity',
        relationType: 'syncs_from'
    }
]);
```

### Add Observations

```javascript
mcp__memory__add_observations([
    {
        entityName: 'EmployeeValidationPattern',
        contents: ['Also supports .AndNot() for negative validation', 'Use .Of<IPlatformCqrsRequest>() for type conversion']
    }
]);
```

### Search Knowledge

```javascript
// Search by query
mcp__memory__search_nodes({ query: 'validation pattern' });

// Open specific entities
mcp__memory__open_nodes({ names: ['EmployeeValidationPattern', 'GrowthService'] });

// Read entire graph
mcp__memory__read_graph();
```

### Delete Outdated Knowledge

```javascript
// Delete entities
mcp__memory__delete_entities({ entityNames: ['OutdatedPattern'] });

// Delete specific observations
mcp__memory__delete_observations([
    {
        entityName: 'EmployeeValidationPattern',
        observations: ['Outdated observation text']
    }
]);

// Delete relations
mcp__memory__delete_relations([
    {
        from: 'OldService',
        to: 'NewService',
        relationType: 'depends_on'
    }
]);
```

---

## When to Save to Memory

### Always Save

1. **Discovered Patterns**: New code patterns not in documentation
2. **Bug Solutions**: Complex bugs with non-obvious solutions
3. **Service Boundaries**: Which service owns what
4. **Architectural Decisions**: Why a particular approach was chosen
5. **Anti-Patterns**: Mistakes to avoid

### Save at Session End

```javascript
// Session summary template
mcp__memory__create_entities([
    {
        name: `Session_${taskName}_${date}`,
        entityType: 'SessionSummary',
        observations: [
            `Task: ${taskDescription}`,
            `Completed: ${completedItems.join(', ')}`,
            `Remaining: ${remainingItems.join(', ')}`,
            `Key Files: ${keyFiles.join(', ')}`,
            `Discoveries: ${discoveries.join(', ')}`,
            `Next Steps: ${nextSteps.join(', ')}`
        ]
    }
]);
```

---

## Memory Retrieval Patterns

### Session Start Protocol

```javascript
// 1. Search for related context
const results = mcp__memory__search_nodes({
    query: 'current feature or task keywords'
});

// 2. Load relevant entities
mcp__memory__open_nodes({
    names: results.entities.map(e => e.name)
});

// 3. Check for incomplete sessions
mcp__memory__search_nodes({ query: 'SessionSummary Remaining' });
```

### Before Implementation

```javascript
// Check for existing patterns
mcp__memory__search_nodes({ query: 'CQRS command pattern' });

// Check for anti-patterns
mcp__memory__search_nodes({ query: 'AntiPattern command' });

// Check for related decisions
mcp__memory__search_nodes({ query: 'Decision validation' });
```

### After Bug Fix

```javascript
// Save the fix
mcp__memory__create_entities([
    {
        name: `BugFix_${bugName}`,
        entityType: 'BugFix',
        observations: [
            `Symptom: ${symptomDescription}`,
            `Root Cause: ${rootCause}`,
            `Solution: ${solution}`,
            `Files: ${affectedFiles.join(', ')}`,
            `Prevention: ${preventionTip}`
        ]
    }
]);
```

---

## Knowledge Graph Structure

```
┌─────────────────────────────────────────────────────────────┐
│                     Project Knowledge                       │
├─────────────────────────────────────────────────────────────┤
│  Services                                                   │
│  ├── ServiceA ──depends_on──> AccountsService               │
│  ├── ServiceB ──depends_on──> AccountsService               │
│  └── ServiceC ──depends_on──> AccountsService               │
│                                                             │
│  Patterns                                                   │
│  ├── CQRSCommandPattern                                     │
│  ├── CQRSQueryPattern                                       │
│  ├── EntityEventPattern                                     │
│  └── ValidationPattern                                      │
│                                                             │
│  Entities                                                   │
│  ├── Employee ──syncs_from──> User                          │
│  ├── Company ──syncs_from──> Organization                   │
│  └── LeaveRequest ──owned_by──> GrowthService               │
│                                                             │
│  Sessions                                                   │
│  ├── Session_LeaveRequest_2025-01-15                        │
│  └── Session_EmployeeImport_2025-01-14                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Importance Scoring

When saving observations, prioritize:

| Score | Criteria                                    |
| ----- | ------------------------------------------- |
| 10    | Critical bug fixes, security issues         |
| 8-9   | Architectural decisions, service boundaries |
| 6-7   | Code patterns, best practices               |
| 4-5   | Session summaries, progress notes           |
| 1-3   | Temporary notes, exploration results        |

---

## Memory Maintenance

### Weekly Cleanup

```javascript
// Find old session summaries (> 30 days)
mcp__memory__search_nodes({ query: 'SessionSummary' });

// Delete outdated sessions
mcp__memory__delete_entities({
    entityNames: ['Session_OldTask_2024-12-01']
});
```

### Consolidation

When multiple observations cover same topic:

```javascript
// 1. Read existing entity
mcp__memory__open_nodes({ names: ['PatternName'] });

// 2. Delete fragmented observations
mcp__memory__delete_observations([
    {
        entityName: 'PatternName',
        observations: ['Fragment 1', 'Fragment 2']
    }
]);

// 3. Add consolidated observation
mcp__memory__add_observations([
    {
        entityName: 'PatternName',
        contents: ['Consolidated comprehensive observation']
    }
]);
```

---

## Quick Reference

**Create**: `mcp__memory__create_entities` / `mcp__memory__create_relations`
**Read**: `mcp__memory__read_graph` / `mcp__memory__open_nodes` / `mcp__memory__search_nodes`
**Update**: `mcp__memory__add_observations`
**Delete**: `mcp__memory__delete_entities` / `mcp__memory__delete_observations` / `mcp__memory__delete_relations`

---

## Part 3: Integration with Workflows

### Long-Running Task Memory Pattern

All long-running workflows should follow this pattern:

```
┌─────────────────────────────────────────────────────────┐
│ TASK START                                               │
│   └── Create initial checkpoint with task context        │
│   └── Initialize todo list                               │
│                                                          │
│ EVERY 20-30 OPERATIONS                                   │
│   └── Update checkpoint with progress                    │
│   └── Update todo list status                            │
│                                                          │
│ MILESTONE REACHED                                         │
│   └── Create detailed checkpoint                         │
│   └── Save key findings to MCP memory (if reusable)      │
│                                                          │
│ BEFORE COMPACTION (auto via PreCompact hook)             │
│   └── Auto-checkpoint created by system                  │
│                                                          │
│ AFTER COMPACTION / SESSION RESUME                        │
│   └── Read latest checkpoint                             │
│   └── Search MCP memory for relevant context             │
│   └── Continue from documented Next Steps                │
│                                                          │
│ TASK COMPLETE                                             │
│   └── Final checkpoint with summary                      │
│   └── Save reusable patterns to MCP memory               │
│   └── Clean up temporary checkpoints                     │
└─────────────────────────────────────────────────────────┘
```

### Checkpoint Naming Convention

| Type              | Format                                      | Example                                |
| ----------------- | ------------------------------------------- | -------------------------------------- |
| Manual checkpoint | `checkpoint-{YYMMDD}-{HHMM}-{slug}.md`      | `checkpoint-250106-1430-user-auth.md`  |
| Auto checkpoint   | `memory-checkpoint-{timestamp}.md`          | `memory-checkpoint-20250106-143000.md` |
| Analysis notes    | `{type}-{date}-{slug}.md`                   | `analysis-250106-payment-flow.md`      |
| Task notes        | `.ai/workspace/analysis/{slug}.analysis.md` | Used by feature-implementation         |

### Related Commands & Skills

| Command/Skill            | Purpose                             |
| ------------------------ | ----------------------------------- |
| `/checkpoint`            | Create manual memory checkpoint     |
| `/context`               | Load project context                |
| `/compact`               | Manually trigger context compaction |
| `/watzup`                | Generate progress summary           |
| `feature-implementation` | Uses task analysis notes pattern    |
| `debug`                  | Uses investigation logs             |
| `feature-investigation`  | Uses analysis report pattern        |

### Memory Decision Matrix

| Context Type            | Storage         | Why                      |
| ----------------------- | --------------- | ------------------------ |
| Task progress           | File checkpoint | Specific to current task |
| Code patterns           | MCP memory      | Reusable across sessions |
| Bug solutions           | MCP memory      | Helps future debugging   |
| Service boundaries      | MCP memory      | Architectural knowledge  |
| Investigation findings  | File checkpoint | Task-specific analysis   |
| Architectural decisions | MCP memory      | Long-term knowledge      |

## Related

- `learn`
- `context-optimization`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
