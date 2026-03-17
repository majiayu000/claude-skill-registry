---
name: daem0nmcp-protocol
description: Use when Daem0nMCP tools are available - enforces the sacred covenant (commune at session start, seek counsel before changes, inscribe decisions, seal outcomes)
---

# The Daem0n's Protocol

## Overview

When Daem0nMCP memory tools are available, you MUST follow this protocol. Memory without discipline is noise.

**Core principle:** Check before you change, record what you decide, track whether it worked.

## Tool Detection

First, verify Daem0nMCP tools are available:

```
Look for these 8 workflow tools in your available tools:
- mcp__daem0nmcp__commune      (session start & status)
- mcp__daem0nmcp__consult      (pre-action intelligence)
- mcp__daem0nmcp__inscribe     (memory writing & linking)
- mcp__daem0nmcp__reflect      (outcomes & verification)
- mcp__daem0nmcp__understand   (code comprehension)
- mcp__daem0nmcp__govern       (rules & triggers)
- mcp__daem0nmcp__explore      (graph & discovery)
- mcp__daem0nmcp__maintain     (housekeeping & federation)
```

**If tools are NOT available:** This skill does not apply. Proceed normally.

**If tools ARE available:** Follow the protocol below. No exceptions.

## The Protocol

### 1. SESSION START (Non-Negotiable)

```
IMMEDIATELY when you have daem0nmcp tools:

mcp__daem0nmcp__commune(action="briefing")

DO NOT:
- Ask user what they want first
- Skip briefing because "it's a quick task"
- Assume you remember from last session
```

The briefing loads:
- Past decisions and their outcomes
- Warnings and failed approaches to AVOID
- Patterns to FOLLOW
- Git changes since last session

### 2. BEFORE ANY CODE CHANGES

```
BEFORE touching any file:

mcp__daem0nmcp__consult(action="preflight", description="what you're about to do")

OR for specific files:

mcp__daem0nmcp__consult(action="recall_file", file_path="path/to/file")
```

**If preflight returns:**
- **WARNING:** You MUST acknowledge it to the user
- **FAILED APPROACH:** Explain how your approach differs
- **must_not:** These are HARD CONSTRAINTS - do not violate

### 3. AFTER MAKING DECISIONS

```
AFTER every significant decision:

memory_result = mcp__daem0nmcp__inscribe(
    action="remember",
    category="decision",  # or "pattern", "warning", "learning"
    content="What you decided",
    rationale="Why you decided it",
    file_path="relevant/file.py",  # optional
    tags=["relevant", "tags"]
)

SAVE THE MEMORY ID - you need it for reflect(action="outcome")
```

**Category Guide:**
| Category | Use For | Persistence |
|----------|---------|-------------|
| decision | Architectural/design choices | Decays over 30 days |
| pattern | Recurring approaches to follow | PERMANENT |
| warning | Things to avoid | PERMANENT |
| learning | Lessons from experience | Decays over 30 days |

### 4. AFTER IMPLEMENTATION (Critical)

```
AFTER implementing and testing:

mcp__daem0nmcp__reflect(
    action="outcome",
    memory_id=<id from inscribe>,
    outcome_text="What actually happened",
    worked=true  # or false
)
```

**FAILURES ARE VALUABLE.** If something doesn't work:
- Record `worked=false` with explanation
- Failed approaches get 1.5x boost in future searches
- You WILL see past mistakes - that's the point

## Red Flags - STOP

- About to edit a file without calling `consult(action="recall_file")`
- Making a significant decision without calling `inscribe(action="remember")`
- Implementation complete but no `reflect(action="outcome")` called
- Preflight returned WARNING but you didn't acknowledge it
- Repeating an approach that previously failed

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "It's a small change" | Small changes compound into big problems |
| "I'll remember later" | You won't. Record now. |
| "Context check is overkill" | 5 seconds now vs hours debugging later |
| "The warning doesn't apply" | Warnings exist because someone failed before |
| "I don't need to record failures" | Failures are the most valuable memories |

## Enforcement (2026 Update)

The Sacred Covenant is now ENFORCED, not advisory:

### What Happens If You Skip Steps

1. **Skip `commune(action="briefing")`**: ALL tools return `COMMUNION_REQUIRED` block
2. **Skip `consult(action="preflight")`**: Mutating tools return `COUNSEL_REQUIRED` block
3. **Each block includes a `remedy`**: The exact tool call to fix it

### Enforcement

Workflow actions are classified:
- **Requires counsel**: `inscribe(action="remember")`, `inscribe(action="remember_batch")`, `govern(action="add_rule")`, `govern(action="update_rule")`, `maintain(action="prune")`, `maintain(action="cleanup")`, `maintain(action="compact")`, `maintain(action="export")`, `maintain(action="import_data")`, `inscribe(action="ingest")`
- **Requires communion**: All other actions except briefing and health
- **Exempt**: `commune(action="briefing")`, `commune(action="health")`

### Preflight Token

After `consult(action="preflight")`, you receive a `preflight_token` in the response.
This is cryptographic proof you consulted the Daem0n.
Token is valid for 5 minutes.

### Parallel Preflight

Before file edits, run these IN PARALLEL for maximum efficiency:
- `consult(action="preflight")` + `consult(action="recall_file")` + `understand(action="impact")`

## Workflow Summary

```
SESSION START
    └─> commune(action="briefing")

BEFORE CHANGES
    └─> consult(action="preflight", description="what you're doing")
    └─> consult(action="recall_file", file_path="path") for specific files
    └─> ACKNOWLEDGE any warnings

AFTER DECISIONS
    └─> inscribe(action="remember", category=..., content=..., rationale=...)
    └─> SAVE the memory_id
    └─> inscribe(action="link") if causally related to other decisions

AFTER IMPLEMENTATION
    └─> reflect(action="outcome", memory_id=..., outcome_text=..., worked=...)

INVESTIGATING CONTEXT
    └─> explore(action="chain") to understand decision history
    └─> explore(action="graph") to visualize relationships
```

## Why This Matters

Without protocol discipline:
- You repeat past mistakes
- Decisions get lost between sessions
- Patterns aren't captured
- Failures aren't learned from
- The memory system becomes useless noise

With protocol discipline:
- Past mistakes surface before you repeat them
- Decisions persist across sessions
- Patterns compound into project knowledge
- Failures become learning opportunities
- The AI actually gets smarter over time

## Graph Memory Tools

Memories can be explicitly linked to create a knowledge graph. Use these when decisions are causally related.

### Relationship Types

| Type | Meaning | Example |
|------|---------|---------|
| `led_to` | A caused/resulted in B | "PostgreSQL choice led to connection pooling pattern" |
| `supersedes` | A replaces B (B is outdated) | "New auth flow supersedes old JWT approach" |
| `depends_on` | A requires B to be valid | "Caching strategy depends on database choice" |
| `conflicts_with` | A contradicts B | "Sync processing conflicts with async pattern" |
| `related_to` | General association | "Both relate to authentication" |

### Link Memories

```
mcp__daem0nmcp__inscribe(
    action="link",
    source_id=<memory_id>,
    target_id=<other_memory_id>,
    relationship="led_to",
    description="Optional context for the link"
)
```

**When to link:**
- A decision directly caused another decision
- A pattern emerged from a specific choice
- An approach supersedes a previous one

### Trace Causal Chains

```
mcp__daem0nmcp__explore(
    action="related",
    memory_id=<id>,
    direction="backward",  # "forward", "backward", or "both"
    max_depth=5
)
```

**Use cases:**
- "What decisions led to this pattern?" → trace backward
- "What emerged from this architectural choice?" → trace forward
- "Show me the full context around this decision" → trace both

### Visualize the Graph

```
mcp__daem0nmcp__explore(
    action="graph",
    memory_ids=[1, 2, 3],  # OR
    topic="authentication",
    format="mermaid"  # or "json"
)
```

Returns a mermaid diagram or JSON structure showing nodes and edges.

### Remove Links

```
mcp__daem0nmcp__inscribe(
    action="unlink",
    source_id=<id>,
    target_id=<id>,
    relationship="led_to"
)
```

## OpenSpec Integration

If the project uses OpenSpec (spec-driven development), the `openspec-daem0n-bridge` skill provides bidirectional integration:

**Auto-detection:** After `get_briefing()`, if `openspec/` directory exists, specs are automatically imported as patterns and rules.

**Before creating proposals:** Use "prepare proposal for [feature]" to query past decisions and failures.

**After archiving changes:** Use "record outcome for [change-id]" to convert completed work to learnings.

See the `openspec-daem0n-bridge` skill for full workflow details.

## Enhanced Search & Indexing (v2.15.0)

### Automatic Tag Inference

Memories now auto-detect tags from content:
- **bugfix**: fix, bug, error, issue, broken, crash
- **tech-debt**: todo, hack, workaround, temporary
- **perf**: cache, performance, slow, fast, optimize
- **warning**: Added automatically for warning category

You don't need to manually tag common patterns.

### Condensed Mode for Large Projects

For projects with many memories, use condensed recall:

```
mcp__daem0nmcp__consult(action="recall", topic="authentication", condensed=True)
```

Returns compressed output (~75% token reduction):
- Content truncated to 150 chars
- Rationale/context stripped
- Ideal for broad surveys before deep dives

### Code Intelligence Tools

**Index your codebase:**
```
mcp__daem0nmcp__understand(action="index")  # Index all code entities
```

**Search code semantically:**
```
mcp__daem0nmcp__understand(action="find", query="user authentication")
```

**Analyze change impact:**
```
mcp__daem0nmcp__understand(action="impact", entity_name="UserService.authenticate")
```

### Incremental Indexing

Only re-indexes changed files:
- Uses SHA256 content hashes
- Automatically skips unchanged files
- Entities have stable IDs (survive line changes)

### Enhanced Health Monitoring

```
mcp__daem0nmcp__commune(action="health")
```

Now returns:
- `code_entities_count`: Total indexed entities
- `entities_by_type`: Breakdown by class/function
- `last_indexed_at`: When index was last updated
- `index_stale`: True if >24 hours since last index

## The Bottom Line

**Memory tools exist. Use them correctly.**

Check context. Record decisions. Track outcomes. Link related memories.

This is non-negotiable when Daem0nMCP tools are available.
