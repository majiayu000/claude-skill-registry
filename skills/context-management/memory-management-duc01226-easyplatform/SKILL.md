---
name: memory-management
description: Use when saving or retrieving important patterns, decisions, and learnings across sessions. Triggers on keywords like "remember", "save pattern", "recall", "memory", "persist", "knowledge base", "learnings".
allowed-tools: Read, Write, Edit, mcp__memory__*
infer: true
---

# Memory Management & Knowledge Persistence

Build and maintain a knowledge graph of patterns, decisions, and learnings across sessions.

This is the **SSOT** for MCP memory operations. Other skills should reference this.

---

## Entity Types

| Entity Type       | Purpose                            | Examples                        |
| ----------------- | ---------------------------------- | ------------------------------- |
| `Pattern`         | Recurring code patterns            | CQRS, Validation, Repository    |
| `Decision`        | Architectural/design decisions     | Why we chose X over Y           |
| `BugFix`          | Bug solutions for future reference | Race condition fixes            |
| `ServiceBoundary` | Service ownership                  | TextSnippet owns Snippets       |
| `SessionSummary`  | End-of-session progress            | Task progress, next steps       |
| `Dependency`      | Cross-service dependencies         | TextSnippet depends on Accounts |
| `AntiPattern`     | Patterns to avoid                  | Don't call side effects in cmd  |

---

## Quick Operations

| Operation           | Command                                         |
| ------------------- | ----------------------------------------------- |
| Create entity       | `mcp__memory__create_entities([...])`           |
| Create relation     | `mcp__memory__create_relations([...])`          |
| Add observations    | `mcp__memory__add_observations([...])`          |
| Search              | `mcp__memory__search_nodes({ query })`          |
| Open by name        | `mcp__memory__open_nodes({ names })`            |
| Read all            | `mcp__memory__read_graph()`                     |
| Delete entity       | `mcp__memory__delete_entities({ entityNames })` |
| Delete observations | `mcp__memory__delete_observations([...])`       |
| Delete relation     | `mcp__memory__delete_relations([...])`          |

For detailed examples and templates, see [references/memory-operations.md](references/memory-operations.md).

---

## When to Save

### Always Save
1. Discovered patterns not in documentation
2. Complex bug solutions
3. Service boundary ownership
4. Architectural decisions with rationale
5. Anti-patterns encountered

### Save at Session End
Create `SessionSummary` entity with: Task, Completed, Remaining, Key Files, Discoveries, Next Steps.

---

## Session Workflow

### Session Start
1. Search for related context: `search_nodes({ query: 'task keywords' })`
2. Load relevant entities: `open_nodes({ names: [...] })`
3. Check incomplete sessions: `search_nodes({ query: 'SessionSummary Remaining' })`

### During Work
- Save discoveries as `Pattern` entities
- Save architectural choices as `Decision` entities
- Save bugs as `BugFix` entities

### Session End
- Create `SessionSummary` with progress snapshot
- Update existing entities with new observations

---

## Importance Scoring

| Score | Criteria                                    |
| ----- | ------------------------------------------- |
| 10    | Critical bug fixes, security issues         |
| 8-9   | Architectural decisions, service boundaries |
| 6-7   | Code patterns, best practices               |
| 4-5   | Session summaries, progress notes           |
| 1-3   | Temporary notes, exploration results        |

---

## Maintenance

- **Consolidation**: Merge fragmented observations into comprehensive ones
- **Cleanup**: Delete session summaries older than 30 days
- **Pruning**: Remove outdated patterns no longer relevant

See [references/memory-operations.md](references/memory-operations.md) for operation details and templates.


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
