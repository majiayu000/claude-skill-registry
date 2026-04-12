---
name: memory-palace
description: "Hierarchical memory organization for multi-session context retention. Wings (projects) > Rooms (domains) > Drawers (decisions). Semantic search across all memories with zero cloud dependency."
---

# Memory Palace

Hierarchical, persistent memory system for Claude Code sessions. Organizes knowledge so agents never lose context across sessions.

## Architecture

```
Palace (global)
  Wing: project-name
    Room: authentication
      Drawer: "chose JWT over sessions" (2026-04-07)
      Drawer: "rate limiting at 100 req/min" (2026-04-06)
    Room: database
      Drawer: "PostgreSQL with pgvector" (2026-04-05)
      Drawer: "migration strategy: blue-green" (2026-04-04)
    Room: deployment
      Drawer: "Vercel + GitHub Actions" (2026-04-03)
  Wing: another-project
    Room: ...
```

## Storage Format

All memories stored in `~/.claude/palace/` as flat JSONL files per wing:

```
~/.claude/palace/
  index.json          # Wing registry
  my-project.jsonl    # All drawers for this wing
  other-project.jsonl # All drawers for this wing
```

### Drawer Entry Format
```json
{
  "id": "d-abc123",
  "wing": "my-project",
  "room": "authentication",
  "content": "Chose JWT with refresh tokens over session-based auth. Reason: stateless, mobile-friendly, scalable.",
  "tags": ["auth", "jwt", "architecture"],
  "timestamp": "2026-04-07T14:30:00Z",
  "session_id": "s-xyz789",
  "agent": "architect",
  "type": "decision"
}
```

### Entry Types
- `decision` - Architectural or design choice with reasoning
- `discovery` - Something learned about the codebase
- `error` - Error encountered and how it was resolved
- `constraint` - External limitation or requirement
- `pattern` - Recurring code or workflow pattern

## Operations

### Store a Memory
When an important decision, discovery, or constraint is identified:

```
Wing: detect from CLAUDE_PROJECT_DIR or package.json name
Room: infer from topic (auth, db, deploy, frontend, api, etc.)
Content: what was decided/discovered and WHY
Tags: relevant keywords for search
```

### Recall Memories
Before starting work on a topic, query relevant rooms:

```
1. Get wing from current project
2. List rooms with recent activity
3. Load drawers matching current task keywords
4. Inject as context: "Previous decisions in this area: ..."
```

### Search Across Wings
For cross-project pattern detection:

```
Search all wings for entries matching query
Return sorted by relevance (keyword match + recency)
Useful for: "Have I solved this before in another project?"
```

## Integration Points

### With Agents
- **architect**: Store architectural decisions automatically
- **self-learner**: Store error resolutions as discoveries
- **planner**: Load relevant rooms before planning
- **compass**: Use palace for session recovery context

### With Hooks
- **palace-auto-save** hook: Captures decisions from conversation
- **palace-recall** hook: Injects relevant memories at session start
- **pre-compact-continuity**: Saves WIP state to palace before compaction

### With Existing Memory System
Palace complements (does not replace) the existing PostgreSQL memory:
- PostgreSQL: raw embeddings, vector search, learning store
- Palace: structured, human-readable, hierarchical organization
- Both can be queried; palace is faster for targeted recall

## Room Detection Heuristics

| Keywords in Context | Room |
|---------------------|------|
| auth, login, session, JWT, OAuth | authentication |
| database, SQL, migration, schema | database |
| deploy, CI/CD, Docker, K8s | deployment |
| React, CSS, component, UI | frontend |
| API, endpoint, REST, GraphQL | api |
| test, TDD, coverage, mock | testing |
| security, XSS, injection, CORS | security |
| performance, cache, optimize | performance |
| config, env, settings | configuration |

## When to Store

**ALWAYS store:**
- Architectural decisions with reasoning
- External constraints (client requirements, hosting limits)
- Error resolutions that took > 5 minutes to solve
- Chosen patterns and why alternatives were rejected

**NEVER store:**
- Code snippets (they're in git)
- Temporary debugging notes
- Information already in CLAUDE.md
- Ephemeral task progress (use tasks for that)
