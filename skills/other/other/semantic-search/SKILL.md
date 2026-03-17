---
name: semantic-search
description: Use when exploring the codebase conceptually — semantic search via claude-context MCP for queries like "how does X work", "find implementation of Y pattern", "where is the architecture for Z", understanding unfamiliar code, finding code by description rather than exact identifier
---

# Semantic Search

Use the `mcp__claude-context__search_code` tool for conceptual, exploratory,
and description-based code search. It searches against an indexed embedding
store built from the codebase, so it finds code by **meaning** rather than
exact text matching.

## When to Use

- **Conceptual queries**: "how does shard allocation work", "where is the gossip protocol implemented"
- **Exploring unfamiliar code**: understanding architecture, finding entry points, tracing data flow
- **Finding by description**: "retry logic with exponential backoff", "error handling for network failures"
- **Cross-cutting concerns**: "all places that validate shard boundaries", "code related to claim lifecycle"
- **Pattern discovery**: "builder pattern usage", "state machine implementations"
- **Architecture understanding**: "how do boundaries interact", "what coordinates shard splits"

## When NOT to Use

- **Exact identifiers** — use Grep: `Grep(pattern="ShardRecord", type="rust")`
- **File names or paths** — use Glob: `Glob(pattern="**/coordination/**/*.rs")`
- **Simple string literals** — use Grep: `Grep(pattern="SHARD_LIMIT")`
- **Broad exploration of directory structure** — use Task with `subagent_type=Explore`

## Decision Matrix

| Signal in query | Tool | Example |
|-----------------|------|---------|
| Exact function/struct/const name | **Grep** | "find `PreallocShardBuilder`" |
| File name or glob pattern | **Glob** | "find all test files in coordination/" |
| "How does X work" | **Semantic search** | "how does shard checkpoint restoration work" |
| "Find code that does Y" | **Semantic search** | "find code that validates range boundaries" |
| "Where is the Z pattern" | **Semantic search** | "where is the builder pattern for bulk operations" |
| Known regex pattern | **Grep** | `fn acquire.*restore` |
| Concept or behavior | **Semantic search** | "claim expiry and reclamation logic" |

## Usage

```
mcp__claude-context__search_code(
  path="/Users/ahrav/Projects/Gossip-rs",
  query="<descriptive natural language query>",
  limit=10
)
```

**Parameters:**
- `path` — **Must be absolute.** Use `/Users/ahrav/Projects/Gossip-rs`.
- `query` — Natural language description of what you are looking for. Be specific.
- `limit` — Number of results (default 10, max 50). Start with 10, increase if needed.
- `extensionFilter` — Optional file extension filter, e.g. `[".rs"]` for Rust only.

## Writing Good Queries

| Weak query | Strong query |
|------------|-------------|
| "shard" | "shard allocation and registration in the coordination engine" |
| "error" | "error handling for resource exhaustion during shard registration" |
| "test" | "simulation test invariant checking for shard consistency" |
| "split" | "split planning and range boundary calculation for bulk operations" |
| "pool" | "byte slab pool allocation and slot lifecycle management" |

Use **domain language** from the project: shards, claims, cursors, checkpoints,
boundaries, coordination, gossip, lineage, manifests, splits, epoch, quorum.

## Combining Tools

For thorough investigation, chain tools:

1. **Semantic search** to find the right area of the codebase
2. **Read** the top results to understand context
3. **Grep** to find all exact references to specific identifiers discovered in step 2
4. **Glob** to map out related files in the same module

## Re-indexing

If the index is stale or search returns no results for queries that should match:

```
mcp__claude-context__index_codebase(
  path="/Users/ahrav/Projects/Gossip-rs",
  force=true
)
```

Check indexing status with `mcp__claude-context__get_indexing_status`.

## DO

- Write queries as natural language descriptions of behavior or architecture
- Use project domain terms (shard, claim, cursor, checkpoint, epoch, etc.)
- Start with semantic search for exploratory work, then narrow with Grep
- Filter by extension when you know the file type

## DON'T

- Use semantic search for exact identifier lookup (Grep is faster and precise)
- Write single-word queries — always provide context
- Forget the absolute path requirement
- Use semantic search when you already know the file — just Read it
