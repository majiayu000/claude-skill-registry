---
name: memory-management
description: Use when saving or retrieving important patterns, decisions, and learnings across sessions. Triggers on keywords like "remember", "save pattern", "recall", "memory", "persist", "knowledge base", "learnings".
allowed-tools: Read, Write, Edit, mcp__memory__*
infer: true
---

# Memory Management & Knowledge Persistence

Build and maintain a knowledge graph of patterns, decisions, and learnings across sessions.

---

## Memory Entity Types

| Entity Type       | Purpose                                | Examples                       |
| ----------------- | -------------------------------------- | ------------------------------ |
| `Pattern`         | Recurring code patterns                | CQRS, Validation, Repository   |
| `Decision`        | Architectural/design decisions         | Why we chose X over Y          |
| `BugFix`          | Bug solutions for future reference     | Race condition fixes           |
| `ServiceBoundary` | Service ownership and responsibilities | TextSnippet owns Snippets      |
| `SessionSummary`  | End-of-session progress snapshots      | Task progress, next steps      |
| `Dependency`      | Cross-service dependencies             | TextSnippet depends on Accounts|
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
        from: 'TextSnippetService',
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
mcp__memory__open_nodes({ names: ['EmployeeValidationPattern', 'TextSnippetService'] });

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
│                     EasyPlatform Knowledge                    │
├─────────────────────────────────────────────────────────────┤
│  Services                                                   │
│  ├── TextSnippetService ──depends_on──> AccountsService          │
│  ├── TalentsService ──depends_on──> AccountsService         │
│  └── SurveysService ──depends_on──> AccountsService         │
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
│  └── LeaveRequest ──owned_by──> TextSnippetService               │
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
