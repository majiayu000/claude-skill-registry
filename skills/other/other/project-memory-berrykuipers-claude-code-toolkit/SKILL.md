---
name: project-memory
description: Persist and recall project-specific context across sessions. Store architectural decisions, patterns, solutions, and learnings. Automatically recall relevant context when facing similar problems.
---

# Project Memory Skill

Use the memory MCP (`mcp__memory__*`) to persist project knowledge across sessions. This complements personal memory (Qdrant) by focusing on **project-specific** technical context.

## When to Store

### Architectural Decisions
Store when you make or discover significant choices:
- "We chose X pattern over Y because..."
- "This service uses Z approach for..."
- "The team decided to structure components as..."

```
Store: "Auth architecture: JWT tokens with httpOnly cookies, refresh tokens in Redis,
15min access / 7d refresh. Chosen over session-based for API scalability."
Tags: ["architecture", "auth", "decisions"]
```

### Solved Problems
Store when you fix non-trivial issues:
- Complex debugging sessions
- Performance optimizations
- Integration gotchas

```
Store: "Prisma N+1 fix: Use `include` with explicit `select` for nested relations.
findMany({ include: { posts: { select: { id: true, title: true } } } })"
Tags: ["prisma", "performance", "patterns"]
```

### Project-Specific Patterns
Store recurring patterns unique to this codebase:
- Custom hooks and their usage
- Service layer conventions
- Error handling approaches

```
Store: "Error handling pattern: All API errors extend BaseError with code,
statusCode, isOperational. Use errorHandler middleware for centralized catching."
Tags: ["patterns", "errors", "conventions"]
```

### Implementation Learnings
Store insights from implementation:
- "This API requires X header"
- "This library has quirk Y"
- "Integration with Z needs..."

## When to Recall

### Before Implementation
Check memory when starting work that might have prior context:
- "Implementing auth" → recall auth-related memories
- "Adding new API endpoint" → recall API patterns
- "Fixing performance" → recall past optimizations

### When Stuck
Query memory when facing challenges:
- "Similar error before?"
- "How did we handle this pattern?"
- "What was the decision about X?"

### During Review
Check for consistency with past decisions:
- "Does this align with our patterns?"
- "Have we solved this differently elsewhere?"

## How to Use

### Storing Memories

```
Use mcp__memory__store or similar tool:
- content: Clear, searchable description
- tags: Relevant categories for retrieval
- metadata: { project: "project-name", type: "decision|pattern|fix|learning" }
```

**Good memory content:**
- Concise but complete
- Includes the "why" not just "what"
- Searchable keywords
- Context for future recall

### Recalling Memories

```
Use mcp__memory__search or similar tool:
- query: Natural language description of what you need
- tags: Filter by category if known
- limit: Start with 5, expand if needed
```

**Effective queries:**
- "authentication implementation decisions"
- "prisma performance patterns"
- "error handling conventions"
- "API rate limiting approach"

## Memory Categories

Use consistent tags for organization:

| Tag | Use For |
|-----|---------|
| `architecture` | System design, service boundaries |
| `patterns` | Recurring code patterns |
| `decisions` | Why we chose X over Y |
| `fixes` | Bug fixes and debugging solutions |
| `performance` | Optimizations, bottlenecks |
| `integrations` | External API quirks, configs |
| `conventions` | Team standards, naming, structure |
| `gotchas` | Non-obvious behaviors, pitfalls |

## What NOT to Store

- Generic programming knowledge (you already know this)
- Trivial fixes (typos, simple syntax)
- Temporary workarounds (unless documenting tech debt)
- Sensitive data (credentials, keys, PII)

## Relationship with Personal Memory (Qdrant)

| Project Memory | Personal Memory (Qdrant) |
|----------------|--------------------------|
| Technical decisions | Life experiences |
| Code patterns | Personal preferences |
| Project-specific | Cross-project/personal |
| Implementation details | Skills, relationships |
| Ephemeral (project lifetime) | Permanent (life memory) |

**Rule:** If it's about THIS project's code → project memory. If it's about Berry → Qdrant.

## Session Start Reminder

At session start, consider:
1. What work am I continuing?
2. Are there relevant memories to load?
3. Query: "recent decisions about [current task area]"

## Examples

### Example 1: Storing an Architecture Decision

After implementing a feature:
```
"Implemented image generation queue with Bull + Redis. Chose over in-memory
because: 1) Survives restarts, 2) Rate limiting per user, 3) Priority queues
for premium users. Max 3 concurrent jobs per user, 10 global."

Tags: ["architecture", "queue", "images", "decisions"]
```

### Example 2: Recalling Before Work

Starting work on similar feature:
```
Query: "queue implementation patterns"
→ Recalls Bull + Redis decision
→ Apply same patterns for consistency
```

### Example 3: Storing a Gotcha

After debugging:
```
"Gemini API safetySettings must be top-level param, NOT inside generationConfig.
Wasted 2 hours on this. SDK docs are misleading."

Tags: ["gotchas", "gemini", "api", "integrations"]
```

## Integration with Workflow

1. **Issue Pickup** → Recall related context
2. **Implementation** → Store patterns/decisions as you go
3. **PR Creation** → Ensure key decisions are stored
4. **Review** → Check consistency with stored patterns
