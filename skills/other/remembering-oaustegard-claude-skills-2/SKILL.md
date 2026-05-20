---
name: remembering
description: Advanced memory operations reference. Basic patterns (profile loading, simple recall/remember) are in project instructions. Consult this skill for background writes, memory versioning, complex queries, edge cases, session scoping, retention management, type-safe results, proactive memory hints, GitHub access detection, autonomous curation, episodic scoring, and decision traces.
metadata:
  version: 5.4.0
---

# Remembering - Advanced Operations

**Basic patterns are in project instructions.** This skill covers advanced features and edge cases.

For development context, see [references/CLAUDE.md](references/CLAUDE.md).

## Two-Table Architecture

| Table | Purpose | Growth |
|-------|---------|--------|
| `config` | Stable operational state (profile + ops + journal) | Small, mostly static |
| `memories` | Timestamped observations | Unbounded |

Config loads fast at startup. Memories are queried as needed.

## Boot Sequence

Load context at conversation start to maintain continuity across sessions.

```python
from scripts import boot
print(boot())
```

**Performance:** ~150ms (single HTTP request). All queries go directly to Turso.

Boot includes a `# CAPABILITIES` section reporting GitHub access and installed utilities. See [references/advanced-operations.md](references/advanced-operations.md) for details.

## Memory Type System

**Type is required** on all write operations. Valid types:

| Type | Use For | Defaults |
|------|---------|----------|
| `decision` | Explicit choices: prefers X, always/never do Y | conf=0.8 |
| `world` | External facts: tasks, deadlines, project state | |
| `anomaly` | Errors, bugs, unexpected behavior | |
| `experience` | General observations, catch-all | |
| `procedure` | Workflows, step-by-step processes, decision trees | conf=0.9, priority=1 |
| `analysis` | Findings from structured analysis or research | |

```python
from scripts import TYPES  # {'decision', 'world', 'anomaly', 'experience', 'procedure', 'analysis', ...}
```

### Procedural Memories (v4.4.0)

Store reusable workflows and operational patterns as first-class memories:

```python
from scripts import remember

# Store a workflow
id = remember(
    "Deploy workflow: 1) Run tests 2) Build artifacts 3) Push to staging 4) Smoke test 5) Promote to prod",
    "procedure",
    tags=["deployment", "workflow"],
)

# Retrieve workflows
procedures = recall(type="procedure", tags=["deployment"])
```

Procedural memories default to `confidence=0.9` and `priority=1` (important), ensuring they survive age-based pruning. Use tags to categorize by domain and workflow name for targeted retrieval.

## Core Operations

### Remember

```python
from scripts import remember, remember_bg, flush

# Blocking write (default)
id = remember("User prefers dark mode", "decision", tags=["ui"], conf=0.9)

# Background write (non-blocking)
remember("Quick note", "world", sync=False)

# Ensure all background writes complete before conversation ends
flush()
```

**When to use sync=False:** Storing derived insights during active work, when latency matters.
**When to use sync=True (default):** User explicitly requests storage, critical memories, handoffs.

### Recall

```python
from scripts import recall

# FTS5 search with BM25 ranking + Porter stemmer
memories = recall("dark mode")

# Filtered queries
decisions = recall(type="decision", conf=0.85, n=20)
tasks = recall("API", tags=["task"], n=15)
urgent = recall(tags=["task", "urgent"], tag_mode="all", n=10)

# Comprehensive retrieval (v4.1.0)
all_memories = recall(fetch_all=True, n=1000)  # Get all memories without search filtering

# Time-windowed queries (v4.3.0) - since/until with inclusive bounds
recent = recall("API", since="2025-02-01")
jan_memories = recall(since="2025-01-01", until="2025-01-31T23:59:59Z")

# Multi-tag convenience (v4.3.0)
both = recall(tags_all=["correction", "bsky"])    # AND: must have all tags
either = recall(tags_any=["therapy", "self-improvement"])  # OR: any tag matches

# Wildcard patterns are NOT supported - use fetch_all instead
# recall("*", n=1000)  # ❌ Raises ValueError
# recall(fetch_all=True, n=1000)  # ✅ Correct approach
```

Results return as `MemoryResult` objects with attribute and dict access. Common aliases (`m.content` -> `m.summary`, `m.conf` -> `m.confidence`) resolve transparently.

### Decision Alternatives (v4.2.0)

Track rejected alternatives on decision memories to prevent revisiting settled conclusions:

```python
from scripts import remember, get_alternatives

# Store decision with alternatives considered
id = remember(
    "Chose PostgreSQL for the database",
    "decision",
    tags=["architecture", "database"],
    alternatives=[
        {"option": "MongoDB", "rejected": "Schema-less adds complexity for our relational data"},
        {"option": "SQLite", "rejected": "Doesn't support concurrent writes at our scale"},
    ]
)

# Later: retrieve what was considered
alts = get_alternatives(id)
for alt in alts:
    print(f"Rejected {alt['option']}: {alt.get('rejected', 'no reason')}")
```

Alternatives are stored in the `refs` field as a typed object alongside memory ID references. The `alternatives` computed field is automatically extracted on `MemoryResult` objects for decision memories.

### Reference Chain Traversal (v4.3.0)

Follow reference chains to build context graphs around a memory:

```python
from scripts import get_chain

# Follow refs up to 3 levels deep (default)
chain = get_chain("memory-uuid", depth=3)
for m in chain:
    print(f"[depth={m['_chain_depth']}] {m['summary'][:80]}")

# Useful for understanding supersede chains, consolidated memory origins, etc.
```

Handles cycles via visited set. Max depth capped at 10.

### Batch Operations (v4.5.0)

Execute multiple memory operations in a single HTTP round-trip, reducing tool call overhead:

```python
from scripts import recall_batch, remember_batch

# Multiple searches in one call (uses server-side FTS5 with BM25 ranking)
results = recall_batch(["architecture", "turso", "FTS5"], n=5)
for i, result_set in enumerate(results):
    print(f"Query {i}: {len(result_set)} results")

# Multiple stores in one call
ids = remember_batch([
    {"what": "User prefers dark mode", "type": "decision", "tags": ["ui"]},
    {"what": "Project uses React", "type": "world", "tags": ["tech"]},
    {"what": "Found auth bug", "type": "anomaly", "conf": 0.7},
])
```

`recall_batch()` uses server-side FTS5 with composite scoring (BM25 × recency × priority). Falls back to sequential `recall()` calls if server FTS5 is unavailable. `remember_batch()` validates each item independently — per-item errors return `{"error": str}` without blocking other items.

### Forget and Supersede

```python
from scripts import forget, supersede

# Soft delete — supports both full UUIDs and partial ID prefixes (v5.1.0, #244)
forget("memory-uuid")          # Full UUID
forget("d5022772")             # Partial prefix (must be unique)

# Version without losing history (also supports partial IDs)
supersede(original_id, "User now prefers Python 3.12", "decision", conf=0.9)
```

Partial IDs resolve to the unique memory matching the prefix. If the prefix matches zero or multiple memories, a `ValueError` is raised. All ID-based functions (`forget`, `supersede`, `reprioritize`, `strengthen`, `weaken`) support partial IDs.

### Decision Traces (v5.1.0)

Store structured decision traces with standardized format for architectural documentation:

```python
from scripts import decision_trace

id = decision_trace(
    choice="Chose Turso FTS5 over local SQLite cache",
    context="Need to simplify architecture after cache sync bugs",
    rationale="Cache latency savings (~145ms) negligible vs tool overhead (~3-4s). "
              "Eliminating sync eliminates a whole class of bugs.",
    alternatives=[
        {"option": "Keep local cache", "rejected": "Ongoing sync bugs"},
        {"option": "Redis", "rejected": "External dependency, overkill"}
    ],
    tradeoffs="Slightly higher latency per query, network dependency",
    contraindications="If tool call overhead drops below 500ms, reconsider caching",
    tags=["architecture", "turso"]
)
```

Decision traces are automatically tagged `"decision-trace"` and stored at `priority=1`. The structured body captures context, rationale, alternatives, tradeoffs, and contraindications — answering *why* not just *what*.

### Autonomous Curation (v5.1.0)

Analyze memory health and identify consolidation opportunities, stale memories, and duplicates:

```python
from scripts import curate

# Preview curation recommendations (dry run)
report = curate(dry_run=True)
for rec in report["recommendations"]:
    print(rec)

# Auto-apply: consolidate clusters and demote stale memories
report = curate(dry_run=False, stale_days=90, consolidation_threshold=3)
print(f"Actions taken: {report['actions_taken']}")
```

### Episodic Relevance Scoring (v5.1.0)

Boost frequently-accessed memories in search results using access-pattern weighting:

```python
from scripts import recall

# Standard recall (BM25 × recency × priority)
results = recall("architecture decisions")

# Episodic recall (adds access-count boost)
results = recall("architecture decisions", episodic=True)
```

Episodic mode adds `ln(1 + access_count) × 0.2` to the composite score, rewarding memories that have been validated as useful through repeated retrieval.

## Config Table

Key-value store for profile (behavioral), ops (operational), and journal (temporal) settings.

```python
from scripts import config_get, config_set, config_delete, config_list, profile, ops

# Read
config_get("identity")                    # Single key
profile()                                  # All profile entries
ops()                                      # All ops entries
config_list()                              # Everything

# Write
config_set("new-key", "value", "profile")  # Category: 'profile', 'ops', or 'journal'
config_set("bio", "Short bio here", "profile", char_limit=500)  # Enforce max length
config_set("core-rule", "Never modify this", "ops", read_only=True)  # Mark immutable

# Delete
config_delete("old-key")
```

For progressive disclosure, priority-based ordering, and dynamic topic categories, see [references/advanced-operations.md](references/advanced-operations.md).

## Journal System

Temporal awareness via rolling journal entries in config.

```python
from scripts import journal, journal_recent, journal_prune

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

## Background Writes

Use `remember(..., sync=False)` for background writes. **Always call `flush()` before conversation ends** to ensure persistence.

```python
from scripts import remember, flush

remember("Derived insight", "experience", sync=False)
remember("Another note", "world", sync=False)

# Before conversation ends:
flush()  # Blocks until all background writes finish
```

`remember_bg()` still works as deprecated alias for `remember(..., sync=False)`.

## Memory Quality Guidelines

Write complete, searchable summaries that standalone without conversation context:

- **Good**: "User prefers direct answers with code examples over lengthy conceptual explanations"
- **Bad**: "User wants code" (lacks context, unsearchable)
- **Bad**: "User asked question" + "gave code" + "seemed happy" (fragmented)

## Edge Cases

- **Empty recall results:** Returns `MemoryResultList([])`, not an error
- **Tag partial matching:** `tags=["task"]` matches memories with tags `["task", "urgent"]`
- **Confidence defaults:** `decision` type defaults to 0.8 if not specified
- **Invalid type:** Raises `ValueError` with list of valid types
- **Tag mode:** `tag_mode="all"` requires all tags present; `tag_mode="any"` (default) matches any
- **Query expansion:** When FTS5 returns fewer than `expansion_threshold` results (default 3), tags from partial matches find related memories. Set `expansion_threshold=0` to disable.

## Implementation Notes

- Backend: Turso SQLite HTTP API (all queries go directly to Turso)
- Credential auto-detection (v3.8.0): Scans env vars, then `/mnt/project/turso.env`, `/mnt/project/muninn.env`, `~/.muninn/.env`
- FTS5 search: Server-side FTS5 with Porter stemmer tokenizer, BM25 × recency × priority composite scoring (tags weighted equally with summary since v5.1.0)
- Retry with exponential backoff for transient errors (503, 429, SSL)
- Thread-safe for background writes
- Repo defaults fallback: `scripts/defaults/` used when Turso is unavailable

## Session Continuity (v4.3.0)

Save and resume session state for cross-session persistence:

```python
from scripts import session_save, session_resume, sessions

# Save a checkpoint before ending session
session_save("Implementing FTS5 search", context={"files": ["cache.py"], "status": "in-progress"})

# In a new session: resume from last checkpoint
checkpoint = session_resume("previous-session-id")
print(checkpoint['summary'])      # What was happening
print(checkpoint['context'])      # Custom context data
print(len(checkpoint['recent_memories']))  # Recent memories from that session

# List available session checkpoints
for s in sessions():
    print(f"{s['session_id']}: {s['summary'][:60]}")
```

## Memory Consolidation (v4.2.0)

Automatically cluster related memories and synthesize summaries, reducing retrieval noise while preserving traceability:

```python
from scripts import consolidate

# Preview what would be consolidated
result = consolidate(dry_run=True)
for c in result['clusters']:
    print(f"Tag '{c['tag']}': {c['count']} memories")

# Actually consolidate (creates summaries, demotes originals to background)
result = consolidate(dry_run=False, min_cluster=3)
print(f"Consolidated {result['consolidated']} clusters, demoted {result['demoted']} memories")

# Scope to specific tags
result = consolidate(tags=["debugging"], dry_run=False)
```

How it works:
1. **Clustering**: Groups memories by shared tags (minimum `min_cluster` memories per group)
2. **Synthesis**: Creates a `type=world` summary memory tagged `consolidated` containing all originals
3. **Archival**: Demotes original memories to `priority=-1` (background)
4. **Traceability**: Summary's `refs` field lists all original memory IDs

## Cross-Episodic Reflection (v4.4.0)

Phase 1.5 of the therapy workflow: systematically convert clusters of similar experiences into generalized semantic knowledge.

```python
from scripts import therapy_reflect

# Preview discovered patterns without creating memories
result = therapy_reflect(dry_run=True)
for c in result['clusters']:
    print(f"Pattern ({len(c['source_ids'])} episodes): {c['pattern'][:80]}")
    print(f"  Common tags: {c['tags']}")

# Create semantic memories from patterns
result = therapy_reflect(dry_run=False)
print(f"Created {result['created']} pattern memories from {len(result['clusters'])} clusters")
```

How it works:
1. **Sampling**: Retrieves recent episodic memories (`type=experience`)
2. **Similarity search**: For each experience, finds similar past episodes via `recall()`
3. **Clustering**: Groups 3+ similar experiences into pattern clusters
4. **Extraction**: Creates `type=world` semantic memories tagged `reflection` + `cross-episodic`
5. **Traceability**: Each pattern memory's `refs` field lists all source episode IDs

Integrates into the existing therapy workflow between pruning and synthesis phases.

## Task Discipline (v5.3.0, #332)

Structural enforcement for multi-step work. Prevents premature completion.

```python
from scripts.task import task, task_resume, incomplete_tasks, recall_gate

# Create task with type-specific checklist
t = task("Analyze bluesky trends", task_type="analysis")
# Steps auto-loaded: recall → synthesize → verify → store

# Mark steps complete
t.done("recall").done("synthesize").done("verify")

# Prefix incomplete output with warning
output = t.incomplete_prefix("My analysis...")
# → "INCOMPLETE: [store not done]\n\nMy analysis..."

# deliver() auto-marks store step
deliver(content, "analysis", tags=["trends"], task=t)

# complete() raises with structured report if steps remain
print(t.complete())
# → "✓ Task 'Analyze bluesky trends' complete (12.3s)\n  Type: analysis\n  Verified:..."

# Cross-session continuity — tasks persist in Turso
t = task_resume("Analyze bluesky trends")  # → Task object or None

# Boot surfaces incomplete tasks automatically
# → # INCOMPLETE TASKS (1)\n⚠️  Resume these before starting new work:...

# recall_gate: enforce recall() before analysis
with recall_gate("bluesky zeitgeist") as gate:
    results = gate.recall("bluesky trends", n=10)
    # ... analyze results
# Raises if recall not called or returns empty
```

Task types and their checklists:

| Type | Steps |
|------|-------|
| `analysis` | recall → synthesize → verify → store |
| `research` | recall → search → read → synthesize → store |
| `synthesis` | recall → outline → write → verify → store |
| `zeitgeist` | recall → sample → cluster → summarize → store |

## Advanced Topics

For architecture details, see [_ARCH.md](_ARCH.md).

See [references/advanced-operations.md](references/advanced-operations.md) for:

- Date-filtered queries (`recall_since`, `recall_between`, `since`/`until` parameters)
- Priority system and memory consolidation (`strengthen`, `weaken`)
- Therapy helpers, cross-episodic reflection, and analysis helpers
- Handoff convention (cross-environment coordination)
- Session scoping and continuity (`session_save`, `session_resume`, `sessions`)
- Retrieval observability and retention management
- Export/import for portability
- Type-safe results (MemoryResult) details
- Proactive memory hints (`recall_hints`)
- GitHub access detection and unified API
- Progressive disclosure and priority-based ordering
- Decision alternatives (`get_alternatives`) and memory consolidation (`consolidate`)
- Reference chain traversal (`get_chain`)
- Batch APIs (`recall_batch`, `remember_batch`) for reducing HTTP round-trips
- Autonomous curation (`curate`) for memory health management
- Decision traces (`decision_trace`) for structured architectural documentation
- Episodic relevance scoring (`episodic=True` in `recall`) for access-pattern boosting
- Task discipline (`task`, `task_resume`, `incomplete_tasks`, `recall_gate`) for structural enforcement
