---
name: ralph-memory
description: Query and manage RALPH's persistent memory layer
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

# RALPH-MEMORY - Knowledge Management

Query and manage RALPH's persistent cross-session memory.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-memory` | Show memory stats and recent insights |
| `/ralph-memory query "term"` | Search memory for a term |
| `/ralph-memory insights` | Show all insights |
| `/ralph-memory entities` | Show all entities |
| `/ralph-memory add-insight "learning"` | Add a manual insight |
| `/ralph-memory export` | Export memory to file |
| `/ralph-memory cleanup` | Clean old entries |

## Triggers

- `/ralph-memory`
- "show memory"
- "what have you learned"
- "search memory"

## Memory Structure

RALPH stores knowledge in three JSON files:

```
.ralph/memory/
├── entities.json       # Files, functions, classes, patterns
├── relationships.json  # How entities relate to each other
└── insights.json       # Learnings and gotchas
```

### Entities

Things RALPH knows about:

```json
{
  "type": "file",
  "name": "src/types/user.ts",
  "properties": {
    "exports": ["User", "CreateUserInput"],
    "imports": ["zod"],
    "lastModified": "2026-01-25T10:00:00Z"
  }
}
```

**Entity Types:**
- `file` - Source files and their contents
- `function` - Functions and their signatures
- `class` - Classes and their methods
- `pattern` - Architectural patterns used
- `config` - Configuration files
- `test` - Test files and coverage

### Relationships

How entities connect:

```json
{
  "fromId": "src/types/user.ts",
  "toId": "src/services/user.service.ts",
  "type": "imports",
  "properties": {
    "symbols": ["User", "CreateUserInput"]
  }
}
```

**Relationship Types:**
- `imports` - File imports another
- `exports` - File exports symbols
- `uses` - Function uses another
- `extends` - Class extends another
- `implements` - Class implements interface
- `tests` - Test file tests source

### Insights

Learnings from implementation:

```json
{
  "context": "Implementing user authentication",
  "learning": "Always export new types from index.ts immediately",
  "tags": ["types", "exports", "patterns"],
  "occurrences": 3,
  "createdAt": "2026-01-25T10:00:00Z",
  "lastSeen": "2026-01-25T15:00:00Z"
}
```

## Commands

### Show Stats (Default)

```
╔════════════════════════════════════════════════════════════════╗
║                    RALPH Memory                                 ║
╚════════════════════════════════════════════════════════════════╝

Entities: 45 total
  - Files: 28
  - Functions: 12
  - Patterns: 5

Relationships: 67 total
  - imports: 34
  - exports: 22
  - tests: 11

Insights: 15 total
  - Unique tags: 8
  - Total occurrences: 42

Recent Insights:
  1. "Always export new types from index.ts" (×3)
  2. "Use Zod for runtime validation" (×2)
  3. "Prefer async/await over raw promises"

Top Tags: types, patterns, validation, testing, exports
```

### Query Memory

```bash
/ralph-memory query "validation"
```

Output:

```
╔════════════════════════════════════════════════════════════════╗
║                    Memory Query: "validation"                   ║
╚════════════════════════════════════════════════════════════════╝

Entities (3 matches):
  [file] src/schemas/user.schema.ts
    Properties: uses Zod validation

  [pattern] runtime-validation
    Properties: Use Zod for all runtime checks

  [function] validateUserInput
    Properties: Located in src/services/user.service.ts

Relationships (2 matches):
  src/services/user.service.ts --uses--> src/schemas/user.schema.ts
  src/routes/user.routes.ts --uses--> validateUserInput

Insights (2 matches):
  - "Use Zod for runtime validation" (×2)
    Tags: validation, zod, patterns

  - "Validate inputs at API boundaries"
    Tags: validation, api, security
```

### Show Insights

```bash
/ralph-memory insights
```

Output:

```
╔════════════════════════════════════════════════════════════════╗
║                    All Insights                                 ║
╚════════════════════════════════════════════════════════════════╝

By Frequency:
  1. "Always export new types from index.ts" (×5)
     Tags: types, exports, patterns
     Context: Multiple type definition tasks

  2. "Use Zod for runtime validation" (×3)
     Tags: validation, zod
     Context: User input validation

  3. "Prefer async/await over raw promises" (×2)
     Tags: async, patterns
     Context: Service layer implementation

By Tag:
  [patterns] 5 insights
  [types] 3 insights
  [validation] 3 insights
  [testing] 2 insights
  [security] 1 insight
```

### Add Manual Insight

```bash
/ralph-memory add-insight "Database migrations should be run before tests"
```

Use AskUserQuestion:

```
? What was the context for this learning?
> Running integration tests

? Add tags (comma-separated):
> database, migrations, testing
```

Output:

```
✓ Insight added:
  "Database migrations should be run before tests"
  Context: Running integration tests
  Tags: database, migrations, testing
```

### Export Memory

```bash
/ralph-memory export
```

Output:

```
╔════════════════════════════════════════════════════════════════╗
║                    Memory Export                                ║
╚════════════════════════════════════════════════════════════════╝

Exporting to: .ralph/memory-export-2026-01-25.json

Contents:
  - 45 entities
  - 67 relationships
  - 15 insights

✓ Export complete

This file can be:
  - Shared with team members
  - Imported into another project
  - Backed up for safety
```

### Cleanup Memory

```bash
/ralph-memory cleanup
```

Output:

```
╔════════════════════════════════════════════════════════════════╗
║                    Memory Cleanup                               ║
╚════════════════════════════════════════════════════════════════╝

Analyzing memory entries older than 90 days...

Candidates for removal:
  - 5 entities (not referenced in 90+ days)
  - 8 relationships (orphaned)
  - 2 insights (single occurrence, old)

? Proceed with cleanup?
  ○ Yes, remove old entries
  ○ No, keep everything

Cleanup Results:
  ✓ Removed 5 entities
  ✓ Removed 8 relationships
  ✓ Kept 15 insights (frequently occurring)

Memory size reduced by 12%
```

## Agent Memory Integration

### Planner Agent

Queries memory before planning:

```
Loading memory context...

Relevant patterns found:
  - "Use service layer pattern for business logic"
  - "Separate types from implementation"

Past similar implementations:
  - US-005: User authentication (similar patterns)
  - US-012: Payment processing (related concepts)

Applying learnings to plan...
```

### Coder Agent

Logs patterns during implementation:

```
Implementation complete.

Insights logged:
  + "This project uses barrel exports (index.ts)"
  + "Error handling uses custom AppError class"

Entities tracked:
  + [file] src/services/payment.service.ts
  + [function] processPayment
  + [function] validateCard
```

### QA Reviewer

Logs recurring issues:

```
QA validation complete.

Recurring issues detected:
  ⚠ "Missing exports" - 3rd occurrence
    → Consider adding to pre-commit hook

Insight logged:
  + "Export statements should be added immediately after creating types"
```

## Memory Query in Prompts

Agents include memory context in their prompts:

```markdown
## Memory Context

### Relevant Insights
- "Always export new types from index.ts"
- "Use Zod for runtime validation"
- "Prefer async/await over raw promises"

### Related Entities
- src/types/user.ts (exports User, CreateUserInput)
- src/schemas/user.schema.ts (Zod validation)

### Past Patterns
- Service layer pattern used in src/services/
- Repository pattern for data access
```

## Error Handling

| Error | Action |
|-------|--------|
| Memory not initialized | Run `initMemory()` automatically |
| Query returns nothing | Suggest broader search terms |
| Export fails | Check disk space, permissions |
| Cleanup too aggressive | Offer to restore from backup |

## Best Practices

1. **LOG LIBERALLY** - More insights = smarter future iterations
2. **TAG CONSISTENTLY** - Use standard tags for better queries
3. **CLEAN REGULARLY** - Remove stale entries every few weeks
4. **EXPORT OFTEN** - Backup valuable learnings
5. **SHARE ACROSS PROJECTS** - Import proven patterns
