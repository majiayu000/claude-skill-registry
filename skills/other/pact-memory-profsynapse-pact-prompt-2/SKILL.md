---
name: pact-memory
description: |
  Persistent memory for PACT agents. Save context, goals, lessons learned,
  decisions, and entities. Semantic search across sessions.
  Use when: saving session context, recalling past decisions, searching lessons.
  Triggers: memory, save memory, search memory, lessons learned, remember, recall
---

# PACT Memory Skill

Persistent memory system for PACT framework agents. Store and retrieve context,
goals, lessons learned, decisions, and entities across sessions with semantic search.

## Overview

The PACT Memory skill provides:
- **Rich Memory Objects**: Store context, goals, tasks, lessons, decisions, and entities
- **Semantic Search**: Find relevant memories using natural language queries
- **Graph-Enhanced Retrieval**: Memories linked to files are boosted when working on related files
- **Session Tracking**: Automatic file tracking and session context
- **Cross-Session Learning**: Memories persist across sessions for cumulative knowledge

## Quick Start

```python
from pact_memory.scripts import PACTMemory

# Initialize
memory = PACTMemory()

# Save a memory
memory_id = memory.save({
    "context": "Implementing user authentication",
    "goal": "Add JWT refresh token support",
    "lessons_learned": [
        "Redis INCR is atomic - perfect for rate limiting",
        "Always validate refresh token rotation"
    ],
    "decisions": [
        {
            "decision": "Use Redis for token blacklist",
            "rationale": "Fast TTL support, distributed access"
        }
    ],
    "entities": [
        {"name": "AuthService", "type": "component"},
        {"name": "TokenManager", "type": "class"}
    ]
})

# Search memories
results = memory.search("rate limiting tokens")
for mem in results:
    print(f"Context: {mem.context}")
    print(f"Lessons: {mem.lessons_learned}")

# List recent memories
recent = memory.list(limit=10)
```

## Memory Structure

Each memory can contain:

| Field | Type | Description |
|-------|------|-------------|
| `context` | string | Current working context description |
| `goal` | string | What you're trying to achieve |
| `active_tasks` | list | Tasks with status and priority |
| `lessons_learned` | list | What worked or didn't work |
| `decisions` | list | Decisions with rationale and alternatives |
| `entities` | list | Referenced components, services, modules |
| `files` | list | Associated file paths (auto-linked) |
| `project_id` | string | Auto-detected from environment |
| `session_id` | string | Auto-detected from environment |

### Task Format
```python
{"task": "Implement token refresh", "status": "in_progress", "priority": "high"}
```

### Decision Format
```python
{
    "decision": "Use Redis for caching",
    "rationale": "Fast, supports TTL natively",
    "alternatives": ["Memcached", "In-memory LRU"]
}
```

### Entity Format
```python
{"name": "AuthService", "type": "component", "notes": "Handles all auth flows"}
```

## API Reference

### PACTMemory Class

```python
class PACTMemory:
    def save(self, memory: dict, files: list = None) -> str
    def search(self, query: str, current_file: str = None, limit: int = 5) -> list[MemoryObject]
    def get(self, memory_id: str) -> MemoryObject | None
    def update(self, memory_id: str, updates: dict) -> bool
    def delete(self, memory_id: str) -> bool
    def list(self, limit: int = 20, session_only: bool = False) -> list[MemoryObject]
    def get_status(self) -> dict
```

### Convenience Functions

```python
from pact_memory.scripts import save_memory, search_memory, list_memories_simple

# Quick save
memory_id = save_memory({
    "context": "Bug fix",
    "lessons_learned": ["Check null values first"]
})

# Quick search
results = search_memory("authentication")

# Quick list
recent = list_memories_simple(10)
```

## Search Capabilities

### Semantic Search
Uses embeddings to find semantically similar memories. Requires either:
- sqlite-lembed with GGUF model (preferred)
- sentence-transformers (fallback)

### Graph-Enhanced Search
When searching while working on a file, memories linked to:
- The current file
- Files imported by/importing the current file
- Files modified in the same session

...are boosted in ranking.

### Keyword Fallback
If embeddings are unavailable, falls back to substring matching across
context, goal, lessons_learned, and decisions fields.

## Setup

### Dependencies

```bash
# Required for database
pip install sqlite-vec

# For local embeddings (recommended)
pip install sqlite-lembed

# Alternative embedding backend
pip install sentence-transformers
```

### Model Download

The skill uses a 24MB GGUF model for embeddings. Download automatically:

```python
from pact_memory.scripts.setup_memory import ensure_initialized
ensure_initialized(download_model_if_missing=True)
```

Or manually:
```bash
python -m pact_memory.scripts.setup_memory model
```

### Check Status

```python
from pact_memory.scripts.setup_memory import get_setup_status
status = get_setup_status()
print(f"Semantic search: {'Available' if status['can_use_semantic_search'] else 'Unavailable'}")
```

## Storage

Memories are stored in `~/.claude/pact-memory/memory.db` using SQLite with:
- WAL mode for crash safety
- Vector extensions for semantic search
- Graph tables for file relationships

## Command Line Usage

When invoked via `/pact-memory <command> "<args>"`:

### Save Command
```
/pact-memory save "<description>"
```

**IMPORTANT**: The description argument is just a hint. You MUST construct a comprehensive memory object with ALL relevant fields. Never just save the raw string. Think of each memory as a detailed journal entry that your future self (or another agent) needs to fully understand what happened, why it mattered, and what was learned.

**Required fields for every save:**

| Field | Minimum Length | What to Include |
|-------|----------------|-----------------|
| `context` | 3-5 sentences (paragraph) | Full background: what you were working on, why, what led to this point, relevant history, the state of things when this memory was created |
| `goal` | 1-2 sentences | The specific objective, including success criteria if applicable |
| `lessons_learned` | 3-5 items | Specific, actionable insights with enough detail to be useful months later. Each lesson should explain the "why" not just the "what" |

**Recommended fields:**
- `decisions`: Key decisions made with full rationale, alternatives considered, and why they were rejected
- `entities`: Components, files, services, APIs involved (enables graph-based retrieval)

**Writing comprehensive context:**

BAD (too sparse):
> "Debugging auth bug"

STILL BAD (single sentence):
> "Debugging authentication failure in the login flow where users were getting 401 errors."

GOOD (comprehensive):
> "Working on the fix/auth-refresh branch to resolve issue #234 where users reported intermittent 401 errors after being logged in for extended periods. The bug was reported by 3 enterprise customers last week and is blocking the v2.1 release. Initial investigation pointed to the token refresh mechanism, specifically a race condition between concurrent API requests. The authentication system uses JWT tokens with 15-minute expiry and a refresh token rotation pattern. This session focused on reproducing the bug locally by simulating high-latency conditions."

**Example transformation:**
```
# User invokes:
/pact-memory save "figured out the auth bug"

# You should construct:
{
    "context": "Working on the fix/auth-refresh branch to resolve issue #234 where users reported intermittent 401 errors after being logged in for extended periods. The bug was reported by 3 enterprise customers last week and is blocking the v2.1 release. Initial investigation pointed to the token refresh mechanism, specifically a race condition between concurrent API requests. The authentication system uses JWT tokens with 15-minute expiry and a refresh token rotation pattern. This session focused on reproducing the bug locally by simulating high-latency conditions and tracing through the token refresh flow.",
    "goal": "Identify and fix the root cause of intermittent authentication failures that occur after extended user sessions, ensuring the fix doesn't introduce performance regressions.",
    "lessons_learned": [
        "The token refresh mechanism had a race condition: when multiple API requests detected an expired token simultaneously, each would trigger its own refresh, causing token rotation conflicts where subsequent requests used invalidated tokens",
        "Adding a mutex/lock around the token refresh operation prevents concurrent refresh attempts - the first request refreshes while others wait and then use the new token",
        "The bug only manifests under high latency conditions (>500ms API response time) because faster responses complete before the token expiry window, making it hard to reproduce in development",
        "Our existing retry logic actually made the problem worse by immediately retrying with the same stale token instead of waiting for the refresh to complete",
        "Integration tests should include latency simulation to catch timing-dependent bugs like this"
    ],
    "decisions": [
        {
            "decision": "Use mutex pattern for token refresh instead of request queuing",
            "rationale": "Simpler implementation with less state to manage. A mutex ensures only one refresh happens at a time while other requests wait. Our concurrency level (typically <10 concurrent requests) doesn't warrant the complexity of a full request queue.",
            "alternatives": ["Request queue with single refresh - more complex, better for high concurrency", "Optimistic token prefetch - would require predicting refresh timing", "Retry with backoff - doesn't solve the root cause, just masks it"]
        }
    ],
    "entities": [
        {"name": "AuthService", "type": "service", "notes": "Central authentication service handling login, logout, and token management"},
        {"name": "TokenManager", "type": "class", "notes": "Manages JWT token lifecycle including refresh logic"},
        {"name": "src/auth/refresh.ts", "type": "file", "notes": "Contains the token refresh implementation where the bug was fixed"}
    ]
}
```

### Search Command
```
/pact-memory search "<query>"
```
Returns semantically similar memories. Use natural language queries.

### List Command
```
/pact-memory list [limit]
```
Shows recent memories (default: 10).

## Best Practices

1. **Save at Phase Completion**: Save memories after completing PACT phases
2. **Include Lessons**: Always capture what worked and what didn't
3. **Document Decisions**: Record rationale and alternatives considered
4. **Link Entities**: Reference components for better graph connectivity
5. **Search Before Acting**: Check for relevant past context before starting work
6. **Write Complete Sentences**: Context should be a full description, not a fragment
7. **Be Specific in Lessons**: "X didn't work because Y" is better than "X didn't work"

## Memory Layers: pact-memory vs Auto-Memory

The PACT framework operates with multiple memory layers. Understanding their
distinct roles prevents duplication and ensures the right tool is used for the
right purpose.

| Layer | Storage | Content | Who Writes | Auto-Loaded |
|-------|---------|---------|------------|-------------|
| **Auto-memory** (MEMORY.md) | `~/.claude/projects/{hash}/memory/` | Free-form session learnings, user preferences, general patterns | Platform (automatic) | Yes (first 200 lines) |
| **pact-memory** (SQLite) | `~/.claude/pact-memory/memory.db` | Structured institutional knowledge: context, goals, decisions, lessons, entities | Agents via this skill | Via Working Memory sync to CLAUDE.md |
| **Agent persistent memory** | `~/.claude/agent-memory/<name>/` | Per-agent domain expertise accumulated across sessions | Individual agents (automatic) | Yes (first 200 lines, per agent) |

**pact-memory's unique value**: Structured fields (context, goal, decisions,
lessons_learned, entities) enable semantic search, graph-enhanced retrieval,
and cross-agent knowledge sharing -- capabilities that auto-memory's free-form
markdown does not provide.

**Coexistence model**: Auto-memory captures broad session context automatically.
pact-memory captures deliberate, structured knowledge at PACT phase boundaries.
The Working Memory section in CLAUDE.md shows the 3 most recent pact-memory
entries, providing structured context that complements auto-memory's general
learnings.

## Integration with PACT

The memory skill integrates with PACT phases:

- **Prepare**: Search for relevant past context before starting
- **Architect**: Record design decisions with rationale
- **Code**: Save lessons learned during implementation
- **Test**: Document test strategies and findings

See `references/memory-patterns.md` for detailed usage patterns.
