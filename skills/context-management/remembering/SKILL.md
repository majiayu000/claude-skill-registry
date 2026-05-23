---
name: remembering
description: Advanced memory operations reference. Basic patterns (profile loading, simple recall/remember) are in project instructions. Consult this skill for background writes, memory versioning, complex queries, edge cases, session scoping, and retention management.
metadata:
  version: 3.3.0
---

> **⚠️ IMPORTANT FOR CLAUDE CODE AGENTS**
> Before working with this skill, read `CLAUDE.md` in this directory.
> It contains critical development context, import patterns, and instructs you to use Muninn to track work on Muninn (meta-usage pattern).

# Remembering - Advanced Operations

**Basic patterns are in project instructions.** This skill covers advanced features and edge cases.

## Two-Table Architecture

| Table | Purpose | Growth |
|-------|---------|--------|
| `config` | Stable operational state (profile + ops + journal) | Small, mostly static |
| `memories` | Timestamped observations | Unbounded |

Config loads fast at startup. Memories are queried as needed.

## Boot Sequence

Load context at conversation start to maintain continuity across sessions.

### Optimized: Compressed Boot (Recommended)

Use `boot()` for fast startup (~150ms):

```python
from remembering import boot
print(boot())
```

Output: Complete profile and ops values for full context at boot.

**Performance:**
- Execution: ~150ms (single HTTP request)
- Populates local cache for fast subsequent recall()

## Journal System

Temporal awareness via rolling journal entries in config. Inspired by Strix's journal.jsonl pattern.

```python
from remembering import journal, journal_recent, journal_prune

# Record what happened this interaction
journal(
    topics=["project-x", "debugging"],
    user_stated="Will review PR tomorrow",
    my_intent="Investigating memory leak"
)

# Boot: load recent entries for context
for entry in journal_recent(10):
    print(f"[{entry['t'][:10]}] {entry.get('topics', [])}: {entry.get('my_intent', '')}")

# Maintenance: keep last 40 entries
pruned = journal_prune(keep=40)
```

**Entry structure:**
- `t`: ISO timestamp
- `topics`: array of tags (enables filtering at scale)
- `user_stated`: commitments/plans user verbalized
- `my_intent`: current goal/task

**Key insight from Strix:** "If you didn't write it down, you won't remember it next message."

## Config Table

Key-value store for profile (behavioral), ops (operational), and journal (temporal) settings.

```python
from remembering import config_get, config_set, config_delete, config_list, config_set_boot_load, profile, ops

# Read
config_get("identity")                    # Single key
profile()                                  # All profile entries
ops()                                      # All ops entries
config_list()                              # Everything

# Write
config_set("new-key", "value", "profile")  # Category: 'profile', 'ops', or 'journal'
config_set("skill-foo", "usage notes", "ops")

# Write with constraints (new!)
config_set("bio", "Short bio here", "profile", char_limit=500)  # Enforce max length
config_set("core-rule", "Never modify this", "ops", read_only=True)  # Mark immutable

# Delete
config_delete("old-key")
```

**Config constraints:**
- `char_limit`: Enforces maximum character count on writes (raises `ValueError` if exceeded)
- `read_only`: Prevents modifications (raises `ValueError` on attempted updates)

### Progressive Disclosure (v2.1.0)

Ops entries can be marked as **boot-loaded** (default) or **reference-only** to reduce boot() output size:

```python
from remembering import config_set_boot_load, ops

# Mark entry as reference-only (won't load at boot)
config_set_boot_load('github-api-endpoints', False)
config_set_boot_load('container-limits', False)

# Mark entry as boot-loaded (loads at boot)
config_set_boot_load('storage-discipline', True)

# Query ops with filtering
boot_ops = ops()                          # Only boot-loaded entries (default)
all_ops = ops(include_reference=True)     # All entries (boot + reference)
```

**How it works:**
- `boot()` outputs only ops with `boot_load=1` (reduces token usage at boot)
- Reference-only ops (`boot_load=0`) appear in a **Reference Entries** index at the end of boot output
- Reference entries remain fully accessible via `config_get(key)` when needed
- Ideal for: API documentation, container specs, rarely-triggered guidance

**Example boot output:**
```
=== OPS ===

## Core Boot & Behavior
storage-discipline:
[Full content here...]

## Reference Entries (load via config_get)
container-limits, github-api-endpoints, network-tools, recall-triggers
```

## Memory Type System

**Type is required** on all write operations. Valid types:

| Type | Use For |
|------|---------|
| `decision` | Explicit choices: prefers X, always/never do Y |
| `world` | External facts: tasks, deadlines, project state |
| `anomaly` | Errors, bugs, unexpected behavior |
| `experience` | General observations, catch-all |

Note: `profile` is no longer a memory type—use `config_set(key, value, "profile")` instead.

```python
from remembering import TYPES  # {'decision', 'world', 'anomaly', 'experience'}
```

## Priority System (v2.0.0)

Memories have a priority field that affects ranking in search results:

| Priority | Value | Description |
|----------|-------|-------------|
| Background | -1 | Low-value, can age out first |
| Normal | 0 | Default for new memories |
| Important | 1 | Boosted in ranking |
| Critical | 2 | Always surface, never auto-age |

```python
from remembering import remember, reprioritize

# Set priority at creation
remember("Critical security finding", "anomaly", tags=["security"], priority=2)

# Adjust priority later
reprioritize("memory-uuid", priority=1)  # Upgrade to important
reprioritize("memory-uuid", priority=-1)  # Demote to background
```

**Ranking formula:**
```
score = bm25_score * recency_weight * (1 + priority * 0.5)
```

Priority affects composite ranking score - higher priority memories surface more readily in search results.

### Memory Consolidation (v3.3.0)

Biological memory consolidation pattern: memories that participate in active cognition consolidate more strongly.

```python
from remembering import strengthen, weaken, recall

# Strengthen a memory (increment priority, max 2)
result = strengthen("memory-uuid", boost=1)
# Returns: {'memory_id': '...', 'old_priority': 0, 'new_priority': 1, 'changed': True}

# Weaken a memory (decrement priority, min -1)
result = weaken("memory-uuid", drop=1)
# Returns: {'memory_id': '...', 'old_priority': 1, 'new_priority': 0, 'changed': True}

# Auto-strengthen top results during recall (opt-in)
results = recall("important topic", auto_strengthen=True, n=10)
# Automatically strengthens top 3 results with priority < 2
```

**Use cases:**
- Consolidate memories that prove useful across conversations
- Implement spaced repetition patterns
- Automatically promote frequently accessed knowledge
- Simulate biological memory consolidation mechanisms

**Notes:**
- `strengthen()` caps at priority=2 (critical)
- `weaken()` floors at priority=-1 (background)
- `auto_strengthen=True` only affects top 3 results with priority < 2
- Returns dict with old/new priority and whether change occurred
- Replaced no-op placeholder functions from v2.0.0 with working implementations

## Background Writes (Agentic Pattern)

**v0.6.0:** Unified API with `sync` parameter. Use `remember(..., sync=False)` for background writes:

```python
from remembering import remember, flush

# Background writes (non-blocking, returns immediately)
remember("User's project uses Python 3.12 with FastAPI", "world", sync=False)
remember("Discovered: batch insert reduces latency 70%", "experience",
         tags=["optimization"], sync=False)

# Ensure all pending writes complete before conversation end
flush()  # Blocks until all background writes finish
```

**Backwards compatibility:** `remember_bg()` still works (deprecated, calls `remember(..., sync=False)`):

```python
from remembering import remember_bg
remember_bg("Quick note", "world")  # Same as remember(..., sync=False)
```

**When to use sync=False (background):**
- Storing derived insights during active work
- Memory write shouldn't block response
- Agentic pattern where latency matters

**When to use sync=True (blocking, default):**
- User explicitly requests storage
- Need confirmation of write success
- Critical memories (handoffs, decisions)
- End of workflow when durability matters

**⚠️ IMPORTANT - Cache Sync Guarantee:**
- If you use `sync=False` for ANY writes in a conversation, you MUST call `flush()` before the conversation ends
- This ensures all background writes persist to the database before the ephemeral container is destroyed
- Single-user context: no concurrent write conflicts, all writes will succeed
- Prefer `sync=True` (default) for critical writes to guarantee immediate persistence

## Memory Versioning (Patch/Snapshot)

Supersede without losing history:

```python
from remembering import supersede

# User's preference evolved
original_id = "abc-123"
supersede(original_id, "User now prefers Python 3.12", "decision", conf=0.9)
```

Creates new memory with `refs=[original_id]`. Original preserved but not returned in default queries. Trace evolution via `refs` chain.

**v3.3.0 Performance:** `supersede()` now uses batched operations, reducing HTTP requests by 50% (single request instead of two).

## Complex Queries

Multiple filters, custom confidence thresholds:

```python
from remembering import recall

# High-confidence decisions only
decisions = recall(type="decision", conf=0.85, n=20)

# Recent anomalies for debugging context
bugs = recall(type="anomaly", n=5)

# Search with tag filter (any match)
tasks = recall("API", tags=["task"], n=15)

# Require ALL tags (tag_mode="all")
urgent_tasks = recall(tags=["task", "urgent"], tag_mode="all", n=10)
```

## Date-Filtered Queries

Query memories by temporal range:

```python
from remembering import recall_since, recall_between

# Get memories after a specific timestamp
recent = recall_since("2025-12-01T00:00:00Z", n=50)
recent_bugs = recall_since("2025-12-20T00:00:00Z", type="anomaly", tags=["critical"])

# Get memories within a time range
december = recall_between("2025-12-01T00:00:00Z", "2025-12-31T23:59:59Z", n=100)
sprint_mems = recall_between("2025-12-15T00:00:00Z", "2025-12-22T00:00:00Z",
                             type="decision", tags=["sprint-5"])
```

**Use cases:**
- Review decisions made during a project phase
- Analyze bugs discovered in a time window
- Track learning progress over specific periods
- Build time-based memory summaries

**Notes:**
- Timestamps are exclusive (use `>` and `<` not `>=` and `<=`)
- Supports all standard filters: `search`, `type`, `tags`, `tag_mode`
- Sorted by timestamp descending (newest first)
- Excludes soft-deleted and superseded memories

## Therapy Helpers

Support for reflection and memory consolidation workflows:

```python
from remembering import therapy_scope, therapy_session_count

# Get unprocessed memories since last therapy session
cutoff_time, unprocessed_memories = therapy_scope()
# cutoff_time: timestamp of last therapy session (or None if no sessions)
# unprocessed_memories: all memories created after that timestamp

# Count how many therapy sessions have been recorded
count = therapy_session_count()
```

**Therapy session workflow:**
1. Call `therapy_scope()` to get unprocessed memories
2. Analyze and consolidate memories (group patterns, extract insights)
3. Record therapy session completion:
   ```python
   remember(f"Therapy Session #{count+1}: Consolidated {len(unprocessed)} memories...",
            "experience", tags=["therapy"])
   ```

**Pattern detection example:**
```python
cutoff, mems = therapy_scope()
by_type = group_by_type(mems)  # See Analysis Helpers below

print(f"Since {cutoff}:")
print(f"  {len(by_type.get('decision', []))} decisions")
print(f"  {len(by_type.get('anomaly', []))} anomalies to investigate")
```

## Analysis Helpers

Group and organize memories for pattern detection:

```python
from remembering import group_by_type, group_by_tag

# Get memories and group by type
memories = recall(n=100)
by_type = group_by_type(memories)
# Returns: {"decision": [...], "world": [...], "anomaly": [...], "experience": [...]}

# Group by tags
by_tag = group_by_tag(memories)
# Returns: {"ui": [...], "bug": [...], "performance": [...], ...}
# Note: Memories with multiple tags appear under each tag
```

**Use cases:**
- **Pattern detection**: Find clusters of related memories
- **Quality analysis**: Identify over/under-represented memory types
- **Tag hygiene**: Discover inconsistent tagging patterns
- **Therapy sessions**: Organize unprocessed memories before consolidation

**Example - Find overused tags:**
```python
mems = recall(n=200)
by_tag = group_by_tag(mems)
sorted_tags = sorted(by_tag.items(), key=lambda x: len(x[1]), reverse=True)
print("Top tags:")
for tag, tagged_mems in sorted_tags[:5]:
    print(f"  {tag}: {len(tagged_mems)} memories")
```

## FTS5 Search with Porter Stemmer (v0.13.0)

Full-text search uses FTS5 with Porter stemmer for morphological variant matching:

```python
from remembering import recall

# Searches match word variants automatically
# "running" matches "run", "runs", "runner"
# "beads" matches "bead"
results = recall("running performance")

# Query expansion fallback
# When FTS5 returns < 3 results, automatically extracts tags from
# partial results and searches for related memories
sparse_results = recall("rare term")  # Auto-expands if < 3 matches
```

**How it works:**
- FTS5 tokenizer: `porter unicode61` handles stemming
- BM25 ranking for relevance scoring
- Query expansion extracts tags from partial results when < 3 matches found
- Composite ranking: BM25 × salience × recency × access patterns

## Soft Delete

Remove without destroying data:

```python
from remembering import forget

forget("memory-uuid")  # Sets deleted_at, excluded from queries
```

Memories remain in database for audit/recovery. Hard deletes require direct SQL.

## Memory Quality Guidelines

Write complete, searchable summaries that standalone without conversation context:

✓ "User prefers direct answers with code examples over lengthy conceptual explanations"

✗ "User wants code" (lacks context, unsearchable)

✗ "User asked question" + "gave code" + "seemed happy" (fragmented, no synthesis)

## Handoff Convention

Cross-environment work coordination with version tracking and automatic completion marking.

### Creating Handoffs

From Claude.ai (web/mobile) - cannot persist file changes:

```python
from remembering import remember

remember("""
HANDOFF: Implement user authentication

## Context
User wants OAuth2 + JWT authentication for the API.

## Files to Modify
- src/auth/oauth.py
- src/middleware/auth.py
- tests/test_auth.py

## Implementation Notes
- Use FastAPI OAuth2PasswordBearer
- JWT tokens with 24h expiry
- Refresh token support
...
""", "world", tags=["handoff", "pending", "auth"])
```

**Important:** Tag with `["handoff", "pending", ...]` so it appears in `handoff_pending()` queries.

**Handoff structure:**
- **Title**: Brief summary of what needs to be done
- **Context**: Why this work is needed
- **Files to Modify**: Specific paths
- **Implementation Notes**: Code patterns, constraints, dependencies

### Completing Handoffs

From Claude Code - streamlined workflow:

```python
from remembering import handoff_pending, handoff_complete

# Get pending work (excludes completed handoffs)
pending = handoff_pending()
print(f"{len(pending)} pending handoff(s)")

for h in pending:
    print(f"[{h['created_at'][:10]}] {h['summary'][:80]}")

# Complete a handoff (automatically tags with version)
handoff_id = pending[0]['id']
handoff_complete(
    handoff_id,
    "COMPLETED: Implemented boot() function with batched queries...",
    # version auto-detected from VERSION file, or specify: "0.5.0"
)
```

**What happens:**
- Original handoff is superseded (won't appear in future `handoff_pending()` queries)
- Completion record created with tags `["handoff-completed", "v0.5.0"]`
- Version tracked automatically from `VERSION` file
- Full history preserved via `supersede()` chain

### Querying History

```python
from remembering import recall

# See what was completed in a specific version
v050_work = recall(tags=["handoff-completed", "v0.5.0"])

# See all completion records
completed = recall(tags=["handoff-completed"], n=50)
```

**Use when:**
- Working in Claude.ai (web/mobile) without file write access
- Planning work that needs Claude Code execution
- Coordinating between environments
- Leaving detailed instructions for future sessions

## Session Scoping (v3.2.0)

Filter memories by conversation or work session using `session_id`:

```python
from remembering import remember, recall, set_session_id

# Set session for all subsequent remember() calls
set_session_id("project-alpha-sprint-1")
remember("Feature spec approved", "decision", tags=["project-alpha"])

# Query by session
alpha_memories = recall(session_id="project-alpha-sprint-1", n=50)

# Session ID defaults to MUNINN_SESSION_ID env var or 'default-session'
import os
os.environ['MUNINN_SESSION_ID'] = 'my-session'
```

**Note**: Session filtering bypasses cache (queries Turso directly). Cache support planned for future release.

## Retrieval Observability (v3.2.0)

Monitor query performance and usage patterns:

```python
from remembering import recall_stats, top_queries

# Get retrieval statistics
stats = recall_stats(limit=100)
print(f"Cache hit rate: {stats['cache_hit_rate']:.1%}")
print(f"Avg query time: {stats['avg_exec_time_ms']:.1f}ms")

# Find most common searches
for query_info in top_queries(n=10):
    print(f"{query_info['query']}: {query_info['count']} times")
```

## Retention Management (v3.2.0)

Analyze memory distribution and prune old/low-priority memories:

```python
from remembering import memory_histogram, prune_by_age, prune_by_priority

# Get memory distribution
hist = memory_histogram()
print(f"Total: {hist['total']}")
print(f"By type: {hist['by_type']}")
print(f"By priority: {hist['by_priority']}")
print(f"By age: {hist['by_age_days']}")

# Preview what would be deleted (dry run)
result = prune_by_age(older_than_days=90, priority_floor=0, dry_run=True)
print(f"Would delete {result['count']} memories")

# Actually delete old low-priority memories
result = prune_by_age(older_than_days=90, priority_floor=0, dry_run=False)

# Delete all background-priority memories
result = prune_by_priority(max_priority=-1, dry_run=False)
```

## Export/Import for Portability

Backup or migrate Muninn state across environments:

```python
from remembering import muninn_export, muninn_import
import json

# Export all state to JSON
state = muninn_export()
# Returns: {"version": "1.0", "exported_at": "...", "config": [...], "memories": [...]}

# Save to file
with open("muninn-backup.json", "w") as f:
    json.dump(state, f, indent=2)

# Import (merge with existing data)
with open("muninn-backup.json") as f:
    data = json.load(f)
stats = muninn_import(data, merge=True)
print(f"Imported {stats['config_count']} config, {stats['memory_count']} memories")

# Import (replace all - destructive!)
stats = muninn_import(data, merge=False)
```

**Notes:**
- `merge=False` deletes all existing data before import (use with caution!)
- Memory IDs are regenerated on import to avoid conflicts
- Returns stats dict with counts and any errors

## Edge Cases

**Empty recall results:** Returns `[]`, not an error. Check list length before accessing.

**Search literal matching:** Current implementation uses SQL LIKE. Searches "API test" matches "API testing" but not "test API" (order matters).

**Tag partial matching:** `tags=["task"]` matches memories with tags `["task", "urgent"]` via JSON substring search.

**Confidence defaults:** `decision` type defaults to 0.8 if not specified. Others default to `NULL`.

**Invalid type:** Raises `ValueError` with list of valid types.

**Invalid category:** `config_set` raises `ValueError` if category not 'profile', 'ops', or 'journal'.

**Journal pruning:** Call `journal_prune()` periodically to prevent unbounded growth. Default keeps 40 entries.

**Tag mode:** `tag_mode="all"` requires all specified tags to be present. `tag_mode="any"` (default) matches if any tag present.

**Query expansion:** When FTS5 returns < 3 results, tags are automatically extracted from partial matches and used to find related memories.

## Implementation Notes

- Backend: Turso SQLite HTTP API
- URL: `TURSO_URL` environment variable or `/mnt/project/muninn.env`, falls back to default
- Token: `TURSO_TOKEN` environment variable, `/mnt/project/muninn.env`, or `/mnt/project/turso-token.txt`
- Two tables: `config` (KV) and `memories` (observations)
- FTS5 search: Porter stemmer tokenizer with BM25 ranking
- HTTP API required (libsql SDK bypasses egress proxy)
- Local SQLite cache for fast recall (< 5ms vs 150ms+ network)
- Thread-safe for background writes
