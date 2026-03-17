---
name: context-graph
description: "Use when storing decision traces, querying past precedents, or implementing learning loops. Load in COMPLETE state or when needing to learn from history. Covers semantic search with Voyage AI embeddings, ChromaDB for cross-platform vector storage, and pattern extraction from history."
keywords: traces, learning, memory, precedent, semantic-search, vector-embeddings, chromadb
---

# Context Graph

Living records of decision traces with semantic search. Find similar past decisions by meaning, not keywords.

## Setup

**MCP Server (recommended):**

The context-graph MCP server provides the same functionality via tools:
- `context_store_trace` - Store decisions with embeddings
- `context_query_traces` - Semantic search
- `context_get_trace` - Get by ID
- `context_update_outcome` - Mark success/failure
- `context_list_traces` - List with pagination
- `context_list_categories` - Category breakdown

Configure in `.claude/mcp.json`:
```json
{
  "mcpServers": {
    "context-graph": {
      "command": "uv",
      "args": ["--directory", "context-graph-mcp", "run", "python", "server.py"],
      "env": {"VOYAGE_API_KEY": "your_key_here"}
    }
  }
}
```

**CLI Scripts (alternative):**

```bash
# 1. Install dependencies
pip install voyageai chromadb

# 2. Set Voyage AI key
export VOYAGE_API_KEY="your_key_here"

# 3. Store/query traces
python scripts/store-trace.py "DECISION"
python scripts/query-traces.py "similar situation"
```

## Instructions

1. **Store trace** after decisions with category + outcome
2. **Query precedents** when facing similar situations
3. **Update outcome** to success/failure after validation

## Quick Commands (MCP)

```
context_store_trace(decision="Chose FastAPI for async", category="framework")
context_query_traces(query="web framework choice", limit=5)
context_update_outcome(trace_id="trace_abc...", outcome="success")
```

## Quick Commands (CLI)

```bash
# Store a decision trace
python scripts/store-trace.py "Chose FastAPI over Flask for async support" --category framework

# Find similar past decisions
python scripts/query-traces.py "web framework selection"

# Query by category
python scripts/query-traces.py "database choice" --category architecture --limit 3

# Output JSON for parsing
python scripts/query-traces.py "error handling" --json
```

## Trace Schema

| Field | Description |
|-------|-------------|
| `id` | Unique trace identifier |
| `timestamp` | When stored |
| `category` | Grouping (framework, api, error, etc.) |
| `decision` | What was decided (text) |
| `outcome` | pending / success / failure |
| `state` | State machine state when decided |
| `feature_id` | Related feature (if any) |
| `embedding` | 1024-dim vector (Voyage AI) |

## Categories

- `framework` - Tech stack choices
- `architecture` - Design patterns, structure
- `api` - Endpoint design, contracts
- `error` - Failure modes, fixes
- `testing` - Test strategies
- `deployment` - Infra decisions

## When to Use

| Situation | Action |
|-----------|--------|
| Made a technical decision | Store trace with category |
| Facing similar problem | Query traces before deciding |
| Session complete | Query category → extract patterns |
| Repeating error | Query traces for that error |
