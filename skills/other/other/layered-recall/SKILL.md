---
name: layered-recall
description: "Progressive memory recall with 4 scope layers AND 3 depth layers. Scope: identity > project > room > deep. Depth: IDs only > summary > full. 10-50x token savings through fetch-on-confirmation pattern."
---

# Layered Recall

Progressive memory system with **two orthogonal dimensions** of lazy loading:
1. **Scope layers** - What is relevant (identity, project, domain, deep)
2. **Depth layers** - How much detail to fetch (IDs, summary, full)

Combined savings: 10-50x tokens vs eager loading.

## Depth Pattern (Fetch-on-Confirmation)

Instead of loading full memory entries upfront, agents fetch in 3 depths:

```
Depth 1: IDs only        (~10 tokens per match)
  Agent decides which are worth investigating

Depth 2: Summary         (~50 tokens per match)
  Room, type, preview (first 80 chars)
  Agent confirms relevance

Depth 3: Full content    (~500+ tokens per match)
  Only fetched for confirmed matches
```

**Example flow:**
```
1. Agent searches "auth refresh token"
2. Depth 1 returns 8 IDs: d-abc123, d-def456, ...
3. Agent requests Depth 2 for IDs 1-3
4. Sees room=authentication, type=decision, preview="Chose JWT..."
5. Agent confirms IDs 1,3 are relevant
6. Requests Depth 3 only for those 2 entries
7. Gets full content for ~1000 tokens instead of 4000+
```

## The 4 Layers

```
Layer 1: Identity (always loaded, ~200 tokens)
   Who is the user? What are their preferences?

Layer 2: Critical Facts (per-project, ~500 tokens)
   Hard constraints, active decisions, blockers

Layer 3: Room Recall (on-demand, ~1-2K tokens)
   Relevant memories for current task domain

Layer 4: Deep Search (when needed, ~2-5K tokens)
   Full semantic search across all memories
```

## Layer Details

### Layer 1: Identity (~200 tokens, ALWAYS loaded)

Loaded at every session start. Contains:
- User preferences (language, style, autonomy level)
- Global constraints (no emojis, Turkish responses, etc.)
- Tool preferences (which editors, which terminal)

**Source:** `~/.claude/projects/*/memory/user_*.md`

### Layer 2: Critical Facts (~500 tokens, per-project)

Loaded when entering a project directory. Contains:
- Active architectural decisions
- Known blockers and constraints
- Current sprint/milestone goals
- Tech stack and versions

**Source:** `~/.claude/projects/*/memory/project_*.md` + `thoughts/CONTEXT.md`

### Layer 3: Room Recall (~1-2K tokens, on-demand)

Loaded when task domain is detected (auth, database, deploy, etc.). Contains:
- Previous decisions in this domain
- Past errors and fixes
- Patterns that worked
- Patterns that failed

**Source:** Memory palace rooms + `mature-instincts.json` filtered by domain

**Trigger:** Intent classifier detects domain (e.g., "fix the login bug" -> room: authentication)

### Layer 4: Deep Search (~2-5K tokens, explicit)

Only loaded when explicitly needed or when Layers 1-3 don't have enough context. Contains:
- Full semantic search results
- Cross-project pattern matches
- Historical error resolutions
- Archived decisions

**Source:** PostgreSQL vector search + palace cross-wing search

**Trigger:** Agent explicitly queries, or user asks "have we done this before?"

## Recall Flow

```
Session Start
  -> Load Layer 1 (identity)
  -> Detect project -> Load Layer 2 (facts)
  -> User sends prompt
  -> Classify intent/domain -> Load Layer 3 (room)
  -> If insufficient context -> Load Layer 4 (deep)
```

## Token Budget

| Layer | Tokens | When |
|-------|--------|------|
| L1 | ~200 | Always |
| L2 | ~500 | Per project |
| L3 | ~1-2K | Per task domain |
| L4 | ~2-5K | On demand |
| **Total max** | **~8K** | Worst case |

vs. loading everything: ~30-50K tokens

**Savings: 4-6x token reduction**

## Integration

### With Existing Hooks
- `instinct-loader` -> feeds Layer 2 and Layer 3
- `smart-memory-recall` -> implements Layer 3 scoring
- `intent-classifier` -> triggers Layer 3 room selection
- `graph-indexer` -> powers Layer 4 deep search

### With Memory Palace
- Layer 2 pulls from palace wing index
- Layer 3 pulls from palace room drawers
- Layer 4 searches across all wings

### With Agents
- Agents inherit parent's Layer 1-2 context
- Each agent can request Layer 3-4 for their domain
- Agent memories feed back into palace for future recall
