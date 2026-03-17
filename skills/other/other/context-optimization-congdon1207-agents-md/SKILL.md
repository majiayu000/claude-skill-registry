---
name: context-optimization
description: Use when managing context window usage, compressing long sessions, or optimizing token usage. Triggers on keywords like "context", "memory", "tokens", "compress", "summarize session", "context limit", "optimize context".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite, mcp__memory__*
infer: true
---

# Context Optimization & Management

Manage context window efficiently to maintain productivity in long sessions.

---

## Context Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Context Window (~200K tokens)           │
├─────────────────────────────────────────────────────────────┤
│ System Prompt (CLAUDE.md excerpts)          ~2,000 tokens   │
│ ─────────────────────────────────────────────────────────── │
│ Working Memory (current task state)         ~10,000 tokens  │
│ ─────────────────────────────────────────────────────────── │
│ Retrieved Context (RAG from codebase)       ~20,000 tokens  │
│ ─────────────────────────────────────────────────────────── │
│ Episodic Memory (past session learnings)    ~5,000 tokens   │
│ ─────────────────────────────────────────────────────────── │
│ Tool Descriptions (relevant tools only)     ~3,000 tokens   │
└─────────────────────────────────────────────────────────────┘
```

---

## Four Context Strategies

### 1. Writing (Save Important Context)

Save critical findings to persistent memory:

```javascript
// After discovering important patterns or decisions
mcp__memory__create_entities([
    {
        name: 'EmployeeValidation',
        entityType: 'Pattern',
        observations: ['Uses PlatformValidationResult fluent API', 'Async validation via ValidateRequestAsync', 'Found in Growth.Application/UseCaseCommands/']
    }
]);
```

**When to Write:**

- Discovered architectural patterns
- Important business rules
- Cross-service dependencies
- Solution decisions

### 2. Selecting (Retrieve Relevant Context)

Load relevant memories at session start:

```javascript
// Search for relevant patterns
mcp__memory__search_nodes({ query: 'Employee validation pattern' });

// Open specific entities
mcp__memory__open_nodes({ names: ['EmployeeValidation', 'GrowthService'] });
```

**When to Select:**

- Starting a related task
- Continuing previous work
- Cross-referencing patterns

### 3. Compressing (Summarize Long Trajectories)

Create context anchors every 10 operations:

```markdown
=== CONTEXT ANCHOR ===
Current Task: Implement employee leave request feature
Completed:

- Created LeaveRequest entity with validation
- Added SaveLeaveRequestCommand with handler
- Implemented entity event handler for notifications

Remaining:

- Create GetLeaveRequestListQuery
- Add controller endpoint
- Write unit tests

Key Findings:

- Leave requests use GrowthRootRepository
- Notifications via entity event handlers, not direct calls
- Validation uses PlatformValidationResult.AndAsync()

# Next Action: Create query handler with GetQueryBuilder pattern
```

### 4. Isolating (Use Sub-Agents)

Delegate specialized tasks to sub-agents:

```javascript
// Explore codebase (reduced context)
Task({ subagent_type: 'Explore', prompt: 'Find all entity event handlers in Growth service' });

// Plan implementation (focused context)
Task({ subagent_type: 'Plan', prompt: 'Plan leave request approval workflow' });
```

**When to Isolate:**

- Broad codebase exploration
- Independent research tasks
- Parallel investigations

---

## Context Anchor Protocol

**Every 10 operations, write a context anchor:**

1. **Re-read original task** from todo list or initial prompt
2. **Verify alignment** with current work
3. **Write anchor** summarizing progress
4. **Save to memory** if discovering important patterns

```markdown
=== CONTEXT ANCHOR [10] ===
Task: [Original task description]
Phase: [Current phase number]
Progress: [What's been completed]
Findings: [Key discoveries]
Next: [Specific next step]
Confidence: [High/Medium/Low]
===========================
```

---

## Token-Efficient Patterns

### File Reading

```javascript
// ❌ Reading entire files
Read({ file_path: 'large-file.cs' });

// ✅ Read specific sections
Read({ file_path: 'large-file.cs', offset: 100, limit: 50 });

// ✅ Use grep to find specific content first
Grep({ pattern: 'class SaveEmployeeCommand', path: 'src/' });
```

### Search Optimization

```javascript
// ❌ Multiple sequential searches
Grep({ pattern: 'CreateAsync' });
Grep({ pattern: 'UpdateAsync' });
Grep({ pattern: 'DeleteAsync' });

// ✅ Combined pattern
Grep({ pattern: 'CreateAsync|UpdateAsync|DeleteAsync', output_mode: 'files_with_matches' });
```

### Parallel Operations

```javascript
// ✅ Parallel reads for independent files
[Read({ file_path: 'file1.cs' }), Read({ file_path: 'file2.cs' }), Read({ file_path: 'file3.cs' })];
```

---

## Memory Management Commands

### Save Session Summary

```javascript
// Before ending session or hitting limits
const summary = {
    task: 'Implementing employee leave request feature',
    completed: ['Entity', 'Command', 'Handler'],
    remaining: ['Query', 'Controller', 'Tests'],
    discoveries: ['Use entity events for notifications'],
    files: ['LeaveRequest.cs', 'SaveLeaveRequestCommand.cs']
};

// Save to memory
mcp__memory__create_entities([
    {
        name: `Session_${new Date().toISOString().split('T')[0]}`,
        entityType: 'SessionSummary',
        observations: [JSON.stringify(summary)]
    }
]);
```

### Load Previous Session

```javascript
// At session start
mcp__memory__search_nodes({ query: 'Session leave request' });
```

---

## Anti-Patterns

| Anti-Pattern               | Better Approach                |
| -------------------------- | ------------------------------ |
| Reading entire large files | Use offset/limit or grep first |
| Sequential searches        | Combine with OR patterns       |
| Repeating same searches    | Cache results in memory        |
| No context anchors         | Write anchor every 10 ops      |
| Not using sub-agents       | Isolate exploration tasks      |
| Forgetting discoveries     | Save to memory entities        |

---

## Quick Reference

**Token Estimation:**

- 1 line of code ≈ 10-15 tokens
- 1 page of text ≈ 500 tokens
- Average file ≈ 1,000-3,000 tokens

**Context Thresholds:**

- 50K tokens: Consider compression
- 100K tokens: Required compression
- 150K tokens: Critical - save and summarize

**Memory Commands:**

- `mcp__memory__create_entities` - Save new knowledge
- `mcp__memory__search_nodes` - Find relevant context
- `mcp__memory__add_observations` - Update existing entities
