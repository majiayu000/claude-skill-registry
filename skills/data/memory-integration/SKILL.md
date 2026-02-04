---
name: memory-integration
description: Use to maintain context across sessions - integrates episodic-memory for conversation recall and mcp__memory knowledge graph for persistent facts
---

# Memory Integration

## Overview

Use both memory systems to maintain context across sessions.

**Core principle:** You have no memory between sessions. Use these tools to remember.

**Systems:**
- **Episodic Memory** - Conversation history search
- **Knowledge Graph** (mcp__memory) - Structured facts and relationships

## When to Use Memory

| Moment | Memory Action |
|--------|---------------|
| Session start | Search for relevant context |
| Before starting issue | Search for previous work |
| Making decision | Check for past decisions |
| Completing work | Store important learnings |
| Session end | Store key outcomes |

## Episodic Memory

### What It Stores

- Full conversation history
- Decisions made
- Problems solved
- Approaches tried
- Lessons learned

### Searching Episodic Memory

Use the episodic-memory skill or MCP tools:

```
Search for:
- Issue number: "issue 123", "#123"
- Feature name: "authentication", "user login"
- Problem type: "TypeScript error", "build failure"
- Project name: repository name
```

#### Semantic Search (Single Query)

```javascript
// Search with natural language
mcp__plugin_episodic-memory_episodic-memory__search({
  query: "user authentication implementation decisions"
})
```

#### Precise Search (Multiple Concepts)

```javascript
// Search for intersection of concepts
mcp__plugin_episodic-memory_episodic-memory__search({
  query: ["authentication", "session", "JWT"]
})
```

#### Reading Full Conversations

After finding relevant results:

```javascript
// Read the full conversation
mcp__plugin_episodic-memory_episodic-memory__read({
  path: "/path/to/conversation.jsonl"
})
```

### What to Search For

| Situation | Search Terms |
|-----------|-------------|
| Starting issue #123 | "issue 123", "#123" |
| Working on auth | "authentication", "login", "session" |
| TypeScript problem | "TypeScript", "type error", specific error message |
| Similar feature | Feature name, related concepts |

## Knowledge Graph (mcp__memory)

### What It Stores

- Entities (Projects, Issues, Decisions, Patterns)
- Relationships between entities
- Observations about entities

### Creating Entities

Store important facts:

```javascript
// Create an entity for a project decision
mcp__memory__create_entities({
  entities: [{
    name: "Decision: Use JWT for Auth",
    entityType: "Decision",
    observations: [
      "Decided on 2024-12-01",
      "JWT chosen over sessions for API statelessness",
      "Related to issue #123",
      "Implementation in src/auth/jwt.ts"
    ]
  }]
})
```

### Creating Relationships

Link entities together:

```javascript
// Create relationships
mcp__memory__create_relations({
  relations: [
    {
      from: "Project: MyApp",
      to: "Decision: Use JWT for Auth",
      relationType: "has_decision"
    },
    {
      from: "Issue #123",
      to: "Decision: Use JWT for Auth",
      relationType: "resulted_in"
    }
  ]
})
```

### Searching the Graph

```javascript
// Search for relevant nodes
mcp__memory__search_nodes({
  query: "authentication"
})

// Open specific nodes
mcp__memory__open_nodes({
  names: ["Decision: Use JWT for Auth"]
})

// Read entire graph (for small graphs)
mcp__memory__read_graph({})
```

## Memory Protocol

### At Session Start

1. **Search episodic memory** for:
   - Current issue number
   - Project/repository name
   - Active feature being worked on

2. **Search knowledge graph** for:
   - Project entity
   - Related decisions
   - Known patterns

3. **Synthesize context** before proceeding

### During Work

Store as you go:

| Event | Store In |
|-------|----------|
| Major decision | Knowledge graph entity |
| Problem solved | Add observation to issue entity |
| Pattern discovered | Knowledge graph entity |
| Lesson learned | Add observation |

### At Session End

1. **Update knowledge graph** with:
   - New decisions made
   - Problems solved
   - Patterns discovered

2. **Add observations** to existing entities:
   - Progress on issues
   - Learnings
   - Next steps

## Entity Types

Suggested entity types for the knowledge graph:

| Type | Use For | Example |
|------|---------|---------|
| Project | Repository/codebase | "Project: MyApp" |
| Issue | GitHub issues | "Issue #123: Auth" |
| Decision | Architectural decisions | "Decision: Use JWT" |
| Pattern | Code patterns | "Pattern: Repository Layer" |
| Problem | Known issues | "Problem: Race Condition in X" |
| Person | Collaborators | "Person: Alice (maintainer)" |

## Example: Issue Memory Flow

### Session 1: Starting Issue

```javascript
// Search for any previous context
const episodic = await search("issue 456 user profile");
const graph = await search_nodes("user profile");

// If nothing found, create fresh entity
await create_entities({
  entities: [{
    name: "Issue #456: User Profile Page",
    entityType: "Issue",
    observations: [
      "Started: 2024-12-01",
      "Scope: Profile display, edit, avatar upload"
    ]
  }]
});
```

### Session 1: Mid-Work Decision

```javascript
// Store a decision made
await add_observations({
  observations: [{
    entityName: "Issue #456: User Profile Page",
    contents: [
      "Decision: Using react-image-crop for avatar cropping",
      "Reason: Best mobile support, active maintenance"
    ]
  }]
});
```

### Session 2: Resuming

```javascript
// Search for context
const results = await search("issue 456");
// Read: "Using react-image-crop for avatar cropping"

// Continue with context maintained
```

## What to Store

### Always Store

- Architectural decisions with rationale
- Non-obvious problem solutions
- Important constraints discovered
- Dependencies between components

### Don't Store

- Trivial implementation details
- Things obvious from code
- Temporary debugging notes
- Speculation without conclusion

## Checklist

At session start:
- [ ] Search episodic memory for issue/project
- [ ] Search knowledge graph for context
- [ ] Note relevant findings

During work:
- [ ] Store major decisions
- [ ] Record problem solutions
- [ ] Note discovered patterns

At session end:
- [ ] Update entities with progress
- [ ] Add new learnings
- [ ] Record next steps

## Integration

This skill is called by:
- `session-start` - Initial context gathering
- `issue-driven-development` - Step 4

This skill supports:
- Cross-session continuity
- Decision documentation
- Pattern discovery
